from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core" / "shop" / "ShopController.cs"
text = path.read_text(encoding="utf-8")
old = "[FromBody] "
if old not in text:
    raise RuntimeError("alpha51b expected ShopController FromBody markers were not found")
text = text.replace(old, "")
path.write_text(text, encoding="utf-8")
print("PKVault V8 alpha51b Shop controller binding fix applied")
