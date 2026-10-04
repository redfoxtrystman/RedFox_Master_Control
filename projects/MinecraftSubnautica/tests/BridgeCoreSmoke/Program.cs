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

                // Simulate the existing SkyCraft Minecraft side publishing McState.
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

            Console.WriteLine("PASS: SkyCraft v11 shared-memory contract smoke test");
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine("FAIL: " + ex);
            return 1;
        }
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

    private static void AssertEqual(int expected, int actual, string name)
    {
        if (expected != actual)
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
