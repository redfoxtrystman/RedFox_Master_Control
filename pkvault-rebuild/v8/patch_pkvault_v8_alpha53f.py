from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

# Alpha53f economy balance:
# - Bottle Caps are now meaningful even before PKVault gets a Hyper Training UI:
#   they can be sold from the PKVault Item Bank.
# - Gym badge/circuit rewards stop flooding mature vaults with Rare Candies.
# - Existing claimed achievement IDs are untouched, so this does not re-pay or
#   claw back rewards from established users.

shop = root / "PKVault.Core/shop/ShopService.cs"
text = shop.read_text(encoding="utf-8")
old_shop = '''        new("rare-candy", "Utilities", 5000, 2500),
        new("pp-up", "Utilities", 9800, 4900),
'''
new_shop = '''        new("rare-candy", "Utilities", 5000, 2500),
        new("pp-up", "Utilities", 9800, 4900),

        // PKVault currently awards Bottle Caps before it exposes an in-app
        // Hyper Training system. Keep them useful in the meantime by allowing
        // players to cash them out without making them purchasable.
        new("bottle-cap", "Valuables", 0, 10000, false, true),
        new("gold-bottle-cap", "Valuables", 0, 50000, false, true),
'''
if old_shop in text:
    text = text.replace(old_shop, new_shop, 1)
elif 'new("gold-bottle-cap", "Valuables", 0, 50000, false, true)' not in text:
    raise RuntimeError("alpha53f ShopService anchor missing")
shop.write_text(text, encoding="utf-8")

quest = root / "PKVault.Core/quest/QuestService.cs"
text = quest.read_text(encoding="utf-8")
old_badges = '''    private static GymRewardPlan GetGymBadgeReward(int badgeIndex) => badgeIndex switch
    {
        0 => new(new("Great Ball", 5), "great-ball", null),
        1 => new(new("Super Potion", 5), "super-potion", null),
        2 => new(new("5 Great Balls + 2 Revives", 1), null, [("great-ball", 5L), ("revive", 2L)]),
        3 => new(new("Ultra Ball", 5), "ultra-ball", null),
        4 => new(new("5 Hyper Potions + 3 Full Heals", 1), null, [("hyper-potion", 5L), ("full-heal", 3L)]),
        5 => new(new("Rare Candy", 3), "rare-candy", null),
        6 => new(new("5 Ultra Balls + 2 Max Revives", 1), null, [("ultra-ball", 5L), ("max-revive", 2L)]),
        7 => new(new("5 Rare Candies + 5 Full Restores", 1), null, [("rare-candy", 5L), ("full-restore", 5L)]),
        8 => new(new("5 Ultra Balls + 2 Rare Candies", 1), null, [("ultra-ball", 5L), ("rare-candy", 2L)]),
        9 => new(new("5 Ultra Balls + 3 Full Restores", 1), null, [("ultra-ball", 5L), ("full-restore", 3L)]),
        10 => new(new("3 Rare Candies + 2 Max Revives", 1), null, [("rare-candy", 3L), ("max-revive", 2L)]),
        11 => new(new("Ultra Ball", 10), "ultra-ball", null),
        12 => new(new("Rare Candy", 5), "rare-candy", null),
        13 => new(new("PP Up + 5 Full Restores", 1), null, [("pp-up", 1L), ("full-restore", 5L)]),
        14 => new(new("2 PP Ups + 3 Max Revives", 1), null, [("pp-up", 2L), ("max-revive", 3L)]),
        _ => new(new("Bottle Cap + PP Max + 10 Ultra Balls", 1), null, [("bottle-cap", 1L), ("pp-max", 1L), ("ultra-ball", 10L)]),
    };

    private static GymRewardPlan GetGymCircuitReward(int badgeCount)
        => badgeCount > 8
            ? new(new("Gold Bottle Cap + 2 PP Max + 10 Rare Candies + 20 Ultra Balls", 1), null, [("gold-bottle-cap", 1L), ("pp-max", 2L), ("rare-candy", 10L), ("ultra-ball", 20L)])
            : new(new("Bottle Cap + 5 Rare Candies + 10 Ultra Balls + 5 Max Revives", 1), null, [("bottle-cap", 1L), ("rare-candy", 5L), ("ultra-ball", 10L), ("max-revive", 5L)]);
'''
new_badges = '''    private static GymRewardPlan GetGymBadgeReward(int badgeIndex) => badgeIndex switch
    {
        0 => new(new("Great Ball", 5), "great-ball", null),
        1 => new(new("Super Potion", 5), "super-potion", null),
        2 => new(new("5 Great Balls + 2 Revives", 1), null, [("great-ball", 5L), ("revive", 2L)]),
        3 => new(new("Ultra Ball", 5), "ultra-ball", null),
        4 => new(new("5 Hyper Potions + 3 Full Heals", 1), null, [("hyper-potion", 5L), ("full-heal", 3L)]),
        5 => new(new("Rare Candy", 1), "rare-candy", null),
        6 => new(new("5 Ultra Balls + 2 Max Revives", 1), null, [("ultra-ball", 5L), ("max-revive", 2L)]),
        7 => new(new("2 Rare Candies + 5 Full Restores", 1), null, [("rare-candy", 2L), ("full-restore", 5L)]),
        8 => new(new("5 Ultra Balls + Rare Candy", 1), null, [("ultra-ball", 5L), ("rare-candy", 1L)]),
        9 => new(new("5 Ultra Balls + 3 Full Restores", 1), null, [("ultra-ball", 5L), ("full-restore", 3L)]),
        10 => new(new("Rare Candy + 2 Max Revives", 1), null, [("rare-candy", 1L), ("max-revive", 2L)]),
        11 => new(new("Ultra Ball", 10), "ultra-ball", null),
        12 => new(new("Rare Candy", 2), "rare-candy", null),
        13 => new(new("PP Up + 5 Full Restores", 1), null, [("pp-up", 1L), ("full-restore", 5L)]),
        14 => new(new("2 PP Ups + 3 Max Revives", 1), null, [("pp-up", 2L), ("max-revive", 3L)]),
        _ => new(new("Bottle Cap + PP Max + 10 Ultra Balls", 1), null, [("bottle-cap", 1L), ("pp-max", 1L), ("ultra-ball", 10L)]),
    };

    private static GymRewardPlan GetGymCircuitReward(int badgeCount)
        => badgeCount > 8
            ? new(new("Gold Bottle Cap + 2 PP Max + 3 Rare Candies + 20 Ultra Balls", 1), null, [("gold-bottle-cap", 1L), ("pp-max", 2L), ("rare-candy", 3L), ("ultra-ball", 20L)])
            : new(new("Bottle Cap + 2 Rare Candies + 10 Ultra Balls + 5 Max Revives", 1), null, [("bottle-cap", 1L), ("rare-candy", 2L), ("ultra-ball", 10L), ("max-revive", 5L)]);
'''
if old_badges in text:
    text = text.replace(old_badges, new_badges, 1)
elif 'Gold Bottle Cap + 2 PP Max + 3 Rare Candies + 20 Ultra Balls' not in text:
    raise RuntimeError("alpha53f gym reward anchor missing")
quest.write_text(text, encoding="utf-8")

print("PASS alpha53f Bottle Cap sale + gym Rare Candy rebalance")
