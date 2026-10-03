from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def rep(path: str, old: str, new: str, label: str):
    p = root / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            print(f"ALREADY {path}: {label}")
            return
        raise RuntimeError(f"alpha53m anchor not found: {label} in {path}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"PATCHED {path}: {label}")


# Shop category icons were being rendered with a sprite multiplier larger than
# their fixed icon box. That made the inner sprites clip against the 38 px
# category rows. Scale ItemIcon to the actual requested box size and give the
# category list a little extra padding.
rep(
    "frontend/src/shop/shop-page.tsx",
    "            '--sprite-item-size-multiplier': size >= 42 ? '2.15' : '1.55',\n",
    "            '--sprite-item-size-multiplier': String(size / 32),\n",
    "fit shop sprites to ItemIcon box",
)
rep(
    "frontend/src/shop/shop-page.tsx",
    "                                ? <ItemIcon item={categoryIconItem(iconKey, items)} size={26} />\n",
    "                                ? <ItemIcon item={categoryIconItem(iconKey, items)} size={22} />\n",
    "shrink category icons",
)

# Gen I's historical Elixer/Max Elixer records deliberately keep their old
# spelling in static data, but those records have no sprite path. Borrow the
# canonical modern Elixir textures just like the existing Gen II Apricorn
# sprite aliases while preserving the original item IDs and display names.
rep(
    "frontend/src/hooks/use-static-data.ts",
    '''            // Gen 2's PKHeX/static-data item keys use six abbreviated Apricorn
            // identifiers (WHT/BLU/GRN/PNK/YLW/BLK). Their records have no
            // sprites even though the modern full-name Apricorn records do.
            // Keep the Gen 2 name/id, but borrow the canonical colour sprite.
            const apricornSpriteAliases: Record<string, string> = {
                'blk-apricorn': 'black-apricorn',
                'blu-apricorn': 'blue-apricorn',
                'grn-apricorn': 'green-apricorn',
                'pnk-apricorn': 'pink-apricorn',
                'wht-apricorn': 'white-apricorn',
                'ylw-apricorn': 'yellow-apricorn',
            };
            const spriteAlias = apricornSpriteAliases[key];
''',
    '''            // Some older PKHeX/static-data keys have no sprite of their own.
            // Keep their original item name/id, but borrow the matching modern
            // canonical texture. This covers Gen 2's abbreviated Apricorn keys
            // and Gen 1's historical Elixer / Max Elixer spellings.
            const itemSpriteAliases: Record<string, string> = {
                'blk-apricorn': 'black-apricorn',
                'blu-apricorn': 'blue-apricorn',
                'grn-apricorn': 'green-apricorn',
                'pnk-apricorn': 'pink-apricorn',
                'wht-apricorn': 'white-apricorn',
                'ylw-apricorn': 'yellow-apricorn',
                'elixer': 'elixir',
                'max-elixer': 'max-elixir',
                'max-elixir-(~)': 'max-elixir',
            };
            const spriteAlias = itemSpriteAliases[key];
''',
    "Gen I Elixer sprite aliases",
)

# The common elemental stones are meant to remain affordable after discovery.
# Keep the permanent first-obtained unlock from alpha53l, but restore these four
# basic stones to ₽5,000 buy / ₽2,500 sell. Thunder Stone is the Electric stone.
for key in ("fire-stone", "water-stone", "thunder-stone", "leaf-stone"):
    rep(
        "PKVault.Core/shop/ShopService.cs",
        f'        new("{key}", "Evolution Items", 12_000, 6_000, false, true),\n',
        f'        new("{key}", "Evolution Items", 5_000, 2_500, false, true),\n',
        f"{key} price",
    )

print("PASS alpha53m shop category sizing + basic stone prices + Elixer sprites")
