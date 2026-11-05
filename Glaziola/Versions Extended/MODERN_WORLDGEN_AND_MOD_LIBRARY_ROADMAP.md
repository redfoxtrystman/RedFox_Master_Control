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

## Owner-selected dependency architecture (2026-11-05)

**Do not use CubicChunks or CubicWorldGen.** The owner rejects CubicChunks for performance/optimization reasons. VE must use the following existing mods as independent runtime components, avoiding duplicate or conflicting features:

| Existing external dependency | Responsibility | Project/source |
| --- | --- | --- |
| **Cave Biomes API / CaveBiomesAPI** | Configurable finite signed-Y world height, 3D/vertical biome resolution, extended chunk sections and compatible rendering | https://github.com/Vendetta1871/CaveBiomesAPI |
| **Nether API** | Nether biomes, generation integration, associated structures and atmospheric/ambient behavior; also includes End functionality, though Nether is the VE priority | https://github.com/jbredwards/Nether-API |
| **Aqua Acrobatics** | Modern swimming, crawling and movement animations/poses; use the working mod instead of duplicating swimming or independently replacing it | https://github.com/embeddedt/aquaacrobatics |
| **User's existing ID-extension / flattening components** | Expanded block/item registry capacity, existing VE flat IDs and save/registry compatibility | Exact mod name/build not yet verified; inspect before altering |

### CaveBiomesAPI integration

- The project's public README documents `WorldHeightAPI.getMinY()`, `getMaxY()`, `BiomeLayerAPI.register(...)`, and `ExtendedChunkAPI.requireRange(...)` / `setBlockState(...)`. The library's configurable limits can target **Y=-64..319** via `minY=-64`, `maxY=320` (exclusive upper bound).
- CaveBiomesAPI is an infrastructure layer, **not** a complete 26.2 generator. VE must implement 26.2 climate/noise, caves, aquifers, ore distribution, surfaces, biomes, structures, features and datapack worldgen semantics against the supplied 26.2 reference code. Do not mix in the old 1.12 biome generator for data that needs genuine Y-aware resolution.
- Confirm compatibility with the exact user-installed ID-extension/flattening patch, server and client renderers, signed-Y storage, chunk NBT, lighting, entity and AI height checks, world migration and dedicated-server sync. Verify load/save performance in fresh disposable test worlds and ensure existing worlds retain generator identity.
- CaveBiomesAPI's biome providers should be side-effect-free and deterministic. Its README notes `Chunk.blockBiomeArray` remains a vanilla projection, so VE must not assume persisted 3D biome identities without implementing an appropriate virtual resolver/persistence strategy.
- CaveBiomesAPI is GPL-3.0: retain it as an external dependency and review licensing before copying any code.

### Nether API integration for accurate Nether generation

- Use Nether API's registry/events, biome weighting, surfaces/populators, fog, music, ambient particles/sounds, structure support and relevant dimension settings rather than implementing a competing biome framework.
- Its public description documents `NetherAPIRegistryEvent`, `NetherAPIFogColorEvent`, `BiomeAmbienceEvent`, custom surface builders and chunk populators. Determine exactly which exposed interfaces are usable in the **pinned runtime version**.
- 1.16 Nether work must audit modern **26.2** Nether biome selection, generation, basalt deltas, soul sand valleys, crimson/warped forests, spawn rules, structures and mob AI; registering biome names alone is not enough.
- Inspect Nether API's existing optional **256-block-tall Nether** setting before selecting a dimension-height strategy, and coordinate any height patches with CaveBiomesAPI rather than assuming they stack correctly. No old-world Nether height conversion without user approval and backups.
- Nether API has its own distribution/license conditions; don't redistribute its JAR without checking permission.

### Aqua Acrobatics integration for swimming and movement

- **Do not re-port swimming as a second independent player-movement implementation.** Use the installed Aqua Acrobatics behavior/animations as the baseline, preserving swimming/crawling/eye height/collision behavior and compatibility with relevant 1.12 mods.
- Disable, remove or reconcile duplicate VE movement patches after verifying they don't conflict with Aqua Acrobatics; perform mod-with-mod tests on client and dedicated server.
- **First-person trident viewmodel/charging pose — FIXED (owner-confirmed, 2026-11-05).** Earlier incorrect camera-side raised position and animation are already resolved. Do not schedule a new renderer rewrite; protect the established correction with regression checks during Aqua Acrobatics or rendering changes. Other trident mechanics should be tested independently only where not already verified.
- Retain regression coverage for trident throw/loyalty/channeling/riptide physics and any renderer-mod interactions when those subsystems are changed. Do not confuse this general compatibility testing with an unfinished first-person trident pose fix.
- Use the existing original Aqua Acrobatics release unless the owner explicitly identifies a particular fork/update. Do not silently replace it with an unofficial continuation.

### Integration and sign-off gate

1. Obtain exact JAR/mod versions and source snapshot; inspect installed Mixins/coremods, Forge and MixinBootstrap versions.
2. Verify the **1.14 milestone and existing modern datapack support** before advancing to 1.15. The dependency selection doesn't waive validation requirements.
3. Test CaveBiomesAPI, Nether API and Aqua Acrobatics separately, in combinations, and alongside VE plus the current ID extender; record conflicts and performance.
4. For modern 1.16 Nether and eventual modern Overworld generator, validate identical seeded generation behavior where possible, AI, renderer, structure placement and world saves. Never label a feature complete based only on registration/compilation.
5. Keep all three as explicit, independently tracked dependencies in the **canonical** `src/versions_extended_changelog_handoff.txt` once working VE source is accessible.

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
