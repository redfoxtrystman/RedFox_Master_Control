using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Loader;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Unity.IL2CPP;
using Il2CppInterop.Runtime.Injection;

namespace RedFox.PlanetCrafter.LegacyBridge
{
    [BepInPlugin(GUID, NAME, VERSION)]
    public sealed class Plugin : BasePlugin
    {
        private const string GUID = "redfox.planetcrafter.legacybepinex5bridge";
        private const string NAME = "RedFox Planet Crafter Legacy BepInEx 5 Bridge";
        private const string VERSION = "0.1.1";

        private readonly Dictionary<string, string> _legacyAssemblyPaths =
            new(StringComparer.InvariantCultureIgnoreCase);
        private object _managerObject;

        public override void Load()
        {
            var legacyRoot = Path.Combine(Paths.BepInExRootPath, "legacy_plugins");
            Directory.CreateDirectory(legacyRoot);

            Log.LogMessage("Legacy BepInEx 5 bridge starting.");
            Log.LogInfo("Legacy plugin folder: " + legacyRoot);

            BuildAssemblyMap(legacyRoot);
            AssemblyLoadContext.Default.Resolving += ResolveLegacyAssembly;

            try
            {
                _managerObject = CreateManagerObject();
                Chainloader.LegacyBridgeSetManagerObject(_managerObject);
            }
            catch (Exception ex)
            {
                Log.LogError("Could not create the legacy plugin manager GameObject. " + ex);
                return;
            }

            var candidates = DiscoverCandidates(legacyRoot);
            if (candidates.Count == 0)
            {
                Log.LogInfo("No compatible legacy BepInEx 5 plugin classes were discovered.");
                return;
            }

            Log.LogInfo($"Discovered {candidates.Count} legacy plugin class(es). Attempting IL2CPP registration.");
            LoadCandidates(candidates);
        }

        private void BuildAssemblyMap(string legacyRoot)
        {
            foreach (var dll in Directory.EnumerateFiles(legacyRoot, "*.dll", SearchOption.AllDirectories))
            {
                try
                {
                    var name = AssemblyName.GetAssemblyName(dll).Name;
                    if (string.IsNullOrWhiteSpace(name))
                        continue;
                    if (string.Equals(name, "BepInEx", StringComparison.InvariantCultureIgnoreCase))
                        continue;
                    _legacyAssemblyPaths.TryAdd(name, Path.GetFullPath(dll));
                }
                catch (Exception ex)
                {
                    Log.LogWarning($"Ignoring non-.NET or unreadable DLL '{dll}': {ex.Message}");
                }
            }
        }

        private Assembly ResolveLegacyAssembly(AssemblyLoadContext context, AssemblyName requested)
        {
            var loaded = AppDomain.CurrentDomain.GetAssemblies()
                .FirstOrDefault(a => string.Equals(a.GetName().Name, requested.Name,
                    StringComparison.InvariantCultureIgnoreCase));
            if (loaded != null)
                return loaded;

            if (requested.Name != null && _legacyAssemblyPaths.TryGetValue(requested.Name, out var path))
            {
                try
                {
                    return context.LoadFromAssemblyPath(path);
                }
                catch (Exception ex)
                {
                    Log.LogWarning($"Dependency load failed for {requested.Name} from '{path}': {ex.Message}");
                }
            }
            return null;
        }

        private object CreateManagerObject()
        {
            var unityAssembly = AppDomain.CurrentDomain.GetAssemblies()
                .First(a => string.Equals(a.GetName().Name, "UnityEngine.CoreModule",
                    StringComparison.InvariantCultureIgnoreCase));
            var gameObjectType = unityAssembly.GetType("UnityEngine.GameObject", throwOnError: true);
            var objectType = unityAssembly.GetType("UnityEngine.Object", throwOnError: true);
            var hideFlagsType = unityAssembly.GetType("UnityEngine.HideFlags", throwOnError: true);

            var manager = Activator.CreateInstance(gameObjectType, new object[] { "BepInEx_Legacy_Manager" });

            // Planet Crafter's current Unity build is sensitive to visible manager objects.
            // Match BepInEx HideManagerGameObject behavior for the bridge's own manager too.
            var hideFlagsProperty = gameObjectType.GetProperty("hideFlags",
                BindingFlags.Instance | BindingFlags.Public);
            if (hideFlagsProperty != null)
            {
                var hideAndDontSave = Enum.Parse(hideFlagsType, "HideAndDontSave");
                hideFlagsProperty.SetValue(manager, hideAndDontSave);
            }

            var dontDestroy = objectType.GetMethods(BindingFlags.Public | BindingFlags.Static)
                .FirstOrDefault(m => m.Name == "DontDestroyOnLoad" && m.GetParameters().Length == 1);
            dontDestroy?.Invoke(null, new[] { manager });
            return manager;
        }

