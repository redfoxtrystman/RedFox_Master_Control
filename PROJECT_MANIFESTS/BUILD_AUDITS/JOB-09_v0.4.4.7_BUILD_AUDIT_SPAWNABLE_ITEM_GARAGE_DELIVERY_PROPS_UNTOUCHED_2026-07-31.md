# JOB-09 v0.4.4.7 Build Audit — Spawnable Item Garage Delivery, Props Untouched

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Baseline:** v0.4.4.6  
**Status:** STATIC VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Owner-requested correction

v0.4.4.6 incorrectly blocked spawnable equipment/props such as `FP Crane Chains 2 rotatable chains` from native RLS garage delivery. David instructed JOB-09 to remove that block and leave props alone.

## Exact artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_7_SpawnableItemGarageDeliveryPropFilesUntouchedRuntimeSlim.zip`

- SHA-256: `b28308a2c64698d3197312be5e97bbfc6b776f0ad7e765f3858141eec7489c05`
- ZIP bytes: `891,611`
- ZIP entries: `16`
- Uncompressed bytes: `1,465,331`

## Exact source lineage

- Baseline source commit: `1b4b1496f5e9e9e80627d8baa01dd56ce076f311`
- Verified source commit: `2ddfa48df383d66352ca79a10a39c07664b8e567`
- Source patch SHA-256: `706581130f93b4cad932ce85f56b99a7efa6ea3018ef58fc0cc8ce924288cb4f`

## Implemented

- Removed equipment/attachment/prop category rejection from claimed-shop garage delivery.
- Removed equipment/attachment/prop category rejection from legacy-company recovery.
- Requires complete exact model/config identity before native delivery.
- Leaves the native spawn, `addVehicle`, garage placement and verification transaction authoritative.
- Preserves existing pending-ID, rollback, duplicate-prevention and identity-conflict safeguards.
- Removed real-world-title wording from the blocking message.
- Added no prop classification metadata.
- Changed no prop, equipment, vehicle, JBeam or controller file.

## Verification

- Source static checks: **50 passed / 0 failed**
- Package static checks after independent extraction: **50 passed / 0 failed**
- Transaction mock assertions: **43 passed / 0 failed**
- Exact source/package hash matches: **16/16**
- Browser Core active-path overlap: **0**
- JOB-04 slim active-path overlap: **0**
- JOB-13 active-path overlap: **0**
- Prop/JBeam files changed: **0**

## Runtime status

BeamNG runtime remains untested. Test the exact FP Crane Chains record first, then one ordinary claimed road vehicle. v0.4.4.6 remains the rollback artifact.
