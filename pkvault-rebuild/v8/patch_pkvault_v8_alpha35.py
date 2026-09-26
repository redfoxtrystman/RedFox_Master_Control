from pathlib import Path
import json
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
PKVAULT = Path(sys.argv[1]).resolve()

def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"alpha35 anchor missing in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# V8 alpha35
# - Uranium dex shows only Uranium-original fakemon (no reused canon species)
# - Uranium and Insurgence are both labeled as Generation 6
# - both fan-game dex sections are inserted immediately after vanilla Gen 6
# - Insurgence dex shows Delta species #727-924 plus UFI #925
# - MISSINGNO and ordinary canon Pokémon are excluded from the Insurgence overlay
# ---------------------------------------------------------------------------

frontend_romhacks = PKVAULT / "frontend/src/romhacks"

# Generate the Insurgence frontend dex profile from the pinned C# compatibility
# profile already used by the save parser. Keep one source of truth.
src = PKVAULT / "PKVault.Core/romhacks/essentials/InsurgenceProfile.Generated.cs"
text = src.read_text(encoding="utf-8")
pattern = re.compile(
    r'\[(\d+)\] = new\((\d+), "([^"]+)", \[(.*?)\], \[(.*?)\]\),'
)
rows = []
for match in pattern.finditer(text):
    species_id = int(match.group(1))
    if species_id != int(match.group(2)):
        raise RuntimeError("Insurgence generated profile has mismatched ids")
    if species_id < 727 or species_id > 925:
        continue

    types = [
        part.strip().strip('"')
        for part in match.group(4).split(",")
        if part.strip()
    ]
    stats = [
        int(part.strip())
        for part in match.group(5).split(",")
        if part.strip()
    ]
    rows.append((
        species_id,
        match.group(3),
        types,
        stats,
        "fakemon" if species_id == 925 else "delta",
    ))

if len(rows) != 199:
    raise RuntimeError(
        f"Expected 199 Insurgence Delta/fakemon entries, got {len(rows)}"
    )

entries = "\n".join(
    "  "
    + str(species_id)
    + ": { id: "
    + str(species_id)
    + ", name: "
    + json.dumps(name, ensure_ascii=False)
    + ", types: "
    + json.dumps(types, ensure_ascii=False)
    + ", baseStats: "
    + json.dumps(stats)
    + ", kind: "
    + json.dumps(kind)
    + " },"
    for species_id, name, types, stats, kind in rows
)

(frontend_romhacks / "insurgence-profile.ts").write_text(
    f"""// Generated from InsurgenceProfile.Generated.cs.
// Dex overlay intentionally includes Delta species #727-924 plus UFI #925.
// Canon Pokémon and MISSINGNO are excluded.
export const INSURGENCE_PROFILE_ID = 'pokemon-insurgence';
export const INSURGENCE_GENERATION = 6;
export const INSURGENCE_DEX_OFFSET = 20_000;

export type InsurgenceDexSpeciesEntry = {{
  id: number;
  name: string;
  types: string[];
  // Essentials/Insurgence order: HP, Atk, Def, Speed, SpAtk, SpDef.
  baseStats: number[];
  kind: 'delta' | 'fakemon';
}};

export const INSURGENCE_DEX_SPECIES: Record<number, InsurgenceDexSpeciesEntry> = {{
{entries}
}};

export const INSURGENCE_DEX_SPECIES_LIST = Object.values(INSURGENCE_DEX_SPECIES)
  .sort((a, b) => a.id - b.id);

export const isInsurgenceDexSpeciesId = (id: number): boolean =>
  Object.prototype.hasOwnProperty.call(INSURGENCE_DEX_SPECIES, id);

export const getInsurgenceFrontSpritePath = (id: number): string =>
  `/romhacks/insurgence/front/${{String(id).padStart(3, '0')}}.png`;
""",
    encoding="utf-8",
)

