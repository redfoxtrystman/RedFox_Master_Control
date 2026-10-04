using System;
using System.Diagnostics;
using System.IO.MemoryMappedFiles;
using System.Threading;
using MinecraftSubnautica.Bridge;

internal static class Program
{
    private static int Main()
    {
        string name = @"Local\MinecraftSubnautica_Smoke_" + Process.GetCurrentProcess().Id;
        string itemName = @"Local\MinecraftSubnautica_Items_Smoke_" + Process.GetCurrentProcess().Id;

        try
        {
            using (var bridge = new SharedMemoryBridge(name))
            using (var map = MemoryMappedFile.OpenExisting(name, MemoryMappedFileRights.ReadWrite))
            using (var view = map.CreateViewAccessor(0, BridgeProtocol.MappingBytes, MemoryMappedFileAccess.ReadWrite))
            {
                AssertEqual(BridgeProtocol.Magic, view.ReadUInt32(BridgeProtocol.OffHeader + BridgeProtocol.HMagic), "magic");
                AssertEqual(BridgeProtocol.Version, view.ReadUInt32(BridgeProtocol.OffHeader + BridgeProtocol.HVersion), "version");
                AssertTrue(view.ReadUInt32(BridgeProtocol.OffHeader + BridgeProtocol.HHostPid) != 0, "host pid");
                AssertTrue(view.ReadUInt64(BridgeProtocol.OffHeader + BridgeProtocol.HHostHeartbeat) != 0, "host heartbeat");

                var host = new HostState
                {
                    Flags = BridgeProtocol.HostInGame,
                    WorldId = 7,
                    CollisionEpoch = 9,
                    X = 10.25,
                    Y = -34.5,
                    Z = 99.75,
                    Yaw = 42.0f,
                    Pitch = -12.0f,
                    ViewportWidth = 1920,
                    ViewportHeight = 1080,
                    GameHour = 13.5f
                };
                bridge.WriteHostState(host);

                long hs = BridgeProtocol.OffHostState;
                AssertTrue((view.ReadUInt32(hs + BridgeProtocol.HSSeq) & 1u) == 0u, "host seqlock even");
                AssertNear(host.X, view.ReadDouble(hs + BridgeProtocol.HSPosX), "host X");
                AssertNear(host.Y, view.ReadDouble(hs + BridgeProtocol.HSPosY), "host Y");
                AssertNear(host.Z, view.ReadDouble(hs + BridgeProtocol.HSPosZ), "host Z");

                int count = BridgeProtocol.WaterGridSize * BridgeProtocol.WaterGridSize;
                float[] water = new float[count];
                for (int i = 0; i < water.Length; i++)
                    water[i] = i == 3 ? BridgeProtocol.NoWater : 0.75f;

                bridge.WriteWaterGrid(-8, -8, 7, water);
                long wg = BridgeProtocol.OffWaterGrid;
                AssertTrue((view.ReadUInt32(wg + BridgeProtocol.WGSeq) & 1u) == 0u, "water seqlock even");
                AssertEqual(-8, view.ReadInt32(wg + BridgeProtocol.WGOriginX), "water origin X");
                AssertEqual(-8, view.ReadInt32(wg + BridgeProtocol.WGOriginZ), "water origin Z");
                AssertNear(0.75f, view.ReadSingle(wg + BridgeProtocol.WGSurface), "water surface");
                AssertNear(BridgeProtocol.NoWater, view.ReadSingle(wg + BridgeProtocol.WGSurface + 3 * 4L), "dry sentinel");

                AssertTrue(bridge.PushKey(26, true), "push W down");
                long input = BridgeProtocol.OffInputRing;
                AssertEqual(1UL, view.ReadUInt64(input + BridgeProtocol.IRHead), "input head");
                long ev = input + BridgeProtocol.IRData;
                AssertEqual(BridgeProtocol.InputKey, view.ReadUInt16(ev + 0), "input type");
                AssertEqual((ushort)26, view.ReadUInt16(ev + 2), "input scancode");
                AssertEqual(1, view.ReadInt32(ev + 4), "input down");

                view.Write(input + BridgeProtocol.IRTail, 1UL);
                AssertTrue(bridge.ReleaseAllInput(), "release-all input");
                AssertEqual(2UL, view.ReadUInt64(input + BridgeProtocol.IRHead), "input head after release");
                long ev2 = input + BridgeProtocol.IRData + BridgeProtocol.InputEventBytes;
                AssertEqual(BridgeProtocol.InputReleaseAll, view.ReadUInt16(ev2 + 0), "release-all type");

                long ms = BridgeProtocol.OffMinecraftState;
                view.Write(ms + BridgeProtocol.MSSeq, 1u);
                Thread.MemoryBarrier();
                view.Write(ms + BridgeProtocol.MSFlags, BridgeProtocol.MinecraftInWorld | BridgeProtocol.MinecraftSwimming);
                view.Write(ms + BridgeProtocol.MSX, 12.5);
                view.Write(ms + BridgeProtocol.MSY, -2.0);
                view.Write(ms + BridgeProtocol.MSZ, 44.0);
                view.Write(ms + BridgeProtocol.MSYaw, 90.0f);
                view.Write(ms + BridgeProtocol.MSPitch, -20.0f);
                view.Write(ms + BridgeProtocol.MSFov, 80.0f);
                Thread.MemoryBarrier();
                view.Write(ms + BridgeProtocol.MSSeq, 2u);

                AssertTrue(bridge.TryReadMinecraftState(out MinecraftState minecraft), "read Minecraft state");
                AssertTrue(minecraft.InWorld, "Minecraft in-world flag");
                AssertTrue(minecraft.Swimming, "Minecraft swimming flag");
                AssertNear(12.5, minecraft.X, "Minecraft X");
                AssertNear(-2.0, minecraft.Y, "Minecraft Y");
                AssertNear(44.0, minecraft.Z, "Minecraft Z");
                AssertNear(80.0f, minecraft.Fov, "Minecraft FOV");
            }

            using (var items = new CrossGameItemChannel(itemName))
            using (var itemMap = MemoryMappedFile.OpenExisting(itemName, MemoryMappedFileRights.ReadWrite))
            using (var itemView = itemMap.CreateViewAccessor(0, CrossGameItemProtocol.MappingBytes, MemoryMappedFileAccess.ReadWrite))
            {
                AssertEqual(CrossGameItemProtocol.Magic, itemView.ReadUInt32(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HMagic), "item magic");
                AssertEqual(CrossGameItemProtocol.Version, itemView.ReadUInt32(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HVersion), "item version");

                var seaglide = new CrossGameItem
                {
                    TransferId = 42,
                    Operation = CrossGameItemOp.Transfer,
                    Origin = CrossGameOrigin.Subnautica,
                    Flags = CrossGameItemFlags.Tool | CrossGameItemFlags.HasEnergy,
                    Count = 1,
                    MaxStack = 1,
                    Energy = 72.38f,
                    MaxEnergy = 100.0f,
                    ItemId = "subnautica:seaglide",
                    DisplayName = "Seaglide",
                    StateJson = "{\"battery\":{\"techType\":\"Battery\",\"charge\":72.38}}"
                };

                AssertTrue(items.TrySendToMinecraft(seaglide), "host -> Minecraft item enqueue");
                long h2m = CrossGameItemProtocol.OffHostToMinecraft;
                AssertEqual(1UL, itemView.ReadUInt64(h2m + CrossGameItemProtocol.RHead), "host -> Minecraft item head");
                long record = h2m + CrossGameItemProtocol.RData;
                AssertEqual(42UL, itemView.ReadUInt64(record + CrossGameItemProtocol.ITransferId), "seaglide transfer id");
                AssertNear(72.38f, itemView.ReadSingle(record + CrossGameItemProtocol.IEnergy), "seaglide charge");

                // Simulate Minecraft consuming that item and sending a state update back after use.
                itemView.Write(h2m + CrossGameItemProtocol.RTail, 1UL);

                long m2h = CrossGameItemProtocol.OffMinecraftToHost;
                itemView.Write(m2h + CrossGameItemProtocol.RHead, 0UL);
                itemView.Write(m2h + CrossGameItemProtocol.RTail, 0UL);
                WriteItemRecord(itemView, m2h + CrossGameItemProtocol.RData, new CrossGameItem
                {
                    TransferId = 42,
                    Operation = CrossGameItemOp.Update,
                    Origin = CrossGameOrigin.Subnautica,
                    Flags = CrossGameItemFlags.Tool | CrossGameItemFlags.HasEnergy,
                    Count = 1,
                    MaxStack = 1,
                    Energy = 41.06f,
                    MaxEnergy = 100.0f,
                    ItemId = "subnautica:seaglide",
                    DisplayName = "Seaglide",
                    StateJson = "{\"battery\":{\"techType\":\"Battery\",\"charge\":41.06}}"
                });
                Thread.MemoryBarrier();
                itemView.Write(m2h + CrossGameItemProtocol.RHead, 1UL);

                AssertTrue(items.TryReceiveFromMinecraft(out CrossGameItem updated), "Minecraft -> host item dequeue");
                AssertEqual(42UL, updated.TransferId, "returned transfer id");
                AssertEqual("subnautica:seaglide", updated.ItemId, "returned item id");
                AssertNear(41.06f, updated.Energy, "returned charge");
                AssertEqual(1UL, itemView.ReadUInt64(m2h + CrossGameItemProtocol.RTail), "Minecraft -> host item tail");
            }

            Console.WriteLine("PASS: SkyCraft v11 + cross-game item transport smoke test");
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine("FAIL: " + ex);
            return 1;
        }
    }

