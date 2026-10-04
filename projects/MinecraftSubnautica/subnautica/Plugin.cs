using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

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
        private SubnauticaInputForwarder _input;
        private SubnauticaItemBridge _items;
        private Harmony _harmony;
        private float _nextErrorLog;
        private bool _haveConnectionState;
        private bool _lastConnected;

        private void Awake()
        {
            _takeover = Config.Bind(
                "Bridge",
                "MinecraftTakeover",
                false,
                "When true, Minecraft's authoritative player state puppets the Subnautica player " +
                "and Subnautica keyboard/mouse input is forwarded into Minecraft. " +
                "Leave false until coordinate calibration is verified.");

            _host = new SubnauticaWorldAdapter(Logger, _takeover.Value);
            _runtime = new BridgeRuntime(_host, BridgeProtocol.DefaultMappingName);
            _input = new SubnauticaInputForwarder();
            _items = new SubnauticaItemBridge(Logger);
            _harmony = new Harmony(PluginGuid);
            _harmony.PatchAll(typeof(Plugin).Assembly);

            Logger.LogInfo($"{PluginName} {PluginVersion} created {BridgeProtocol.DefaultMappingName}");
            Logger.LogInfo(
                "Launch the SkyCraft Minecraft side with " +
                "-Dskycraft.link=Local\\SkyCraft_Subnautica_v1");
        }

        private void Update()
        {
            if (_runtime == null)
                return;

            try
            {
                bool minecraftConnected = _runtime.MinecraftConnected;
                if (!_haveConnectionState || minecraftConnected != _lastConnected)
                {
                    Logger.LogInfo(
                        minecraftConnected
                            ? $"BRIDGE PROOF: Minecraft connected (PID {_runtime.MinecraftPid})."
                            : "BRIDGE PROOF: Minecraft disconnected.");
                    _lastConnected = minecraftConnected;
                    _haveConnectionState = true;
                }

                bool takeoverActive = _takeover.Value && minecraftConnected;

                // Never leave the native Subnautica motor disabled if Minecraft disappears.
                _host.Takeover = takeoverActive;
                _runtime.Tick();
                _items?.Tick();

                bool forwardInput = takeoverActive && Application.isFocused;
                _input.SetActive(forwardInput, _runtime);
                if (forwardInput)
                    _input.Tick(_runtime);
            }
            catch (System.Exception ex)
            {
                // Don't flood BepInEx log every frame if a live-game API changes.
                if (Time.unscaledTime >= _nextErrorLog)
                {
                    _nextErrorLog = Time.unscaledTime + 5.0f;
                    Logger.LogError(ex);
                }
            }
        }

        private void OnDestroy()
        {
            if (_runtime != null)
                _input?.SetActive(false, _runtime);

            _host?.Release();
            _items?.Dispose();
            _items = null;
            _harmony?.UnpatchSelf();
            _harmony = null;
            _runtime?.Dispose();
            _runtime = null;
        }
    }
}
