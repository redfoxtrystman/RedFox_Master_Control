from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "frontend/src/shop/shop-page.tsx"
text = path.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str):
    global text
    if old not in text:
        raise RuntimeError(f"alpha51h anchor not found: {label}")
    text = text.replace(old, new, 1)

replace_once(
"""    loadedVersions: number[];
    onAdd: (count: number) => void;
}> = ({ item, mode, loadedVersions, onAdd }) => {
    const max = mode === 'sell' ? item.ownedInBank : 999_999;
""",
"""    loadedVersions: number[];
    basketCount: number;
    onAdd: (count: number) => void;
}> = ({ item, mode, loadedVersions, basketCount, onAdd }) => {
    const sellRemaining = Math.max(0, item.ownedInBank - basketCount);
    const max = mode === 'sell' ? sellRemaining : 999_999;
""",
"CatalogRow basketCount + remaining"
)

replace_once(
"""    const enabled = mode === 'buy' ? item.canBuy : item.canSell && item.ownedInBank > 0;
""",
"""    const enabled = mode === 'buy' ? item.canBuy : item.canSell && sellRemaining > 0;
""",
"CatalogRow sell enabled"
)

replace_once(
"""                gridTemplateColumns: '54px minmax(145px, 1fr) minmax(108px, 0.7fr) 134px 76px',
""",
"""                gridTemplateColumns: mode === 'sell'
                    ? '54px minmax(145px, 1fr) minmax(108px, 0.7fr) 190px 76px'
                    : '54px minmax(145px, 1fr) minmax(108px, 0.7fr) 134px 76px',
""",
"CatalogRow sell quantity column"
)

replace_once(
"""            <QuantityControl
                value={quantity}
                onChange={setQuantity}
                min={0}
                max={max}
                disabled={!enabled}
                compact
            />

            <Button
""",
"""            <Group gap={6} wrap='nowrap' style={{ flexShrink: 0 }}>
                <QuantityControl
                    value={quantity}
                    onChange={setQuantity}
                    min={0}
                    max={max}
                    disabled={!enabled}
                    compact
                />
                {mode === 'sell' && <Button
                    size='compact-xs'
                    variant='default'
                    w={48}
                    disabled={!enabled || max <= 0}
                    onClick={() => setQuantity(max)}
                >
                    MAX
                </Button>}
            </Group>

            <Button
""",
"CatalogRow MAX control"
)

replace_once(
"""                                    loadedVersions={state.loadedVersions}
                                    onAdd={count => updateBasket(item.key, (basket[item.key] ?? 0) + count)}
""",
"""                                    loadedVersions={state.loadedVersions}
                                    basketCount={basket[item.key] ?? 0}
                                    onAdd={count => {
                                        const current = basket[item.key] ?? 0;
                                        const next = mode === 'sell'
                                            ? Math.min(item.ownedInBank, current + count)
                                            : current + count;
                                        updateBasket(item.key, next);
                                    }}
""",
"CatalogRow parent basket clamp"
)

path.write_text(text, encoding="utf-8")
print("PKVault V8 alpha51h SELL MAX buttons applied")
