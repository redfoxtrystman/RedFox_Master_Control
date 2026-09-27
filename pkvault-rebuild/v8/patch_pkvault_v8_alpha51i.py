from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha51i anchor not found: {label}")
    return text.replace(old, new, 1)

# Reuse Storage's existing scale control in the Shop sub-header.
header_path = root / "frontend/src/header/header.tsx"
header = header_path.read_text(encoding="utf-8")
header = replace_once(
    header,
    """            'shop': () => null,
""",
    """            'shop': () => <Group wrap='nowrap' align='flex-start' gap='sm' style={{ flexGrow: 1 }}>
                <UISpriteSizingButton
                    localStorageKey='storage-sprite-size'
                    ml='auto'
                />
            </Group>,
""",
    "Shop header scale button"
)
header_path.write_text(header, encoding="utf-8")

# Scale the whole Shop workspace with the same persisted value used by Storage.
page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = replace_once(
    page,
    """import { getGameInfos } from '../pokedex/details/util/get-game-infos';
""",
    """import { getGameInfos } from '../pokedex/details/util/get-game-infos';
import { useSpriteSizeLocalStorage } from '../ui/local-storage/use-storage-size-local-storage';
""",
    "Shop scale hook import"
)

page = replace_once(
    page,
    """    const [ compatibleOnly, setCompatibleOnly ] = useLocalStorage({ key: 'pkvault-shop-compatible-only', defaultValue: false });
""",
    """    const [ compatibleOnly, setCompatibleOnly ] = useLocalStorage({ key: 'pkvault-shop-compatible-only', defaultValue: false });
    const [ shopScaleRaw ] = useSpriteSizeLocalStorage('storage-sprite-size');
""",
    "Shop shared scale state"
)

page = replace_once(
    page,
    """    return <Box h='100%' p='xs' style={{ minHeight: 0, overflow: 'hidden' }}>
        <Stack h='100%' gap='xs' style={{ minHeight: 0 }}>
""",
    """    const shopScale = Math.max(1, shopScaleRaw);
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
    "Shop scaled workspace wrapper"
)

page = replace_once(
    page,
    """        </Stack>

        <Modal
""",
    """        </Stack>
        </Box>

        <Modal
""",
    "close Shop scaled workspace wrapper"
)

page = replace_once(
    page,
    """            title={mode === 'buy' ? 'Confirm purchase' : 'Confirm sale'}
            centered
        >
""",
    """            title={mode === 'buy' ? 'Confirm purchase' : 'Confirm sale'}
            centered
            styles={{ content: { zoom: shopScale } }}
        >
""",
    "scale Shop transaction modal"
)

page_path.write_text(page, encoding="utf-8")
print("PKVault V8 alpha51i shared Storage/Shop GUI scale applied")
