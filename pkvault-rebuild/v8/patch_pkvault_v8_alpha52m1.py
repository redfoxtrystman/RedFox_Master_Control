from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52m1 anchor not found: {label}")
    return text.replace(old, new, 1)

# ===========================================================================
# Gen-2 TM/HM pocket: TMs are transferable, HMs remain protected.
# ===========================================================================
item_path = root / "PKVault.Core/storage/services/ItemBankService.cs"
item = item_path.read_text(encoding="utf-8")

item = rep(item,
"""    private static bool IsProtectedPouch(InventoryType type) => type switch
    {
        InventoryType.KeyItems => true,
        InventoryType.TMHMs => true,
        InventoryType.ZCrystals => true,
        _ => false,
    };

    private static bool IsMovablePouch(InventoryType type)
        => type != InventoryType.None && !IsProtectedPouch(type);
""",
"""    private static bool IsProtectedPouch(InventoryType type) => type switch
    {
        InventoryType.KeyItems => true,
        InventoryType.ZCrystals => true,
        _ => false,
    };

    private static bool IsMovablePouch(InventoryType type)
        => type != InventoryType.None && !IsProtectedPouch(type);

    private static bool IsHmKey(string? itemKey)
    {
        if (string.IsNullOrWhiteSpace(itemKey))
            return false;

        var key = CanonicalItemKey(itemKey);
        return key.StartsWith("hm", StringComparison.Ordinal)
            && key.Length > 2
            && int.TryParse(key.AsSpan(2), out _);
    }

    private static bool IsMovableItem(InventoryType pouchType, string? itemKey)
        => IsMovablePouch(pouchType)
            && !(pouchType == InventoryType.TMHMs && IsHmKey(itemKey));
""",
"TM/HM pouch protection helpers")

item = rep(item,
"""                        Movable: !protectedPocket && mapped,
""",
"""                        Movable: mapped && IsMovableItem(pouch.Type, itemKey),
""",
"slot-specific TM movement")

item = rep(item,
"""        var provenanceKey = SaveProvenanceKey(save.Id, pouch.Type, itemKey);
""",
"""        if (!IsMovableItem(pouch.Type, itemKey))
            throw new InvalidOperationException(
                $"{GetItemName(others, itemKey)} is protected and cannot be moved."
            );

        var provenanceKey = SaveProvenanceKey(save.Id, pouch.Type, itemKey);
""",
"source HM guard")

item = rep(item,
"""        var requested = Math.Min(sourceItem.Count, input.Count);
""",
"""        if (!IsMovableItem(pouch.Type, itemKey))
            throw new InvalidOperationException(
                $"{GetItemName(others, itemKey)} is protected and cannot be moved."
            );

        var requested = Math.Min(sourceItem.Count, input.Count);
""",
"same-pouch HM guard")

item = rep(item,
"""        var targetItemId = (ushort)targetPair.Key;

        if (!pouch.CanContain(targetItemId))
""",
"""        var targetItemId = (ushort)targetPair.Key;

        if (!IsMovableItem(pouch.Type, source.ItemKey))
            throw new InvalidOperationException(
                $"{source.ItemName} is protected and cannot be transferred into {GetPouchLabel(pouch.Type)}."
            );

        if (!pouch.CanContain(targetItemId))
""",
"target HM guard")

item_path.write_text(item, encoding="utf-8")

# ===========================================================================
# Shop: generation-gated catalog + permanent discovered-TM unlocks.
# ===========================================================================
shop_path = root / "PKVault.Core/shop/ShopService.cs"
shop = shop_path.read_text(encoding="utf-8")

shop = rep(shop,
"""public class ShopService(
    ItemBankService itemBankService,
    StaticDataService staticDataService
)
""",
"""public class ShopService(
    ItemBankService itemBankService,
    StaticDataService staticDataService,
    ProgressionFileStore progressionStore
)
""",
"ShopService progression store")

