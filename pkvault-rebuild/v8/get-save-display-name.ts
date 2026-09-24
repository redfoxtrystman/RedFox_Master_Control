export const TMT_PROFILE_ID = 'too-many-types-v1.6';

export const getSaveDisplayName = (
    defaultName: string | undefined,
    romHackProfile?: string | null,
): string => {
    const base = defaultName ?? '';
    return romHackProfile === TMT_PROFILE_ID
        ? `${base} TMT`
        : base;
};
