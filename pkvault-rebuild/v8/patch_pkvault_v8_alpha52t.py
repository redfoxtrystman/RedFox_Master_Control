from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def edit(path: Path, old: str, new: str, label: str):
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'alpha52t anchor missing: {label}: {path}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')

# Berry menu: the 15 rows reported as free were the only ₽80/₽40 rows.
# Put all 18 berries on the same working ₽200/₽100 tier as Gold/Miracle/Sitrus.
shop = root / 'PKVault.Core/shop/ShopService.cs'
text = shop.read_text(encoding='utf-8')
for key in ('berry','przcure-berry','psncure-berry','bitter-berry','burnt-berry','ice-berry','mint-berry',
            'mystery-berry','oran-berry','pecha-berry','cheri-berry','chesto-berry','rawst-berry','aspear-berry','persim-berry'):
    old = f'new("{key}", "Berries", 80, 40)'
    if old not in text:
        raise RuntimeError(f'alpha52t berry anchor missing: {key}')
    text = text.replace(old, f'new("{key}", "Berries", 200, 100)', 1)
shop.write_text(text, encoding='utf-8')

# Yellow interprets the same raw glitch indices differently from Red/Blue.
yellow = root / 'PKVault.Core/storage/glitch/Gen1GlitchYellow.cs'
yellow.write_text(r'''using PKHeX.Core;

namespace PKVault.Core;

public static class Gen1GlitchYellow
{
    private static readonly IReadOnlyDictionary<byte, (string Name, ushort Dex)> Named =
        new Dictionary<byte, (string, ushort)>
        {
            [0x00] = ("3TrainerPoké $",176), [0xBF] = ("4 4",250), [0xC0] = ("4 4Hy",80),
            [0xC1] = ("♀ .",205), [0xC2] = ("PkMnp' '",230), [0xC3] = ("ゥ ( Z4",15),
            [0xC4] = ("X ゥ- xゥ,",203), [0xC5] = ("4. .",55), [0xC6] = ("ァ7g",79),
            [0xC7] = ("u",6), [0xC8] = ("g g",0), [0xC9] = ("ァ / g J 1",33),
            [0xCA] = ("Glitch (CA)",229), [0xCB] = (". pゥ",81), [0xCC] = (".8",9),
            [0xCD] = ("ゥ. B",9), [0xCE] = ("PkMn pゥぁ ゥぇ (CE)",9), [0xCF] = ("4, ゥァ (CF)",9),
            [0xD0] = ("ゥ'",93), [0xD1] = ("B ァ h",84), [0xD2] = ("PkMn ? A",33),
            [0xD3] = ("ゥゥ]",128), [0xD4] = ("ゥ (D4)",143), [0xD5] = ("'ゥ.",1),
            [0xD6] = ("PkMn pゥぁ ゥぇ (D6)",4), [0xD7] = ("B (D7)",16), [0xD8] = ("PkMn (D8)",205),
            [0xD9] = ("ゥ (D9)",254), [0xDA] = ("]",21), [0xDB] = ("ゥ' B",250),
            [0xDC] = ("PkMn (DC)",202), [0xDD] = ("4, ゥァ (DD)",207), [0xDE] = ("8 (DE)",245),
            [0xDF] = ("p ID",62), [0xE0] = ("8 P ァ",255), [0xE1] = ("'r 'r 4",234),
            [0xE2] = ("(h4to89",202), [0xE3] = ("4 89 4",207), [0xE4] = ("8B 4 8",250),
            [0xE5] = ("Z ゥ",53), [0xE6] = ("9",215), [0xE7] = ("ゥHIゥ.",203),
            [0xE8] = ("4(h4hi?$",119), [0xE9] = ("4HI?",33), [0xEA] = ("'r ゥ",143),
            [0xEB] = ("$ Pゥ. 4(",195), [0xEC] = ("?/",17), [0xED] = ("4(h4?",159),
            [0xEE] = ("ゥ► ゥ▼ ゥ",195), [0xEF] = ("h 4Pゥ ゥ...",40), [0xF0] = (". ゥ ( .I' .",6),
            [0xF1] = ("' B' ゥ",33), [0xF2] = ("ゥ ゥェ ゥ ▷",127), [0xF3] = ("ゥ $ A (F3)",195),
            [0xF4] = ("♂ p ゥ",17), [0xF5] = ("▼ pゥ",143), [0xF6] = ("ゥ $ A (F6)",195),
            [0xF7] = ("PkMn (F7)",1), [0xF8] = ("ゥ 4- 4",144), [0xF9] = ("$",0),
            [0xFA] = ("ゥ▾ ゥ♂",126), [0xFB] = ("F q ,",18), [0xFC] = ("ゥ$ 4MN ゥ",43),
            [0xFD] = ("× 'rゥ. 4-",27), [0xFE] = ("ゥ/ 4ァ 4,",11), [0xFF] = ("Q ◣",121),
        };

    public static string GetName(byte index)
        => Named.TryGetValue(index, out var value) ? value.Name : $"MissingNo. ({index:X2})";

    public static ushort GetDexNumber(byte index)
        => Named.TryGetValue(index, out var value) ? value.Dex : (ushort)0;

    public static string? GetNameImageUrl(byte index)
        => index == 0 ? "https://archives.bulbagarden.net/wiki/Special:Redirect/file/YGlitchName00.png" : null;
}
''', encoding='utf-8')

