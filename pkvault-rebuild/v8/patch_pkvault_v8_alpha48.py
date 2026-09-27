from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(rel, old, new):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"{path}: alpha48 anchor missing")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"patched {path}")

replace_once(
    "PKVault.Core/storage/services/ItemBankService.cs",
    """public record MoveInventoryItemActionInput(
    string SourceKind,
    string SourceId,
    string? SourcePouch,
    int SourceSlot,
    string TargetKind,
    string TargetId,
    string? TargetPouch,
    int TargetSlot,
    int Count
);
""",
    """public record MoveInventoryItemActionInput(
    string SourceKind,
    string SourceId,
    string? SourcePouch,
    int SourceSlot,
    string TargetKind,
    string TargetId,
    string? TargetPouch,
    int TargetSlot,
    int Count
);

public record TrashInventoryItemActionInput(
    string SourceKind,
    string SourceId,
    int SourceSlot
);
""",
)

replace_once(
    "PKVault.Core/storage/services/ItemBankService.cs",
    """    public async Task GrantQuestReward(string questId, string itemKey, long count)
""",
    """    public async Task<ItemBankMoveResult> Trash(TrashInventoryItemActionInput input)
    {
        if (!IsBank(input.SourceKind))
        {
            throw new InvalidOperationException(
                "Only PKVault Item Bank stacks can be trashed. Move the item into PKVault first."
            );
        }

        var page = ParseBankPage(input.SourceId);
        ValidateBankSlot(input.SourceSlot);

        var bank = await LoadBankState();
        var key = BankKey(page, input.SourceSlot);
        var stack = bank.GetValueOrDefault(key)
            ?? throw new InvalidOperationException(
                "The PKVault inventory stack no longer exists. Reloading inventory will remove the phantom slot."
            );

        var others = await staticDataService.GetStaticOthers();
        bank.Remove(key);
        await SaveBankState(bank);

        return new(
            ItemName: GetItemName(others, stack.ItemKey),
            MovedCount: checked((int)Math.Min(stack.Count, int.MaxValue)),
            SourceVersion: null,
            TargetVersion: null
        );
    }

    public async Task GrantQuestReward(string questId, string itemKey, long count)
""",
)

replace_once(
    "PKVault.Core/storage/services/ItemBankService.cs",
    """    private async Task<Dictionary<string, BankStack>> LoadBankState()
""",
    """    public async Task<bool> ReconcilePersistedBankFiles()
    {
        // The .item files are the human-editable persisted mirror of the item bank.
        // During a normal live session the DB remains authoritative so unsaved
        // drag/drop actions are not reverted. A fresh session/reload calls this
        // method once, allowing intentional external file deletion to remove stale
        // metadata instead of leaving an unmovable phantom inventory card.
        if (!Directory.Exists(InventoryRoot))
            return false;

        var hasPersistedMirror = Directory.EnumerateDirectories(InventoryRoot).Any()
            || Directory.EnumerateFiles(InventoryRoot, "*.item", SearchOption.AllDirectories).Any();

        if (!hasPersistedMirror)
            return false;

        var fromFiles = ReadBankFiles();
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK);
        var current = entity is null
            ? new Dictionary<string, BankStack>(StringComparer.Ordinal)
            : ParseMeta(entity.Value);

        static string Fingerprint(Dictionary<string, BankStack> bank)
            => string.Join("\\n", bank.Values
                .Where(x => x.Count > 0)
                .OrderBy(x => x.Page)
                .ThenBy(x => x.Slot)
                .Select(x => $"{x.Page}\t{x.Slot}\t{x.Id}\t{x.ItemKey}\t{x.Count}"));

        if (string.Equals(Fingerprint(current), Fingerprint(fromFiles), StringComparison.Ordinal))
            return false;

        await SaveBankState(fromFiles);
        return true;
    }

    private async Task<Dictionary<string, BankStack>> LoadBankState()
""",
)

