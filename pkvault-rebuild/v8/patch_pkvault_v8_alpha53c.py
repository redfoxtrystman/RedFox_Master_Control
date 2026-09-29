from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def patch(path, old, new, label):
    p = root / path
    t = p.read_text(encoding='utf-8')
    if old not in t:
        raise RuntimeError(f'alpha53c anchor not found: {label} in {path}')
    p.write_text(t.replace(old, new, 1), encoding='utf-8')

svc = 'PKVault.Core/storage/services/ItemBankService.cs'
patch(svc,
'''public record TrashInventoryItemActionInput(
    string SourceKind,
    string SourceId,
    int SourceSlot
);

public record ItemBankMoveResult(
''',
'''public record TrashInventoryItemActionInput(
    string SourceKind,
    string SourceId,
    int SourceSlot
);

public record MoveInventoryPageActionInput(int Page, int TargetPage);
public record DeleteInventoryPageActionInput(int Page);

public record MoveInventoryPageResult(string Name, int FromPage, int ToPage);
public record DeleteInventoryPageResult(string Name, int Page, int StackCount, long ItemCount);

public record ItemBankMoveResult(
''',
'page action records')

patch(svc,
'''    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
''',
'''    public async Task<MoveInventoryPageResult> MovePage(int page, int targetPage)
    {
        var bank = await LoadBankState();
        var pageCount = await GetPageCount(bank);
        ValidatePageNumber(page, pageCount, nameof(page));
        ValidatePageNumber(targetPage, pageCount, nameof(targetPage));

        var names = await LoadPageNames();
        var pageName = names.GetValueOrDefault(page, $"Box {page}");
        if (page == targetPage)
            return new(pageName, page, targetPage);

        var reordered = bank.Values
            .Select(stack => stack with
            {
                Page = ReorderPageNumber(stack.Page, page, targetPage),
            })
            .ToDictionary(stack => BankKey(stack.Page, stack.Slot), StringComparer.Ordinal);

        var pageSizes = RemapPageMetadata(
            await LoadPageSizes(), pageCount,
            current => ReorderPageNumber(current, page, targetPage));
        var pageNames = RemapPageMetadata(
            names, pageCount,
            current => ReorderPageNumber(current, page, targetPage));

        await SaveBankState(reordered);
        await SavePageSizes(pageSizes);
        await SavePageNames(pageNames);

        return new(pageName, page, targetPage);
    }

    public async Task<DeleteInventoryPageResult> DeletePage(int page)
    {
        var bank = await LoadBankState();
        var pageCount = await GetPageCount(bank);
        ValidatePageNumber(page, pageCount, nameof(page));
        if (pageCount <= 1)
            throw new InvalidOperationException("PKVault Item Bank must keep at least one item box.");

        var names = await LoadPageNames();
        var pageName = names.GetValueOrDefault(page, $"Box {page}");
        var removed = bank.Values.Where(stack => stack.Page == page).ToArray();

        var compacted = bank.Values
            .Where(stack => stack.Page != page)
            .Select(stack => stack.Page > page ? stack with { Page = stack.Page - 1 } : stack)
            .ToDictionary(stack => BankKey(stack.Page, stack.Slot), StringComparer.Ordinal);

        var pageSizes = RemapPageMetadata(
            await LoadPageSizes(), pageCount,
            current => current == page ? null : current > page ? current - 1 : current);
        var pageNames = RemapPageMetadata(
            names, pageCount,
            current => current == page ? null : current > page ? current - 1 : current);

        await SaveBankState(compacted);
        await SavePageSizes(pageSizes);
        await SavePageNames(pageNames);
        await SavePageCount(pageCount - 1);

        return new(
            pageName,
            page,
            removed.Length,
            removed.Sum(stack => stack.Count)
        );
    }

    private static int ReorderPageNumber(int current, int page, int targetPage)
    {
        if (current == page)
            return targetPage;
        if (page < targetPage && current > page && current <= targetPage)
            return current - 1;
        if (page > targetPage && current >= targetPage && current < page)
            return current + 1;
        return current;
    }

    private static Dictionary<int, T> RemapPageMetadata<T>(
        Dictionary<int, T> source,
        int pageCount,
        Func<int, int?> remap
    )
    {
        var result = new Dictionary<int, T>();
        foreach (var pair in source)
        {
            if (pair.Key <= 0 || pair.Key > pageCount)
                continue;
            var target = remap(pair.Key);
            if (target is > 0)
                result[target.Value] = pair.Value;
        }
        return result;
    }

    private static void ValidatePageNumber(int page, int pageCount, string parameterName)
    {
        if (page <= 0 || page > pageCount)
            throw new ArgumentOutOfRangeException(parameterName);
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
''',
'page methods')

