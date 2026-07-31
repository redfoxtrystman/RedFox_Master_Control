# JOB-09 v0.4.4.6 Build Audit — Direct Garage Link, Legacy Recovery and Equipment Guard

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Status:** STATIC VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Exact artifact

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_6_DirectGarageLinkLegacyCompanyRecoveryEquipmentGuardRuntimeSlim.zip
```

- SHA-256: `f768fab30efdd663ba70f60d02c5b74c552c126afff333577ad6af1e35a166c5`
- ZIP bytes: `891,621`
- Uncompressed runtime bytes: `1,465,670`
- Runtime files: `16`
- Source/package exact hash matches: `16/16`

## Runtime failure repaired

v0.4.4.5 allowed a lien vehicle to enter virtual Tow Company Garage but did not make the real-garage step understandable or directly usable. Existing legacy virtual company records also remained permanently locked.

## Repair

### Direct garage selection on the selected vehicle

- Purchased RLS garages are shown directly on the selected Tow Company Garage record.
- The player can select a garage and press `Link Yard & Deliver` without leaving the record page.
- Exactly one valid garage can be selected only by the player's explicit delivery click.
- One purchased garage cannot be silently shared by multiple RedFox yards.
- Wrong-map, full-garage, missing-link and stale-link states produce distinct messages.

### Legacy company record recovery

- Removed the permanent `LEGACY COMPANY GARAGE MOVEMENT IS DISABLED` lock.
- Existing original Career inventory ID is adopted when it still exists and model/config match.
- A confirmed-removed legacy vehicle is recreated exactly once when no native inventory record remains.
- Transaction ID and pending inventory ID persist before native movement.
- Reload resumes the same pending ID rather than creating another vehicle.
- Exact garage placement verifies before the virtual company record is deleted.
- Identity conflicts, ambiguous ownership and failed cleanup preserve/lock the record for review.

### Equipment guard

`FP Crane Chains 2 rotatable chains` and similar chains, spreader bars, crane parts, props and attachments are company equipment, not titled road vehicles. They remain safely stored for sale/auction/scrap/equipment handling and cannot be inserted into native Career garage inventory.

## Changed runtime files

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
```

The remaining 10 allowlisted runtime assets are byte-identical to v0.4.4.5.

## Verification

- Source static checks: `42 passed / 0 failed`
- Mock transaction assertions: `38 passed / 0 failed`
- Re-extracted package static checks: `42 passed / 0 failed`
- Exact source-to-package hashes: `16/16`
- ZIP CRC/integrity: PASS
- Duplicate paths: 0
- Unsafe traversal paths: 0
- Executable/native payloads: 0
- Lua compilation: PASS
- JavaScript syntax: PASS
- JSON parse: PASS
- Images: PASS
- Portal local references: PASS
- Browser Core overlap: `0`
- JOB-04 slim overlap: `0`
- JOB-13 overlap: `0`

## Documentation incident

The first pre-package GitHub source report contained an incorrect source-patch hash and byte count. It was caught and corrected before package creation. No source/runtime file changed because of the documentation correction.

## Runtime gate

Do not call the garage transfer proven until David tests this exact ZIP. v0.4.4.5 remains the rollback artifact. Saved-job Resume remains deferred.
