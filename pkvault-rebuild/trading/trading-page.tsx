import {
    Alert, Badge, Button, Card, Divider, Group, SimpleGrid, Stack, Tabs, Text, TextInput, Title
} from '@mantine/core';
import { useQueryClient } from '@tanstack/react-query';
import { CircleCheckIcon, LinkIcon, ServerIcon, Trash2Icon, UnplugIcon } from 'lucide-react';
import React from 'react';
import { customInstance, type ResponseBack } from '../data/mutator/custom-instance';
import { EntityContext } from '../data/sdk/model';
import { SpeciesImg } from '../img/species-img';
import { UISpriteSizeWrapper } from '../ui/sprite-img/ui-sprite-size-wrapper';

type TradePokemon = {
    variantId?: string | null;
    peerName: string;
    nickname: string;
    species: number;
    form: number;
    gender: number;
    isShiny: boolean;
    isEgg: boolean;
    isShadow: boolean;
    level: number;
    generation: number;
    context: EntityContext;
    extension: string;
    payloadBase64: string;
    fingerprint: string;
};

type TradeState = {
    status: string;
    isHost: boolean;
    connected: boolean;
    profileName: string;
    peerName?: string | null;
    hostAddress?: string | null;
    listenPort?: number | null;
    localOffers: TradePokemon[];
    remoteOffers: TradePokemon[];
    localReady: boolean;
    remoteReady: boolean;
    activeTransactionId?: string | null;
    lastError?: string | null;
};

type MainPkm = {
    id: string;
    nickname: string;
    species: number;
    form: number;
    gender: number;
    isShiny: boolean;
    isEgg: boolean;
    isShadow: boolean;
    level: number;
    generation: number;
    context: EntityContext;
    boxId: number;
    boxSlot: number;
    isMain: boolean;
    isEnabled: boolean;
    isExternal: boolean;
    canDelete: boolean;
};

type StorageBox = {
    id: string;
    type: number;
    name: string;
    slotCount: number;
    order: number;
    bankId?: string | null;
};

const jsonHeaders = { 'Content-Type': 'application/json' };
const MAX_OFFERS = 5;
const dragMime = 'text/pkvault-trade-id';

async function api<T>(url: string, init?: RequestInit): Promise<T> {
    const result = await customInstance<ResponseBack<T>>(url, init);
    return result.data;
}

const Sprite: React.FC<{
    species: number;
    form: number;
    gender: number;
    isShiny: boolean;
    isEgg: boolean;
    isShadow: boolean;
    context: EntityContext;
}> = props => (
    <UISpriteSizeWrapper component='div' speciesSize='sm'>
        <SpeciesImg
            species={props.species}
            form={props.form}
            context={props.context}
            isFemale={props.gender === 1}
            isShiny={props.isShiny}
            isEgg={props.isEgg}
            isShadow={props.isShadow}
        />
    </UISpriteSizeWrapper>
);

const OfferSlot: React.FC<{
    index: number;
    offer?: TradePokemon;
    local?: boolean;
    disabled?: boolean;
    onDropId?: (index: number, id: string) => void;
    onRemove?: (index: number) => void;
}> = ({ index, offer, local, disabled, onDropId, onRemove }) => {
    return <Card
        withBorder
        p='xs'
        h={112}
        style={{
            borderStyle: offer ? 'solid' : 'dashed',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
        }}
        onDragOver={local && !disabled ? e => e.preventDefault() : undefined}
        onDrop={local && !disabled ? e => {
            e.preventDefault();
            const id = e.dataTransfer.getData(dragMime);
            if (id)
                onDropId?.(index, id);
        } : undefined}
    >
        {offer
            ? <Stack gap={1} align='center'>
                <Sprite
                    species={offer.species}
                    form={offer.form}
                    gender={offer.gender}
                    isShiny={offer.isShiny}
                    isEgg={offer.isEgg}
                    isShadow={offer.isShadow}
                    context={offer.context}
                />
                <Text size='xs' fw={700} lineClamp={1}>{offer.nickname || 'Unnamed'}</Text>
                <Text size='xs' c='dimmed'>Lv.{offer.level}</Text>
                {local && !disabled && <Button
                    variant='subtle'
                    color='red'
                    size='compact-xs'
                    leftSection={<Trash2Icon size={12}/>}
                    onClick={() => onRemove?.(index)}
                >Remove</Button>}
              </Stack>
            : <Stack gap={2} align='center'>
                <Text c='dimmed' fw={700}>Slot {index + 1}</Text>
                <Text size='xs' c='dimmed'>{local ? 'Drop Pokémon here' : 'Empty'}</Text>
              </Stack>}
    </Card>;
};

