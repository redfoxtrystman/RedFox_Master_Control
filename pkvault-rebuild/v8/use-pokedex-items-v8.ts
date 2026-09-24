import { useDexGetAll } from '../../../data/sdk/dex/dex.gen';
import type { DexItemForm, EntityContext, GameVersion, Gender, StaticVersion } from '../../../data/sdk/model';
import { useStaticData } from '../../../hooks/use-static-data';
import { Route } from '../../../routes/pokedex';
import { filterIsDefined } from '../../../util/filter-is-defined';
import { getGameInfos } from '../../details/util/get-game-infos';
import { usePokedexFilters } from './use-pokedex-filters';

type PokedexItems = Counts & {
    isPending: boolean;
    speciesItemsByGenerationList: SpeciesItemsByGeneration[];
};

type SpeciesItemsByGeneration = Counts & {
    generation: number;
    versionsForImgs: GameVersion[][];
    speciesInfos: SpeciesInfos[];
    minSpecies: number;
    maxSpecies: number;
};

type Counts = {
    seenCount: number;
    caughtCount: number;
    ownedCount: number;
    shinyCount: number;
    totalCount: number;
    itemsCount: number;
};

type SpeciesInfos = {
    species: number;
    speciesName: string;
    itemsToRender: SpeciesFormItem[];
    isSeen: boolean;
};

export type SpeciesFormItem = {
    id: string;
    context: EntityContext;
    species: number;
    form: number;
    genders: Gender[];
    isSeen?: boolean;
    isSeenShiny?: boolean;
    isSeenAlpha?: boolean;
    isCaught?: boolean;
    isOwned?: boolean;
    isOwnedShiny?: boolean;
};

/**
 * Normal National Pokédex only.
 *
 * TMT contributes seen/caught/owned state through DexTmtService, but ROM-hack
 * typing/presentation is intentionally not represented here. TMT-specific
 * information belongs to the storage/details UI.
 */
