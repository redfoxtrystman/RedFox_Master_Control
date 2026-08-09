using System;
using System.IO;
using System.Runtime.CompilerServices;
using BepInEx;
using BepInEx.Logging;

namespace RedFox.PlanetCrafter.LegacyBridge
{
    internal static class BridgeReportBootstrap
    {
        private static BridgeReportListener _listener;

        [ModuleInitializer]
        internal static void Initialize()
        {
            try
            {
                var reportPath = Path.Combine(Paths.BepInExRootPath, "LegacyBridgeReport.txt");
                File.WriteAllText(reportPath,
                    "RedFox Planet Crafter Game Pass - Legacy BepInEx 5 Bridge diagnostic report\r\n" +
                    "Started: " + DateTime.Now.ToString("O") + "\r\n" +
                    "BepInEx root: " + Paths.BepInExRootPath + "\r\n" +
                    "----------------------------------------------------------------\r\n");
                _listener = new BridgeReportListener(reportPath);
                Logger.Listeners.Add(_listener);
            }
            catch
            {
                // Never allow diagnostics to prevent the bridge from starting.
            }
        }
    }

    internal sealed class BridgeReportListener : ILogListener
    {
        private readonly string _path;
        private readonly object _gate = new object();

        internal BridgeReportListener(string path) => _path = path;

        public LogLevel LogLevelFilter => LogLevel.All;

        public void LogEvent(object sender, LogEventArgs eventArgs)
        {
            try
            {
                var source = eventArgs.Source?.SourceName ?? string.Empty;
                if (!source.Equals("RedFox Planet Crafter Legacy BepInEx 5 Bridge", StringComparison.OrdinalIgnoreCase))
                    return;

                lock (_gate)
                {
                    File.AppendAllText(_path,
                        $"[{DateTime.Now:HH:mm:ss.fff}] [{eventArgs.Level}] {eventArgs.Data}{Environment.NewLine}");
                }
            }
            catch
            {
                // Diagnostics must remain non-fatal.
            }
        }

        public void Dispose() { }
    }
}
