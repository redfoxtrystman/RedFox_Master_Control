import React from 'react';
import { useDexGetAll } from '../../../data/sdk/dex/dex.gen';
import { EntityContext, type DexItemDTO, type DexItemForm, type SaveInfosDTO } from '../../../data/sdk/model';
import { useSaveInfosGetAll } from '../../../data/sdk/save-infos/save-infos.gen';
import { useStaticData } from '../../../hooks/use-static-data';
import { Route } from '../../../routes/pokedex';
import { filterIsDefined } from '../../../util/filter-is-defined';
import { useSelectCallback } from '../../../util/use-select-callback';

export const usePokedexDetailsSelect = () => {
    const selectedSpecies = Route.useSearch({ select: search => search.selected });
    const selectedSaveId = Route.useSearch({ select: search => search.selectedSaveId });
    const dexProfile = Route.useSearch({ select: search => search.dexProfile });

    const navigate = Route.useNavigate();
    const staticData = useStaticData();

    const speciesValuesQuery = useDexGetAll({
        query: {
            select: useSelectCallback(
                data => data.data[ selectedSpecies + "" ],
                [ selectedSpecies ]
            ),
        },
    });
    const saveInfosMainQuery = useSaveInfosGetAll();

    const [ selectedFormId, setSelectedFormId ] = React.useState('');

    const savesRecord = saveInfosMainQuery.data?.data ?? {};
    const speciesValuesRaw = Object.values(speciesValuesQuery.data ?? {});

    // TMT and National Dex are two presentations of the same ownership history.
    // In TMT mode keep only ROM-hack forms. In canonical mode deliberately
    // remove the ROM-hack presentation metadata so official types are shown.
    const speciesValues: DexItemDTO[] = speciesValuesRaw
        .map(value => ({
            ...value,
            forms: value.forms
                .filter(form => dexProfile === 'tmt' ? !!form.romHackTypes?.length : true)
                .map(form => dexProfile === 'tmt' ? form : { ...form, romHackTypes: null }),
        }))
        .filter(value => value.forms.length > 0);

    type GameSave = Pick<
        SaveInfosDTO,
        'id' | 'context' | 'generation' | 'trainerName' | 'romHackProfile'
    > & {
        displayedVersion: SaveInfosDTO['displayedVersion'] | null;
    };

    const gameSaves: GameSave[] = speciesValues
        .filter((spec) => spec.forms.some(form => form.isSeen))
        .map((spec) => spec.saveId === 0
            ? {
                id: 0,
                context: EntityContext.Gen9a,
                generation: 9,
                displayedVersion: null,
                trainerName: '',
                romHackProfile: null,
            }
            : savesRecord[ spec.saveId ])
        .filter(filterIsDefined);

    const setSelectedSaveId = React.useCallback((saveId: number | undefined) => {
        navigate({
            search: (search) => ({
                ...search,
                selectedSaveId: saveId,
            }),
        });
    }, [ navigate ]);

    const selectedSaveIfAny = selectedSaveId !== undefined
        ? gameSaves.find(save => save.id === selectedSaveId)
        : undefined;

    const selectedSave = selectedSaveIfAny ?? gameSaves[ 0 ];

    const selectedSpeciesValue = selectedSave && speciesValues.find(
        (value) => value.saveId === selectedSave.id
    );

    const getFormWeight = (f: DexItemForm) =>
        (f.isOwned ? 100000 : 0)
        + (f.isCaught ? 10000 : 0)
        + (f.isSeenShiny ? 1000 : 0)
        + (f.isSeenAlpha ? 100 : 0);

    const seenForms = selectedSpeciesValue?.forms.filter(form => form.isSeen) ?? [];

    const getDefaultForm = (formIndex: number) => {
        const formsSortedByWeight = [ ...seenForms ]
            .filter(form => form.form === formIndex)
            .sort((f1, f2) => getFormWeight(f2) - getFormWeight(f1));
        return formsSortedByWeight[ 0 ];
    };

    const selectedForm = selectedFormId
        ? seenForms.find(form => form.id === selectedFormId) ?? getDefaultForm(seenForms?.[ 0 ]?.form ?? 0)
        : getDefaultForm(seenForms?.[ 0 ]?.form ?? 0);

    const selectedFormIndexForms = seenForms
        .filter(form => form.form === selectedForm?.form)
        .sort((f1, f2) => getFormWeight(f2) - getFormWeight(f1));

    const selectedByFormIndex = (formIndex: number) => {
        const form = getDefaultForm(formIndex);
        if (form)
            setSelectedFormId(form.id);
    };

    if (!selectedSpecies || !gameSaves.length || !selectedSave || !selectedSpeciesValue || !selectedForm) {
        return null;
    }

    const allStaticForms = staticData.species[ selectedSpecies ]?.forms ?? {};

    // A TMT save is Gen3, but species such as Braixen have no official Gen3
    // static form table. Fall back to the newest official context containing
    // the selected form. This keeps the National Dex entry fully selectable.
    const staticForms = allStaticForms[ selectedSave.context ]
        ?? Object.values(allStaticForms)
            .reverse()
            .find(forms => forms?.[ selectedForm.form ] ?? forms?.[ 0 ])
        ?? [];

    const staticFormsFiltered = staticForms
        .map((staticForm, index) => ({ ...staticForm, index }));

    const selectedStaticFormWithIndex = staticFormsFiltered.find(sf => sf.index === selectedForm.form)
        ?? staticFormsFiltered[ 0 ];

    if (!selectedStaticFormWithIndex) {
        return null;
    }

    return {
        dexProfile,
        selectedSaveId,
        selectedSpecies,
        selectedSave,
        selectedForm,

        setSelectedSaveId,
        setSelectedFormId,
        selectedByFormIndex,

        selectedFormIndexForms,
        selectedStaticFormWithIndex,
        selectedSpeciesValue,

        gameSaves,
        staticFormsFiltered,
    };
};
