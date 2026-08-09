using System;
using System.IO;
using System.Linq;
using System.Reflection;
using BepInEx.Configuration;
using BepInEx.Logging;
using UnityEngine;

namespace BepInEx
{
    /// <summary>
    /// Compatibility implementation of the BepInEx 5 BaseUnityPlugin type.
    /// It intentionally lives in an assembly named BepInEx.dll so legacy plugins
    /// can bind to it while running under BepInEx 6 IL2CPP.
    /// </summary>
    public abstract class BaseUnityPlugin : MonoBehaviour
    {
        protected BaseUnityPlugin()
        {
            var type = GetType();
            var metadata = type.GetCustomAttributes(typeof(BepInPlugin), true)
                               .OfType<BepInPlugin>()
                               .FirstOrDefault();
            if (metadata == null)
                throw new InvalidOperationException("Can't create an instance of " + type.FullName +
                                                    " because it inherits from BaseUnityPlugin and the BepInPlugin attribute is missing.");

            Logger = BepInEx.Logging.Logger.CreateLogSource(metadata.Name);
            Config = new ConfigFile(Path.Combine(Paths.ConfigPath, metadata.GUID + ".cfg"), false, metadata);
            Info = BuildPluginInfo(type, metadata, this);
        }

        public PluginInfo Info { get; }
        protected ManualLogSource Logger { get; }
        public ConfigFile Config { get; }

        private static PluginInfo BuildPluginInfo(Type type, BepInPlugin metadata, object instance)
        {
            var info = new PluginInfo();
            Set(info, "Metadata", metadata);
            Set(info, "Instance", instance);
            Set(info, "Dependencies", type.GetCustomAttributes(typeof(BepInDependency), true).OfType<BepInDependency>().ToArray());
            Set(info, "Processes", type.GetCustomAttributes(typeof(BepInProcess), true).OfType<BepInProcess>().ToArray());
            Set(info, "Incompatibilities", type.GetCustomAttributes(typeof(BepInIncompatibility), true).OfType<BepInIncompatibility>().ToArray());
            Set(info, "Location", type.Assembly.Location);
            Set(info, "TypeName", type.FullName);
            return info;
        }

        private static void Set(PluginInfo info, string propertyName, object value)
        {
            var p = typeof(PluginInfo).GetProperty(propertyName,
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            p?.SetValue(info, value);
        }
    }
}
