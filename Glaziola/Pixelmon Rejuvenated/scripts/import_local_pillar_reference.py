#!/usr/bin/env python3
"""Install only the temple-pillar model definitions from a locally supplied Pixelmon 9.4.1 JAR.
No proprietary original models/JAR are checked into GitHub.
Usage: python scripts/import_local_pillar_reference.py path/to/Pixelmon-1.21.1-9.4.1-universal.jar
"""
import json,sys,zipfile
from pathlib import Path
z=zipfile.ZipFile(sys.argv[1])
base=Path(__file__).resolve().parent.parent/"src/main/resources/assets/pixelmonrejuvenated"
paths=[
 "blockstates/temple_pillar.json","blockstates/temple_pillar_fractured.json",
 "models/block/temple_pillar_cap_top.json","models/block/temple_pillar_cap_bottom.json",
 "models/block/temple_pillar_fracture.json",
]
for tail in paths:
    raw=z.read("assets/pixelmon/"+tail)
    value=json.loads(raw)
    def convert(o):
        if isinstance(o,dict):return {k:convert(v) for k,v in o.items()}
        if isinstance(o,list):return [convert(v) for v in o]
        if isinstance(o,str) and o.startswith("pixelmon:"):return "pixelmonrejuvenated:"+o[len("pixelmon:"):]
        return o
    path=base/tail;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(convert(value),indent=2)+"\n",encoding="utf-8")
    print(path)