# ContextVersion must be the actual save version for Red/Blue vs Yellow.
base = root / 'PKVault.Core/storage/dto/PkmBaseDTO.cs'
edit(base,
'''    public GameVersion ContextVersion => Version.Context == Context
        ? Version
        : Context.GetSingleGameVersion();
''',
'''    public virtual GameVersion ContextVersion => Version.Context == Context
        ? Version
        : Context.GetSingleGameVersion();
''', 'virtual ContextVersion')
edit(base,
'''    public string? Gen1GlitchName => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.Name : null;
    public ushort? Gen1GlitchDexNumber => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.RedBlueDexNumber : null;
    public string? Gen1GlitchNameImageUrl => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch) ? glitch.NameImageUrl : null;
''',
'''    public string? Gen1GlitchName => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch)
            ? ContextVersion == GameVersion.YW ? Gen1GlitchYellow.GetName(glitch.Index) : glitch.Name
            : null;
    public ushort? Gen1GlitchDexNumber => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch)
            ? ContextVersion == GameVersion.YW ? Gen1GlitchYellow.GetDexNumber(glitch.Index) : glitch.RedBlueDexNumber
            : null;
    public string? Gen1GlitchNameImageUrl => Pkm.GetMutablePkm() is PK1 pk1
        && Gen1GlitchDex.TryGet(pk1, out var glitch)
            ? ContextVersion == GameVersion.YW ? Gen1GlitchYellow.GetNameImageUrl(glitch.Index) : glitch.NameImageUrl
            : null;
''', 'versioned Gen1 glitch DTO')

save = root / 'PKVault.Core/storage/dto/PkmSaveDTO.cs'
edit(save,
'''    public override string IdBase => Pkm.GetPKMIdBase(Evolves, BoxId);
    public uint SaveId => Save.Id;
''',
'''    public override string IdBase => Pkm.GetPKMIdBase(Evolves, BoxId);
    public override GameVersion ContextVersion => Save.Version;
    public uint SaveId => Save.Id;
''', 'save ContextVersion')

