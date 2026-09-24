using System;

namespace PKHeX.Core;

/// <summary>
/// Compatibility helpers for pokeemerald-expansion based ROM hacks that store
/// National-Dex species constants directly in the Gen-3 PKM species field.
/// Vanilla R/S/E/FR/LG must leave this mode disabled.
/// </summary>
public static class Gen3DirectSpecies
{
    // pokeemerald-expansion constants used by Too Many Types v1.6's 2023 base.
    public const ushort FormsStart = 905;
    public const ushort PonytaGalarian = FormsStart + 70;       // 975
    public const ushort RapidashGalarian = FormsStart + 71;     // 976
    public const ushort LycanrocMidnight = FormsStart + 268;    // 1173
    public const ushort WishiwashiSchool = FormsStart + 270;    // 1175

    public const ushort MaxBaseSpecies = 905;
    public const ushort MaxDirectMove = 1023;

    public static ushort GetSpecies(ushort raw) => raw switch
    {
        PonytaGalarian => (ushort)Core.Species.Ponyta,
        RapidashGalarian => (ushort)Core.Species.Rapidash,
        LycanrocMidnight => (ushort)Core.Species.Lycanroc,
        WishiwashiSchool => (ushort)Core.Species.Wishiwashi,
        _ when raw <= MaxBaseSpecies => raw,
        _ => 0,
    };

    public static byte GetForm(ushort raw) => raw switch
    {
        PonytaGalarian or RapidashGalarian or LycanrocMidnight or WishiwashiSchool => 1,
        _ => 0,
    };

    public static bool TryGetRaw(ushort species, byte form, out ushort raw)
    {
        if (form == 0 && species <= MaxBaseSpecies)
        {
            raw = species;
            return true;
        }

        raw = (species, form) switch
        {
            ((ushort)Core.Species.Ponyta, 1) => PonytaGalarian,
            ((ushort)Core.Species.Rapidash, 1) => RapidashGalarian,
            ((ushort)Core.Species.Lycanroc, 1) => LycanrocMidnight,
            ((ushort)Core.Species.Wishiwashi, 1) => WishiwashiSchool,
            _ => 0,
        };
        return raw != 0;
    }

    public static PersonalInfo3 GetPersonal(ushort species, byte form)
    {
        if (species <= Legal.MaxSpeciesID_3)
            return PersonalTable.RS[species];

        PersonalInfo src = GetModernPersonal(species, form);
        var result = new PersonalInfo3(new byte[PersonalInfo3.SIZE])
        {
            HP = src.HP,
            ATK = src.ATK,
            DEF = src.DEF,
            SPE = src.SPE,
            SPA = src.SPA,
            SPD = src.SPD,
            Type1 = src.Type1,
            Type2 = src.Type2,
            CatchRate = src.CatchRate,
            BaseEXP = Math.Min(byte.MaxValue, src.BaseEXP),
            EV_HP = src.EV_HP,
            EV_ATK = src.EV_ATK,
            EV_DEF = src.EV_DEF,
            EV_SPE = src.EV_SPE,
            EV_SPA = src.EV_SPA,
            EV_SPD = src.EV_SPD,
            Gender = src.Gender,
            HatchCycles = src.HatchCycles,
            BaseFriendship = src.BaseFriendship,
            EXPGrowth = src.EXPGrowth,
            EggGroup1 = src.EggGroup1,
            EggGroup2 = src.EggGroup2,
            EscapeRate = src.EscapeRate,
            Color = src.Color,
        };

        result.Ability1 = ClampAbility(src, 0);
        result.Ability2 = src.AbilityCount > 1 ? ClampAbility(src, 1) : result.Ability1;
        return result;
    }

    private static int ClampAbility(PersonalInfo info, int index)
    {
        var value = info.GetAbilityAtIndex(index);
        return (uint)value <= byte.MaxValue ? value : 0;
    }

    private static PersonalInfo GetModernPersonal(ushort species, byte form)
    {
        var sv = PersonalTable.SV[species, form];
        if (sv.HP != 0)
            return sv;

        var swsh = PersonalTable.SWSH[species, form];
        if (swsh.HP != 0)
            return swsh;

        var usum = PersonalTable.USUM[species, form];
        if (usum.HP != 0)
            return usum;

        throw new ArgumentOutOfRangeException(nameof(species), $"No personal data available for direct Gen-3 species {species}, form {form}.");
    }
}
