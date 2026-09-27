from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "frontend/src/shop/shop-page.tsx"
text = path.read_text(encoding="utf-8")

old = """    const rowPadding = Math.max(2, Math.min(8, (rowHeight - 30) / 2));
    const iconSize = Math.max(24, Math.min(46, rowHeight - 6));

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
        <Box
            style={{
                display: 'grid',
"""
new = """    // rowHeight is already calculated from the real catalog viewport.
    // Keep this height in raw CSS pixels so Mantine scaling cannot inflate
    // the row beyond its allotted slot. Then fit the contents inside it.
    const rowPadding = Math.max(1, Math.min(4, rowHeight * 0.08));
    const innerHeight = Math.max(0, rowHeight - (rowPadding * 2) - 2);
    const iconSize = Math.max(16, Math.min(40, innerHeight));

    return <Card
        withBorder
        p={0}
        radius='sm'
        style={{
            backgroundColor: SHOP_ROW,
            borderColor: SHOP_BORDER,
            overflow: 'hidden',
            flexShrink: 0,
            height: rowHeight,
            padding: rowPadding,
            boxSizing: 'border-box',
            display: 'flex',
            alignItems: 'stretch',
        }}
    >
        <Box
            style={{
                display: 'grid',
"""

if old not in text:
    raise RuntimeError("alpha52e CatalogRow sizing anchor not found")
text = text.replace(old, new, 1)

old = """                alignItems: 'center',
                columnGap: 'calc(8px * var(--mantine-scale, 1))',
                minWidth: 0,
            }}
        >
            <Box style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
"""
new = """                alignItems: 'center',
                columnGap: 'calc(8px * var(--mantine-scale, 1))',
                minWidth: 0,
                width: '100%',
                height: '100%',
                minHeight: 0,
            }}
        >
            <Box style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', minHeight: 0, overflow: 'hidden' }}>
"""
if old not in text:
    raise RuntimeError("alpha52e CatalogRow grid centering anchor not found")
text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("PKVault V8 alpha52e catalog row vertical alignment fix applied")
