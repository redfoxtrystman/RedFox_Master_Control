using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Explicit cross-game conversion rules for Pokémon Essentials profiles.
/// Insurgence intentionally accepts only species its own data contains.
/// </summary>
public static class EssentialsInterop
{
    public static bool CanImportTo(EssentialsLegacySaveFile target, ImmutablePKM source)
    {
        if (source.GetMutablePkm() is PKEssentials existing)
            return string.Equals(existing.ProfileId, target.ProfileId, StringComparison.Ordinal)
                && !existing.ReadOnlySource
                && existing.SourceRubyMarshal.Length > 0;

        if (!string.Equals(target.ProfileId, InsurgenceProfileGenerated.ProfileId, StringComparison.Ordinal))
            return false;

        var mutable = source.GetMutablePkm();
        if (mutable is PK1 pk1 && PokeList1.IsMissingNo50(pk1))
            return true;
        if (mutable is PK1 otherGlitch && PokeList1.IsKnownGen1Glitch(otherGlitch))
            return false;

        return InsurgenceProfileGenerated.IsOfficialSpecies(source.Species);
    }

    public static ImmutablePKM ImportTo(EssentialsLegacySaveFile target, ImmutablePKM source)
    {
        if (source.GetMutablePkm() is PKEssentials existing)
        {
            if (!string.Equals(existing.ProfileId, target.ProfileId, StringComparison.Ordinal))
                throw new InvalidOperationException($"Cross-profile Essentials conversion blocked: {existing.ProfileId} -> {target.ProfileId}.");
            if (existing.ReadOnlySource || existing.SourceRubyMarshal.Length == 0)
                throw new InvalidOperationException("Essentials Pokémon lacks a writable Ruby source template.");
            return new((PKEssentials)existing.Clone());
        }

        if (!string.Equals(target.ProfileId, InsurgenceProfileGenerated.ProfileId, StringComparison.Ordinal))
            throw new InvalidOperationException($"Official Pokémon cannot be imported into {target.ProfileId}; only Insurgence has an explicit official-species mapping.");

        var mutable = source.GetMutablePkm();
        if (mutable is PK1 missingNo && PokeList1.IsMissingNo50(missingNo))
            return BuildInsurgenceMissingNo(target, missingNo);

        if (mutable is PK1 glitch && PokeList1.IsKnownGen1Glitch(glitch))
            throw new InvalidOperationException("Only raw-50 MISSINGNO maps to Insurgence MISSINGNO #722. Raw-00 'M is intentionally not aliased.");

        if (!InsurgenceProfileGenerated.IsOfficialSpecies(source.Species))
            throw new InvalidOperationException(
                $"Species {source.Species} is not present in Pokémon Insurgence. Official imports are limited to National Dex 1-{InsurgenceProfileGenerated.OfficialMaxSpecies}.");

        return BuildInsurgenceOfficial(target, mutable);
    }

    private static ImmutablePKM BuildInsurgenceOfficial(EssentialsLegacySaveFile target, PKM source)
    {
        var species = source.Species;
        var name = SafeName(GameInfo.Strings.Species, species, $"Species {species}");
        var personal = PersonalTable.AO.GetFormEntry(species, 0);
        var types = GetTypeNames(personal);
        var moves = SanitizeMoves([source.Move1, source.Move2, source.Move3, source.Move4]);
        var heldItem = source.HeldItem <= InsurgenceProfileGenerated.MaxOfficialItemId ? source.HeldItem : 0;
        var ability = source.Ability <= InsurgenceProfileGenerated.MaxOfficialAbilityId ? source.Ability : 0;
        var ball = source.Ball <= InsurgenceProfileGenerated.MaxOfficialBallId ? source.Ball : (byte)Ball.Poke;

        var template = target.CreateWritableTemplate();
        var payload = template.ToPayload() with
        {
            ProfileId = target.ProfileId,
            ProfileVersion = target.ProfileVersion,
            SpeciesName = name,
            TypeNames = types,
            AbilityName = SafeName(GameInfo.Strings.Ability, ability, ""),
            ItemName = SafeName(GameInfo.Strings.Item, heldItem, ""),
            MoveNames = moves.Select(z => SafeName(GameInfo.Strings.Move, z, "")).ToArray(),
            LocalSpeciesId = species,
            LocalFormId = 0,
            Level = (byte)Math.Clamp(source.CurrentLevel, 1, 120),
            ReadOnlySource = false,
            SourceSavePath = target.Metadata.FilePath,
            SourceContainer = "import",
            SourceSlot = -1,
            SourceFingerprint = $"import-official-{species}-{source.PID:X8}",
            Nickname = source.IsNicknamed ? source.Nickname : name,
            OriginalTrainerName = source.OriginalTrainerName,
            TID16 = source.TID16,
            SID16 = source.SID16,
            PID = source.PID,
            EXP = source.EXP,
            Gender = source.Gender,
            Nature = (byte)source.Nature,
            HeldItem = heldItem,
            Ability = ability,
            AbilityNumber = source.AbilityNumber,
            Friendship = source.CurrentFriendship,
            IsEgg = source.IsEgg,
            Ball = ball,
            MetLevel = source.MetLevel,
            OriginalTrainerGender = source.OriginalTrainerGender,
            Moves = moves,
            MovePP = [
                moves[0] == 0 ? 0 : source.Move1_PP,
                moves[1] == 0 ? 0 : source.Move2_PP,
                moves[2] == 0 ? 0 : source.Move3_PP,
                moves[3] == 0 ? 0 : source.Move4_PP
            ],
            MovePPUps = [source.Move1_PPUps, source.Move2_PPUps, source.Move3_PPUps, source.Move4_PPUps],
            IVs = [source.IV_HP, source.IV_ATK, source.IV_DEF, source.IV_SPE, source.IV_SPA, source.IV_SPD],
            EVs = [source.EV_HP, source.EV_ATK, source.EV_DEF, source.EV_SPE, source.EV_SPA, source.EV_SPD],
            BaseStats = [personal.HP, personal.ATK, personal.DEF, personal.SPE, personal.SPA, personal.SPD],
            Stats = [source.Stat_HPMax, source.Stat_ATK, source.Stat_DEF, source.Stat_SPE, source.Stat_SPA, source.Stat_SPD],
            CurrentHP = source.Stat_HPCurrent,
            StatusCondition = source.Status_Condition,
            ExpGrowth = personal.EXPGrowth,
            GenderRatio = personal.Gender,
            BaseFriendship = personal.BaseFriendship,
            CatchRate = personal.CatchRate,
            HatchCycles = personal.HatchCycles,
            BaseEXP = personal.BaseEXP,
            AbilityIds = Enumerable.Range(0, personal.AbilityCount)
                .Select(personal.GetAbilityAtIndex)
                .Where(z => z > 0 && z <= InsurgenceProfileGenerated.MaxOfficialAbilityId)
                .Distinct()
                .ToArray(),
        };

        return new(new PKEssentials(payload));
    }

