from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52q anchor not found: {label}")
    return text.replace(old, new, 1)

img_path = root / "frontend/src/img/species-img.tsx"
img = img_path.read_text(encoding="utf-8")

img = rep(
    img,
    """    romHackSpeciesName?: string | null;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;
""",
    """    romHackSpeciesName?: string | null;
    suppressTitle?: boolean;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;
""",
    "SpeciesImg suppressTitle prop",
)

img = rep(
    img,
    """    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName,
    ...imgProps
}) => {
""",
    """    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName, suppressTitle,
    ...imgProps
}) => {
""",
    "SpeciesImg suppressTitle destructure",
)

img = rep(
    img,
    """            title={isInsurgenceMissingNo ? 'Pokémon Insurgence MISSINGNO #722' : "MissingNo / 'M Gen 1 glitch Pokemon"}
""",
    """            title={suppressTitle
                ? undefined
                : isInsurgenceMissingNo
                    ? 'Pokémon Insurgence MISSINGNO #722'
                    : "MissingNo / 'M Gen 1 glitch Pokemon"}
""",
    "MissingNo title suppression",
)

img = rep(
    img,
    """            title={romHackSpeciesName ?? (romHackProfile ?? 'ROM hack') + ' #' + localSpeciesId}
""",
    """            title={suppressTitle
                ? undefined
                : romHackSpeciesName ?? (romHackProfile ?? 'ROM hack') + ' #' + localSpeciesId}
""",
    "ROM hack title suppression",
)

img_path.write_text(img, encoding="utf-8")

for rel in [
    "frontend/src/romhacks/uranium-pokedex.tsx",
    "frontend/src/romhacks/insurgence-pokedex.tsx",
]:
    path = root / rel
    text = path.read_text(encoding="utf-8")

    # Only the Dex-list sprite gets suppression. Details/storage continue showing
    # normal titles because the species is already known there.
    anchor = """                romHackSpeciesName={entry.name}
              />
"""
    replacement = """                romHackSpeciesName={entry.name}
                suppressTitle={!isSeen}
              />
"""
    if anchor not in text:
        raise RuntimeError(f"alpha52q locked ROM-hack sprite anchor not found: {rel}")
    text = text.replace(anchor, replacement, 1)
    path.write_text(text, encoding="utf-8")

print("PKVault V8 alpha52q locked ROM-hack Dex hover-name leak fixed")
