using System;
using BepInEx.Logging;
using UnityEngine;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// First real Subnautica host adapter.
    ///
    /// Vertical slice 001 intentionally models the open ocean only. Ocean.main supplies the real
    /// Subnautica ocean surface. Bases, caves, moonpools, flooded interiors and arbitrary water
    /// volumes will replace this with a per-column spatial sampler after the open-ocean proof.
    /// </summary>
    public sealed class SubnauticaWorldAdapter : IHostWorldAdapter
    {
        private const uint OpenOceanWorldId = 1;

        private readonly ManualLogSource _log;
        private bool _takeover;
        private uint _collisionEpoch = 1;
        private int _lastMinecraftPid;
        private float _lastStatusLog;

        public SubnauticaWorldAdapter(ManualLogSource log, bool takeover)
        {
            _log = log;
            _takeover = takeover;
        }

        public bool Takeover
        {
            get => _takeover;
            set => _takeover = value;
        }

        public bool TryGetFrame(out HostFrame frame)
        {
            frame = default;

            Player player = Player.main;
            if (player == null)
                return false;

            Transform playerTransform = player.transform;
            Vector3 p = playerTransform.position;

            Camera camera = Camera.main;
            Vector3 euler = camera != null
                ? camera.transform.rotation.eulerAngles
                : playerTransform.rotation.eulerAngles;

            frame.Flags = BridgeProtocol.HostInGame;
            frame.WorldId = OpenOceanWorldId;
            frame.CollisionEpoch = _collisionEpoch;
            frame.X = p.x;
            frame.Y = p.y;
            frame.Z = p.z;
            frame.Yaw = NormalizeSignedDegrees(playerTransform.rotation.eulerAngles.y);
            frame.Pitch = NormalizeSignedDegrees(euler.x);
            frame.TeleportSeq = 0;
            frame.ViewportWidth = (uint)Math.Max(1, Screen.width);
            frame.ViewportHeight = (uint)Math.Max(1, Screen.height);
            frame.GameHour = 12.0f;

            return true;
        }

        public bool TryGetWaterSurface(int minecraftX, int minecraftZ, out float surfaceY)
        {
            surfaceY = BridgeProtocol.NoWater;

            if (Player.main == null || Ocean.main == null)
                return false;

            // Phase 0: open-ocean plane. Do not claim an accurate local water volume when the
            // player is in a dry structure. The spatial volume sampler replaces this after the
            // first real swimming/drowning test.
            if (Player.main.IsInside() || Player.main.precursorOutOfWater)
                return false;

            surfaceY = Ocean.main.GetOceanLevel();
            return true;
        }

        public void OnMinecraftState(MinecraftState state)
        {
            if (!state.InWorld || Player.main == null)
                return;

            if (!_takeover)
            {
                if (Time.unscaledTime - _lastStatusLog > 5.0f)
                {
                    _lastStatusLog = Time.unscaledTime;
                    _log.LogInfo(
                        $"Minecraft state: pos=({state.X:F2},{state.Y:F2},{state.Z:F2}) " +
                        $"swimming={state.Swimming} dead={state.Dead} fov={state.Fov:F1}");
                }
                return;
            }

            // Initial calibration assumes Unity/Subnautica and Minecraft share +X/+Y/+Z and
            // meter:block scale 1:1. We intentionally keep takeover opt-in until the calibration
            // pass verifies axis signs and yaw offset in the real game.
            Transform t = Player.main.transform;
            t.position = new Vector3((float)state.X, (float)state.Y, (float)state.Z);
            t.rotation = Quaternion.Euler(0.0f, state.Yaw, 0.0f);
        }

        private static float NormalizeSignedDegrees(float degrees)
        {
            degrees %= 360.0f;
            if (degrees > 180.0f)
                degrees -= 360.0f;
            return degrees;
        }
    }
}
