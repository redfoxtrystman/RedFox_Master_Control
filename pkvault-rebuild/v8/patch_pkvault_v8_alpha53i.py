from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: patch_pkvault_v8_alpha53i.py <pkvault-src> <pkhex-src>")

pkvault = Path(sys.argv[1]).resolve()
pkhex = Path(sys.argv[2]).resolve()

def replace_once(path: Path, old: str, new: str, already: str):
    text = path.read_text(encoding="utf-8")
    if already in text:
        return
    if old not in text:
        raise RuntimeError(f"alpha53i anchor missing: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# alpha53h used a guessed bitmask. The actual mGBA v1.4 script creates exactly
# one custom DV pair per A-Z letter. Mirror those exact signatures, byte-for-byte.
shiny = pkhex / "PKHeX.Core/Legality/RNG/Util/ShinyUtil.cs"
replace_once(
    shiny,
    '''    public static bool GetIsShinyGBExtendedUnown(ushort dv16)
    {
        byte dv1 = (byte)(dv16 >> 8);
        byte dv2 = (byte)dv16;
        return (dv1 & 0x99) == 0x08 && (dv2 & 0xBF) == 0xAA;
    }''',
    '''    public static bool GetIsShinyGBExtendedUnown(ushort dv16) => dv16 is
        0x9999 or 0x99DD or 0x9BB9 or 0x9BFD or 0x9DD9 or 0x9F9D or 0x9FF9 or
        0xB9BD or 0xBB99 or 0xBBDD or 0xBDB9 or 0xBDFD or 0xBFD9 or 0xD99D or
        0xD9F9 or 0xDBBD or 0xDD99 or 0xDDDD or 0xDFB9 or 0xDFFD or 0xF9D9 or
        0xFB9D or 0xFBF9 or 0xFDBD or 0xFF99 or 0xFFDD;

    /// <summary>
    /// Returns the exact custom DV signature emitted by Silver Unown Shiny Fix v1.4
    /// for an A-Z Unown form (0=A ... 25=Z).
    /// </summary>
    public static ushort GetShinyGBExtendedUnownDV(byte form) => form switch
    {
        0 => 0x9999,  1 => 0x99DD,  2 => 0x9BB9,  3 => 0x9BFD,
        4 => 0x9DD9,  5 => 0x9F9D,  6 => 0x9FF9,  7 => 0xB9BD,
        8 => 0xBB99,  9 => 0xBBDD, 10 => 0xBDB9, 11 => 0xBDFD,
       12 => 0xBFD9, 13 => 0xD99D, 14 => 0xD9F9, 15 => 0xDBBD,
       16 => 0xDD99, 17 => 0xDDDD, 18 => 0xDFB9, 19 => 0xDFFD,
       20 => 0xF9D9, 21 => 0xFB9D, 22 => 0xFBF9, 23 => 0xFDBD,
       24 => 0xFF99, 25 => 0xFFDD,
        _ => throw new ArgumentOutOfRangeException(nameof(form), form, "Gen-II Unown form must be A-Z."),
    };''',
    "GetShinyGBExtendedUnownDV(byte form)",
)

bridge = pkvault / "PKVault.Core/storage/services/PkmConvertService/Gen2ExtendedUnownShinyBridge.cs"
replace_once(
    bridge,
    '''        ushort? dv = CanVanillaGen2RepresentForm(form)
            ? FindBestDV(pk2.DV16, form, vanillaOnly: true)
            : FindBestDV(pk2.DV16, form, vanillaOnly: false);

        if (dv is null)
            throw new InvalidOperationException($"No Gen-II shiny DV signature found for Unown form {form}.");

        pk2.DV16 = dv.Value;''',
    '''        // Match the mGBA script exactly. It emits one custom signature for every
        // letter, including I and V, even though stock Gen II can also represent
        // vanilla shiny I/V.
        pk2.DV16 = ShinyUtil.GetShinyGBExtendedUnownDV(form);''',
    "pk2.DV16 = ShinyUtil.GetShinyGBExtendedUnownDV(form);",
)

# Remove the obsolete DV-search helper now that Silver uses the script's exact table.
text = bridge.read_text(encoding="utf-8")
start = text.find("    private static ushort? FindBestDV(")
end = text.find("    private static byte GetUnownForm(", start)
if start >= 0 and end >= 0:
    # GetUnownForm is now unused as well; remove through the class's final closing brace
    # by finding the method close and retaining only the class close.
    method_start = end
    # The file ends with method close + class close. Replace both helpers with nothing.
    helper_block = text[start:text.rfind("}")]
    # helper_block intentionally excludes the final class brace.
    text = text[:start] + text[text.rfind("}"):]
    bridge.write_text(text, encoding="utf-8")

# Correct the alpha53h source-level regression expectations too.
test = pkvault / "PKVault.Core.Tests/storage/Gen2ExtendedUnownShinyBridgeTests.cs"
t = test.read_text(encoding="utf-8")
t = t.replace("ExtendedRuleHas32SignaturesAndCoversAZ", "ExtendedRuleHas26ExactSignaturesAndCoversAZ")
t = t.replace("Assert.Equal(32, count);", "Assert.Equal(26, count);")
t = t.replace("CombinedRuleHas38Gen2ShinyDvCombinations", "CombinedRuleHas34Gen2ShinyDvCombinations")
t = t.replace("Assert.Equal(38, count);", "Assert.Equal(34, count);")
test.write_text(t, encoding="utf-8")

print("PASS alpha53i exact Silver v1.4 Unown shiny signatures")
