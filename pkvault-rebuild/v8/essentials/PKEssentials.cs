using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace PKHeX.Core;

/// <summary>
/// Pokémon object for Pokémon Essentials / RPG Maker fan games.
///
/// Species, move, item, and ability IDs are profile-local. They MUST NOT be
/// interpreted as National Dex / official-game IDs without an explicit profile
/// conversion. This is intentionally a PKM so PKVault can store and display
/// Essentials Pokémon without aliasing Uranium #1 (Orchynx) to Bulbasaur #1.
/// </summary>
public sealed class PKEssentials : PKM
{
    public const int InternalSerializedVersion = 3;

    private readonly byte[] NickTrash = new byte[64];
    private readonly byte[] OtTrash = new byte[64];
    private EssentialsPersonalInfo PersonalData = new();

    public string ProfileId { get; set; } = "";
    public string ProfileVersion { get; set; } = "";
    public string SpeciesName { get; set; } = "";
    public string[] TypeNames { get; set; } = [];
    public string AbilityName { get; set; } = "";
    public string ItemName { get; set; } = "";
    public string[] MoveNames { get; set; } = ["", "", "", ""];
    public int LocalSpeciesId { get; set; }
    public int LocalFormId { get; set; }
    public int OfficialNationalDexId { get; set; }
    public byte StoredLevel { get; set; } = 1;
    public bool ReadOnlySource { get; set; } = true;

    // Enough provenance to re-associate the object with its exact Ruby record.
    public string SourceSavePath { get; set; } = "";
    public string SourceContainer { get; set; } = ""; // party or box:N
    public int SourceSlot { get; set; } = -1;
    public string SourceFingerprint { get; set; } = "";
    public byte[] SourceRubyMarshal { get; set; } = [];

    public PKEssentials() : base(1)
    {
        Valid = false;
        Language = (int)LanguageID.English;
    }

    public PKEssentials(EssentialsPkmPayload payload) : this() => Apply(payload);

