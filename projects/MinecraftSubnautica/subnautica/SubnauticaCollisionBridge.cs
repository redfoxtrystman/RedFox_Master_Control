using System;
using System.Collections.Generic;
using System.IO;
using BepInEx.Logging;
using UnityEngine;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// First Subnautica -> Minecraft physical-world bridge.
    ///
    /// Samples Unity's real collision around the player into SkyCraft's existing 8x8x8 region
    /// protocol. Phase 1 deliberately sends block-resolution occupancy (an intersecting Unity
    /// collider fills the Minecraft block) so terrain, reefs, trees/plants with collision,
    /// wrecks and bases become solid immediately. Later passes can refine intersected blocks to
    /// 1/8-block occupancy and exact triangles without changing the protocol.
    /// </summary>
    public sealed class SubnauticaCollisionBridge
    {
        private const int RegionSize = 8;
        private const uint CollisionEpoch = 1;

        private readonly ManualLogSource _log;
        private readonly BridgeRuntime _runtime;
        private readonly Queue<Vector3Int> _pending = new Queue<Vector3Int>();
        private readonly Collider[] _hits = new Collider[48];

        private Vector3Int _lastCenter = new Vector3Int(int.MinValue, int.MinValue, int.MinValue);
        private float _nextRefresh;
        private bool _initialized;
        private bool _loggedFirst;

        public SubnauticaCollisionBridge(ManualLogSource log, BridgeRuntime runtime)
        {
            _log = log ?? throw new ArgumentNullException(nameof(log));
            _runtime = runtime ?? throw new ArgumentNullException(nameof(runtime));
        }

        public void Tick(bool minecraftConnected)
        {
            if (!minecraftConnected || Player.main == null)
            {
                _initialized = false;
                _pending.Clear();
                _lastCenter = new Vector3Int(int.MinValue, int.MinValue, int.MinValue);
                return;
            }

            if (!_initialized)
            {
                byte[] clear = BitConverter.GetBytes(CollisionEpoch);
                if (!_runtime.TryWriteCollision(BridgeProtocol.CollisionClear, clear))
                    return;

                _initialized = true;
                _nextRefresh = 0f;
                _log.LogInfo("COLLISION PROOF: initialized Subnautica -> Minecraft collision stream.");
            }

            Vector3 p = Player.main.transform.position;
            Vector3Int center = new Vector3Int(
                FloorDiv(Mathf.FloorToInt(p.x), RegionSize),
                FloorDiv(Mathf.FloorToInt(p.y), RegionSize),
                FloorDiv(Mathf.FloorToInt(p.z), RegionSize));

            if (center != _lastCenter || Time.unscaledTime >= _nextRefresh)
            {
                _lastCenter = center;
                _nextRefresh = Time.unscaledTime + 2.0f;
                ScheduleNeighborhood(center);
            }

            // One 8x8x8 region per frame keeps Physics queries bounded and progressively fills
            // the 24-block neighborhood in every direction.
            if (_pending.Count != 0)
            {
                Vector3Int region = _pending.Dequeue();
                byte[] payload = SampleRegion(region, out int solidBlocks);
                if (!_runtime.TryWriteCollision(BridgeProtocol.CollisionRegion, payload))
                {
                    _pending.Enqueue(region);
                    return;
                }

                if (!_loggedFirst)
                {
                    _loggedFirst = true;
                    _log.LogInfo(
                        $"COLLISION PROOF: sent first Unity region ({region.x},{region.y},{region.z}), " +
                        $"{solidBlocks} solid Minecraft-space blocks.");
                }
            }
        }

        private void ScheduleNeighborhood(Vector3Int center)
        {
            _pending.Clear();

            // Nearest regions first so ground/walls around the player arrive before far scenery.
            List<Vector3Int> regions = new List<Vector3Int>(27);
            for (int dy = -1; dy <= 1; dy++)
            {
                for (int dz = -1; dz <= 1; dz++)
                {
                    for (int dx = -1; dx <= 1; dx++)
                        regions.Add(new Vector3Int(center.x + dx, center.y + dy, center.z + dz));
                }
            }

            regions.Sort((a, b) =>
            {
                int da = Math.Abs(a.x - center.x) + Math.Abs(a.y - center.y) + Math.Abs(a.z - center.z);
                int db = Math.Abs(b.x - center.x) + Math.Abs(b.y - center.y) + Math.Abs(b.z - center.z);
                return da.CompareTo(db);
            });

            foreach (Vector3Int region in regions)
                _pending.Enqueue(region);
        }

        private byte[] SampleRegion(Vector3Int region, out int solidBlocks)
        {
            int minX = region.x * RegionSize;
            int minY = region.y * RegionSize;
            int minZ = region.z * RegionSize;
            int maxX = minX + RegionSize - 1;
            int maxY = minY + RegionSize - 1;
            int maxZ = minZ + RegionSize - 1;

            List<BlockOccupancy> blocks = new List<BlockOccupancy>(128);

            for (int by = 0; by < RegionSize; by++)
            {
                for (int bz = 0; bz < RegionSize; bz++)
                {
                    for (int bx = 0; bx < RegionSize; bx++)
                    {
                        int x = minX + bx;
                        int y = minY + by;
                        int z = minZ + bz;

                        if (!IsSolidCell(x, y, z))
                            continue;

                        blocks.Add(new BlockOccupancy { X = x, Y = y, Z = z });
                    }
                }
            }

            solidBlocks = blocks.Count;

            using (MemoryStream stream = new MemoryStream(
                BridgeProtocol.CollisionRegionHeaderBytes + blocks.Count * BridgeProtocol.CollisionBlockBytes))
            using (BinaryWriter writer = new BinaryWriter(stream))
            {
                writer.Write(minX);
                writer.Write(minY);
                writer.Write(minZ);
                writer.Write(maxX);
                writer.Write(maxY);
                writer.Write(maxZ);
                writer.Write(CollisionEpoch);
                writer.Write((uint)blocks.Count);

                foreach (BlockOccupancy block in blocks)
                {
                    writer.Write(block.X);
                    writer.Write(block.Y);
                    writer.Write(block.Z);
                    writer.Write(0u);

                    // Full 8x8x8 occupancy for the first live collision pass.
                    // SkyCollision already supports the exact same record when we refine it later.
                    for (int layer = 0; layer < 8; layer++)
                        writer.Write(ulong.MaxValue);
                }

                return stream.ToArray();
            }
        }

        private bool IsSolidCell(int x, int y, int z)
        {
            Vector3 center = new Vector3(x + 0.5f, y + 0.5f, z + 0.5f);
            int count = Physics.OverlapBoxNonAlloc(
                center,
                new Vector3(0.48f, 0.48f, 0.48f),
                _hits,
                Quaternion.identity,
                ~0,
                QueryTriggerInteraction.Ignore);

            if (count <= 0)
                return false;

            Transform player = Player.main != null ? Player.main.transform : null;

            int limit = Math.Min(count, _hits.Length);
            for (int i = 0; i < limit; i++)
            {
                Collider collider = _hits[i];
                _hits[i] = null;

                if (collider == null || !collider.enabled || collider.isTrigger)
                    continue;

                Transform t = collider.transform;
                if (player != null && (t == player || t.IsChildOf(player)))
                    continue;

                Rigidbody body = collider.attachedRigidbody;
                if (body != null && !body.isKinematic)
                    continue; // creatures, loose items and other moving bodies are entity work, not static world collision

                return true;
            }

            return false;
        }

        private struct BlockOccupancy
        {
            public int X;
            public int Y;
            public int Z;
        }

        private static int FloorDiv(int value, int divisor)
        {
            int q = value / divisor;
            int r = value % divisor;
            return r != 0 && ((r < 0) != (divisor < 0)) ? q - 1 : q;
        }
    }
}
