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
    title?: string;
} & SpriteImgProps> = ({ file, nameTile, title, sourceRealHeight: _sourceRealHeight, style, className, ...rest }) => {
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
            style={{
                width: nameTile ? '70%' : '58.333%',
                height: nameTile ? '32%' : '58.333%',
                objectFit: 'contain',
                imageRendering: 'pixelated',
                pointerEvents: 'none',
            }}
        />
    </div>;
};

'''
t = t[:start] + component + t[end:]

start = t.index("    const getGen1GlitchFront = (): Gen1GlitchFront | null => {")
end = t.index("    const gen1GlitchFront = isGen1Glitch", start)
front = r'''    const getGen1GlitchFront = (): Gen1GlitchFront | null => {
        const dex = gen1GlitchDexNumber ?? 0;
        const yellow = contextVersion === GameVersion.YW;
        const hex = gen1GlitchIndex?.toString(16).toUpperCase().padStart(2, '0') ?? '00';
        const pad = String(dex).padStart(3, '0');

        if (!yellow) {
            if (gen1GlitchIndex === 0xB6) return { file: '/gen1-glitch/rb/b6.png' };
            if (gen1GlitchIndex === 0xB7) return { file: '/gen1-glitch/rb/b7.png' };
            if (gen1GlitchIndex === 0xB8) return { file: '/gen1-glitch/rb/b8.png' };
            if (gen1GlitchIndex === 0xFA) return { file: '/gen1-glitch/rb/fa.png' };
            if (dex === 0) return { file: '/gen1-glitch/rb/missingno.png', missingno: true };

            const archived = new Set([
                17, 18, 24, 26, 40, 61, 62, 64, 72, 79, 85, 94, 95, 135,
                174, 175, 204, 205, 207, 209, 213, 225, 234, 236, 240, 245,
                250, 254, 255,
            ]);
            if (archived.has(dex))
                return { file: `/gen1-glitch/rb/dex${pad}.png` };

            if (dex >= 1 && dex <= 151)
                return null;

            if (gen1GlitchIndex === 0xE1 || gen1GlitchIndex === 0xEC
                || gen1GlitchIndex === 0xED || gen1GlitchIndex === 0xEF)
                return { file: `/gen1-glitch/names/RBGlitchName${hex}.png`, nameTile: true };

            return null;
        }

        if (dex === 0)
            return { file: '/gen1-glitch/y/missingno.png', missingno: true };

        const yellowArchived = new Set([
            6, 9, 11, 15, 16, 18, 21, 27, 40, 53, 55, 62, 79, 80, 84, 85,
            93, 121, 126, 127, 128, 143, 144, 159, 176, 195, 202, 203, 205,
            206, 207, 215, 229, 230, 234, 245, 250, 254,
        ]);
        if (yellowArchived.has(dex))
            return { file: `/gen1-glitch/y/dex${pad}.png` };

        if (dex >= 1 && dex <= 151)
            return null;

        if (gen1GlitchIndex === 0xE0)
            return { file: '/gen1-glitch/names/YGlitchNameE0.png', nameTile: true };

        return null;
    };

'''
t = t[:start] + front + t[end:]

p.write_text(t, encoding='utf-8')

check = p.read_text(encoding='utf-8')
assert 'useEffect' not in check and 'useState' not in check
assert '/api/StaticData/gen1-glitch-sprite' not in check
assert "17, 18, 24, 26, 40" in check
assert "95, 135" in check
assert '`/gen1-glitch/rb/dex${pad}.png`' in check
assert "RBGlitchName${hex}.png" in check
print('PKVault V8 alpha52x local canonical Gen-I glitch sprite mapping applied')
