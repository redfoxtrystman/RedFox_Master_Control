import { Card, Group, Space, Stack, Text } from '@mantine/core';
import { useQueries } from '@tanstack/react-query';
import React from 'react';
import { usePkmSaveIndex, getPkmSaveIndexOptions } from '../data/hooks/use-pkm-save-index';
import { useSaveInfosGetAll } from '../data/sdk/save-infos/save-infos.gen';
import { EntityContext, Gender } from '../data/sdk/model';
import { SpeciesImg } from '../img/species-img';
import { Route } from '../routes/pokedex';
import { UIPokedexMainSection } from '../ui/pokedex/main/section/ui-pokedex-main-section';
import { UIPokedexMainSectionHeader } from '../ui/pokedex/main/section/ui-pokedex-main-section-header';
import { UIPokedexItem } from '../ui/pokedex/pokedex-item/ui-pokedex-item';
import { UIPokedexFormItem } from '../ui/pokedex/pokedex-item/ui-pokedex-form-item';
import { UIPokedexDetails } from '../ui/pokedex/pokedex-details/ui-pokedex-details';
import { UIPokedexDetailsMain } from '../ui/pokedex/pokedex-details/ui-pokedex-details-main';
import { UIDetailsContent } from '../ui/storage/storage-details/content/ui-details-content';
import { UIDetailsContentStats } from '../ui/storage/storage-details/content/stats/ui-details-content-stats';
import { UIDetailsStatsRow } from '../ui/storage/storage-details/content/stats/ui-details-stats-row';
import { UIDetailsStatsTotalRow } from '../ui/storage/storage-details/content/stats/ui-details-stats-total-row';
import { usePokedexSelectExpanded } from '../pokedex/details/hooks/use-pokedex-select-expanded';
import { TmtTypeItem } from './tmt-type-item';
import {
  URANIUM_ADDED_SPECIES,
  URANIUM_DEX_OFFSET,
  URANIUM_PROFILE_ID,
  URANIUM_SPECIES,
} from './uranium-profile';

export const useUraniumDexState = () => {
  const savesQuery = useSaveInfosGetAll();
  const saveIds = React.useMemo(() =>
    Object.values(savesQuery.data?.data ?? {})
      .filter(save => save?.romHackProfile === URANIUM_PROFILE_ID)
      .map(save => save!.id)
      .sort((a, b) => a - b),
    [savesQuery.data]
  );

  const pkmQueries = useQueries({
    queries: saveIds.map(saveId => getPkmSaveIndexOptions(saveId)),
  });

  const owned = React.useMemo(() => {
    const values = new Set<number>();
    for (const query of pkmQueries) {
      for (const pkm of Object.values(query.data?.data.byId ?? {})) {
        if (pkm.romHackProfile !== URANIUM_PROFILE_ID || !pkm.romHackLocalSpeciesId)
          continue;
        const entry = URANIUM_SPECIES[pkm.romHackLocalSpeciesId];
        if (entry?.officialNationalDexId === null)
          values.add(pkm.romHackLocalSpeciesId);
      }
    }
    return values;
  }, [pkmQueries]);

  return {
    enabled: saveIds.length > 0,
    isPending: savesQuery.isPending || pkmQueries.some(q => q.isPending),
    owned,
  };
};

