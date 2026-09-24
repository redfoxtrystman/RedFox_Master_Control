using PKHeX.Core;

namespace PKVault.Core;

public static class TooManyTypesCompat
{
    public const string StorageExtension = "tmt3";
    public const ushort VanillaGen3MaxMove = 354;
    public const ushort CanonicalExpansionMoveMax = 826;

    public static bool IsTmt(PKM pkm) => pkm is PK3 { DirectSpeciesIDs: true };
    public static bool IsTmt(ImmutablePKM pkm) => IsTmt(pkm.GetMutablePkm());
    public static bool IsTmt(SaveFile save) => save is SAV3 { DirectSpeciesIDs: true };

    public static string GetStorageExtension(ImmutablePKM pkm) => IsTmt(pkm) ? StorageExtension : pkm.Extension;

    public static bool ConfigureSave(SaveFile save, string path)
    {
        if (save is not SAV3E emerald)
            return false;

        if (!LooksLikeTmt(emerald, path))
            return false;

        emerald.DirectSpeciesIDs = true;
        return true;
    }

    private static bool LooksLikeTmt(SAV3E save, string path)
    {
        var fileName = Path.GetFileName(path);
        if (fileName.Contains("TooManyTypes", StringComparison.OrdinalIgnoreCase) ||
            fileName.Contains("Too Many Types", StringComparison.OrdinalIgnoreCase))
            return true;

        foreach (var pkm in save.PartyData.OfType<PK3>())
        {
            if (IsExpandedTmtRecord(pkm))
                return true;
        }

        for (var box = 0; box < save.BoxCount; box++)
        {
            foreach (var pkm in save.GetBoxData(box).OfType<PK3>())
            {
                if (IsExpandedTmtRecord(pkm))
                    return true;
            }
        }

        return false;
    }

    private static bool IsExpandedTmtRecord(PK3 pkm)
    {
        if (pkm.SpeciesInternal > LegalMaxVanillaGen3Species &&
            TooManyTypesProfileGenerated.TryGetRaw(pkm.SpeciesInternal, out _))
            return true;

        return pkm.Move1 > VanillaGen3MaxMove || pkm.Move2 > VanillaGen3MaxMove ||
               pkm.Move3 > VanillaGen3MaxMove || pkm.Move4 > VanillaGen3MaxMove;
    }

    private const ushort LegalMaxVanillaGen3Species = 386;

    public static TmtSpeciesEntry RequireSupported(ushort species, byte form)
    {
        if (!TooManyTypesProfileGenerated.TryGet(species, form, out var entry))
            throw new InvalidOperationException($"Species/form {species}:{form} is not available in Too Many Types v1.6.");
        return entry;
    }

    public static string[]? GetTypes(ImmutablePKM pkm)
    {
        if (!IsTmt(pkm))
            return null;
        return TooManyTypesProfileGenerated.TryGet(pkm.Species, pkm.Form, out var entry)
            ? entry.Types
            : null;
    }

    public static PK3 ConvertDirectToVanilla(PK3 source, SaveFile targetSave)
    {
        var species = source.Species;
        var form = source.Form;
        if (species is 0 or > LegalMaxVanillaGen3Species)
            throw new InvalidOperationException($"{species} cannot be represented in vanilla Generation 3.");
        if (form != 0 && species != (ushort)Species.Unown)
            throw new InvalidOperationException($"Species {species} form {form} cannot be represented in vanilla Generation 3.");

        var result = source.Clone();
        result.DirectSpeciesIDs = false;
        result.Species = species;
        if (species == (ushort)Species.Unown)
            result.Form = form;

        if (result.Move1 > VanillaGen3MaxMove) result.Move1 = 0;
        if (result.Move2 > VanillaGen3MaxMove) result.Move2 = 0;
        if (result.Move3 > VanillaGen3MaxMove) result.Move3 = 0;
        if (result.Move4 > VanillaGen3MaxMove) result.Move4 = 0;
        if (result.HeldItem > targetSave.MaxItemID) result.HeldItem = 0;
        if (result.Ball > targetSave.MaxBallID) result.Ball = 4;
        result.RefreshChecksum();
        return result;
    }

    public static void ApplyTmtIdentity(PK3 result, ImmutablePKM source)
    {
        var entry = RequireSupported(source.Species, source.Form);
        result.DirectSpeciesIDs = true;
        result.Species = entry.Species;
        result.Form = entry.Form;

        bool preserveCustom = IsTmt(source);
        result.Move1 = NormalizeMove(source.Move1, preserveCustom);
        result.Move2 = NormalizeMove(source.Move2, preserveCustom);
        result.Move3 = NormalizeMove(source.Move3, preserveCustom);
        result.Move4 = NormalizeMove(source.Move4, preserveCustom);
        result.Move1_PP = source.Move1_PP;
        result.Move2_PP = source.Move2_PP;
        result.Move3_PP = source.Move3_PP;
        result.Move4_PP = source.Move4_PP;
        result.Move1_PPUps = source.Move1_PPUps;
        result.Move2_PPUps = source.Move2_PPUps;
        result.Move3_PPUps = source.Move3_PPUps;
        result.Move4_PPUps = source.Move4_PPUps;

        result.EXP = source.EXP;
        result.EV_HP = source.EV_HP;
        result.EV_ATK = source.EV_ATK;
        result.EV_DEF = source.EV_DEF;
        result.EV_SPE = source.EV_SPE;
        result.EV_SPA = source.EV_SPA;
        result.EV_SPD = source.EV_SPD;
        result.IV_HP = source.IV_HP;
        result.IV_ATK = source.IV_ATK;
        result.IV_DEF = source.IV_DEF;
        result.IV_SPE = source.IV_SPE;
        result.IV_SPA = source.IV_SPA;
        result.IV_SPD = source.IV_SPD;
        result.OriginalTrainerFriendship = source.OriginalTrainerFriendship;
        result.PokerusStrain = source.PokerusStrain;
        result.PokerusDays = source.PokerusDays;
        result.Nickname = source.Nickname;
        result.OriginalTrainerName = source.OriginalTrainerName;
        result.RefreshChecksum();
    }

    private static ushort NormalizeMove(ushort move, bool preserveCustom)
    {
        if (move == 0)
            return 0;
        if (move <= CanonicalExpansionMoveMax)
            return move;
        if (preserveCustom && move <= Gen3DirectSpecies.MaxDirectMove)
            return move;
        return 0;
    }
}
