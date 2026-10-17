# Alpha 48.3 — Temple pillar registry initialization hotfix

**Crash (2026-10-17 14:16:11):** `NoSuchFieldError: BuiltInRegistries.BLOCK` at `TemplePillarBlock.fractured()`, triggered when NeoForge bakes the pillar block-state cache.

**Root problem:** The old code queried the block's registry identity while registration was underway, using a field descriptor compiled against a stub with an incorrect Minecraft type. Fixing only that field descriptor would leave the underlying premature registry lookup.

**New architecture:** Normal pillars are `TemplePillarBlock`; fractured pillars are a concrete subtype `FracturedTemplePillarBlock`. `fractured()` checks `this instanceof FracturedTemplePillarBlock`, avoiding registry access entirely. The fractured deferred factory now constructs the subclass. Shape/cap/axis/waterlogging rules and all other features stay the same.

**Build:** Alpha 48.3 is a targeted Java 21 ASM class repair based on Alpha 48.2, **not** a full NeoForge Gradle build or a live game startup test. The only pre-existing JAR files changed are `TemplePillarBlock.class`, `ExtraPixelmonBlocks.class` and version metadata, plus new `FracturedTemplePillarBlock.class`. Static tests: 41 compiled classes present, 3,424 parseable JSON files, ZIP CRC and internal class refs valid. Further API incompatibilities are possible because prior builds used incomplete Minecraft stubs.

**Install:** Remove Alpha 48.2; install only `PixelmonRejuvenated-0.1.0-alpha.48.3-PILLAR-REGISTRY-INIT-HOTFIX-neoforge-1.21.1.jar`. No CobbleNav changes needed.

The full source/binary archive delivered in ChatGPT contains private Pixelmon-derived visual resources; these are not uploaded to the public repo without permission.
