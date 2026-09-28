from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52n anchor not found: {label}")
    return text.replace(old, new, 1)

shop_path = root / "PKVault.Core/shop/ShopService.cs"
shop = shop_path.read_text(encoding="utf-8")

shop = rep(
    shop,
    '    private const string TmUnlockProgressionKey = "shop.tm.unlocks";\n',
    '    private const string TmUnlockProgressionKey = "shop.tm.unlocks";\n'
    '    private const string MasterBallUnlockProgressionKey = "shop.master-ball.unlocked";\n',
    "master ball progression key",
)

old = '''        foreach (var tm in unlockedTms
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
'''
new = '''        foreach (var tm in unlockedTms
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

        if (await LoadAndUpdateMasterBallUnlock(inventory)
            && !catalog.Any(price => string.Equals(price.Key, "master-ball", StringComparison.Ordinal)))
        {
            // A Master Ball becomes a permanent luxury purchase only after the
            // player has legitimately obtained one somewhere PKVault can see.
            catalog.Add(new("master-ball", "Poké Balls", 3_500_000, 0, true, false));
        }

        return catalog;
'''
shop = rep(shop, old, new, "master ball catalog unlock")

shop = rep(
    shop,
    '    private async Task<HashSet<string>> LoadAndUpdateTmUnlocks(ItemInventoryStateDTO inventory)\n    {\n',
    '''    private async Task<bool> LoadAndUpdateMasterBallUnlock(ItemInventoryStateDTO inventory)
    {
        var persisted = await progressionStore.Get(MasterBallUnlockProgressionKey);
        var unlocked = string.Equals(persisted, "1", StringComparison.Ordinal);

        if (!unlocked)
        {
            unlocked = inventory.BankPages
                .SelectMany(page => page.Slots)
                .Concat(inventory.Saves.SelectMany(save => save.Pockets).SelectMany(pocket => pocket.Slots))
                .Any(slot => slot.ItemKey is not null
                    && Equivalent(slot.ItemKey, "master-ball")
                    && slot.Count > 0);

            if (unlocked)
                await progressionStore.Set(MasterBallUnlockProgressionKey, "1");
        }

        return unlocked;
    }

    private async Task<HashSet<string>> LoadAndUpdateTmUnlocks(ItemInventoryStateDTO inventory)
    {
''',
    "master ball discovery helper",
)

shop_path.write_text(shop, encoding="utf-8")

page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = rep(
    page,
    "import { getGameInfos } from '../pokedex/details/util/get-game-infos';\n",
    "import { getGameInfos } from '../pokedex/details/util/get-game-infos';\n"
    "import { useStaticData } from '../hooks/use-static-data';\n",
    "static data import",
)

page = rep(
    page,
    "const CompatibilityBadges: React.FC<{ item: ShopItem; loadedVersions: number[] }> = ({ item, loadedVersions }) => {\n"
    "    const versions = item.compatibleVersions\n",
    "const CompatibilityBadges: React.FC<{ item: ShopItem; loadedVersions: number[] }> = ({ item, loadedVersions }) => {\n"
    "    const staticData = useStaticData();\n"
    "    const versions = item.compatibleVersions\n",
    "compatibility static data",
)

tick = chr(96)
old_compat = (
    "                return <Tooltip key={version} label={" + tick + "Compatible game ${version}" + tick + "}>\n"
    "                    <Image src={info.img} w={16} h={16} fit='contain' />\n"
    "                </Tooltip>;\n"
    "            } catch {\n"
    "                return <Badge key={version} size='xs' variant='light'>{version}</Badge>;"
)
new_compat = """                const versionName = staticData.versions[version]?.name ?? ('Game ' + version);
                return <Tooltip key={version} label={'Compatible with ' + versionName}>
                    <Image src={info.img} w={16} h={16} fit='contain' />
                </Tooltip>;
            } catch {
                const versionName = staticData.versions[version]?.name ?? ('Game ' + version);
                return <Badge key={version} size='xs' variant='light'>{versionName}</Badge>;"""
page = rep(page, old_compat, new_compat, "compatibility names")

page = rep(
    page,
    """    React.useEffect(() => {
        if (!state || category === 'All')
            return;
        if (!state.items.some(item => item.category === category))
            setCategory('All');
    }, [ state, category, setCategory ]);
""",
    """    React.useEffect(() => {
        if (!state || category === 'All')
            return;
        const visibleForMode = state.items.filter(item =>
            mode === 'buy' ? item.canBuy : item.canSell && item.ownedInBank > 0
        );
        if (!visibleForMode.some(item => item.category === category))
            setCategory('All');
    }, [ state, category, mode, setCategory ]);
""",
    "mode-aware category reset",
)

page = rep(
    page,
    """    const normalizedSearch = normalize(search);
    const items = state.items
        .filter(item => mode === 'buy' ? item.canBuy : item.canSell && item.ownedInBank > 0)
""",
    """    const normalizedSearch = normalize(search);
    const modeItems = state.items
        .filter(item => mode === 'buy' ? item.canBuy : item.canSell && item.ownedInBank > 0);
    const items = modeItems
""",
    "mode-visible catalog",
)

page = rep(
    page,
    "                                <CategoryList items={state.items} selected={category} onSelect={setCategory} />\n",
    "                                <CategoryList items={modeItems} selected={category} onSelect={setCategory} />\n",
    "category list mode items",
)

page = rep(
    page,
    "                                data={['All', ...new Set(state.items.map(item => item.category))]}\n",
    "                                data={['All', ...new Set(modeItems.map(item => item.category))]}\n",
    "category select mode items",
)

page_path.write_text(page, encoding="utf-8")
print("PKVault V8 alpha52n compatibility labels + accurate category counts + Master Ball unlock applied")
