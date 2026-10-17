#!/usr/bin/env python3
"""Regenerate all 30 Berry Wood Plank recolor recipes for 1.21.1.

Run from the Pixelmon Rejuvenated source directory:
python scripts/generate_berry_plank_recipes.py
"""
from pathlib import Path
import json

COLORS = ("green", "yellow", "red", "blue", "pink", "purple")
OUT = Path(__file__).resolve().parent.parent / "src/main/resources/data/pixelmonrejuvenated/recipe"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for color in COLORS:
        (OUT / f"{color}_berry_wood_planks_dyed.json").unlink(missing_ok=True)
    created = 0
    for source in COLORS:
        for target in COLORS:
            if source == target:
                continue
            data = {
                "type": "minecraft:crafting_shaped",
                "category": "building",
                "group": f"pixelmonrejuvenated:berry_wood_planks_{target}",
                "pattern": ["PPP", "PDP", "PPP"],
                "key": {"P": f"pixelmonrejuvenated:{source}_berry_wood_planks",
                        "D": f"minecraft:{target}_dye"},
                "result": {"id": f"pixelmonrejuvenated:{target}_berry_wood_planks", "count": 8},
            }
            path = OUT / f"{target}_berry_wood_planks_from_{source}.json"
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            created += 1
    print(f"Generated {created} Berry Wood Plank recolor recipes.")

if __name__ == "__main__":
    main()