replace_once(
    "PKVault.Core/db/services/SessionService.cs",
    """            await Task.WhenAll(
                ResetDbSession(flags),
                savesLoadersService.Setup(flags)
            );

            if (checkInitialActions)
""",
    """            await Task.WhenAll(
                ResetDbSession(flags),
                savesLoadersService.Setup(flags)
            );

            // Reconcile the persisted .item mirror only at fresh-session/reload
            // boundaries. Normal inventory reads keep the session DB authoritative
            // so undoable drag/drop changes are not reverted.
            using (var inventoryScope = sp.CreateScope())
            {
                var itemBankService = inventoryScope.ServiceProvider.GetRequiredService<ItemBankService>();
                if (await itemBankService.ReconcilePersistedBankFiles())
                    Log.Logger.Information("PKVault item bank reconciled from persisted .item files");
            }

            if (checkInitialActions)
""",
)

(root / "PKVault.Core/storage/data-action/TrashInventoryItemAction.cs").write_text(
"""namespace PKVault.Core;

public class TrashInventoryItemAction(ItemBankService itemBankService) : DataAction<TrashInventoryItemActionInput>
{
    protected override async Task<DataActionPayload> Execute(TrashInventoryItemActionInput input, DataUpdateFlags flags)
    {
        var result = await itemBankService.Trash(input);
        flags.SaveInfos = true;

        return new(
            type: DataActionType.TRASH_ITEM,
            parameters: [
                result.ItemName,
                result.MovedCount,
            ]
        );
    }
}
""",
    encoding="utf-8",
)

replace_once(
    "PKVault.Core/storage/data-action/DataAction.cs",
    """    MOVE_ITEM,
    CREATE_ITEM_PAGE,
""",
    """    MOVE_ITEM,
    CREATE_ITEM_PAGE,
    TRASH_ITEM,
""",
)

replace_once(
    "PKVault.Core/Program.cs",
    """        services.AddScoped<MoveInventoryItemAction>();
        services.AddScoped<MoveMoneyAction>();
""",
    """        services.AddScoped<MoveInventoryItemAction>();
        services.AddScoped<TrashInventoryItemAction>();
        services.AddScoped<MoveMoneyAction>();
""",
)

replace_once(
    "PKVault.Core/storage/services/ActionService.cs",
    """    public async Task<DataUpdateFlags> MoveMoney(
""",
    """    public async Task<DataUpdateFlags> TrashInventoryItem(
        string sourceKind, string sourceId, int sourceSlot
    )
    {
        using var scope = sp.CreateScope();

        return await AddAction(
            scope,
            (scope) => scope.ServiceProvider.GetRequiredService<TrashInventoryItemAction>(),
            new(sourceKind, sourceId, sourceSlot)
        );
    }

    public async Task<DataUpdateFlags> MoveMoney(
""",
)

replace_once(
    "PKVault.Core/storage/routes/StorageRoute.cs",
    """    [HttpPut("inventory/money/move")]
""",
    """    [HttpDelete("inventory/item")]
    public async Task<ItemInventoryStateDTO> TrashInventoryItem(
        string sourceKind,
        string sourceId,
        int sourceSlot
    )
    {
        await actionService.TrashInventoryItem(sourceKind, sourceId, sourceSlot);
        return await itemBankService.GetState();
    }

    [HttpPut("inventory/money/move")]
""",
)

replace_once(
    "frontend/src/inventory/inventory-api.ts",
    """export const moveMoney = async (
""",
    """export const trashInventory = async (source: InventoryLocation) => {
    if (source.kind !== 'bank')
        throw new Error('Only PKVault Item Bank stacks can be trashed.');

    const p = new URLSearchParams({
        sourceKind: source.kind,
        sourceId: source.id,
        sourceSlot: String(source.slot),
    });

    return (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/item?' + p.toString(),
        { method: 'DELETE' }
    )).data;
};

export const moveMoney = async (
""",
)

replace_once(
    "frontend/src/inventory/inventory-page.tsx",
    """import { createInventoryPage, loadInventory, moveInventory, moveMoney, resizeInventoryPage } from './inventory-api';
""",
    """import { createInventoryPage, loadInventory, moveInventory, moveMoney, resizeInventoryPage, trashInventory } from './inventory-api';
""",
)

