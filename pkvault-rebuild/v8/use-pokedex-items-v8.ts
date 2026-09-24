import { useDexGetAll } from '../../../data/sdk/dex/dex.gen';
import type { DexItemDTO, DexItemForm, EntityContext, GameVersion, Gender, StaticVersion } from '../../../data/sdk/model';
import { useStaticData } from '../../../hooks/use-static-data';
import { Route } from '../../../routes/pokedex';
import { filterIsDefined } from '../../../util/filter-is-defined';
import { getGameInfos } from '../../details/util/get-game-infos';
import { usePokedexFilters } from './use-pokedex-filters';

export type DexProfile = 'tmt';

type PokedexItems = Counts & {
    isPending: boolean;
    speciesItemsByGenerationList: SpeciesItemsByGeneration[];
};

export type SpeciesItemsByGeneration = Counts & {
    generation: number;
    versionsForImgs: GameVersion[][];
    speciesInfos: SpeciesInfos[];
    minSpecies: number;
    maxSpecies: number;
    dexProfile?: DexProfile;
    sectionLabel?: string;
    sectionRegions?: string[];
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
    romHackTypes?: string[] | null;
};

const emptyCounts = (): Counts => ({
    seenCount: 0,
    caughtCount: 0,
    ownedCount: 0,
    shinyCount: 0,
    totalCount: 0,
    itemsCount: 0,
});