    public void Apply(EssentialsPkmPayload p)
    {
        ProfileId = p.ProfileId ?? "";
        ProfileVersion = p.ProfileVersion ?? "";
        SpeciesName = p.SpeciesName ?? "";
        TypeNames = p.TypeNames ?? [];
        AbilityName = p.AbilityName ?? "";
        ItemName = p.ItemName ?? "";
        MoveNames = NormalizeMoveNames(p.MoveNames);
        LocalSpeciesId = p.LocalSpeciesId;
        LocalFormId = p.LocalFormId;
        OfficialNationalDexId = p.OfficialNationalDexId;
        StoredLevel = p.Level == 0 ? (byte)1 : p.Level;
        ReadOnlySource = p.ReadOnlySource;
        SourceSavePath = p.SourceSavePath ?? "";
        SourceContainer = p.SourceContainer ?? "";
        SourceSlot = p.SourceSlot;
        SourceFingerprint = p.SourceFingerprint ?? "";
        SourceRubyMarshal = p.SourceRubyMarshal ?? [];
        ReadOnlySource = p.ReadOnlySource || SourceRubyMarshal.Length == 0;

        Species = checked((ushort)Math.Clamp(
            p.OfficialNationalDexId > 0 ? p.OfficialNationalDexId : p.LocalSpeciesId,
            0,
            ushort.MaxValue
        ));
        Form = checked((byte)Math.Clamp(p.LocalFormId, 0, byte.MaxValue));
        Nickname = p.Nickname ?? SpeciesName;
        OriginalTrainerName = p.OriginalTrainerName ?? "";
        TID16 = p.TID16;
        SID16 = p.SID16;
        PID = p.PID;
        EXP = p.EXP;
        Gender = p.Gender;
        Nature = (Nature)Math.Clamp((int)p.Nature, 0, 24);
        HeldItem = p.HeldItem;
        Ability = p.Ability;
        AbilityNumber = p.AbilityNumber;
        CurrentFriendship = p.Friendship;
        IsEgg = p.IsEgg;
        Ball = p.Ball;
        MetLevel = p.MetLevel;
        OriginalTrainerGender = p.OriginalTrainerGender;

        Move1 = GetMove(p.Moves, 0); Move2 = GetMove(p.Moves, 1);
        Move3 = GetMove(p.Moves, 2); Move4 = GetMove(p.Moves, 3);
        Move1_PP = GetValue(p.MovePP, 0); Move2_PP = GetValue(p.MovePP, 1);
        Move3_PP = GetValue(p.MovePP, 2); Move4_PP = GetValue(p.MovePP, 3);
        Move1_PPUps = GetValue(p.MovePPUps, 0); Move2_PPUps = GetValue(p.MovePPUps, 1);
        Move3_PPUps = GetValue(p.MovePPUps, 2); Move4_PPUps = GetValue(p.MovePPUps, 3);

        var iv = NormalizeStats(p.IVs, 0);
        IV_HP = iv[0]; IV_ATK = iv[1]; IV_DEF = iv[2];
        IV_SPE = iv[3]; IV_SPA = iv[4]; IV_SPD = iv[5];

        var ev = NormalizeStats(p.EVs, 0);
        EV_HP = ev[0]; EV_ATK = ev[1]; EV_DEF = ev[2];
        EV_SPE = ev[3]; EV_SPA = ev[4]; EV_SPD = ev[5];

        var bs = NormalizeStats(p.BaseStats, 1);
        PersonalData = new EssentialsPersonalInfo
        {
            HP = bs[0], ATK = bs[1], DEF = bs[2], SPE = bs[3], SPA = bs[4], SPD = bs[5],
            Type1 = p.OfficialNationalDexId > 0
                ? PersonalTable.AO.GetFormEntry((ushort)p.OfficialNationalDexId, 0).Type1
                : (byte)0,
            Type2 = p.OfficialNationalDexId > 0
                ? PersonalTable.AO.GetFormEntry((ushort)p.OfficialNationalDexId, 0).Type2
                : (byte)0,
            EXPGrowth = (byte)Math.Clamp(p.ExpGrowth, 0, 5),
            Gender = p.GenderRatio,
            BaseFriendship = p.BaseFriendship,
            CatchRate = p.CatchRate,
            HatchCycles = p.HatchCycles,
            BaseEXP = p.BaseEXP,
            Abilities = p.AbilityIds ?? [],
        };

        // Party stats in Essentials are persisted. If unavailable, derive a
        // conservative set from the supplied base stats/level.
        var stats = NormalizeStats(p.Stats, 0);
        Stat_Level = StoredLevel;
        Stat_HPMax = stats[0] > 0 ? stats[0] : Math.Max(1, bs[0] + StoredLevel);
        Stat_HPCurrent = p.CurrentHP > 0 ? p.CurrentHP : Stat_HPMax;
        Stat_ATK = stats[1] > 0 ? stats[1] : bs[1];
        Stat_DEF = stats[2] > 0 ? stats[2] : bs[2];
        Stat_SPE = stats[3] > 0 ? stats[3] : bs[3];
        Stat_SPA = stats[4] > 0 ? stats[4] : bs[4];
        Stat_SPD = stats[5] > 0 ? stats[5] : bs[5];
        Status_Condition = p.StatusCondition;

        Valid = Species > 0;
        SyncTrash();
    }

