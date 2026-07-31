# JOB-09 v0.4.4.7 Build Audit — Spawnable Item Garage Delivery, Props Untouched

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Baseline:** v0.4.4.6  
**Status:** STATIC VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Owner-requested correction

v0.4.4.6 incorrectly blocked spawnable equipment/props such as `FP Crane Chains 2 rotatable chains` from native RLS garage delivery. David instructed JOB-09 to remove that block and leave props alone.

## Exact artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_7_SpawnableItemGarageDeliveryPropFilesUntouchedRuntimeSlim.zip`

- SHA-256: `970acf3070242cdd2aca34b28c74bf37bde4b7919eebe5304f66604a4f74fab2`
- ZIP bytes: `891,619`
- ZIP entries: `16`
- Uncompressed bytes: `1,465,364`

## Exact source lineage

- Baseline source commit: `1b4b1496f5e9e9e80627d8baa01dd56ce076f311`
- Verified source commit: `840500b5e2c52c7c5f939afdda5367b7903f9128`
- Source patch SHA-256: `6254dc73678bdee6be2ba276374ba3b0d391eda92eebab5f1cac7a4af0191f5c`

## Implemented

- Removed equipment/attachment/prop category rejection from claimed-shop garage delivery.
- Removed equipment/attachment/prop category rejection from legacy-company recovery.
- Requires complete exact model/config identity before native delivery.
- Leaves the native spawn, `addVehicle`, garage placement and verification transaction authoritative.
- Preserves existing pending-ID, rollback, duplicate-prevention and identity-conflict safeguards.
- Removed real-world-title wording from the blocking message.
- Corrected all package descriptions so they no longer claim equipment blocking.
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
