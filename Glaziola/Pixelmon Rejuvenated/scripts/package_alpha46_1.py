#!/usr/bin/env python3
"""Package repaired compiled class pack. Run RepairMinecraftComponentLinks first."""
from pathlib import Path
import zipfile, json, subprocess
root = Path(__file__).resolve().parents[1]
pack = root/'build/pack'
out = root/'dist/PixelmonRejuvenated-0.1.0-alpha.46.1-COMPONENT-HOTFIX-neoforge-1.21.1.jar'
out.parent.mkdir(parents=True,exist_ok=True)
assert (pack/'com/glaziola/pixelmonrejuvenated/StoneEquipment.class').exists()
assert '0.1.0-alpha.46.1' in (pack/'META-INF/neoforge.mods.toml').read_text()
files = sorted(p for p in pack.rglob('*') if p.is_file())
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:
        z.write(p,p.relative_to(pack).as_posix())
with zipfile.ZipFile(out,'r') as z:
    assert z.testzip() is None
    assert len(set(z.namelist()))==len(z.namelist())
    assert z.read('META-INF/neoforge.mods.toml').count(b'0.1.0-alpha.46.1')==1
    assert z.read('com/glaziola/pixelmonrejuvenated/StoneEquipment.class')
print(f'Built: {out}, entries={len(files)}')