    public EssentialsPkmPayload ToPayload() => new()
    {
        Version = InternalSerializedVersion,
        ProfileId = ProfileId,
        ProfileVersion = ProfileVersion,
        SpeciesName = SpeciesName,
        TypeNames = TypeNames,
        AbilityName = AbilityName,
        ItemName = ItemName,
        MoveNames = MoveNames,
        LocalSpeciesId = LocalSpeciesId,
        LocalFormId = LocalFormId,
        OfficialNationalDexId = OfficialNationalDexId,
        Level = StoredLevel,
        ReadOnlySource = ReadOnlySource,
        SourceSavePath = SourceSavePath,
        SourceContainer = SourceContainer,
        SourceSlot = SourceSlot,
        SourceFingerprint = SourceFingerprint,
        SourceRubyMarshal = SourceRubyMarshal,
        Nickname = Nickname,
        OriginalTrainerName = OriginalTrainerName,
        TID16 = TID16,
        SID16 = SID16,
        PID = PID,
        EXP = EXP,
        Gender = Gender,
        Nature = (byte)Nature,
        HeldItem = HeldItem,
        Ability = Ability,
        AbilityNumber = AbilityNumber,
        Friendship = CurrentFriendship,
        IsEgg = IsEgg,
        Ball = Ball,
        MetLevel = MetLevel,
        OriginalTrainerGender = OriginalTrainerGender,
        Moves = [Move1, Move2, Move3, Move4],
        MovePP = [Move1_PP, Move2_PP, Move3_PP, Move4_PP],
        MovePPUps = [Move1_PPUps, Move2_PPUps, Move3_PPUps, Move4_PPUps],
        IVs = [IV_HP, IV_ATK, IV_DEF, IV_SPE, IV_SPA, IV_SPD],
        EVs = [EV_HP, EV_ATK, EV_DEF, EV_SPE, EV_SPA, EV_SPD],
        BaseStats = [PersonalData.HP, PersonalData.ATK, PersonalData.DEF, PersonalData.SPE, PersonalData.SPA, PersonalData.SPD],
        Stats = [Stat_HPMax, Stat_ATK, Stat_DEF, Stat_SPE, Stat_SPA, Stat_SPD],
        CurrentHP = Stat_HPCurrent,
        StatusCondition = Status_Condition,
        ExpGrowth = PersonalData.EXPGrowth,
        GenderRatio = PersonalData.Gender,
        BaseFriendship = PersonalData.BaseFriendship,
        CatchRate = PersonalData.CatchRate,
        HatchCycles = PersonalData.HatchCycles,
        BaseEXP = PersonalData.BaseEXP,
        AbilityIds = PersonalData.Abilities,
    };

    public static byte[] Serialize(PKEssentials pkm) =>
        JsonSerializer.SerializeToUtf8Bytes(
            pkm.ToPayload(),
            EssentialsJsonContext.Default.EssentialsPkmPayload
        );

    public static PKEssentials Deserialize(ReadOnlySpan<byte> data)
    {
        var payload = JsonSerializer.Deserialize(
            data,
            EssentialsJsonContext.Default.EssentialsPkmPayload
        ) ?? throw new InvalidDataException("Invalid PKVault Essentials Pokémon payload.");
        return new(payload);
    }

    private static ushort GetMove(ushort[]? values, int index) => values is { Length: > 0 } && index < values.Length ? values[index] : (ushort)0;
    private static int GetValue(int[]? values, int index) => values is { Length: > 0 } && index < values.Length ? values[index] : 0;
    private static int[] NormalizeStats(int[]? values, int fallback)
    {
        var result = Enumerable.Repeat(fallback, 6).ToArray();
        if (values != null)
            Array.Copy(values, result, Math.Min(values.Length, result.Length));
        return result;
    }
    private static string[] NormalizeMoveNames(string[]? values)
    {
        var result = new[] {"", "", "", ""};
        if (values != null)
            Array.Copy(values, result, Math.Min(values.Length, result.Length));
        return result;
    }

    private void SyncTrash()
    {
        NickTrash.AsSpan().Clear();
        OtTrash.AsSpan().Clear();
        Encoding.UTF8.GetBytes(Nickname.AsSpan(), NickTrash);
        Encoding.UTF8.GetBytes(OriginalTrainerName.AsSpan(), OtTrash);
    }

    public override int SIZE_PARTY => 1;
    public override int SIZE_STORED => 1;
    public override PersonalInfo PersonalInfo => PersonalData;
    public override bool Valid { get; set; }
    public override Span<byte> NicknameTrash => NickTrash;
    public override Span<byte> OriginalTrainerTrash => OtTrash;
    public override EntityContext Context => EntityContext.Gen3;

    public override ushort Species { get; set; }
    public override string Nickname { get; set; } = "";
    public override int HeldItem { get; set; }
    public override byte Gender { get; set; }
    public override Nature Nature { get; set; }
    public override int Ability { get; set; }
    public override byte CurrentFriendship { get; set; }
    public override byte Form { get; set; }
    public override bool IsEgg { get; set; }
    public override bool IsNicknamed { get; set; }
    public override uint EXP { get; set; }
    public override ushort TID16 { get; set; }
    public override ushort SID16 { get; set; }
    public override string OriginalTrainerName { get; set; } = "";
    public override byte OriginalTrainerGender { get; set; }
    public override byte Ball { get; set; }
    public override byte MetLevel { get; set; }

