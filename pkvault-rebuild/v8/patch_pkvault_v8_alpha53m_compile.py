from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/shop/EvolutionItemShopService.cs"
text = path.read_text(encoding="utf-8")
old = "                .Select(version => (int)version.Generation)\n"
new = "                .Select(version => (int)(others.Versions.GetValueOrDefault(version)?.Generation ?? 1))\n"
if new not in text:
    if old not in text:
        raise RuntimeError("alpha53m compile-fix anchor missing")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PASS alpha53m evolution item generation lookup compile fix")
