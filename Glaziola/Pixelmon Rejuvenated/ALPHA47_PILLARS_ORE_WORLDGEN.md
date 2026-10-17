# Pixelmon Rejuvenated — Alpha 47 (2026-10-17)

Target: Minecraft 1.21.1 / NeoForge 21.1.259 / Cobblemon 1.8.1 / Java 21.

## Temple pillar corrections

The older `temple_pillar` and `temple_pillar_fractured` were ordinary `RotatedPillarBlock`s with only `axis` variants. The Pixelmon reference has multipart blockstates, **six neighbor connection states** (`air`, `solid`, `pillar`), a shaft and separate cap models, plus separate fractured-end pieces.

- `TemplePillarBlock.java` now owns X/Y/Z axis state, six neighbor-facing state properties, waterlogging, placement and neighbor-change updates.
- Both pillar IDs use this block class, not a generic rotated cube. Opposing pillar ends now remove caps when same-axis neighboring pillars connect; caps remain on exposed normal ends and solid-supported fractured ends.
- Core dimensions 12×16×12 with 16×3×16 caps, rotated for X/Z. The raycast outline and collision shape use actual geometry, not a full 16×16×16 cube.
- `.noOcclusion()` prevents culling surrounding blocks as if the partial pillar occupied a full cube.
- Fractured edge hitboxes are approximations to the broken models; a comprehensive audit of all decorative block collision models is still pending.
- The original Pixelmon 9.4.1 multipart JSON definitions and missing `temple_pillar_cap_top`, `temple_pillar_cap_bottom`, `temple_pillar_fracture` models have been adapted in the local private build. **These derived third-party model files are not committed here.** They are in the private source ZIP and runtime JAR provided directly to the user. Run the local reference-model extraction script if reconstructing resources from the user-supplied JAR.

## Ruby, Sapphire, Crystal ore generation

Restored the original 9.4.1 generation mechanics with Rejuvenated registry identifiers only:

- Ruby: small (4 blocks, discard chance 0.5; 5 placement attempts), buried (8 blocks, 1.0; 4 attempts), large (8 blocks, 0.7; rarity 1/9). All use trapezoid height range bottom-80 to bottom+80.
- Sapphire: identical three vein types and distribution, but sapphire and deepslate sapphire block targets.
- Crystal: geode feature, with Crystal Ore inner shell, calcite middle, smooth basalt outer; rarity 1/24, height bottom+6 through Y=30.
- Three NeoForge biome modifiers add the placed features to `#minecraft:is_overworld` at `underground_ores`.
- Only `minecraft:stone_ore_replaceables` and `minecraft:deepslate_ore_replaceables` target tags are used for Ruby/Sapphire, so vanilla's normal stone/deepslate ore replacement remains intact.
- World generation applies to **new chunks**; pre-existing explored chunks are not retroactively repopulated.

## Verification and limits

The distributed Alpha 47 JAR was produced by compiling `TemplePillarBlock` with Java 21 signature stubs, patching the factory method handle in `ExtraPixelmonBlocks.class`, and re-packaging resources. It is **not a verified clean Gradle compilation or in-game startup test**. Internal class completeness, archive CRCs, parsed JSONs, 17 worldgen definitions and cross-referenced features were statically validated. Those tests cannot establish that NeoForge loads all resources or that the pillar behavior works in-game.

The private Pixelmon 9.4.1 JAR itself and extracted graphical assets have not been published on GitHub due to redistribution restrictions.
