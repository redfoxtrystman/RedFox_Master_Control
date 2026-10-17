# Alpha 48.1 — Crash fix: wrong Minecraft BlockState JVM return descriptor

The Alpha 48 crash report (2026-10-17 14:04:23) shows:

```
java.lang.NoSuchMethodError:
net.minecraft.world.level.block.state.BlockState
  net.minecraft.world.level.block.state.BlockState.setValue(
    net.minecraft.world.level.block.state.properties.Property, java.lang.Comparable)
at com.glaziola.pixelmonrejuvenated.TemplePillarBlock.<init>(TemplePillarBlock.java:47)
```

This crash is caused by Pixelmon Rejuvenated's compiled class, not CobbleNav. The additional "unbound value: pixelmonrejuvenated:temple_pillar" failure follows because registry initialization aborted.

**Root cause:** Java 21 classes built against Minecraft signature stubs were linked to `BlockState.setValue(Property,Comparable):BlockState`, but the actual Minecraft 1.21.1 method's erased descriptor is `(Property,Comparable)Object`. This descriptor was independently confirmed with `javap` from the user-supplied official Pixelmon 9.4.1 binary; that code invokes the method with `Object` return and `CHECKCAST BlockState`.

**Targeted fix:** Alpha 48.1 repairs **13 sites in TemplePillarBlock.class and 7 in BerryTrees.class**, a total of **20 faulty calls**, adding the explicit `CHECKCAST` after each rewritten invocation. All other game functionality and compiled classes are preserved, including Alpha 48 natural berry trees and earlier Alpha 47 temple pillar/worldgen.

**Checks:** Verified the bytecode of all 40 mod classes with `javap`; checked every rewritten invocation is followed by `checkcast BlockState`. The resulting JAR has 4,152 entries and 3,424 JSONs, all valid; ZIP CRC and uniqueness checks pass. Source ZIP is provided with the private binary in the ChatGPT conversation.

**Limits:** Not a clean Gradle build and **not tested by launching NeoForge/Minecraft**. The Java source can be compiled using actual Minecraft/NeoForge artifacts; compiling against handwritten signature stubs must be avoided. This patch fixes the specific reported linkage error but cannot guarantee additional stub-origin errors are absent.

**Version:** `0.1.0-alpha.48.1`, NeoForge 21.1.259, Minecraft 1.21.1, Cobblemon 1.8.1. Remove Alpha 48; install only Alpha 48.1. Third-party Pixelmon-derived assets remain outside the public GitHub repository.