(root / 'PKVault.Core/storage/data-action/MoveInventoryPageAction.cs').write_text(
'''namespace PKVault.Core;

public class MoveInventoryPageAction(ItemBankService itemBankService) : DataAction<MoveInventoryPageActionInput>
{
    protected override async Task<DataActionPayload> Execute(MoveInventoryPageActionInput input, DataUpdateFlags flags)
    {
        var result = await itemBankService.MovePage(input.Page, input.TargetPage);
        flags.SaveInfos = true;
        return new(
            type: DataActionType.MOVE_ITEM_PAGE,
            parameters: [result.Name, result.FromPage, result.ToPage]
        );
    }
}
''', encoding='utf-8')

(root / 'PKVault.Core/storage/data-action/DeleteInventoryPageAction.cs').write_text(
'''namespace PKVault.Core;

public class DeleteInventoryPageAction(ItemBankService itemBankService) : DataAction<DeleteInventoryPageActionInput>
{
    protected override async Task<DataActionPayload> Execute(DeleteInventoryPageActionInput input, DataUpdateFlags flags)
    {
        var result = await itemBankService.DeletePage(input.Page);
        flags.SaveInfos = true;
        return new(
            type: DataActionType.DELETE_ITEM_PAGE,
            parameters: [result.Name, result.Page, result.ItemCount, result.StackCount]
        );
    }
}
''', encoding='utf-8')

patch('PKVault.Core/storage/data-action/DataAction.cs',
'''    CREATE_ITEM_PAGE,
    TRASH_ITEM,
}
''',
'''    CREATE_ITEM_PAGE,
    TRASH_ITEM,
    MOVE_ITEM_PAGE,
    DELETE_ITEM_PAGE,
}
''',
'DataActionType')

patch('PKVault.Core/Program.cs',
'''        services.AddScoped<CreateInventoryPageAction>();
''',
'''        services.AddScoped<CreateInventoryPageAction>();
        services.AddScoped<MoveInventoryPageAction>();
        services.AddScoped<DeleteInventoryPageAction>();
''',
'action registration')

patch('PKVault.Core/storage/services/ActionService.cs',
'''    public async Task<DataUpdateFlags> Save()
''',
'''    public async Task<DataUpdateFlags> MoveInventoryPage(int page, int targetPage)
    {
        using var scope = sp.CreateScope();
        return await AddAction(
            scope,
            scope => scope.ServiceProvider.GetRequiredService<MoveInventoryPageAction>(),
            new(page, targetPage)
        );
    }

    public async Task<DataUpdateFlags> DeleteInventoryPage(int page)
    {
        using var scope = sp.CreateScope();
        return await AddAction(
            scope,
            scope => scope.ServiceProvider.GetRequiredService<DeleteInventoryPageAction>(),
            new(page)
        );
    }

    public async Task<DataUpdateFlags> Save()
''',
'ActionService page methods')

patch('PKVault.Core/storage/routes/StorageRoute.cs',
'''    [HttpGet("action")]
''',
'''    [HttpPut("inventory/page/order")]
    public async Task<ItemInventoryStateDTO> MoveInventoryPage(int page, int targetPage)
    {
        await actionService.MoveInventoryPage(page, targetPage);
        return await itemBankService.GetState();
    }

    [HttpDelete("inventory/page")]
    public async Task<ItemInventoryStateDTO> DeleteInventoryPage(int page)
    {
        await actionService.DeleteInventoryPage(page);
        return await itemBankService.GetState();
    }

    [HttpGet("action")]
''',
'routes')

api = root / 'frontend/src/inventory/inventory-api.ts'
t = api.read_text(encoding='utf-8')
old = '''export const moveInventory = async (
'''
new = '''export const moveInventoryPage = async (page: number, targetPage: number) => {
    const p = new URLSearchParams({
        page: String(page),
        targetPage: String(targetPage),
    });

    return (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/page/order?' + p.toString(),
        { method: 'PUT' }
    )).data;
};

export const deleteInventoryPage = async (page: number) => {
    const p = new URLSearchParams({ page: String(page) });
    return (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/page?' + p.toString(),
        { method: 'DELETE' }
    )).data;
};

export const moveInventory = async (
'''
if old not in t:
    raise RuntimeError('alpha53c inventory api anchor')
api.write_text(t.replace(old, new, 1), encoding='utf-8')

page = 'frontend/src/inventory/inventory-page.tsx'
patch(page,
'''import { createInventoryPage, editInventoryPage, loadInventory, moveInventory, moveMoney, trashInventory } from './inventory-api';
''',
'''import { createInventoryPage, deleteInventoryPage, editInventoryPage, loadInventory, moveInventory, moveInventoryPage, moveMoney, trashInventory } from './inventory-api';
''',
'inventory imports')