shutil.copyfile(
    HERE / "insurgence-pokedex.tsx",
    frontend_romhacks / "insurgence-pokedex.tsx",
)

# Uranium overlay: fake species only, not the entire 200-species Tandor dex.
uranium_profile = frontend_romhacks / "uranium-profile.ts"
replace_once(
    uranium_profile,
    "export const URANIUM_GENERATION_FILTER_ID = 100;\n",
    "export const URANIUM_GENERATION = 6;\n",
)
replace_once(
    uranium_profile,
    """export const URANIUM_DEX_SPECIES = Object.values(URANIUM_SPECIES)
  .sort((a, b) => a.id - b.id);""",
    """export const URANIUM_DEX_SPECIES = URANIUM_ADDED_SPECIES
  .sort((a, b) => a.id - b.id);""",
)

generation_filter = PKVAULT / "frontend/src/pokedex/filters/components/filter-generation.tsx"
replace_once(
    generation_filter,
    "import { URANIUM_GENERATION_FILTER_ID } from '../../../romhacks/uranium-profile';\n",
    "",
)
replace_once(
    generation_filter,
    """  const options = [
    ...allGenerations.map((generation) => ({
      value: generation.toString(),
      label: t('dex.filters.generations.option', { generation, regions: staticData.generations[ generation ]?.regions.join(', ') }),
    })),
    {
      value: URANIUM_GENERATION_FILTER_ID.toString(),
      label: 'Pokémon Uranium (Tandor)',
    },
  ];
""",
    """  const options = allGenerations.map((generation) => ({
    value: generation.toString(),
    label: t('dex.filters.generations.option', { generation, regions: staticData.generations[ generation ]?.regions.join(', ') }),
  }));
""",
)
replace_once(
    generation_filter,
    """    renderPill={({ value = '' }) => <span>{Number(value) === URANIUM_GENERATION_FILTER_ID ? 'Uranium' : `G${value}`}</span>""",
    """    renderPill={({ value = '' }) => <span>G{value}</span>""",
)

uranium_dex = frontend_romhacks / "uranium-pokedex.tsx"
replace_once(
    uranium_dex,
    "  URANIUM_GENERATION_FILTER_ID,\n",
    "  URANIUM_GENERATION,\n",
)
replace_once(
    uranium_dex,
    """        if (URANIUM_SPECIES[pkm.romHackLocalSpeciesId])
          values.add(pkm.romHackLocalSpeciesId);""",
    """        const entry = URANIUM_SPECIES[pkm.romHackLocalSpeciesId];
        if (entry?.officialNationalDexId === null)
          values.add(pkm.romHackLocalSpeciesId);""",
)
replace_once(
    uranium_dex,
    """  const seen = React.useMemo(() => new Set(dexQuery.data?.seen ?? []), [dexQuery.data]);
  const caught = React.useMemo(() => new Set(dexQuery.data?.caught ?? []), [dexQuery.data]);""",
    """  const fakeSpeciesIds = React.useMemo(() => new Set(URANIUM_DEX_SPECIES.map(entry => entry.id)), []);
  const seen = React.useMemo(
    () => new Set((dexQuery.data?.seen ?? []).filter(id => fakeSpeciesIds.has(id))),
    [dexQuery.data, fakeSpeciesIds],
  );
  const caught = React.useMemo(
    () => new Set((dexQuery.data?.caught ?? []).filter(id => fakeSpeciesIds.has(id))),
    [dexQuery.data, fakeSpeciesIds],
  );""",
)
replace_once(
    uranium_dex,
    "  if (filterGenerations.length > 0 && !filterGenerations.includes(URANIUM_GENERATION_FILTER_ID))",
    "  if (filterGenerations.length > 0 && !filterGenerations.includes(URANIUM_GENERATION))",
)
replace_once(
    uranium_dex,
    """        generation='Pokémon Uranium'
        regions={['Tandor']}
        games={<Text size='sm'>Tandor Pokédex · 200 species</Text>}""",
    """        generation='Generation 6'
        regions={['Tandor']}
        games={<Text size='sm'>Pokémon Uranium · Fakemon Pokédex</Text>}""",
)
replace_once(
    uranium_dex,
    """  if (!entry)
    return null;""",
    """  if (!entry || entry.officialNationalDexId !== null)
    return null;""",
)
replace_once(
    uranium_dex,
    """      <Text c='dimmed' size='sm'>Tandor Pokédex #{localId}</Text>""",
    """      <Text c='dimmed' size='sm'>Generation 6 · Tandor Fakemon #{localId}</Text>""",
)
replace_once(
    uranium_dex,
    """    items={<Text size='sm' c='dimmed'>{entry.officialNationalDexId === null ? 'Pokémon Uranium original species.' : 'Also appears in the National Pokédex as #' + entry.officialNationalDexId + '.'}</Text>}""",
    """    items={<Text size='sm' c='dimmed'>Pokémon Uranium original species.</Text>}""",
)

