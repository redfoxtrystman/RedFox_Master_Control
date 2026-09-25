from pathlib import Path

def put28(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ===========================================================================
# V8 alpha28: true Storage drag controls + Gen1 inventory + exact split UX.
# ===========================================================================

# ---------------------------------------------------------------------------
# Gen 1 inventory mapping.
# PKVault's normal static item map is derived from SaveFile.HeldItems.
# SAV1.HeldItems is intentionally empty because Gen1 Pokemon cannot hold items,
# but PlayerBag1 has a complete bag/PC inventory. Fall back to the actual bag
# item storage + generation-specific names when the held-item map is empty.
# ---------------------------------------------------------------------------
item_service28 = PKVAULT / "PKVault.Core/storage/services/ItemBankService.cs"

item_service28_text = item_service28.read_text(encoding="utf-8")
old_calls = "GetVersionMap(others, save.Version)"
call_count = item_service28_text.count(old_calls)
if call_count != 3:
    raise RuntimeError(f"alpha28 expected 3 GetVersionMap calls, found {call_count}")
item_service28_text = item_service28_text.replace(old_calls, "GetVersionMap(others, save.GetSave())")

old_map = '''    private static Dictionary<int, string> GetVersionMap(StaticOthersData others, GameVersion version)
    {
        return others.Items.VersionItems
            .FirstOrDefault(x => x.Versions.Contains((byte)version))
            ?.ComboItems
            ?? [];
    }
'''
new_map = '''    private static Dictionary<int, string> GetVersionMap(StaticOthersData others, SaveFile save)
    {
        var mapped = others.Items.VersionItems
            .FirstOrDefault(x => x.Versions.Contains((byte)save.Version))
            ?.ComboItems;

        if (mapped is { Count: > 0 })
            return mapped;

        // Generation 1 has no held items, so PKVault's normal static item map
        // is empty even though PlayerBag1 exposes the real bag and PC item
        // tables. Build the same canonical PokeAPI-style keys directly from
        // the save's inventory storage instead.
        var result = new Dictionary<int, string>();
        var itemNames = GameInfo.Strings.GetItemStrings(save.Context, save.Version);
        var bag = save.Inventory;

        foreach (var pouch in bag.Pouches)
        {
            foreach (var itemId in bag.Info.GetItems(pouch.Type))
            {
                if (itemId <= 0 || itemId >= itemNames.Length)
                    continue;

                var key = PokeApiFromPKHeX.GetPokeapiItemName(itemNames[itemId]);
                if (string.IsNullOrWhiteSpace(key) || key == "???")
                    continue;

                if (others.Items.Items.ContainsKey(key))
                    result[itemId] = key;
            }
        }

        return result;
    }
'''
if old_map not in item_service28_text:
    raise RuntimeError("alpha28 GetVersionMap method anchor missing")
item_service28.write_text(item_service28_text.replace(old_map, new_map, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# Inventory move provider: use the exact same MoveProvider machinery as
# Pokemon storage instead of browser HTML5 drag/drop.
# ---------------------------------------------------------------------------
put28("frontend/src/inventory/inventory-move-provider.tsx", r'''import React from 'react';
import type { MoveSource } from '../ui/interaction/move/state/move-state';
import { MoveProvider, type MoveProviderProps } from '../ui/interaction/move/context/move-provider';
import type { InventoryLocation, InventorySlot, InventoryState } from './types';

export type InventoryMoveContainer = Omit<InventoryLocation, 'slot'>;

const getContainerHash = (value: InventoryMoveContainer) =>
    [ value.kind, value.id, value.pouch ?? '' ].join('---');

const getContainerValue = (hash: string): InventoryMoveContainer => {
    const [ kind, id, pouch = '' ] = hash.split('---');

    return {
        kind: kind === 'save' ? 'save' : 'bank',
        id: id ?? '',
        pouch: pouch || undefined,
    };
};

export const inventoryContainerFns = {
    getContainerHash,
    getContainerValue,
};

const getSlot = (
    state: InventoryState,
    container: InventoryMoveContainer,
    slot: number,
): InventorySlot | undefined => {
    if (container.kind === 'bank') {
        return state.bankPages
            .find(page => String(page.page) === container.id)
            ?.slots.find(item => item.slot === slot);
    }

    return state.saves
        .find(save => String(save.saveId) === container.id)
        ?.pockets.find(pocket => pocket.pouch === container.pouch)
        ?.slots.find(item => item.slot === slot);
};

const getAllContainers = (state: InventoryState) => [
    ...state.bankPages.map(page => ({
        container: {
            kind: 'bank' as const,
            id: String(page.page),
        },
        slots: page.slots,
        protected: false,
    })),
    ...state.saves.flatMap(save => save.pockets.map(pocket => ({
        container: {
            kind: 'save' as const,
            id: String(save.saveId),
            pouch: pocket.pouch,
        },
        slots: pocket.slots,
        protected: pocket.protected,
    }))),
];

type InventoryMoveProviderProps = {
    state: InventoryState;
    onMove: (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => Promise<void>;
    onError: (message: string) => void;
    children: React.ReactNode;
};

export const InventoryMoveProvider: React.FC<InventoryMoveProviderProps> = ({
    state, onMove, onError, children
}) => {
    const stateRef = React.useRef(state);
    const onMoveRef = React.useRef(onMove);
    const onErrorRef = React.useRef(onError);

    stateRef.current = state;
    onMoveRef.current = onMove;
    onErrorRef.current = onError;

    const useFilterStartDragIds:
        MoveProviderProps<InventoryMoveContainer, never>[ 'useFilterStartDragIds' ] =
        (container, ids) => () => {
            const current = stateRef.current;
            const movable = ids.filter(id => {
                const slot = getSlot(current, container, Number(id));
                return !!slot?.itemKey && slot.count > 0 && slot.movable;
            });
            return new Set(movable);
        };

    const dragStartComputeSlotStates = React.useCallback((source: MoveSource<never>) => {
        const current = stateRef.current;
        const sourceContainer = getContainerValue(source.containerId);
        const sourceSlot = Number(source.sourceId);
        const sourceItem = getSlot(current, sourceContainer, sourceSlot);

        const items: Record<string, Record<string, {
            canDrop: boolean;
            helpText?: string;
        }>> = {};

        for (const target of getAllContainers(current)) {
            const hash = getContainerHash(target.container);
            items[hash] = {};

            for (const slot of target.slots) {
                const sameSlot =
                    hash === source.containerId
                    && slot.slot === sourceSlot;

                let canDrop =
                    !!sourceItem?.itemKey
                    && sourceItem.movable
                    && !target.protected
                    && !sameSlot;

                if (canDrop && slot.itemKey) {
                    const sameItem = slot.itemKey === sourceItem!.itemKey;
                    const bankSwap =
                        sourceContainer.kind === 'bank'
                        && target.container.kind === 'bank';

                    canDrop = sameItem || bankSwap;
                }

                items[hash][String(slot.slot)] = {
                    canDrop,
                    helpText: canDrop
                        ? slot.itemKey === sourceItem?.itemKey
                            ? 'Restack ' + sourceItem.name
                            : 'Move ' + sourceItem?.name
                        : 'Cannot move item here',
                };
            }
        }

        return {
            rootItems: {},
            items,
        };
    }, []);

    const getTargetAllPositions = React.useCallback(
        (source: MoveSource<never>, target: {
            targetContainer: InventoryMoveContainer;
            targetPosition: number;
        }) => ({
            [source.sourceId]: target.targetPosition,
        }),
        []
    );

    const onDrop = React.useCallback(async (
        source: MoveSource<never>,
        target: {
            targetContainer: InventoryMoveContainer;
            targetPosition: number;
        },
    ) => {
        const current = stateRef.current;
        const sourceContainer = getContainerValue(source.containerId);
        const sourceSlot = Number(source.sourceId);
        const sourceItem = getSlot(current, sourceContainer, sourceSlot);

        if (!sourceItem?.itemKey || sourceItem.count <= 0)
            return;

        try {
            await onMoveRef.current(
                {
                    ...sourceContainer,
                    slot: sourceSlot,
                },
                {
                    ...target.targetContainer,
                    slot: target.targetPosition,
                },
                Number(sourceItem.count),
            );
        } catch (error) {
            onErrorRef.current(error instanceof Error ? error.message : String(error));
        }
    }, []);

    return <MoveProvider<InventoryMoveContainer, never>
        {...inventoryContainerFns}
        moveContainerId='inventory-move-container'
        useFilterStartDragIds={useFilterStartDragIds}
        dragStartComputeSlotStates={dragStartComputeSlotStates}
        getTargetAllPositions={getTargetAllPositions}
        onDrop={onDrop}
    >
        {children}
    </MoveProvider>;
};
''')

# ---------------------------------------------------------------------------
# Inventory item slots now use PKVault's move hooks and controls directly.
# Empty slots use UIStorageItemPlaceholder verbatim, giving them the same
# hover/drop highlighting as Pokemon storage.
# Splitting is a separate click action with its own exact quantity.
# ---------------------------------------------------------------------------
put28("frontend/src/inventory/inventory-item.tsx", r'''import { Badge, Box, Button, Group, NumberInput, Popover, Stack, Text } from '@mantine/core';
import { useMergedRef } from '@mantine/hooks';
import { LockIcon, SplitIcon } from 'lucide-react';
import React from 'react';
import { ItemImg } from '../img/item-img';
import { WithControlsIcons } from '../ui/interaction/controls/icons/with-controls-icons';
import { getSelectControl } from '../ui/interaction/focus-controls/common-controls/select-controls';
import { useDragControls } from '../ui/interaction/focus-controls/common-controls/drag-controls';
import { useFocusControls } from '../ui/interaction/focus-controls/use-focus-controls';
import { DragRender } from '../ui/interaction/move/components/drag-render';
import { useDragSubmitting } from '../ui/interaction/move/hooks/use-drag-submitting';
import { useDragging } from '../ui/interaction/move/hooks/use-dragging';
import { useDroppable } from '../ui/interaction/move/hooks/use-droppable';
import { UIStorageItemBase } from '../ui/storage/storage-item/base/ui-storage-item-base';
import { UIStorageItemPlaceholder } from '../ui/storage/storage-item/placeholder/ui-storage-item-placeholder';
import { useCurrentPanel } from '../ui/storage/storage-content/context/ui-panel-context';
import { UISpeciesImgSkeleton } from '../ui/sprite-img/species-img/ui-species-img-skeleton';
import type { InventoryLocation, InventorySlot } from './types';
import type { InventoryMoveContainer } from './inventory-move-provider';

type InventoryItemProps = {
    slot: InventorySlot;
    location: InventoryLocation;
    isBank: boolean;
    nearestEmptySlot?: number;
    globalOrder: number;
    nodeId: string;
    onSplit: (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => Promise<void>;
    onError: (message: string) => void;
};

const ItemSprite: React.FC<{ slot: InventorySlot }> = ({ slot }) => <>
    <UISpeciesImgSkeleton visible={false} />

    {!!slot.itemKey && <Box
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
            item={slot.itemKey}
            version={slot.spriteVersion}
            sourceRealHeight={32}
            style={{
                '--sprite-item-size-multiplier':
                    'calc(var(--sprite-species-size-multiplier, 1) * 2.5)',
            } as React.CSSProperties}
        />
    </Box>}

    {slot.count > 0 && <Badge
        size='md'
        variant='filled'
        pos='absolute'
        right={4}
        bottom={4}
    >
        {slot.count}
    </Badge>}

    {slot.count > 0 && !slot.movable && <LockIcon
        size={17}
        style={{ position: 'absolute', left: 5, bottom: 5 }}
    />}
</>;

export const InventoryItem: React.FC<InventoryItemProps> = ({
    slot, location, isBank, nearestEmptySlot,
    globalOrder, nodeId, onSplit, onError
}) => {
    const panel = useCurrentPanel();
    const [ opened, setOpened ] = React.useState(false);
    const [ splitAmount, setSplitAmount ] = React.useState(1);

    const hasItem = !!slot.itemKey && slot.count > 0;
    const container: InventoryMoveContainer = {
        kind: location.kind,
        id: location.id,
        pouch: location.pouch,
    };

    if (!hasItem) {
        return <UIStorageItemPlaceholder
            nodeId={nodeId}
            container={container}
            slot={slot.slot}
            globalOrder={globalOrder}
        />;
    }

    const itemId = String(slot.slot);

    const dragging = useDragging(itemId, container);
    const draggingMove = dragging.useDrag();

    const droppable = useDroppable({
        targetContainer: container,
        targetPosition: slot.slot,
        targetId: itemId,
    });

    const submitting = useDragSubmitting(container, slot.slot, itemId);
    const disabled = !slot.movable || droppable.canDrop === false;
    const isDraggingState = dragging.isDragging || droppable.isDroppable;

    const dragControls = useDragControls({
        dragging,
        draggingMove,
        droppable,
        disabled: disabled || submitting,
    });

    const { focusProps, controlProps, controlIcons } = useFocusControls({
        scopeNodeId: nodeId,
        order: globalOrder,
        onFocus: ({ node }) => {
            dragging.focusNode(node);
            panel.normalizeCurrentPanel();
        },
        controls: [
            !isDraggingState && !disabled && !submitting && getSelectControl({
                label: slot.name ?? 'Item',
                action: () => setOpened(value => !value),
            }),
            ...dragControls,
        ],
    });

    const ref = useMergedRef(
        dragging.ref,
        focusProps.ref,
    );

    const split = async () => {
        if (!isBank || nearestEmptySlot === undefined)
            return;

        const amount = Math.max(1, Math.min(Number(slot.count) - 1, splitAmount));
        if (amount <= 0 || amount >= slot.count) {
            onError('Split amount must be smaller than the current stack.');
            return;
        }

        try {
            await onSplit(
                location,
                { ...location, slot: nearestEmptySlot },
                amount,
            );
            setOpened(false);
            setSplitAmount(1);
        } catch (error) {
            onError(error instanceof Error ? error.message : String(error));
        }
    };

    const itemButton = <WithControlsIcons
        placement='out'
        icons={controlIcons('open', 'drag', 'drop')}
    >
        <UIStorageItemBase
            label={droppable.helpText ?? <Group gap='xs'>
                <Text>{slot.name}</Text>
                <Badge variant='light'>×{slot.count}</Badge>
            </Group>}
            loading={submitting}
            disabled={disabled}
            {...focusProps}
            {...controlProps('open', 'drag', 'drop')}
            ref={ref}
        >
            <ItemSprite slot={slot} />
        </UIStorageItemBase>
    </WithControlsIcons>;

    return <>
        <Popover
            opened={opened}
            onChange={setOpened}
            position='bottom'
            withArrow
            shadow='md'
        >
            <Popover.Target>
                {itemButton}
            </Popover.Target>

            <Popover.Dropdown>
                <Stack gap='xs' w={230}>
                    <Text fw={600}>{slot.name}</Text>
                    <Text size='xs' c='dimmed'>
                        Stack: {slot.count}
                    </Text>

                    {isBank
                        ? <>
                            <Text size='xs'>
                                Amount to split into the nearest empty slot:
                            </Text>
                            <NumberInput
                                min={1}
                                max={Math.max(1, Number(slot.count) - 1)}
                                value={splitAmount}
                                onChange={value => setSplitAmount(Number(value) || 1)}
                            />
                            <Button
                                leftSection={<SplitIcon size={14} />}
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
                        : <Text size='xs' c='dimmed'>
                            Dragging moves the whole stack. Move it into a PKVault item box if you want to split it.
                        </Text>}
                </Stack>
            </Popover.Dropdown>
        </Popover>

        {dragging.isDragging && <DragRender elementRef={dragging.ref}>
            <UIStorageItemBase opacity={0.75}>
                <ItemSprite slot={slot} />
            </UIStorageItemBase>
        </DragRender>}
    </>;
};
''')

# ---------------------------------------------------------------------------
# Panel: drag movement no longer receives a custom callback. Only Split needs
# the direct move callback; drag/drop is handled by InventoryMoveProvider.
# ---------------------------------------------------------------------------
panel28 = PKVAULT / "frontend/src/inventory/inventory-panel.tsx"
panel28_text = panel28.read_text(encoding="utf-8")

panel28_text = panel28_text.replace(
'''    onMove: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onCreatePage: () => Promise<number>;
''',
'''    onSplit: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onCreatePage: () => Promise<number>;
''',
1)

panel28_text = panel28_text.replace(
'''    state, initial, onMove, onCreatePage, onError
''',
'''    state, initial, onSplit, onCreatePage, onError
''',
1)

old_item = '''                return <InventoryItem
                    key={slot.slot}
                    slot={slot}
                    location={location}
                    isBank={selection.kind === 'bank'}
                    nearestEmptySlot={selection.kind === 'bank' ? nearestEmpty(slot.slot) : undefined}
                    onMove={onMove}
                    onError={onError}
                />;
'''
new_item = '''                return <InventoryItem
                    key={slot.slot}
                    slot={slot}
                    location={location}
                    isBank={selection.kind === 'bank'}
                    nearestEmptySlot={selection.kind === 'bank' ? nearestEmpty(slot.slot) : undefined}
                    globalOrder={slot.slot}
                    nodeId={'inventory-item-' + location.kind + '-' + location.id + '-' + (location.pouch ?? '') + '-' + slot.slot}
                    onSplit={onSplit}
                    onError={onError}
                />;
'''
if old_item not in panel28_text:
    raise RuntimeError("alpha28 InventoryItem render anchor missing")
panel28.write_text(panel28_text.replace(old_item, new_item, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# Page: wrap the exact Storage content tree in InventoryMoveProvider.
# ---------------------------------------------------------------------------
page28 = PKVAULT / "frontend/src/inventory/inventory-page.tsx"
page28_text = page28.read_text(encoding="utf-8")

page28_text = page28_text.replace(
'''import { InventoryPanel } from './inventory-panel';
''',
'''import { InventoryPanel } from './inventory-panel';
import { InventoryMoveProvider } from './inventory-move-provider';
''',
1)

page28_text = page28_text.replace(
'''        <UIStorageContent
            id='inventory-move-container'
''',
'''        <InventoryMoveProvider
            state={state}
            onMove={onMove}
            onError={setError}
        >
        <UIStorageContent
            id='inventory-move-container'
''',
1)

page28_text = page28_text.replace(
'''                onMove={onMove}
                onCreatePage={onCreatePage}
''',
'''                onSplit={onMove}
                onCreatePage={onCreatePage}
''',
2)

page28_text = page28_text.replace(
'''        />
    </>;
});
''',
'''        />
        </InventoryMoveProvider>
    </>;
});
''',
1)

page28.write_text(page28_text, encoding="utf-8")

print("PKVault V8 alpha28 exact Storage drag controls + Gen1 items + exact split applied")
