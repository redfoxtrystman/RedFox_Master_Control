import {
    Alert, Badge, Button, Card, Group, SimpleGrid, Stack, Text, TextInput
} from '@mantine/core';
import { useQueryClient } from '@tanstack/react-query';
import { CircleCheckIcon, LinkIcon, ServerIcon, Trash2Icon, UnplugIcon } from 'lucide-react';
import React from 'react';
import { SpeciesImg } from '../img/species-img';
import { useDroppable } from '../ui/interaction/move/hooks/use-droppable';
import { UISpriteSizeWrapper } from '../ui/sprite-img/ui-sprite-size-wrapper';
import type { MoveContainerValue } from '../storage/move/move-container-fns';
import {
    tradingConnect, tradingDisconnect, tradingGetState, tradingHost,
    tradingSetOffers, tradingSetReady, type TradePokemon, type TradeState,
} from './trading-api';

const MAX_OFFERS = 6;

const TradeSprite: React.FC<{ pkm: TradePokemon }> = ({ pkm }) => <UISpriteSizeWrapper component='div' speciesSize='sm'>
    <SpeciesImg
        species={pkm.species}
        form={pkm.form}
        context={pkm.context}
        isFemale={pkm.gender === 1}
        isShiny={pkm.isShiny}
        isEgg={pkm.isEgg}
        isShadow={pkm.isShadow}
    />
</UISpriteSizeWrapper>;

const LocalOfferSlot: React.FC<{
    index: number;
    offer?: TradePokemon;
    locked: boolean;
    onRemove: (index: number) => void;
}> = ({ index, offer, locked, onRemove }) => {
    const droppable = useDroppable<MoveContainerValue>({
        targetContainer: { type: 'trade' },
        targetPosition: index,
        targetId: offer?.variantId ?? undefined,
    });

    const canReceive = droppable.isDroppable && droppable.canDrop !== false && !locked;

    return <Card
        withBorder
        p={4}
        h={116}
        ref={undefined}
        onPointerUp={!locked ? droppable.onPointerUp : undefined}
        onClick={!locked ? droppable.onClick : undefined}
        style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderStyle: offer ? 'solid' : 'dashed',
            outline: canReceive ? '2px solid var(--mantine-color-green-6)' : undefined,
            opacity: locked ? 0.78 : 1,
        }}
    >
        {offer
            ? <Stack gap={0} align='center'>
                <TradeSprite pkm={offer} />
                <Text size='xs' fw={700} lineClamp={1}>{offer.nickname || 'Unnamed'}</Text>
                <Text size='xs' c='dimmed'>Lv.{offer.level}</Text>
                {!locked && <Button
                    variant='subtle'
                    color='red'
                    size='compact-xs'
                    leftSection={<Trash2Icon size={12}/>}
                    onClick={(e) => {
                        e.stopPropagation();
                        onRemove(index);
                    }}
                >Remove</Button>}
            </Stack>
            : <Stack gap={2} align='center'>
                <Text fw={700} c={canReceive ? 'green' : 'dimmed'}>Trade {index + 1}</Text>
                <Text size='xs' c='dimmed'>Drop here</Text>
            </Stack>}
    </Card>;
};

const RemoteOfferSlot: React.FC<{ index: number; offer?: TradePokemon }> = ({ index, offer }) => <Card
    withBorder
    p={4}
    h={104}
    style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
>
    {offer
        ? <Stack gap={0} align='center'>
            <TradeSprite pkm={offer} />
            <Text size='xs' fw={700} lineClamp={1}>{offer.nickname || 'Unnamed'}</Text>
            <Text size='xs' c='dimmed'>Lv.{offer.level}</Text>
        </Stack>
        : <Text size='xs' c='dimmed'>Peer {index + 1}</Text>}
</Card>;

