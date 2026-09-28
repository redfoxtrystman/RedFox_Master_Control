from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52r2 anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# SpeciesImg: render canonical Gen1 glitch sprites.
# - If the R/B glitch points at a normal #001-151 sprite, reuse PKVault's
#   existing Gen1 sprite sheet.
# - MissingNo/fossil/ghost and out-of-range glitch Pokédex numbers use the
#   Bulbagarden Archives front sprite with the normal MissingNo sprite fallback
#   concept instead of the old '?' icon.
# ---------------------------------------------------------------------------
p = root / "frontend/src/img/species-img.tsx"
text = p.read_text(encoding="utf-8")

text = rep(
    text,
    """    romHackLocalSpeciesId?: number | null;
    romHackSpeciesName?: string | null;
    suppressTitle?: boolean;
""",
    """    romHackLocalSpeciesId?: number | null;
    romHackSpeciesName?: string | null;
    gen1GlitchIndex?: number | null;
    gen1GlitchDexNumber?: number | null;
    gen1GlitchName?: string | null;
    suppressTitle?: boolean;
""",
    "SpeciesImg Gen1 glitch props",
)

text = rep(
    text,
    """    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName, suppressTitle,
    ...imgProps
}) => {
""",
    """    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName,
    gen1GlitchIndex, gen1GlitchDexNumber, gen1GlitchName, suppressTitle,
    ...imgProps
}) => {
""",
    "SpeciesImg Gen1 glitch destructure",
)

anchor = """    const isInsurgenceMissingNo = profileLocalSpecies
        && romHackProfile === INSURGENCE_PROFILE_ID
        && localSpeciesId === 722;

"""
insert = anchor + """    const isGen1Glitch = context === EntityContext.Gen1
        && gen1GlitchIndex !== null
        && gen1GlitchIndex !== undefined;

    const getGen1GlitchSpriteUrl = () => {
        const base = 'https://archives.bulbagarden.net/wiki/Special:Redirect/file/';
        const file = gen1GlitchIndex === 0xB6
            ? 'Spr 1b 141 f.png'
            : gen1GlitchIndex === 0xB7
                ? 'Spr 1b 142 f.png'
                : gen1GlitchIndex === 0xB8
                    ? 'Ghost I.png'
                    : (gen1GlitchDexNumber ?? 0) === 0
                        ? 'Missingno RB.png'
                        : 'RBGlitch' + String(gen1GlitchDexNumber).padStart(3, '0') + '.png';

        return base + encodeURIComponent(file);
    };

    if (isGen1Glitch && !gen1GlitchDexNumber) {
        return <UISpeciesImg
            {...imgProps}
            data-species-id={0}
            data-glitch-species='gen1'
            data-gen1-glitch-index={gen1GlitchIndex}
            sheetUrl={getGen1GlitchSpriteUrl()}
            spriteInfos={{ x: 0, y: 0, width: 56, height: 56 }}
            sourceRealHeight={56}
            species={1}
            isShadow={false}
            title={suppressTitle ? undefined : (gen1GlitchName ?? ('Gen I glitch 0x' + gen1GlitchIndex.toString(16).toUpperCase().padStart(2, '0')))}
        />;
    }

    if (isGen1Glitch && (gen1GlitchDexNumber ?? 0) > 151) {
        return <UISpeciesImg
            {...imgProps}
            data-species-id={gen1GlitchDexNumber}
            data-glitch-species='gen1'
            data-gen1-glitch-index={gen1GlitchIndex}
            sheetUrl={getGen1GlitchSpriteUrl()}
            spriteInfos={{ x: 0, y: 0, width: 56, height: 56 }}
            sourceRealHeight={56}
            species={gen1GlitchDexNumber ?? 1}
            isShadow={false}
            title={suppressTitle ? undefined : gen1GlitchName ?? undefined}
        />;
    }

"""
text = rep(text, anchor, insert, "Gen1 glitch sprite branch")

text = text.replace(
    "    if ((species === 0 && context === EntityContext.Gen1) || isInsurgenceMissingNo) {",
    "    if ((species === 0 && context === EntityContext.Gen1 && !isGen1Glitch) || isInsurgenceMissingNo) {",
    1
)

text = rep(
    text,
    """    const usedSpecies = species === 0
        ? 1
        : species;
""",
    """    const usedSpecies = isGen1Glitch
        && (gen1GlitchDexNumber ?? 0) >= 1
        && (gen1GlitchDexNumber ?? 0) <= 151
        ? gen1GlitchDexNumber!
        : species === 0
            ? 1
            : species;
""",
    "Gen1 glitch official sprite reuse",
)

text = rep(
    text,
    """        species={species}
        isShadow={isShadow}
""",
    """        species={isGen1Glitch ? usedSpecies : species}
        data-glitch-species={isGen1Glitch ? 'gen1' : undefined}
        data-gen1-glitch-index={isGen1Glitch ? gen1GlitchIndex ?? undefined : undefined}
        title={isGen1Glitch && !suppressTitle ? gen1GlitchName ?? undefined : undefined}
        isShadow={isShadow}
""",
    "Gen1 glitch normal-sheet output",
)

