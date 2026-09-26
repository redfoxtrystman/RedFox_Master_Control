import { Card, Group, Space, Text } from '@mantine/core';
import { useQueries, useQuery } from '@tanstack/react-query';
import React from 'react';
import { getPkmSaveIndexOptions } from '../data/hooks/use-pkm-save-index';
import { customInstance } from '../data/mutator/custom-instance';
import { useSaveInfosGetAll } from '../data/sdk/save-infos/save-infos.gen';
import { EntityContext, Gender } from '../data/sdk/model';
import { SpeciesImg } from '../img/species-img';
import { usePokedexSelectExpanded } from '../pokedex/details/hooks/use-pokedex-select-expanded';
import { Route } from '../routes/pokedex';
import { UIPokedexDetails } from '../ui/pokedex/pokedex-details/ui-pokedex-details';
import { UIPokedexDetailsMain } from '../ui/pokedex/pokedex-details/ui-pokedex-details-main';
import { UIPokedexMainSection } from '../ui/pokedex/main/section/ui-pokedex-main-section';
import { UIPokedexMainSectionHeader } from '../ui/pokedex/main/section/ui-pokedex-main-section-header';
import { UIPokedexFormItem } from '../ui/pokedex/pokedex-item/ui-pokedex-form-item';
import { UIPokedexItem } from '../ui/pokedex/pokedex-item/ui-pokedex-item';
import { UIDetailsContent } from '../ui/storage/storage-details/content/ui-details-content';
import { UIDetailsContentStats } from '../ui/storage/storage-details/content/stats/ui-details-content-stats';
import { UIDetailsStatsRow } from '../ui/storage/storage-details/content/stats/ui-details-stats-row';
import { UIDetailsStatsTotalRow } from '../ui/storage/storage-details/content/stats/ui-details-stats-total-row';
import {
  INSURGENCE_DEX_OFFSET,
  INSURGENCE_DEX_SPECIES,
  INSURGENCE_DEX_SPECIES_LIST,
  INSURGENCE_GENERATION,
  INSURGENCE_PROFILE_ID,
} from './insurgence-profile';
import { TmtTypeItem } from './tmt-type-item';

type InsurgenceDexStatus = {
  seen: number[];
  caught: number[];
};

const loadInsurgenceDexStatus = async () =>
  (await customInstance<{ data: InsurgenceDexStatus; status: number; headers: Headers }>(
    '/api/storage/romhack/insurgence/dex'
  )).data;

const useInsurgenceDexState = () => {
  const savesQuery = useSaveInfosGetAll();
  const saveIds = React.useMemo(() =>
    Object.values(savesQuery.data?.data ?? {})
      .filter(save => save?.romHackProfile === INSURGENCE_PROFILE_ID)
      .map(save => save!.id)
      .sort((a, b) => a - b),
    [savesQuery.data]
  );

  const pkmQueries = useQueries({
    queries: saveIds.map(saveId => getPkmSaveIndexOptions(saveId)),
  });

  const dexQuery = useQuery({
    queryKey: ['insurgence-dex-state', ...saveIds],
    queryFn: loadInsurgenceDexStatus,
    enabled: saveIds.length > 0,
  });

  const dexSpeciesIds = React.useMemo(() => new Set(INSURGENCE_DEX_SPECIES_LIST.map(entry => entry.id)), []);

  const owned = React.useMemo(() => {
    const values = new Set<number>();
    for (const query of pkmQueries) {
      for (const pkm of Object.values(query.data?.data.byId ?? {})) {
        if (pkm.romHackProfile !== INSURGENCE_PROFILE_ID || !pkm.romHackLocalSpeciesId)
          continue;
        if (dexSpeciesIds.has(pkm.romHackLocalSpeciesId))
          values.add(pkm.romHackLocalSpeciesId);
      }
    }
    return values;
  }, [dexSpeciesIds, pkmQueries]);

  const seen = React.useMemo(
    () => new Set((dexQuery.data?.seen ?? []).filter(id => dexSpeciesIds.has(id))),
    [dexQuery.data, dexSpeciesIds],
  );
  const caught = React.useMemo(
    () => new Set((dexQuery.data?.caught ?? []).filter(id => dexSpeciesIds.has(id))),
    [dexQuery.data, dexSpeciesIds],
  );

  return {
    enabled: saveIds.length > 0,
    isPending: savesQuery.isPending || dexQuery.isPending || pkmQueries.some(q => q.isPending),
    seen,
    caught,
    owned,
  };
};

