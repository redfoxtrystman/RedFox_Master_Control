from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
p = root / 'frontend/src/img/species-img.tsx'
t = p.read_text(encoding='utf-8')

t = t.replace("import { useEffect, useState } from 'react';\n", "")

start = t.index("const Gen1GlitchStandaloneImg: React.FC<{")
end = t.index("export const SpeciesImg", start)
component = r'''const Gen1GlitchStandaloneImg: React.FC<{
    file: string;
    nameTile?: boolean;
    missingno?: boolean;
    title?: string;
} & SpriteImgProps> = ({ file, nameTile, missingno, title, sourceRealHeight: _sourceRealHeight, style, className, ...rest }) => {
    const size = 'calc(var(--sprite-species-size-multiplier, 1) * 96px)';
    return <div
        {...rest}
        className={className}
        title={title}
        data-glitch-species='gen1'
        style={{
            width: size,
            height: size,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden',
            flexShrink: 0,
            ...style,
        }}
    >
        <img
            src={file}
            alt=''
            draggable={false}
            data-fallback-stage='0'
            onError={event => {
                const image = event.currentTarget;
                const stage = Number(image.dataset.fallbackStage ?? '0');
                const filename = decodeURIComponent(image.src.split('/').pop() ?? '');
                if (stage === 0) {
                    image.dataset.fallbackStage = '1';
                    image.src = file.replace(
                        'https://archives.bulbagarden.net/media/upload/',
                        'https://cdn.bulbagarden.net/upload/',
                    );
                    return;
                }
                if (stage === 1 && filename) {
                    image.dataset.fallbackStage = '2';
                    image.src = 'https://archives.bulbagarden.net/wiki/Special:Redirect/file/' + encodeURIComponent(filename);
                    return;
                }
                image.style.visibility = 'hidden';
            }}
            style={{
                width: nameTile ? '70%' : '58.333%',
                height: nameTile ? '32%' : '58.333%',
                objectFit: 'contain',
                imageRendering: 'pixelated',
                pointerEvents: 'none',
                transform: missingno ? 'translateX(-16%)' : undefined,
            }}
        />
    </div>;
};

'''
t = t[:start] + component + t[end:]

