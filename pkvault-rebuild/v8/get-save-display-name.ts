export const TMT_PROFILE_ID = 'too-many-types-v1.6';
export const URANIUM_PROFILE_ID = 'pokemon-uranium';
export const INSURGENCE_PROFILE_ID = 'pokemon-insurgence';

export const getSaveDisplayName = (
    defaultName: string | undefined,
    romHackProfile?: string | null,
): string => {
    const base = defaultName ?? '';
    if (romHackProfile === URANIUM_PROFILE_ID)
        return 'Pokémon Uranium';
    if (romHackProfile === INSURGENCE_PROFILE_ID)
        return 'Pokémon Insurgence';
    return romHackProfile === TMT_PROFILE_ID
        ? `${base} TMT`
        : base;
};
