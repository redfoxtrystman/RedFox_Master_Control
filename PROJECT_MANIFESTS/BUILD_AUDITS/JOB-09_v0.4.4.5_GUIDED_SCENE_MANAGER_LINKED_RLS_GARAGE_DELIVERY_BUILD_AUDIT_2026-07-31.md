# JOB-09 v0.4.4.5 Build Audit — Guided Scene Manager and Linked RLS Garage Delivery

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Base artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_4_ActiveCallPerformanceEmergencyFilterSameYardClaimRuntimeSlim.zip`  
**Base SHA-256:** `61b1ef9e746f5978bba2cd7e7a4368aef4c19d2fe17f6c1207142d4fd3a4f6ad`

## Order-of-operations records

- Pre-build scope commit: `c50dfece8388cd24d761c02ddbf033437693e8c1`
- Source verification commit, created before packaging: `05bea43e57620dadbf64c12100467eb57314d075`
- Source checks before packaging: `62 passed / 0 failed`

## Exact output

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_5_GuidedSceneManagerLinkedRLSGarageDeliveryRuntimeSlim.zip`

- SHA-256: `1271ea5a987b04b10e1ed88e928008d2599d5682e682199790802d4a7558dbfb`
- ZIP bytes: `884,951`
- Runtime files: `16`
- Uncompressed bytes: `1,430,020`
- Status: **STATIC AND PACKAGE VERIFIED — BEAMNG RUNTIME UNTESTED**

## Exact files changed from v0.4.4.4

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
ui/modules/apps/redfoxTowPortal/portal.html
```

No Browser Core, JOB-04, JOB-13, stock Career/RLS, Random Events, or other job file was edited.

## Scene Manager repair

The confusing Scene Builder presentation is replaced with a guided **Scene Manager**.

The normal workflow is now presented in five steps:

1. load or accept a call scene;
2. turn editing on only when needed;
3. select an object and choose whether it belongs in a reusable saved scene;
4. accept or reject the current live scene for this job;
5. optionally save the adjusted layout as a reusable scene.

The UI now explicitly separates:

- accepting the current scene for the active job;
- keeping or excluding an object from a future template;
- saving a reusable template;
- replaying a saved template;
- rejecting/rerolling a live scene.

Technical transform controls, role classification, equipment teaching, and prop spawning are hidden under **Advanced Scene Tools**. Active tow targets remain protected from deletion.

## Custody/lien to garage repair

The vehicle path is now explicit:

```text
Custody / Impound Hold
        ↓ lien eligible
Claim into Tow Company Garage
        ↓ optional physical delivery
Deliver to Linked RLS Garage
```

### Claim into Tow Company Garage

- validates legal eligibility, exact yard and company/shop capacity;
- charges lien, capped storage and title costs exactly once;
- atomically replaces the custody record with one same-yard company/shop record;
- does not require a personal/RLS garage merely to claim company ownership.

### Deliver to Linked RLS Garage

- requires the exact tow yard to be linked to a purchased RLS/Career garage;
- checks destination capacity before creating ownership;
- stages a persistent transaction before creating a Career inventory vehicle;
- preserves and resumes a pending inventory ID rather than creating a second vehicle;
- verifies ownership and exact garage placement before removing the virtual Tow Company Garage record;
- charges no second lien/title amount;
- rolls back a temporary inventory vehicle on failure and restores the company/shop record;
- preserves the exact inventory ID in a locked conflict record if cleanup cannot be verified, preventing a second delivery attempt from duplicating the vehicle;
- retains the old `shop_transfer_personal` action as a compatibility alias while the visible wording now uses linked-garage delivery.

## Verification completed

### Source/static verification

```text
62 focused checks passed
Lua compilation: PASS
JavaScript syntax: PASS (2/2)
JSON parse: PASS (4/4)
Images readable: PASS (6/6)
HTML local references: PASS
Version consistency: PASS
Scene Manager action and label checks: PASS
Garage transaction ordering: PASS
Pending-delivery idempotency: PASS
Rollback/conflict protection: PASS
```

### Independent packaged-copy verification

```text
45 packaged checks passed
ZIP CRC: PASS
Duplicate paths: 0
Unsafe paths: 0
Nested archives: 0
Executable/native payloads: 0
Exact source-to-reextracted hashes: 16/16 matched
Packaged Lua/JavaScript/JSON/images: PASS
Packaged Scene Manager controls: PASS
Packaged garage transaction protections: PASS
```

### Cross-job package boundaries

Ignoring required root metadata:

```text
Browser Core overlap: 0
JOB-04 slim overlap: 0
JOB-13 overlap: 0
Protected shared/core paths present: 0
```

## Preserved behavior

- v0.4.4.4 call-performance repairs;
- emergency-vehicle abandoned/lien filtering;
- Random Events payment and location handling;
- boundary-aware Rail/Train classification;
- exact-yard custody and company storage;
- runtime allowlist packaging;
- v0.4.4.4 remains the rollback build.

## Deferred

- Saved-job reconstruction/Resume after a game or computer crash remains deferred.
- Periodic recovery autosaving remains unchanged pending David's v0.4.4.4/v0.4.4.5 call-performance runtime result.

## Runtime gate

Do not mark Scene Manager usability, claim movement, or linked-garage delivery proven until David tests this exact SHA in BeamNG. On any failure, preserve the save, screenshot, money values, source yard, destination garage, custody/company/Career inventory state, and the relevant `beamng.log` lines before another patch.