from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/quest/routes/QuestRoute.cs"
text = path.read_text()
old = "[FromBody] QuestRerollRequest request"
new = "QuestRerollRequest request"
if old not in text:
    raise RuntimeError("alpha42b reroll route binding anchor not found")
path.write_text(text.replace(old, new, 1))
print("PKVault V8 alpha42b reroll body binding compile fix applied")