# Both fan-game dexes live immediately after the normal Generation 6 section.
pokedex_list = PKVAULT / "frontend/src/pokedex/list/pokedex-list.tsx"
replace_once(
    pokedex_list,
    """import { UraniumPokedexSection } from '../../romhacks/uranium-pokedex';""",
    """import { UraniumPokedexSection } from '../../romhacks/uranium-pokedex';
import { InsurgencePokedexSection } from '../../romhacks/insurgence-pokedex';""",
)

old_map = """      {speciesItemsByGenerationList.map(({
        generation,
        versionsForImgs,
        speciesInfos,
        minSpecies,
        maxSpecies,
        seenCount,
        caughtCount,
        ownedCount,
        shinyCount,
        totalCount,
      }, i) => [
          <Card.Section key={i} inheritPadding withBorder>
            <UIPokedexMainSectionHeader
              generation={t('dex.list.title', { generation })}
              regions={staticData.generations[ generation ]?.regions ?? []}
              games={versionsForImgs.map((versions, gameIndex) => <Group key={gameIndex} gap='xs' wrap='nowrap' visibleFrom='md'>
                {versions.map(version => <UIGameImg
                  key={version}
                  version={version}
                  size='1lh'
                />)}
              </Group>)}
              seenCount={seenCount}
              caughtCount={caughtCount}
              ownedCount={ownedCount}
              shinyCount={shinyCount}
              totalCount={totalCount}
            />
          </Card.Section>,
          <Card.Section key={i + 100} inheritPadding withBorder>
            <UIPokedexMainSection isFirstSection={i === 0} minSpecies={minSpecies} maxSpecies={maxSpecies}>
              {speciesInfos.map(({ species, speciesName, isSeen, itemsToRender }) => (
                <PokedexItem
                  key={species}
                  species={species}
                  speciesName={speciesName}
                  isSeen={isSeen}
                >
                  {itemsToRender.map((item) => (
                    <DexFormItem key={item.id} {...item} />
                  ))}
                </PokedexItem>
              ))}
            </UIPokedexMainSection>
          </Card.Section>,
        ])}

      <UraniumPokedexSection />
"""

