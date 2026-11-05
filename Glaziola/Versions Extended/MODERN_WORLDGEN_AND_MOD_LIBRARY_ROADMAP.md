# Versions Extended — Modern Overworld and Cross-Version Mod Compatibility

Status: Strategic roadmap, NOT implemented/verified.
Host: Forge Minecraft 1.12.2.
Reference: user-provided Minecraft Java 26.2 code and asset archives.
Order: finish 1.14 including live datapack tests; finish 1.15; repair the experimental 1.16; then continue chronological vanilla-version milestones. Research/prototypes of deeper engine changes may proceed in parallel but may not be treated as a completed feature.

## Strategic goals

1. Accurately reproduce modern 26.2 Overworld generation in 1.12.2, including mountains, rivers, biome placement, caves, aquifers, terrain elevation/depth, ores, structures and datapack-defined worldgen.
2. Develop a separate **Versions Extended Compatibility Library** to allow 1.12.2 to load mods targeting later Minecraft versions, ultimately 26.2. Emulate/remap modern APIs into working legacy or newly implemented engine equivalents with behavioral fidelity and test actual mods. Support for arbitrary modern JARs is an aspirational goal, **not currently proven possible**.
3. Preserve Forge 1.12.2 mod support, existing worlds, registry identities and existing VE modern-datapack compatibility.
4. The existing modded registry / flattening work and user's near-unlimited block/item ID solution must be inventoried as an explicit dependency. Do not assume all ID-limit mods can co-exist with modern world-height patches.

## World-height / terrain foundation: evaluate side mods first

Candidate: **OpenCubicChunks / CubicChunks for Forge 1.12.2** (open-source, MIT). It implements almost-unlimited vertical world height/depth and vertical 16x16x16 cube loading. Related **CubicWorldGen** supports custom cubic terrain generation. These are starting points for a host engine rather than turnkey implementations of exact modern 26.2 noise generation. Source: https://github.com/OpenCubicChunks/CubicChunks ; https://github.com/OpenCubicChunks/CubicWorldGen ; https://modrinth.com/mod/cubicchunks

**Critical compatibility hazard:** CubicChunks' official mod description warns that the combination with **JustEnoughIDs (JEID)** can irreversibly corrupt worlds after certain ID thresholds, and that other mods can break unexpectedly. Do not install or recommend a CC+JEID combination in an existing world. Source: https://modrinth.com/mod/cubicchunks and https://www.curseforge.com/minecraft/mc-mods/jeid

**Promising alternative for ID extension:** **Roughly Enough IDs (REID)** explicitly documents compatibility with CubicChunks 1.12.2-0.0.1208.0 and 1.12.2-0.0.1271.0 in its changelog. This is not a guarantee against other coremod interactions or proof that our current flattening implementation is compatible. Source: https://modrinth.com/mod/reid/

### Proof-of-concept gate (new disposable test world only)

- Identify exact ID-extension mod and version, registry patches in VE, serialization format, and JEID/REID/NEID present or absent. Record all block/item/biome ID thresholds and format mutations.
- Compare a clean 1.12.2 Forge + VE baseline; add CubicChunks and chosen ID patch to disposable fresh test instance only. Test above y=255, below y=0, chunk load/unload, block entities, lighting, rendering, pathfinding, redstone, world saves/reopens, dedicated server, and extended IDs. Back up worlds first and retain hash-verified baseline.
- Verify no interaction with JEID corruption threshold and no unsupported backward conversion. Prefer an isolated, genuinely compatible palette/ID serializer or adapter; never silently replace registry serializer in an established world.
- Implement correct finite modern range -64..319 first when needed, even if underlying engine supports much more. 1.12 assumes 0..255 in lighting, client packets, chunk storage, entities, world height, collision and rendering, so a compatible height mod can reduce but not necessarily eliminate our integration work.
- Inject the actual 26.2 terrain and cave generation pipeline on the adapted height/storage engine. CubicWorldGen vanilla-style presets are NOT identical to 26.2; noise/density, terrain surfaces, biomes, structures, features and data-driven generation require their own ports.
- Test datapack worldgen registry/codecs and boundaries with old 1.12 worlds. Avoid destructive world migrations. Record known unsupported interactions.

## Separate 26.2 mod-compatibility library: proposed subsystems

- Loader/metadata and dependencies: identify Fabric/NeoForge (or other selected modern loader) entrypoints, registries and dependencies, and present meaningful unsupported diagnostics.
- Namespace and bytecode bridge: modern class/member/field interfaces, mappings, method descriptors and transformation hooks, not merely name substitution.
- Semantic compatibility core: item data components, tags, dynamic registries, codecs, world/chunk/height APIs, entities and AI, resource/datapack reload, modern networking, client UI, renderer, shaders, and save formats.
- JVM bridge: address modern classfile version and Java APIs versus Java-8-era 1.12 Forge; use a supported Java runtime path and selective transformations with tests rather than promising universal bytecode downleveling.
- Loader-specific bridge: implement a deliberately chosen Fabric API or NeoForge subset; some Mixins target bytecode that does not exist on 1.12 and cannot simply be redirected without behavior reimplementation.
- Validation ladder: controlled remapped class -> simple content mod -> real datapack/content mod -> chosen loader mod -> mobs/worldgen/UI -> complex networked mod. Mark each target mod "compatible" only after functional tests on actual client and server.

## Release rules

1. Minecraft 26.2 is the behavioral source of truth for each backport regardless of introduction version.
2. No 1.15 work declared complete until 1.14 gameplay, GUI, AI, recipes and modern datapack support are verified.
3. No 1.16 declared complete until experimental Nether logic and mobs, structures, worldgen and AI have been audited against modern source and tested.
4. Never claim full arbitrary modern-mod support based on successful loading or remapping alone.
5. Report exact build/test evidence, incompatibilities, reproducible seeds and save safeguards. Maintain canonical `src/versions_extended_changelog_handoff.txt` inside VE source when source access is available.
