# Alpha 48.4 — Restore full-block Temple Pillar hitboxes

**User report:** When a pillar was standing alone, its top-cap selection/collision shape was inaccurate; attached pillars changed the shape, and horizontal pillars were also inconsistent. The requested behavior is the **previous full-block hitbox**, not model-accurate shaft/cap outlines.

## Change

In `TemplePillarBlock.java`, both `getShape(...)` and `getCollisionShape(...)` now directly return `Shapes.block()`, which covers an entire 16×16×16 block. The specialized `pillarShape` helper is no longer called by these two overrides. The `FracturedTemplePillarBlock` subclass inherits the same behavior.

This is independent of pillar rotation, neighbor connections, caps, or fractured type. It changes **collision and selection only**, not rendered models, culling flags, cap attachment models, waterlogging, any other block's hitbox, berry trees or gemstone world generation.

## Validation

The private Alpha 48.4 runtime JAR was produced by changing only the two shape methods in the already-working Alpha 48.3 compiled class using Java 21 ASM. `javap` confirms each method directly invokes `Shapes.block()` then returns. JAR diff against 48.3 shows only `TemplePillarBlock.class` and `META-INF/neoforge.mods.toml` changed. All 41 mod classes are packaged, the 3,424 JSON files parse, internal class references resolve, and ZIP CRC/uniqueness checks pass.

**Limit:** No Minecraft/NeoForge startup or in-world placement test was performed, and this remains a targeted bytecode hotfix, not a clean Gradle build. The complete private source ZIP includes a reproducible `scripts/PatchTemplePillarFullHitbox.java` helper; third-party Pixelmon-derived assets are not mirrored publicly.

## Installation

Remove the Alpha 48.3 JAR, install only `PixelmonRejuvenated-0.1.0-alpha.48.4-FULL-PILLAR-HITBOX-neoforge-1.21.1.jar` on Minecraft 1.21.1/NeoForge 21.1.259/Cobblemon 1.8.1.
