from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/quest/QuestService.cs"
text = path.read_text()
old = "DexTarget: Math.Max(1, save.MaxSpeciesID)"
new = "DexTarget: Math.Max(1, (int)save.MaxSpeciesID)"
if old not in text:
    raise RuntimeError("alpha42c MaxSpeciesID compile-fix anchor not found")
path.write_text(text.replace(old, new, 1))
print("PKVault V8 alpha42c MaxSpeciesID compile fix applied")
