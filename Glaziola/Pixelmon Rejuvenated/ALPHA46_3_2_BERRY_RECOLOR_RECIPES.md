# Alpha 46.3.2 — Any Berry Planks to Any Other Color

The user requested bidirectional dyeing between **all six** Berry Wood Plank colors, not only recoloring yellow planks. Source colors: green, yellow, red, blue, pink and purple.

- For each different pair (source, target), craft **8 source-color planks** in a 3x3 ring with **1 target-color dye** at center; output **8 target-color planks**.
- There are **30 recipes** = 6 source colors x 5 different destination colors. No same-color dye recipe.
- Sample: 8 `pixelmonrejuvenated:green_berry_wood_planks` + 1 `minecraft:red_dye` -> 8 `pixelmonrejuvenated:red_berry_wood_planks`.
- Existing `berry_log` -> 4 green plank recipe is preserved.
- Remove six old `*_berry_wood_planks_dyed.json` recipes (which only supported yellow-based recolors), replacing with explicitly named `<target>_berry_wood_planks_from_<source>.json` recipes.
- Every file uses the proper shaped-recipe JSON format for Minecraft 1.21.1, with matching group key per result color.
- **Do not touch Cobblemon apricorn logs/planks or any Cobblemon recipes.** Neither the new inputs nor outputs reference `cobblemon`.
- Generator: `scripts/generate_berry_plank_recipes.py` can regenerate all thirty combinations.

## Validation

46.3.2 is a **resource-only repack of 46.3.1** with a version bump, not a full recompilation. Both delivered ZIP/JAR archives pass ZIP CRC, uniqueness, all-JSON parsing and all 30 input->output pair assertions. The JAR retains 32 compiled classes; NeoForge in-game startup and crafting UI **have not been tested here**.

The full mod JAR/source ZIP contain user-supplied Pixelmon-derived artwork. They were provided directly to the user but **not committed to public GitHub** pending redistribution permission. This public commit contains only Java-independent original recipes, the generator, documentation, and build metadata.
