from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52r1 anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# PKHeX-side occupancy: all 105 R/B glitch index values map to national species
# 0. Keep raw 00's body check so a genuinely blank slot is still empty.
# ---------------------------------------------------------------------------
p = root / "PKHeX.Core/PKM/Shared/PokeList1.cs"
text = p.read_text(encoding="utf-8")
text = rep(
    text,
    "    public static bool IsKnownGen1Glitch(PK1 pk) => IsRawZeroGlitch(pk) || IsMissingNo50(pk);\n",
    """    public static bool IsKnownGen1Glitch(PK1 pk)
        => IsRawZeroGlitch(pk)
            || (pk.SpeciesInternal != 0 && SpeciesConverter.GetNational1(pk.SpeciesInternal) == 0);
""",
    "all Gen1 glitch occupancy",
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Canonical English Red/Blue glitch metadata.
# Names and Red/Blue Pokédex numbers follow Bulbapedia's Generation I glitch
# table. MissingNo copies are discovered dynamically from SpeciesConverter.
# ---------------------------------------------------------------------------
info = root / "PKVault.Core/storage/glitch/Gen1GlitchDex.cs"
info.parent.mkdir(parents=True, exist_ok=True)
info.write_text(r'''using PKHeX.Core;

namespace PKVault.Core;

public sealed record Gen1GlitchInfo(
    byte Index,
    string Name,
    ushort RedBlueDexNumber,
    string HexIndex,
    string? NameImageUrl = null
);

public static class Gen1GlitchDex
{
    private const string NameImageBase =
        "https://archives.bulbagarden.net/wiki/Special:Redirect/file/RBGlitchName";

    private static readonly IReadOnlyDictionary<byte, (string Name, ushort Dex)> Named =
        new Dictionary<byte, (string, ushort)>
        {
            [0x00] = ("'M (00)", 0),
            [0xBF] = ("▶ A", 250),
            [0xC0] = ("a", 61),
            [0xC1] = ("ゥ (C1)", 205),
            [0xC2] = ("ゥ .4", 234),
            [0xC3] = ("h POKé", 94),
            [0xC4] = ("PokéWTrainer", 205),
            [0xC5] = ("PkMn (C5)", 250),
            [0xC6] = ("ゥL ゥM 4", 62),
            [0xC7] = ("♀Pゥ ゥゥT", 205),
            [0xC8] = ("ゥU?", 234),
            [0xC9] = ("◣ゥ 8", 95),
            [0xCA] = ("PC4SH", 205),
            [0xCB] = ("p", 17),
            [0xCC] = ("PkMn ◣ n", 56),
            [0xCD] = ("Trainer", 81),
            [0xCE] = ("▼ W G d", 24),
            [0xCF] = ("OPkMn4X", 15),
            [0xD0] = ("PkMn PkMn T", 250),
            [0xD1] = ("4B 8 4 8", 62),
            [0xD2] = ("ゥ '", 205),
            [0xD3] = ("M p'u ゥ", 234),
            [0xD4] = ("Aゥ G", 94),
            [0xD5] = ("Pゥ ゥ ゥ", 205),
            [0xD6] = ("4h", 250),
            [0xD7] = ("Glitch (D7)", 61),
            [0xD8] = ("PkMnaPkMnゥ ♂ fPkMnk", 205),
            [0xD9] = ("PkMnRPkMn \"", 234),
            [0xDA] = ("B (DA)", 95),
            [0xDB] = ("Glitch (DB)", 205),
            [0xDC] = ("Glitch (DC)", 17),
            [0xDD] = ("7PkMn 'v", 73),
            [0xDE] = ("-PkMn", 81),
            [0xDF] = (".PkMn", 250),
            [0xE0] = ("/PkMn ▼PkMn", 85),
            [0xE1] = ("'v", 211),
            [0xE2] = ("……", 245),
            [0xE3] = ("ゥ (E3)", 240),
            [0xE4] = ("Glitch (E4)", 175),
            [0xE5] = ("C", 245),
            [0xE6] = ("- -", 240),
            [0xE7] = ("Pゥ 4$", 174),
            [0xE8] = ("X C", 245),
            [0xE9] = ("c", 175),
            [0xEA] = ("A (EA)", 234),
            [0xEB] = ("Glitch (EB)", 85),
            [0xEC] = ("Glitch (EC)", 211),
            [0xED] = ("hゥ", 224),
            [0xEE] = (".g", 175),
            [0xEF] = ("ゥ$'M", 224),
            [0xF0] = ("ゥ$ (F0)", 174),
            [0xF1] = ("94", 213),
            [0xF2] = ("ゥ l (F2)", 209),
            [0xF3] = ("ゥ l (F3)", 26),
            [0xF4] = ("ゥ$ (F4)", 254),
            [0xF5] = ("ゥ (F5)", 255),
            [0xF6] = ("G'Mp", 40),
            [0xF7] = ("'Ng'Mp", 18),
            [0xF8] = ("'Ng ゥ$", 19),
            [0xF9] = ("94 h", 213),
            [0xFA] = ("Glitch (FA)", 33),
            [0xFB] = ("'M 'N g", 95),
            [0xFC] = ("O", 81),
            [0xFD] = ("ゥ$ 6ゥ", 135),
            [0xFE] = ("'M (FE)", 79),
            [0xFF] = ("'M (FF)", 6),
        };

    public static bool IsGlitchIndex(byte index)
        => SpeciesConverter.GetNational1(index) == 0;

    public static bool TryGet(PK1 pk, out Gen1GlitchInfo info)
    {
        if (!PokeList1.IsKnownGen1Glitch(pk))
        {
            info = default!;
            return false;
        }

        info = Get(pk.SpeciesInternal);
        return true;
    }

    public static Gen1GlitchInfo Get(byte index)
    {
        if (!IsGlitchIndex(index))
            throw new ArgumentOutOfRangeException(nameof(index), $"0x{index:X2} is not a Red/Blue glitch index.");

        var hex = index.ToString("X2");

        if (Named.TryGetValue(index, out var named))
        {
            return new(
                index,
                named.Name,
                named.Dex,
                hex,
                index == 0 ? $"{NameImageBase}00.png" : $"{NameImageBase}{hex}.png"
            );
        }

        var name = index switch
        {
            0xB6 => "MissingNo. Kabutops Fossil",
            0xB7 => "MissingNo. Aerodactyl Fossil",
            0xB8 => "MissingNo. Ghost",
            _ => $"MissingNo. ({hex})",
        };

        return new(index, name, 0, hex);
    }

    public static IReadOnlyList<byte> AllRedBlueIndices { get; } =
        Enumerable.Range(0, 256)
            .Select(x => (byte)x)
            .Where(IsGlitchIndex)
            .ToArray();
}
''', encoding="utf-8")

# ---------------------------------------------------------------------------
# DTO surface: make the raw index, canonical name and R/B sprite number visible
# to the frontend without pretending these are National Dex species.
# ---------------------------------------------------------------------------
p = root / "PKVault.Core/storage/dto/PkmBaseDTO.cs"
text = p.read_text(encoding="utf-8")
text = rep(
    text,
    "    public ushort Species => Pkm.Species;\n",
    """    public ushort Species => Pkm.Species;
    public byte? Gen1GlitchIndex => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.Index : null;
    public string? Gen1GlitchName => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.Name : null;
    public ushort? Gen1GlitchDexNumber => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.RedBlueDexNumber : null;
    public string? Gen1GlitchNameImageUrl => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.NameImageUrl : null;
""",
    "Gen1 glitch DTO metadata",
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Stable identity: raw glitch index must not collapse to Species=0 when hashing.
# ---------------------------------------------------------------------------
p = root / "PKVault.Core/storage/wrapper/ImmutablePKM.cs"
text = p.read_text(encoding="utf-8")
text = rep(
    text,
    """    public string GetPKMIdBase(Dictionary<ushort, StaticEvolve> evolves, int boxId = (int)BoxType.Box)
    {
        if (Pkm is PKEssentials essentials)
""",
    """    public string GetPKMIdBase(Dictionary<ushort, StaticEvolve> evolves, int boxId = (int)BoxType.Box)
    {
        if (Pkm is PK1 pk1 && PokeList1.IsKnownGen1Glitch(pk1))
        {
            var scoped = BoxLoader.IsScopedBox(boxId) ? $"_{boxId}" : "";
            var ot = OriginalTrainerName.Replace("_", "-");
            return $"G1GLITCH_{pk1.SpeciesInternal:X2}_{pk1.DV16:X4}_{pk1.TID16:X4}_{ot}{scoped}";
        }

        if (Pkm is PKEssentials essentials)
""",
    "Gen1 glitch stable identity",
)
text = text.replace(
    "// General storage occupancy. Normal Pokemon remain normal; only the two\n    // explicitly supported Gen-1 glitch families bypass Species==0.",
    "// General storage occupancy. Normal Pokemon remain normal; all canonical\n    // English Red/Blue glitch index values bypass Species==0."
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Storage filenames: use the canonical glitch name and raw index instead of '?'.
# ---------------------------------------------------------------------------
p = root / "PKVault.Core/db/loader/PkmFileLoader.cs"
text = p.read_text(encoding="utf-8")
old = """        var speciesName = pkm.GetMutablePkm() is PKEssentials essentials
            ? essentials.SpeciesName.ToUpperInvariant().Replace(":", "")
            : pkm.IsGen1RawZeroGlitch
                ? "'M-RAW00"
                : pkm.IsGen1MissingNo50
                    ? "MISSINGNO-RAW50"
                    : GameInfo.Strings.Species[pkm.Species].ToUpperInvariant().Replace(":", "");
"""
new = """        var speciesName = pkm.GetMutablePkm() switch
        {
            PKEssentials essentials => essentials.SpeciesName.ToUpperInvariant().Replace(":", ""),
            PK1 pk1 when Gen1GlitchDex.TryGet(pk1, out var glitch) =>
                SanitizeFilename($"{glitch.Name}-RAW{glitch.HexIndex}").ToUpperInvariant(),
            _ => GameInfo.Strings.Species[pkm.Species].ToUpperInvariant().Replace(":", ""),
        };
"""
text = rep(text, old, new, "glitch filename naming")
text = rep(
    text,
    "public class PkmFileLoader : IPkmFileLoader\n{\n",
    """public class PkmFileLoader : IPkmFileLoader
{
    private static string SanitizeFilename(string value)
    {
        var invalid = Path.GetInvalidFileNameChars();
        return new(value.Select(ch => invalid.Contains(ch) ? '_' : ch).ToArray());
    }

""",
    "filename sanitizer",
)
p.write_text(text, encoding="utf-8")

print("PKVault V8 alpha52r1 full Red/Blue glitch species metadata applied")
