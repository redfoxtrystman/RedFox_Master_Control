using System;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Compatibility mirror of the SkyCraft/FalloutCraft shared-memory protocol v11.
    /// Phase 0 intentionally reuses this byte layout so the existing Minecraft side can connect
    /// without rewriting working SkyCraft systems.
    /// </summary>
    public static class BridgeProtocol
    {
        public const uint Magic = 0x43594B53; // "SKYC"
        public const uint Version = 11;

        public const string DefaultMappingName = @"Local\SkyCraft_Subnautica_v1";

        public const long OffHeader = 0x0;
        public const long OffHostState = 0x100;
        public const long OffMinecraftState = 0x200;
        public const long OffOverlayCtl = 0x300;
        public const long OffOverlaySlotHeader = 0x340;
        public const long OffWaterGrid = 0x400;
        public const long OffInputRing = 0x1000;
        public const long OffActorTable = 0x12000;
        public const long OffEventRing = 0x17000;
        public const long OffWorldEntities = 0x1C000;
        public const long OffCollisionRing = 0x20000;

        public const long CollisionRingBytes = 32L << 20;
        public const int MaxOverlayWidth = 3840;
        public const int MaxOverlayHeight = 2160;
        public const int OverlaySlots = 3;
        public const long OverlaySlotBytes = (long)MaxOverlayWidth * MaxOverlayHeight * 4;
        public const long OffOverlayPixels = OffCollisionRing + CollisionRingBytes * 1L;
        public const long OffRenderRing = OffOverlayPixels + OverlaySlotBytes * OverlaySlots;
        public const long RenderRingBytes = 64L << 20;
        public const long MappingBytes = OffRenderRing + RenderRingBytes;

        // Header offsets.
        public const long HMagic = 0x00;
        public const long HVersion = 0x04;
        public const long HHostPid = 0x08;
        public const long HMinecraftPid = 0x0C;
        public const long HHostHeartbeat = 0x10;
        public const long HMinecraftHeartbeat = 0x18;

        // Host state offsets (SkyState in the original protocol).
        public const long HSSeq = 0x00;
        public const long HSFlags = 0x04;
        public const long HSWorldId = 0x08;
        public const long HSCollisionEpoch = 0x0C;
        public const long HSPosX = 0x10;
        public const long HSPosY = 0x18;
        public const long HSPosZ = 0x20;
        public const long HSYaw = 0x28;
        public const long HSPitch = 0x2C;
        public const long HSTeleportSeq = 0x30;
        public const long HSViewportW = 0x34;
        public const long HSViewportH = 0x38;
        public const long HSGameHour = 0x3C;

        public const uint HostInGame = 1u << 0;
        public const uint HostMenuOpen = 1u << 1;
        public const uint HostLoading = 1u << 2;

        // WaterGrid offsets.
        public const int WaterGridSize = 16;
        public const float NoWater = -1.0e30f;
        public const long WGSeq = 0x00;
        public const long WGOriginX = 0x04;
        public const long WGOriginZ = 0x08;
        public const long WGWorldId = 0x0C;
        public const long WGSurface = 0x10;

        // Input ring: host produces, Minecraft consumes.
        public const int InputRingEntries = 4096;
        public const int InputEventBytes = 16;
        public const long IRHead = 0x00;
        public const long IRTail = 0x40;
        public const long IRData = 0x80;

        public const ushort InputKey = 1;
        public const ushort InputMouseButton = 2;
        public const ushort InputScroll = 3;
        public const ushort InputCursor = 4;
        public const ushort InputText = 5;
        public const ushort InputReleaseAll = 6;
        public const ushort InputHurt = 7;
        public const ushort InputOpenMenu = 8;

        // Minecraft state offsets.
        public const long MSSeq = 0x00;
        public const long MSFlags = 0x04;
        public const long MSX = 0x08;
        public const long MSY = 0x10;
        public const long MSZ = 0x18;
        public const long MSYaw = 0x20;
        public const long MSPitch = 0x24;
        public const long MSEyeHeight = 0x28;
        public const long MSSensitivity = 0x2C;
        public const long MSTeleportAck = 0x30;
        public const long MSGuiScale = 0x34;
        public const long MSFrameCounter = 0x38;
        public const long MSFov = 0x40;
        public const long MSBobPhase = 0x44;
        public const long MSBobAmount = 0x48;
        public const long MSEyeX = 0x50;
        public const long MSEyeY = 0x58;
        public const long MSEyeZ = 0x60;
        public const long MSTickQpc = 0x68;
        public const long MSPrevX = 0x70;
        public const long MSCurX = 0x88;
        public const long MSEyeHeightO = 0xA0;
        public const long MSEyeHeightT = 0xA4;
        public const long MSWalkO = 0xA8;
        public const long MSWalk = 0xAC;
        public const long MSBobO = 0xB0;
        public const long MSBob = 0xB4;
        public const long MSTickMs = 0xB8;
        public const long MSCameraMode = 0xC0;
        public const long MSCameraDistance = 0xC4;

        public const uint MinecraftInWorld = 1u << 0;
        public const uint MinecraftScreenOpen = 1u << 1;
        public const uint MinecraftOnGround = 1u << 2;
        public const uint MinecraftSneaking = 1u << 3;
        public const uint MinecraftSprinting = 1u << 4;
        public const uint MinecraftDead = 1u << 5;
        public const uint MinecraftSwimming = 1u << 6;
        public const uint MinecraftFlying = 1u << 7;
    }

    public struct HostState
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

    public struct MinecraftState
    {
        public uint Flags;
        public double X;
        public double Y;
        public double Z;
        public float Yaw;
        public float Pitch;
        public float EyeHeight;
        public float Sensitivity;
        public uint TeleportAck;
        public uint GuiScale;
        public ulong FrameCounter;
        public float Fov;
        public double EyeX;
        public double EyeY;
        public double EyeZ;
        public int CameraMode;
        public float CameraDistance;

        public bool InWorld { get { return (Flags & BridgeProtocol.MinecraftInWorld) != 0; } }
        public bool ScreenOpen { get { return (Flags & BridgeProtocol.MinecraftScreenOpen) != 0; } }
        public bool Swimming { get { return (Flags & BridgeProtocol.MinecraftSwimming) != 0; } }
        public bool Dead { get { return (Flags & BridgeProtocol.MinecraftDead) != 0; } }
    }
}