patch(page,
'''    const onTrash = React.useCallback(async (source: InventoryLocation) => {
''',
'''    const onMovePage = React.useCallback(async (page: number, targetPage: number) => {
        try {
            setState(await moveInventoryPage(page, targetPage));
            setError(undefined);
            await queryClient.invalidateQueries();
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    const onDeletePage = React.useCallback(async (page: number) => {
        try {
            setState(await deleteInventoryPage(page));
            setError(undefined);
            await queryClient.invalidateQueries();
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    const onTrash = React.useCallback(async (source: InventoryLocation) => {
''',
'page callbacks')

for label in ('left panel props', 'right panel props'):
    patch(page,
'''                onEditPage={onEditPage}
                onError={setError}
''',
'''                onEditPage={onEditPage}
                onMovePage={onMovePage}
                onDeletePage={onDeletePage}
                onError={setError}
''',
label)

edit = root / 'frontend/src/inventory/inventory-page-edit.tsx'
t = edit.read_text(encoding='utf-8')
t = t.replace(
    "import { NumberInput, Text, TextInput } from '@mantine/core';",
    "import { Group, NumberInput, Text, TextInput } from '@mantine/core';"
)
t = t.replace(
    "import React from 'react';",
    "import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';\nimport React from 'react';"
)
t = t.replace(
    "import { UIFormCard } from '../ui/popover/popover-card/ui-form-card';",
    "import { useTranslate } from '../translate/i18n';\nimport { UIButton } from '../ui/form/button/ui-button';\nimport { UIFormCard } from '../ui/popover/popover-card/ui-form-card';"
)
old = '''    minSlotCount: number;
    onSubmit: (name: string, slotCount: number) => Promise<void>;
};
'''
new = '''    minSlotCount: number;
    canMoveLeft: boolean;
    canMoveRight: boolean;
    onMove: (direction: -1 | 1) => Promise<void>;
    onSubmit: (name: string, slotCount: number) => Promise<void>;
};
'''
if old not in t:
    raise RuntimeError('alpha53c InventoryPageEdit props anchor')
t = t.replace(old, new, 1)

old = '''    slotCount,
    minSlotCount,
    onSubmit: onSubmitRaw,
}) => {
    const popover = usePopover();
'''
new = '''    slotCount,
    minSlotCount,
    canMoveLeft,
    canMoveRight,
    onMove,
    onSubmit: onSubmitRaw,
}) => {
    const { t } = useTranslate();
    const popover = usePopover();
'''
if old not in t:
    raise RuntimeError('alpha53c InventoryPageEdit destructure anchor')
t = t.replace(old, new, 1)

old = '''        <Text size='xs' c='dimmed'>
            Item boxes use the same maximum size as normal PKVault Pokémon boxes.
        </Text>
'''
new = '''        <Group justify='space-between'>
            <UIButton
                name='inventory-box-order-left'
                controlLabel={t('storage.bank.edit.order.controls-label.1')}
                onClick={() => void onMove(-1)}
                disabled={!canMoveLeft}
            >
                <ChevronLeftIcon />
            </UIButton>
            {t('storage.bank.edit.order')}
            <UIButton
                name='inventory-box-order-right'
                controlLabel={t('storage.bank.edit.order.controls-label.2')}
                onClick={() => void onMove(1)}
                disabled={!canMoveRight}
            >
                <ChevronRightIcon />
            </UIButton>
        </Group>

        <Text size='xs' c='dimmed'>
            Item boxes use the same maximum size as normal PKVault Pokémon boxes.
        </Text>
'''
if old not in t:
    raise RuntimeError('alpha53c InventoryPageEdit body anchor')
edit.write_text(t.replace(old, new, 1), encoding='utf-8')

panel = 'frontend/src/inventory/inventory-panel.tsx'
patch(panel,
'''    onEditPage: (page: number, name: string, slotCount: number) => Promise<void>;
    onError: (message: string) => void;
''',
'''    onEditPage: (page: number, name: string, slotCount: number) => Promise<void>;
    onMovePage: (page: number, targetPage: number) => Promise<void>;
    onDeletePage: (page: number) => Promise<void>;
    onError: (message: string) => void;
''',
'panel props')

patch(panel,
'''    state, initial, onSplit, onTrash, onCreatePage, onEditPage, onError
''',
'''    state, initial, onSplit, onTrash, onCreatePage, onEditPage, onMovePage, onDeletePage, onError
''',
'panel destructure')

