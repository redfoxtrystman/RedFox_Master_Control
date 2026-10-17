# Alpha 46.2 — Missing compiled class repaired (2026-10-17)

**Confirmed cause:** After the `Component.translatable` hotfix in Alpha 46.1, the Minecraft 1.21.1 / NeoForge 21.1.259 client failed to initialize Pixelmon Rejuvenated:

```text
java.lang.NoClassDefFoundError:
  com/glaziola/pixelmonrejuvenated/UltraFallingBlock
at UltraSpaceBlocks.falling(UltraSpaceBlocks.java:55)
at UltraSpaceBlocks.<clinit>(UltraSpaceBlocks.java:80)
```

The original Alpha 46 and Alpha 46.1 JARs both **omitted** `UltraFallingBlock.class`, even though `UltraFallingBlock.java` was included in the original source archive. Both `UltraSpaceBlocks` and `ExtraPixelmonBlocks` need that class. This is a packaging bug in our own mod, not a CobbleNav defect.

## Remedy

- Compiled the existing `UltraFallingBlock.java` for Java 21 using a minimal compile-only API signature scaffold consistent with the actual Minecraft 1.21.1 `FallingBlock`, `MapCodec`, and `BlockBehaviour` declarations.
- Added **only** the missing `UltraFallingBlock.class` to the previously patched JAR. Preserved the Alpha 46.1 `StoneEquipment` bytecode linkage fix.
- Bumped mod metadata and source `build.gradle` version to `0.1.0-alpha.46.2`.
- Inspected every compiled class for missing internal `com/glaziola/pixelmonrejuvenated` references and compared all surviving JAR members against 46.1 (unchanged other than metadata).
- All 3,380 JSON resources parsed; ZIP CRC checks passed; **32 classes, 4,100 JAR entries**.
- Added `scripts/check_pack_classes.py` to fail future packaging when a referenced internal class is absent.

## Limitations and installation

This is a **compiled-class repair and repack**, not a full clean ModDevGradle build. It does **not** prove the JAR boots successfully; no local game client run was available. Continue with real dependencies instead of compile stubs for a supported release.

The patched JAR and full source snapshot were delivered directly in ChatGPT; they are **not** committed to this public repository because the source ZIP contains third-party Pixelmon artwork whose redistribution rights have not been established.

Install only `PixelmonRejuvenated-0.1.0-alpha.46.2-CLASS-PACKAGING-FIX-neoforge-1.21.1.jar`. Remove previous Pixelmon Rejuvenated JARs. No modification of CobbleNav or other addons is necessary for this reported error.
