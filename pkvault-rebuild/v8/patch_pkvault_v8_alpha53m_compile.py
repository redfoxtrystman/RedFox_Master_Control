from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/shop/EvolutionItemShopService.cs"
text = path.read_text(encoding="utf-8")

if "using PKHeX.Core;" not in text:
    text = "using PKHeX.Core;\n\n" + text

old = ".Select(version => (int)version.Generation)"
new = ".Select(version => (int)((GameVersion)version).Generation)"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("alpha53m compile fix generation anchor missing")

path.write_text(text, encoding="utf-8")
print("PASS alpha53m compile fix: evolution item version bytes -> GameVersion generation")