export const usePokedexItems = (): PokedexItems => {
    const staticData = useStaticData();

    const showForms = Route.useSearch({ select: (search) => search.showForms ?? false });
    const showGendersRaw = Route.useSearch({ select: (search) => search.showGenders ?? false });

    const { data, isPending } = useDexGetAll();
    const { isPkmFiltered, filterSpeciesValues } = usePokedexFilters();

    const speciesRecord = data?.data ?? {};

    const keys = Object.keys(speciesRecord)
        .map(Number)
        .sort((a, b) => a - b);

    const lastSpecies = keys[ keys.length - 1 ] ?? 0;
    const speciesList = new Array(lastSpecies).fill(0).map((_, i) => i + 1);

    const filteredSpeciesList = speciesList
        .map((species) =>
            Object.values(speciesRecord[ species + "" ] ?? {}).filter(
                filterSpeciesValues,
            ),
        )
        .filter((speciesValues) => !isPkmFiltered(speciesValues));

    const speciesItemsByGeneration = filteredSpeciesList.reduce<{
        [ generation in number ]?: SpeciesItemsByGeneration;
    }>((acc, dexItems) => {
        const species = dexItems[ 0 ]!.species;
        const generation = staticData.species[ species ]?.generation ?? -1;

        const staticForms = staticData.species[ species ]?.forms ?? {};
        const speciesName = Object.values(staticForms)[ 0 ]?.[ 0 ]?.name ?? '';
        const allForms = dexItems.flatMap(value => value.forms);

        const differentForms = [ ...new Set(allForms.map(form => form.form)) ];

        const hasGenderDifferencesByForm = differentForms.reduce<Record<number, boolean>>((formAcc, formValue) => {
            const hasGenderDifferences = allForms
                .some(form => form.form === formValue
                    && staticForms[ form.context ]?.[ form.form ]?.hasGenderDifferences);

            return {
                ...formAcc,
                [ formValue ]: hasGenderDifferences
            };
        }, {});

        const groupBy = <K extends keyof Pick<DexItemForm, 'form' | 'gender'>>(groupKeysRaw: K[]) => {
            return allForms.reduce<{
                [ key in string ]?: SpeciesFormItem
            }>((groupAcc, form) => {
                const groupKeys = hasGenderDifferencesByForm[ form.form ]
                    ? groupKeysRaw
                    : groupKeysRaw.filter(key => key !== 'gender');

                const key = groupKeys.map(groupKey => form[ groupKey ]).join('.');
                const oldGroup = groupAcc[ key ];
                const formValue = Math.min(oldGroup?.form ?? 99, form.form);

                const getContext = (): EntityContext => {
                    const initialContext = Math.max(oldGroup?.context ?? -1, form.context) as EntityContext;
                    if (staticForms[ initialContext ]?.[ formValue ])
                        return initialContext;

                    return (Object.keys(staticForms)
                        .reverse()
                        .find(val => staticForms[ val ]?.[ formValue ]) ?? initialContext) as EntityContext;
                };

                const group: SpeciesFormItem = {
                    ...oldGroup,
                    id: key,
                    context: getContext(),
                    species,
                    form: formValue,
                    genders: [ ...new Set([ form.gender, ...oldGroup?.genders ?? [] ]) ].sort(),
                    isSeen: oldGroup?.isSeen || form.isSeen,
                    isSeenShiny: oldGroup?.isSeenShiny || form.isSeenShiny,
                    isSeenAlpha: oldGroup?.isSeenAlpha || form.isSeenAlpha,
                    isCaught: oldGroup?.isCaught || form.isCaught,
                    isOwned: oldGroup?.isOwned || form.isOwned,
                    isOwnedShiny: oldGroup?.isOwnedShiny || form.isOwnedShiny,
                };

                return {
                    ...groupAcc,
                    [ key ]: group,
                };
            }, {});
        };

        const hasGenderDifferences = Object.values(hasGenderDifferencesByForm).some(v => v);
        const showGenders = showGendersRaw && hasGenderDifferences;

        const getItemsToRender = (): SpeciesFormItem[] => {
            if (!showForms && !showGenders)
                return [ groupBy([])[ '' ]! ];

            if (!showForms && showGenders)
                return Object.values(groupBy([ 'gender' ])).filter(filterIsDefined);

            if (showForms && !showGenders)
                return Object.values(groupBy([ 'form' ])).filter(filterIsDefined);

            return Object.values(groupBy([ 'form', 'gender' ])).filter(filterIsDefined);
        };

        const itemsToRender = getItemsToRender()
            .sort((g1, g2) => {
                if (g1.species !== g2.species)
                    return g1.species - g2.species;

                if (g1.form !== g2.form)
                    return g1.form - g2.form;

                if (g1.genders.length === 1 && g2.genders.length === 1
                    && g1.genders[ 0 ] !== g2.genders[ 0 ])
                    return g1.genders[ 0 ]! - g2.genders[ 0 ]!;

                return 0;
            });

        const isSeen = itemsToRender.some(item => item.isSeen);
        const isCaught = itemsToRender.some(item => item.isCaught);
        const isOwned = itemsToRender.some(item => item.isOwned);
        const isOwnedShiny = itemsToRender.some(item => item.isOwnedShiny);

        const minSpecies = Math.min(acc[ generation ]?.minSpecies ?? Infinity, species);
        const maxSpecies = Math.max(acc[ generation ]?.maxSpecies ?? 0, species);

        const seenCount = acc[ generation ]?.seenCount ?? 0;
        const caughtCount = acc[ generation ]?.caughtCount ?? 0;
        const ownedCount = acc[ generation ]?.ownedCount ?? 0;
        const shinyCount = acc[ generation ]?.shinyCount ?? 0;
        const totalCount = acc[ generation ]?.totalCount ?? 0;
        const itemsCount = acc[ generation ]?.itemsCount ?? 0;

        const getVersionsForImgs = () => {
            const versions = Object.values(staticData.versions)
                .filter(version =>
                    version.isGameVersion
                    && version.region.some(region => staticData.generations[ generation ]?.regions.includes(region))
                )
                .sort((v1, v2) => v1.generation - v2.generation);

            const filteredVersions = Object.values(
                versions.reduce<Record<string, StaticVersion>>((versionsAcc, version) => ({
                    ...versionsAcc,
                    [ getGameInfos(version.id as GameVersion).img ]: version,
                }), {})
            );

            const splitVersions = filteredVersions.reduce<StaticVersion[][]>((versionsAcc, version) => {
                const previousArr = versionsAcc[ versionsAcc.length - 1 ];
                const previousVersion = previousArr && previousArr[ previousArr.length - 1 ];

                if (previousVersion && previousVersion.context === version.context) {
                    previousArr.push(version);
                    return versionsAcc;
                }

                return [
                    ...versionsAcc,
                    [ version ]
                ];
            }, []);

            return splitVersions.map(versions => versions.map(version => version.id as GameVersion));
        };

        const versionsForImgs = acc[ generation ]?.versionsForImgs ?? getVersionsForImgs();

        const itemForGeneration: SpeciesItemsByGeneration = {
            ...acc[ generation ],
            generation,
            versionsForImgs,
            speciesInfos: [
                ...acc[ generation ]?.speciesInfos ?? [],
                {
                    species,
                    speciesName,
                    itemsToRender,
                    isSeen,
                },
            ],
            minSpecies,
            maxSpecies,
            seenCount: seenCount + (isSeen ? 1 : 0),
            caughtCount: caughtCount + (isCaught ? 1 : 0),
            ownedCount: ownedCount + (isOwned ? 1 : 0),
            shinyCount: shinyCount + (isOwnedShiny ? 1 : 0),
            totalCount: totalCount + 1,
            itemsCount: itemsCount + itemsToRender.length,
        };

        return {
            ...acc,
            [ generation ]: itemForGeneration,
        } satisfies typeof acc;
    }, {});

    const speciesItemsByGenerationList = Object.values(speciesItemsByGeneration)
        .filter(filterIsDefined)
        .sort((a, b) => a.generation - b.generation);

    const seenCount = speciesItemsByGenerationList.reduce((acc, item) => acc + item.seenCount, 0);
    const caughtCount = speciesItemsByGenerationList.reduce((acc, item) => acc + item.caughtCount, 0);
    const ownedCount = speciesItemsByGenerationList.reduce((acc, item) => acc + item.ownedCount, 0);
    const shinyCount = speciesItemsByGenerationList.reduce((acc, item) => acc + item.shinyCount, 0);
    const totalCount = speciesItemsByGenerationList.reduce((acc, item) => acc + item.totalCount, 0);
    const itemsCount = speciesItemsByGenerationList.reduce((acc, item) => acc + item.itemsCount, 0);

    return {
        isPending,
        speciesItemsByGenerationList,
        seenCount,
        caughtCount,
        ownedCount,
        shinyCount,
        totalCount,
        itemsCount,
    };
};
