using System.Buffers.Binary;
using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Writable SaveFile facade over a legacy Pokémon Essentials .rxdata save.
/// The in-memory buffer contains registry indexes. Export rebuilds only the
/// trainer/party and PokemonStorage/box Marshal streams.
/// </summary>
public sealed class EssentialsLegacySaveFile : SaveFile, IBoxDetailNameRead
{
    private const int SlotBytes = sizeof(int);
    private readonly EssentialsLegacySaveData Source;
    private readonly List<PKEssentials> Registry;
    private readonly string[] BoxNames;
    private readonly int LocalMaxSpecies;
    private readonly int BoxSlots;
    private bool Dirty;

    private sealed record BuildResult(
        byte[] Buffer,
        List<PKEssentials> Registry,
        string[] BoxNames,
        int BoxSlotCount,
        int MaxSpecies
    );

    public EssentialsLegacySaveFile(EssentialsLegacySaveData source)
        : this(source, Build(source))
    {
    }

    private EssentialsLegacySaveFile(EssentialsLegacySaveData source, BuildResult built)
        : base(built.Buffer, exportable: true)
    {
        Source = source;
        Registry = built.Registry;
        BoxNames = built.BoxNames;
        BoxSlots = built.BoxSlotCount;
        LocalMaxSpecies = built.MaxSpecies;

        Party = 0;
        Box = source.Boxes.Count > 0 ? 0 : int.MinValue;
        PartyCount = Math.Min(6, source.Party.Count);
        CurrentBox = 0;

        ID32 = source.TrainerId;
        OT = source.TrainerName;
        Language = (int)LanguageID.English;
    }

    public string ProfileId => Source.ProfileId;
    public string ProfileVersion => Source.ProfileVersion;
    public EssentialsGameKind Game => Source.Game;

    protected override string ShortSummary => Game switch
    {
        EssentialsGameKind.Uranium => "Pokémon Uranium",
        EssentialsGameKind.Insurgence => "Pokémon Insurgence",
        _ => "Pokémon Essentials",
    };

    public override string Extension => "rxdata";
    public override GameVersion Version { get => GameVersion.E; set { } }
    public override bool ChecksumsValid => true;
    public override string ChecksumInfo => Dirty
        ? "Essentials trainer/storage streams will be rebuilt on write."
        : "Original Essentials bytes are unchanged.";
    public override byte Generation => 3;
    public override EntityContext Context => EntityContext.Gen3;

    public override IPersonalTable Personal => PersonalTable.RS;
    public override int MaxStringLengthTrainer => 32;
    public override int MaxStringLengthNickname => 32;
    public override ushort MaxMoveID => ushort.MaxValue;
    public override ushort MaxSpeciesID => checked((ushort)Math.Clamp(LocalMaxSpecies, 1, ushort.MaxValue));
    public override int MaxAbilityID => ushort.MaxValue;
    public override int MaxItemID => ushort.MaxValue;
    public override int MaxBallID => byte.MaxValue;
    public override GameVersion MaxGameID => GameVersion.E;

    public override byte Gender { get; set; }
    public override int Language { get; set; } = (int)LanguageID.English;
    public override uint ID32 { get; set; }
    public override string OT { get; set; } = "";
    public override int BoxCount => Source.Boxes.Count;
    public override int BoxSlotCount => BoxSlots;
    public override int SlotCount => BoxCount * BoxSlotCount;
    public override int CurrentBox { get; set; }

    public override Type PKMType => typeof(PKEssentials);
    public override PKEssentials BlankPKM => new();
    public override int SIZE_STORED => SlotBytes;
    public override int SIZE_PARTY => SlotBytes;
    public override int SIZE_BOXSLOT => SlotBytes;
    public override int MaxEV => 252;
    public override ReadOnlySpan<ushort> HeldItems => [];

    protected override Span<byte> PartyBuffer => Data[..(6 * SlotBytes)];
    protected override Span<byte> BoxBuffer => Data[(6 * SlotBytes)..];

    public override int GetPartyOffset(int slot)
    {
        if ((uint)slot >= 6)
            throw new ArgumentOutOfRangeException(nameof(slot));
        return slot * SlotBytes;
    }

    public override int GetBoxOffset(int box)
    {
        if ((uint)box >= BoxCount)
            throw new ArgumentOutOfRangeException(nameof(box));
        return box * BoxSlotCount * SlotBytes;
    }

    public override bool IsPKMPresent(ReadOnlySpan<byte> data)
        => data.Length >= SlotBytes && BinaryPrimitives.ReadInt32LittleEndian(data) > 0;

    protected override PKEssentials GetPKM(Memory<byte> data)
    {
        if (data.Length < SlotBytes)
            return BlankPKM;

        var index = BinaryPrimitives.ReadInt32LittleEndian(data.Span);
        if (index <= 0 || index > Registry.Count)
            return BlankPKM;

        return (PKEssentials)Registry[index - 1].Clone();
    }

    protected override void DecryptPKM(Span<byte> data) { }

    public override StorageSlotSource GetBoxSlotFlags(int index)
    {
        if (index < 0)
        {
            var slot = index + BoxSlotCount;
            if ((uint)slot < 6)
                return (StorageSlotSource)(1 << slot);
        }

        return StorageSlotSource.None;
    }

    public string GetBoxName(int box)
        => (uint)box < BoxNames.Length ? BoxNames[box] : BoxDetailNameExtensions.GetDefaultBoxName(box);

