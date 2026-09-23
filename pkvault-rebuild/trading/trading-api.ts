import { customInstance, type ResponseBack } from '../data/mutator/custom-instance';
import type { EntityContext } from '../data/sdk/model';

export type TradePokemon = {
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

export type TradeState = {
    status: string;
    isHost: boolean;
    connected: boolean;
    profileName: string;
    peerName?: string | null;
    hostAddress?: string | null;
    hostAddresses: string[];
    peerAddress?: string | null;
    listenPort?: number | null;
    localOffers: TradePokemon[];
    remoteOffers: TradePokemon[];
    localReady: boolean;
    remoteReady: boolean;
    activeTransactionId?: string | null;
    lastError?: string | null;
};

const jsonHeaders = { 'Content-Type': 'application/json' };

async function api<T>(url: string, init?: RequestInit): Promise<T> {
    const result = await customInstance<ResponseBack<T>>(url, init);
    return result.data;
}

export const tradingGetState = () => api<TradeState>('/api/trading/state');

export const tradingHost = (localTest: boolean) => api<TradeState>('/api/trading/host', {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({ localTest }),
});

export const tradingConnect = (address: string) => api<TradeState>('/api/trading/connect', {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({ address }),
});

export const tradingSetOffers = (pkmVariantIds: string[]) => api<TradeState>('/api/trading/offer', {
    method: 'PUT',
    headers: jsonHeaders,
    body: JSON.stringify({ pkmVariantIds }),
});

export const tradingSetReady = (ready: boolean) => api<TradeState>('/api/trading/ready', {
    method: 'PUT',
    headers: jsonHeaders,
    body: JSON.stringify({ ready }),
});

export const tradingDisconnect = () => api<TradeState>('/api/trading/session', {
    method: 'DELETE',
});