export const InsurgencePokedexSection: React.FC = () => {
  const navigate = Route.useNavigate();
  const selected = Route.useSearch({ select: search => search.selected });
  const filterGenerations = Route.useSearch({ select: search => search.filterGenerations }) ?? [];
  const { enabled, seen, caught, owned } = useInsurgenceDexState();

  if (!enabled)
    return null;
  if (filterGenerations.length > 0 && !filterGenerations.includes(INSURGENCE_GENERATION))
    return null;

  return <>
    <Card.Section inheritPadding withBorder>
      <UIPokedexMainSectionHeader
        generation='Generation 6'
        regions={['Torren']}
        games={<Text size='sm'>Pokémon Insurgence · Delta & Fakemon Pokédex</Text>}
        seenCount={seen.size}
        caughtCount={caught.size}
        ownedCount={owned.size}
        shinyCount={0}
        totalCount={INSURGENCE_DEX_SPECIES_LIST.length}
      />
    </Card.Section>

    <Card.Section inheritPadding withBorder>
      <UIPokedexMainSection
        isFirstSection={false}
        minSpecies={INSURGENCE_DEX_OFFSET + 727}
        maxSpecies={INSURGENCE_DEX_OFFSET + 925}
      >
        {INSURGENCE_DEX_SPECIES_LIST.map(entry => {
          const syntheticId = INSURGENCE_DEX_OFFSET + entry.id;
          const isSeen = seen.has(entry.id) || caught.has(entry.id) || owned.has(entry.id);
          const isCaught = caught.has(entry.id) || owned.has(entry.id);
          const isOwned = owned.has(entry.id);
          const isSelected = selected === syntheticId;

          return <UIPokedexItem
            key={entry.id}
            id={'insurgence-species-' + entry.id}
            species={entry.id}
            label={entry.name}
            selected={isSelected}
            onClick={() => navigate({
              search: { selected: isSelected ? undefined : syntheticId },
            })}
          >
            <UIPokedexFormItem
              genders={[Gender.Genderless]}
              isSeen={isSeen}
              isCaught={isCaught}
              isOwned={isOwned}
              isOwnedShiny={false}
              isMega={false}
            >
              <SpeciesImg
                species={entry.id}
                context={EntityContext.Gen3}
                form={0}
                profileLocalSpecies
                romHackProfile={INSURGENCE_PROFILE_ID}
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

export const InsurgencePokedexDetails: React.FC = () => {
  const navigate = Route.useNavigate();
  const selected = Route.useSearch({ select: search => search.selected });
  const { expanded, toggleExpanded } = usePokedexSelectExpanded();
  const { seen, caught, owned } = useInsurgenceDexState();

  if (selected === undefined || selected < INSURGENCE_DEX_OFFSET)
    return null;

  const localId = selected - INSURGENCE_DEX_OFFSET;
  const entry = INSURGENCE_DEX_SPECIES[localId];
  if (!entry)
    return null;

  const isSeen = seen.has(localId) || caught.has(localId) || owned.has(localId);
  const isCaught = caught.has(localId) || owned.has(localId);
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
      <Text fw={700}>Pokémon Insurgence</Text>
      <Text c='dimmed' size='sm'>Generation 6 · Torren #{localId}</Text>
      <Space ml='auto' />
      {closeBtn}
    </Group>}
    main={<UIPokedexDetailsMain
      species={entry.id}
      speciesName={entry.name}
      gender={Gender.Genderless}
      isSeen={isSeen}
      isCaught={isCaught}
      isOwned={isOwned}
      types={entry.types.map(type => <TmtTypeItem key={type} type={type} />)}
    >
      <SpeciesImg
        species={entry.id}
        context={EntityContext.Gen3}
        form={0}
        profileLocalSpecies
        romHackProfile={INSURGENCE_PROFILE_ID}
        romHackLocalSpeciesId={entry.id}
        romHackSpeciesName={entry.name}
      />
    </UIPokedexDetailsMain>}
    items={<Text size='sm' c='dimmed'>
      {entry.kind === 'delta' ? 'Pokémon Insurgence Delta variant.' : 'Pokémon Insurgence original fakemon.'}
    </Text>}
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