        private List<Candidate> DiscoverCandidates(string legacyRoot)
        {
            var result = new List<Candidate>();
            foreach (var dll in Directory.EnumerateFiles(legacyRoot, "*.dll", SearchOption.AllDirectories)
                         .OrderBy(x => x, StringComparer.InvariantCultureIgnoreCase))
            {
                var fileName = Path.GetFileName(dll);
                if (fileName.Equals("MiscModEnabler.dll", StringComparison.InvariantCultureIgnoreCase))
                {
                    Log.LogInfo("Skipping legacy MiscModEnabler.dll: Game Pass already uses HideManagerGameObject=true; the original also references Steam/GOG-only assemblies.");
                    continue;
                }

                Assembly assembly;
                try
                {
                    assembly = AssemblyLoadContext.Default.LoadFromAssemblyPath(Path.GetFullPath(dll));
                }
                catch (Exception ex)
                {
                    Log.LogError($"Could not load legacy assembly '{dll}': {ex}");
                    continue;
                }

                foreach (var type in GetLoadableTypes(assembly))
                {
                    if (type == null || type.IsAbstract || !typeof(BaseUnityPlugin).IsAssignableFrom(type))
                        continue;

                    var metadata = type.GetCustomAttributes(typeof(BepInPlugin), true)
                        .OfType<BepInPlugin>()
                        .FirstOrDefault();
                    if (metadata == null)
                    {
                        Log.LogWarning($"Skipping {type.FullName}: no BepInPlugin attribute.");
                        continue;
                    }

                    var deps = type.GetCustomAttributes(typeof(BepInDependency), true)
                        .OfType<BepInDependency>()
                        .ToArray();
                    result.Add(new Candidate(dll, type, metadata, deps));
                }
            }
            return result;
        }

        private IEnumerable<Type> GetLoadableTypes(Assembly assembly)
        {
            try
            {
                return assembly.GetTypes();
            }
            catch (ReflectionTypeLoadException ex)
            {
                foreach (var loaderError in ex.LoaderExceptions.Where(x => x != null))
                    Log.LogWarning($"Type load warning in {assembly.GetName().Name}: {loaderError.Message}");
                return ex.Types.Where(x => x != null);
            }
        }

        private void LoadCandidates(List<Candidate> candidates)
        {
            var pending = new List<Candidate>(candidates);
            var knownGuids = new HashSet<string>(candidates.Select(c => c.Metadata.GUID),
                StringComparer.InvariantCultureIgnoreCase);
            var loadedGuids = new HashSet<string>(Chainloader.PluginInfos.Keys,
                StringComparer.InvariantCultureIgnoreCase);

            bool progress;
            do
            {
                progress = false;
                for (var i = pending.Count - 1; i >= 0; i--)
                {
                    var candidate = pending[i];
                    var internalHardDeps = candidate.Dependencies
                        .Where(d => d.Flags == BepInDependency.DependencyFlags.HardDependency &&
                                    knownGuids.Contains(d.DependencyGUID))
                        .Select(d => d.DependencyGUID)
                        .ToArray();
                    if (internalHardDeps.Any(d => !loadedGuids.Contains(d)))
                        continue;

                    pending.RemoveAt(i);
                    progress = true;
                    if (TryLoad(candidate))
                        loadedGuids.Add(candidate.Metadata.GUID);
                }
            } while (progress && pending.Count > 0);

            foreach (var candidate in pending)
            {
                var message = $"Could not order/load [{candidate.Metadata.Name} {candidate.Metadata.Version}] because a hard legacy dependency did not load.";
                Chainloader.DependencyErrors.Add(message);
                Log.LogError(message);
            }
        }

        private bool TryLoad(Candidate candidate)
        {
            try
            {
                Log.LogInfo($"Registering legacy plugin [{candidate.Metadata.Name} {candidate.Metadata.Version}] from {Path.GetFileName(candidate.Path)}");
                ClassInjector.RegisterTypeInIl2Cpp(candidate.Type,
                    new RegisterTypeOptions { LogSuccess = false });

                var managerType = _managerObject.GetType();
                var addComponent = managerType.GetMethods(BindingFlags.Instance | BindingFlags.Public)
                    .First(m => m.Name == "AddComponent" && m.IsGenericMethodDefinition &&
                                m.GetParameters().Length == 0);
                var instance = addComponent.MakeGenericMethod(candidate.Type).Invoke(_managerObject, null);
                if (instance == null)
                    throw new InvalidOperationException("Unity returned a null component instance.");

                Chainloader.LegacyBridgeRegister(instance);
                Log.LogMessage($"LEGACY PORT ACTIVE: {candidate.Metadata.Name} {candidate.Metadata.Version}");
                return true;
            }
            catch (Exception ex)
            {
                var root = ex is TargetInvocationException tie && tie.InnerException != null ? tie.InnerException : ex;
                Log.LogError($"Legacy port failed for [{candidate.Metadata.Name} {candidate.Metadata.Version}]: {root}");
                return false;
            }
        }

        private sealed record Candidate(string Path, Type Type, BepInPlugin Metadata, BepInDependency[] Dependencies);
    }
}