    public PKEssentials CreateWritableTemplate()
    {
        var source = Registry.FirstOrDefault(z => !z.ReadOnlySource && z.SourceRubyMarshal.Length > 0)
            ?? throw new InvalidOperationException(
                "This Essentials save has no existing writable Pokémon record to use as an import template.");
        var clone = (PKEssentials)source.Clone();
        clone.SourceContainer = "import";
        clone.SourceSlot = -1;
        clone.SourceSavePath = Metadata.FilePath;
        clone.ReadOnlySource = false;
        return clone;
    }

    protected override void WriteSlotStored(PKM pk, Span<byte> data) => WriteRegistrySlot(pk, data);
    protected override void WriteSlotParty(PKM pk, Span<byte> data) => WriteRegistrySlot(pk, data);
    protected override void SetPartyValues(PKM pk, bool isParty) { }

    private void WriteRegistrySlot(PKM pk, Span<byte> data)
    {
        if (pk.Species == 0)
        {
            BinaryPrimitives.WriteInt32LittleEndian(data[..SlotBytes], 0);
            Dirty = true;
            return;
        }

        if (pk is not PKEssentials essentials)
            throw new InvalidOperationException($"Expected PKEssentials, got {pk.GetType().Name}.");
        if (!string.Equals(essentials.ProfileId, ProfileId, StringComparison.Ordinal))
            throw new InvalidOperationException($"Cross-profile Essentials write blocked: {essentials.ProfileId} -> {ProfileId}.");
        if (essentials.ReadOnlySource || essentials.SourceRubyMarshal.Length == 0)
            throw new InvalidOperationException(
                "This Essentials Pokémon lacks a writable Ruby source template. Re-import it from its game save first.");

        Registry.Add((PKEssentials)essentials.Clone());
        BinaryPrimitives.WriteInt32LittleEndian(data[..SlotBytes], Registry.Count);
        Dirty = true;
    }

    protected override void SetChecksums() { }
    protected override EssentialsLegacySaveFile CloneInternal()
    {
        var clone = new EssentialsLegacySaveFile(Source);
        for (var i = 0; i < Data.Length; i++)
            clone.Data[i] = Data[i];
        clone.Registry.Clear();
        clone.Registry.AddRange(Registry.Select(z => (PKEssentials)z.Clone()));
        clone.PartyCount = PartyCount;
        clone.CurrentBox = CurrentBox;
        clone.Dirty = Dirty;
        return clone;
    }

    protected override Memory<byte> GetFinalData()
    {
        if (!Dirty)
            return Source.OriginalBytes.ToArray();

        var party = new List<PKEssentials>();
        for (var slot = 0; slot < Math.Min(6, PartyCount); slot++)
        {
            if (GetPartySlotAtIndex(slot) is PKEssentials pkm && pkm.LocalSpeciesId > 0)
                party.Add(pkm);
        }

        var boxes = new List<EssentialsBoxData>(BoxCount);
        for (var box = 0; box < BoxCount; box++)
        {
            var slots = new List<PKEssentials?>(BoxSlotCount);
            for (var slot = 0; slot < BoxSlotCount; slot++)
            {
                var pkm = GetBoxSlotAtIndex(box, slot) as PKEssentials;
                slots.Add(pkm is { LocalSpeciesId: > 0 } ? pkm : null);
            }
            boxes.Add(new EssentialsBoxData(GetBoxName(box), slots));
        }

        var bytes = EssentialsLegacySaveWriter.Write(Source, party, boxes);
        var validationPath = Game == EssentialsGameKind.Uranium
            ? "Pokemon Uranium/Uranium.rxdata"
            : "Pokemon Insurgence/Game.rxdata";
        if (!EssentialsLegacySaveReader.TryRead(bytes, validationPath, out var validation, out var error)
            || validation == null
            || validation.Game != Game
            || validation.Party.Count != party.Count
            || validation.Boxes.Count != boxes.Count)
        {
            throw new InvalidDataException($"Essentials write validation failed: {error ?? "round-trip structure mismatch"}");
        }

        return bytes;
    }

    public override string GetString(ReadOnlySpan<byte> data) => "";
    public override int LoadString(ReadOnlySpan<byte> data, Span<char> destBuffer) => 0;
    public override int SetString(Span<byte> destBuffer, ReadOnlySpan<char> value, int maxLength, StringConverterOption option) => 0;

    private static BuildResult Build(EssentialsLegacySaveData source)
    {
        var registry = new List<PKEssentials>();
        var boxSlots = Math.Max(1, source.Boxes.Select(z => z.Pokemon.Count).DefaultIfEmpty(30).Max());
        var buffer = new byte[(6 + (source.Boxes.Count * boxSlots)) * SlotBytes];

        static void Put(Span<byte> target, int slot, int registryIndex)
            => BinaryPrimitives.WriteInt32LittleEndian(target.Slice(slot * SlotBytes, SlotBytes), registryIndex);

        for (var slot = 0; slot < Math.Min(6, source.Party.Count); slot++)
        {
            registry.Add((PKEssentials)source.Party[slot].Clone());
            Put(buffer, slot, registry.Count);
        }

        var boxBase = 6;
        for (var box = 0; box < source.Boxes.Count; box++)
        {
            var mons = source.Boxes[box].Pokemon;
            for (var slot = 0; slot < Math.Min(boxSlots, mons.Count); slot++)
            {
                var mon = mons[slot];
                if (mon == null)
                    continue;

                registry.Add((PKEssentials)mon.Clone());
                Put(buffer, boxBase + (box * boxSlots) + slot, registry.Count);
            }
        }

        var maxSpecies = registry.Select(z => z.LocalSpeciesId).DefaultIfEmpty(1).Max();
        return new(
            Buffer: buffer,
            Registry: registry,
            BoxNames: [.. source.Boxes.Select(z => z.Name)],
            BoxSlotCount: boxSlots,
            MaxSpecies: maxSpecies
        );
    }
}
