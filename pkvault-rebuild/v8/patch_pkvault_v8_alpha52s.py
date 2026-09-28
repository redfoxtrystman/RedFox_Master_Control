from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52s anchor not found: {label}")
    return text.replace(old, new, 1)

# ===========================================================================
# SHOP: fill obvious Gen I/II sell gaps and make Apricorns sellable immediately,
# but purchasable only after the permanent all-colors achievement is claimed.
# ===========================================================================
shop_path = root / "PKVault.Core/shop/ShopService.cs"
shop = shop_path.read_text(encoding="utf-8")

shop = rep(
    shop,
    """        new("max-elixir", "Medicine", 4500, 2250),

        new("antidote", "Status", 200, 100),
""",
    """        new("max-elixir", "Medicine", 4500, 2250),
        new("fresh-water", "Medicine", 200, 100),
        new("soda-pop", "Medicine", 300, 150),
        new("lemonade", "Medicine", 350, 175),
        new("moomoo-milk", "Medicine", 500, 250),
        new("energy-powder", "Medicine", 500, 250),
        new("energy-root", "Medicine", 800, 400),
        new("revival-herb", "Medicine", 2800, 1400),

        new("antidote", "Status", 200, 100),
""",
    "early medicine expansion",
)

shop = rep(
    shop,
    """        new("full-heal", "Status", 600, 300),

        new("repel", "Utilities", 350, 175),
""",
    """        new("full-heal", "Status", 600, 300),
        new("heal-powder", "Status", 450, 225),

        new("repel", "Utilities", 350, 175),
""",
    "heal powder",
)

shop = rep(
    shop,
    """        new("pp-up", "Utilities", 9800, 4900),

        // Classic sell-for-cash treasure items. Sell-only by design.
""",
    """        new("pp-up", "Utilities", 9800, 4900),

        // Gen I/II permanent-stat items. These were missing from the original
        // conservative Shop table even though they are ordinary Mart items.
        new("hp-up", "Vitamins", 9800, 4900),
        new("protein", "Vitamins", 9800, 4900),
        new("iron", "Vitamins", 9800, 4900),
        new("carbos", "Vitamins", 9800, 4900),
        new("calcium", "Vitamins", 9800, 4900),

        // Classic sell-for-cash treasure items. Sell-only by design.
""",
    "Gen1/2 vitamins",
)

shop = rep(
    shop,
    """        new("x-accuracy", "Battle", 950, 475),
        new("dire-hit", "Battle", 650, 325),
""",
    """        new("x-accuracy", "Battle", 950, 475),
        new("x-special", "Battle", 350, 175),
        new("dire-hit", "Battle", 650, 325),
""",
    "X Special",
)

shop = rep(
    shop,
    """        new("guard-spec", "Battle", 700, 350),

        // Generation II berry names remain distinct from their Gen III+
""",
    """        new("guard-spec", "Battle", 700, 350),

        // Gen II Apricorns are always sellable once present in PKVault.
        // Buying them is a convenience reward unlocked by the all-colors
        // achievement below. Their GSC sell value is ₽100; PKVault charges a
        // convenience premium when the permanent purchase unlock is earned.
        new("red-apricorn", "Apricorns", 1000, 100, false, true),
        new("yellow-apricorn", "Apricorns", 1000, 100, false, true),
        new("blue-apricorn", "Apricorns", 1000, 100, false, true),
        new("green-apricorn", "Apricorns", 1000, 100, false, true),
        new("pink-apricorn", "Apricorns", 1000, 100, false, true),
        new("white-apricorn", "Apricorns", 1000, 100, false, true),
        new("black-apricorn", "Apricorns", 1000, 100, false, true),

        // Generation II berry names remain distinct from their Gen III+
""",
    "Apricorn sell catalog",
)

shop = rep(
    shop,
    """    private const string TmUnlockProgressionKey = "shop.tm.unlocks";
    private const string MasterBallUnlockProgressionKey = "shop.master-ball.unlocked";
""",
    """    private const string TmUnlockProgressionKey = "shop.tm.unlocks";
    private const string MasterBallUnlockProgressionKey = "shop.master-ball.unlocked";
    private const string ApricornUnlockProgressionKey = "shop.apricorn.unlocked";

    private static readonly HashSet<string> ApricornKeys = new(StringComparer.Ordinal)
    {
        "red-apricorn",
        "yellow-apricorn",
        "blue-apricorn",
        "green-apricorn",
        "pink-apricorn",
        "white-apricorn",
        "black-apricorn",
    };
""",
    "Apricorn unlock constants",
)

shop = rep(
    shop,
    """        var catalog = Prices
            .Where(price => GetMinimumGeneration(price.Key) <= maxGeneration)
            .ToList();

        var unlockedTms = await LoadAndUpdateTmUnlocks(inventory);
""",
    """        var catalog = Prices
            .Where(price => GetMinimumGeneration(price.Key) <= maxGeneration)
            .ToList();

        if (string.Equals(
            await progressionStore.Get(ApricornUnlockProgressionKey),
            "1",
            StringComparison.Ordinal))
        {
            catalog = catalog
                .Select(price => ApricornKeys.Contains(Canonical(price.Key))
                    ? price with { CanBuy = true }
                    : price)
                .ToList();
        }

        var unlockedTms = await LoadAndUpdateTmUnlocks(inventory);
""",
    "Apricorn buy unlock",
)

