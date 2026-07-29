# JOB-09 v0.4.2.1 — All-Mission Generation Emergency Hotfix Build Audit

**Job:** JOB-09 — RedFox Tow / Recovery / Dispatch  
**Date:** 2026-07-29  
**Status:** STATIC VERIFIED — BEAMNG / RLS / RANDOM EVENTS RUNTIME TEST REQUIRED

## Runtime failure reported

David reported that abandoned missions and then all missions failed to start. The JOB-09 window showed:

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua:1535: attempt to call global 'dispatchClassName' (a nil value)
```

## Confirmed cause

`chooseDiverseByClass()` called an undefined global helper:

```lua
return selected, dispatchClassName(selected, candidateClass)
```

The actual helper is namespaced under `vehicleRules`.

## Correction

The call was changed to:

```lua
return selected, vehicleRules.dispatchClassName(selected, candidateClass)
```

This is the only runtime behavior correction in the hotfix. Existing v0.4.2 police-roster, protected-dispatch, Random Events bridge, active-job recovery, payout, records, yard, fleet, and portal behavior was otherwise preserved.

## Verification

- ZIP CRC/testzip: PASS
- Lua syntax via texlua `loadfile`: PASS
- Portal JavaScript syntax via Node: PASS
- All JSON parsed: PASS
- No unqualified `dispatchClassName(` calls remain: PASS
- Exact regression assertion on `vehicleRules.dispatchClassName`: PASS
- No duplicate ZIP entries: PASS
- No unsafe archive paths: PASS
- No native/executable payloads: PASS
- Source-to-re-extracted file hash comparison: PASS

## Artifact

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_2_1_AllMissionGenerationEmergencyHotfix.zip
SHA-256: e3c0662d1a2859febd9d500d995c1f4a5784544290210e202a8c5f65f950fc43
Size: 1,607,442 bytes
ZIP entries: 144
Files: 120
```

## Mandatory first runtime test

1. Disable/delete v0.4.2 and every older JOB-09 ZIP.
2. Install only v0.4.2.1.
3. Reload BeamNG or reload Lua extensions.
4. Request and accept **Abandoned Vehicle**.
5. Confirm the offer transitions to an active call and a target scene appears.
6. Then test one ordinary tow and one Random Events scene.
