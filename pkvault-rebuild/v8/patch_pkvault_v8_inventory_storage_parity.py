from pathlib import Path

def put26(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ===========================================================================
# V8 alpha26: inventory UI parity with normal PKVault storage.
# - real storage-sized slots (fixes collapsed empty slots)
# - normal storage box-list controls for item pages / pockets
# - create additional PKVault item boxes
# - storage scale button also controls the inventory page
# ===========================================================================

# Persist explicit empty item-box count in the session DB.
meta_entity = PKVAULT / "PKVault.Core/db/entity/MetaEntity.cs"
replace_once(meta_entity,
'''    USER_ID,
    ITEM_BANK,
}
''',
'''    USER_ID,
    ITEM_BANK,
    ITEM_BANK_PAGES,
}
''')

# New action type so creating an item box participates in normal Save/undo.
data_action = PKVAULT / "PKVault.Core/storage/data-action/DataAction.cs"
replace_once(data_action,
'''    SET_PKM_VERSION_MAIN,
    MOVE_ITEM,
}
''',
'''    SET_PKM_VERSION_MAIN,
    MOVE_ITEM,
    CREATE_ITEM_PAGE,
}
''')

# Service: explicit page count, create page, and persist empty inventory folders.
item_service = PKVAULT / "PKVault.Core/storage/services/ItemBankService.cs"
replace_once(item_service,
'''        var maxStoredPage = bank.Count == 0 ? 1 : Math.Max(1, bank.Values.Max(x => x.Page));
        var lastHasItems = bank.Values.Any(x => x.Page == maxStoredPage);
        var pageCount = lastHasItems ? maxStoredPage + 1 : maxStoredPage;

        var bankPages = Enumerable.Range(1, pageCount)
''',
'''        var pageCount = await GetPageCount(bank);

        var bankPages = Enumerable.Range(1, pageCount)
''')

replace_once(item_service,
'''    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
    {
''',
'''    public async Task<int> CreatePage()
    {
        var bank = await LoadBankState();
        var nextPage = await GetPageCount(bank) + 1;
        await SavePageCount(nextPage);
        return nextPage;
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
    {
''')

replace_once(item_service,
'''    public async Task WriteToFiles()
    {
        var bank = await LoadBankState();

        fileIOService.Delete(InventoryRoot);
        fileIOService.CreateDirectory(Path.Combine(InventoryRoot, "1"));

        foreach (var stack in bank.Values.OrderBy(x => x.Page).ThenBy(x => x.Slot))
''',
'''    public async Task WriteToFiles()
    {
        var bank = await LoadBankState();
        var pageCount = await GetPageCount(bank);

        fileIOService.Delete(InventoryRoot);
        foreach (var page in Enumerable.Range(1, pageCount))
            fileIOService.CreateDirectory(Path.Combine(InventoryRoot, page.ToString()));

        foreach (var stack in bank.Values.OrderBy(x => x.Page).ThenBy(x => x.Slot))
''')

replace_once(item_service,
'''    private async Task<Dictionary<string, BankStack>> LoadBankState()
    {
''',
'''    private async Task<int> GetPageCount(Dictionary<string, BankStack> bank)
    {
        var stackMax = bank.Count == 0 ? 1 : Math.Max(1, bank.Values.Max(x => x.Page));
        var fileMax = 1;

        if (Directory.Exists(InventoryRoot))
        {
            fileMax = Directory.EnumerateDirectories(InventoryRoot)
                .Select(Path.GetFileName)
                .Select(name => int.TryParse(name, out var page) ? page : 0)
                .DefaultIfEmpty(1)
                .Max();
        }

        var inferred = Math.Max(1, Math.Max(stackMax, fileMax));
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGES);

        return entity is not null && int.TryParse(entity.Value, out var stored) && stored > 0
            ? Math.Max(stored, inferred)
            : inferred;
    }

    private async Task SavePageCount(int pageCount)
    {
        pageCount = Math.Max(1, pageCount);
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGES);

        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_BANK_PAGES,
                Value = pageCount.ToString(),
            });
        }
        else
        {
            entity.Value = pageCount.ToString();
            await metaLoader.UpdateEntity(entity);
        }
    }

    private async Task<Dictionary<string, BankStack>> LoadBankState()
    {
''')

# Action used by the + box control.
put26("PKVault.Core/storage/data-action/CreateInventoryPageAction.cs", r'''namespace PKVault.Core;

public class CreateInventoryPageAction(ItemBankService itemBankService) : DataAction<int>
{
    protected override async Task<DataActionPayload> Execute(int input, DataUpdateFlags flags)
    {
        var page = await itemBankService.CreatePage();
        flags.SaveInfos = true;

        return new(
            type: DataActionType.CREATE_ITEM_PAGE,
            parameters: [ page ]
        );
    }
}
''')

program = PKVAULT / "PKVault.Core/Program.cs"
replace_once(program,
'''        services.AddScoped<MoveInventoryItemAction>();

        Log.Information($"Setup services - Loaders");
''',
'''        services.AddScoped<MoveInventoryItemAction>();
        services.AddScoped<CreateInventoryPageAction>();

        Log.Information($"Setup services - Loaders");
''')

action_service = PKVAULT / "PKVault.Core/storage/services/ActionService.cs"
replace_once(action_service,
'''    public async Task<DataUpdateFlags> Save()
    {
''',
'''    public async Task<DataUpdateFlags> CreateInventoryPage()
    {
        using var scope = sp.CreateScope();

        return await AddAction(
            scope,
            (scope) => scope.ServiceProvider.GetRequiredService<CreateInventoryPageAction>(),
            0
        );
    }

    public async Task<DataUpdateFlags> Save()
    {
''')

storage_route = PKVAULT / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(storage_route,
'''    [HttpGet("action")]
    public List<DataActionPayload> GetActions()
''',
'''    [HttpPost("inventory/page")]
    public async Task<ItemInventoryStateDTO> CreateInventoryPage()
    {
        await actionService.CreateInventoryPage();
        return await itemBankService.GetState();
    }

    [HttpGet("action")]
    public List<DataActionPayload> GetActions()
''')

# Swagger enum follows DataActionType.
swagger = PKVAULT / "PKVault.Core/swagger.json"
swagger_text = swagger.read_text(encoding="utf-8")
old_names = '''          "SET_PKM_VERSION_MAIN",
          "MOVE_ITEM"
'''
new_names = '''          "SET_PKM_VERSION_MAIN",
          "MOVE_ITEM",
          "CREATE_ITEM_PAGE"
'''
if old_names not in swagger_text:
    raise RuntimeError("alpha26 swagger enum-name anchor missing")
swagger_text = swagger_text.replace(old_names, new_names, 1)

old_vals = '''          19,
          20
'''
new_vals = '''          19,
          20,
          21
'''
if old_vals not in swagger_text:
    raise RuntimeError("alpha26 swagger enum-value anchor missing")
swagger.write_text(swagger_text.replace(old_vals, new_vals, 1), encoding="utf-8")

# Header: inventory gets the same storage scale button users already know.
header = PKVAULT / "frontend/src/header/header.tsx"
replace_once(header,
'''            'inventory': () => null,
''',
'''            'inventory': () => <Group wrap='nowrap' align='flex-start' gap='sm' style={{ flexGrow: 1 }}>
                <UISpriteSizingButton
                    localStorageKey='storage-sprite-size'
                    ml='auto'
                />
            </Group>,
''')

# Action timeline label/description for creating item boxes.
action_label = PKVAULT / "frontend/src/storage/actions/action-label.tsx"
replace_once(action_label,
'''    MoveItem: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='gray' size='xs' fz='sm'>
                <MoveIcon />
            </ThemeIcon>
        </>;
    },
};
''',
'''    MoveItem: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='gray' size='xs' fz='sm'>
                <MoveIcon />
            </ThemeIcon>
        </>;
    },
    CreateItemPage: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='gray' size='xs' fz='sm'>
                <PlusCircleIcon />
            </ThemeIcon>
        </>;
    },
};
''')
replace_once(action_label,
'''        [ DataActionType.MOVE_ITEM ]: ActionLabelMap.MoveItem,
    });
''',
'''        [ DataActionType.MOVE_ITEM ]: ActionLabelMap.MoveItem,
        [ DataActionType.CREATE_ITEM_PAGE ]: ActionLabelMap.CreateItemPage,
    });
''')

action_desc = PKVAULT / "frontend/src/storage/actions/hooks/use-action-description.ts"
replace_once(action_desc,
'''            [ DataActionType.MOVE_ITEM ]: () => {
                const source = typeof parameters[ 1 ] === 'number'
                    ? staticData.versions[ parameters[ 1 ] ]?.name
                    : 'PKVault Item Bank';
                const target = typeof parameters[ 2 ] === 'number'
                    ? staticData.versions[ parameters[ 2 ] ]?.name
                    : 'PKVault Item Bank';
                return 'Move ×' + parameters[ 3 ] + ' ' + parameters[ 0 ] + ' from ' + source + ' to ' + target;
            },
''',
'''            [ DataActionType.MOVE_ITEM ]: () => {
                const source = typeof parameters[ 1 ] === 'number'
                    ? staticData.versions[ parameters[ 1 ] ]?.name
                    : 'PKVault Item Bank';
                const target = typeof parameters[ 2 ] === 'number'
                    ? staticData.versions[ parameters[ 2 ] ]?.name
                    : 'PKVault Item Bank';
                return 'Move ×' + parameters[ 3 ] + ' ' + parameters[ 0 ] + ' from ' + source + ' to ' + target;
            },
            [ DataActionType.CREATE_ITEM_PAGE ]: () =>
                'Create PKVault item box ' + parameters[ 0 ],
''')

action_color = PKVAULT / "frontend/src/ui/actions-panel/utils/get-action-color.ts"
replace_once(action_color,
'''        case DataActionType.MOVE_ITEM:
            return 'gray';
''',
'''        case DataActionType.MOVE_ITEM:
        case DataActionType.CREATE_ITEM_PAGE:
            return 'gray';
''')

# API: create a real item box/page.
inventory_api = PKVAULT / "frontend/src/inventory/inventory-api.ts"
replace_once(inventory_api,
'''export const moveInventory = async (
''',
'''export const createInventoryPage = async () =>
    (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/page',
        { method: 'POST' }
    )).data;

export const moveInventory = async (
''')

# Slot geometry: use the same 96px footprint as normal PKVault storage,
# driven by the normal storage scale control.
inventory_item = PKVAULT / "frontend/src/inventory/inventory-item.tsx"
replace_once(inventory_item,
'''        pos='relative'
        mih={84}
        p='xs'
        style={{
            cursor: canDrag ? 'grab' : hasItem ? 'pointer' : 'default',
        }}
''',
'''        pos='relative'
        w='calc(96px * var(--sprite-species-size-multiplier, 1))'
        h='calc(96px * var(--sprite-species-size-multiplier, 1))'
        miw='calc(96px * var(--sprite-species-size-multiplier, 1))'
        mih='calc(96px * var(--sprite-species-size-multiplier, 1))'
        p='xs'
        style={{
            cursor: canDrag ? 'grab' : hasItem ? 'pointer' : 'default',
        }}
''')
replace_once(inventory_item,
'''            style={{ width: 48, height: 48 }}
''',
'''            style={{
                width: 'calc(48px * var(--sprite-species-size-multiplier, 1))',
                height: 'calc(48px * var(--sprite-species-size-multiplier, 1))',
            }}
''')
replace_once(inventory_item,
'''            size='sm'
            variant='filled'
''',
'''            size='md'
            variant='filled'
''')

# Rewrite panel header to use the actual PKVault box-list UI instead of tiny
# custom Tabs. The + control is the same style/placement as normal storage.
put26("frontend/src/inventory/inventory-panel.tsx", r'''import { Alert, Group, Tabs, Text } from '@mantine/core';
import React from 'react';
import { BoxType } from '../data/sdk/model';
import { getGameInfos } from '../pokedex/details/util/get-game-infos';
import { useStaticData } from '../hooks/use-static-data';
import { UIBoxExpanded } from '../ui/storage/storage-panel/box-list/ui-box-expanded';
import {
    UIStoragePanelBoxList,
    type UIBoxData,
} from '../ui/storage/storage-panel/box-list/ui-storage-panel-box-list';
import { UIStoragePanel } from '../ui/storage/storage-panel/ui-storage-panel';
import {
    UIStoragePanelGameList,
    type UIGameData,
} from '../ui/storage/storage-panel/game-list/ui-storage-panel-game-list';
import { getBoxColumns } from '../ui/storage/storage-panel/get-box-columns';
import { InventoryItem } from './inventory-item';
import type {
    InventoryBankPage,
    InventoryLocation,
    InventorySlot,
    InventoryState,
    SaveInventory,
    SaveInventoryPocket,
} from './types';

type ContainerSelection =
    | { kind: 'bank'; page: number }
    | { kind: 'save'; saveId: number; pouch?: string };

type InventoryPanelProps = {
    state: InventoryState;
    initial: ContainerSelection;
    onMove: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onCreatePage: () => Promise<number>;
    onError: (message: string) => void;
};

const pkvaultId = 'pkvault';

export const InventoryPanel: React.FC<InventoryPanelProps> = ({
    state, initial, onMove, onCreatePage, onError
}) => {
    const staticData = useStaticData();
    const [ selection, setSelection ] = React.useState<ContainerSelection>(initial);

    const selectedSave: SaveInventory | undefined = selection.kind === 'save'
        ? state.saves.find(s => s.saveId === selection.saveId)
        : undefined;

    const selectedBank: InventoryBankPage | undefined = selection.kind === 'bank'
        ? state.bankPages.find(p => p.page === selection.page) ?? state.bankPages[0]
        : undefined;

    const selectedPocket: SaveInventoryPocket | undefined = selection.kind === 'save' && selectedSave
        ? selectedSave.pockets.find(p => p.pouch === selection.pouch) ?? selectedSave.pockets[0]
        : undefined;

    const gameValue = selection.kind === 'bank' ? pkvaultId : String(selection.saveId);
    const gameData: UIGameData[] = [
        {
            id: pkvaultId,
            imgSrc: '/logo.svg',
            label: 'PKVault',
        },
        ...state.saves.map(save => ({
            id: String(save.saveId),
            imgSrc: getGameInfos(save.version).img,
            label: staticData.versions[save.version]?.name ?? String(save.version),
            disabled: !save.supported,
        })),
    ];

    const selectGame = (id: string) => {
        if (id === pkvaultId) {
            setSelection({
                kind: 'bank',
                page: selectedBank?.page ?? state.bankPages[0]?.page ?? 1,
            });
            return;
        }

        const save = state.saves.find(s => String(s.saveId) === id);
        if (!save)
            return;

        setSelection({
            kind: 'save',
            saveId: save.saveId,
            pouch: save.pockets[0]?.pouch,
        });
    };

    let slots: InventorySlot[] = [];
    let header: React.ReactNode = null;

    if (selection.kind === 'bank') {
        const page = selectedBank ?? state.bankPages[0];
        slots = page?.slots ?? [];

        const pageData: UIBoxData[] = state.bankPages.map(p => ({
            id: String(p.page),
            label: 'Box ' + p.page,
            type: BoxType.Box,
        }));

        const selectPage = (id: string) => {
            setSelection({ kind: 'bank', page: Number(id) });
        };

        header = <UIStoragePanelBoxList
            value={String(page?.page ?? 1)}
            data={pageData}
            onSelect={selectPage}
            onCreate={async () => {
                const newPage = await onCreatePage();
                setSelection({ kind: 'bank', page: newPage });
            }}
            renderTab={({ item, selected }, { reduce }) => <Tabs.Tab
                key={item.id}
                value={item.id}
                onClick={reduce}
                py={0}
                style={{ gap: 4 }}
            >
                <Text component={selected ? 'b' : undefined} textWrap='nowrap'>
                    {item.label}
                </Text>
            </Tabs.Tab>}
            renderExpanded={(data, { reduce }) => data.map(({ item, selected }) => {
                const itemPage = state.bankPages.find(p => String(p.page) === item.id);
                return <UIBoxExpanded
                    key={item.id}
                    id={item.id}
                    label={item.label}
                    selected={selected}
                    slotsStates={(itemPage?.slots ?? []).map(slot => !!slot.itemKey)}
                    editDropdown={null}
                    onSelect={() => {
                        selectPage(item.id);
                        reduce();
                    }}
                />;
            })}
            advancedActionSort={null}
            advancedDexSync={null}
        />;
    } else {
        slots = selectedPocket?.slots ?? [];

        const pocketData: UIBoxData[] = (selectedSave?.pockets ?? []).map(pocket => ({
            id: pocket.pouch,
            label: pocket.label,
            type: BoxType.Box,
        }));

        const selectPocket = (pouch: string) => {
            setSelection({
                kind: 'save',
                saveId: selection.saveId,
                pouch,
            });
        };

        header = <UIStoragePanelBoxList
            value={selectedPocket?.pouch ?? ''}
            data={pocketData}
            onSelect={selectPocket}
            renderTab={({ item, selected }, { reduce }) => <Tabs.Tab
                key={item.id}
                value={item.id}
                onClick={reduce}
                py={0}
                style={{ gap: 4 }}
            >
                <Text component={selected ? 'b' : undefined} textWrap='nowrap'>
                    {item.label}
                </Text>
            </Tabs.Tab>}
            renderExpanded={(data, { reduce }) => data.map(({ item, selected }) => {
                const pocket = selectedSave?.pockets.find(p => p.pouch === item.id);
                return <UIBoxExpanded
                    key={item.id}
                    id={item.id}
                    label={item.label}
                    selected={selected}
                    slotsStates={(pocket?.slots ?? []).map(slot => !!slot.itemKey)}
                    editDropdown={null}
                    onSelect={() => {
                        selectPocket(item.id);
                        reduce();
                    }}
                />;
            })}
            advancedActionSort={null}
            advancedDexSync={null}
        />;
    }

    const nearestEmpty = (slot: number) => {
        const empty = slots
            .filter(s => !s.itemKey)
            .map(s => s.slot)
            .sort((a, b) => Math.abs(a - slot) - Math.abs(b - slot) || a - b);
        return empty[0];
    };

    const cols = getBoxColumns(slots.length) ?? 6;

    return <UIStoragePanel
        gameTabs={<UIStoragePanelGameList
            value={gameValue}
            data={gameData}
            onChange={selectGame}
            expanded={false}
            sortValue='inventory'
            sortData={[ { value: 'inventory', label: 'Inventory' } ]}
            onSortChange={() => undefined}
            createActions={null}
            renderHoverCard={({ item }) => <Text>{item.label}</Text>}
            renderExpanded={() => null}
        />}
        header={header}
        footer={selection.kind === 'save' && selectedPocket?.protected
            ? <Alert color='yellow' py='xs'>
                {selectedPocket.label} is visible but protected from cross-game moves.
            </Alert>
            : null}
    >
        <Group
            gap={4}
            wrap='wrap'
            mx='auto'
            pos='relative'
            w='fit-content'
            style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(' + cols + ', auto)',
            }}
        >
            {slots.map(slot => {
                const location: InventoryLocation = selection.kind === 'bank'
                    ? {
                        kind: 'bank',
                        id: String(selectedBank?.page ?? 1),
                        slot: slot.slot,
                    }
                    : {
                        kind: 'save',
                        id: String(selection.saveId),
                        pouch: selectedPocket?.pouch,
                        slot: slot.slot,
                    };

                return <InventoryItem
                    key={slot.slot}
                    slot={slot}
                    location={location}
                    isBank={selection.kind === 'bank'}
                    nearestEmptySlot={selection.kind === 'bank' ? nearestEmpty(slot.slot) : undefined}
                    onMove={onMove}
                    onError={onError}
                />;
            })}
        </Group>
    </UIStoragePanel>;
};
''')

# Parent page wires create-page mutation to both sides.
inventory_page = PKVAULT / "frontend/src/inventory/inventory-page.tsx"
replace_once(inventory_page,
'''import { loadInventory, moveInventory } from './inventory-api';
''',
'''import { createInventoryPage, loadInventory, moveInventory } from './inventory-api';
''')

replace_once(inventory_page,
'''    if (!state)
''',
'''    const onCreatePage = React.useCallback(async () => {
        try {
            const next = await createInventoryPage();
            setState(next);
            setError(undefined);
            await queryClient.invalidateQueries();
            return Math.max(...next.bankPages.map(page => page.page));
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    if (!state)
''')

replace_once(inventory_page,
'''            left={<InventoryPanel
                state={state}
                initial={{ kind: 'bank', page: 1 }}
                onMove={onMove}
                onError={setError}
            />}
            right={<InventoryPanel
                state={state}
                initial={firstSave
                    ? { kind: 'save', saveId: firstSave.saveId, pouch: firstSave.pockets[0]?.pouch }
                    : { kind: 'bank', page: 1 }}
                onMove={onMove}
                onError={setError}
            />}
''',
'''            left={<InventoryPanel
                state={state}
                initial={{ kind: 'bank', page: 1 }}
                onMove={onMove}
                onCreatePage={onCreatePage}
                onError={setError}
            />}
            right={<InventoryPanel
                state={state}
                initial={firstSave
                    ? { kind: 'save', saveId: firstSave.saveId, pouch: firstSave.pockets[0]?.pouch }
                    : { kind: 'bank', page: 1 }}
                onMove={onMove}
                onCreatePage={onCreatePage}
                onError={setError}
            />}
''')

print("PKVault V8 alpha26 item-storage parity pass applied")