    private static void WriteItemRecord(MemoryMappedViewAccessor view, long b, CrossGameItem item)
    {
        view.Write(b + CrossGameItemProtocol.ITransferId, item.TransferId);
        view.Write(b + CrossGameItemProtocol.IOperation, (uint)item.Operation);
        view.Write(b + CrossGameItemProtocol.IOrigin, (uint)item.Origin);
        view.Write(b + CrossGameItemProtocol.IFlags, (uint)item.Flags);
        view.Write(b + CrossGameItemProtocol.ICount, item.Count);
        view.Write(b + CrossGameItemProtocol.IMaxStack, item.MaxStack);
        view.Write(b + CrossGameItemProtocol.IEnergy, item.Energy);
        view.Write(b + CrossGameItemProtocol.IMaxEnergy, item.MaxEnergy);
        view.Write(b + CrossGameItemProtocol.IDurability, item.Durability);
        view.Write(b + CrossGameItemProtocol.IMaxDurability, item.MaxDurability);
        WriteUtf8(view, b + CrossGameItemProtocol.IId, CrossGameItemProtocol.IdBytes, b + CrossGameItemProtocol.IIdLength, item.ItemId);
        WriteUtf8(view, b + CrossGameItemProtocol.IName, CrossGameItemProtocol.NameBytes, b + CrossGameItemProtocol.INameLength, item.DisplayName);
        WriteUtf8(view, b + CrossGameItemProtocol.IState, CrossGameItemProtocol.StateBytes, b + CrossGameItemProtocol.IStateLength, item.StateJson);
    }

