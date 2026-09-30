from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: patch_pkvault_v8_alpha53h.py <pkvault-src> <pkhex-src>")

pkvault = Path(sys.argv[1]).resolve()
pkhex = Path(sys.argv[2]).resolve()

def replace_once(path: Path, old: str, new: str, already: str):
    text = path.read_text(encoding="utf-8")
    if already in text:
        return
    if old not in text:
        raise RuntimeError(f"alpha53h anchor missing: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# PKHeX: recognize the exact RedFox/mGBA Silver v4 extended Unown shiny rule.
# Vanilla Gen-II shininess remains unchanged and is still checked separately.
# ---------------------------------------------------------------------------
shiny = pkhex / "PKHeX.Core/Legality/RNG/Util/ShinyUtil.cs"
replace_once(
    shiny,
    '''    public static bool GetIsShinyGB(ushort dv16) => (dv16 & 0x2FFF) == 0x2AAA;
}''',
    '''    public static bool GetIsShinyGB(ushort dv16) => (dv16 & 0x2FFF) == 0x2AAA;

    /// <summary>
    /// Checks the RedFox/mGBA "Gen2 Extended Unown Shiny v1" DV signature.
    /// This is the finished Pokémon Silver v4 rule and deliberately preserves
    /// all A-Z Unown forms. Vanilla Gen-II shininess remains GetIsShinyGB.
    /// </summary>
    public static bool GetIsShinyGBExtendedUnown(ushort dv16)
    {
        byte dv1 = (byte)(dv16 >> 8);
        byte dv2 = (byte)dv16;
        return (dv1 & 0x99) == 0x08 && (dv2 & 0xBF) == 0xAA;
    }
}''',
    "GetIsShinyGBExtendedUnown",
)

gb = pkhex / "PKHeX.Core/PKM/Shared/GBPKM.cs"
replace_once(
    gb,
    '    public sealed override bool IsShiny => ShinyUtil.GetIsShinyGB(DV16);\n',
    '''    public sealed override bool IsShiny => ShinyUtil.GetIsShinyGB(DV16)
        || (Species == (ushort)Core.Species.Unown && ShinyUtil.GetIsShinyGBExtendedUnown(DV16));
''',
    "ShinyUtil.GetIsShinyGBExtendedUnown(DV16)",
)

# ---------------------------------------------------------------------------
# PKVault compatibility bridge.
# The Silver-only DV encoding is a source representation, not a portable one:
# when leaving Gen II we construct a normal vanilla Gen-III shiny PID that
# preserves the Unown letter and nature. Later converters carry that vanilla
# shiny state forward.
# ---------------------------------------------------------------------------
bridge = pkvault / "PKVault.Core/storage/services/PkmConvertService/Gen2ExtendedUnownShinyBridge.cs"
bridge.write_text(r'''using System.Numerics;
using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Compatibility bridge for the mGBA Pokémon Silver "Gen2 Extended Unown Shiny v1" scheme.
/// Silver stores A-Z form and shiny state in the same Gen-II DVs, so non-I/V forms use an
/// extension signature while in Silver. Once converted to Gen III+, shininess is re-encoded
/// into a normal vanilla PID and the Unown letter is preserved.
/// </summary>
public static class Gen2ExtendedUnownShinyBridge
{
    public const string CompatibilityId = "Gen2 Extended Unown Shiny v1";

    public static bool IsExtended(PKM pkm) => pkm is GBPKM gb
        && pkm.Species == (ushort)Species.Unown
        && ShinyUtil.GetIsShinyGBExtendedUnown(gb.DV16);

    public static bool IsRecognizedShiny(PKM pkm) => pkm.IsShiny || IsExtended(pkm);

    // Stock Gen II can only combine shiny + the same Unown letter for I and V.
    public static bool CanVanillaGen2RepresentForm(byte form) => form is 8 or 21;

    /// <summary>
    /// Re-encodes a Gen-II Unown shiny while preserving the requested form.
    /// I/V use a stock Gen-II shiny DV. Every other A-Z form uses the Silver
    /// extension signature.
    /// </summary>
    public static void ApplySilverShiny(PK2 pk2, byte form)
    {
        if (pk2.Species != (ushort)Species.Unown)
            throw new ArgumentException("Extended Gen-II shiny encoding only applies to Unown.", nameof(pk2));
        if (form > 25)
            throw new InvalidOperationException("Generation II only supports Unown A-Z.");

        ushort? dv = CanVanillaGen2RepresentForm(form)
            ? FindBestDV(pk2.DV16, form, vanillaOnly: true)
            : FindBestDV(pk2.DV16, form, vanillaOnly: false);

        if (dv is null)
            throw new InvalidOperationException($"No Gen-II shiny DV signature found for Unown form {form}.");

        pk2.DV16 = dv.Value;
    }

    /// <summary>
    /// Re-encodes a recognized Gen-II shiny Unown as a completely normal
    /// vanilla Gen-III shiny PID, preserving both its Unown letter and nature.
    /// </summary>
    public static void ApplyVanillaGen3Shiny(PK3 pk3, byte form)
    {
        if (pk3.Species != (ushort)Species.Unown)
            throw new ArgumentException("Gen-II Unown bridge only applies to Unown.", nameof(pk3));
        if (form > 27)
            throw new InvalidOperationException($"Invalid Gen-III Unown form {form}.");

        var preferred = pk3.PID;
        var nature = pk3.Nature;
        if (IsValidGen3Pid(pk3, preferred, form, nature))
            return;

        ushort start = (ushort)preferred;
        for (int offset = 0; offset <= ushort.MaxValue; offset++)
        {
            ushort low = (ushort)(start + offset);
            for (uint shinyXor = 0; shinyXor < 8; shinyXor++)
            {
                ushort high = (ushort)(low ^ pk3.TID16 ^ pk3.SID16 ^ shinyXor);
                uint pid = ((uint)high << 16) | low;
                if (!IsValidGen3Pid(pk3, pid, form, nature))
                    continue;

                pk3.PID = pid;
                return;
            }
        }

        throw new InvalidOperationException(
            $"Could not create a vanilla shiny Gen-III PID for Unown form {form}.");
    }

    private static bool IsValidGen3Pid(PK3 pk3, uint pid, byte form, Nature nature)
        => ShinyUtil.GetIsShiny3(pk3.ID32, pid)
            && EntityPID.GetUnownForm3(pid) == form
            && (Nature)(pid % 25) == nature;

    private static ushort? FindBestDV(ushort preferred, byte form, bool vanillaOnly)
    {
        ushort best = 0;
        int bestDistance = int.MaxValue;
        bool found = false;

        for (int raw = 0; raw <= ushort.MaxValue; raw++)
        {
            ushort dv = (ushort)raw;
            bool shiny = vanillaOnly
                ? ShinyUtil.GetIsShinyGB(dv)
                : ShinyUtil.GetIsShinyGBExtendedUnown(dv);
            if (!shiny || GetUnownForm(dv) != form)
                continue;

            int distance = BitOperations.PopCount((uint)(dv ^ preferred));
            if (distance >= bestDistance)
                continue;

            best = dv;
            bestDistance = distance;
            found = true;
            if (distance == 0)
                break;
        }

        return found ? best : null;
    }

    private static byte GetUnownForm(ushort dv16)
    {
        int atk = (dv16 >> 12) & 0xF;
        int def = (dv16 >> 8) & 0xF;
        int spe = (dv16 >> 4) & 0xF;
        int spc = dv16 & 0xF;

        ushort value = 0;
        value |= (ushort)((atk & 0x6) << 5);
        value |= (ushort)((def & 0x6) << 3);
        value |= (ushort)((spe & 0x6) << 1);
        value |= (ushort)((spc & 0x6) >> 1);
        return (byte)(value / 10);
    }
}
''', encoding="utf-8")

# PK2 -> PK3: once the destination IDs exist, replace the Silver-only
# representation with a vanilla shiny Gen-III PID, keeping the letter.
pk2c = pkvault / "PKVault.Core/storage/services/PkmConvertService/PK2Converter.cs"
replace_once(
    pk2c,
    '''        utils.FixSID(pk3);

        utils.CopyHeldItemFrom(pk3, pk2.HeldItem, pk2.Context, pk2.Version);''',
    '''        utils.FixSID(pk3);

        if (pk2.Species == (ushort)Species.Unown && Gen2ExtendedUnownShinyBridge.IsRecognizedShiny(pk2))
            Gen2ExtendedUnownShinyBridge.ApplyVanillaGen3Shiny(pk3, pk2.Form);

        utils.CopyHeldItemFrom(pk3, pk2.HeldItem, pk2.Context, pk2.Version);''',
    "Gen2ExtendedUnownShinyBridge.ApplyVanillaGen3Shiny(pk3, pk2.Form)",
)

# PK3 -> PK2: Silver can use the extension; Gold/Crystal cannot represent
# non-I/V shiny Unown without changing either shininess or the letter.
pk3c = pkvault / "PKVault.Core/storage/services/PkmConvertService/PK3Converter.cs"
replace_once(
    pk3c,
    '''        utils.FixPersonalData(pk2, pk3.IsShiny, pk3.Form, pk3.Gender, pk2.Nature, pk2.Ability, false, ctx);

        utils.CopyMovesFrom(pk2, pk3);''',
    '''        var desiredForm = pk3.Form;
        utils.FixPersonalData(pk2, pk3.IsShiny, desiredForm, pk3.Gender, pk2.Nature, pk2.Ability, false, ctx);

        if (pk3.Species == (ushort)Species.Unown && pk3.IsShiny)
        {
            var targetVersion = ctx.TargetSave?.Version;
            if (targetVersion is GameVersion.GD or GameVersion.C
                && !Gen2ExtendedUnownShinyBridge.CanVanillaGen2RepresentForm(desiredForm))
            {
                throw new InvalidOperationException(
                    $"Vanilla {targetVersion} cannot represent shiny Unown form {desiredForm} while preserving its letter. " +
                    "Use Pokémon Silver with the Gen2 Extended Unown Shiny v1 bridge, or a Gen III+ save.");
            }

            Gen2ExtendedUnownShinyBridge.ApplySilverShiny(pk2, desiredForm);
        }

        utils.CopyMovesFrom(pk2, pk3);''',
    "Gen2ExtendedUnownShinyBridge.ApplySilverShiny(pk2, desiredForm)",
)

# Same-format GB writes must not call stock SetShiny() over an already-recognized
# extended Unown and destroy its form-preserving DV signature.
fixer = pkvault / "PKVault.Core/storage/services/PkmConvertService/utils/PKMPersonalFixer.cs"
replace_once(
    fixer,
    '''                if (isShiny)
                    gbpkm.SetShiny();
                else
                    gbpkm.SetPIDGender(gender);''',
    '''                if (isShiny)
                {
                    if (!gbpkm.IsShiny)
                        gbpkm.SetShiny();
                }
                else
                    gbpkm.SetPIDGender(gender);''',
    "if (!gbpkm.IsShiny)",
)

# Synchronization normally avoids copying PID from a GB source. Extended shiny
# Unown is the exception: its PK2->PK3 conversion intentionally generated the
# destination's real vanilla shiny PID and that PID must reach the target.
share = pkvault / "PKVault.Core/storage/services/PkmConvertService/PkmSharePropertiesService.cs"
replace_once(
    share,
    '''        var resultPkm = result.GetMutablePkm();

        targetPkm.Species = resultPkm.Species;''',
    '''        var resultPkm = result.GetMutablePkm();

        // Normalize a shiny Unown for the actual destination save even when both
        // source and target are PK2, which otherwise bypasses recursive conversion.
        if (targetPkm is PK2
            && resultPkm is PK2 resultPk2ForTarget
            && resultPk2ForTarget.Species == (ushort)Species.Unown
            && Gen2ExtendedUnownShinyBridge.IsRecognizedShiny(resultPk2ForTarget))
        {
            var desiredForm = sourcePkm.Form;
            var targetVersion = save?.Version;
            if (targetVersion is GameVersion.GD or GameVersion.C
                && !Gen2ExtendedUnownShinyBridge.CanVanillaGen2RepresentForm(desiredForm))
            {
                throw new InvalidOperationException(
                    $"Vanilla {targetVersion} cannot represent shiny Unown form {desiredForm} while preserving its letter. " +
                    "Use Pokémon Silver with the Gen2 Extended Unown Shiny v1 bridge, or a Gen III+ save.");
            }

            Gen2ExtendedUnownShinyBridge.ApplySilverShiny(resultPk2ForTarget, desiredForm);
        }

        targetPkm.Species = resultPkm.Species;''',
    "resultPk2ForTarget",
)

replace_once(
    share,
    '''        if (sourcePkm is not GBPKM)
        {
            targetPkm.Nature = resultPkm.Nature;''',
    '''        var sourceGen2Shiny = sourcePkm is GBPKM
            && Gen2ExtendedUnownShinyBridge.IsRecognizedShiny(sourcePkm);
        if (sourcePkm is not GBPKM || sourceGen2Shiny)
        {
            targetPkm.Nature = resultPkm.Nature;''',
    "sourceGen2Shiny",
)

replace_once(
    share,
    '''        if (sourcePkm is not PB7)
        {
            var resultIVs = utils.GetAllIVs(resultPkm);''',
    '''        if (targetPkm is PK2 targetPk2
            && resultPkm is PK2 resultPk2
            && resultPk2.Species == (ushort)Species.Unown
            && Gen2ExtendedUnownShinyBridge.IsRecognizedShiny(resultPk2))
        {
            targetPk2.DV16 = resultPk2.DV16;
        }
        else if (sourcePkm is not PB7)
        {
            var resultIVs = utils.GetAllIVs(resultPkm);''',
    "targetPk2.DV16 = resultPk2.DV16",
)

# Regression tests for the exact v4 signature and the portable Gen-III encoding.
test = pkvault / "PKVault.Core.Tests/storage/Gen2ExtendedUnownShinyBridgeTests.cs"
test.parent.mkdir(parents=True, exist_ok=True)
test.write_text(r'''using PKHeX.Core;
using PKVault.Core;

public class Gen2ExtendedUnownShinyBridgeTests
{
    [Fact]
    public void ExtendedRuleHas32SignaturesAndCoversAZ()
    {
        var forms = new HashSet<byte>();
        int count = 0;

        for (int raw = 0; raw <= ushort.MaxValue; raw++)
        {
            ushort dv = (ushort)raw;
            if (!ShinyUtil.GetIsShinyGBExtendedUnown(dv))
                continue;

            count++;
            var pk2 = new PK2 { Species = (ushort)Species.Unown, DV16 = dv };
            forms.Add(pk2.Form);
        }

        Assert.Equal(32, count);
        Assert.Equal(26, forms.Count);
        Assert.True(Enumerable.Range(0, 26).All(i => forms.Contains((byte)i)));
    }

    [Fact]
    public void CombinedRuleHas38Gen2ShinyDvCombinations()
    {
        int count = 0;
        for (int raw = 0; raw <= ushort.MaxValue; raw++)
        {
            ushort dv = (ushort)raw;
            if (ShinyUtil.GetIsShinyGB(dv) || ShinyUtil.GetIsShinyGBExtendedUnown(dv))
                count++;
        }

        Assert.Equal(38, count);
    }

    [Fact]
    public void OnlyIAndVAreVanillaGen2ShinyUnownForms()
    {
        var forms = new HashSet<byte>();
        for (int raw = 0; raw <= ushort.MaxValue; raw++)
        {
            ushort dv = (ushort)raw;
            if (!ShinyUtil.GetIsShinyGB(dv))
                continue;

            var pk2 = new PK2 { Species = (ushort)Species.Unown, DV16 = dv };
            forms.Add(pk2.Form);
        }

        Assert.Equal([8, 21], forms.Order().Select(x => (int)x).ToArray());
        Assert.True(Gen2ExtendedUnownShinyBridge.CanVanillaGen2RepresentForm(8));
        Assert.True(Gen2ExtendedUnownShinyBridge.CanVanillaGen2RepresentForm(21));
        Assert.False(Gen2ExtendedUnownShinyBridge.CanVanillaGen2RepresentForm(12));
    }

    [Theory]
    [InlineData(0)]  // A
    [InlineData(12)] // M
    [InlineData(25)] // Z
    public void SilverExtendedShinyPreservesLetter(byte form)
    {
        var pk2 = new PK2 { Species = (ushort)Species.Unown, DV16 = 0xFFFF };

        Gen2ExtendedUnownShinyBridge.ApplySilverShiny(pk2, form);

        Assert.Equal(form, pk2.Form);
        Assert.True(pk2.IsShiny);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(12)]
    [InlineData(25)]
    public void Gen3VanillaShinyPreservesLetterAndNature(byte form)
    {
        var pk3 = new PK3
        {
            Species = (ushort)Species.Unown,
            TID16 = 12345,
            SID16 = 54321,
            PID = 0x12345678,
        };
        var nature = pk3.Nature;

        Gen2ExtendedUnownShinyBridge.ApplyVanillaGen3Shiny(pk3, form);

        Assert.True(pk3.IsShiny);
        Assert.Equal(form, pk3.Form);
        Assert.Equal(nature, pk3.Nature);
        Assert.True(ShinyUtil.GetIsShiny3(pk3.ID32, pk3.PID));
    }
}
''', encoding="utf-8")

print("PASS alpha53h Gen2 Extended Unown Shiny v1 bridge")
