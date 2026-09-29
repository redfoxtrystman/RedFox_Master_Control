from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

identity = root / "PKVault.Core/progression/ProgressionPkmIdentity.cs"
text = identity.read_text(encoding="utf-8")
if "using PKHeX.Core;" not in text:
    anchor = "using System.Globalization;\n"
    if anchor not in text:
        raise RuntimeError("alpha53d compile fix: identity using anchor missing")
    text = text.replace(anchor, anchor + "using PKHeX.Core;\n", 1)
identity.write_text(text, encoding="utf-8")

evolution = root / "PKVault.Core/storage/services/EvolutionService.cs"
text = evolution.read_text(encoding="utf-8")
old = "        var currentFormId = pkm.Species;\n"
new = "        var currentFormId = (int)pkm.Species;\n"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("alpha53d compile fix: currentFormId anchor missing")
evolution.write_text(text, encoding="utf-8")

print("PASS alpha53d compile fixes")
