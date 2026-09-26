from pathlib import Path

def put33(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ===========================================================================
# V8 alpha33:
# - item-bank pages can resize to the same 300-slot maximum as Pokemon boxes
# - same-save/same-pouch item moves use one atomic PlayerBag snapshot/write
# - inventory left/right copies get unique panel identities like Storage
# ===========================================================================

meta = PKVAULT / "PKVault.Core/db/entity/MetaEntity.cs"
replace_once(meta,
'''    ITEM_BANK_PAGES,
    ITEM_SAVE_PROVENANCE,
''',
'''    ITEM_BANK_PAGES,
    ITEM_BANK_PAGE_SIZES,
    ITEM_SAVE_PROVENANCE,
''')

item_service33 = PKVAULT / "PKVault.Core/storage/services/ItemBankService.cs"
item_service33_text = item_service33.read_text(encoding="utf-8")

item_service33_text = item_service33_text.replace(
'''[JsonSerializable(typeof(Dictionary<string, List<ItemOriginDTO>>))]
''',
'''[JsonSerializable(typeof(Dictionary<string, List<ItemOriginDTO>>))]
[JsonSerializable(typeof(Dictionary<int, int>))]
''',
1)

item_service33_text = item_service33_text.replace(
'''    public const int BankPageSlots = 30;
''',
'''    public const int BankPageSlots = 30;
    public const int MaxBankPageSlots = 300;
''',
1)

old_state = '''        var pageCount = await GetPageCount(bank);

        var bankPages = Enumerable.Range(1, pageCount)
            .Select(page => new InventoryBankPageDTO(
                Page: page,
                SlotCount: BankPageSlots,
                Slots: Enumerable.Range(0, BankPageSlots)
                    .Select(slot => ToBankSlotDto(
                        bank.GetValueOrDefault(BankKey(page, slot)),
                        others,
                        slot
                    ))
                    .ToList()
            ))
            .ToList();
'''
new_state = '''        var pageCount = await GetPageCount(bank);
        var pageSizes = await LoadPageSizes();

        var bankPages = Enumerable.Range(1, pageCount)
            .Select(page =>
            {
                var slotCount = GetPageSlotCount(page, bank, pageSizes);
                return new InventoryBankPageDTO(
                    Page: page,
                    SlotCount: slotCount,
                    Slots: Enumerable.Range(0, slotCount)
                        .Select(slot => ToBankSlotDto(
                            bank.GetValueOrDefault(BankKey(page, slot)),
                            others,
                            slot
                        ))
                        .ToList()
                );
            })
            .ToList();
'''
if old_state not in item_service33_text:
    raise RuntimeError("alpha33 GetState bank page anchor missing")
item_service33_text = item_service33_text.replace(old_state, new_state, 1)

old_create = '''    public async Task<int> CreatePage()
    {
        var bank = await LoadBankState();
        var nextPage = await GetPageCount(bank) + 1;
        await SavePageCount(nextPage);
        return nextPage;
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
'''
new_create = '''    public async Task<int> CreatePage()
    {
        var bank = await LoadBankState();
        var nextPage = await GetPageCount(bank) + 1;
        await SavePageCount(nextPage);
        return nextPage;
    }

    public async Task UpdatePageSize(int page, int slotCount)
    {
        var bank = await LoadBankState();
        var pageCount = await GetPageCount(bank);

        if (page <= 0 || page > pageCount)
            throw new ArgumentOutOfRangeException(nameof(page));

        var minSlotCount = bank.Values
            .Where(x => x.Page == page && x.Count > 0)
            .Select(x => x.Slot + 1)
            .DefaultIfEmpty(1)
            .Max();

        if (slotCount < minSlotCount || slotCount > MaxBankPageSlots)
        {
            throw new ArgumentOutOfRangeException(
                nameof(slotCount),
                $"PKVault item box size must be between {minSlotCount} and {MaxBankPageSlots}."
            );
        }

        var pageSizes = await LoadPageSizes();
        pageSizes[page] = slotCount;
        await SavePageSizes(pageSizes);
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
'''
if old_create not in item_service33_text:
    raise RuntimeError("alpha33 CreatePage anchor missing")
item_service33_text = item_service33_text.replace(old_create, new_create, 1)

old_move = '''        var others = await staticDataService.GetStaticOthers();
        var bank = await LoadBankState();
        var saveProvenance = await LoadSaveProvenance();

        var source = ResolveSource(input, bank, saveProvenance, others);
'''
new_move = '''        var others = await staticDataService.GetStaticOthers();
        var bank = await LoadBankState();
        var saveProvenance = await LoadSaveProvenance();

        if (IsSave(input.SourceKind)
            && IsSave(input.TargetKind)
            && input.SourceId == input.TargetId
            && string.Equals(input.SourcePouch, input.TargetPouch, StringComparison.Ordinal)
            && input.SourceSlot != input.TargetSlot)
        {
            return MoveWithinSameSavePouch(input, others);
        }

        var source = ResolveSource(input, bank, saveProvenance, others);
'''
if old_move not in item_service33_text:
    raise RuntimeError("alpha33 Move setup anchor missing")
item_service33_text = item_service33_text.replace(old_move, new_move, 1)

apply_anchor = '''    private TargetResult ApplyTarget(
'''
helper = r'''    private ItemBankMoveResult MoveWithinSameSavePouch(
        MoveInventoryItemActionInput input,
        StaticOthersData others
    )
    {
        var saveId = ParseSaveId(input.SourceId);
        var loaders = savesLoadersService.GetLoaders(saveId)
            ?? throw new KeyNotFoundException($"Save {saveId} not found.");

        var save = loaders.Save;
        var saveFile = save.GetSave();
        var bag = saveFile.Inventory;
        var pouch = GetPouch(bag, input.SourcePouch);

        if (!IsMovablePouch(pouch.Type))
            throw new InvalidOperationException(
                $"{GetPouchLabel(pouch.Type)} is protected and cannot be moved."
            );

        if ((uint)input.SourceSlot >= pouch.Items.Length)
            throw new ArgumentOutOfRangeException(nameof(input.SourceSlot));
        if ((uint)input.TargetSlot >= pouch.Items.Length)
            throw new ArgumentOutOfRangeException(nameof(input.TargetSlot));

        var sourceItem = pouch.Items[input.SourceSlot];

        if (sourceItem.Index <= 0 || sourceItem.Count <= 0)
            throw new InvalidOperationException(
                "The source save inventory slot is empty."
            );

        var map = GetVersionMap(others, saveFile);
        if (!map.TryGetValue(sourceItem.Index, out var itemKey)
            || string.IsNullOrWhiteSpace(itemKey))
        {
            throw new InvalidOperationException(
                $"Item {sourceItem.Index} in {save.Version} has no safe cross-generation mapping."
            );
        }

        var requested = Math.Min(sourceItem.Count, input.Count);
        if (requested <= 0)
            throw new InvalidOperationException("Nothing was moved.");

        var moved = MoveWithinSamePouch(
            bag,
            pouch,
            input.SourceSlot,
            input.TargetSlot,
            requested
        );

        if (moved <= 0)
            throw new InvalidOperationException(
                "The target stack has no room; nothing was moved."
            );

        bag.CopyTo(saveFile);
        loaders.Pkms.HasWritten = true;

        return new(
            ItemName: GetItemName(others, itemKey),
            MovedCount: moved,
            SourceVersion: save.Version,
            TargetVersion: save.Version
        );
    }

    private static int MoveWithinSamePouch(
        PlayerBag bag,
        InventoryPouch pouch,
        int sourceSlot,
        int targetSlot,
        int requested
    )
    {
        var source = pouch.Items[sourceSlot];
        var target = pouch.Items[targetSlot];

        if (target.Index == 0)
        {
            if (requested < source.Count)
            {
                throw new InvalidOperationException(
                    "Game-save bags keep one stack per item. Split this stack in a PKVault inventory box instead."
                );
            }

            var count = source.Count;
            target.Index = source.Index;
            target.SetNewDetails(count);
            source.Clear();
            pouch.ClearCount0();
            return count;
        }

        if (target.Index != source.Index)
        {
            throw new InvalidOperationException(
                "Target save slot contains a different item."
            );
        }

        var max = bag.GetMaxCount(pouch.Type, source.Index);
        var capacity = Math.Max(0, max - target.Count);
        var moved = Math.Min(requested, capacity);
        if (moved <= 0)
            return 0;

        target.Count += moved;
        source.Count -= moved;
        if (source.Count <= 0)
            source.Clear();

        pouch.ClearCount0();
        return moved;
    }

'''
if apply_anchor not in item_service33_text:
    raise RuntimeError("alpha33 ApplyTarget anchor missing")
item_service33_text = item_service33_text.replace(apply_anchor, helper + apply_anchor, 1)

page_count_anchor = '''    private async Task<Dictionary<string, BankStack>> LoadBankState()
'''
page_size_helpers = r'''    private async Task<Dictionary<int, int>> LoadPageSizes()
    {
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGE_SIZES);
        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return [];

        try
        {
            return JsonSerializer.Deserialize<Dictionary<int, int>>(
                entity.Value,
                JsonOptions
            ) ?? [];
        }
        catch (JsonException)
        {
            return [];
        }
    }

    private async Task SavePageSizes(Dictionary<int, int> pageSizes)
    {
        var value = JsonSerializer.Serialize(
            pageSizes
                .Where(x => x.Key > 0)
                .ToDictionary(
                    x => x.Key,
                    x => Math.Clamp(x.Value, 1, MaxBankPageSlots)
                ),
            JsonOptions
        );

        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGE_SIZES);
        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_BANK_PAGE_SIZES,
                Value = value,
            });
        }
        else
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
        }
    }

    private static int GetPageSlotCount(
        int page,
        Dictionary<string, BankStack> bank,
        Dictionary<int, int> pageSizes
    )
    {
        var occupiedMinimum = bank.Values
            .Where(x => x.Page == page && x.Count > 0)
            .Select(x => x.Slot + 1)
            .DefaultIfEmpty(1)
            .Max();

        var configured = pageSizes.GetValueOrDefault(page, BankPageSlots);
        return Math.Clamp(
            Math.Max(configured, occupiedMinimum),
            1,
            MaxBankPageSlots
        );
    }

'''
if page_count_anchor not in item_service33_text:
    raise RuntimeError("alpha33 LoadBankState anchor missing")
item_service33_text = item_service33_text.replace(page_count_anchor, page_size_helpers + page_count_anchor, 1)

item_service33_text = item_service33_text.replace('(uint)data.Slot >= BankPageSlots', '(uint)data.Slot >= MaxBankPageSlots')
item_service33_text = item_service33_text.replace('(uint)legacySlot >= BankPageSlots', '(uint)legacySlot >= MaxBankPageSlots')
item_service33_text = item_service33_text.replace('(uint)raw.Slot >= BankPageSlots', '(uint)raw.Slot >= MaxBankPageSlots')
item_service33_text = item_service33_text.replace('(uint)slot < BankPageSlots', '(uint)slot < MaxBankPageSlots')
item_service33_text = item_service33_text.replace(
'''    private static void ValidateBankSlot(int slot)
    {
        if ((uint)slot >= BankPageSlots)
            throw new ArgumentOutOfRangeException(nameof(slot));
    }
''',
'''    private static void ValidateBankSlot(int slot)
    {
        if ((uint)slot >= MaxBankPageSlots)
            throw new ArgumentOutOfRangeException(nameof(slot));
    }
''',
1)

item_service33.write_text(item_service33_text, encoding="utf-8")

storage_route33 = PKVAULT / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(storage_route33,
'''    [HttpPost("inventory/page")]
    public async Task<ItemInventoryStateDTO> CreateInventoryPage()
    {
        await actionService.CreateInventoryPage();
        return await itemBankService.GetState();
    }

    [HttpGet("action")]
''',
'''    [HttpPost("inventory/page")]
    public async Task<ItemInventoryStateDTO> CreateInventoryPage()
    {
        await actionService.CreateInventoryPage();
        return await itemBankService.GetState();
    }

    [HttpPut("inventory/page/size")]
    public async Task<ItemInventoryStateDTO> ResizeInventoryPage(
        int page,
        int slotCount
    )
    {
        await itemBankService.UpdatePageSize(page, slotCount);
        return await itemBankService.GetState();
    }

    [HttpGet("action")]
''')

inventory_api33 = PKVAULT / "frontend/src/inventory/inventory-api.ts"
replace_once(inventory_api33,
'''export const moveInventory = async (
''',
'''export const resizeInventoryPage = async (page: number, slotCount: number) => {
    const p = new URLSearchParams({
        page: String(page),
        slotCount: String(slotCount),
    });

    return (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/page/size?' + p.toString(),
        { method: 'PUT' }
    )).data;
};

export const moveInventory = async (
''')

put33("frontend/src/inventory/inventory-page-edit.tsx", r'''import { NumberInput, Text } from '@mantine/core';
import React from 'react';
import { usePopover } from '../ui/interaction/focus-controls/components/popover/hooks/use-popover';
import { UIFormCard } from '../ui/popover/popover-card/ui-form-card';

type InventoryPageEditProps = {
    page: number;
    slotCount: number;
    minSlotCount: number;
    onSubmit: (slotCount: number) => Promise<void>;
};

export const InventoryPageEdit: React.FC<InventoryPageEditProps> = ({
    page,
    slotCount,
    minSlotCount,
    onSubmit: onSubmitRaw,
}) => {
    const popover = usePopover();
    const [ value, setValue ] = React.useState(slotCount);

    const valid = Number.isFinite(value)
        && value >= minSlotCount
        && value <= 300;

    return <UIFormCard
        title={'Edit item box ' + page}
        disabled={!valid || value === slotCount}
        onSubmit={async event => {
            event.preventDefault();
            if (!valid)
                return;

            await onSubmitRaw(value);
            popover?.setOpened(false);
        }}
        miw={260}
    >
        <NumberInput
            label='Slots'
            description={minSlotCount + ' - 300'}
            min={minSlotCount}
            max={300}
            value={value}
            onChange={next => setValue(Number(next) || minSlotCount)}
        />

        <Text size='xs' c='dimmed'>
            Item boxes use the same maximum size as normal PKVault Pokémon boxes.
        </Text>
    </UIFormCard>;
};
''')

inventory_page33 = PKVAULT / "frontend/src/inventory/inventory-page.tsx"
replace_once(inventory_page33,
'''import { createInventoryPage, loadInventory, moveInventory } from './inventory-api';
''',
'''import { createInventoryPage, loadInventory, moveInventory, resizeInventoryPage } from './inventory-api';
''')
replace_once(inventory_page33,
'''    if (!state)
        return error ? <Alert color='red'>{error}</Alert> : <>Loading inventory…</>;
''',
'''    const onResizePage = React.useCallback(async (page: number, slotCount: number) => {
        try {
            const next = await resizeInventoryPage(page, slotCount);
            setState(next);
            setError(undefined);
            await queryClient.invalidateQueries();
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    if (!state)
        return error ? <Alert color='red'>{error}</Alert> : <>Loading inventory…</>;
''')
inventory_page33_text = inventory_page33.read_text(encoding="utf-8")
inventory_page33_text = inventory_page33_text.replace(
'''                onCreatePage={onCreatePage}
                onError={setError}
''',
'''                onCreatePage={onCreatePage}
                onResizePage={onResizePage}
                onError={setError}
''',
2)
inventory_page33.write_text(inventory_page33_text, encoding="utf-8")

inventory_panel33 = PKVAULT / "frontend/src/inventory/inventory-panel.tsx"
replace_once(inventory_panel33,
'''import { UIStoragePanelFooter } from '../ui/storage/storage-panel/ui-storage-panel-footer';
''',
'''import { UIStoragePanelFooter } from '../ui/storage/storage-panel/ui-storage-panel-footer';
import { usePanel } from '../ui/storage/storage-content/context/ui-panel-context';
''')
replace_once(inventory_panel33,
'''import { InventoryItem } from './inventory-item';
''',
'''import { InventoryItem } from './inventory-item';
import { InventoryPageEdit } from './inventory-page-edit';
''')
replace_once(inventory_panel33,
'''    onCreatePage: () => Promise<number>;
    onError: (message: string) => void;
''',
'''    onCreatePage: () => Promise<number>;
    onResizePage: (page: number, slotCount: number) => Promise<void>;
    onError: (message: string) => void;
''')
replace_once(inventory_panel33,
'''    state, initial, onSplit, onCreatePage, onError
}) => {
    const staticData = useStaticData();
''',
'''    state, initial, onSplit, onCreatePage, onResizePage, onError
}) => {
    const staticData = useStaticData();
    const panel = usePanel();
    const panelOrderOffset = panel === 'right' ? 1000 : 0;
''')

replace_once(inventory_panel33,
'''                return <UIBoxExpanded
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
''',
'''                const minSlotCount = (itemPage?.slots ?? [])
                    .filter(slot => !!slot.itemKey)
                    .map(slot => slot.slot + 1)
                    .reduce((max, value) => Math.max(max, value), 1);

                return <UIBoxExpanded
                    key={item.id}
                    id={panel + '-inventory-bank-' + item.id}
                    label={item.label}
                    selected={selected}
                    slotsStates={(itemPage?.slots ?? []).map(slot => !!slot.itemKey)}
                    editDropdown={itemPage && <InventoryPageEdit
                        page={itemPage.page}
                        slotCount={itemPage.slotCount}
                        minSlotCount={minSlotCount}
                        onSubmit={slotCount => onResizePage(itemPage.page, slotCount)}
                    />}
                    onSelect={() => {
                        selectPage(item.id);
                        reduce();
                    }}
                />;
''')

replace_once(inventory_panel33,
'''                return <UIBoxExpanded
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
''',
'''                return <UIBoxExpanded
                    key={item.id}
                    id={panel + '-inventory-pocket-' + item.id}
                    label={item.label}
                    selected={selected}
                    slotsStates={(pocket?.slots ?? []).map(slot => !!slot.itemKey)}
                    editDropdown={null}
                    onSelect={() => {
                        selectPocket(item.id);
                        reduce();
                    }}
                />;
''')

replace_once(inventory_panel33,
'''                    globalOrder={slot.slot}
                    nodeId={'inventory-item-' + location.kind + '-' + location.id + '-' + (location.pouch ?? '') + '-' + slot.slot}
''',
'''                    globalOrder={panelOrderOffset + slot.slot}
                    nodeId={'inventory-item-' + panel + '-' + location.kind + '-' + location.id + '-' + (location.pouch ?? '') + '-' + slot.slot}
''')

print("PKVault V8 alpha33 item-box resize + Red PC atomic move + duplicate inventory panel identity applied")