p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Storage cards: canonical glitch names replace '?' / copied nicknames, and the
# raw index/sprite metadata travels with every card.
# ---------------------------------------------------------------------------
for rel in [
    "frontend/src/storage/item/main/storage-main-item.tsx",
    "frontend/src/storage/item/save/storage-save-item.tsx",
]:
    p = root / rel
    text = p.read_text(encoding="utf-8")

    text = text.replace(
        "'romHackProfile', 'romHackSpeciesName', 'romHackLocalSpeciesId',",
        "'romHackProfile', 'romHackSpeciesName', 'romHackLocalSpeciesId', 'gen1GlitchIndex', 'gen1GlitchName', 'gen1GlitchDexNumber',",
    )

    if "const { id, species, nickname" in text:
        if "main/storage-main-item" in rel:
            old = """        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile, romHackSpeciesName, romHackLocalSpeciesId } = mainVariant;
"""
            new = """        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile, romHackSpeciesName, romHackLocalSpeciesId, gen1GlitchIndex, gen1GlitchName, gen1GlitchDexNumber } = mainVariant;
"""
        else:
            old = """        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile, romHackSpeciesName, romHackLocalSpeciesId } = savePkm;
"""
            new = """        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile, romHackSpeciesName, romHackLocalSpeciesId, gen1GlitchIndex, gen1GlitchName, gen1GlitchDexNumber } = savePkm;
"""
        text = rep(text, old, new, f"{rel} destructure")

    text = rep(
        text,
        """            romHackLocalSpeciesId={romHackLocalSpeciesId}
            romHackSpeciesName={romHackSpeciesName}
            name={romHackSpeciesName ?? nickname}
""",
        """            romHackLocalSpeciesId={romHackLocalSpeciesId}
            romHackSpeciesName={romHackSpeciesName}
            gen1GlitchIndex={gen1GlitchIndex}
            gen1GlitchDexNumber={gen1GlitchDexNumber}
            gen1GlitchName={gen1GlitchName}
            name={gen1GlitchName ?? romHackSpeciesName ?? nickname}
""",
        f"{rel} glitch display",
    )

    p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# StorageItem prop pass-through to SpeciesImg.
# ---------------------------------------------------------------------------
p = root / "frontend/src/storage/item/storage-item.tsx"
text = p.read_text(encoding="utf-8")
text = rep(
    text,
    """    romHackLocalSpeciesId?: number | null;
    romHackSpeciesName?: string | null;
""",
    """    romHackLocalSpeciesId?: number | null;
    romHackSpeciesName?: string | null;
    gen1GlitchIndex?: number | null;
    gen1GlitchDexNumber?: number | null;
    gen1GlitchName?: string | null;
""",
    "StorageItem glitch props",
)
text = rep(
    text,
    """    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName,
""",
    """    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName,
    gen1GlitchIndex, gen1GlitchDexNumber, gen1GlitchName,
""",
    "StorageItem glitch destructure",
)
text = rep(
    text,
    """                romHackLocalSpeciesId={romHackLocalSpeciesId}
                romHackSpeciesName={romHackSpeciesName}
""",
    """                romHackLocalSpeciesId={romHackLocalSpeciesId}
                romHackSpeciesName={romHackSpeciesName}
                gen1GlitchIndex={gen1GlitchIndex}
                gen1GlitchDexNumber={gen1GlitchDexNumber}
                gen1GlitchName={gen1GlitchName}
""",
    "StorageItem SpeciesImg glitch pass",
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# Details: show the canonical glitch name and use Bulbapedia's exact 00 name
# image for 'M Block beneath/next to the text label.
# ---------------------------------------------------------------------------
p = root / "frontend/src/storage/details/details-main.tsx"
text = p.read_text(encoding="utf-8")
text = rep(
    text,
    """    const speciesName = pkm.romHackSpeciesName ?? formObj?.name ?? '';
""",
    """    const speciesName = pkm.gen1GlitchName ?? pkm.romHackSpeciesName ?? formObj?.name ?? '';
""",
    "details glitch name",
)
text = rep(
    text,
    """        species={pkm.species}
        speciesName={speciesName}
""",
    """        species={pkm.gen1GlitchDexNumber ?? pkm.species}
        speciesName={speciesName}
        speciesNameImage={pkm.gen1GlitchIndex === 0 ? pkm.gen1GlitchNameImageUrl : undefined}
""",
    "details glitch number/name image",
)
text = rep(
    text,
    """            romHackLocalSpeciesId={pkm.romHackLocalSpeciesId}
            romHackSpeciesName={pkm.romHackSpeciesName}
""",
    """            romHackLocalSpeciesId={pkm.romHackLocalSpeciesId}
            romHackSpeciesName={pkm.romHackSpeciesName}
            gen1GlitchIndex={pkm.gen1GlitchIndex}
            gen1GlitchDexNumber={pkm.gen1GlitchDexNumber}
            gen1GlitchName={pkm.gen1GlitchName}
""",
    "details SpeciesImg glitch pass",
)
p.write_text(text, encoding="utf-8")

p = root / "frontend/src/ui/storage/storage-details/ui-details-main.tsx"
text = p.read_text(encoding="utf-8")
text = rep(
    text,
    """    speciesName: string;
    gender: Gender;
""",
    """    speciesName: string;
    speciesNameImage?: string | null;
    gender: Gender;
""",
    "UIDetailsMain name image prop",
)
text = rep(
    text,
    """    species, speciesName, level, pokerusDays = 0, isPokerusCured,
""",
    """    species, speciesName, speciesNameImage, level, pokerusDays = 0, isPokerusCured,
""",
    "UIDetailsMain name image destructure",
)
text = rep(
    text,
    """                >{speciesName}</Text>

                <UIButton
""",
    """                >{speciesName}</Text>
                {speciesNameImage && <Tooltip label="Exact Red/Blue glitch-name tiles">
                    <img
                        src={speciesNameImage}
                        alt={speciesName}
                        style={{ imageRendering: 'pixelated', maxWidth: 96, maxHeight: 16 }}
                    />
                </Tooltip>}

                <UIButton
""",
    "UIDetailsMain exact glitch name image",
)
p.write_text(text, encoding="utf-8")

print("PKVault V8 alpha52r2 Gen1 glitch names/icons UI applied")