export const UraniumPokedexSection: React.FC = () => {
  const navigate = Route.useNavigate();
  const selected = Route.useSearch({ select: search => search.selected });
  const { enabled, owned } = useUraniumDexState();

  if (!enabled)
    return null;

  return <>
    <Card.Section inheritPadding withBorder>
      <UIPokedexMainSectionHeader
        generation='Pokémon Uranium'
        regions={['Tandor']}
        games={<Text size='sm'>Added Pokémon only</Text>}
        seenCount={owned.size}
        caughtCount={owned.size}
        ownedCount={owned.size}
        shinyCount={0}
        totalCount={URANIUM_ADDED_SPECIES.length}
      />
    </Card.Section>

    <Card.Section inheritPadding withBorder>
      <UIPokedexMainSection
        isFirstSection={false}
        minSpecies={URANIUM_DEX_OFFSET + 1}
        maxSpecies={URANIUM_DEX_OFFSET + 200}
      >
        {URANIUM_ADDED_SPECIES.map(entry => {
          const syntheticId = URANIUM_DEX_OFFSET + entry.id;
          const isOwned = owned.has(entry.id);
          const isSelected = selected === syntheticId;

          return <UIPokedexItem
            key={entry.id}
            id={'uranium-species-' + entry.id}
            species={entry.id}
            label={entry.name}
            selected={isSelected}
            onClick={() => navigate({
              search: { selected: isSelected ? undefined : syntheticId },
            })}
          >
            <UIPokedexFormItem
              genders={[Gender.Genderless]}
              isSeen={isOwned}
              isCaught={isOwned}
              isOwned={isOwned}
              isOwnedShiny={false}
              isMega={false}
            >
              <SpeciesImg
                species={entry.id}
                context={EntityContext.Gen3}
                form={0}
                profileLocalSpecies
                romHackProfile={URANIUM_PROFILE_ID}
                romHackLocalSpeciesId={entry.id}
                romHackSpeciesName={entry.name}
              />
            </UIPokedexFormItem>
          </UIPokedexItem>;
        })}
      </UIPokedexMainSection>
    </Card.Section>
  </>;
};

export const UraniumPokedexDetails: React.FC = () => {
  const navigate = Route.useNavigate();
  const selected = Route.useSearch({ select: search => search.selected });
  const { expanded, toggleExpanded } = usePokedexSelectExpanded();
  const { owned } = useUraniumDexState();

  if (selected === undefined || selected < URANIUM_DEX_OFFSET)
    return null;

  const localId = selected - URANIUM_DEX_OFFSET;
  const entry = URANIUM_SPECIES[localId];
  if (!entry || entry.officialNationalDexId !== null)
    return null;

  const isOwned = owned.has(localId);
  const statValues = [
    entry.baseStats[0] ?? 1,
    entry.baseStats[1] ?? 1,
    entry.baseStats[2] ?? 1,
    entry.baseStats[4] ?? 1,
    entry.baseStats[5] ?? 1,
    entry.baseStats[3] ?? 1,
  ];
  const statNames = ['hp', 'atk', 'def', 'spa', 'spd', 'spe'] as const;
  const total = statValues.reduce((sum, value) => sum + value, 0);

  return <UIPokedexDetails
    expanded={expanded}
    onExpand={toggleExpanded}
    onClose={() => navigate({ search: { selected: undefined } })}
    header={closeBtn => <Group px='md' py='xs' wrap='nowrap'>
      <Text fw={700}>Pokémon Uranium</Text>
      <Text c='dimmed' size='sm'>Uranium-added species</Text>
      <Space ml='auto' />
      {closeBtn}
    </Group>}
    main={<UIPokedexDetailsMain
      species={entry.id}
      speciesName={entry.name}
      gender={Gender.Genderless}
      isSeen={isOwned}
      isCaught={isOwned}
      isOwned={isOwned}
      types={entry.types.map(type => <TmtTypeItem key={type} type={type} />)}
    >
      <SpeciesImg
        species={entry.id}
        context={EntityContext.Gen3}
        form={0}
        profileLocalSpecies
        romHackProfile={URANIUM_PROFILE_ID}
        romHackLocalSpeciesId={entry.id}
        romHackSpeciesName={entry.name}
      />
    </UIPokedexDetailsMain>}
    items={<Text size='sm' c='dimmed'>Only Pokémon added by Uranium appear in this dex.</Text>}
    content={<UIDetailsContent content={[{
      name: 'stats',
      label: 'Stats',
      content: <UIDetailsContentStats>
        {statNames.map((stat, index) => <UIDetailsStatsRow
          key={stat}
          stat={stat}
          value={statValues[index]!}
          level={50}
        />)}
        <UIDetailsStatsTotalRow total={total} level={50} />
      </UIDetailsContentStats>,
    }]} />}
  />;
};
