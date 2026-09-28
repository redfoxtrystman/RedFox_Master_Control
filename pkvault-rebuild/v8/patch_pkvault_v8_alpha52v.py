from pathlib import Path
import os
import sys
import urllib.parse
import urllib.request

root = Path(sys.argv[1]).resolve()
pkhex_root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root.parent / 'pkhex-src'


def edit(path: Path, old: str, new: str, label: str):
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'alpha52v anchor missing: {label}: {path}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


# Raw Gen-I species 0x00 and 0xFF both collide with list sentinels. Alpha52t
# used non-zero body bytes to distinguish them from empty slots, but PKHeX's
# BlankPKM body is not guaranteed to be all-zero; that made cleared slots look
# occupied and caused the real-template generator to reload 151 "glitches".
# Single-slot lists already have an unambiguous count byte: 1 = occupied,
# 0 = blank. Preserve that count for raw 00/FF and use it as the authority.
poke_list = pkhex_root / 'PKHeX.Core/PKM/Shared/PokeList1.cs'
edit(
    poke_list,
    '''    public static bool IsSingleSlotOccupied(ReadOnlySpan<byte> single)
    {
        if (single.Length < 3 + PokeCrypto.SIZE_1STORED)
            return false;

        var marker = single[1];
        if (marker is not (0 or SlotEmpty))
            return true;

        // Raw 00 and raw FF are both valid Gen-I glitch species. Their header
        // markers collide with list sentinels, so the stored body disambiguates
        // a real glitch Pokemon from a genuinely blank slot.
        return single.Slice(3, PokeCrypto.SIZE_1STORED).ContainsAnyExcept<byte>(0);
    }
''',
    '''    public static bool IsSingleSlotOccupied(ReadOnlySpan<byte> single)
    {
        if (single.Length < 3 + PokeCrypto.SIZE_1STORED)
            return false;

        var marker = single[1];
        if (marker is not (0 or SlotEmpty))
            return true;

        // For a single-slot list the count byte is authoritative. Unpack()
        // writes 1 for an occupied raw 00/FF slot, while BlankPKM writes 0.
        // This avoids mistaking non-zero padding/body bytes for a real glitch.
        return single[0] != 0;
    }
''',
    'single-slot raw 00/FF occupancy count',
)

# WriteToList normally recalculates count only from the species marker. That
# cannot work for a one-slot raw 00 or raw FF because those bytes are also the
# list sentinels. For single-slot storage, derive count from the PK1 itself.
edit(
    poke_list,
    '''        output[1 + index] = GetHeaderIdentifierMark(pk);

        // Count normal markers normally, but treat raw-00 as occupied only
        // when its stored Gen-1 body is actually populated.
        var count = 0;
        for (int i = 0; i < capacity; i++)
        {
            var marker = output[1 + i];
            if (IsPresent(marker))
            {
                count++;
                continue;
            }
            if (marker is not (0 or SlotEmpty))
                continue;

            var bodyOffset = start + (sizeBody * i);
            if (output.Slice(bodyOffset, PokeCrypto.SIZE_1STORED).ContainsAnyExcept<byte>(0))
                count++;
        }
        output[0] = (byte)count;
        output[1 + capacity] = SlotEmpty; // cap off the list
''',
    '''        output[1 + index] = GetHeaderIdentifierMark(pk);

        // Single-slot storage has an unambiguous count byte. This is the only
        // reliable way to distinguish occupied raw 00/FF from an empty slot.
        if (capacity == 1)
        {
            output[0] = (byte)(IsOccupied(pk) ? 1 : 0);
        }
        else
        {
            var count = 0;
            for (int i = 0; i < capacity; i++)
            {
                var marker = output[1 + i];
                if (IsPresent(marker))
                {
                    count++;
                    continue;
                }

                var bodyOffset = start + (sizeBody * i);
                if (output.Slice(bodyOffset, PokeCrypto.SIZE_1STORED).ContainsAnyExcept<byte>(0))
                    count++;
            }
            output[0] = (byte)count;
        }
        output[1 + capacity] = SlotEmpty; // cap off the list
''',
    'single-slot raw 00/FF count preservation',
)

# Keep Bulbapedia's actual name for the 39 ordinary MissingNo. indices. The
# raw identifier is already carried separately as Gen1GlitchIndex/HexIndex, so
# putting "(B5)" into the Pokemon name made it look like a distinct species.
glitch = root / 'PKVault.Core/storage/glitch/Gen1GlitchDex.cs'
edit(
    glitch,
    '''            _ => $"MissingNo. ({hex})",\n''',
    '''            _ => "MissingNo.",\n''',
    'plain MissingNo name',
)