new_map = """      {speciesItemsByGenerationList.map(({
        generation,
        versionsForImgs,
        speciesInfos,
        minSpecies,
        maxSpecies,
        seenCount,
        caughtCount,
        ownedCount,
        shinyCount,
        totalCount,
      }, i) => <React.Fragment key={generation}>
          <Card.Section inheritPadding withBorder>
            <UIPokedexMainSectionHeader
              generation={t('dex.list.title', { generation })}
              regions={staticData.generations[ generation ]?.regions ?? []}
              games={versionsForImgs.map((versions, gameIndex) => <Group key={gameIndex} gap='xs' wrap='nowrap' visibleFrom='md'>
                {versions.map(version => <UIGameImg
                  key={version}
                  version={version}
                  size='1lh'
                />)}
              </Group>)}
              seenCount={seenCount}
              caughtCount={caughtCount}
              ownedCount={ownedCount}
              shinyCount={shinyCount}
              totalCount={totalCount}
            />
          </Card.Section>
          <Card.Section inheritPadding withBorder>
            <UIPokedexMainSection isFirstSection={i === 0} minSpecies={minSpecies} maxSpecies={maxSpecies}>
              {speciesInfos.map(({ species, speciesName, isSeen, itemsToRender }) => (
                <PokedexItem
                  key={species}
                  species={species}
                  speciesName={speciesName}
                  isSeen={isSeen}
                >
                  {itemsToRender.map((item) => (
                    <DexFormItem key={item.id} {...item} />
                  ))}
                </PokedexItem>
              ))}
            </UIPokedexMainSection>
          </Card.Section>

          {generation === 6 && <>
            <UraniumPokedexSection />
            <InsurgencePokedexSection />
          </>}
        </React.Fragment>)}
"""

replace_once(pokedex_list, old_map, new_map)

# Route synthetic Insurgence dex selections to their own details panel.
wrapper = PKVAULT / "frontend/src/pokedex/details/pokedex-main-wrapper-details.tsx"
replace_once(
    wrapper,
    """import { UraniumPokedexDetails } from '../../romhacks/uranium-pokedex';""",
    """import { UraniumPokedexDetails } from '../../romhacks/uranium-pokedex';
import { InsurgencePokedexDetails } from '../../romhacks/insurgence-pokedex';""",
)
replace_once(
    wrapper,
    """import { URANIUM_DEX_OFFSET, URANIUM_SPECIES_COUNT } from '../../romhacks/uranium-profile';""",
    """import { URANIUM_DEX_OFFSET, URANIUM_SPECIES_COUNT } from '../../romhacks/uranium-profile';
import { INSURGENCE_DEX_OFFSET } from '../../romhacks/insurgence-profile';""",
)
replace_once(
    wrapper,
    """    const isUraniumDex = selected !== undefined
        && selected > URANIUM_DEX_OFFSET
        && selected <= URANIUM_DEX_OFFSET + URANIUM_SPECIES_COUNT;""",
    """    const isUraniumDex = selected !== undefined
        && selected > URANIUM_DEX_OFFSET
        && selected <= URANIUM_DEX_OFFSET + URANIUM_SPECIES_COUNT;
    const isInsurgenceDex = selected !== undefined
        && selected > INSURGENCE_DEX_OFFSET
        && selected <= INSURGENCE_DEX_OFFSET + 925;""",
)
replace_once(
    wrapper,
    """        details={isUraniumDex ? <UraniumPokedexDetails /> : <PokedexDetails />}""",
    """        details={isUraniumDex
            ? <UraniumPokedexDetails />
            : isInsurgenceDex
                ? <InsurgencePokedexDetails />
                : <PokedexDetails />}""",
)

