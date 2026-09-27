from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "frontend/src/shop/shop-page.tsx"
text = path.read_text(encoding="utf-8")

old = """                <Stack gap='xs' style={{ flex: 1, minWidth: 0, minHeight: 0 }}>
                    <Group wrap='nowrap' gap='sm'>
"""
new = """                <Stack gap='xs' style={{ flex: 1, minWidth: 0, minHeight: 0 }}>
                    <Group wrap='nowrap' gap='sm' pt={4}>
"""
if old not in text:
    raise RuntimeError("alpha51g Shop filter-row offset anchor not found")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PKVault V8 alpha51g Shop filter-row seam removed")