p = root / panel
t = p.read_text(encoding='utf-8')
old = '''                    editDropdown={itemPage && <InventoryPageEdit
                        page={itemPage.page}
                        name={itemPage.name}
                        slotCount={itemPage.slotCount}
                        minSlotCount={minSlotCount}
                        onSubmit={(name, slotCount) => onEditPage(itemPage.page, name, slotCount)}
                    />}
                    onSelect={() => {
'''
new = '''                    editDropdown={itemPage && <InventoryPageEdit
                        page={itemPage.page}
                        name={itemPage.name}
                        slotCount={itemPage.slotCount}
                        minSlotCount={minSlotCount}
                        canMoveLeft={itemPage.page > 1}
                        canMoveRight={itemPage.page < state.bankPages.length}
                        onMove={async direction => {
                            const fromPage = itemPage.page;
                            const targetPage = fromPage + direction;
                            await onMovePage(fromPage, targetPage);
                            setSelection(current => {
                                if (current.kind !== 'bank') return current;
                                let page = current.page;
                                if (page === fromPage) page = targetPage;
                                else if (fromPage < targetPage && page > fromPage && page <= targetPage) page--;
                                else if (fromPage > targetPage && page >= targetPage && page < fromPage) page++;
                                return { kind: 'bank', page };
                            });
                        }}
                        onSubmit={(name, slotCount) => onEditPage(itemPage.page, name, slotCount)}
                    />}
                    onDelete={state.bankPages.length > 1 && itemPage
                        ? async () => {
                            const deletedPage = itemPage.page;
                            await onDeletePage(deletedPage);
                            setSelection(current => current.kind === 'bank'
                                ? { kind: 'bank', page: current.page > deletedPage ? current.page - 1 : current.page }
                                : current);
                        }
                        : undefined}
                    onSelect={() => {
'''
if old not in t:
    raise RuntimeError('alpha53c expanded box anchor')
p.write_text(t.replace(old, new, 1), encoding='utf-8')

patch('frontend/src/storage/actions/hooks/use-action-description.ts',
'''            [ DataActionType.TRASH_ITEM ]: () =>
                'Trash ×' + parameters[ 1 ] + ' ' + parameters[ 0 ] + ' from PKVault Item Bank',
''',
'''            [ DataActionType.TRASH_ITEM ]: () =>
                'Trash ×' + parameters[ 1 ] + ' ' + parameters[ 0 ] + ' from PKVault Item Bank',
            [ DataActionType.MOVE_ITEM_PAGE ]: () =>
                'Move PKVault item box ' + parameters[ 0 ] + ' from position ' + parameters[ 1 ] + ' to ' + parameters[ 2 ],
            [ DataActionType.DELETE_ITEM_PAGE ]: () =>
                'Delete PKVault item box ' + parameters[ 0 ] + ' and trash ×' + parameters[ 2 ] + ' items',
''',
'action descriptions')

patch('frontend/src/storage/actions/action-label.tsx',
'''        [ DataActionType.TRASH_ITEM ]: ActionLabelMap.TrashItem,
''',
'''        [ DataActionType.TRASH_ITEM ]: ActionLabelMap.TrashItem,
        [ DataActionType.MOVE_ITEM_PAGE ]: ActionLabelMap.MoveItem,
        [ DataActionType.DELETE_ITEM_PAGE ]: ActionLabelMap.TrashItem,
''',
'action labels')

patch('frontend/src/ui/actions-panel/utils/get-action-color.ts',
'''        case DataActionType.CREATE_ITEM_PAGE:
            return 'gray';
''',
'''        case DataActionType.CREATE_ITEM_PAGE:
        case DataActionType.MOVE_ITEM_PAGE:
            return 'gray';
''',
'move page color')

patch('frontend/src/ui/actions-panel/utils/get-action-color.ts',
'''        case DataActionType.TRASH_ITEM:
        case DataActionType.MAIN_DELETE_BANK:
''',
'''        case DataActionType.TRASH_ITEM:
        case DataActionType.DELETE_ITEM_PAGE:
        case DataActionType.MAIN_DELETE_BANK:
''',
'delete page color')

checks = {
    'PKVault.Core/storage/services/ItemBankService.cs': [
        'MovePage(int page, int targetPage)',
        'DeletePage(int page)',
        'ReorderPageNumber',
    ],
    'frontend/src/inventory/inventory-panel.tsx': [
        'onMovePage',
        'onDeletePage',
        'canMoveLeft',
        'onDelete={state.bankPages.length > 1',
    ],
    'frontend/src/inventory/inventory-api.ts': [
        'moveInventoryPage',
        'deleteInventoryPage',
    ],
    'frontend/src/inventory/inventory-page-edit.tsx': [
        'inventory-box-order-left',
        'inventory-box-order-right',
    ],
}
for rel, needles in checks.items():
    body = (root / rel).read_text(encoding='utf-8')
    for needle in needles:
        assert needle in body, (rel, needle)

print('PASS alpha53c inventory box reorder/delete parity')
