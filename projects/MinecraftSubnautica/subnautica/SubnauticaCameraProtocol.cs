using System;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Dedicated host-camera mapping for the Universal Modder colour+depth passthrough path.
    /// Kept separate from SkyCraft protocol v11 so FalloutCraft's proven state protocol stays ABI-stable.
    /// </summary>
    public static class SubnauticaCameraProtocol
    {
        public const string MappingName = @"Local\SkyCraft_Subnautica_Camera_v1";
        public const uint Magic = 0x4D414353; // "SCAM" little-endian
        public const uint Version = 1;
        public const long MappingBytes = 4096;

        public const long MagicOff = 0x00;
        public const long VersionOff = 0x04;
        public const long HostPidOff = 0x08;
        public const long HeartbeatOff = 0x10;

        // Seqlock: odd while host is writing, even when stable.
        public const long SeqOff = 0x20;
        public const long HostFrameOff = 0x28;
        public const long CameraXOff = 0x30;
        public const long CameraYOff = 0x38;
        public const long CameraZOff = 0x40;
        public const long YawOff = 0x48;
        public const long PitchOff = 0x4C;
        public const long RollOff = 0x50;
        public const long VerticalFovOff = 0x54;
        public const long NearClipOff = 0x58;
        public const long FarClipOff = 0x5C;
        public const long FlagsOff = 0x60;
        public const long ViewportWidthOff = 0x64;
        public const long ViewportHeightOff = 0x68;
        public const long PlayerXOff = 0x70;
        public const long PlayerYOff = 0x78;
        public const long PlayerZOff = 0x80;
        public const long BodyYawOff = 0x88;

        public const uint FirstPerson = 1u << 0;
    }

    public struct SubnauticaCameraFrame
    {
        public ulong HostFrame;
        public double CameraX, CameraY, CameraZ;
        public float Yaw, Pitch, Roll;
        public float VerticalFov;
        public float NearClip, FarClip;
        public uint Flags;
        public uint ViewportWidth, ViewportHeight;
        public double PlayerX, PlayerY, PlayerZ;
        public float BodyYaw;
    }
}
