# Alpha 48.2 — Fluid JVM linkage hotfix (2026-10-17)

The 14:08:55 crash report for Alpha 48.1 shows:

    java.lang.NoSuchFieldError:
      net.minecraft.world.level.material.Fluids.WATER
      expected descriptor: Lnet/minecraft/world/level/material/Fluid;
    at TemplePillarBlock.getFluidState(TemplePillarBlock.java:111)

**Cause:** Alpha 48.1 compiled TemplePillarBlock against an incomplete Minecraft API stub. Minecraft 1.21.1 declares \`Fluids.WATER\` as \`FlowingFluid\`, not \`Fluid\`. The same compiled class also invoked \`Fluid.getSource(boolean)\`; the real method is declared by \`FlowingFluid\`. Fixing only the reported field would have caused a subsequent \`NoSuchMethodError\`.

**Alpha 48.2 repair:** Four \`Fluids.WATER\` field descriptors and one \`getSource(boolean)\` method owner patched in \`TemplePillarBlock.class\`. Java source already uses a valid Java expression; compiling it against **actual** Minecraft/NeoForge dependencies is the sustainable fix.

**Validation:** Inspected all 40 compiled mod classes with \`javap\`: no remaining known \`Fluids.WATER:Fluid\`, \`Fluid.getSource\`, or invalid \`BlockState.setValue(...):BlockState\` references. The only runtime JAR changes relative to Alpha 48.1 are \`TemplePillarBlock.class\` and \`META-INF/neoforge.mods.toml\` version metadata. JAR has 4,152 entries and 3,424 parseable JSON files. ZIP CRC and duplicate-file checks passed.

**Limitations:** This is a Java 21 bytecode correction/repack, **not** a clean Gradle build and **not** validated in a running Minecraft client. Prior releases were generated against stubs, so further binary mismatches may still emerge.

**Installation:** Remove Alpha 48.1; install only Alpha 48.2 on Minecraft 1.21.1 / NeoForge 21.1.259 / Cobblemon 1.8.1. Do not remove or modify CobbleNav for this crash.

Java 21 script: \`scripts/PatchFluidLinkage.java\` uses JDK-included ASM with \`--add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED\` and \`--add-exports java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED\`.

The full mod JAR and complete source snapshot remain private downloadable conversation artifacts because the pack contains Pixelmon-derived assets; these assets are not mirrored publicly without redistribution rights.