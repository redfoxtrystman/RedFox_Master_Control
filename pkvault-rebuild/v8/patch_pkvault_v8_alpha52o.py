from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52o anchor not found: {label}")
    return text.replace(old, new, 1)

# ===========================================================================
# Inventory backend: expose exact per-pocket accepted item keys so the UI can
# block impossible drops before the move request is sent.
# ===========================================================================
item_path = root / "PKVault.Core/storage/services/ItemBankService.cs"
item = item_path.read_text(encoding="utf-8")

item = rep(
    item,
    """public record SaveInventoryPocketDTO(
    string Pouch,
    string Label,
    int SlotCount,
    bool Protected,
    List<InventorySlotDTO> Slots
);
""",
    """public record SaveInventoryPocketDTO(
    string Pouch,
    string Label,
    int SlotCount,
    bool Protected,
    List<string> AcceptedItemKeys,
    List<InventorySlotDTO> Slots
);
""",
    "accepted item keys DTO",
)

item = rep(
    item,
    """            foreach (var pouch in bag.Pouches.Where(x => x.Type != InventoryType.None))
            {
                var protectedPocket = IsProtectedPouch(pouch.Type);
                var slots = new List<InventorySlotDTO>(pouch.Items.Length);
""",
    """            foreach (var pouch in bag.Pouches.Where(x => x.Type != InventoryType.None))
            {
                var protectedPocket = IsProtectedPouch(pouch.Type);
                var acceptedItemKeys = protectedPocket
                    ? []
                    : map
                        .Where(pair => pair.Key > 0
                            && pair.Key <= ushort.MaxValue
                            && IsMovableItem(pouch.Type, pair.Value)
                            && pouch.CanContain((ushort)pair.Key))
                        .SelectMany(pair => new[] { pair.Value, CanonicalItemKey(pair.Value) })
                        .Where(key => !string.IsNullOrWhiteSpace(key))
                        .Distinct(StringComparer.Ordinal)
                        .OrderBy(key => key, StringComparer.Ordinal)
                        .ToList();
                var slots = new List<InventorySlotDTO>(pouch.Items.Length);
""",
    "regular accepted keys",
)

item = rep(
    item,
    """                pockets.Add(new(
                    Pouch: pouch.Type.ToString(),
                    Label: GetPouchLabel(pouch.Type),
                    SlotCount: pouch.Items.Length,
                    Protected: protectedPocket,
                    Slots: slots
                ));
""",
    """                pockets.Add(new(
                    Pouch: pouch.Type.ToString(),
                    Label: GetPouchLabel(pouch.Type),
                    SlotCount: pouch.Items.Length,
                    Protected: protectedPocket,
                    AcceptedItemKeys: acceptedItemKeys,
                    Slots: slots
                ));
""",
    "regular pocket DTO accepted keys",
)

item = rep(
    item,
    """        foreach (var pocket in essentials.InventoryPockets.OrderBy(p => p.PocketIndex))
        {
            var protectedPocket = IsProtectedEssentialsPocket(pocket.PocketIndex);
            var slotCount = Math.Max(30, pocket.Items.Count + 1);
""",
    """        foreach (var pocket in essentials.InventoryPockets.OrderBy(p => p.PocketIndex))
        {
            var protectedPocket = IsProtectedEssentialsPocket(pocket.PocketIndex);
            var acceptedItemKeys = protectedPocket
                ? []
                : EssentialsItemProfile.GetAll(essentials.ProfileId)
                    .Where(definition => definition.Pocket == pocket.PocketIndex)
                    .Select(definition => ResolveEssentialsItemKey(
                        others,
                        essentials.ProfileId,
                        definition.Id,
                        definition.Pocket
                    ))
                    .Concat(pocket.Items.Select(existing => ResolveEssentialsItemKey(
                        others,
                        essentials.ProfileId,
                        existing.ItemId,
                        pocket.PocketIndex
                    )))
                    .Where(key => !string.IsNullOrWhiteSpace(key))
                    .Distinct(StringComparer.Ordinal)
                    .OrderBy(key => key, StringComparer.Ordinal)
                    .ToList();
            var slotCount = Math.Max(30, pocket.Items.Count + 1);
""",
    "essentials accepted keys",
)

item = rep(
    item,
    """            pockets.Add(new(
                Pouch: $"essentials:{pocket.PocketIndex}",
                Label: pocket.Label,
                SlotCount: slotCount,
                Protected: protectedPocket,
                Slots: slots
            ));
""",
    """            pockets.Add(new(
                Pouch: $"essentials:{pocket.PocketIndex}",
                Label: pocket.Label,
                SlotCount: slotCount,
                Protected: protectedPocket,
                AcceptedItemKeys: acceptedItemKeys,
                Slots: slots
            ));
""",
    "essentials pocket DTO accepted keys",
)

