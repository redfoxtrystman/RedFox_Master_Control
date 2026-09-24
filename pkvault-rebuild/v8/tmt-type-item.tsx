import { Badge, type BadgeProps } from '@mantine/core';
import type React from 'react';

type TmtTypeStyle = {
    background: string;
    foreground?: string;
};

// Too Many Types v1.6 palette, reconstructed from the exact public v1.6 ROM's
// type icon graphics/palettes. Single-color entries use the icon's primary
// background color; genuinely split/multicolor icons preserve that presentation
// with a CSS gradient instead of collapsing them to one arbitrary color.
export const TMT_TYPE_STYLES: Record<string, TmtTypeStyle> = {
    normal:    { background: '#ACAC7B' },
    fighting:  { background: '#C53129' },
    flying:    { background: '#AC94F6' },
    poison:    { background: '#A441A4' },
    ground:    { background: '#E6C56A' },
    rock:      { background: '#BDA439' },
    bug:       { background: '#ACBD20' },
    ghost:     { background: '#735A9C', foreground: '#FFFFFF' },
    steel:     { background: '#BDBDD5' },
    mystery:   { background: '#6AA494' },
    fire:      { background: '#F68331' },
    water:     { background: '#6A94F6' },
    grass:     { background: '#7BCD52' },
    electric:  { background: '#FFD531' },
    psychic:   { background: '#FF5A8B' },
    ice:       { background: '#9CDEDE' },
    dragon:    { background: '#7339FF', foreground: '#FFFFFF' },
    dark:      { background: '#735A4A', foreground: '#FFFFFF' },
    fairy:     { background: '#DE83BD' },

    monke:     { background: '#BDA439' },
    angy:      { background: '#C53129' },
    baby:      { background: '#9CDEDE' },
    friend:    { background: '#7BCD52' },
    guys:      { background: '#BDBDD5' },
    liquid:    { background: 'linear-gradient(90deg, #9CDEDE 0%, #6A94F6 100%)' },
    vibe:      { background: '#7339FF', foreground: '#FFFFFF' },
    song:      { background: '#6A94F6' },
    space:     { background: '#000000', foreground: '#FFFFFF' },
    fluffy:    { background: '#E6C56A' },
    sus:       { background: '#735A4A', foreground: '#FFFFFF' },
    furry:     { background: '#6A94F6' },
    bad:       { background: '#C53129' },
    ancient:   { background: '#BDA439' },
    silly:     { background: '#BDA4FF' },
    stinky:    { background: '#946262', foreground: '#FFFFFF' },
    sharp:     { background: '#BDBDD5' },
    magic:     { background: '#FF5A8B' },
    gender:    { background: 'linear-gradient(90deg, #9CDEDE 0 50%, #DE83BD 50% 100%)' },
    little:    { background: '#7BCD52' },
    crab:      { background: 'linear-gradient(90deg, #6A94F6 0 70%, #F68331 70% 100%)' },
    dream:     { background: '#AC94F6' },
    right:     { background: '#ACAC7B' },
    left:      { background: '#ACAC7B' },
    zoomer:    { background: '#6A94F6' },
    gamer:     { background: '#6AA494' },
    dance:     { background: '#7BCD52' },
    boring:    { background: '#ACAC7B' },
    ugly:      { background: 'linear-gradient(90deg, #4A3994 0 62%, #C5FF62 62% 100%)', foreground: '#FFFFFF' },
    emerald:   { background: 'linear-gradient(90deg, #5A8341 0 50%, #7BCD52 50% 100%)', foreground: '#FFFFFF' },
    gun:       { background: '#F68331' },
    pikachu:   { background: '#FFD531' },
    prime:     { background: '#A441A4', foreground: '#FFFFFF' },
    ohio:      { background: '#A441A4', foreground: '#FFFFFF' },
    'deez nuts': { background: '#7339FF', foreground: '#FFFFFF' },
    normal2:   { background: '#ACAC7B' },
    bean:      { background: '#ACBD20' },
    boomer:    { background: '#AC94F6' },
    smash:     { background: 'linear-gradient(90deg, #F68331 0 64%, #C53129 64% 100%)' },
    ou:        { background: '#73CDB4' },
    ball:      { background: '#73CDB4' },
    sans:      { background: 'linear-gradient(90deg, #000000 0 58%, #FFFFFF 58% 100%)', foreground: '#FFFFFF' },
    reverse:   { background: 'linear-gradient(90deg, #C53129 0 50%, #BDBDD5 50% 100%)', foreground: '#FFFFFF' },
    type:      { background: '#000000', foreground: '#FFFFFF' },
};

const getReadableForeground = (background: string): string => {
    const match = /^#([0-9a-f]{6})$/i.exec(background);
    if (!match)
        return '#171717';

    const raw = match[1]!;
    const r = Number.parseInt(raw.slice(0, 2), 16);
    const g = Number.parseInt(raw.slice(2, 4), 16);
    const b = Number.parseInt(raw.slice(4, 6), 16);
    const luminance = (0.299 * r) + (0.587 * g) + (0.114 * b);
    return luminance >= 145 ? '#171717' : '#FFFFFF';
};

export type TmtTypeItemProps = {
    type: string;
} & Omit<BadgeProps, 'children' | 'color'>;

export const TmtTypeItem: React.FC<TmtTypeItemProps> = ({ type, style, ...rest }) => {
    const entry = TMT_TYPE_STYLES[type.toLowerCase()]
        ?? { background: '#735A9C', foreground: '#FFFFFF' };
    const foreground = entry.foreground ?? getReadableForeground(entry.background);

    return <Badge
        variant='filled'
        size='sm'
        radius='sm'
        {...rest}
        style={{
            background: entry.background,
            color: foreground,
            border: '1px solid rgba(255, 255, 255, 0.22)',
            boxShadow: 'inset 0 -1px 0 rgba(0, 0, 0, 0.18)',
            textShadow: foreground === '#FFFFFF' ? '0 1px 1px rgba(0, 0, 0, 0.65)' : undefined,
            ...style,
        }}
    >
        {type}
    </Badge>;
};