export const TradingStoragePanel: React.FC = () => {
    const queryClient = useQueryClient();
    const [ state, setState ] = React.useState<TradeState>();
    const [ address, setAddress ] = React.useState('localhost:0000');
    const [ busy, setBusy ] = React.useState(false);
    const [ error, setError ] = React.useState<string | null>(null);
    const previousStatus = React.useRef<string>();

    const refresh = React.useCallback(async () => {
        try {
            const next = await tradingGetState();
            const prev = previousStatus.current;
            previousStatus.current = next.status;
            setState(next);
            if (next.lastError)
                setError(next.lastError);

            if (next.status === 'Completed' && prev !== 'Completed') {
                await queryClient.invalidateQueries();
                await queryClient.refetchQueries({ type: 'active' });
            }
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, [ queryClient ]);

    React.useEffect(() => {
        void refresh();
        const timer = window.setInterval(() => void refresh(), 400);
        return () => window.clearInterval(timer);
    }, [ refresh ]);

    const act = async (fn: () => Promise<TradeState>) => {
        setBusy(true);
        setError(null);
        try {
            const next = await fn();
            setState(next);
            previousStatus.current = next.status;
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        } finally {
            setBusy(false);
        }
    };

    const localOffers = state?.localOffers ?? [];
    const remoteOffers = state?.remoteOffers ?? [];
    const locked = !!state?.localReady || state?.status === 'Trading';
    const canReady = !!state?.connected
        && state.status !== 'Trading'
        && (localOffers.length > 0 || remoteOffers.length > 0);

    const removeOffer = (index: number) => {
        const ids = localOffers
            .map(o => o.variantId)
            .filter((id): id is string => !!id)
            .filter((_, i) => i !== index);
        void act(() => tradingSetOffers(ids));
    };

    return <Stack gap='sm'>
        <Group justify='space-between'>
            <Stack gap={0}>
                <Text fw={700}>Trading</Text>
                <Text size='xs' c='dimmed'>Drag Pokémon from the other Storage pane into one of the six slots.</Text>
            </Stack>
            <Badge color={state?.status === 'Completed' ? 'green' : state?.status === 'Error' ? 'red' : state?.connected ? 'blue' : 'gray'}>
                {state?.status ?? 'Loading'}
            </Badge>
        </Group>

        {error && <Alert color='red' p='xs'>{error}</Alert>}

        {!state?.connected && state?.status !== 'Hosting'
            ? <Stack gap='xs'>
                <Group grow>
                    <Button
                        leftSection={<ServerIcon size={14}/>}
                        loading={busy}
                        onClick={() => void act(() => tradingHost(true))}
                    >Host Local</Button>
                    <Button
                        variant='light'
                        loading={busy}
                        onClick={() => void act(() => tradingHost(false))}
                    >Host Direct / VPN</Button>
                </Group>
                <Text size='xs' c='dimmed'>
                    For Radmin/Hamachi/LAN, host with Direct / VPN and send your partner the matching IP:port shown below.
                </Text>
                <TextInput
                    leftSection={<LinkIcon size={14}/>}
                    value={address}
                    onChange={e => setAddress(e.currentTarget.value)}
                    placeholder='localhost:0000 or 26.x.x.x:port'
                />
                <Button loading={busy} onClick={() => void act(() => tradingConnect(address))}>Connect</Button>
            </Stack>
            : <Card withBorder p='xs'>
                <Stack gap='xs'>
                    <Group justify='space-between' align='flex-start'>
                        <Stack gap={0}>
                            <Text size='sm'><b>You:</b> {state?.profileName ?? '-'}</Text>
                            <Text size='sm'><b>Peer:</b> {state?.peerName ?? (state?.status === 'Hosting' ? 'Waiting…' : '-')}</Text>
                            {state?.peerAddress && <Text size='xs' c='dimmed'>
                                Peer address: {state.peerAddress}
                            </Text>}
                        </Stack>
                        <Button
                            color='red'
                            variant='light'
                            size='compact-sm'
                            leftSection={<UnplugIcon size={14}/>}
                            onClick={() => void act(tradingDisconnect)}
                        >Cancel</Button>
                    </Group>

                    {state?.isHost && (state.hostAddresses?.length ?? 0) > 0 && <Stack gap={4}>
                        <Text size='xs' fw={700}>Connection addresses</Text>
                        {state.hostAddresses.map(host => <Group key={host} justify='space-between' gap='xs' wrap='nowrap'>
                            <Text size='xs' ff='monospace' style={{ overflowWrap: 'anywhere' }}>{host}</Text>
                            <Button
                                size='compact-xs'
                                variant='subtle'
                                onClick={() => void navigator.clipboard?.writeText(host)}
                            >Copy</Button>
                        </Group>)}
                        {state.hostAddresses.some(host => host.startsWith('26.')) && <Text size='xs' c='dimmed'>
                            The 26.x.x.x address is the likely Radmin VPN address. Your partner should paste that exact IP:port.
                        </Text>}
                        {!state.hostAddresses.some(host => host.startsWith('26.')) && state.hostAddress !== 'localhost:0000' && <Text size='xs' c='dimmed'>
                            If you are using Radmin/Hamachi and its VPN address is not listed, copy the VPN IPv4 from that app and add the port shown here: {state.listenPort ?? '-'}.
                        </Text>}
                    </Stack>}
                </Stack>
            </Card>}

        <Card withBorder p='xs'>
            <Stack gap='xs'>
                <Group justify='space-between'>
                    <Text fw={700}>Your offer ({localOffers.length}/{MAX_OFFERS})</Text>
                    <Group gap='xs'>
                        {!locked && localOffers.length > 0 && <Button
                            size='compact-xs'
                            variant='subtle'
                            color='red'
                            onClick={() => void act(() => tradingSetOffers([]))}
                        >Clear</Button>}
                        <Badge color={state?.localReady ? 'green' : 'gray'}>{state?.localReady ? 'Ready' : 'Not ready'}</Badge>
                    </Group>
                </Group>
                <SimpleGrid cols={3} spacing='xs'>
                    {Array.from({ length: MAX_OFFERS }, (_, i) => <LocalOfferSlot
                        key={i}
                        index={i}
                        offer={localOffers[i]}
                        locked={locked || !state?.connected}
                        onRemove={removeOffer}
                    />)}
                </SimpleGrid>
            </Stack>
        </Card>

        <Card withBorder p='xs'>
            <Stack gap='xs'>
                <Group justify='space-between'>
                    <Text fw={700}>{state?.peerName ? `${state.peerName}'s offer` : 'Peer offer'} ({remoteOffers.length}/{MAX_OFFERS})</Text>
                    <Badge color={state?.remoteReady ? 'green' : 'gray'}>{state?.remoteReady ? 'Ready' : 'Not ready'}</Badge>
                </Group>
                <SimpleGrid cols={3} spacing='xs'>
                    {Array.from({ length: MAX_OFFERS }, (_, i) => <RemoteOfferSlot key={i} index={i} offer={remoteOffers[i]} />)}
                </SimpleGrid>
            </Stack>
        </Card>

        <Button
            size='md'
            color={state?.localReady ? 'yellow' : 'green'}
            leftSection={state?.localReady ? undefined : <CircleCheckIcon size={16}/>}
            disabled={!canReady}
            loading={busy}
            onClick={() => void act(() => tradingSetReady(!state?.localReady))}
        >{state?.localReady ? 'Unready' : 'Ready to Trade'}</Button>

        {state?.status === 'Completed' && <Alert color='green' p='xs'>
            Trade complete. Storage refreshed automatically.
        </Alert>}
    </Stack>;
};
