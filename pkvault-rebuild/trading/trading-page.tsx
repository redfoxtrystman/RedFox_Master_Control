import { Alert, Badge, Button, Card, Divider, Group, Select, SimpleGrid, Stack, Text, TextInput, Title } from '@mantine/core';
import { ArrowLeftRightIcon, CircleCheckIcon, LinkIcon, ServerIcon, UnplugIcon } from 'lucide-react';
import React from 'react';
import { customInstance, type ResponseBack } from '../data/mutator/custom-instance';

type TradePokemon = {
    variantId?: string | null;
    peerName: string;
    nickname: string;
    species: number;
    level: number;
    generation: number;
    context: number;
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
    localOffer?: TradePokemon | null;
    remoteOffer?: TradePokemon | null;
    localReady: boolean;
    remoteReady: boolean;
    activeTransactionId?: string | null;
    lastError?: string | null;
};

type MainPkm = {
    id: string;
    nickname: string;
    species: number;
    level: number;
    generation: number;
    context: number;
    boxId: number;
    boxSlot: number;
    isMain: boolean;
    isEnabled: boolean;
    isExternal: boolean;
    canDelete: boolean;
};

const jsonHeaders = { 'Content-Type': 'application/json' };

async function api<T>(url: string, init?: RequestInit): Promise<T> {
    const result = await customInstance<ResponseBack<T>>(url, init);
    return result.data;
}

const PokemonLine: React.FC<{ title: string; pkm?: TradePokemon | null; ready?: boolean }> = ({ title, pkm, ready }) => (
    <Card withBorder p='md'>
        <Stack gap='xs'>
            <Group justify='space-between'>
                <Text fw={700}>{title}</Text>
                <Badge color={ready ? 'green' : 'gray'}>{ready ? 'Ready' : 'Not ready'}</Badge>
            </Group>
            {pkm
                ? <>
                    <Text size='lg' fw={700}>{pkm.nickname || 'Unnamed Pokémon'}</Text>
                    <Text size='sm'>Species #{pkm.species} · Lv.{pkm.level} · Gen {pkm.generation}</Text>
                    <Text size='xs' c='dimmed'>From {pkm.peerName} · {pkm.extension.toUpperCase()}</Text>
                  </>
                : <Text c='dimmed'>No Pokémon offered.</Text>}
        </Stack>
    </Card>
);

