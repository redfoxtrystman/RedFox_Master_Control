# Pixelmon Rejuvenated — Alpha 46.3.1 (2026-10-17)

Target Minecraft 1.21.1 / NeoForge 21.1.259 / Cobblemon 1.8.1.

## Essential correction: do not compete with Cobblemon's apricorn plank recipe

User correctly identified that Cobblemon **already converts apricorn logs into apricorn planks**.

Alpha 46.2 additionally supplied a recipe consuming `cobblemon:apricorn_log` to produce `pixelmonrejuvenated:yellow_berry_wood_planks`. That recipe used a distinct ID but matched the same input as Cobblemon's own recipe, causing competing outputs.

Alpha 46.3.1 removes `data/pixelmonrejuvenated/recipe/yellow_berry_wood_planks.json` entirely. The replacement recipe is `yellow_berry_wood_planks_dyed.json`, using 8 Rejuvenated green planks and yellow dye. The **original Cobblemon apricorn-plank conversion remains untouched**.

The Rejuvenated color progression is:
1. `pixelmonrejuvenated:berry_log` → 4 `pixelmonrejuvenated:green_berry_wood_planks`.
2. 8 green planks surrounding 1 yellow dye → 8 yellow Berry Wood Planks.
3. 8 yellow planks + the matching red, blue, pink or purple dye → 8 matching planks.
4. Optional 8 yellow planks + green dye → 8 green planks.

Removed the four legacy duplicate dye recipes with obsolete ingredient syntax.

## Other fixes incorporated in Alpha 46.3.1

- Added 38 Ruby, Sapphire and Crystal English translation entries: material items, all registered tools/armor and all ore/storage blocks. The complete updated `en_us.json` is in the supplied full-source ZIP.
- Added both durability and attack attributes to 60 evolution-stone tools and 18 Ruby/Sapphire/Crystal tools. The compiled source had `new Item.Properties()` without required 1.21.1 item attribute components. Vanilla `SwordItem.createAttributes` and `DiggerItem.createAttributes` are used.
- Added a small 12 × 4 × 12 voxel outline in `UltraDecorativePlantBlock` for the Ultra Forest Flower rather than a full-cube targeting shape. The file is used by this one block in current project registration.
- Preserved all 46.1 linkage and 46.2 missing-class fixes.

## Build status and caveats

The JAR distributed in the ChatGPT conversation was packaged from the previous 46.2 JAR with **three Java 21 ASM bytecode repairs**, JSON/lang recipe corrections and version bump. This is **not a clean Gradle compile** and the runtime client was not available for a launch test. Verified ZIP CRC, class count (32), 3,377 valid JSON resources and that our recipes no longer reference native Cobblemon apricorn logs or planks.

The complete source ZIP contains third-party Pixelmon artwork for private local use and is NOT mirrored publicly without permission. GitHub includes the shareable Java source and recipe examples. Project packaging must not regenerate the removed apricorn-log conversion recipe. Natural Ruby/Sapphire/Crystal ore generation and specialized Pixelmon hammer behavior remain future work.