# Shop transactions must never overwrite a newer live money-bank balance with an
# older committed balance. Force the user to save/undo the pending money move.
item = rep(
    item,
    """            var updatedCommittedMoney = checked(committedMoney + moneyDelta);
            var updatedLiveMoney = checked(liveMoney + moneyDelta);

            if (updatedCommittedMoney < 0)
""",
    """            if (liveMoney != committedMoney)
            {
                throw new InvalidOperationException(
                    $"The PKVault Pokédollar Bank has unsaved changes (live ₽{liveMoney:N0}, saved ₽{committedMoney:N0}). Save or undo the pending Pokédollar transfer before using the Shop."
                );
            }

            var updatedCommittedMoney = checked(committedMoney + moneyDelta);
            var updatedLiveMoney = checked(liveMoney + moneyDelta);

            if (updatedCommittedMoney < 0)
""",
    "shop live/committed money guard",
)

item = rep(
    item,
    """            var updatedCommitted = checked(committedMoney + moneyDelta);
            var updatedLive = checked(liveMoney + moneyDelta);

            if (updatedCommitted < 0)
""",
    """            if (liveMoney != committedMoney)
            {
                throw new InvalidOperationException(
                    $"The PKVault Pokédollar Bank has unsaved changes (live ₽{liveMoney:N0}, saved ₽{committedMoney:N0}). Save or undo the pending Pokédollar transfer first."
                );
            }

            var updatedCommitted = checked(committedMoney + moneyDelta);
            var updatedLive = checked(liveMoney + moneyDelta);

            if (updatedCommitted < 0)
""",
    "progression money guard",
)

# Money quest rewards must be committed, not only written to pkvault-session.db.
item = rep(
    item,
    """        var bank = await LoadMoneyBank();
        var updated = checked(bank + amount);
        if (updated > MaxMoneyBank)
            throw new InvalidOperationException("The PKVault Pokédollar Bank has no remaining capacity for this quest reward.");

        await SaveMoneyBank(updated);

        var value = string.Join('\\n', claimed.OrderBy(x => x, StringComparer.Ordinal));
""",
    """        await ApplyProgressionMoneyDelta(amount);

        var value = string.Join('\\n', claimed.OrderBy(x => x, StringComparer.Ordinal));
""",
    "persistent quest money reward",
)

item_path.write_text(item, encoding="utf-8")

# ===========================================================================
# Shop backend: compatibility is based on each currently loaded save/profile,
# not only the underlying PKHeX GameVersion enum.
# ===========================================================================
shop_path = root / "PKVault.Core/shop/ShopService.cs"
shop = shop_path.read_text(encoding="utf-8")

shop = rep(
    shop,
    """public record ShopItemDTO(
""",
    """public record ShopCompatibilityDTO(
    int Version,
    string? RomHackProfile
);

public record ShopItemDTO(
""",
    "ShopCompatibilityDTO",
)

shop = rep(
    shop,
    """    int SortOrder,
    List<int> CompatibleVersions,
    List<string> Aliases
);
""",
    """    int SortOrder,
    List<int> CompatibleVersions,
    List<ShopCompatibilityDTO> CompatibleGames,
    List<string> Aliases
);
""",
    "ShopItemDTO compatible games",
)

shop = rep(
    shop,
    """public record ShopStateDTO(
    long MoneyBank,
    long MoneyBankMax,
    List<int> LoadedVersions,
    List<ShopItemDTO> Items
);
""",
    """public record ShopStateDTO(
    long MoneyBank,
    long MoneyBankMax,
    bool MoneyBankPendingSave,
    List<int> LoadedVersions,
    List<ShopItemDTO> Items
);
""",
    "shop pending money state",
)

shop = rep(
    shop,
    """            var aliases = new HashSet<string>(price.Aliases, StringComparer.OrdinalIgnoreCase)
""",
    """            var compatibleGames = inventory.Saves
                .Where(save => save.Pockets.Any(pocket =>
                    pocket.AcceptedItemKeys.Any(key => Equivalent(key, price.Key))))
                .Select(save => new ShopCompatibilityDTO(
                    Version: (int)save.Version,
                    RomHackProfile: save.RomHackProfile
                ))
                .Distinct()
                .OrderBy(game => game.RomHackProfile ?? string.Empty, StringComparer.Ordinal)
                .ThenBy(game => game.Version)
                .ToList();

            var aliases = new HashSet<string>(price.Aliases, StringComparer.OrdinalIgnoreCase)
""",
    "build loaded compatible games",
)