# Exact front sprites for every Gen-I glitch. Keep their full image contained and centered.
species = root / 'frontend/src/img/species-img.tsx'
t = species.read_text(encoding='utf-8')
t = t.replace("import { EntityContext } from '../data/sdk/model';", "import { EntityContext, GameVersion } from '../data/sdk/model';", 1)
t = t.replace("    gen1GlitchName?: string | null;\n", "    gen1GlitchName?: string | null;\n    contextVersion?: GameVersion;\n", 1)
t = t.replace("    gen1GlitchIndex, gen1GlitchDexNumber, gen1GlitchName, suppressTitle,\n", "    gen1GlitchIndex, gen1GlitchDexNumber, gen1GlitchName, contextVersion, suppressTitle,\n", 1)
start = t.index('    const getGen1GlitchSpriteUrl = () => {')
end = t.index('\n    if ((species === 0 && context === EntityContext.Gen1', start)
block = r'''    const getGen1GlitchSpriteUrl = () => {
        const base = 'https://archives.bulbagarden.net/wiki/Special:Redirect/file/';
        const dex = gen1GlitchDexNumber ?? 0;
        const yellow = contextVersion === GameVersion.YW;
        const pad = String(dex).padStart(3, '0');

        if (!yellow && gen1GlitchIndex === 0xB6) return base + encodeURIComponent('Spr 1b 141 f.png');
        if (!yellow && gen1GlitchIndex === 0xB7) return base + encodeURIComponent('Spr 1b 142 f.png');
        if (!yellow && gen1GlitchIndex === 0xB8) return base + encodeURIComponent('Ghost I.png');
        if (dex === 0) return base + encodeURIComponent(yellow ? 'Missingno Y.png' : 'Missingno RB.png');

        const rbGlitch = new Set([17,18,24,26,40,61,62,64,72,79,85,94,95,135,174,175,204,205,207,209,213,225,234,236,240,245,250,254,255]);
        const yGlitch = new Set([6,9,11,15,16,17,18,21,27,40,53,55,62,79,80,84,85,93,121,126,127,128,143,144,159,176,195,202,203,205,206,207,215,229,230,234,245,250,254]);
        const file = yellow
            ? (dex > 151 || yGlitch.has(dex) ? `YGlitch${pad}.png` : `Spr 1y ${pad}.png`)
            : (dex > 151 || rbGlitch.has(dex) ? `RBGlitch${pad}.png` : `Spr 1b ${pad}.png`);
        return base + encodeURIComponent(file);
    };

    if (isGen1Glitch) {
        return <UISpeciesImg
            {...imgProps}
            data-species-id={gen1GlitchDexNumber ?? 0}
            data-glitch-species='gen1'
            data-gen1-glitch-index={gen1GlitchIndex}
            sheetUrl={getGen1GlitchSpriteUrl()}
            spriteInfos={{ x: 0, y: 0, width: 56, height: 56 }}
            sourceRealHeight={56}
            style={{ ...imgProps.style, '--sprite-content-scale': 56 / 96 } as React.CSSProperties}
            species={gen1GlitchDexNumber || 1}
            isShadow={false}
            title={suppressTitle ? undefined : (gen1GlitchName ?? ('Gen I glitch 0x' + gen1GlitchIndex.toString(16).toUpperCase().padStart(2, '0')))}
        />;
    }
'''
t = t[:start] + block + t[end:]
t = t.replace("    const usedSpecies = isGen1Glitch\n        && (gen1GlitchDexNumber ?? 0) >= 1\n        && (gen1GlitchDexNumber ?? 0) <= 151\n        ? gen1GlitchDexNumber!\n        : species === 0\n            ? 1\n            : species;\n", "    const usedSpecies = species === 0 ? 1 : species;\n", 1)
t = t.replace("        species={isGen1Glitch ? usedSpecies : species}\n        data-glitch-species={isGen1Glitch ? 'gen1' : undefined}\n        data-gen1-glitch-index={isGen1Glitch ? gen1GlitchIndex ?? undefined : undefined}\n        title={isGen1Glitch && !suppressTitle ? gen1GlitchName ?? undefined : undefined}\n", "        species={species}\n", 1)
species.write_text(t, encoding='utf-8')

css = root / 'frontend/src/ui/sprite-img/species-img/ui-species-img.module.css'
with css.open('a', encoding='utf-8') as f:
    f.write(r'''

/* Generation-I glitch fronts are standalone files, not atlas cells. */
.ui-species-img[data-glitch-species="gen1"] img {
    object-fit: contain;
    object-position: center;
    width: calc(var(--sprite-size) * var(--sprite-content-scale, 1) * 1px);
    height: calc(var(--sprite-size) * var(--sprite-content-scale, 1) * 1px);
    transform: none;
}
''')

# Thread the save version to thumbnail/detail images.
item = root / 'frontend/src/storage/item/storage-item.tsx'
t = item.read_text(encoding='utf-8')
t = t.replace("'gen1GlitchIndex' | 'gen1GlitchDexNumber' | 'gen1GlitchName'>;", "'gen1GlitchIndex' | 'gen1GlitchDexNumber' | 'gen1GlitchName' | 'contextVersion'>;", 1)
t = t.replace("  gen1GlitchName,\n", "  gen1GlitchName,\n  contextVersion,\n", 1)
t = t.replace("gen1GlitchName={gen1GlitchName} />", "gen1GlitchName={gen1GlitchName} contextVersion={contextVersion} />", 1)
item.write_text(t, encoding='utf-8')

for rel in ('frontend/src/storage/item/main/storage-main-item.tsx','frontend/src/storage/item/save/storage-save-item.tsx'):
    p = root / rel
    t = p.read_text(encoding='utf-8')
    t = t.replace("            gen1GlitchName={gen1GlitchName}\n            name=", "            gen1GlitchName={gen1GlitchName}\n            contextVersion={contextVersion}\n            name=", 1)
    p.write_text(t, encoding='utf-8')

details = root / 'frontend/src/storage/details/details-main.tsx'
t = details.read_text(encoding='utf-8')
t = t.replace("            gen1GlitchName={pkm.gen1GlitchName}\n        />", "            gen1GlitchName={pkm.gen1GlitchName}\n            contextVersion={pkm.contextVersion}\n        />", 1)
details.write_text(t, encoding='utf-8')

print('PKVault V8 alpha52t berry + complete Gen-I glitch display patch applied')