    private static ImmutablePKM BuildInsurgenceMissingNo(EssentialsLegacySaveFile target, PK1 source)
    {
        var template = target.CreateWritableTemplate();
        var moves = SanitizeMoves([source.Move1, source.Move2, source.Move3, source.Move4]);
        var payload = template.ToPayload() with
        {
            ProfileId = target.ProfileId,
            ProfileVersion = target.ProfileVersion,
            SpeciesName = "MISSINGNO",
            TypeNames = ["Flying", "Normal"],
            AbilityName = "Glitch",
            ItemName = "",
            MoveNames = moves.Select(z => SafeName(GameInfo.Strings.Move, z, "")).ToArray(),
            LocalSpeciesId = InsurgenceProfileGenerated.MissingNoSpecies,
            LocalFormId = 0,
            Level = (byte)Math.Clamp(source.CurrentLevel, 1, 120),
            ReadOnlySource = false,
            SourceSavePath = target.Metadata.FilePath,
            SourceContainer = "import",
            SourceSlot = -1,
            SourceFingerprint = $"import-missingno-{source.PID:X8}",
            Nickname = "MISSINGNO",
            OriginalTrainerName = source.OriginalTrainerName,
            TID16 = source.TID16,
            SID16 = source.SID16,
            PID = source.PID,
            EXP = source.EXP,
            Gender = (byte)Gender.Genderless,
            Nature = (byte)Nature.Hardy,
            HeldItem = 0,
            Ability = 0,
            AbilityNumber = 0,
            Friendship = 70,
            IsEgg = false,
            Ball = (byte)Ball.Poke,
            MetLevel = source.MetLevel,
            OriginalTrainerGender = source.OriginalTrainerGender,
            Moves = moves,
            MovePP = [source.Move1_PP, source.Move2_PP, source.Move3_PP, source.Move4_PP],
            MovePPUps = [0,0,0,0],
            IVs = [source.IV_HP, source.IV_ATK, source.IV_DEF, source.IV_SPE, source.IV_SPA, source.IV_SPD],
            EVs = [source.EV_HP, source.EV_ATK, source.EV_DEF, source.EV_SPE, source.EV_SPA, source.EV_SPD],
            BaseStats = [33,136,0,29,6,6],
            Stats = [source.Stat_HPMax, source.Stat_ATK, source.Stat_DEF, source.Stat_SPE, source.Stat_SPA, source.Stat_SPD],
            CurrentHP = source.Stat_HPCurrent,
            StatusCondition = source.Status_Condition,
            ExpGrowth = 0,
            GenderRatio = PersonalInfo.RatioMagicGenderless,
            BaseFriendship = 70,
            CatchRate = 35,
            HatchCycles = 0,
            BaseEXP = 0,
            AbilityIds = [],
        };
        return new(new PKEssentials(payload));
    }

    private static ushort[] SanitizeMoves(ushort[] moves)
        => moves.Select(z => z <= InsurgenceProfileGenerated.MaxOfficialMoveId ? z : (ushort)0).ToArray();

    private static string[] GetTypeNames(PersonalInfo personal)
    {
        var first = SafeName(GameInfo.Strings.Types, personal.Type1, "");
        var second = SafeName(GameInfo.Strings.Types, personal.Type2, "");
        if (string.IsNullOrWhiteSpace(second) || string.Equals(first, second, StringComparison.Ordinal))
            return [first];
        return [first, second];
    }

    private static string SafeName(IReadOnlyList<string> values, int id, string fallback)
        => id >= 0 && id < values.Count ? values[id] : fallback;
}