# Profile-local Insurgence Deltas/fakemon use packaged static art just like Uranium.
species_img = PKVAULT / "frontend/src/img/species-img.tsx"
replace_once(
    species_img,
    """import { getUraniumFrontSpritePath, isUraniumSpeciesId, URANIUM_PROFILE_ID } from '../romhacks/uranium-profile';""",
    """import { getUraniumFrontSpritePath, isUraniumSpeciesId, URANIUM_PROFILE_ID } from '../romhacks/uranium-profile';
import { getInsurgenceFrontSpritePath, isInsurgenceDexSpeciesId, INSURGENCE_PROFILE_ID } from '../romhacks/insurgence-profile';""",
)
replace_once(
    species_img,
    """        const isUranium = romHackProfile === URANIUM_PROFILE_ID && isUraniumSpeciesId(localSpeciesId);
        const fallbackIcon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='5' fill='%23444'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-size='20' fill='white'%3E%3F%3C/text%3E%3C/svg%3E";

        return <UISpeciesImg
            {...imgProps}
            data-rom-hack-profile={romHackProfile ?? undefined}
            data-local-species-id={localSpeciesId}
            sheetUrl={isUranium ? getUraniumFrontSpritePath(localSpeciesId) : fallbackIcon}
            spriteInfos={{ x: 0, y: 0, width: isUranium ? 80 : 32, height: isUranium ? 80 : 32 }}
            sourceRealHeight={isUranium ? 80 : 32}
            style={{
                ...imgProps.style,
                '--sprite-content-scale': isUranium ? (56 / 96) : undefined,
            } as React.CSSProperties}""",
    """        const isUranium = romHackProfile === URANIUM_PROFILE_ID && isUraniumSpeciesId(localSpeciesId);
        const isInsurgence = romHackProfile === INSURGENCE_PROFILE_ID && isInsurgenceDexSpeciesId(localSpeciesId);
        const isStaticRomHackSprite = isUranium || isInsurgence;
        const fallbackIcon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='5' fill='%23444'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-size='20' fill='white'%3E%3F%3C/text%3E%3C/svg%3E";
        const sheetUrl = isUranium
            ? getUraniumFrontSpritePath(localSpeciesId)
            : isInsurgence
                ? getInsurgenceFrontSpritePath(localSpeciesId)
                : fallbackIcon;

        return <UISpeciesImg
            {...imgProps}
            data-rom-hack-profile={romHackProfile ?? undefined}
            data-local-species-id={localSpeciesId}
            sheetUrl={sheetUrl}
            spriteInfos={{ x: 0, y: 0, width: isStaticRomHackSprite ? 80 : 32, height: isStaticRomHackSprite ? 80 : 32 }}
            sourceRealHeight={isStaticRomHackSprite ? 80 : 32}
            style={{
                ...imgProps.style,
                '--sprite-content-scale': isStaticRomHackSprite ? (56 / 96) : undefined,
            } as React.CSSProperties}""",
)

# Add a parallel save-dex endpoint for Insurgence.
route = PKVAULT / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(
    route,
    """    [HttpGet("romhack/uranium/dex")]
    public UraniumDexStateDTO GetUraniumDexState()
    {
        var seen = new HashSet<int>();
        var caught = new HashSet<int>();

        foreach (var loaders in savesLoadersService.GetAllLoaders())
        {
            if (loaders.Save.GetSave() is not EssentialsLegacySaveFile essentials
                || !string.Equals(essentials.ProfileId, "pokemon-uranium", StringComparison.Ordinal))
                continue;

            seen.UnionWith(essentials.SeenSpecies);
            caught.UnionWith(essentials.OwnedSpecies);
        }

        seen.UnionWith(caught);
        return new(
            Seen: [.. seen.OrderBy(x => x)],
            Caught: [.. caught.OrderBy(x => x)]
        );
    }""",
    """    [HttpGet("romhack/uranium/dex")]
    public UraniumDexStateDTO GetUraniumDexState()
        => GetEssentialsDexState("pokemon-uranium");

    [HttpGet("romhack/insurgence/dex")]
    public UraniumDexStateDTO GetInsurgenceDexState()
        => GetEssentialsDexState("pokemon-insurgence");

    private UraniumDexStateDTO GetEssentialsDexState(string profileId)
    {
        var seen = new HashSet<int>();
        var caught = new HashSet<int>();

        foreach (var loaders in savesLoadersService.GetAllLoaders())
        {
            if (loaders.Save.GetSave() is not EssentialsLegacySaveFile essentials
                || !string.Equals(essentials.ProfileId, profileId, StringComparison.Ordinal))
                continue;

            seen.UnionWith(essentials.SeenSpecies);
            caught.UnionWith(essentials.OwnedSpecies);
        }

        seen.UnionWith(caught);
        return new(
            Seen: [.. seen.OrderBy(x => x)],
            Caught: [.. caught.OrderBy(x => x)]
        );
    }""",
)

print("PKVault V8 alpha35 Gen6 Uranium/Insurgence dex overlays applied")
