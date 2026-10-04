using System;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Game-neutral runtime loop between a host adapter and SkyCraft shared memory.
    /// Subnautica-specific code implements IHostWorldAdapter; protocol/state timing stays here.
    /// </summary>
    public sealed class BridgeRuntime : IDisposable
    {
        private readonly SharedMemoryBridge _bridge;
        private readonly IHostWorldAdapter _host;
        private readonly float[] _water = new float[BridgeProtocol.WaterGridSize * BridgeProtocol.WaterGridSize];

        public BridgeRuntime(IHostWorldAdapter host, string mappingName = null)
        {
            _host = host ?? throw new ArgumentNullException(nameof(host));
            _bridge = new SharedMemoryBridge(mappingName);
        }

        public uint MinecraftPid => _bridge.MinecraftPid;
        public bool MinecraftConnected => _bridge.MinecraftHeartbeatIsFresh();

        public bool PushKey(ushort sdlScancode, bool down) => _bridge.PushKey(sdlScancode, down);
        public bool PushMouseButton(ushort sdlButton, bool down) => _bridge.PushMouseButton(sdlButton, down);
        public bool PushScroll(int wheelUnits) => _bridge.PushScroll(wheelUnits);
        public bool PushCursor(int x, int y) => _bridge.PushCursor(x, y);
        public bool ReleaseAllInput() => _bridge.ReleaseAllInput();
        public bool OpenMinecraftMenu() => _bridge.OpenMinecraftMenu();
        public VisualDiagnostics ReadVisualDiagnostics() => _bridge.ReadVisualDiagnostics();
        public bool TryAcquireOverlayFrame(out OverlayFrame frame) => _bridge.TryAcquireOverlayFrame(out frame);
        public int DrainRender(Action<uint, byte[]> handler, long maxBytes = 48L << 20) => _bridge.DrainRender(handler, maxBytes);
        public bool TryWriteCollision(uint type, byte[] payload) => _bridge.TryWriteCollision(type, payload);

        public void Tick()
        {
            _bridge.PulseHeartbeat();

            if (!_host.TryGetFrame(out HostFrame frame))
                return;

            _bridge.WriteHostState(new HostState
            {
                Flags = frame.Flags,
                WorldId = frame.WorldId,
                CollisionEpoch = frame.CollisionEpoch,
                X = frame.X,
                Y = frame.Y,
                Z = frame.Z,
                Yaw = frame.Yaw,
                Pitch = frame.Pitch,
                TeleportSeq = frame.TeleportSeq,
                ViewportWidth = frame.ViewportWidth,
                ViewportHeight = frame.ViewportHeight,
                GameHour = frame.GameHour
            });

            int size = BridgeProtocol.WaterGridSize;
            int playerX = FloorBlock(frame.X);
            int playerZ = FloorBlock(frame.Z);
            int originX = playerX - size / 2;
            int originZ = playerZ - size / 2;

            for (int z = 0; z < size; z++)
            {
                for (int x = 0; x < size; x++)
                {
                    int blockX = originX + x;
                    int blockZ = originZ + z;
                    _water[z * size + x] = _host.TryGetWaterSurface(blockX, blockZ, out float surface)
                        ? surface
                        : BridgeProtocol.NoWater;
                }
            }

            _bridge.WriteWaterGrid(originX, originZ, frame.WorldId, _water);

            if (_bridge.TryReadMinecraftState(out MinecraftState minecraft))
                _host.OnMinecraftState(minecraft);
        }

        private static int FloorBlock(double value)
        {
            return (int)Math.Floor(value);
        }

        public void Dispose()
        {
            _bridge.Dispose();
        }
    }

    public interface IHostWorldAdapter
    {
        bool TryGetFrame(out HostFrame frame);

        /// <summary>
        /// Return a Minecraft-space water surface Y for this X/Z column.
        /// False means Minecraft should see no host-provided water in the column.
        /// </summary>
        bool TryGetWaterSurface(int minecraftX, int minecraftZ, out float surfaceY);

        /// <summary>
        /// Called after a consistent Minecraft state snapshot is available.
        /// The host decides whether it is observing, puppeting, or blending.
        /// </summary>
        void OnMinecraftState(MinecraftState state);
    }

    public struct HostFrame
    {
        public uint Flags;
        public uint WorldId;
        public uint CollisionEpoch;
        public double X;
        public double Y;
        public double Z;
        public float Yaw;
        public float Pitch;
        public uint TeleportSeq;
        public uint ViewportWidth;
        public uint ViewportHeight;
        public float GameHour;
    }
}
