import React from "react";
import { withErrorCatcher } from "../../error/with-error-catcher";
import { Route } from "../../routes/pokedex";
import { UIPokedexItem } from '../../ui/pokedex/pokedex-item/ui-pokedex-item';
import type { DexProfile } from "./hooks/use-pokedex-items";

export type PokedexItemProps = {
  species: number;
  speciesName: string;
  isSeen: boolean;
  dexProfile?: DexProfile;
  children: React.ReactNode[];
};

export const PokedexItem: React.FC<PokedexItemProps> = withErrorCatcher("item", React.memo(({
  species,
  speciesName,
  isSeen,
  dexProfile,
  children,
}) => {
  const navigate = Route.useNavigate();

  const selected = Route.useSearch({
    select: (search) => search.selected === species && search.dexProfile === dexProfile,
  });

  const onClick = React.useMemo(() => isSeen
    ? () =>
      navigate({
        search: search => ({
          ...search,
          selected: selected ? undefined : species,
          dexProfile: selected ? undefined : dexProfile,
          selectedSaveId: undefined,
        }),
      })
    : undefined,
    [ navigate, isSeen, selected, species, dexProfile ],
  );

  return <UIPokedexItem
    id={`species-${dexProfile ?? 'national'}-${species}`}
    species={species}
    label={speciesName}
    selected={selected}
    onClick={onClick}
  >
    {children}
  </UIPokedexItem>;
}));
