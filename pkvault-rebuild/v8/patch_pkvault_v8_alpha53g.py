from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
shop = root / "PKVault.Core/shop/ShopService.cs"
text = shop.read_text(encoding="utf-8")

old = '        new("rare-candy", "Utilities", 5000, 2500),\n'
new = '        new("rare-candy", "Utilities", 20000, 10000),\n'

if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("alpha53g Rare Candy price anchor missing")

shop.write_text(text, encoding="utf-8")
print("PASS alpha53g Rare Candy price: buy 20000 / sell 10000")
