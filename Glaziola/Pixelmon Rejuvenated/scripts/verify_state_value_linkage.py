#!/usr/bin/env python3
"""Fail if compiled Rejuvenated classes contain the known bad Minecraft 1.21.1 setValue descriptor."""
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile
import tempfile

bad = "BlockState.setValue:(Lnet/minecraft/world/level/block/state/properties/Property;Ljava/lang/Comparable;)Lnet/minecraft/world/level/block/state/BlockState;"
def check(classes):
    wrong = []
    for file in classes.rglob("*.class"):
        if "/com/glaziola/pixelmonrejuvenated/" not in file.as_posix():
            continue
        output = subprocess.run(["javap", "-p", "-c", str(file)], text=True, capture_output=True, check=True).stdout
        if bad in output:
            wrong.append(str(file))
    if wrong:
        print("ERROR: invalid Minecraft JVM signatures:\n" + "\n".join(wrong),file=sys.stderr)
        return 1
    print("PASS: no BlockState.setValue():BlockState references remain.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/verify_state_value_linkage.py <JAR or build/pack>")
    arg = Path(sys.argv[1]).resolve()
    if arg.is_file():
        with tempfile.TemporaryDirectory() as t:
            with ZipFile(arg) as z:
                for n in z.namelist():
                    if n.startswith("com/glaziola/pixelmonrejuvenated/") and n.endswith(".class"):
                        z.extract(n, t)
            raise SystemExit(check(Path(t)))
    raise SystemExit(check(arg))
