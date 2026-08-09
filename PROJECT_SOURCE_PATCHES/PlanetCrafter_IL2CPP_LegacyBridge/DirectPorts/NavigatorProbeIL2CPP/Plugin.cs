using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Unity.IL2CPP;
using UnityEngine;

namespace RedFox.Navigator.GamePass.IL2CPP.Probe;

[BepInPlugin(GUID, NAME, VERSION)]
public sealed class Plugin : BasePlugin
{
    public const string GUID = "redfox.planetcrafter.gamepass.navigatorprobe";
    public const string NAME = "NAVIGATOR - Game Pass IL2CPP Compatibility Probe";
    public const string VERSION = "0.1.0";

    private readonly List<string> _report = new();

    public override void Load()
    {
        Report("NAVIGATOR Game Pass IL2CPP probe starting.");
        Report("This is a compatibility probe, not the full ship port.");
        ProbeGameApi();
        ProbeAssetBundle();
        WriteReport();
        Log.LogMessage("NAVIGATOR PROBE COMPLETE - see BepInEx/NavigatorGamePassProbe.txt");
    }

    private void ProbeGameApi()
    {
        Report("--- GAME API ---");
        var required = new[]
        {
            "SpaceCraft.PlayerMainController",
            "SpaceCraft.PlayersManager",
            "SpaceCraft.WorldObjectsHandler",
            "SpaceCraft.WorldObject",
            "SpaceCraft.Group",
            "SpaceCraft.GroupsHandler",
            "SpaceCraft.InventoriesHandler",
            "SpaceCraft.PlayerInputDispatcher",
            "SpaceCraft.WindowsHandler",
            "SpaceCraft.MapDisplayerHandler",
            "SpaceCraft.MapMarker",
            "SpaceCraft.PlanetLoader",
            "SpaceCraft.PlanetData",
            "SpaceCraft.VisualsResourcesHandler",
            "SpaceCraft.GamepadConfig"
        };

        foreach (var name in required)
        {
            var t = FindType(name);
            Report((t != null ? "FOUND   " : "MISSING ") + name);
        }

        ProbeMethod("SpaceCraft.PlayerInputDispatcher", "OnShowMapDispatcher");
        ProbeMethod("SpaceCraft.PlayerInputDispatcher", "OnEscapeDispatcher");
        ProbeMethod("SpaceCraft.WindowsHandler", "GetHasUiOpen");
        ProbeMethod("SpaceCraft.PlayersManager", "GetActivePlayerController");
        ProbeMethod("SpaceCraft.PlanetLoader", "GetCurrentPlanetData");
    }

