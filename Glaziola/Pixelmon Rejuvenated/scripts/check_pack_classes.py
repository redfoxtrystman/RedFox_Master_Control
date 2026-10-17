#!/usr/bin/env python3
"""Preflight Pixelmon Rejuvenated pack/JAR for missing own compiled classes.
Usage: python scripts/check_pack_classes.py path/to/mod.jar
       python scripts/check_pack_classes.py build/pack
This checks internal binary completeness, not compatibility with Minecraft APIs.
"""
from pathlib import Path
from zipfile import ZipFile
import re
import sys

PREFIX = "com/glaziola/pixelmonrejuvenated/"
REFERENCE = re.compile(rb"com/glaziola/pixelmonrejuvenated/[A-Za-z0-9_$/]+")

def inspect(target: Path):
    if target.is_dir():
        classes = {
            p.relative_to(target).as_posix(): p.read_bytes()
            for p in target.rglob("*.class")
        }
    else:
        with ZipFile(target) as archive:
            broken = archive.testzip()
            if broken:
                raise ValueError("ZIP CRC failure: " + broken)
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError("duplicate ZIP entries")
            classes = {n: archive.read(n) for n in names if n.endswith(".class")}
    own = {name for name in classes if name.startswith(PREFIX)}
    problems = []
    for caller, data in classes.items():
        if caller not in own:
            continue
        for match in REFERENCE.findall(data):
            symbol = match.decode("utf-8")
            expected = symbol + ".class"
            # Ignore package-directory names (e.g. .../mixin).
            if expected not in own and not any(p.startswith(symbol + "/") for p in own):
                problems.append((caller, expected))
    return own, sorted(set(problems))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/check_pack_classes.py <JAR or build/pack>")
    own, missing = inspect(Path(sys.argv[1]))
    print(f"Checked {len(own)} mod classes.")
    if missing:
        for caller, required in missing:
            print(f"ERROR: {caller} references missing {required}")
        raise SystemExit(1)
    print("PASS: All internal mod class references resolve.")
