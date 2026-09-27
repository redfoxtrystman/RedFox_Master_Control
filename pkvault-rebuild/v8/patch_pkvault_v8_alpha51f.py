from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha51f anchor not found: {label}")
    return text.replace(old, new, 1)

# Backend: preserve canonical catalog order and expose it to the frontend.
service_path = root / "PKVault.Core/shop/ShopService.cs"
service = service_path.read_text(encoding="utf-8")

service = replace_once(
    service,
    """    long OwnedInBank,
    long OwnedTotal,
    List<int> CompatibleVersions,
""",
    """    long OwnedInBank,
    long OwnedTotal,
    int SortOrder,
    List<int> CompatibleVersions,
""",
    "ShopItemDTO SortOrder"
)

service = replace_once(
    service,
    "        var items = Prices.Select(price =>\n",
    "        var items = Prices.Select((price, sortOrder) =>\n",
    "Prices indexed projection"
)

service = replace_once(
    service,
    """                OwnedInBank: BankCount(price.Key),
                OwnedTotal: TotalCount(price.Key),
                CompatibleVersions: compatible,
""",
    """                OwnedInBank: BankCount(price.Key),
                OwnedTotal: TotalCount(price.Key),
                SortOrder: sortOrder,
                CompatibleVersions: compatible,
""",
    "ShopItemDTO projection SortOrder"
)

service = replace_once(
    service,
    """        })
        .OrderBy(x => x.Name, StringComparer.CurrentCultureIgnoreCase)
        .ToList();
""",
    """        })
        .ToList();
""",
    "remove forced alpha sorting"
)

service_path.write_text(service, encoding="utf-8")

# Frontend model.
types_path = root / "frontend/src/shop/types.ts"
types = types_path.read_text(encoding="utf-8")
types = replace_once(
    types,
    """    ownedInBank: number;
    ownedTotal: number;
    compatibleVersions: number[];
""",
    """    ownedInBank: number;
    ownedTotal: number;
    sortOrder: number;
    compatibleVersions: number[];
""",
    "frontend ShopItem sortOrder"
)
types_path.write_text(types, encoding="utf-8")

# Frontend visual/category/sorting parity.
page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

start = page.index("const CategoryList:")
end = page.index("const CatalogRow:", start)

category_block = r"""const CATEGORY_ICON_KEYS: Record<string, string> = {
    'Poké Balls': 'poke-ball',
    'Medicine': 'potion',
    'Status': 'full-heal',
    'Battle': 'x-attack',
    'Berries': 'oran-berry',
    'Stones': 'hard-stone',
    'TMs': 'tm01',
    'Utilities': 'escape-rope',
    'Key Items': 'coin-case',
    'Evolution Items': 'fire-stone',
};

const categoryIconItem = (key: string, items: ShopItem[]): ShopItem =>
    items.find(item => item.key === key) ?? {
        key,
        name: key,
        category: '',
        buyPrice: 0,
        sellPrice: 0,
        canBuy: false,
        canSell: false,
        ownedInBank: 0,
        ownedTotal: 0,
        sortOrder: 0,
        compatibleVersions: [],
        aliases: [],
    };

const CategoryList: React.FC<{
    items: ShopItem[];
    selected: string;
    onSelect: (category: string) => void;
}> = ({ items, selected, onSelect }) => {
    const preferred = [
        'All', 'Poké Balls', 'Medicine', 'Status', 'Battle', 'Berries',
        'Stones', 'TMs', 'Utilities', 'Key Items', 'Evolution Items',
    ];
    const counts = new Map<string, number>();
    for (const item of items)
        counts.set(item.category, (counts.get(item.category) ?? 0) + 1);

    const available = new Set(items.map(item => item.category));
    const categories = [ ...preferred ];
    for (const category of [...available].sort())
        if (!categories.includes(category)) categories.push(category);

    return <Stack gap={0}>
        {categories.map(category => {
            const active = selected === category;
            const iconKey = CATEGORY_ICON_KEYS[category];
            const count = category === 'All' ? items.length : (counts.get(category) ?? 0);

            return <Button
                key={category}
                size='compact-sm'
                variant='subtle'
                onClick={() => onSelect(category)}
                fullWidth
                px={8}
                radius={active ? 'sm' : 0}
                styles={{
                    root: active ? {
                        ...actionButtonStyle(SHOP_RED, '#d56b5c'),
                        minHeight: 38,
                        borderBottom: '1px solid var(--mantine-color-dark-5)',
                    } : {
                        minHeight: 38,
                        color: 'var(--mantine-color-text)',
                        backgroundColor: 'transparent',
                        borderBottom: '1px solid var(--mantine-color-dark-6)',
                    },
                    inner: {
                        justifyContent: 'stretch',
                    },
                    label: {
                        width: '100%',
                        overflow: 'visible',
                    },
                }}
            >
                <Box
                    style={{
                        width: '100%',
                        display: 'grid',
                        gridTemplateColumns: '30px minmax(0, 1fr) 42px',
                        alignItems: 'center',
                        columnGap: 8,
                    }}
                >
                    <Box style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        {category === 'All'
                            ? <Grid2X2Icon size={20} />
                            : iconKey
                                ? <ItemIcon item={categoryIconItem(iconKey, items)} size={26} />
                                : null}
                    </Box>
                    <Text
                        size='sm'
                        fw={active ? 700 : 500}
                        ta='left'
                        truncate
                    >
                        {category}
                    </Text>
                    <Text
                        size='sm'
                        fw={active ? 700 : 500}
                        ta='right'
                        style={{ fontVariantNumeric: 'tabular-nums' }}
                    >
                        {count.toLocaleString()}
                    </Text>
                </Box>
            </Button>;
        })}
    </Stack>;
};

"""

page = page[:start] + category_block + page[end:]

page = replace_once(
    page,
    "    const [ sort, setSort ] = useLocalStorage({ key: 'pkvault-shop-sort', defaultValue: 'name' });\n",
    "    const [ sort, setSort ] = useLocalStorage({ key: 'pkvault-shop-sort', defaultValue: 'game' });\n",
    "default in-game sort"
)

page = replace_once(
    page,
    """        .sort((a, b) => {
            if (sort === 'price-low')
""",
    """        .sort((a, b) => {
            if (sort === 'game')
                return a.sortOrder - b.sortOrder || a.name.localeCompare(b.name);
            if (sort === 'price-low')
""",
    "in-game sort branch"
)

page = page.replace(
    """            if (sort === 'owned')
                return b.ownedInBank - a.ownedInBank || a.name.localeCompare(b.name);
""",
    ""
)

page = replace_once(
    page,
    """                                data={[
                                    { value: 'name', label: 'Name (A–Z)' },
                                    { value: 'price-low', label: 'Price (low–high)' },
                                    { value: 'price-high', label: 'Price (high–low)' },
                                    { value: 'owned', label: 'Owned' },
                                ]}
""",
    """                                data={[
                                    { value: 'game', label: 'In-game' },
                                    { value: 'name', label: 'Name (A–Z)' },
                                    { value: 'price-low', label: 'Price (low–high)' },
                                    { value: 'price-high', label: 'Price (high–low)' },
                                ]}
""",
    "sort select options"
)

page_path.write_text(page, encoding="utf-8")
print("PKVault V8 alpha51f Shop category rail + in-game sorting applied")
