from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/contract/ContractService.cs"
text = path.read_text(encoding="utf-8")

old = """                if (pair.Length == 3 && ushort.TryParse(pair[0], out var species) && int.TryParse(pair[1], out var level))
                    state.Pokemon[key[4..]] = new(species, Math.Max(1, level), pair[2] == "1");
"""
new = """                if (pair.Length == 3 && ushort.TryParse(pair[0], out var pkmSpecies) && int.TryParse(pair[1], out var level))
                    state.Pokemon[key[4..]] = new(pkmSpecies, Math.Max(1, level), pair[2] == "1");
"""
if old not in text:
    raise RuntimeError("alpha52b ContractService species parser anchor not found")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PKVault V8 alpha52b contract tracker parser compile fix applied")
