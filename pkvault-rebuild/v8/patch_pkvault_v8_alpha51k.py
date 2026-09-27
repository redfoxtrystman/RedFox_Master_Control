from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "frontend/src/shop/shop-page.tsx"
text = path.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str):
    global text
    if old not in text:
        raise RuntimeError(f"alpha51k anchor not found: {label}")
    text = text.replace(old, new, 1)

replace_once(
    "import { useLocalStorage, useViewportSize } from '@mantine/hooks';",
    "import { useLocalStorage } from '@mantine/hooks';",
    "remove automatic viewport scaling import",
)

replace_once(
    """    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
    const { width: viewportWidth } = useViewportSize();
""",
    """    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
""",
    "remove viewport scale state",
)

replace_once(
    """    // Keep 100% comfortable on high-resolution displays without making
    // smaller windows unusably large. Manual Storage/Shop scale multiplies this.
    const automaticDisplayScale = Math.min(1.5, Math.max(1, viewportWidth / 1600));
    const shopScale = Math.max(1, shopScaleRaw) * automaticDisplayScale;
    const inverseScalePercent = `${100 / shopScale}%`;

    return <Box h='100%' style={{ minHeight: 0, overflow: 'hidden' }}>
        <Box
            w={inverseScalePercent}
            h={inverseScalePercent}
            p='xs'
            style={{
                minHeight: 0,
                overflow: 'hidden',
                zoom: shopScale,
            }}
        >
        <Stack h='100%' gap='xs' style={{ minHeight: 0 }}>
""",
    """    const shopScale = Math.max(1, shopScaleRaw);

    return <Box
        h='100%'
        p='xs'
        style={{
            minHeight: 0,
            overflow: 'hidden',
            '--mantine-scale': shopScale,
        } as React.CSSProperties}
    >
        <Stack h='100%' gap='xs' style={{ minHeight: 0 }}>
""",
    "replace destructive whole-page zoom",
)

replace_once(
    """        </Stack>
        </Box>

        <Modal
""",
    """        </Stack>

        <Modal
""",
    "remove inverse wrapper close",
)

replace_once(
    """            centered
            styles={{ content: { zoom: shopScale } }}
        >
""",
    """            centered
            styles={{ content: { '--mantine-scale': shopScale } as React.CSSProperties }}
        >
""",
    "modal uses manual scale variable",
)

replace_once(
    """                gridTemplateColumns: mode === 'sell'
                    ? '48px minmax(96px, 1fr) minmax(76px, 0.55fr) minmax(158px, 176px) 60px'
                    : '48px minmax(96px, 1fr) minmax(76px, 0.55fr) minmax(112px, 134px) 60px',
                alignItems: 'center',
                columnGap: 10,
""",
    """                gridTemplateColumns: mode === 'sell'
                    ? '48px minmax(96px, 1fr) minmax(72px, 0.55fr) 170px 64px'
                    : '48px minmax(96px, 1fr) minmax(72px, 0.55fr) 116px 64px',
                alignItems: 'center',
                columnGap: 8,
""",
    "CatalogRow columns fit controls",
)

replace_once(
    """            <Button
                size='xs'
                w={76}
                disabled={!enabled}
""",
    """            <Button
                size='xs'
                fullWidth
                disabled={!enabled}
""",
    "Add/Sell button fits grid cell",
)

replace_once(
    """                        <ScrollArea h='calc(100% - 30px)' type='always' offsetScrollbars>
                            <Stack gap={5} pr='xs'>
""",
    """                        <ScrollArea
                            h='calc(100% - 30px)'
                            type='always'
                            offsetScrollbars
                            scrollbarSize={8}
                        >
                            <Stack gap={5} pr='sm'>
""",
    "reserve item scrollbar edge",
)

path.write_text(text, encoding="utf-8")
print("PKVault V8 alpha51k reverted monitor auto-zoom and fixed row clipping")
