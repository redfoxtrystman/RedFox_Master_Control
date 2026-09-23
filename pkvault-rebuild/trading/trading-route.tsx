import { createFileRoute } from '@tanstack/react-router';
import { TradingPage } from '../pages/trading';

export const Route = createFileRoute('/trading')({
    component: TradingPage,
});
