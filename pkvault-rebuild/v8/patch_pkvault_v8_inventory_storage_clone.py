from pathlib import Path

def put27(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ===========================================================================
# V8 alpha27: make Inventory a true item sibling of Storage.
# ===========================================================================

# ---------------------------------------------------------------------------
# Backend route: PKVault's custom router only treats a query parameter as
# optional when ParameterInfo.HasDefaultValue is true. Nullable reference
# annotations alone do not count. Put optional pouch parameters at the end
# with explicit defaults so save->bank and bank->save no longer 400.
# ---------------------------------------------------------------------------
storage_route27 = PKVAULT / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(storage_route27,
'''    [HttpPut("inventory/move")]
    public async Task<ItemInventoryStateDTO> MoveInventoryItem(
        string sourceKind,
        string sourceId,
        string? sourcePouch,
        int sourceSlot,
        string targetKind,
        string targetId,
        string? targetPouch,
        int targetSlot,
        int count
    )
    {
        await actionService.MoveInventoryItem(
            sourceKind, sourceId, sourcePouch, sourceSlot,
            targetKind, targetId, targetPouch, targetSlot,
            count
        );

        return await itemBankService.GetState();
    }
''',
'''    [HttpPut("inventory/move")]
    public async Task<ItemInventoryStateDTO> MoveInventoryItem(
        string sourceKind,
        string sourceId,
        int sourceSlot,
        string targetKind,
        string targetId,
        int targetSlot,
        int count,
        string? sourcePouch = null,
        string? targetPouch = null
    )
    {
        await actionService.MoveInventoryItem(
            sourceKind, sourceId, sourcePouch, sourceSlot,
            targetKind, targetId, targetPouch, targetSlot,
            count
        );

        return await itemBankService.GetState();
    }
''')

# Frontend also always sends both pouch query keys. This protects older/custom
# router builds and makes the request shape deterministic.
inventory_api27 = PKVAULT / "frontend/src/inventory/inventory-api.ts"
replace_once(inventory_api27,
'''    const p = new URLSearchParams({
        sourceKind: source.kind,
        sourceId: source.id,
        sourceSlot: String(source.slot),
        targetKind: target.kind,
        targetId: target.id,
        targetSlot: String(target.slot),
        count: String(count),
    });

    if (source.pouch)
        p.set('sourcePouch', source.pouch);
    if (target.pouch)
        p.set('targetPouch', target.pouch);
''',
'''    const p = new URLSearchParams({
        sourceKind: source.kind,
        sourceId: source.id,
        sourcePouch: source.pouch ?? '',
        sourceSlot: String(source.slot),
        targetKind: target.kind,
        targetId: target.id,
        targetPouch: target.pouch ?? '',
        targetSlot: String(target.slot),
        count: String(count),
    });
''')

# ---------------------------------------------------------------------------
# Inventory item slot: use the exact invisible 96px species skeleton Storage
# uses for empty Pokémon slots. Put the item sprite on top. This means both
# occupied and empty item slots use the same geometry and scale variable as
# Storage instead of hand-sized custom buttons.
# ---------------------------------------------------------------------------
put27("frontend/src/inventory/inventory-item.tsx", r'''import { Badge, Box, Button, Group, NumberInput, Popover, Stack, Text } from '@mantine/core';
import { LockIcon, SplitIcon } from 'lucide-react';
import React from 'react';
import { ItemImg } from '../img/item-img';
import { UIStorageItemBase } from '../ui/storage/storage-item/base/ui-storage-item-base';
import { UISpeciesImgSkeleton } from '../ui/sprite-img/species-img/ui-species-img-skeleton';
import type { InventoryDragPayload, InventoryLocation, InventorySlot } from './types';

const dragMime = 'application/x-pkvault-inventory';

type InventoryItemProps = {
    slot: InventorySlot;
    location: InventoryLocation;
    isBank: boolean;
    nearestEmptySlot?: number;
    onMove: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onError: (message: string) => void;
};

export const InventoryItem: React.FC<InventoryItemProps> = ({
    slot, location, isBank, nearestEmptySlot, onMove, onError
}) => {
    const [ opened, setOpened ] = React.useState(false);
    const [ amount, setAmount ] = React.useState<number>(Math.max(1, Number(slot.count)));

    const hasItem = !!slot.itemKey && slot.count > 0;
    const canDrag = hasItem && slot.movable;
    const transferAmount = Math.max(1, Math.min(Number(slot.count), amount || Number(slot.count)));

    const split = async () => {
        if (!isBank || nearestEmptySlot === undefined || !hasItem)
            return;

        if (transferAmount >= slot.count) {
            onError('Split amount must be smaller than the current stack.');
            return;
        }

        await onMove(
            location,
            { ...location, slot: nearestEmptySlot },
            transferAmount
        );
        setOpened(false);
    };

    const onDragStart = (e: React.DragEvent) => {
        if (!canDrag || !slot.itemKey) {
            e.preventDefault();
            return;
        }

        const payload: InventoryDragPayload = {
            location,
            count: transferAmount,
            itemKey: slot.itemKey,
        };

        e.dataTransfer.setData(dragMime, JSON.stringify(payload));
        e.dataTransfer.effectAllowed = 'move';
    };

    const onDrop = async (e: React.DragEvent) => {
        e.preventDefault();

        const raw = e.dataTransfer.getData(dragMime);
        if (!raw)
            return;

        try {
            const payload = JSON.parse(raw) as InventoryDragPayload;
            await onMove(payload.location, location, payload.count);
        } catch (error) {
            onError(error instanceof Error ? error.message : String(error));
        }
    };

    const card = <UIStorageItemBase
        label={hasItem
            ? <Group gap='xs'>
                <Text>{slot.name}</Text>
                <Badge variant='light'>×{slot.count}</Badge>
            </Group>
            : undefined}
        draggable={canDrag}
        onDragStart={onDragStart}
        onDragOver={e => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        }}
        onDrop={onDrop}
        onClick={() => hasItem && setOpened(true)}
        style={{
            cursor: canDrag ? 'grab' : hasItem ? 'pointer' : 'default',
        }}
    >
        <UISpeciesImgSkeleton visible={false} />

        {hasItem && <Box
            pos='absolute'
            inset={0}
            display='flex'
            style={{
                alignItems: 'center',
                justifyContent: 'center',
                pointerEvents: 'none',
            }}
        >
            <ItemImg
                item={slot.itemKey!}
                version={slot.spriteVersion}
                sourceRealHeight={32}
                style={{
                    '--sprite-item-size-multiplier':
                        'calc(var(--sprite-species-size-multiplier, 1) * 2.5)',
                } as React.CSSProperties}
            />
        </Box>}

        {hasItem && <Badge
            size='md'
            variant='filled'
            pos='absolute'
            right={4}
            bottom={4}
        >
            {slot.count}
        </Badge>}

        {hasItem && !slot.movable && <LockIcon
            size={17}
            style={{ position: 'absolute', left: 5, bottom: 5 }}
        />}
    </UIStorageItemBase>;

    if (!hasItem)
        return card;

    return <Popover
        opened={opened}
        onChange={setOpened}
        position='bottom'
        withArrow
        shadow='md'
    >
        <Popover.Target>
            {card}
        </Popover.Target>

        <Popover.Dropdown>
            <Stack gap='xs' w={220}>
                <Text fw={600}>{slot.name}</Text>
                <Text size='xs' c='dimmed'>
                    Choose how many this stack will move when you drag it.
                </Text>

                <NumberInput
                    min={1}
                    max={Number(slot.count)}
                    value={transferAmount}
                    onChange={v => setAmount(Number(v) || 1)}
                />

                {isBank && <Button
                    size='xs'
                    variant='light'
                    leftSection={<SplitIcon size={14} />}
                    disabled={nearestEmptySlot === undefined || slot.count <= 1}
                    onClick={() => void split()}
                >
                    Split to nearest empty slot
                </Button>}

                {!isBank && <Text size='xs' c='dimmed'>
                    Game bags keep one stack per item. Drag a partial amount to another game or into PKVault to split it safely.
                </Text>}
            </Stack>
        </Popover.Dropdown>
    </Popover>;
};
''')

# ---------------------------------------------------------------------------
# Inventory panel body/footer: match StoragePanelItems and StoragePanelFooter.
# Same gap, same grid columns, same empty-box overlay, same footer shape.
# ---------------------------------------------------------------------------
inventory_panel27 = PKVAULT / "frontend/src/inventory/inventory-panel.tsx"

replace_once(inventory_panel27,
'''import { Alert, Group, Tabs, Text } from '@mantine/core';
''',
'''import { Alert, EmptyState, Group, Tabs, Text } from '@mantine/core';
''')

replace_once(inventory_panel27,
'''import React from 'react';
''',
'''import { PackageOpenIcon } from 'lucide-react';
import React from 'react';
''')

replace_once(inventory_panel27,
'''import { UIStoragePanel } from '../ui/storage/storage-panel/ui-storage-panel';
''',
'''import { UIStoragePanel } from '../ui/storage/storage-panel/ui-storage-panel';
import { UIStoragePanelFooter } from '../ui/storage/storage-panel/ui-storage-panel-footer';
''')

replace_once(inventory_panel27,
'''    const cols = getBoxColumns(slots.length) ?? 6;

    return <UIStoragePanel
''',
'''    const cols = getBoxColumns(slots.length) ?? 6;
    const occupiedCount = slots.filter(slot => !!slot.itemKey).length;
    const totalCount = selection.kind === 'bank'
        ? state.bankPages.reduce((sum, page) =>
            sum + page.slots.filter(slot => !!slot.itemKey).length, 0)
        : (selectedSave?.pockets ?? []).reduce((sum, pocket) =>
            sum + pocket.slots.filter(slot => !!slot.itemKey).length, 0);
    const emptyBox = occupiedCount === 0;

    return <UIStoragePanel
''')

replace_once(inventory_panel27,
'''        footer={selection.kind === 'save' && selectedPocket?.protected
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
''',
'''        footer={<>
            {selection.kind === 'save' && selectedPocket?.protected && <Alert color='yellow' py='xs'>
                {selectedPocket.label} is visible but protected from cross-game moves.
            </Alert>}

            <UIStoragePanelFooter
                boxSize={slots.length}
                pkmCount={occupiedCount}
                pkmTotalCount={totalCount}
            />
        </>}
    >
        <Group
            gap='sm'
            wrap='wrap'
            mx='auto'
            pos='relative'
            w='fit-content'
            style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(' + cols + ', 1fr)',
            }}
        >
''')

replace_once(inventory_panel27,
'''            })}
        </Group>
    </UIStoragePanel>;
};
''',
'''            })}

            {emptyBox && <EmptyState
                size='sm'
                icon={<PackageOpenIcon />}
                title='Box is empty'
                style={{
                    position: 'absolute',
                    left: '50%',
                    top: 'calc(var(--sprite-species-size-multiplier) * 240px)',
                    transform: 'translate(-50%,-50%)',
                    pointerEvents: 'none',
                }}
            />}
        </Group>
    </UIStoragePanel>;
};
''')

# ---------------------------------------------------------------------------
# Page shell: StoragePage returns UIStorageContent directly. Do the same here.
# The extra Box wrapper was why both grey cards stopped halfway down.
# ---------------------------------------------------------------------------
put27("frontend/src/inventory/inventory-page.tsx", r'''import { Alert } from '@mantine/core';
import { useQueryClient } from '@tanstack/react-query';
import { ArrowLeftRightIcon } from 'lucide-react';
import React from 'react';
import { withErrorCatcher } from '../error/with-error-catcher';
import { UIStorageContent } from '../ui/storage/storage-content/ui-storage-content';
import { UIStorageContentMiddle } from '../ui/storage/storage-content/middle/ui-storage-content-middle';
import { createInventoryPage, loadInventory, moveInventory } from './inventory-api';
import { InventoryPanel } from './inventory-panel';
import type { InventoryLocation, InventoryState } from './types';

export const InventoryPage: React.FC = withErrorCatcher('default', () => {
    const queryClient = useQueryClient();
    const [ state, setState ] = React.useState<InventoryState>();
    const [ error, setError ] = React.useState<string>();

    const reload = React.useCallback(async () => {
        try {
            setState(await loadInventory());
            setError(undefined);
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, []);

    React.useEffect(() => {
        void reload();
    }, [ reload ]);

    const onMove = React.useCallback(async (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => {
        try {
            setState(await moveInventory(source, target, count));
            setError(undefined);
            await queryClient.invalidateQueries();
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    const onCreatePage = React.useCallback(async () => {
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
        return error ? <Alert color='red'>{error}</Alert> : <>Loading inventory…</>;

    const firstSave = state.saves[0];

    return <>
        {error && <Alert
            color='red'
            pos='fixed'
            top={60}
            left='50%'
            maw='80vw'
            style={{
                transform: 'translateX(-50%)',
                zIndex: 1000,
            }}
            withCloseButton
            onClose={() => setError(undefined)}
        >
            {error}
        </Alert>}

        <UIStorageContent
            id='inventory-move-container'
            left={<InventoryPanel
                state={state}
                initial={{ kind: 'bank', page: 1 }}
                onMove={onMove}
                onCreatePage={onCreatePage}
                onError={setError}
            />}
            right={<InventoryPanel
                state={state}
                initial={firstSave
                    ? {
                        kind: 'save',
                        saveId: firstSave.saveId,
                        pouch: firstSave.pockets[0]?.pouch,
                    }
                    : { kind: 'bank', page: 1 }}
                onMove={onMove}
                onCreatePage={onCreatePage}
                onError={setError}
            />}
            middle={<UIStorageContentMiddle>
                <ArrowLeftRightIcon />
            </UIStorageContentMiddle>}
        />
    </>;
});
''')

print("PKVault V8 alpha27 true Storage-clone inventory shell applied")
