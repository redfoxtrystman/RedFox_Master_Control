using System;

namespace MinecraftSubnautica.Bridge
{
    public enum CrossGameOrigin : uint
    {
        Unknown = 0,
        Minecraft = 1,
        Subnautica = 2
    }

    [Flags]
    public enum CrossGameItemFlags : uint
    {
        None = 0,
        HasEnergy = 1u << 0,
        HasDurability = 1u << 1,
        Consumable = 1u << 2,
        Tool = 1u << 3,
        Weapon = 1u << 4,
        Equipment = 1u << 5,
        Creature = 1u << 6,
        Vehicle = 1u << 7
    }

    public enum CrossGameItemOp : uint
    {
        Transfer = 1,
        Update = 2,
        Consume = 3,
        Remove = 4,
        Use = 5
    }

    /// <summary>
    /// Separate item/state transport for Minecraft <-> Subnautica.
    /// It intentionally does not alter SkyCraft protocol v11, keeping FalloutCraft binary-compatible.
    /// </summary>
    public static class CrossGameItemProtocol
    {
        public const uint Magic = 0x4D495853; // "SXIM" little-endian
        public const uint Version = 1;
        public const string DefaultMappingName = @"Local\SkyCraft_Subnautica_Items_v1";

        public const int RingEntries = 64;
        public const int RecordBytes = 1024;

        public const long OffHeader = 0x0000;
        public const long OffHostToMinecraft = 0x1000;
        public const long OffMinecraftToHost = OffHostToMinecraft + 0x100 + (long)RingEntries * RecordBytes;
        public const long MappingBytes = OffMinecraftToHost + 0x100 + (long)RingEntries * RecordBytes;

        public const long HMagic = 0x00;
        public const long HVersion = 0x04;
        public const long HHostPid = 0x08;
        public const long HMinecraftPid = 0x0C;
        public const long HHostHeartbeat = 0x10;
        public const long HMinecraftHeartbeat = 0x18;

        public const long RHead = 0x00;
        public const long RTail = 0x40;
        public const long RData = 0x100;

        public const long ITransferId = 0x00;
        public const long IOperation = 0x08;
        public const long IOrigin = 0x0C;
        public const long IFlags = 0x10;
        public const long ICount = 0x14;
        public const long IMaxStack = 0x18;
        public const long IEnergy = 0x1C;
        public const long IMaxEnergy = 0x20;
        public const long IDurability = 0x24;
        public const long IMaxDurability = 0x28;
        public const long IIdLength = 0x2C;
        public const long INameLength = 0x30;
        public const long IStateLength = 0x34;
        public const long IId = 0x40;
        public const int IdBytes = 128;
        public const long IName = IId + IdBytes;
        public const int NameBytes = 128;
        public const long IState = IName + NameBytes;
        public const int StateBytes = RecordBytes - (int)IState;
    }

    public sealed class CrossGameItem
    {
        public ulong TransferId;
        public CrossGameItemOp Operation = CrossGameItemOp.Transfer;
        public CrossGameOrigin Origin;
        public CrossGameItemFlags Flags;
        public int Count = 1;
        public int MaxStack = 1;
        public float Energy;
        public float MaxEnergy;
        public float Durability;
        public float MaxDurability;
        public string ItemId = string.Empty;
        public string DisplayName = string.Empty;

        /// <summary>
        /// Opaque UTF-8 JSON/state owned by the adapter for the item's origin game.
        /// The bridge transports it losslessly and does not reinterpret it.
        /// </summary>
        public string StateJson = string.Empty;
    }
}