replace_once(
    "frontend/src/inventory/inventory-page.tsx",
    """    React.useEffect(() => {
        void reload();
    }, [ reload ]);

    const onMove = React.useCallback(async (
""",
    """    React.useEffect(() => {
        void reload();
    }, [ reload ]);

    React.useEffect(() => {
        const onReloadAll = () => void reload();
        window.addEventListener('pkvault:reload-all', onReloadAll);
        return () => window.removeEventListener('pkvault:reload-all', onReloadAll);
    }, [ reload ]);

    const onMove = React.useCallback(async (
""",
)

replace_once(
    "frontend/src/inventory/inventory-page.tsx",
    """    const onMoveMoney = React.useCallback(async (
""",
    """    const onTrash = React.useCallback(async (source: InventoryLocation) => {
        try {
            setState(await trashInventory(source));
            setError(undefined);
            await queryClient.invalidateQueries();
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    const onMoveMoney = React.useCallback(async (
""",
)

page_path = root / "frontend/src/inventory/inventory-page.tsx"
page_text = page_path.read_text(encoding="utf-8")
needle = """                onSplit={onMove}
                onCreatePage={onCreatePage}
"""
if page_text.count(needle) != 2:
    raise RuntimeError(f"{page_path}: expected two inventory-panel anchors")
page_path.write_text(
    page_text.replace(
        needle,
        """                onSplit={onMove}
                onTrash={onTrash}
                onCreatePage={onCreatePage}
""",
    ),
    encoding="utf-8",
)
print(f"patched {page_path}")

replace_once(
    "frontend/src/inventory/inventory-panel.tsx",
    """    onSplit: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onCreatePage: () => Promise<number>;
""",
    """    onSplit: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onTrash: (source: InventoryLocation) => Promise<void>;
    onCreatePage: () => Promise<number>;
""",
)

replace_once(
    "frontend/src/inventory/inventory-panel.tsx",
    """    state, initial, onSplit, onCreatePage, onResizePage, onError
""",
    """    state, initial, onSplit, onTrash, onCreatePage, onResizePage, onError
""",
)

replace_once(
    "frontend/src/inventory/inventory-panel.tsx",
    """                    onSplit={onSplit}
                    onError={onError}
""",
    """                    onSplit={onSplit}
                    onTrash={onTrash}
                    onError={onError}
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """import { LockIcon, SplitIcon } from 'lucide-react';
""",
    """import { LockIcon, SplitIcon, Trash2Icon } from 'lucide-react';
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """    onSplit: (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => Promise<void>;
    onError: (message: string) => void;
""",
    """    onSplit: (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => Promise<void>;
    onTrash: (source: InventoryLocation) => Promise<void>;
    onError: (message: string) => void;
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """    onSplit,
    onError,
}) => {
""",
    """    onSplit,
    onTrash,
    onError,
}) => {
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """    const [ splitAmount, setSplitAmount ] = React.useState(1);
    const [ tab, setTab ] = React.useState<string | null>('stack');
""",
    """    const [ splitAmount, setSplitAmount ] = React.useState(1);
    const [ confirmTrash, setConfirmTrash ] = React.useState(false);
    const [ trashing, setTrashing ] = React.useState(false);
    const [ tab, setTab ] = React.useState<string | null>('stack');
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """    const itemButton = <WithControlsIcons
""",
    """    const trash = async () => {
        if (!isBank)
            return;

        try {
            setTrashing(true);
            await onTrash(location);
            setOpened(false);
            setConfirmTrash(false);
        } catch (error) {
            onError(error instanceof Error ? error.message : String(error));
        } finally {
            setTrashing(false);
        }
    };

    const itemButton = <WithControlsIcons
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """        <Popover
            opened={opened}
            onChange={setOpened}
""",
    """        <Popover
            opened={opened}
            onChange={value => {
                setOpened(value);
                if (!value)
                    setConfirmTrash(false);
            }}
""",
)

