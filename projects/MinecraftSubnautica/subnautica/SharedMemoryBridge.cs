using System;
using System.Diagnostics;
using System.IO.MemoryMappedFiles;
using System.Threading;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Host-side implementation of SkyCraft protocol v11.
    /// Subnautica owns/creates the mapping; the existing SkyCraft Minecraft client opens it.
    /// This file intentionally has no Unity/BepInEx dependency so protocol work can be tested alone.
    /// </summary>
    public sealed class SharedMemoryBridge : IDisposable
    {
        private readonly MemoryMappedFile _mapping;
        private readonly MemoryMappedViewAccessor _view;
        private bool _disposed;

        public string MappingName { get; private set; }

        public SharedMemoryBridge(string mappingName = null)
        {
            MappingName = string.IsNullOrWhiteSpace(mappingName)
                ? BridgeProtocol.DefaultMappingName
                : mappingName;

            _mapping = MemoryMappedFile.CreateOrOpen(
                MappingName,
                BridgeProtocol.MappingBytes,
                MemoryMappedFileAccess.ReadWrite);

            _view = _mapping.CreateViewAccessor(
                0,
                BridgeProtocol.MappingBytes,
                MemoryMappedFileAccess.ReadWrite);

            InitializeHeader();
        }

        private void InitializeHeader()
        {
            _view.Write(BridgeProtocol.OffHeader + BridgeProtocol.HMagic, BridgeProtocol.Magic);
            _view.Write(BridgeProtocol.OffHeader + BridgeProtocol.HVersion, BridgeProtocol.Version);
            _view.Write(BridgeProtocol.OffHeader + BridgeProtocol.HHostPid, (uint)Process.GetCurrentProcess().Id);
            _view.Write(BridgeProtocol.OffHeader + BridgeProtocol.HMinecraftPid, 0u);
            PulseHeartbeat();
        }

        public void PulseHeartbeat()
        {
            ThrowIfDisposed();
            _view.Write(
                BridgeProtocol.OffHeader + BridgeProtocol.HHostHeartbeat,
                unchecked((ulong)Environment.TickCount64));
        }

        public uint MinecraftPid
        {
            get
            {
                ThrowIfDisposed();
                return _view.ReadUInt32(BridgeProtocol.OffHeader + BridgeProtocol.HMinecraftPid);
            }
        }

        public bool MinecraftHeartbeatIsFresh(long timeoutMs = 8000)
        {
            ThrowIfDisposed();
            ulong beat = _view.ReadUInt64(BridgeProtocol.OffHeader + BridgeProtocol.HMinecraftHeartbeat);
            if (beat == 0)
                return false;

            ulong now = unchecked((ulong)Environment.TickCount64);
            return now >= beat && now - beat < (ulong)Math.Max(1, timeoutMs);
        }

        public void WriteHostState(HostState state)
        {
            ThrowIfDisposed();
            long b = BridgeProtocol.OffHostState;

            uint seq = _view.ReadUInt32(b + BridgeProtocol.HSSeq);
            uint odd = (seq & 1u) == 0u ? seq + 1u : seq + 2u;

            _view.Write(b + BridgeProtocol.HSSeq, odd);
            Thread.MemoryBarrier();

            _view.Write(b + BridgeProtocol.HSFlags, state.Flags);
            _view.Write(b + BridgeProtocol.HSWorldId, state.WorldId);
            _view.Write(b + BridgeProtocol.HSCollisionEpoch, state.CollisionEpoch);
            _view.Write(b + BridgeProtocol.HSPosX, state.X);
            _view.Write(b + BridgeProtocol.HSPosY, state.Y);
            _view.Write(b + BridgeProtocol.HSPosZ, state.Z);
            _view.Write(b + BridgeProtocol.HSYaw, state.Yaw);
            _view.Write(b + BridgeProtocol.HSPitch, state.Pitch);
            _view.Write(b + BridgeProtocol.HSTeleportSeq, state.TeleportSeq);
            _view.Write(b + BridgeProtocol.HSViewportW, state.ViewportWidth);
            _view.Write(b + BridgeProtocol.HSViewportH, state.ViewportHeight);
            _view.Write(b + BridgeProtocol.HSGameHour, state.GameHour);

            Thread.MemoryBarrier();
            _view.Write(b + BridgeProtocol.HSSeq, odd + 1u);
        }

        /// <summary>
        /// Writes one 16x16 grid of water surface Y values in Minecraft block coordinates.
        /// Use BridgeProtocol.NoWater for a dry column.
        /// </summary>
        public void WriteWaterGrid(int originX, int originZ, uint worldId, float[] surfaceY)
        {
            ThrowIfDisposed();

            if (surfaceY == null)
                throw new ArgumentNullException("surfaceY");

            int expected = BridgeProtocol.WaterGridSize * BridgeProtocol.WaterGridSize;
            if (surfaceY.Length != expected)
                throw new ArgumentException("Water grid must contain exactly " + expected + " entries.", "surfaceY");

            long b = BridgeProtocol.OffWaterGrid;
            uint seq = _view.ReadUInt32(b + BridgeProtocol.WGSeq);
            uint odd = (seq & 1u) == 0u ? seq + 1u : seq + 2u;

            _view.Write(b + BridgeProtocol.WGSeq, odd);
            Thread.MemoryBarrier();

            _view.Write(b + BridgeProtocol.WGOriginX, originX);
            _view.Write(b + BridgeProtocol.WGOriginZ, originZ);
            _view.Write(b + BridgeProtocol.WGWorldId, worldId);

            for (int i = 0; i < surfaceY.Length; i++)
                _view.Write(b + BridgeProtocol.WGSurface + i * 4L, surfaceY[i]);

            Thread.MemoryBarrier();
            _view.Write(b + BridgeProtocol.WGSeq, odd + 1u);
        }

        public bool TryReadMinecraftState(out MinecraftState state)
        {
            ThrowIfDisposed();
            state = new MinecraftState();

            long b = BridgeProtocol.OffMinecraftState;
            for (int attempt = 0; attempt < 32; attempt++)
            {
                uint seq1 = _view.ReadUInt32(b + BridgeProtocol.MSSeq);
                if ((seq1 & 1u) != 0u)
                {
                    Thread.SpinWait(8);
                    continue;
                }

                MinecraftState snapshot = new MinecraftState();
                snapshot.Flags = _view.ReadUInt32(b + BridgeProtocol.MSFlags);
                snapshot.X = _view.ReadDouble(b + BridgeProtocol.MSX);
                snapshot.Y = _view.ReadDouble(b + BridgeProtocol.MSY);
                snapshot.Z = _view.ReadDouble(b + BridgeProtocol.MSZ);
                snapshot.Yaw = _view.ReadSingle(b + BridgeProtocol.MSYaw);
                snapshot.Pitch = _view.ReadSingle(b + BridgeProtocol.MSPitch);
                snapshot.EyeHeight = _view.ReadSingle(b + BridgeProtocol.MSEyeHeight);
                snapshot.Sensitivity = _view.ReadSingle(b + BridgeProtocol.MSSensitivity);
                snapshot.TeleportAck = _view.ReadUInt32(b + BridgeProtocol.MSTeleportAck);
                snapshot.GuiScale = _view.ReadUInt32(b + BridgeProtocol.MSGuiScale);
                snapshot.FrameCounter = _view.ReadUInt64(b + BridgeProtocol.MSFrameCounter);
                snapshot.Fov = _view.ReadSingle(b + BridgeProtocol.MSFov);
                snapshot.EyeX = _view.ReadDouble(b + BridgeProtocol.MSEyeX);
                snapshot.EyeY = _view.ReadDouble(b + BridgeProtocol.MSEyeY);
                snapshot.EyeZ = _view.ReadDouble(b + BridgeProtocol.MSEyeZ);
                snapshot.CameraMode = _view.ReadInt32(b + BridgeProtocol.MSCameraMode);
                snapshot.CameraDistance = _view.ReadSingle(b + BridgeProtocol.MSCameraDistance);

                Thread.MemoryBarrier();
                uint seq2 = _view.ReadUInt32(b + BridgeProtocol.MSSeq);

                if (seq1 == seq2 && (seq2 & 1u) == 0u)
                {
                    state = snapshot;
                    return true;
                }
            }

            return false;
        }

        public void FillUniformOcean(float waterSurfaceY, int playerBlockX, int playerBlockZ, uint worldId)
        {
            int size = BridgeProtocol.WaterGridSize;
            int originX = playerBlockX - size / 2;
            int originZ = playerBlockZ - size / 2;
            float[] grid = new float[size * size];

            for (int i = 0; i < grid.Length; i++)
                grid[i] = waterSurfaceY;

            WriteWaterGrid(originX, originZ, worldId, grid);
        }

        private void ThrowIfDisposed()
        {
            if (_disposed)
                throw new ObjectDisposedException("SharedMemoryBridge");
        }

        public void Dispose()
        {
            if (_disposed)
                return;

            _disposed = true;
            _view.Dispose();
            _mapping.Dispose();
        }
    }
}
