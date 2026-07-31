# JOB-09 v0.4.4.6 Source Verification — Direct Garage Link and Legacy Company Recovery

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Baseline:** JOB-09 v0.4.4.5 runtime-slim package  
**Status:** SOURCE VERIFIED — PACKAGE NOT YET BUILT  
**Runtime tested in BeamNG:** No

## Approved runtime failure

v0.4.4.5 proved custody/lien records could enter virtual Tow Company Garage, but physical delivery remained blocked when the exact yard lacked a linked purchased garage. The selected vehicle page did not provide a direct link chooser. Existing `virtual_company_garage` records also remained behind the old permanent legacy safety lock.

One screenshot record, `FP Crane Chains 2 rotatable chains`, is equipment rather than a normal titled vehicle. This build explicitly prevents such equipment/attachments from becoming native Career garage vehicles.

## Exact source lineage

- Local baseline commit: `ea81a9914a6f0697422d35edcc8df717e5c7c3f7`
- Verified source commit: `1b4b1496f5e9e9e80627d8baa01dd56ce076f311`
- Exact source patch SHA-256: `f6540f8fb61325c2cb6dc42854d7f1521f95e843fd89562f7e058f48c428a37f`
- Exact source patch bytes: `68,338`

## Changed runtime files

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
```

No Browser Core, JOB-04, JOB-13, Random Events, stock Career/RLS, shared phone layout, or shared FoxNet browser files were changed.

## Implemented repair

### Selected Tow Company Garage record

- Shows purchased RLS garage candidates directly on the selected record.
- Allows explicit `Link Yard & Deliver` from that record.
- Auto-selects only when exactly one valid purchased garage exists and the player presses the delivery action.
- Preserves one-to-one exact-yard-to-garage ownership.
- Shows map, capacity and precise blocking information.

### Legacy company-garage recovery

The permanent read-only lock is replaced with a transaction-safe recovery tool:

1. If the original Career inventory ID still exists and matches model/config, adopt that same ID.
2. If the old record confirms the original vehicle was removed, recreate exactly one owned vehicle.
3. Persist transaction ID and pending inventory ID before movement.
4. Resume the same pending ID after reload instead of creating another vehicle.
5. Verify exact linked-garage placement.
6. Remove the virtual legacy record only after verification.
7. Preserve and conflict-lock the record if safe completion cannot be proven.

### Equipment/attachment protection

Chains, spreader bars, detached crane pieces, props and other non-vehicle equipment remain in company equipment/non-titled storage. They may be sold, auctioned, scrapped or handled by a later equipment-storage system, but are not converted into titled Career vehicles.

## Verification

- Runtime allowlist files: **16**
- Static/source checks passed: **42**
- Mock transaction assertions passed: **38**
- Focused source checks total: **80**
- Failures: **0**

Verified:

- Lua compilation with `texlua --luaconly`;
- both JavaScript files with `node --check`;
- all JSON parsing;
- all images readable;
- all local portal references resolve;
- no shared/core override paths;
- no copied Random Events source;
- no development backups or compiler output;
- keyed and array-form garage facility discovery;
- wrong-map garage filtering;
- existing native inventory ID adoption;
- exactly-once recreation for confirmed-removed records;
- model/config identity conflict blocking;
- verification before virtual-record deletion;
- direct shop record link and delivery;
- equipment delivery blocking.

## Packaging gate

Only the 16 manifest-listed runtime files may enter the ZIP. The package must be independently extracted and rechecked before distribution. v0.4.4.5 remains the rollback artifact.