shop = rep(
    shop,
    """                SortOrder: sortOrder,
                CompatibleVersions: compatible,
                Aliases: aliases.OrderBy(x => x, StringComparer.OrdinalIgnoreCase).ToList()
""",
    """                SortOrder: sortOrder,
                CompatibleVersions: compatible,
                CompatibleGames: compatibleGames,
                Aliases: aliases.OrderBy(x => x, StringComparer.OrdinalIgnoreCase).ToList()
""",
    "ShopItemDTO compatible games output",
)

shop = rep(
    shop,
    """        return new(
            MoneyBank: committed.MoneyBank,
            MoneyBankMax: inventory.MoneyBankMax,
            LoadedVersions: loadedVersions,
            Items: items
        );
""",
    """        return new(
            MoneyBank: inventory.MoneyBank,
            MoneyBankMax: inventory.MoneyBankMax,
            MoneyBankPendingSave: inventory.MoneyBank != committed.MoneyBank,
            LoadedVersions: loadedVersions,
            Items: items
        );
""",
    "shop live money display",
)

shop_path.write_text(shop, encoding="utf-8")

# JSON source generation for new DTO.
json_path = root / "PKVault.Core/router/RouteJsonContext.cs"
json = json_path.read_text(encoding="utf-8")
json = rep(
    json,
    """[JsonSerializable(typeof(ShopItemDTO))]
""",
    """[JsonSerializable(typeof(ShopItemDTO))]
[JsonSerializable(typeof(ShopCompatibilityDTO))]
""",
    "ShopCompatibilityDTO JSON context",
)
json_path.write_text(json, encoding="utf-8")

# ===========================================================================
# Inventory frontend: refuse incompatible drops before API call.
# ===========================================================================
types_path = root / "frontend/src/inventory/types.ts"
types = types_path.read_text(encoding="utf-8")
types = rep(
    types,
    """    slotCount: number;
    protected: boolean;
    slots: InventorySlot[];
};
""",
    """    slotCount: number;
    protected: boolean;
    acceptedItemKeys: string[];
    slots: InventorySlot[];
};
""",
    "frontend accepted item keys",
)
types_path.write_text(types, encoding="utf-8")

move_path = root / "frontend/src/inventory/inventory-move-provider.tsx"
move = move_path.read_text(encoding="utf-8")

move = rep(
    move,
    """        slots: page.slots,
        protected: false,
    })),
""",
    """        slots: page.slots,
        protected: false,
        acceptedItemKeys: null as string[] | null,
    })),
""",
    "bank container accepted keys",
)

move = rep(
    move,
    """        slots: pocket.slots,
        protected: pocket.protected,
    }))),
""",
    """        slots: pocket.slots,
        protected: pocket.protected,
        acceptedItemKeys: pocket.acceptedItemKeys,
    }))),
""",
    "save container accepted keys",
)

move = rep(
    move,
    """                if (canDrop && slot.itemKey) {
""",
    """                if (canDrop
                    && target.container.kind === 'save'
                    && sourceItem?.itemKey
                    && !target.acceptedItemKeys?.includes(sourceItem.itemKey))
                {
                    canDrop = false;
                }

                if (canDrop && slot.itemKey) {
""",
    "pre-drop compatibility validation",
)

move = rep(
    move,
    """                        : 'Cannot move item here',
""",
    """                        : target.container.kind === 'save'
                            && sourceItem?.itemKey
                            && !target.acceptedItemKeys?.includes(sourceItem.itemKey)
                            ? (sourceItem?.name ?? 'This item') + ' is not compatible with this game/pocket'
                            : 'Cannot move item here',
""",
    "incompatible drop help",
)

move_path.write_text(move, encoding="utf-8")

# ===========================================================================
# Shop frontend: display ROM hacks by their actual names and use real loaded
# compatibility instead of underlying Emerald enums.
# ===========================================================================
shop_types_path = root / "frontend/src/shop/types.ts"
st = shop_types_path.read_text(encoding="utf-8")
st = rep(
    st,
    """export type ShopItem = {
""",
    """export type ShopCompatibility = {
    version: number;
    romHackProfile?: string | null;
};

export type ShopItem = {
""",
    "frontend ShopCompatibility",
)

st = rep(
    st,
    """    sortOrder: number;
    compatibleVersions: number[];
    aliases: string[];
};
""",
    """    sortOrder: number;
    compatibleVersions: number[];
    compatibleGames: ShopCompatibility[];
    aliases: string[];
};
""",
    "frontend compatible games",
)

st = rep(
    st,
    """    moneyBank: number;
    moneyBankMax: number;
    loadedVersions: number[];
""",
    """    moneyBank: number;
    moneyBankMax: number;
    moneyBankPendingSave: boolean;
    loadedVersions: number[];
""",
    "frontend pending money state",
)
shop_types_path.write_text(st, encoding="utf-8")

