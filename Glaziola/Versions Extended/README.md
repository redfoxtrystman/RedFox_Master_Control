# Versions Extended — development handoff

**Project:** Versions Extended
**Target:** Minecraft Forge 1.12.2 (LegacyForge)
**Behavioral and asset reference:** Minecraft 26.2
**Current milestone:** Minecraft 1.14 Village & Pillage — **not yet signed off**
**Next milestone:** Minecraft 1.15 Buzzy Bees — **do not start until 1.14 passes review**
**Archive inventory:** [REFERENCE_ARCHIVES_2026-10-17.md](REFERENCE_ARCHIVES_2026-10-17.md)

## Binding development ground rules

1. **Review the user-supplied Minecraft 26.2 decompiled source and matching assets before implementing or correcting any vanilla behavior.** Find the actual 26.2 implementation and compare mechanics, state, rendering, model, textures, GUI, recipes, loot, spawning, AI, sounds, data layout, and version-dependent changes as applicable. Do not guess or rely solely on old 1.14 tutorials.
2. **Backport the 26.2 form of each feature immediately.** Content belongs to its original update's VE configuration/creative category, but its behavior should match the modern 26.2 form, including later vanilla revisions. No temporary historic 1.14 imitation followed by repeated rework in later release passes.
3. **Make 1.12.2 able to consume contemporary Minecraft datapacks to the greatest feasible extent.** Preserve namespaced IDs, tags, JSON recipes, advancements, loot tables, functions, data-driven registries/worldgen and relevant modern schema/pack-format version handling. Existing datapack support is a partial foundation, **not blanket full modern datapack compatibility**. Implement and test the adapters needed for modern packs rather than telling users to rewrite every pack for 1.12.2.
4. **Finish and validate all 1.14 content before proceeding to 1.15.** Review code and assets for parity, add missing features, compile, test in-game, and record remaining limitations truthfully.
5. **Preserve backward compatibility for native Forge 1.12.2 and currently supported mods/worlds.** Avoid removing established content, breaking registries/saves, changing canonical IDs without migration, or silently swapping reference assets.
6. **Respect the existing architecture.** Maintain per-update config controls, shared modern-ID/block-state compatibility, and reuse canonical systems. The long-term `Mods_Extended` multi-generation mod-loader idea is a future architecture target, **not an implemented guarantee and not a detour from 1.14 parity**.
7. **Always read the canonical source-tree handoff** at `src/versions_extended_changelog_handoff.txt` and update that **same file** in future development passes. Do not scatter revision-numbered replacement handoff documents within `src/`.
8. **No unverified completion claims.** Code seen in the archive is not proof of functioning gameplay. For a fix: trace official 26.2 reference -> inspect current implementation -> edit -> compile/test where possible -> record concrete results and gaps.

## 2026-10-17 uploaded source snapshot — observed, not a compile certificate

The user supplied `Versions-Extended-1.12.2.zip`, whose ZIP integrity test passed. It contains a complete working project layout, including `build.gradle`, `gradlew`, `gradle.properties`, `settings.gradle`, `src/`, and **unnecessary generated** `build/` and `.gradle/` folders.

Inside `src/`: **627 Java files**, including **137 under `com/versionsextended/v1_14/`**, **42 under `com/versionsextended/datapack/`**, and **7,266 resource files**. The embedded changelog/handoff is about 184 KB.

Examples of implemented 1.14 areas to audit rather than assuming finished: bamboo, barrels, bells, campfires, composters, grindstones, lecterns, lanterns, scaffolding, signs, workstations, crossbows, cats, foxes, pandas, pillagers, ravagers, wandering traders, patrols/outposts, and their renderers.

Existing datapack groundwork includes recipe registries/bridges, modern item/block ID resolvers, modern tag support, loot table support, function/command support, advancement support, and early biome/structure handling. **Each needs specific tests against actual modern packs.**

## 1.14 completion gate

- Compare complete Village & Pillage feature inventory against the 26.2 decompile/assets; document missing blocks, items, entities, worldgen, structures, effects, UI and mechanics.
- Validate each added block's item/block model, light/shading, bounding/selection shapes, orientation, waterlogging where applicable, creative placement, sounds, loot, and expected recipes.
- Verify existing problem areas tracked in the source handoff, notably workstation GUIs/models, grindstone/smooth-stone brightness, sign placement, vegetation shape alignment, scaffolding targeting/crouching, pillager patrol/captain/outpost behavior, and riptide + elytra handling. Treat earlier fixes as **candidates requiring runtime confirmation**, not automatically solved.
- Audit commands/tags/datapack translation and modern recipe inputs/results across survival, server, and client. Confirm save/load, datapack reload, error reporting, and compatibility with ordinary 1.12.2 Forge mods.
- Run a repeatable Gradle build and Minecraft 1.12.2 in-game smoke tests, record exact results, and only then mark 1.14 complete.

## After the 1.14 gate

Begin 1.15 Buzzy Bees using 26.2 parity for bees, hives/nests, honey/honeycomb, honey blocks, breeding/pollination, mechanics, advancements, block behavior and any other 1.15 changes found by comparing authoritative sources; do not assume the update is *only* bees.

## Reference handling and source retention

The three original user-provided archives are listed with exact hashes in the linked inventory. **They are NOT stored in this public GitHub repository.** This handoff and checksum inventory preserve identification, architecture, constraints and next actions; they do **not** replace access to the original archives or the source-tree changelog. Source work in future chats requires that the project source and Mojang references be available in the working session. Do not place Mojang's decompiled source or entire copyrighted asset archives in a public GitHub commit.
