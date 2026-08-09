using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace BepInEx.Bootstrap
{
    /// <summary>
    /// Minimal BepInEx 5 Chainloader surface used by legacy Planet Crafter mods.
    /// The real loading is performed by RedFox.LegacyBepInEx5Bridge.
    /// </summary>
    public static class Chainloader
    {
        public static Dictionary<string, PluginInfo> PluginInfos { get; } =
            new Dictionary<string, PluginInfo>(StringComparer.InvariantCultureIgnoreCase);

        private static readonly List<BaseUnityPlugin> _plugins = new List<BaseUnityPlugin>();

        [Obsolete("Use PluginInfos instead")]
        public static List<BaseUnityPlugin> Plugins
        {
            get
            {
                lock (_plugins)
                    return _plugins.Where(x => x != null).ToList();
            }
        }

        public static List<string> DependencyErrors { get; } = new List<string>();
        public static GameObject ManagerObject { get; private set; }

        public static void LegacyBridgeSetManagerObject(object manager)
        {
            ManagerObject = (GameObject)manager;
        }

        public static void LegacyBridgeRegister(object instance)
        {
            if (instance is not BaseUnityPlugin plugin)
                return;

            lock (_plugins)
                _plugins.Add(plugin);

            var info = plugin.Info;
            var guid = info?.Metadata?.GUID;
            if (!string.IsNullOrWhiteSpace(guid))
                PluginInfos[guid] = info;
        }
    }
}