shop = rep(shop,
"""        new("repel", "Utilities", 350, 175),
        new("super-repel", "Utilities", 500, 250),
        new("max-repel", "Utilities", 700, 350),
        new("escape-rope", "Utilities", 550, 275),
        new("rare-candy", "Utilities", 5000, 2500),
        new("pp-up", "Utilities", 9800, 4900),
""",
"""        new("repel", "Utilities", 350, 175),
        new("super-repel", "Utilities", 500, 250),
        new("max-repel", "Utilities", 700, 350),
        new("escape-rope", "Utilities", 550, 275),
        new("poke-doll", "Utilities", 1000, 500),
        new("rage-candy-bar", "Utilities", 300, 150),
        new("rare-candy", "Utilities", 5000, 2500),
        new("pp-up", "Utilities", 9800, 4900),
""",
"Gen1/2 utilities")

shop = rep(shop,
"""        new("oran-berry", "Berries", 80, 40),
""",
"""        // Generation II berry names remain distinct from their Gen III+
        // replacements so a Red/Silver profile does not expose future berries.
        new("berry", "Berries", 80, 40),
        new("gold-berry", "Berries", 200, 100),
        new("przcure-berry", "Berries", 80, 40),
        new("psncure-berry", "Berries", 80, 40),
        new("bitter-berry", "Berries", 80, 40),
        new("burnt-berry", "Berries", 80, 40),
        new("ice-berry", "Berries", 80, 40),
        new("mint-berry", "Berries", 80, 40),
        new("miracle-berry", "Berries", 200, 100),
        new("mystery-berry", "Berries", 80, 40),

        new("oran-berry", "Berries", 80, 40),
""",
"Gen2 berries")

# Replace fixed price map with dynamic catalog validation.
shop = rep(shop,
"""    private static readonly Dictionary<string, ShopPrice> PriceByKey = Prices
        .ToDictionary(x => x.Key, StringComparer.Ordinal);

    public async Task<ShopStateDTO> GetState()
""",
"""    private const string TmUnlockProgressionKey = "shop.tm.unlocks";

    public async Task<ShopStateDTO> GetState()
""",
"dynamic catalog header")

shop = rep(shop,
"""        var loadedVersions = inventory.Saves
            .Select(x => (int)x.Version)
            .Distinct()
            .OrderBy(x => x)
            .ToList();

        long BankCount(string key) => committed.BankCounts.GetValueOrDefault(Canonical(key));
""",
"""        var loadedVersions = inventory.Saves
            .Select(x => (int)x.Version)
            .Distinct()
            .OrderBy(x => x)
            .ToList();
        var catalog = await BuildCatalog(inventory);

        long BankCount(string key) => committed.BankCounts.GetValueOrDefault(Canonical(key));
""",
"build generation catalog")

shop = rep(shop,
"""        var items = Prices.Select((price, sortOrder) =>
""",
"""        var items = catalog.Select((price, sortOrder) =>
""",
"catalog select")

