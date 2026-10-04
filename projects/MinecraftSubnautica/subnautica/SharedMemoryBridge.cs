using System;
using System.Diagnostics;
using System.IO.MemoryMappedFiles;
using System.Runtime.InteropServices;
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
        private readonly object _inputLock = new object();
        private readonly object _collisionLock = new object();
        private readonly object _renderLock = new object();
        private int _overlayFront = 2;
        private byte[] _overlayPixels;
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
                NativeMethods.GetTickCount64());
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

            ulong now = NativeMethods.GetTickCount64();
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

        /// <summary>
        /// Push one event into the existing SkyCraft single-producer/single-consumer input ring.
        /// Returns false when the ring is full; callers should retry state changes on a later frame.
        /// </summary>
        public bool PushInput(ushort type, ushort code = 0, int a = 0, int b = 0, int c = 0)
        {
            ThrowIfDisposed();

            lock (_inputLock)
            {
                long ring = BridgeProtocol.OffInputRing;
                ulong head = _view.ReadUInt64(ring + BridgeProtocol.IRHead);
                ulong tail = _view.ReadUInt64(ring + BridgeProtocol.IRTail);

                if (head - tail >= (ulong)BridgeProtocol.InputRingEntries)
                    return false;

                ulong slot = head & (ulong)(BridgeProtocol.InputRingEntries - 1);
                long e = ring + BridgeProtocol.IRData + (long)slot * BridgeProtocol.InputEventBytes;

                _view.Write(e + 0, type);
                _view.Write(e + 2, code);
                _view.Write(e + 4, a);
                _view.Write(e + 8, b);
                _view.Write(e + 12, c);

                Thread.MemoryBarrier();
                _view.Write(ring + BridgeProtocol.IRHead, head + 1);
                return true;
            }
        }

        public bool PushKey(ushort sdlScancode, bool down)
        {
            return PushInput(BridgeProtocol.InputKey, sdlScancode, down ? 1 : 0);
        }

        public bool PushMouseButton(ushort sdlButton, bool down)
        {
            return PushInput(BridgeProtocol.InputMouseButton, sdlButton, down ? 1 : 0);
        }

        public bool PushScroll(int wheelUnits)
        {
            return PushInput(BridgeProtocol.InputScroll, 0, wheelUnits);
        }

        public bool PushCursor(int x, int y)
        {
            return PushInput(BridgeProtocol.InputCursor, 0, x, y);
        }

        public bool ReleaseAllInput()
        {
            return PushInput(BridgeProtocol.InputReleaseAll);
        }

        public bool OpenMinecraftMenu()
        {
            return PushInput(BridgeProtocol.InputOpenMenu);
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


        public bool TryAcquireOverlayFrame(out OverlayFrame frame)
        {
            ThrowIfDisposed();
            frame = null;

            uint state = _view.ReadUInt32(BridgeProtocol.OffOverlayCtl + BridgeProtocol.OCState);
            if ((state & BridgeProtocol.OverlayDirty) == 0u)
                return false;

            int published = (int)(state & 3u);
            if (published < 0 || published >= BridgeProtocol.OverlaySlots)
                return false;

            // Mirror SkyCraft's exchange semantics closely. This is one reader/one writer; a
            // publication racing this store can only cost one frame, never corrupt the slot.
            _view.Write(
                BridgeProtocol.OffOverlayCtl + BridgeProtocol.OCState,
                (uint)_overlayFront);
            _overlayFront = published;
            Thread.MemoryBarrier();

            long h = BridgeProtocol.OffOverlaySlotHeader
                + _overlayFront * BridgeProtocol.OverlaySlotHeaderBytes;

            int width = _view.ReadInt32(h + BridgeProtocol.OHWidth);
            int height = _view.ReadInt32(h + BridgeProtocol.OHHeight);
            uint flags = _view.ReadUInt32(h + BridgeProtocol.OHFlags);
            ulong frameId = _view.ReadUInt64(h + BridgeProtocol.OHFrameId);

            if (width <= 0 || height <= 0
                || width > BridgeProtocol.MaxOverlayWidth
                || height > BridgeProtocol.MaxOverlayHeight)
                return false;

            long bytesLong = (long)width * height * 4L;
            if (bytesLong <= 0 || bytesLong > int.MaxValue)
                return false;

            if (_overlayPixels == null || _overlayPixels.Length != (int)bytesLong)
                _overlayPixels = new byte[(int)bytesLong];
            byte[] pixels = _overlayPixels;
            long pixelOffset = BridgeProtocol.OffOverlayPixels
                + _overlayFront * BridgeProtocol.OverlaySlotBytes;

            _view.ReadArray(pixelOffset, pixels, 0, pixels.Length);

            frame = new OverlayFrame
            {
                Width = width,
                Height = height,
                BottomUp = (flags & 1u) != 0u,
                FrameId = frameId,
                Pixels = pixels
            };
            return true;
        }

        /// <summary>
        /// Drain Minecraft's render byte ring. Messages are contiguous by protocol contract:
        /// Minecraft emits RenderPad before wrap.
        /// </summary>
        public int DrainRender(Action<uint, byte[]> handler, long maxBytes = 48L << 20)
        {
            ThrowIfDisposed();
            if (handler == null)
                throw new ArgumentNullException("handler");

            lock (_renderLock)
            {
                long ring = BridgeProtocol.OffRenderRing;
                ulong head = _view.ReadUInt64(ring + BridgeProtocol.RRHead);
                ulong tail = _view.ReadUInt64(ring + BridgeProtocol.RRTail);
                long done = 0;
                int messages = 0;

                while (tail < head && done < maxBytes)
                {
                    ulong pos = tail % (ulong)BridgeProtocol.RRDataBytes;
                    long header = ring + BridgeProtocol.RRData + (long)pos;

                    uint type = _view.ReadUInt32(header);
                    uint payloadBytes = _view.ReadUInt32(header + 4);

                    if (type == BridgeProtocol.RenderPad)
                    {
                        tail += (ulong)BridgeProtocol.RRDataBytes - pos;
                        continue;
                    }

                    if (payloadBytes > BridgeProtocol.RRDataBytes - 8)
                    {
                        // Corrupt producer state: drop to head rather than allocating attacker-sized data.
                        tail = head;
                        break;
                    }

                    ulong messageBytes = Align8(8UL + payloadBytes);
                    if (pos + messageBytes > (ulong)BridgeProtocol.RRDataBytes)
                    {
                        // Producer should have emitted RenderPad before wrap.
                        tail = head;
                        break;
                    }

                    byte[] payload = new byte[payloadBytes];
                    if (payloadBytes != 0)
                        _view.ReadArray(header + 8, payload, 0, payload.Length);

                    handler(type, payload);
                    tail += messageBytes;
                    done += (long)messageBytes;
                    messages++;
                }

                Thread.MemoryBarrier();
                _view.Write(ring + BridgeProtocol.RRTail, tail);
                return messages;
            }
        }

        /// <summary>
        /// Host -> Minecraft collision ring writer. Returns false instead of blocking when Minecraft
        /// has not yet consumed enough space.
        /// </summary>
        public bool TryWriteCollision(uint type, byte[] payload)
        {
            ThrowIfDisposed();
            payload = payload ?? Array.Empty<byte>();

            lock (_collisionLock)
            {
                long ring = BridgeProtocol.OffCollisionRing;
                ulong head = _view.ReadUInt64(ring + BridgeProtocol.CRHead);
                ulong tail = _view.ReadUInt64(ring + BridgeProtocol.CRTail);
                ulong payloadBytes = (ulong)payload.LongLength;
                ulong messageBytes = Align8(8UL + payloadBytes);

                if (messageBytes > (ulong)BridgeProtocol.CRDataBytes / 2UL)
                    throw new ArgumentException("Collision message is too large.", "payload");

                ulong used = head - tail;
                ulong pos = head % (ulong)BridgeProtocol.CRDataBytes;
                ulong pad = pos + messageBytes > (ulong)BridgeProtocol.CRDataBytes
                    ? (ulong)BridgeProtocol.CRDataBytes - pos
                    : 0UL;

                if ((ulong)BridgeProtocol.CRDataBytes - used < messageBytes + pad)
                    return false;

                if (pad != 0UL)
                {
                    long padHeader = ring + BridgeProtocol.CRData + (long)pos;
                    _view.Write(padHeader, BridgeProtocol.CollisionPad);
                    _view.Write(padHeader + 4, 0u);
                    head += pad;
                    pos = 0;
                }

                long at = ring + BridgeProtocol.CRData + (long)pos;
                _view.Write(at, type);
                _view.Write(at + 4, (uint)payload.Length);
                if (payload.Length != 0)
                    _view.WriteArray(at + 8, payload, 0, payload.Length);

                Thread.MemoryBarrier();
                _view.Write(ring + BridgeProtocol.CRHead, head + messageBytes);
                return true;
            }
        }

        private static ulong Align8(ulong value)
        {
            return (value + 7UL) & ~7UL;
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

        private static class NativeMethods
        {
            // SkyCraft's Java side also calls kernel32 GetTickCount64, so both processes compare
            // heartbeats on exactly the same monotonic Windows-uptime clock.
            [DllImport("kernel32.dll")]
            internal static extern ulong GetTickCount64();
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