/**
 * Prepare all pokedex items by grouping them following filters on form/genders if any.
 *
 * V8 ROM-hack rule:
 * - National Dex sections always use official/canonical presentation.
 * - TMT gets a separate section with its own forms/types.
 * - Seen/caught/owned state from TMT still contributes to the canonical entry.
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

    const buildSpeciesInfo = (dexItems: DexItemDTO[], dexProfile?: DexProfile): SpeciesInfos | null => {
        const species = dexItems[ 0 ]?.species;
        if (!species)
            return null;

        const staticForms = staticData.species[ species ]?.forms ?? {};
        const speciesName = Object.values(staticForms)[ 0 ]?.[ 0 ]?.name ?? '';

        const allForms = dexItems.flatMap(value => value.forms)
            .filter(form => dexProfile === 'tmt'
                ? !!form.romHackTypes?.length
                : true)
            .map(form => dexProfile === 'tmt'
                ? form
                : { ...form, romHackTypes: null });

        if (!allForms.length)
            return null;

        const differentForms = [ ...new Set(allForms.map(form => form.form)) ];

        const hasGenderDifferencesByForm = differentForms.reduce<Record<number, boolean>>((acc, formValue) => {
            const hasGenderDifferences = allForms
                .some(form => form.form === formValue
                    && Object.values(staticForms).some(forms => forms?.[ form.form ]?.hasGenderDifferences));

            return {
                ...acc,
                [ formValue ]: hasGenderDifferences
            };
        }, {});

        const groupBy = <K extends keyof Pick<DexItemForm, 'form' | 'gender'>>(groupKeysRaw: K[]) => {
            return allForms.reduce<{
                [ key in string ]?: SpeciesFormItem
            }>((acc, form) => {
                const groupKeys = hasGenderDifferencesByForm[ form.form ]
                    ? groupKeysRaw
                    : groupKeysRaw.filter(key => key !== 'gender');

                const rawKey = groupKeys.map(groupKey => form[ groupKey ]).join('.');
                const key = dexProfile ? `${dexProfile}:${rawKey}` : rawKey;

                const oldGroup = acc[ key ];
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
                    romHackTypes: dexProfile === 'tmt'
                        ? oldGroup?.romHackTypes ?? form.romHackTypes
                        : null,
                };

                return {
                    ...acc,
                    [ key ]: group,
                };
            }, {});
        };

        const hasGenderDifferences = Object.values(hasGenderDifferencesByForm).some(v => v);
        const showGenders = showGendersRaw && hasGenderDifferences;

        const getItemsToRender = (): SpeciesFormItem[] => {
            if (!showForms && !showGenders)
                return [ groupBy([])[ dexProfile ? `${dexProfile}:` : '' ]! ];

            if (!showForms && showGenders)
                return Object.values(groupBy([ 'gender' ])).filter(filterIsDefined);

            if (showForms && !showGenders)
                return Object.values(groupBy([ 'form' ])).filter(filterIsDefined);

            return Object.values(groupBy([ 'form', 'gender' ])).filter(filterIsDefined);
        };

        const itemsToRender = getItemsToRender()
            .filter(filterIsDefined)
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

        return {
            species,
            speciesName,
            itemsToRender,
            isSeen: itemsToRender.some(item => item.isSeen),
        };
    };

    const speciesItemsByGeneration = filteredSpeciesList.reduce<{
        [ generation in number ]?: SpeciesItemsByGeneration;
    }>((acc, dexItems) => {
        const speciesInfo = buildSpeciesInfo(dexItems);
        if (!speciesInfo)
            return acc;

        const { species, itemsToRender, isSeen } = speciesInfo;
        const generation = staticData.species[ species ]?.generation ?? -1;

        const isCaught = itemsToRender.some(item => item.isCaught);
        const isOwned = itemsToRender.some(item => item.isOwned);
        const isOwnedShiny = itemsToRender.some(item => item.isOwnedShiny);

        const minSpecies = Math.min(acc[ generation ]?.minSpecies ?? Infinity, species);
        const maxSpecies = Math.max(acc[ generation ]?.maxSpecies ?? 0, species);

        const oldCounts = acc[ generation ] ?? emptyCounts();

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

                return [ ...versionsAcc, [ version ] ];
            }, []);

            return splitVersions.map(versions => versions.map(version => version.id as GameVersion));
        };

        const itemForGeneration: SpeciesItemsByGeneration = {
            generation,
            versionsForImgs: acc[ generation ]?.versionsForImgs ?? getVersionsForImgs(),
            speciesInfos: [
                ...acc[ generation ]?.speciesInfos ?? [],
                speciesInfo,
            ],
            minSpecies,
            maxSpecies,
            seenCount: oldCounts.seenCount + (isSeen ? 1 : 0),
            caughtCount: oldCounts.caughtCount + (isCaught ? 1 : 0),
            ownedCount: oldCounts.ownedCount + (isOwned ? 1 : 0),
            shinyCount: oldCounts.shinyCount + (isOwnedShiny ? 1 : 0),
            totalCount: oldCounts.totalCount + 1,
            itemsCount: oldCounts.itemsCount + itemsToRender.length,
        };

        return {
            ...acc,
            [ generation ]: itemForGeneration,
        };
    }, {});

    const canonicalSections = Object.values(speciesItemsByGeneration).filter(filterIsDefined);

    const tmtSpeciesInfos = filteredSpeciesList
        .map(dexItems => buildSpeciesInfo(dexItems, 'tmt'))
        .filter(filterIsDefined);

    const tmtSection = (() => {
        if (!tmtSpeciesInfos.length)
            return undefined;

        const counts = tmtSpeciesInfos.reduce<Counts>((acc, info) => {
            const isCaught = info.itemsToRender.some(item => item.isCaught);
            const isOwned = info.itemsToRender.some(item => item.isOwned);
            const isOwnedShiny = info.itemsToRender.some(item => item.isOwnedShiny);

            return {
                seenCount: acc.seenCount + (info.isSeen ? 1 : 0),
                caughtCount: acc.caughtCount + (isCaught ? 1 : 0),
                ownedCount: acc.ownedCount + (isOwned ? 1 : 0),
                shinyCount: acc.shinyCount + (isOwnedShiny ? 1 : 0),
                totalCount: acc.totalCount + 1,
                itemsCount: acc.itemsCount + info.itemsToRender.length,
            };
        }, emptyCounts());

        return {
            generation: 3,
            versionsForImgs: [],
            speciesInfos: tmtSpeciesInfos,
            minSpecies: Math.min(...tmtSpeciesInfos.map(info => info.species)),
            maxSpecies: Math.max(...tmtSpeciesInfos.map(info => info.species)),
            dexProfile: 'tmt' as const,
            sectionLabel: 'Too Many Types v1.6',
            sectionRegions: [ 'ROM Hack', 'Emerald TMT' ],
            ...counts,
        } satisfies SpeciesItemsByGeneration;
    })();

    const speciesItemsByGenerationList = [
        ...canonicalSections.filter(section => section.generation <= 3),
        ...tmtSection ? [ tmtSection ] : [],
        ...canonicalSections.filter(section => section.generation > 3),
    ];

    // Global totals remain canonical National Dex totals. The TMT section is a
    // second presentation of the same caught/owned history and must not double-count.
    const seenCount = canonicalSections.reduce((acc, item) => acc + item.seenCount, 0);
    const caughtCount = canonicalSections.reduce((acc, item) => acc + item.caughtCount, 0);
    const ownedCount = canonicalSections.reduce((acc, item) => acc + item.ownedCount, 0);
    const shinyCount = canonicalSections.reduce((acc, item) => acc + item.shinyCount, 0);
    const totalCount = canonicalSections.reduce((acc, item) => acc + item.totalCount, 0);
    const itemsCount = canonicalSections.reduce((acc, item) => acc + item.itemsCount, 0);

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
