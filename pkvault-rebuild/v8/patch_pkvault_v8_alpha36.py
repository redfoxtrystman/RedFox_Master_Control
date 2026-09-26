from pathlib import Path
import sys

PKVAULT = Path(sys.argv[1]).resolve()

def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"alpha36 anchor missing in {path}: {old[:160]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

pokedex_list = PKVAULT / "frontend/src/pokedex/list/pokedex-list.tsx"

replace_once(
    pokedex_list,
    """import { useStaticData } from "../../hooks/use-static-data";""",
    """import { useStaticData } from "../../hooks/use-static-data";
import { useSaveInfosGetAll } from '../../data/sdk/save-infos/save-infos.gen';""",
)

replace_once(
    pokedex_list,
    """import { InsurgencePokedexSection } from '../../romhacks/insurgence-pokedex';""",
    """import { InsurgencePokedexSection } from '../../romhacks/insurgence-pokedex';
import { URANIUM_PROFILE_ID } from '../../romhacks/uranium-profile';
import { INSURGENCE_PROFILE_ID } from '../../romhacks/insurgence-profile';""",
)

replace_once(
    pokedex_list,
    """  const staticData = useStaticData();

  const {
    isPending,
    speciesItemsByGenerationList,
  } = usePokedexItems();
""",
    """  const staticData = useStaticData();
  const saveInfosQuery = useSaveInfosGetAll();

  const {
    isPending,
    speciesItemsByGenerationList,
  } = usePokedexItems();

  const activeRomHackProfiles = React.useMemo(() => {
    const profiles = new Set<string>();
    for (const save of Object.values(saveInfosQuery.data?.data ?? {})) {
      if (save?.romHackProfile)
        profiles.add(save.romHackProfile);
    }
    return profiles;
  }, [saveInfosQuery.data]);

  const hasUraniumDex = activeRomHackProfiles.has(URANIUM_PROFILE_ID);
  const hasInsurgenceDex = activeRomHackProfiles.has(INSURGENCE_PROFILE_ID);
  const hasFanGameDex = hasUraniumDex || hasInsurgenceDex;

  // Fan-game dexes are Gen-6-era overlays. Put them immediately after the
  // last vanilla generation <= 6. If no such vanilla generation is currently
  // represented by loaded saves, insert them before the first >6 generation;
  // if there are no vanilla groups at all, they become the only dex sections.
  const fanGameInsertAfterIndex = React.useMemo(() => {
    let result = -1;
    speciesItemsByGenerationList.forEach((group, index) => {
      if (group.generation <= 6)
        result = index;
    });
    return result;
  }, [speciesItemsByGenerationList]);
""",
)

replace_once(
    pokedex_list,
    """      {!isPending && speciesItemsByGenerationList.length === 0 && <EmptyState
        size='sm'
        icon={<PackageOpenIcon />}
        title={t('dex.list.empty')}
      />}""",
    """      {!isPending && !saveInfosQuery.isPending && speciesItemsByGenerationList.length === 0 && !hasFanGameDex && <EmptyState
        size='sm'
        icon={<PackageOpenIcon />}
        title={t('dex.list.empty')}
      />}

      {hasFanGameDex && fanGameInsertAfterIndex < 0 && <>
        <UraniumPokedexSection />
        <InsurgencePokedexSection />
      </>}""",
)

replace_once(
    pokedex_list,
    """          {generation === 6 && <>
            <UraniumPokedexSection />
            <InsurgencePokedexSection />
          </>}
""",
    """          {hasFanGameDex && i === fanGameInsertAfterIndex && <>
            <UraniumPokedexSection />
            <InsurgencePokedexSection />
          </>}
""",
)

print("PKVault V8 alpha36 active-save fan-game dex visibility fix applied")
