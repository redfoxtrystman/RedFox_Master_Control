import { ArrowLeftRightIcon } from 'lucide-react';
import type React from 'react';
import { UIGameExpandedWrapper } from '../../../ui/storage/storage-panel/game-list/ui-game-expanded-wrapper';

type GameTradingExpandedProps = {
    label: string;
    imgSrc: string;
    selected?: boolean;
    disabled?: boolean;
    onSelect?: () => unknown;
};

export const GameTradingExpanded: React.FC<GameTradingExpandedProps> = ({
    label, imgSrc, selected, disabled, onSelect,
}) => <UIGameExpandedWrapper
    label={label}
    imgSrc={imgSrc}
    selected={selected}
    disabled={disabled}
    onSelect={onSelect}
    secondaryLine={<>Direct PKVault-to-PKVault trading</>}
    tertiaryLine={<><ArrowLeftRightIcon size={16} /> Up to 6 Pokémon per side</>}
    path='Direct IP / localhost:0000'
/>;