# Replace the all-remote alpha52t glitch sprite branch. Red/Blue glitch art is
# packaged into the app so thumbnails do not randomly turn into broken <img>
# icons. Stable hybrid-family sprites use the exact archived glitch sprite when
# one exists; otherwise ordinary #001-151 families fall through to PKVault's
# native Gen-I sprite sheet. Two R/B families (E1/'v and ED/hゥ) have front
# sprites documented to crash the original game, so they get an explicit local
# CRASH SPRITE tile rather than a fake/broken picture.
species = root / 'frontend/src/img/species-img.tsx'
t = species.read_text(encoding='utf-8')
start = t.index('    const getGen1GlitchSpriteUrl = () => {')
end = t.index('\n    if ((species === 0 && context === EntityContext.Gen1', start)
new_block = r'''    type Gen1GlitchFront = {
        url?: string;
        crash?: boolean;
        missingno?: boolean;
    };

    const getGen1GlitchFront = (): Gen1GlitchFront | null => {
        const dex = gen1GlitchDexNumber ?? 0;
        const yellow = contextVersion === GameVersion.YW;
        const pad = String(dex).padStart(3, '0');

        // Alpha52v vendors the Red/Blue fronts locally. Yellow remains on the
        // existing archive path until a real Yellow SRAM template is supplied.
        if (!yellow) {
            if (gen1GlitchIndex === 0xB6) return { url: '/gen1-glitch/Spr%201b%20141%20f.png' };
            if (gen1GlitchIndex === 0xB7) return { url: '/gen1-glitch/Spr%201b%20142%20f.png' };
            if (gen1GlitchIndex === 0xB8) return { url: '/gen1-glitch/Ghost%20I.png' };
            if (gen1GlitchIndex === 0xFA) return { url: '/gen1-glitch/RBGlitchFA.png' };
            if (dex === 0) return { url: '/gen1-glitch/Missingno%20RB.png', missingno: true };

            // These two front sprites are documented to crash Red/Blue; there
            // is no stable canonical front image to show.
            if (gen1GlitchIndex === 0xE1 || gen1GlitchIndex === 0xED)
                return { crash: true };

            const archived = new Set([
                17, 18, 24, 26, 40, 61, 62, 64, 72, 79, 85, 94, 95, 135,
                174, 175, 204, 205, 207, 209, 213, 225, 234, 236, 240, 245,
                250, 254, 255,
            ]);
            if (archived.has(dex))
                return { url: `/gen1-glitch/RBGlitch${pad}.png` };

            // Real #001-151 families can be rendered from PKVault's normal
            // Gen-I spritesheet below. Any other unknown family is safer as a
            // crash/unavailable tile than a broken web image.
            return dex >= 1 && dex <= 151 ? null : { crash: true };
        }

        const base = 'https://archives.bulbagarden.net/wiki/Special:Redirect/file/';
        if (dex === 0) return { url: base + encodeURIComponent('Missingno Y.png'), missingno: true };
        const yGlitch = new Set([6,9,11,15,16,17,18,21,27,40,53,55,62,79,80,84,85,93,121,126,127,128,143,144,159,176,195,202,203,205,206,207,215,229,230,234,245,250,254]);
        const file = dex > 151 || yGlitch.has(dex) ? `YGlitch${pad}.png` : `Spr 1y ${pad}.png`;
        return { url: base + encodeURIComponent(file) };
    };

    const gen1GlitchFront = isGen1Glitch ? getGen1GlitchFront() : null;
    const crashGlitchSprite = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'%3E%3Crect width='56' height='56' rx='5' fill='%231b1b1b'/%3E%3Cpath d='M8 8h40v40H8z' fill='none' stroke='%23f0a500' stroke-width='2'/%3E%3Ctext x='28' y='25' text-anchor='middle' font-family='monospace' font-size='9' fill='%23f0a500'%3ECRASH%3C/text%3E%3Ctext x='28' y='36' text-anchor='middle' font-family='monospace' font-size='8' fill='white'%3ESPRITE%3C/text%3E%3C/svg%3E";

    if (isGen1Glitch && (gen1GlitchFront?.url || gen1GlitchFront?.crash)) {
        const rawIndex = '0x' + gen1GlitchIndex.toString(16).toUpperCase().padStart(2, '0');
        return <UISpeciesImg
            {...imgProps}
            data-species-id={gen1GlitchDexNumber ?? 0}
            data-glitch-species='gen1'
            data-gen1-glitch-index={gen1GlitchIndex}
            data-gen1-missingno={gen1GlitchFront?.missingno || undefined}
            sheetUrl={gen1GlitchFront?.crash ? crashGlitchSprite : gen1GlitchFront!.url!}
            spriteInfos={{ x: 0, y: 0, width: 56, height: 56 }}
            sourceRealHeight={56}
            style={{ ...imgProps.style, '--sprite-content-scale': 56 / 96 } as React.CSSProperties}
            species={gen1GlitchDexNumber || 1}
            isShadow={false}
            title={suppressTitle ? undefined : `${gen1GlitchName ?? 'Gen I glitch'} · raw index ${rawIndex}`}
        />;
    }
'''
t = t[:start] + new_block + t[end:]

