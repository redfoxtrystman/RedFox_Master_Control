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
        private float _lastStatusLog;
        private PlayerController _disabledController;
        private bool _haveMinecraftFlags;
        private bool _lastSwimming;
        private bool _lastDead;

        public SubnauticaWorldAdapter(ManualLogSource log, bool takeover)
        {
            _log = log;
            _takeover = takeover;
        }

        /// <summary>
        /// True only while Minecraft is connected and is allowed to own the on-foot player.
        /// Changing this immediately hands movement authority between Subnautica and Minecraft.
        /// </summary>
        public bool Takeover
        {
            get => _takeover;
            set
            {
                _takeover = value;
                SynchronizeMovementAuthority();
            }
        }

        public bool TryGetFrame(out HostFrame frame)
        {
            frame = default;

            Player player = Player.main;
            if (player == null)
            {
                ReleaseNativeController();
                return false;
            }

            // Player objects/controllers can be recreated around loads and respawns.
            SynchronizeMovementAuthority();

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

            if (Player.main == null)
                return false;

            // Phase 0: open-ocean plane. Do not claim an accurate local water volume when the
            // player is in a dry structure. The spatial volume sampler replaces this after the
            // first real swimming/drowning test.
            if (Player.main.IsInside() || Player.main.precursorOutOfWater)
                return false;

            surfaceY = Ocean.GetOceanLevel();
            return true;
        }

        public void OnMinecraftState(MinecraftState state)
        {
            if (!state.InWorld || Player.main == null)
                return;

            if (!_haveMinecraftFlags || state.Swimming != _lastSwimming)
            {
                _log.LogInfo(
                    $"BRIDGE PROOF: Minecraft swimming={state.Swimming} " +
                    $"at ({state.X:F2},{state.Y:F2},{state.Z:F2}).");
                _lastSwimming = state.Swimming;
            }

            if (!_haveMinecraftFlags || state.Dead != _lastDead)
            {
                _log.LogInfo($"BRIDGE PROOF: Minecraft dead={state.Dead}.");
                _lastDead = state.Dead;
            }

            _haveMinecraftFlags = true;

            if (!_takeover || _disabledController == null)
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

        public void Release()
        {
            _takeover = false;
            ReleaseNativeController();
        }

        private void SynchronizeMovementAuthority()
        {
            Player player = Player.main;

            bool canOwnOnFootPlayer =
                _takeover &&
                player != null &&
                !player.cinematicModeActive &&
                player.GetMode() == Player.Mode.Normal;

            PlayerController current = canOwnOnFootPlayer ? player.playerController : null;

            if (_disabledController != null && _disabledController != current)
                ReleaseNativeController();

            if (current != null && _disabledController == null)
            {
                current.SetEnabled(false);
                _disabledController = current;
                _log.LogInfo("Minecraft takeover: Subnautica PlayerController disabled; Minecraft owns movement.");
            }
            else if (!canOwnOnFootPlayer)
            {
                ReleaseNativeController();
            }
        }

        private void ReleaseNativeController()
        {
            if (_disabledController == null)
                return;

            try
            {
                _disabledController.SetEnabled(true);
            }
            catch (Exception ex)
            {
                _log.LogWarning($"Could not re-enable Subnautica PlayerController during takeover release: {ex.Message}");
            }

            _disabledController = null;
            _log.LogInfo("Minecraft takeover released: Subnautica PlayerController restored.");
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
