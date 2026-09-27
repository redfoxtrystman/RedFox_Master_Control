from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha51l anchor not found: {label}")
    return text.replace(old, new, 1)

# Catalog rows are sized from the actual list viewport. At 100% exactly
# 12 rows fit; larger scales reduce density to a six-row minimum, while
# smaller scales can expose more than 12.
page = replace_once(
    page,
    """    basketCount: number;
    onAdd: (count: number) => void;
}> = ({ item, mode, loadedVersions, basketCount, onAdd }) => {
""",
    """    basketCount: number;
    rowHeight: number;
    onAdd: (count: number) => void;
}> = ({ item, mode, loadedVersions, basketCount, rowHeight, onAdd }) => {
""",
    "CatalogRow rowHeight prop",
)

page = replace_once(
    page,
    """    return <Card
        withBorder
        p='xs'
        radius='sm'
        style={{
            backgroundColor: SHOP_ROW,
            borderColor: SHOP_BORDER,
            overflow: 'hidden',
        }}
    >
""",
    """    const rowPadding = Math.max(2, Math.min(8, (rowHeight - 30) / 2));
    const iconSize = Math.max(24, Math.min(46 * Math.max(0.75, Number.parseFloat(String(getComputedStyle(document.documentElement).getPropertyValue('--mantine-scale'))) || 1), rowHeight - 6));

    return <Card
        withBorder
        p={rowPadding}
        radius='sm'
        h={rowHeight}
        style={{
            backgroundColor: SHOP_ROW,
            borderColor: SHOP_BORDER,
            overflow: 'hidden',
            flexShrink: 0,
        }}
    >
""",
    "CatalogRow fixed viewport-derived height",
)

# Avoid reading global CSS for icon sizing; derive it directly from the row.
page = page.replace(
    "const iconSize = Math.max(24, Math.min(46 * Math.max(0.75, Number.parseFloat(String(getComputedStyle(document.documentElement).getPropertyValue('--mantine-scale'))) || 1), rowHeight - 6));",
    "const iconSize = Math.max(24, Math.min(46, rowHeight - 6));",
    1,
)

page = replace_once(
    page,
    """                <ItemIcon item={item} size={46} />
""",
    """                <ItemIcon item={item} size={iconSize} />
""",
    "CatalogRow adaptive icon size",
)

page = replace_once(
    page,
    """    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
    const [ buyBasket, setBuyBasket ] = useLocalStorage<ShopBasket>({ key: 'pkvault-shop-buy-basket', defaultValue: {} });
""",
    """    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
    const catalogViewportRef = React.useRef<HTMLDivElement>(null);
    const [ catalogViewportHeight, setCatalogViewportHeight ] = React.useState(0);
    const [ buyBasket, setBuyBasket ] = useLocalStorage<ShopBasket>({ key: 'pkvault-shop-buy-basket', defaultValue: {} });
""",
    "catalog viewport measurement state",
)

page = replace_once(
    page,
    """    React.useEffect(() => { void reload(); }, [ reload ]);
    React.useEffect(() => {
""",
    """    React.useEffect(() => { void reload(); }, [ reload ]);
    React.useLayoutEffect(() => {
        const element = catalogViewportRef.current;
        if (!element) return;

        const update = () => setCatalogViewportHeight(element.clientHeight);
        update();
        const observer = new ResizeObserver(update);
        observer.observe(element);
        return () => observer.disconnect();
    }, [ state ]);

    React.useEffect(() => {
""",
    "catalog ResizeObserver",
)

page = replace_once(
    page,
    """    const shopScale = Math.max(1, shopScaleRaw);

    return <Box
""",
    """    const shopScale = Math.max(0.5, shopScaleRaw);
    const visibleCatalogRows = Math.max(6, Math.round(12 / shopScale));
    const catalogGap = 5;
    const catalogRowHeight = catalogViewportHeight > 0
        ? Math.max(28, (catalogViewportHeight - catalogGap * (visibleCatalogRows - 1) - 1) / visibleCatalogRows)
        : 48;

    return <Box
""",
    "catalog density calculation",
)

page = replace_once(
    page,
    """                        <ScrollArea
                            h='calc(100% - 30px)'
                            type='always'
                            offsetScrollbars
                            scrollbarSize={8}
                        >
                            <Stack gap={5} pr='sm'>
                                {items.map(item => <CatalogRow
""",
    """                        <Box
                            ref={catalogViewportRef}
                            h='calc(100% - 30px)'
                            style={{ minHeight: 0 }}
                        >
                        <ScrollArea
                            h='100%'
                            type='always'
                            offsetScrollbars
                            scrollbarSize={8}
                        >
                            <Stack gap={catalogGap} pr='sm'>
                                {items.map(item => <CatalogRow
""",
    "catalog viewport wrapper",
)

page = replace_once(
    page,
    """                                    basketCount={basket[item.key] ?? 0}
                                    onAdd={count => {
""",
    """                                    basketCount={basket[item.key] ?? 0}
                                    rowHeight={catalogRowHeight}
                                    onAdd={count => {
""",
    "CatalogRow rowHeight binding",
)

page = replace_once(
    page,
    """                            </Stack>
                        </ScrollArea>
                    </Card>
""",
    """                            </Stack>
                        </ScrollArea>
                        </Box>
                    </Card>
""",
    "catalog viewport wrapper close",
)

page_path.write_text(page, encoding="utf-8")

# The shared Storage/Shop scaler previously had sub-100 values commented out.
# Enable 50% and 75% only for storage-sprite-size so Shop can show >12 rows.
scale_path = root / "frontend/src/ui/layout/header/sub-header/ui-sprite-sizing-button.tsx"
scale = scale_path.read_text(encoding="utf-8")
scale = replace_once(
    scale,
    """    const marks = [
        // 25,
        // 50,
        // 75,
        100,
        125,
        150,
        175,
        200,
    ];
""",
    """    const marks = localStorageKey === 'storage-sprite-size'
        ? [ 50, 75, 100, 125, 150, 175, 200 ]
        : [ 100, 125, 150, 175, 200 ];
""",
    "shared Storage/Shop lower scale marks",
)
scale_path.write_text(scale, encoding="utf-8")

print("PKVault V8 alpha51l viewport-based 12-row Shop density applied")