shop = rep(shop,
"""    public async Task<ShopStateDTO> Buy(ShopTransactionRequestDTO request)
    {
        var lines = NormalizeLines(request, buy: true);
        var cost = checked(lines.Sum(line => checked(PriceByKey[line.ItemKey].Buy * line.Count)));
        var deltas = lines.Select(x => new ShopBankDelta(x.ItemKey, x.Count)).ToList();
        await itemBankService.ApplyShopTransaction(deltas, moneyDelta: -cost, owner: "PKVault Shop purchase");
        return await GetState();
    }

    public async Task<ShopStateDTO> Sell(ShopTransactionRequestDTO request)
    {
        var lines = NormalizeLines(request, buy: false);
        var proceeds = checked(lines.Sum(line => checked(PriceByKey[line.ItemKey].Sell * line.Count)));
        var deltas = lines.Select(x => new ShopBankDelta(x.ItemKey, -x.Count)).ToList();
        await itemBankService.ApplyShopTransaction(deltas, moneyDelta: proceeds, owner: "PKVault Shop sale");
        return await GetState();
    }

    private static List<ShopTransactionLineDTO> NormalizeLines(
        ShopTransactionRequestDTO request,
        bool buy
    )
""",
"""    public async Task<ShopStateDTO> Buy(ShopTransactionRequestDTO request)
    {
        var inventory = await itemBankService.GetState();
        var priceMap = (await BuildCatalog(inventory))
            .ToDictionary(x => x.Key, StringComparer.Ordinal);
        var lines = NormalizeLines(request, buy: true, priceMap);
        var cost = checked(lines.Sum(line => checked(priceMap[line.ItemKey].Buy * line.Count)));
        var deltas = lines.Select(x => new ShopBankDelta(x.ItemKey, x.Count)).ToList();
        await itemBankService.ApplyShopTransaction(deltas, moneyDelta: -cost, owner: "PKVault Shop purchase");
        return await GetState();
    }

    public async Task<ShopStateDTO> Sell(ShopTransactionRequestDTO request)
    {
        var inventory = await itemBankService.GetState();
        var priceMap = (await BuildCatalog(inventory))
            .ToDictionary(x => x.Key, StringComparer.Ordinal);
        var lines = NormalizeLines(request, buy: false, priceMap);
        var proceeds = checked(lines.Sum(line => checked(priceMap[line.ItemKey].Sell * line.Count)));
        var deltas = lines.Select(x => new ShopBankDelta(x.ItemKey, -x.Count)).ToList();
        await itemBankService.ApplyShopTransaction(deltas, moneyDelta: proceeds, owner: "PKVault Shop sale");
        return await GetState();
    }

    private static List<ShopTransactionLineDTO> NormalizeLines(
        ShopTransactionRequestDTO request,
        bool buy,
        IReadOnlyDictionary<string, ShopPrice> priceMap
    )
""",
"dynamic transaction validation")

shop = shop.replace("if (!PriceByKey.TryGetValue(line.ItemKey, out var price))", "if (!priceMap.TryGetValue(line.ItemKey, out var price))")

insert_anchor = """    private static string Humanize(string key)
        => CultureInfo.InvariantCulture.TextInfo.ToTitleCase(key.Replace('-', ' '));
"""
insert = """    private async Task<List<ShopPrice>> BuildCatalog(ItemInventoryStateDTO inventory)
    {
        var maxGeneration = inventory.Saves
            .Select(x => (int)x.Version.Generation)
            .DefaultIfEmpty(1)
            .Max();

        var catalog = Prices
            .Where(price => GetMinimumGeneration(price.Key) <= maxGeneration)
            .ToList();

        var unlockedTms = await LoadAndUpdateTmUnlocks(inventory);
        foreach (var tm in unlockedTms
            .Where(tm => GetMinimumGeneration(tm) <= maxGeneration)
            .OrderBy(GetTmNumber)
            .ThenBy(x => x, StringComparer.Ordinal))
        {
            if (catalog.Any(price => string.Equals(price.Key, tm, StringComparison.Ordinal)))
                continue;

            // PKVault uses a single cross-save TM item key. Discovery controls
            // availability; compatibility still controls which saves can receive it.
            catalog.Add(new(tm, "TMs", 3000, 1500, true, true));
        }

        return catalog;
    }

    private async Task<HashSet<string>> LoadAndUpdateTmUnlocks(ItemInventoryStateDTO inventory)
    {
        var persisted = await progressionStore.Get(TmUnlockProgressionKey);
        var unlocked = new HashSet<string>(
            (persisted ?? string.Empty)
                .Split('\\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                .Select(Canonical)
                .Where(IsTmKey),
            StringComparer.Ordinal
        );

        var before = unlocked.Count;

        foreach (var key in inventory.BankPages
            .SelectMany(page => page.Slots)
            .Concat(inventory.Saves.SelectMany(save => save.Pockets).SelectMany(pocket => pocket.Slots))
            .Select(slot => slot.ItemKey)
            .Where(key => !string.IsNullOrWhiteSpace(key))
            .Select(key => Canonical(key!))
            .Where(IsTmKey))
        {
            unlocked.Add(key);
        }

        if (unlocked.Count != before)
        {
            await progressionStore.Set(
                TmUnlockProgressionKey,
                string.Join('\\n', unlocked.OrderBy(GetTmNumber).ThenBy(x => x, StringComparer.Ordinal))
            );
        }

        return unlocked;
    }

    private static bool IsTmKey(string key)
    {
        key = Canonical(key);
        return key.StartsWith("tm", StringComparison.Ordinal)
            && key.Length > 2
            && int.TryParse(key.AsSpan(2), out var number)
            && number >= 0;
    }

    private static int GetTmNumber(string key)
        => int.TryParse(Canonical(key).AsSpan(2), out var number) ? number : int.MaxValue;

    private static int GetMinimumGeneration(string key)
    {
        key = Canonical(key);

        if (IsTmKey(key))
        {
            var number = GetTmNumber(key);
            if (number == 0) return 8;
            if (number <= 50) return 1;
            if (number <= 92) return 4;
            if (number <= 95) return 5;
            if (number <= 100) return 6;
            return 9;
        }

        return key switch
        {
            // Gen II
            "sun-stone" or
            "rage-candy-bar" or
            "berry" or "gold-berry" or "przcure-berry" or "psncure-berry" or
            "bitter-berry" or "burnt-berry" or "ice-berry" or "mint-berry" or
            "miracle-berry" or "mystery-berry" or
            "tiny-mushroom" or "big-mushroom" or "big-pearl" or "star-piece" or
            "slowpoke-tail" or "gold-leaf" or "silver-leaf" => 2,

            // Gen III
            "premier-ball" or "luxury-ball" or "dive-ball" or "repeat-ball" or
            "timer-ball" or "nest-ball" or "net-ball" or
            "oran-berry" or "pecha-berry" or "cheri-berry" or "chesto-berry" or
            "rawst-berry" or "aspear-berry" or "persim-berry" or "sitrus-berry" => 3,

            // Gen IV
            "dusk-ball" or "heal-ball" or "quick-ball" or
            "dusk-stone" or "dawn-stone" or "shiny-stone" or "rare-bone" => 4,

            // Gen V
            "big-nugget" or "balm-mushroom" or "pearl-string" or
            "comet-shard" or "pretty-wing" => 5,

            // Gen VII
            "ice-stone" => 7,

            _ => 1,
        };
    }

""" + insert_anchor
shop = rep(shop, insert_anchor, insert, "shop catalog helpers")