old_used = '''    const usedSpecies = species === 0 ? 1 : species;\n'''
new_used = '''    const usedSpecies = isGen1Glitch\n        && (gen1GlitchDexNumber ?? 0) >= 1\n        && (gen1GlitchDexNumber ?? 0) <= 151\n        ? gen1GlitchDexNumber!\n        : species === 0\n            ? 1\n            : species;\n'''
if old_used not in t:
    raise RuntimeError('alpha52v anchor missing: usedSpecies')
t = t.replace(old_used, new_used, 1)

old_final = '''        spriteInfos={spriteInfos}\n        species={species}\n        isShadow={isShadow}\n        {...imgProps}\n'''
new_final = '''        spriteInfos={spriteInfos}\n        species={isGen1Glitch ? usedSpecies : species}\n        data-glitch-species={isGen1Glitch ? 'gen1' : undefined}\n        data-gen1-glitch-index={isGen1Glitch ? gen1GlitchIndex ?? undefined : undefined}\n        title={isGen1Glitch && !suppressTitle\n            ? `${gen1GlitchName ?? 'Gen I glitch'} · raw index 0x${gen1GlitchIndex!.toString(16).toUpperCase().padStart(2, '0')}`\n            : undefined}\n        isShadow={isShadow}\n        {...imgProps}\n'''
if old_final not in t:
    raise RuntimeError('alpha52v anchor missing: final SpeciesImg output')
t = t.replace(old_final, new_final, 1)
species.write_text(t, encoding='utf-8')

# The canonical MissingNo/'M archive sprite is intentionally right-anchored to
# emulate the game. PKVault storage cards are a centered icon UI, so visually
# recenter the non-transparent portion without altering the source asset.
css = root / 'frontend/src/ui/sprite-img/species-img/ui-species-img.module.css'
with css.open('a', encoding='utf-8') as f:
    f.write(r'''

/* PKVault card presentation: visually center the right-anchored R/B MissingNo/'M art. */
.ui-species-img[data-gen1-missingno="true"] img {
    transform: translateX(calc(var(--sprite-size-rem) * -0.17));
}
''')

# Vendor the Red/Blue glitch fronts so runtime rendering is deterministic and
# does not depend on Archives hot-linking or redirects.
asset_names = [
    'Missingno RB.png', 'Spr 1b 141 f.png', 'Spr 1b 142 f.png', 'Ghost I.png',
    'RBGlitch017.png', 'RBGlitch018.png', 'RBGlitch024.png', 'RBGlitch026.png',
    'RBGlitch040.png', 'RBGlitch061.png', 'RBGlitch062.png', 'RBGlitch064.png',
    'RBGlitch072.png', 'RBGlitch079.png', 'RBGlitch085.png', 'RBGlitch094.png',
    'RBGlitch095.png', 'RBGlitch135.png', 'RBGlitch174.png', 'RBGlitch175.png',
    'RBGlitch204.png', 'RBGlitch205.png', 'RBGlitch207.png', 'RBGlitch209.png',
    'RBGlitch213.png', 'RBGlitch225.png', 'RBGlitch234.png', 'RBGlitch236.png',
    'RBGlitch240.png', 'RBGlitch245.png', 'RBGlitch250.png', 'RBGlitch254.png',
    'RBGlitch255.png', 'RBGlitchFA.png',
]
asset_dir = root / 'frontend/public/gen1-glitch'
asset_dir.mkdir(parents=True, exist_ok=True)

if os.environ.get('PKVAULT_SKIP_GLITCH_ASSET_FETCH') != '1':
    base = 'https://archives.bulbagarden.net/wiki/Special:Redirect/file/'
    for name in asset_names:
        url = base + urllib.parse.quote(name, safe='')
        request = urllib.request.Request(url, headers={'User-Agent': 'PKVault-RedFox-build/alpha52v'})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
        except Exception as exc:
            raise RuntimeError(f'alpha52v failed to fetch {name}: {exc}') from exc
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise RuntimeError(f'alpha52v fetched non-PNG data for {name} ({len(data)} bytes)')
        (asset_dir / name).write_bytes(data)

print('PKVault V8 alpha52v centered/local Gen-I glitch sprite fix applied')