export const TradingPage: React.FC = () => {
    const [ state, setState ] = React.useState<TradeState>();
    const [ address, setAddress ] = React.useState('localhost:0000');
    const [ pkms, setPkms ] = React.useState<MainPkm[]>([]);
    const [ selectedId, setSelectedId ] = React.useState<string | null>(null);
    const [ busy, setBusy ] = React.useState(false);
    const [ error, setError ] = React.useState<string | null>(null);

    const refreshState = React.useCallback(async () => {
        try {
            const next = await api<TradeState>('/api/trading/state');
            setState(next);
            if (next.lastError)
                setError(next.lastError);
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, []);

    const refreshPkms = React.useCallback(async () => {
        try {
            const all = await api<MainPkm[]>('/api/storage/main/pkm-version');
            setPkms(all.filter(p => p.isMain && p.isEnabled && p.canDelete && !p.isExternal));
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, []);

    React.useEffect(() => {
        void refreshState();
        void refreshPkms();
        const timer = window.setInterval(() => void refreshState(), 500);
        const pkmTimer = window.setInterval(() => void refreshPkms(), 2500);
        return () => {
            window.clearInterval(timer);
            window.clearInterval(pkmTimer);
        };
    }, [ refreshState, refreshPkms ]);

    const act = async (fn: () => Promise<TradeState>) => {
        setBusy(true);
        setError(null);
        try {
            const next = await fn();
            setState(next);
            await refreshPkms();
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        } finally {
            setBusy(false);
        }
    };

    const options = pkms.map(p => ({
        value: p.id,
        label: `${p.nickname || 'Unnamed'} · Lv.${p.level} · #${p.species} · Box ${p.boxId} Slot ${p.boxSlot + 1}`,
    }));

    const canOffer = !!state?.connected && !!selectedId && !state.localReady && state.status !== 'Trading';
    const canReady = !!state?.connected && !!state.localOffer && state.status !== 'Trading';

    return <Stack p='lg' gap='md' maw={1050} mx='auto' w='100%'>
        <Group justify='space-between' align='center'>
            <div>
                <Title order={2}>PKVault Trading</Title>
                <Text c='dimmed'>Direct PKVault-to-PKVault trading. Main-vault Pokémon only in this first build.</Text>
            </div>
            <Badge size='lg' color={state?.status === 'Completed' ? 'green' : state?.status === 'Error' ? 'red' : state?.connected ? 'blue' : 'gray'}>
                {state?.status ?? 'Loading'}
            </Badge>
        </Group>

        {error && <Alert color='red' title='Trading error'>{error}</Alert>}

        <SimpleGrid cols={{ base: 1, md: 2 }}>
            <Card withBorder>
                <Stack>
                    <Group><ServerIcon size={20}/><Text fw={700}>Host</Text></Group>
                    <Text size='sm' c='dimmed'>
                        Local Test reserves PKVault's localhost alias. Normal Direct Host uses an OS-assigned random port.
                    </Text>
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
                        Share/connect to: <Text span fw={700} ff='monospace'>{state.hostAddress}</Text>
                        {state.listenPort && state.hostAddress === 'localhost:0000' && <Text span c='dimmed'> (internal port {state.listenPort})</Text>}
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
                <Stack gap={2}>
                    <Text fw={700}>Session</Text>
                    <Text size='sm'>This copy: {state?.profileName ?? '-'}</Text>
                    <Text size='sm'>Peer: {state?.peerName ?? '-'}</Text>
                </Stack>
                <Button
                    color='red'
                    variant='light'
                    leftSection={<UnplugIcon size={16}/>}
                    disabled={!state || (!state.connected && state.status !== 'Hosting' && state.status !== 'Error')}
                    onClick={() => void act(() => api('/api/trading/session', { method: 'DELETE' }))}
                >Disconnect</Button>
            </Group>
        </Card>

        <Divider label='Offer' />

        <Card withBorder>
            <Stack>
                <Select
                    searchable
                    label='Pokémon from this PKVault'
                    placeholder='Choose a Pokémon'
                    data={options}
                    value={selectedId}
                    onChange={setSelectedId}
                    disabled={!state?.connected || state.localReady || state.status === 'Trading'}
                />
                <Button
                    leftSection={<ArrowLeftRightIcon size={16}/>}
                    disabled={!canOffer}
                    loading={busy}
                    onClick={() => selectedId && void act(() => api('/api/trading/offer', {
                        method: 'PUT', headers: jsonHeaders, body: JSON.stringify({ pkmVariantId: selectedId }),
                    }))}
                >Offer Pokémon</Button>
            </Stack>
        </Card>

        <SimpleGrid cols={{ base: 1, md: 2 }}>
            <PokemonLine title='Your offer' pkm={state?.localOffer} ready={state?.localReady} />
            <PokemonLine title={state?.peerName ? `${state.peerName}'s offer` : 'Peer offer'} pkm={state?.remoteOffer} ready={state?.remoteReady} />
        </SimpleGrid>

        <Group justify='center'>
            <Button
                size='lg'
                color={state?.localReady ? 'yellow' : 'green'}
                leftSection={state?.localReady ? undefined : <CircleCheckIcon size={18}/>}
                disabled={!canReady}
                loading={busy}
                onClick={() => void act(() => api('/api/trading/ready', {
                    method: 'PUT', headers: jsonHeaders, body: JSON.stringify({ ready: !state?.localReady }),
                }))}
            >
                {state?.localReady ? 'Unready' : 'Ready to Trade'}
            </Button>
        </Group>

        {state?.status === 'Trading' && <Alert color='blue' title='Trade in progress'>
            Both copies are staging and committing the swap. Transaction {state.activeTransactionId ?? ''}.
        </Alert>}

        {state?.status === 'Completed' && <Alert color='green' title='Trade complete'>
            Both PKVault copies committed the swap successfully.
        </Alert>}
    </Stack>;
};
