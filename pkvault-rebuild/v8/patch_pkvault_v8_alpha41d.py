from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/router/RouteJsonContext.cs"
text = path.read_text(encoding="utf-8")

old = "[JsonSerializable(typeof(QuestAchievementDTO))]"
new = "[JsonSerializable(typeof(QuestEntryDTO))]"

if old not in text:
    if new in text:
        print("PKVault V8 alpha41d quest JSON context already updated")
        raise SystemExit(0)
    raise RuntimeError("alpha41d QuestAchievementDTO JSON context anchor missing")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PKVault V8 alpha41d quest JSON source generation fix applied")