shop = rep(
    shop,
    """            "sun-stone" or
            "rage-candy-bar" or
            "berry" or "gold-berry" or "przcure-berry" or "psncure-berry" or
""",
    """            "sun-stone" or
            "rage-candy-bar" or
            "moomoo-milk" or "energy-powder" or "energy-root" or
            "heal-powder" or "revival-herb" or
            "red-apricorn" or "yellow-apricorn" or "blue-apricorn" or
            "green-apricorn" or "pink-apricorn" or "white-apricorn" or
            "black-apricorn" or
            "berry" or "gold-berry" or "przcure-berry" or "psncure-berry" or
""",
    "Gen2 minimum generation",
)

shop = rep(
    shop,
    """        "ylw-apricorn" => "yellow-apricorn",
        _ => itemKey.Trim().ToLowerInvariant(),
""",
    """        "ylw-apricorn" => "yellow-apricorn",
        // PKHeX/older games retain the pre-Gen-VI item name. The Shop uses the
        // modern canonical row but must treat X Defend and X Defense as one item.
        "x-defend" => "x-defense",
        _ => itemKey.Trim().ToLowerInvariant(),
""",
    "X Defend alias",
)

shop_path.write_text(shop, encoding="utf-8")

# ===========================================================================
# QUESTS / ACHIEVEMENTS: collect every Gen II Apricorn color, then CLAIM the
# achievement to permanently unlock Apricorn purchasing in the Shop.
# ===========================================================================
quest_path = root / "PKVault.Core/quest/QuestService.cs"
quest = quest_path.read_text(encoding="utf-8")

quest = rep(
    quest,
    """    private const string AllRegionsArchivistMagearnaRewardMarker = "reward-region-complete-all-original-color-magearna";
    private const string AllRegionsArchivistMagearnaVariantId = "9be20a53-f28b-4c0c-8c49-801000000001";
""",
    """    private const string AllRegionsArchivistMagearnaRewardMarker = "reward-region-complete-all-original-color-magearna";
    private const string AllRegionsArchivistMagearnaVariantId = "9be20a53-f28b-4c0c-8c49-801000000001";
    private const string ApricornRainbowAchievementId = "achievement-apricorn-rainbow";
    private const string ApricornUnlockProgressionKey = "shop.apricorn.unlocked";

    private static readonly string[] ApricornAchievementKeys =
    [
        "red-apricorn",
        "yellow-apricorn",
        "blue-apricorn",
        "green-apricorn",
        "pink-apricorn",
        "white-apricorn",
        "black-apricorn",
    ];
""",
    "Apricorn achievement constants",
)

# Claiming the achievement is the unlock boundary, matching the user's manual
# claim design instead of unlocking merely when progress reaches 7/7.
quest = rep(
    quest,
    """                completed.Add(plan.CompletionId);
                claimedNotifications.Add(new(
""",
    """                completed.Add(plan.CompletionId);
                if (string.Equals(plan.CompletionId, ApricornRainbowAchievementId, StringComparison.Ordinal))
                    await progressionStore.Set(ApricornUnlockProgressionKey, "1");

                claimedNotifications.Add(new(
""",
    "Apricorn unlock on claim",
)

quest = rep(
    quest,
    """        var achievements = new List<QuestEntryDTO>();

        foreach (var entry in regionProgress)
""",
    """        var achievements = new List<QuestEntryDTO>();

        var apricornColorsOwned = ApricornAchievementKeys.Count(key =>
            GetInventoryItemCount(itemInventory, key) > 0);
        achievements.Add(await EvaluateQuest(
            ApricornRainbowAchievementId,
            ApricornRainbowAchievementId,
            "Collection",
            "Apricorn Rainbow",
            "Own at least one Red, Yellow, Blue, Green, Pink, White, and Black Apricorn at the same time. Claim this achievement to permanently unlock all seven Apricorn colors for purchase in the PKVault Shop.",
            apricornColorsOwned,
            ApricornAchievementKeys.Length,
            new("Apricorn Shop Unlock", 1),
            null,
            completed,
            newlyCompleted
        ));

        foreach (var entry in regionProgress)
""",
    "Apricorn Rainbow achievement",
)

quest_path.write_text(quest, encoding="utf-8")

# ===========================================================================
# SHOP UI: give Apricorns and Vitamins proper category entries/icons.
# ===========================================================================
page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = rep(
    page,
    """    'Battle': 'x-attack',
    'Berries': 'oran-berry',
    'TMs': 'tm01',
""",
    """    'Battle': 'x-attack',
    'Vitamins': 'protein',
    'Berries': 'oran-berry',
    'Apricorns': 'red-apricorn',
    'TMs': 'tm01',
""",
    "Shop category icons",
)

page = rep(
    page,
    """        'All', 'Poké Balls', 'Medicine', 'Status', 'Battle', 'Berries',
        'TMs', 'Utilities', 'Valuables', 'Evolution Items',
""",
    """        'All', 'Poké Balls', 'Medicine', 'Status', 'Battle', 'Vitamins',
        'Berries', 'Apricorns', 'TMs', 'Utilities', 'Valuables', 'Evolution Items',
""",
    "Shop category ordering",
)

page_path.write_text(page, encoding="utf-8")

print("PKVault V8 alpha52s sell-catalog audit + Apricorn Rainbow unlock applied")