    private void ProbeMethod(string typeName, string methodName)
    {
        var t = FindType(typeName);
        if (t == null)
        {
            Report($"METHOD  ? {typeName}.{methodName} (type missing)");
            return;
        }
        var methods = t.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static)
            .Where(m => m.Name == methodName).ToArray();
        if (methods.Length == 0)
        {
            Report($"METHOD  MISSING {typeName}.{methodName}");
            return;
        }
        foreach (var m in methods)
            Report($"METHOD  FOUND {typeName}.{methodName}({string.Join(", ", m.GetParameters().Select(p => p.ParameterType.Name))})");
    }

    private void ProbeAssetBundle()
    {
        Report("--- ASSET BUNDLE ---");
        var pluginDir = Path.GetDirectoryName(GetType().Assembly.Location) ?? Paths.PluginPath;
        var bundlePath = Path.Combine(pluginDir, "akorn_ship");
        Report("Bundle path: " + bundlePath);
        if (!File.Exists(bundlePath))
        {
            Report("BUNDLE  MISSING akorn_ship");
            return;
        }

        try
        {
            var assetBundleType = FindType("UnityEngine.AssetBundle");
            if (assetBundleType == null)
            {
                Report("BUNDLE  FAIL UnityEngine.AssetBundle type not found");
                return;
            }

            var loadFromFile = assetBundleType.GetMethods(BindingFlags.Public | BindingFlags.Static)
                .FirstOrDefault(m => m.Name == "LoadFromFile" && m.GetParameters().Length == 1 && m.GetParameters()[0].ParameterType == typeof(string));
            if (loadFromFile == null)
            {
                Report("BUNDLE  FAIL AssetBundle.LoadFromFile(string) not found");
                return;
            }

            var bundle = loadFromFile.Invoke(null, new object[] { bundlePath });
            if (bundle == null)
            {
                Report("BUNDLE  FAIL Unity returned null. The bundle may target an incompatible Unity version/platform.");
                return;
            }
            Report("BUNDLE  LOADED successfully");

            var getNames = assetBundleType.GetMethods(BindingFlags.Public | BindingFlags.Instance)
                .FirstOrDefault(m => m.Name == "GetAllAssetNames" && m.GetParameters().Length == 0);
            if (getNames != null)
            {
                var names = getNames.Invoke(bundle, null);
                var list = EnumerateStrings(names).Take(100).ToArray();
                Report("ASSETS  " + (list.Length == 0 ? "<none returned>" : string.Join(" | ", list)));
            }

            var goType = FindType("UnityEngine.GameObject");
            if (goType == null)
            {
                Report("PREFAB  ? GameObject type not found");
                return;
            }

            var loadAsset = assetBundleType.GetMethods(BindingFlags.Public | BindingFlags.Instance)
                .FirstOrDefault(m => m.Name == "LoadAsset" && !m.IsGenericMethod &&
                                     m.GetParameters().Length == 2 &&
                                     m.GetParameters()[0].ParameterType == typeof(string) &&
                                     m.GetParameters()[1].ParameterType == typeof(Type));
            if (loadAsset == null)
            {
                Report("PREFAB  ? AssetBundle.LoadAsset(string, Type) overload not found");
                return;
            }

            var prefab = loadAsset.Invoke(bundle, new object[] { "Akorn", goType });
            Report(prefab != null
                ? "PREFAB  FOUND 'Akorn' - hull asset is readable on this Game Pass Unity build"
                : "PREFAB  MISSING 'Akorn' - bundle loaded, but the expected hull prefab was not returned");
        }
        catch (Exception ex)
        {
            Report("BUNDLE  EXCEPTION " + Root(ex));
        }
    }

    private Type? FindType(string fullName)
    {
        foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
        {
            try
            {
                var t = asm.GetType(fullName, false);
                if (t != null) return t;
            }
            catch { }
        }
        return null;
    }

    private static IEnumerable<string> EnumerateStrings(object? source)
    {
        if (source == null) yield break;
        if (source is IEnumerable enumerable)
        {
            foreach (var item in enumerable)
                if (item != null) yield return item.ToString() ?? string.Empty;
            yield break;
        }

        var t = source.GetType();
        var countMember = (MemberInfo?)t.GetProperty("Length") ?? t.GetProperty("Count") ?? t.GetField("Length") ?? t.GetField("Count");
        object? countValue = countMember switch
        {
            PropertyInfo p => p.GetValue(source),
            FieldInfo f => f.GetValue(source),
            _ => null
        };
        var count = 0;
        try { if (countValue != null) count = Convert.ToInt32(countValue); } catch { }
        var indexer = t.GetProperties(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
            .FirstOrDefault(p => p.GetIndexParameters().Length == 1);
        if (indexer == null) yield break;
        for (var i = 0; i < count; i++)
        {
            object? item = null;
            try { item = indexer.GetValue(source, new object[] { i }); } catch { }
            if (item != null) yield return item.ToString() ?? string.Empty;
        }
    }

    private void Report(string line)
    {
        _report.Add(line);
        Log.LogInfo("[NAV-PROBE] " + line);
    }

    private void WriteReport()
    {
        try
        {
            var path = Path.Combine(Paths.BepInExRootPath, "NavigatorGamePassProbe.txt");
            File.WriteAllLines(path, _report);
        }
        catch (Exception ex)
        {
            Log.LogWarning("Could not write NavigatorGamePassProbe.txt: " + ex.Message);
        }
    }

    private static Exception Root(Exception ex) => ex is TargetInvocationException tie && tie.InnerException != null ? tie.InnerException : ex;
}