page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = rep(
    page,
    """import { useStaticData } from '../hooks/use-static-data';
""",
    """import { useStaticData } from '../hooks/use-static-data';
import { getSaveDisplayName } from '../romhacks/get-save-display-name';
""",
    "save display name import",
)

old_badges_start = """const CompatibilityBadges: React.FC<{ item: ShopItem; loadedVersions: number[] }> = ({ item, loadedVersions }) => {
    const staticData = useStaticData();
    const versions = item.compatibleVersions
        .filter(version => loadedVersions.includes(version))
        .slice(0, 5);

    if (versions.length === 0)
        return null;

    return <Group gap={3} wrap='nowrap'>
        {versions.map(version => {
            try {
                const info = getGameInfos(version as GameVersion);
                const versionName = staticData.versions[version]?.name ?? ('Game ' + version);
                return <Tooltip key={version} label={'Compatible with ' + versionName}>
                    <Image src={info.img} w={16} h={16} fit='contain' />
                </Tooltip>;
            } catch {
                const versionName = staticData.versions[version]?.name ?? ('Game ' + version);
                return <Badge key={version} size='xs' variant='light'>{versionName}</Badge>;
            }
        })}
    </Group>;
};
"""
new_badges = """const CompatibilityBadges: React.FC<{ item: ShopItem }> = ({ item }) => {
    const staticData = useStaticData();
    const games = item.compatibleGames.slice(0, 5);

    if (games.length === 0)
        return null;

    return <Group gap={3} wrap='nowrap'>
        {games.map(game => {
            const defaultName = staticData.versions[game.version]?.name ?? ('Game ' + game.version);
            const displayName = getSaveDisplayName(defaultName, game.romHackProfile);
            const key = (game.romHackProfile ?? 'vanilla') + ':' + game.version;

            if (game.romHackProfile)
                return <Badge key={key} size='xs' variant='light'>{displayName}</Badge>;

            try {
                const info = getGameInfos(game.version as GameVersion);
                return <Tooltip key={key} label={'Compatible with ' + displayName}>
                    <Image src={info.img} w={16} h={16} fit='contain' />
                </Tooltip>;
            } catch {
                return <Badge key={key} size='xs' variant='light'>{displayName}</Badge>;
            }
        })}
    </Group>;
};
"""
page = rep(page, old_badges_start, new_badges, "ROM hack compatibility badges")

page = rep(
    page,
    """        compatibleVersions: [],
        aliases: [],
""",
    """        compatibleVersions: [],
        compatibleGames: [],
        aliases: [],
""",
    "category icon fallback compatible games",
)

page = rep(
    page,
    """    loadedVersions: number[];
    basketCount: number;
""",
    """    basketCount: number;
""",
    "CatalogRow remove loaded versions prop",
)

page = rep(
    page,
    """}> = ({ item, mode, loadedVersions, basketCount, rowHeight, onAdd }) => {
""",
    """}> = ({ item, mode, basketCount, rowHeight, onAdd }) => {
""",
    "CatalogRow remove loaded versions arg",
)

page = rep(
    page,
    """                    <CompatibilityBadges item={item} loadedVersions={loadedVersions} />
""",
    """                    <CompatibilityBadges item={item} />
""",
    "CatalogRow badges call",
)

page = rep(
    page,
    """        .filter(item => !compatibleOnly || item.compatibleVersions.some(version => state.loadedVersions.includes(version)))
""",
    """        .filter(item => !compatibleOnly || item.compatibleGames.length > 0)
""",
    "compatible filter loaded games",
)

page = rep(
    page,
    """                                    mode={mode}
                                    loadedVersions={state.loadedVersions}
                                    basketCount={basket[item.key] ?? 0}
""",
    """                                    mode={mode}
                                    basketCount={basket[item.key] ?? 0}
""",
    "CatalogRow remove loaded versions call",
)

# Give the user a visible reason Shop buy/sell is blocked when the live money
# bank differs from the saved/committed bank.
page = rep(
    page,
    """            {error && <Alert color='red'>{error}</Alert>}
""",
    """            {error && <Alert color='red'>{error}</Alert>}
            {state.moneyBankPendingSave && <Alert color='yellow'>
                Your PKVault Pokédollar Bank has unsaved transfer changes. Save or undo those money transfers before buying or selling so the Shop cannot overwrite the newer balance.
            </Alert>}
""",
    "pending money alert",
)

# Disable transaction button while the money bank has pending save changes.
page = page.replace(
    "disabled={basketLines.length === 0}",
    "disabled={basketLines.length === 0 || state.moneyBankPendingSave}",
)

page_path.write_text(page, encoding="utf-8")

print("PKVault V8 alpha52o incompatible-drop guard + ROM-hack shop identities + Pokédollar safety applied")
