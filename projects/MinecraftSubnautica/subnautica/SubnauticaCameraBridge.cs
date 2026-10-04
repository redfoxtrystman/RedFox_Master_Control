using System;
using System.Diagnostics;
using System.IO.MemoryMappedFiles;
using System.Runtime.InteropServices;
using System.Threading;
using BepInEx.Logging;
using UnityEngine;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Publishes Subnautica's canonical gameplay camera to Minecraft.
    ///
    /// This follows Universal Modder's working Minecraft/GTA passthrough architecture: the host owns
    /// the final camera, Minecraft renders its world from that exact pose, and the compositor combines
    /// Minecraft colour/depth with the host frame.
    /// </summary>
    public sealed class SubnauticaCameraBridge : IDisposable
    {
        private readonly ManualLogSource _log;
        private readonly MemoryMappedFile _mapping;
        private readonly MemoryMappedViewAccessor _view;
        private bool _disposed;
        private ulong _frame;
        private bool _logged;

        public SubnauticaCameraBridge(ManualLogSource log)
        {
            _log = log ?? throw new ArgumentNullException(nameof(log));
            _mapping = MemoryMappedFile.CreateOrOpen(
                SubnauticaCameraProtocol.MappingName,
                SubnauticaCameraProtocol.MappingBytes,
                MemoryMappedFileAccess.ReadWrite);
            _view = _mapping.CreateViewAccessor(
                0,
                SubnauticaCameraProtocol.MappingBytes,
                MemoryMappedFileAccess.ReadWrite);

            _view.Write(SubnauticaCameraProtocol.MagicOff, SubnauticaCameraProtocol.Magic);
            _view.Write(SubnauticaCameraProtocol.VersionOff, SubnauticaCameraProtocol.Version);
            _view.Write(SubnauticaCameraProtocol.HostPidOff, (uint)Process.GetCurrentProcess().Id);
            PulseHeartbeat();

            _log.LogInfo(
                $"Camera passthrough mapping created: {SubnauticaCameraProtocol.MappingName}");
        }

        public void Tick()
        {
            ThrowIfDisposed();
            PulseHeartbeat();

            Camera camera = MainCamera.camera;
            Player player = Player.main;
            if (camera == null || player == null)
                return;

            Transform cameraTransform = camera.transform;
            Transform playerTransform = player.transform;
            Vector3 cp = cameraTransform.position;
            Vector3 pp = playerTransform.position;
            Vector3 euler = cameraTransform.rotation.eulerAngles;

            // Subnautica's MainCamera is the source of truth. Keep its Unity axes 1:1 with the
            // existing SkyCraft Subnautica coordinate bridge: +X/+Y/+Z, one metre = one block.
            var frame = new SubnauticaCameraFrame
            {
                HostFrame = ++_frame,
                CameraX = cp.x,
                CameraY = cp.y,
                CameraZ = cp.z,
                Yaw = NormalizeSignedDegrees(euler.y),
                Pitch = NormalizeSignedDegrees(euler.x),
                Roll = NormalizeSignedDegrees(euler.z),
                VerticalFov = camera.fieldOfView,
                NearClip = camera.nearClipPlane,
                FarClip = camera.farClipPlane,
                Flags = IsFirstPerson(camera, player) ? SubnauticaCameraProtocol.FirstPerson : 0u,
                ViewportWidth = (uint)Math.Max(1, camera.pixelWidth),
                ViewportHeight = (uint)Math.Max(1, camera.pixelHeight),
                PlayerX = pp.x,
                PlayerY = pp.y,
                PlayerZ = pp.z,
                BodyYaw = NormalizeSignedDegrees(playerTransform.rotation.eulerAngles.y)
            };

            Write(frame);

            if (!_logged)
            {
                _logged = true;
                _log.LogInfo(
                    $"CAMERA PROOF: publishing MainCamera.camera {frame.ViewportWidth}x{frame.ViewportHeight}, " +
                    $"fov={frame.VerticalFov:F2}, near={frame.NearClip:F3}, far={frame.FarClip:F1}.");
            }
        }

        private void Write(SubnauticaCameraFrame frame)
        {
            ulong seq = _view.ReadUInt64(SubnauticaCameraProtocol.SeqOff);
            ulong odd = (seq & 1UL) == 0UL ? seq + 1UL : seq + 2UL;
            _view.Write(SubnauticaCameraProtocol.SeqOff, odd);
            Thread.MemoryBarrier();

            _view.Write(SubnauticaCameraProtocol.HostFrameOff, frame.HostFrame);
            _view.Write(SubnauticaCameraProtocol.CameraXOff, frame.CameraX);
            _view.Write(SubnauticaCameraProtocol.CameraYOff, frame.CameraY);
            _view.Write(SubnauticaCameraProtocol.CameraZOff, frame.CameraZ);
            _view.Write(SubnauticaCameraProtocol.YawOff, frame.Yaw);
            _view.Write(SubnauticaCameraProtocol.PitchOff, frame.Pitch);
            _view.Write(SubnauticaCameraProtocol.RollOff, frame.Roll);
            _view.Write(SubnauticaCameraProtocol.VerticalFovOff, frame.VerticalFov);
            _view.Write(SubnauticaCameraProtocol.NearClipOff, frame.NearClip);
            _view.Write(SubnauticaCameraProtocol.FarClipOff, frame.FarClip);
            _view.Write(SubnauticaCameraProtocol.FlagsOff, frame.Flags);
            _view.Write(SubnauticaCameraProtocol.ViewportWidthOff, frame.ViewportWidth);
            _view.Write(SubnauticaCameraProtocol.ViewportHeightOff, frame.ViewportHeight);
            _view.Write(SubnauticaCameraProtocol.PlayerXOff, frame.PlayerX);
            _view.Write(SubnauticaCameraProtocol.PlayerYOff, frame.PlayerY);
            _view.Write(SubnauticaCameraProtocol.PlayerZOff, frame.PlayerZ);
            _view.Write(SubnauticaCameraProtocol.BodyYawOff, frame.BodyYaw);

            Thread.MemoryBarrier();
            _view.Write(SubnauticaCameraProtocol.SeqOff, odd + 1UL);
        }

        private void PulseHeartbeat()
        {
            _view.Write(SubnauticaCameraProtocol.HeartbeatOff, NativeMethods.GetTickCount64());
        }

        private static bool IsFirstPerson(Camera camera, Player player)
        {
            // Current Subnautica gameplay is first-person in normal play. Treat cameras pulled
            // materially away from the player's head as detached/third-person so Minecraft can
            // render its avatar when another Subnautica camera mode/mod moves the camera.
            Vector3 eye = player.transform.position + Vector3.up * 1.6f;
            return (camera.transform.position - eye).sqrMagnitude < 1.0f;
        }

        private static float NormalizeSignedDegrees(float degrees)
        {
            degrees %= 360.0f;
            if (degrees > 180.0f)
                degrees -= 360.0f;
            return degrees;
        }

        private void ThrowIfDisposed()
        {
            if (_disposed)
                throw new ObjectDisposedException(nameof(SubnauticaCameraBridge));
        }

        public void Dispose()
        {
            if (_disposed)
                return;
            _disposed = true;
            _view.Dispose();
            _mapping.Dispose();
        }

        private static class NativeMethods
        {
            [DllImport("kernel32.dll")]
            internal static extern ulong GetTickCount64();
        }
    }
}
