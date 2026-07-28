# JOB-09 v0.3.3 — Tabbed WEUI / Scene Builder / Safety Lock Build Audit

**Date:** 2026-07-27  
**Job:** `19 — JOB-09-RedFox_TowRecoveryDispatch`  
**Artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_3_TabbedWEUISceneBuilderSafetyLock.zip`

## Exact artifact

- SHA-256: `2d75e1fcfe4aa907c906fae2d45c6c9c345e7604d11f2fbdda3a68d3fc0b98af`
- Size: 205,793 bytes
- ZIP entries: 62
- ZIP CRC/integrity: PASS
- Duplicate ZIP paths: none
- Metadata version: 0.3.3
- Manifest version: 0.3.3
- Main Lua SHA-256: `a8346b0842bcc81c5329d5ba2175abb5b3a8217b0f92dbbc9ec849cbe4344168`
- Main Lua size: 273,572 bytes
- Status: **BUILT — STATIC VERIFIED — RUNTIME PENDING DAVID**

## Baseline and safety boundary

This build is based on David-confirmed working v0.3.0 dispatch behavior. It does not carry forward the failed v0.3.1 artificial `redfox_towshop_*` garage bridge.

The known unsafe legacy company-garage movement is safety-locked:

- no new personal-to-company transfer;
- no legacy company-record retrieval that could duplicate or alter ownership;
- existing Fleet Book and legacy records remain readable and preserved;
- no stock/RLS file is replaced.

## Main implementation

- Eight top navigation sections remain visible at the top and change the content below.
- Dispatch Center is dispatch-only.
- Scene Builder is a separate top-level section.
- Scene Editor highlights included, selected, excluded, and unsaveable objects.
- Adjusted scene capture stores included tow targets plus saveable support/equipment metadata and relative transforms.
- Saved scene templates can be selected, replayed at the current anchor, or deleted.
- Quick equipment buttons search installed BeamNG configurations for cones, warning signs, barricades, flares/markers, and debris.
- Target blacklist, whitelist, category recataloging, and undo are preserved.
- Temporary Vehicle Spawn Lab moved into Development Tools.
- Custom RedFox tow-yard names are supported while preserving stable RedFox yard IDs.
- Existing Garage Hub open/close/theme/font/button/text contracts remain present.

## Static verification

- Lua parse: PASS
- Lua top-level execution with safe stubs: PASS
- Module status API: PASS (`version=0.3.3`, `activeSection=dispatch`)
- All JSON parse: PASS
- Final ZIP re-extraction: PASS
- Re-extracted Lua parse: PASS
- Re-extracted module status test: PASS
- Protected stock Career/RLS paths: none
- Artificial `redfox_towshop_*` runtime bridge: absent
- Direct source overwrite of stock Career/RLS files: none

## Runtime proof still required

- WEUI top-tab layout and resizing;
- Garage Hub theme/font/button propagation;
- scene debug-drawer highlights;
- include/exclude state behavior;
- adjusted scene save and replay;
- installed prop discovery and spawning;
- custom yard-name persistence;
- no console spam or ownership changes.

No runtime-working claim is made before David tests this exact ZIP.
