using BepInEx;
using BepInEx.Configuration;

namespace MinecraftSubnautica.Bridge
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    [BepInDependency("com.snmodding.nautilus")]
    [BepInProcess("Subnautica.exe")]
    public sealed class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "com.redfox.minecraftsubnautica.bridge";
        public const string PluginName = "Minecraft Subnautica Bridge";
        public const string PluginVersion = "0.0.1";

        private ConfigEntry<bool> _takeover;
        private BridgeRuntime _runtime;
        private SubnauticaWorldAdapter _host;
        private float _nextErrorLog;

        private void Awake()
        {
            _takeover = Config.Bind(
                "Bridge",
                "MinecraftTakeover",
                false,
                "When true, Minecraft's authoritative player state puppets the Subnautica player. " +
                "Leave false until coordinate calibration is verified.");

            _host = new SubnauticaWorldAdapter(Logger, _takeover.Value);
            _runtime = new BridgeRuntime(_host, BridgeProtocol.DefaultMappingName);

            Logger.LogInfo($"{PluginName} {PluginVersion} created {BridgeProtocol.DefaultMappingName}");
            Logger.LogInfo(
                "Launch the SkyCraft Minecraft side with " +
                "-Dskycraft.link=Local\\SkyCraft_Subnautica_v1");
        }

        private void Update()
        {
            if (_runtime == null)
                return;

            _host.Takeover = _takeover.Value;

            try
            {
                _runtime.Tick();
            }
            catch (System.Exception ex)
            {
                // Don't flood BepInEx log every frame if a live-game API changes.
                if (UnityEngine.Time.unscaledTime >= _nextErrorLog)
                {
                    _nextErrorLog = UnityEngine.Time.unscaledTime + 5.0f;
                    Logger.LogError(ex);
                }
            }
        }

        private void OnDestroy()
        {
            _runtime?.Dispose();
            _runtime = null;
        }
    }
}