replace_once(
    "frontend/src/inventory/inventory-item.tsx",
    """                                    <Button
                                        leftSection={
                                            <SplitIcon size={14} />
                                        }
                                        disabled={
                                            nearestEmptySlot === undefined
                                            || slot.count <= 1
                                            || splitAmount <= 0
                                            || splitAmount >= slot.count
                                        }
                                        onClick={() => void split()}
                                    >
                                        Split
                                    </Button>
                                </>
""",
    """                                    <Button
                                        leftSection={
                                            <SplitIcon size={14} />
                                        }
                                        disabled={
                                            nearestEmptySlot === undefined
                                            || slot.count <= 1
                                            || splitAmount <= 0
                                            || splitAmount >= slot.count
                                        }
                                        onClick={() => void split()}
                                    >
                                        Split
                                    </Button>

                                    <Button
                                        color='red'
                                        variant={confirmTrash ? 'filled' : 'light'}
                                        leftSection={<Trash2Icon size={14} />}
                                        loading={trashing}
                                        onClick={() => {
                                            if (confirmTrash)
                                                void trash();
                                            else
                                                setConfirmTrash(true);
                                        }}
                                    >
                                        {confirmTrash
                                            ? 'Confirm trash ×' + slot.count
                                            : 'Trash stack'}
                                    </Button>

                                    {confirmTrash && <Text size='xs' c='red'>
                                        Removes the whole stack from PKVault. You can still undo this action before saving.
                                    </Text>}
                                </>
""",
)

replace_once(
    "frontend/src/header/header.tsx",
    """                    onClick={() => savesScanMutation.mutateAsync()}
""",
    """                    onClick={async () => {
                        await savesScanMutation.mutateAsync();
                        window.dispatchEvent(new Event('pkvault:reload-all'));
                    }}
""",
)

replace_once(
    "PKVault.Core/swagger.json",
    """          "MOVE_ITEM",
          "CREATE_ITEM_PAGE"
        ],
""",
    """          "MOVE_ITEM",
          "CREATE_ITEM_PAGE",
          "TRASH_ITEM"
        ],
""",
)

replace_once(
    "PKVault.Core/swagger.json",
    """          20,
          21
        ]
""",
    """          20,
          21,
          22
        ]
""",
)

replace_once(
    "frontend/src/storage/actions/hooks/use-action-description.ts",
    """            [ DataActionType.CREATE_ITEM_PAGE ]: () =>
                'Create PKVault item box ' + parameters[ 0 ],
""",
    """            [ DataActionType.CREATE_ITEM_PAGE ]: () =>
                'Create PKVault item box ' + parameters[ 0 ],
            [ DataActionType.TRASH_ITEM ]: () =>
                'Trash ×' + parameters[ 1 ] + ' ' + parameters[ 0 ] + ' from PKVault Item Bank',
""",
)

replace_once(
    "frontend/src/storage/actions/action-label.tsx",
    """    CreateItemPage: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='gray' size='xs' fz='sm'>
                <PlusCircleIcon />
            </ThemeIcon>
        </>;
    },
""",
    """    CreateItemPage: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='gray' size='xs' fz='sm'>
                <PlusCircleIcon />
            </ThemeIcon>
        </>;
    },
    TrashItem: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='red' size='xs' fz='sm'>
                <TrashIcon />
            </ThemeIcon>
        </>;
    },
""",
)

replace_once(
    "frontend/src/storage/actions/action-label.tsx",
    """        [ DataActionType.CREATE_ITEM_PAGE ]: ActionLabelMap.CreateItemPage,
""",
    """        [ DataActionType.CREATE_ITEM_PAGE ]: ActionLabelMap.CreateItemPage,
        [ DataActionType.TRASH_ITEM ]: ActionLabelMap.TrashItem,
""",
)

replace_once(
    "frontend/src/ui/actions-panel/utils/get-action-color.ts",
    """        case DataActionType.MAIN_DELETE_BANK:
""",
    """        case DataActionType.TRASH_ITEM:
        case DataActionType.MAIN_DELETE_BANK:
""",
)

print("PKVault V8 alpha48 inventory trash and phantom-item reconciliation applied")
