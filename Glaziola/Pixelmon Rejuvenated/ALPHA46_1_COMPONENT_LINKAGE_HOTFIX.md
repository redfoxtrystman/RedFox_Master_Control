# Pixelmon Rejuvenated Alpha 46.1 — Component linkage hotfix (2026-10-17)

Target: Minecraft 1.21.1, NeoForge 21.1.259, Cobblemon 1.8.1, Java 21.

## Problem confirmed from user-provided Alpha 46 source archive and crash report

The creative tab initialization in `StoneEquipment.lambda$static$12` crashes because its precompiled class was built against an incorrect Minecraft API stub:

```
invokestatic Method net/minecraft/network/chat/Component.translatable:
  (Ljava/lang/String;)Lnet/minecraft/network/chat/Component;
```

Minecraft 1.21.1 declares `Component` as an interface, with `translatable(String)` returning `MutableComponent`. The actual JVM invocation must be:

```
invokestatic InterfaceMethod net/minecraft/network/chat/Component.translatable:
  (Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;
```

The source code's ordinary Java expression `Component.translatable("itemGroup.pixelmonrejuvenated.pixelmon_items")` is valid; **the old compiled binary linkage is the problem**, not that expression.

## Repair

A Java 21 ASM visitor repairs the bytecode invocation in `build/pack/com/glaziola/pixelmonrejuvenated/StoneEquipment.class`. The original compiled classes and resource pack are retained otherwise. Alpha 46.1 changes only this linkage and mod version metadata.

Download the repaired JAR and full user-provided source snapshot from the related ChatGPT conversation; the complete source snapshot has not been committed to this public repository.

**Do not upload the full source archive or JAR with extracted Pixelmon 9.4.1 textures/models into a public repository without verifying redistribution rights.** The provided project's notes explicitly identify third-party Pixelmon assets and prohibit public redistribution absent permission.

## Verification

- The broken `Methodref` in `StoneEquipment.class` is corrected to `InterfaceMethodref` with the `MutableComponent` return type.
- The generated Alpha 46.1 JAR passed ZIP integrity and uniqueness checks: 4,099 entries and 31 compiled classes.
- All 3,380 JSON files in the JAR parsed successfully.
- **Runtime NeoForge startup was not tested.** This is a compiled-class repair/repack, **not** a clean Gradle rebuild. Gradle/NeoForge dependencies and the Cobblemon JAR were not available locally, and the build environment could not access download servers. Subsequent binary incompatibilities remain possible.
- Prior source build relies on `libs/Cobblemon-neoforge-1.8.1+1.21.1.jar`; compile against the real Minecraft/NeoForge/Cobblemon APIs before distributing an official release.

## Reproduction on the original Alpha 46 source ZIP

```sh
javac --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED scripts/RepairMinecraftComponentLinks.java
java --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED -cp scripts RepairMinecraftComponentLinks build/pack
python3 scripts/package_alpha46_1.py
```

Run against an unmodified Alpha 46 source snapshot only; the repair program deliberately fails if the already-broken invocation is absent. Use only one Pixelmon Rejuvenated JAR in the mods folder at a time.

Development follow-ups: full ModDevGradle clean compile and in-game smoke test, item and block creative tabs, equipment crafting, model/texture rendering, and remaining stub-origin linkage auditing.