export const TradingPage: React.FC = () => {
    const queryClient = useQueryClient();
    const [ state, setState ] = React.useState<TradeState>();
    const [ address, setAddress ] = React.useState('localhost:0000');
    const [ pkms, setPkms ] = React.useState<MainPkm[]>([]);
    const [ boxes, setBoxes ] = React.useState<StorageBox[]>([]);
    const [ selectedBoxId, setSelectedBoxId ] = React.useState<string | null>(null);
    const [ busy, setBusy ] = React.useState(false);
    const [ error, setError ] = React.useState<string | null>(null);
    const lastStatusRef = React.useRef<string>();

    const refreshPkms = React.useCallback(async () => {
        try {
            const all = await api<MainPkm[]>('/api/storage/main/pkm-version');
            setPkms(all.filter(p => p.isMain && p.isEnabled && p.canDelete && !p.isExternal));
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, []);

    const refreshBoxes = React.useCallback(async () => {
        try {
            const all = await api<StorageBox[]>('/api/storage/box');
            const mainBoxes = all
                .filter(b => b.type === 0)
                .sort((a, b) => a.order - b.order);
            setBoxes(mainBoxes);
            setSelectedBoxId(old => old && mainBoxes.some(b => b.id === old)
                ? old
                : mainBoxes[0]?.id ?? null);
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, []);

    const refreshState = React.useCallback(async () => {
        try {
            const next = await api<TradeState>('/api/trading/state');
            const previous = lastStatusRef.current;
            lastStatusRef.current = next.status;
            setState(next);

            if (next.lastError)
                setError(next.lastError);

            // A trade persists a fresh session DB. Invalidate every cached data
            // query so Storage/Saves immediately reflect the committed trade.
            if (next.status === 'Completed' && previous !== 'Completed') {
                await queryClient.invalidateQueries();
                await refreshPkms();
                await refreshBoxes();
                await queryClient.refetchQueries({ type: 'active' });
            }
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, [ queryClient, refreshBoxes, refreshPkms ]);

    React.useEffect(() => {
        void refreshState();
        void refreshPkms();
        void refreshBoxes();

        const stateTimer = window.setInterval(() => void refreshState(), 400);
        const storageTimer = window.setInterval(() => {
            void refreshPkms();
            void refreshBoxes();
        }, 2500);

        return () => {
            window.clearInterval(stateTimer);
            window.clearInterval(storageTimer);
        };
    }, [ refreshBoxes, refreshPkms, refreshState ]);

    const act = async (fn: () => Promise<TradeState>) => {
        setBusy(true);
        setError(null);
        try {
            const next = await fn();
            setState(next);
            lastStatusRef.current = next.status;
            await refreshPkms();
            await refreshBoxes();
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        } finally {
            setBusy(false);
        }
    };

    const setOfferIds = React.useCallback(async (ids: string[]) => {
        await act(() => api('/api/trading/offer', {
            method: 'PUT',
            headers: jsonHeaders,
            body: JSON.stringify({ pkmVariantIds: ids }),
        }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [ state ]);

    const localOffers = state?.localOffers ?? [];
    const remoteOffers = state?.remoteOffers ?? [];
    const offeredIds = new Set(localOffers.map(o => o.variantId).filter((id): id is string => !!id));

    const dropIntoOffer = (index: number, id: string) => {
        if (!state?.connected || state.localReady || state.status === 'Trading')
            return;

        const current = localOffers.map(o => o.variantId).filter((v): v is string => !!v);
        const withoutDragged = current.filter(v => v !== id);

        if (index < withoutDragged.length)
            withoutDragged[index] = id;
        else
            withoutDragged.splice(Math.min(index, withoutDragged.length), 0, id);

        void setOfferIds(withoutDragged.slice(0, MAX_OFFERS));
    };

    const removeOffer = (index: number) => {
        const ids = localOffers
            .map(o => o.variantId)
            .filter((v): v is string => !!v)
            .filter((_, i) => i !== index);
        void setOfferIds(ids);
    };

    const selectedBox = boxes.find(b => b.id === selectedBoxId);
    const boxPkms = pkms.filter(p => String(p.boxId) === selectedBoxId);
    const bySlot = new Map(boxPkms.map(p => [ p.boxSlot, p ]));

    const tradeLocked = !!state?.localReady || state?.status === 'Trading';
    const canReady = !!state?.connected
        && state.status !== 'Trading'
        && (localOffers.length > 0 || remoteOffers.length > 0);

    return <Stack p='lg' gap='md' w='100%' maw={1400} mx='auto'>
        <Group justify='space-between' align='center'>
            <div>
                <Title order={2}>PKVault Trading</Title>
                <Text c='dimmed'>Drag up to five Pokémon into your offer. A trade may also be one-way.</Text>
            </div>
            <Badge
                size='lg'
                color={state?.status === 'Completed' ? 'green' : state?.status === 'Error' ? 'red' : state?.connected ? 'blue' : 'gray'}
            >{state?.status ?? 'Loading'}</Badge>
        </Group>

        {error && <Alert color='red' title='Trading error'>{error}</Alert>}

        <SimpleGrid cols={{ base: 1, md: 2 }}>
            <Card withBorder>
                <Stack>
                    <Group><ServerIcon size={20}/><Text fw={700}>Host</Text></Group>
                    <Group>
                        <Button
                            loading={busy}
                            onClick={() => void act(() => api('/api/trading/host', {
                                method: 'POST', headers: jsonHeaders, body: JSON.stringify({ localTest: true }),
                            }))}
                        >Host Local Test</Button>
                        <Button
                            variant='light'
                            loading={busy}
                            onClick={() => void act(() => api('/api/trading/host', {
                                method: 'POST', headers: jsonHeaders, body: JSON.stringify({ localTest: false }),
                            }))}
                        >Host Direct</Button>
                    </Group>
                    {state?.isHost && state.hostAddress && <Text>
                        Address: <Text span fw={700} ff='monospace'>{state.hostAddress}</Text>
                        {state.hostAddress === 'localhost:0000' && state.listenPort
                            ? <Text span c='dimmed'> (internal {state.listenPort})</Text>
                            : null}
                    </Text>}
                </Stack>
            </Card>

            <Card withBorder>
                <Stack>
                    <Group><LinkIcon size={20}/><Text fw={700}>Connect</Text></Group>
                    <TextInput
                        label='Address'
                        value={address}
                        onChange={e => setAddress(e.currentTarget.value)}
                        placeholder='localhost:0000 or 26.x.x.x:port'
                    />
                    <Button
                        loading={busy}
                        onClick={() => void act(() => api('/api/trading/connect', {
                            method: 'POST', headers: jsonHeaders, body: JSON.stringify({ address }),
                        }))}
                    >Connect</Button>
                </Stack>
            </Card>
        </SimpleGrid>

        <Card withBorder>
            <Group justify='space-between'>
                <Group gap='xl'>
                    <Text><b>This copy:</b> {state?.profileName ?? '-'}</Text>
                    <Text><b>Peer:</b> {state?.peerName ?? '-'}</Text>
                </Group>
                <Button
                    color='red'
                    variant='light'
                    leftSection={<UnplugIcon size={16}/>}
                    disabled={!state || (!state.connected && state.status !== 'Hosting' && state.status !== 'Error')}
                    onClick={() => void act(() => api('/api/trading/session', { method: 'DELETE' }))}
                >Cancel / Disconnect</Button>
            </Group>
        </Card>

        <Divider label='Trade Box' />

        <SimpleGrid cols={{ base: 1, lg: 2 }} spacing='md'>
            <Card withBorder p='md'>
                <Stack>
                    <Group justify='space-between'>
                        <Text fw={700}>Your PKVault</Text>
                        <Text size='sm' c='dimmed'>Drag a Pokémon to the right.</Text>
                    </Group>

                    <Tabs value={selectedBoxId} onChange={setSelectedBoxId}>
                        <Tabs.List>
                            {boxes.map(box => <Tabs.Tab key={box.id} value={box.id}>{box.name}</Tabs.Tab>)}
                        </Tabs.List>
                    </Tabs>

                    {selectedBox
                        ? <SimpleGrid cols={6} spacing='xs'>
                            {Array.from({ length: selectedBox.slotCount }, (_, slot) => {
                                const pkm = bySlot.get(slot);
                                const reserved = !!pkm && offeredIds.has(pkm.id);

                                return <Card
                                    key={slot}
                                    withBorder
                                    p={4}
                                    h={100}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        opacity: tradeLocked ? 0.75 : 1,
                                        background: reserved ? 'var(--mantine-color-dark-6)' : undefined,
                                    }}
                                >
                                    {pkm && !reserved
                                        ? <div
                                            draggable={!tradeLocked && !!state?.connected}
                                            onDragStart={e => {
                                                e.dataTransfer.effectAllowed = 'move';
                                                e.dataTransfer.setData(dragMime, pkm.id);
                                            }}
                                            onDoubleClick={() => {
                                                if (localOffers.length < MAX_OFFERS)
                                                    dropIntoOffer(localOffers.length, pkm.id);
                                            }}
                                            style={{ cursor: tradeLocked || !state?.connected ? 'default' : 'grab', width: '100%' }}
                                        >
                                            <Stack gap={0} align='center'>
                                                <Sprite
                                                    species={pkm.species}
                                                    form={pkm.form}
                                                    gender={pkm.gender}
                                                    isShiny={pkm.isShiny}
                                                    isEgg={pkm.isEgg}
                                                    isShadow={pkm.isShadow}
                                                    context={pkm.context}
                                                />
                                                <Text size='xs' fw={700} ta='center' lineClamp={1}>{pkm.nickname || 'Unnamed'}</Text>
                                                <Text size='xs' c='dimmed'>Lv.{pkm.level}</Text>
                                            </Stack>
                                          </div>
                                        : reserved
                                            ? <Stack gap={2} align='center'>
                                                <Text size='xs' fw={700}>Offered →</Text>
                                                <Text size='xs' c='dimmed'>Slot {slot + 1} reserved</Text>
                                              </Stack>
                                            : <Text size='xs' c='dimmed'>{slot + 1}</Text>}
                                </Card>;
                            })}
                          </SimpleGrid>
                        : <Text c='dimmed'>No PKVault boxes available.</Text>}
                </Stack>
            </Card>

            <Stack>
                <Card withBorder p='md'>
                    <Stack>
                        <Group justify='space-between'>
                            <Text fw={700}>Your offer ({localOffers.length}/{MAX_OFFERS})</Text>
                            <Button
                                size='compact-xs'
                                variant='light'
                                color='red'
                                disabled={tradeLocked || localOffers.length === 0}
                                onClick={() => void setOfferIds([])}
                            >Clear offer</Button>
                        </Group>
                        <SimpleGrid cols={5} spacing='xs'>
                            {Array.from({ length: MAX_OFFERS }, (_, i) => <OfferSlot
                                key={i}
                                index={i}
                                offer={localOffers[i]}
                                local
                                disabled={tradeLocked || !state?.connected}
                                onDropId={dropIntoOffer}
                                onRemove={removeOffer}
                            />)}
                        </SimpleGrid>
                    </Stack>
                </Card>

                <Card withBorder p='md'>
                    <Stack>
                        <Group justify='space-between'>
                            <Text fw={700}>{state?.peerName ? `${state.peerName}'s offer` : 'Peer offer'} ({remoteOffers.length}/{MAX_OFFERS})</Text>
                            <Badge color={state?.remoteReady ? 'green' : 'gray'}>
                                {state?.remoteReady ? 'Ready' : 'Not ready'}
                            </Badge>
                        </Group>
                        <SimpleGrid cols={5} spacing='xs'>
                            {Array.from({ length: MAX_OFFERS }, (_, i) => <OfferSlot
                                key={i}
                                index={i}
                                offer={remoteOffers[i]}
                            />)}
                        </SimpleGrid>
                    </Stack>
                </Card>
            </Stack>
        </SimpleGrid>

        <Group justify='center'>
            <Button
                size='lg'
                color={state?.localReady ? 'yellow' : 'green'}
                leftSection={state?.localReady ? undefined : <CircleCheckIcon size={18}/>}
                disabled={!canReady}
                loading={busy}
                onClick={() => void act(() => api('/api/trading/ready', {
                    method: 'PUT',
                    headers: jsonHeaders,
                    body: JSON.stringify({ ready: !state?.localReady }),
                }))}
            >{state?.localReady ? 'Unready' : 'Ready to Trade'}</Button>
        </Group>

        {state?.localReady && <Alert color='yellow' title='Offer locked'>
            Your reserved Pokémon remain in their original PKVault slots until both sides commit. Unready to change the offer.
        </Alert>}

        {state?.status === 'Trading' && <Alert color='blue' title='Trade in progress'>
            Both PKVault copies are staging and committing the full batch. Transaction {state.activeTransactionId ?? ''}.
        </Alert>}

        {state?.status === 'Completed' && <Alert color='green' title='Trade complete'>
            Storage data was refreshed automatically. You can make another offer without using Reload all data & saves.
        </Alert>}
    </Stack>;
};