    public override ushort Move1 { get; set; }
    public override ushort Move2 { get; set; }
    public override ushort Move3 { get; set; }
    public override ushort Move4 { get; set; }
    public override int Move1_PP { get; set; }
    public override int Move2_PP { get; set; }
    public override int Move3_PP { get; set; }
    public override int Move4_PP { get; set; }
    public override int Move1_PPUps { get; set; }
    public override int Move2_PPUps { get; set; }
    public override int Move3_PPUps { get; set; }
    public override int Move4_PPUps { get; set; }
    public override int EV_HP { get; set; }
    public override int EV_ATK { get; set; }
    public override int EV_DEF { get; set; }
    public override int EV_SPE { get; set; }
    public override int EV_SPA { get; set; }
    public override int EV_SPD { get; set; }
    public override int IV_HP { get; set; }
    public override int IV_ATK { get; set; }
    public override int IV_DEF { get; set; }
    public override int IV_SPE { get; set; }
    public override int IV_SPA { get; set; }
    public override int IV_SPD { get; set; }
    public override int Status_Condition { get; set; }
    public override byte Stat_Level { get; set; }
    public override int Stat_HPMax { get; set; }
    public override int Stat_HPCurrent { get; set; }
    public override int Stat_ATK { get; set; }
    public override int Stat_DEF { get; set; }
    public override int Stat_SPE { get; set; }
    public override int Stat_SPA { get; set; }
    public override int Stat_SPD { get; set; }

    public override GameVersion Version { get; set; } = GameVersion.E;
    public override uint ID32
    {
        get => (uint)(TID16 | (SID16 << 16));
        set { TID16 = (ushort)value; SID16 = (ushort)(value >> 16); }
    }
    public override int PokerusStrain { get; set; }
    public override int PokerusDays { get; set; }
    public override uint EncryptionConstant { get; set; }
    public override uint PID { get; set; }
    public override int Language { get; set; }
    public override bool FatefulEncounter { get; set; }
    public override uint TSV => (uint)((TID16 ^ SID16) >> 4);
    public override uint PSV => (uint)(((PID >> 16) ^ (PID & 0xFFFF)) >> 4);
    public override int Characteristic => 0;
    public override ushort MetLocation { get; set; }
    public override ushort EggLocation { get; set; }
    public override byte OriginalTrainerFriendship { get; set; }
    public override byte CurrentHandler { get; set; }

    public override ushort MaxMoveID => ushort.MaxValue;
    public override ushort MaxSpeciesID => ushort.MaxValue;
    public override int MaxItemID => ushort.MaxValue;
    public override int MaxAbilityID => ushort.MaxValue;
    public override int MaxBallID => byte.MaxValue;
    public override GameVersion MaxGameID => GameVersion.E;
    public override GameVersion MinGameID => GameVersion.E;
    public override int MaxIV => 31;
    public override int MaxEV => 252;
    public override int MaxStringLengthTrainer => 32;
    public override int MaxStringLengthNickname => 32;
    public override int TrashCharCountTrainer => OtTrash.Length;
    public override int TrashCharCountNickname => NickTrash.Length;

    public override string GetString(ReadOnlySpan<byte> data) => Encoding.UTF8.GetString(data[..GetStringTerminatorIndex(data)]);
    public override int LoadString(ReadOnlySpan<byte> data, Span<char> text)
    {
        var value = GetString(data);
        value.AsSpan().CopyTo(text);
        return value.Length;
    }
    public override int SetString(Span<byte> data, ReadOnlySpan<char> text, int length, StringConverterOption option)
    {
        data.Clear();
        var value = text[..Math.Min(text.Length, length)];
        return Encoding.UTF8.GetBytes(value, data);
    }
    public override int GetStringTerminatorIndex(ReadOnlySpan<byte> data)
    {
        var i = data.IndexOf((byte)0);
        return i < 0 ? data.Length : i;
    }
    public override int GetStringLength(ReadOnlySpan<byte> data) => GetString(data).Length;
    public override int GetBytesPerChar() => 1;

    protected override void EncryptStored(Span<byte> stored) { }
    protected override void EncryptParty(Span<byte> party) { }
    public override void RefreshChecksum() { }
    public override bool ChecksumValid => true;
    public override PKM Clone() => Deserialize(Serialize(this));
}