    private static void WriteUtf8(MemoryMappedViewAccessor view, long offset, int capacity, long lengthOffset, string value)
    {
        byte[] bytes = System.Text.Encoding.UTF8.GetBytes(value ?? string.Empty);
        if (bytes.Length > capacity)
            throw new InvalidOperationException("test string exceeds protocol capacity");
        byte[] zero = new byte[capacity];
        view.WriteArray(offset, zero, 0, zero.Length);
        view.WriteArray(offset, bytes, 0, bytes.Length);
        view.Write(lengthOffset, bytes.Length);
    }

    private static void AssertTrue(bool condition, string name)
    {
        if (!condition)
            throw new InvalidOperationException("Assertion failed: " + name);
    }

    private static void AssertEqual(uint expected, uint actual, string name)
    {
        if (expected != actual)
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }

    private static void AssertEqual(ulong expected, ulong actual, string name)
    {
        if (expected != actual)
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }

    private static void AssertEqual(ushort expected, ushort actual, string name)
    {
        if (expected != actual)
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }

    private static void AssertEqual(int expected, int actual, string name)
    {
        if (expected != actual)
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }

    private static void AssertEqual(string expected, string actual, string name)
    {
        if (!string.Equals(expected, actual, StringComparison.Ordinal))
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }

    private static void AssertNear(double expected, double actual, string name)
    {
        if (Math.Abs(expected - actual) > 0.0001)
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }

    private static void AssertNear(float expected, float actual, string name)
    {
        if (Math.Abs(expected - actual) > 0.0001f)
            throw new InvalidOperationException($"{name}: expected {expected}, got {actual}");
    }
}
