# RedFox Skin Studio — Three Broken Skin Repair Pack

**Date:** 2026-07-20  
**Owner:** David / Captain  
**Status:** **BUILT — RUNTIME UNTESTED**

## Request

David asked for the three broken RedFox Skin Studio v0.1 skin exports to be repaired and combined into one BeamNG mod for testing.

Inputs:

- `redfox_pickup_RedFox_Towing.zip`
- `redfox_pickup_RedFox_Towing_3.zip`
- `redfox_barstow_RedFox_Towing.zip`

## Confirmed v0.1 failures

The old packages contained malformed JBeam and/or mismatched texture references. Examples included material files requesting texture names that were not present in the ZIP. This was an exporter failure, not user error.

## Repair performed

A combined test pack was created containing:

1. Gavril D-Series — `RedFox Towing`
2. Gavril D-Series — `RedFox Towing 3`
3. Gavril Barstow — `RedFox Towing`

The rebuilt pack uses:

- valid strict JSON/JBeam syntax
- unique skin identifiers
- correct `paint_design` parts and `globalSkin` values
- `*.skin.materials.json` files
- full `/vehicles/...` texture paths
- material references to `*.color.png`
- matching `*.color.dds` companion textures
- 2048 × 1024 power-of-two textures

The random-paint exports contained partial alpha. They were flattened onto an opaque white base so their visible artwork is retained as fixed-color paint instead of producing unpredictable transparency.

## Static validation

Passed:

- all JSON and JBeam parse checks
- every generated local texture reference exists
- all PNG texture dimensions are powers of two
- all three skin part identifiers map to matching material skin names
- final ZIP archive integrity

## Artifact

`RedFox_Fixed_3_Skin_Test_Pack_v0_1_BUILT_RUNTIME_UNTESTED.zip`

SHA-256:

`2577cece1e42a2e33020d2119fb6c5f485238b5f48d07ee8fc03a0273d04885b`

## Test rule

Remove or disable the three original broken ZIPs before testing this combined pack to prevent duplicate or conflicting definitions.

This pack must remain labeled **BUILT — RUNTIME UNTESTED** until David confirms that the exact ZIP appears and renders correctly in BeamNG.