public sealed class EssentialsPersonalInfo : PersonalInfo
{
    public int[] Abilities { get; set; } = [];

    public override byte[] Write() => [];
    public override int HP { get; set; }
    public override int ATK { get; set; }
    public override int DEF { get; set; }
    public override int SPE { get; set; }
    public override int SPA { get; set; }
    public override int SPD { get; set; }
    public override int EV_HP { get; set; }
    public override int EV_ATK { get; set; }
    public override int EV_DEF { get; set; }
    public override int EV_SPE { get; set; }
    public override int EV_SPA { get; set; }
    public override int EV_SPD { get; set; }
    public override byte Type1 { get; set; }
    public override byte Type2 { get; set; }
    public override int EggGroup1 { get; set; }
    public override int EggGroup2 { get; set; }
    public override byte CatchRate { get; set; }
    public override byte Gender { get; set; } = RatioMagicGenderless;
    public override byte HatchCycles { get; set; }
    public override byte BaseFriendship { get; set; } = 70;
    public override byte EXPGrowth { get; set; }
    public override int EscapeRate { get; set; }
    public override int BaseEXP { get; set; }
    public override int Color { get; set; }
    public override int GetIndexOfAbility(int abilityID) => Array.IndexOf(Abilities, abilityID);
    public override int GetAbilityAtIndex(int abilityIndex) => abilityIndex >= 0 && abilityIndex < Abilities.Length ? Abilities[abilityIndex] : 0;
    public override int AbilityCount => Abilities.Length;
}

public sealed record EssentialsPkmPayload
{
    public int Version { get; init; } = PKEssentials.InternalSerializedVersion;
    public string? ProfileId { get; init; }
    public string? ProfileVersion { get; init; }
    public string? SpeciesName { get; init; }
    public string[]? TypeNames { get; init; }
    public string? AbilityName { get; init; }
    public string? ItemName { get; init; }
    public string[]? MoveNames { get; init; }
    public int LocalSpeciesId { get; init; }
    public int LocalFormId { get; init; }
    public int OfficialNationalDexId { get; init; }
    public byte Level { get; init; }
    public bool ReadOnlySource { get; init; } = true;
    public string? SourceSavePath { get; init; }
    public string? SourceContainer { get; init; }
    public int SourceSlot { get; init; } = -1;
    public string? SourceFingerprint { get; init; }
    public byte[]? SourceRubyMarshal { get; init; }

    public string? Nickname { get; init; }
    public string? OriginalTrainerName { get; init; }
    public ushort TID16 { get; init; }
    public ushort SID16 { get; init; }
    public uint PID { get; init; }
    public uint EXP { get; init; }
    public byte Gender { get; init; }
    public byte Nature { get; init; }
    public int HeldItem { get; init; }
    public int Ability { get; init; }
    public int AbilityNumber { get; init; }
    public byte Friendship { get; init; } = 70;
    public bool IsEgg { get; init; }
    public byte Ball { get; init; }
    public byte MetLevel { get; init; }
    public byte OriginalTrainerGender { get; init; }

    public ushort[]? Moves { get; init; }
    public int[]? MovePP { get; init; }
    public int[]? MovePPUps { get; init; }
    public int[]? IVs { get; init; }
    public int[]? EVs { get; init; }
    public int[]? BaseStats { get; init; }
    public int[]? Stats { get; init; }
    public int CurrentHP { get; init; }
    public int StatusCondition { get; init; }
    public int ExpGrowth { get; init; }
    public byte GenderRatio { get; init; } = PersonalInfo.RatioMagicGenderless;
    public byte BaseFriendship { get; init; } = 70;
    public byte CatchRate { get; init; }
    public byte HatchCycles { get; init; }
    public int BaseEXP { get; init; }
    public int[]? AbilityIds { get; init; }
}


[JsonSourceGenerationOptions(
    GenerationMode = JsonSourceGenerationMode.Metadata,
    PropertyNamingPolicy = JsonKnownNamingPolicy.Unspecified
)]
[JsonSerializable(typeof(EssentialsPkmPayload))]
internal partial class EssentialsJsonContext : JsonSerializerContext
{
}
