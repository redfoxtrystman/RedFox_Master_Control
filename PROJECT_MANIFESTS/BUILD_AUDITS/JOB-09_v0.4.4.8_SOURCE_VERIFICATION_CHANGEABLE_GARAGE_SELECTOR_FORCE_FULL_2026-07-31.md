# JOB-09 v0.4.4.8 Source Verification — Changeable Owned-Garage Selector and Forced Full Delivery

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Baseline:** JOB-09 v0.4.4.7 runtime-slim package  
**Status:** SOURCE VERIFIED — PACKAGE NOT YET BUILT  
**BeamNG runtime tested:** No

## Owner-requested repair

The v0.4.4.7 garage link could become confusing and effectively permanent after the wrong purchased RLS garage was selected. RLS also redirected normal vehicle movement away from a selected full garage to another owned garage with capacity.

## Exact scope

- Allow a RedFox tow yard's purchased RLS garage link to be changed at any time when no delivery transaction is pending.
- Allow safe unlinking while preserving all virtual custody/company records and leaving already-delivered Career inventory where it is.
- Add a full-screen JOB-09 owned-garage selector using exact RLS facility IDs, translated names, descriptions/addresses, map positions, ownership, capacity, used slots, nearest-to-player state, and current-computer state.
- Expose the selector from yard management, claimed Tow Company Garage records, and legacy company recovery.
- Add explicit `Save Garage Choice`, `Save & Deliver`, `Use Nearest Owned Garage`, `Use Garage at Current Computer`, and `Unlink Current Garage` controls.
- Add an owner-controlled `Force delivery even if full` option.
- Preserve exact inventory IDs, pending transaction IDs, rollback, placement verification, identity conflict protection, and duplicate prevention.
- Do not modify RLS source files, Browser Core, JOB-04, JOB-13, Random Events, props, vehicles, JBeams, or controllers.
- Keep the temporary Scene Manager equipment palette as a separate later feature.

## Implementation note

The selector uses the same RLS garage facility IDs and ownership data as the Real Estate phone app, but it is a JOB-09 full-screen selector rather than a modification of the RLS Vue page. This avoids taking ownership of or overriding RLS UI files.

Normal delivery still uses RLS `moveVehicleToGarage`. If RLS redirects to a different garage, JOB-09 detects the wrong destination and rolls back. Forced full-garage delivery directly assigns the already-created owned inventory record to the explicitly selected purchased garage, marks it dirty, removes the physical object, verifies exact ownership/location, and restores the previous location/name if verification fails.

## Exact local source lineage

- Baseline local commit: `e21675c996f6a514b703eb7ccf1eb126b32d222b`
- Verified source local commit: `ae98d799c525a553bb969e8eb3198d6925426c4e`
- Exact source patch SHA-256: `9fd08981f24bd32ec53b7020750963708379f6cefaa31fa13f4ec898e962cb71`
- Exact source patch bytes: `73,008`

## Changed runtime files

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
ui/modules/apps/redfoxTowPortal/portal.html
```

## Verification

- Runtime allowlist files: **16**
- Static/source checks: **90 passed / 0 failed**
- Focused transaction assertions: **16 passed / 0 failed**
- Total source checks/assertions: **106 passed / 0 failed**

Verified:

- both Lua files compile with `texlua --luaconly`;
- both JavaScript files pass `node --check`;
- all JSON parses;
- all images are readable;
- all local HTML references resolve and HTML IDs are unique;
- exact seven-file change boundary from v0.4.4.7;
- no RLS/core overrides or copied RLS Real Estate source;
- no prop, equipment, vehicle, JBeam, controller, archive, audit, or catalog payloads;
- exact facility IDs, labels, capacity, nearest/current and marker coordinate data;
- full garages remain selectable but require explicit force authorization to deliver;
- normal RLS redirection to an unintended garage fails exact-destination verification;
- forced assignment verifies exact selected destination;
- forced verification failure restores the prior garage ID and nice-location label;
- relinking changes future destination only;
- unlinking preserves virtual records and already-delivered inventory;
- active pending transactions block relink and unlink;
- force authorization is stored only with a staged transaction and cannot leak from an unrelated failed attempt.

## Packaging gate

Only the 16 runtime-manifest files may enter the ZIP. The ZIP must be independently extracted, recompiled/reparsed, hash-compared to source, and checked for cross-package active-path overlap before distribution. v0.4.4.7 remains the rollback artifact.