start = t.index("    const getGen1GlitchFront = (): Gen1GlitchFront | null => {")
end = t.index("    const gen1GlitchFront = isGen1Glitch", start)
front = r'''    const rbGlitchUrls: Record<number, string> = {
        17: 'https://archives.bulbagarden.net/media/upload/f/f6/RBGlitch017.png',
        18: 'https://archives.bulbagarden.net/media/upload/3/3c/RBGlitch018.png',
        24: 'https://archives.bulbagarden.net/media/upload/f/f7/RBGlitch024.png',
        26: 'https://archives.bulbagarden.net/media/upload/e/ec/RBGlitch026.png',
        40: 'https://archives.bulbagarden.net/media/upload/2/28/RBGlitch040.png',
        61: 'https://archives.bulbagarden.net/media/upload/0/0d/RBGlitch061.png',
        62: 'https://archives.bulbagarden.net/media/upload/c/c9/RBGlitch062.png',
        64: 'https://archives.bulbagarden.net/media/upload/7/79/RBGlitch064.png',
        72: 'https://archives.bulbagarden.net/media/upload/7/71/RBGlitch072.png',
        79: 'https://archives.bulbagarden.net/media/upload/4/4f/RBGlitch079.png',
        85: 'https://archives.bulbagarden.net/media/upload/1/13/RBGlitch085.png',
        94: 'https://archives.bulbagarden.net/media/upload/0/0b/RBGlitch094.png',
        95: 'https://archives.bulbagarden.net/media/upload/a/a6/RBGlitch095.png',
        135: 'https://archives.bulbagarden.net/media/upload/1/18/RBGlitch135.png',
        174: 'https://archives.bulbagarden.net/media/upload/0/0b/RBGlitch174.png',
        175: 'https://archives.bulbagarden.net/media/upload/7/75/RBGlitch175.png',
        204: 'https://archives.bulbagarden.net/media/upload/7/7c/RBGlitch204.png',
        205: 'https://archives.bulbagarden.net/media/upload/b/b1/RBGlitch205.png',
        207: 'https://archives.bulbagarden.net/media/upload/8/83/RBGlitch207.png',
        209: 'https://archives.bulbagarden.net/media/upload/5/5f/RBGlitch209.png',
        213: 'https://archives.bulbagarden.net/media/upload/f/fe/RBGlitch213.png',
        225: 'https://archives.bulbagarden.net/media/upload/0/05/RBGlitch225.png',
        234: 'https://archives.bulbagarden.net/media/upload/6/6f/RBGlitch234.png',
        236: 'https://archives.bulbagarden.net/media/upload/d/d8/RBGlitch236.png',
        240: 'https://archives.bulbagarden.net/media/upload/c/cf/RBGlitch240.png',
        245: 'https://archives.bulbagarden.net/media/upload/1/1f/RBGlitch245.png',
        250: 'https://archives.bulbagarden.net/media/upload/b/b3/RBGlitch250.png',
        254: 'https://archives.bulbagarden.net/media/upload/f/f3/RBGlitch254.png',
        255: 'https://archives.bulbagarden.net/media/upload/5/5b/RBGlitch255.png',
    };

    const yGlitchUrls: Record<number, string> = {
        6: 'https://archives.bulbagarden.net/media/upload/1/1c/YGlitch006.png',
        9: 'https://archives.bulbagarden.net/media/upload/b/b8/YGlitch009.png',
        11: 'https://archives.bulbagarden.net/media/upload/f/fe/YGlitch011.png',
        15: 'https://archives.bulbagarden.net/media/upload/b/bd/YGlitch015.png',
        16: 'https://archives.bulbagarden.net/media/upload/7/7a/YGlitch016.png',
        18: 'https://archives.bulbagarden.net/media/upload/2/21/YGlitch018.png',
        21: 'https://archives.bulbagarden.net/media/upload/e/ed/YGlitch021.png',
        27: 'https://archives.bulbagarden.net/media/upload/b/b6/YGlitch027.png',
        40: 'https://archives.bulbagarden.net/media/upload/7/72/YGlitch040.png',
        53: 'https://archives.bulbagarden.net/media/upload/0/0d/YGlitch053.png',
        55: 'https://archives.bulbagarden.net/media/upload/f/f7/YGlitch055.png',
        62: 'https://archives.bulbagarden.net/media/upload/6/6a/YGlitch062.png',
        79: 'https://archives.bulbagarden.net/media/upload/0/03/YGlitch079.png',
        80: 'https://archives.bulbagarden.net/media/upload/2/29/YGlitch080.png',
        84: 'https://archives.bulbagarden.net/media/upload/1/19/YGlitch084.png',
        85: 'https://archives.bulbagarden.net/media/upload/0/01/YGlitch085.png',
        93: 'https://archives.bulbagarden.net/media/upload/e/ea/YGlitch093.png',
        121: 'https://archives.bulbagarden.net/media/upload/8/83/YGlitch121.png',
        126: 'https://archives.bulbagarden.net/media/upload/3/35/YGlitch126.png',
        127: 'https://archives.bulbagarden.net/media/upload/7/7d/YGlitch127.png',
        128: 'https://archives.bulbagarden.net/media/upload/4/47/YGlitch128.png',
        143: 'https://archives.bulbagarden.net/media/upload/3/38/YGlitch143.png',
        144: 'https://archives.bulbagarden.net/media/upload/6/68/YGlitch144.png',
        159: 'https://archives.bulbagarden.net/media/upload/6/63/YGlitch159.png',
        176: 'https://archives.bulbagarden.net/media/upload/3/3b/YGlitch176.png',
        195: 'https://archives.bulbagarden.net/media/upload/a/ae/YGlitch195.png',
        202: 'https://archives.bulbagarden.net/media/upload/5/58/YGlitch202.png',
        203: 'https://archives.bulbagarden.net/media/upload/0/06/YGlitch203.png',
        205: 'https://archives.bulbagarden.net/media/upload/c/c5/YGlitch205.png',
        206: 'https://archives.bulbagarden.net/media/upload/b/bc/YGlitch206.png',
        207: 'https://archives.bulbagarden.net/media/upload/1/19/YGlitch207.png',
        215: 'https://archives.bulbagarden.net/media/upload/4/42/YGlitch215.png',
        229: 'https://archives.bulbagarden.net/media/upload/3/37/YGlitch229.png',
        230: 'https://archives.bulbagarden.net/media/upload/e/e7/YGlitch230.png',
        234: 'https://archives.bulbagarden.net/media/upload/1/1a/YGlitch234.png',
        245: 'https://archives.bulbagarden.net/media/upload/0/05/YGlitch245.png',
        250: 'https://archives.bulbagarden.net/media/upload/3/39/YGlitch250.png',
        254: 'https://archives.bulbagarden.net/media/upload/f/fb/YGlitch254.png',
    };

    const getGen1GlitchFront = (): Gen1GlitchFront | null => {
        const dex = gen1GlitchDexNumber ?? 0;
        const yellow = contextVersion === GameVersion.YW;

        if (!yellow) {
            if (gen1GlitchIndex === 0xB6) return { file: 'https://archives.bulbagarden.net/media/upload/a/aa/Spr_1b_141_f.png' };
            if (gen1GlitchIndex === 0xB7) return { file: 'https://archives.bulbagarden.net/media/upload/b/bb/Spr_1b_142_f.png' };
            if (gen1GlitchIndex === 0xB8) return { file: 'https://archives.bulbagarden.net/media/upload/9/9e/Ghost_I.png' };
            if (gen1GlitchIndex === 0xFA) return { file: 'https://archives.bulbagarden.net/media/upload/3/3b/RBGlitchFA.png' };
            if (dex === 0) return { file: 'https://archives.bulbagarden.net/media/upload/9/98/Missingno_RB.png', missingno: true };

            if (rbGlitchUrls[dex])
                return { file: rbGlitchUrls[dex] };

            if (dex >= 1 && dex <= 151)
                return null;

            const nameTiles: Record<number, string> = {
                0xE1: 'https://archives.bulbagarden.net/media/upload/5/56/RBGlitchNameE1.png',
                0xEC: 'https://archives.bulbagarden.net/media/upload/f/fb/RBGlitchNameEC.png',
                0xED: 'https://archives.bulbagarden.net/media/upload/a/a8/RBGlitchNameED.png',
                0xEF: 'https://archives.bulbagarden.net/media/upload/d/d3/RBGlitchNameEF.png',
            };
            const nameTile = gen1GlitchIndex === null || gen1GlitchIndex === undefined
                ? undefined
                : nameTiles[gen1GlitchIndex];
            return nameTile ? { file: nameTile, nameTile: true } : null;
        }

        if (dex === 0)
            return { file: 'https://archives.bulbagarden.net/media/upload/0/03/Missingno_Y.png', missingno: true };

        if (yGlitchUrls[dex])
            return { file: yGlitchUrls[dex] };

        if (dex >= 1 && dex <= 151)
            return null;

        if (gen1GlitchIndex === 0xE0)
            return { file: 'https://archives.bulbagarden.net/media/upload/2/2f/YGlitchNameE0.png', nameTile: true };

        return null;
    };

'''
t = t[:start] + front + t[end:]

# Pass MissingNo presentation metadata into the direct standalone renderer.
old = '''            file={gen1GlitchFront.file}
            nameTile={gen1GlitchFront.nameTile}
            title={suppressTitle ? undefined : `${gen1GlitchName ?? 'Gen I glitch'} · raw index ${rawIndex}`}
'''
new = '''            file={gen1GlitchFront.file}
            nameTile={gen1GlitchFront.nameTile}
            missingno={gen1GlitchFront.missingno}
            title={suppressTitle ? undefined : `${gen1GlitchName ?? 'Gen I glitch'} · raw index ${rawIndex}`}
'''
if old not in t:
    raise RuntimeError('alpha52x standalone render anchor missing')
t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8')

check = p.read_text(encoding='utf-8')
assert 'useEffect' not in check and 'useState' not in check
assert '/api/StaticData/gen1-glitch-sprite' not in check
assert 'RBGlitch095.png' in check
assert 'RBGlitch250.png' in check
assert "rbGlitchUrls[dex]" in check
assert "yGlitchUrls[dex]" in check
assert "missingno={gen1GlitchFront.missingno}" in check
assert 'crashGlitchSprite' not in check
print('PKVault V8 alpha52x canonical direct-media Gen-I glitch sprite mapping applied')
