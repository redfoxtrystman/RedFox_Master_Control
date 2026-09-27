from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "frontend/src/shop/shop-page.tsx"
text = path.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str):
    global text
    if old not in text:
        raise RuntimeError(f"alpha51j anchor not found: {label}")
    text = text.replace(old, new, 1)

replace_once(
    "import { useLocalStorage } from '@mantine/hooks';",
    "import { useLocalStorage, useViewportSize } from '@mantine/hooks';",
    "viewport hook import",
)

replace_once(
    """    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
""",
    """    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
    const { width: viewportWidth } = useViewportSize();
""",
    "viewport width state",
)

replace_once(
    """    const shopScale = Math.max(1, shopScaleRaw);
    const inverseScalePercent = `${100 / shopScale}%`;
""",
    """    // Keep 100% comfortable on high-resolution displays without making
    // smaller windows unusably large. Manual Storage/Shop scale multiplies this.
    const automaticDisplayScale = Math.min(1.5, Math.max(1, viewportWidth / 1600));
    const shopScale = Math.max(1, shopScaleRaw) * automaticDisplayScale;
    const inverseScalePercent = `${100 / shopScale}%`;
""",
    "resolution-aware Shop scale",
)

replace_once(
    """                gridTemplateColumns: mode === 'sell'
                    ? '54px minmax(145px, 1fr) minmax(108px, 0.7fr) 190px 76px'
                    : '54px minmax(145px, 1fr) minmax(108px, 0.7fr) 134px 76px',
""",
    """                gridTemplateColumns: mode === 'sell'
                    ? '48px minmax(96px, 1fr) minmax(76px, 0.55fr) minmax(158px, 176px) 60px'
                    : '48px minmax(96px, 1fr) minmax(76px, 0.55fr) minmax(112px, 134px) 60px',
""",
    "responsive CatalogRow columns",
)

replace_once(
    """                        <ScrollArea h='calc(100% - 30px)' type='auto'>
                            <CategoryList items={state.items} selected={category} onSelect={setCategory} />
                        </ScrollArea>
""",
    """                        <ScrollArea
                            h='calc(100% - 30px)'
                            type='auto'
                            offsetScrollbars
                            scrollbarSize={8}
                        >
                            <Box pr={4}>
                                <CategoryList items={state.items} selected={category} onSelect={setCategory} />
                            </Box>
                        </ScrollArea>
""",
    "category scrollbar reservation",
)

path.write_text(text, encoding="utf-8")
print("PKVault V8 alpha51j adaptive Shop scaling + responsive rows applied")