shop_path.write_text(shop, encoding="utf-8")

# ===========================================================================
# Shop category rail: never show empty placeholders. "Stones" was redundant
# with Evolution Items; Key Items should not be a normal buy/sell category.
# ===========================================================================
page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = page.replace("    'Stones': 'hard-stone',\n", "")
page = page.replace("    'Key Items': 'coin-case',\n", "")

page = rep(page,
"""    const preferred = [
        'All', 'Poké Balls', 'Medicine', 'Status', 'Battle', 'Berries',
        'Stones', 'TMs', 'Utilities', 'Valuables', 'Key Items', 'Evolution Items',
    ];
""",
"""    const preferred = [
        'All', 'Poké Balls', 'Medicine', 'Status', 'Battle', 'Berries',
        'TMs', 'Utilities', 'Valuables', 'Evolution Items',
    ];
""",
"category preferred cleanup")

page = rep(page,
"""    const available = new Set(items.map(item => item.category));
    const categories = [ ...preferred ];
    for (const category of [...available].sort())
""",
"""    const available = new Set(items.map(item => item.category));
    const categories = preferred.filter(category => category === 'All' || available.has(category));
    for (const category of [...available].sort())
""",
"hide empty categories")

page = rep(page,
"""    React.useEffect(() => { void reload(); }, [ reload ]);
    React.useLayoutEffect(() => {
""",
"""    React.useEffect(() => { void reload(); }, [ reload ]);
    React.useEffect(() => {
        if (!state || category === 'All')
            return;
        if (!state.items.some(item => item.category === category))
            setCategory('All');
    }, [ state, category, setCategory ]);
    React.useLayoutEffect(() => {
""",
"reset removed category")

page_path.write_text(page, encoding="utf-8")

print("PKVault V8 alpha52m1 Gen2 TM movement + progressive shop/TM unlocks applied")
