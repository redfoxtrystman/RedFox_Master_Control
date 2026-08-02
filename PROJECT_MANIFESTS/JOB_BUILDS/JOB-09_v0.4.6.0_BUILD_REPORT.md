# JOB-09 v0.4.6.0 Build Report

## Ownership correction

JOB-09 owns the complete RedFox Tow web experience:

- public/customer website;
- customer tow request flow;
- company login/portal view;
- dispatch, scenes, records, custody, company assets, fleet, yards, invoices, and settings;
- the Lua bridge connecting those pages to Career/RLS.

JOB-01 Browser Core may host or link the website, but JOB-01 does not own JOB-09 tow-company logic. Reusable native vehicle-registration lessons may later be documented through JOB-02 after runtime acceptance.

## Architecture correction

A lien claim is no longer intended to create only a virtual Tow Company record.

Successful claim sequence:

1. Verify legal eligibility, exact RedFox yard identity, company capacity, funds, current map, linked owned RLS garage, and garage space.
2. Spawn the exact stored vehicle snapshot.
3. Give the actual spawned vehicle to native Career/RLS inventory.
4. Wait for native parts inventory, original-parts/changed-slot tracking, insurance registration, exact garage assignment, and two-stage save verification.
5. Charge the lien/title acquisition only after the native vehicle verifies.
6. Remove the custody record and retain one RedFox company-asset record referencing the same native inventory ID.

Failure before commit removes the temporary native vehicle, preserves custody, and takes no acquisition charge. A native vehicle that cannot be removed is locked as a conflict to prevent duplication.

## Web consolidation

The existing page is now treated as one JOB-09 website with two sides:

- **Public side:** service information, Tow My Current Vehicle, Dispatch Selected Service, and entry into the Company Portal.
- **Company side:** overview, dispatch, scene manager, records, custody and native company assets, fleet, tow-yard links/upgrades, invoices, and tools.

## Files changed from v0.4.5.1

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
- `mod_info/redfox_tow_recovery_dispatch/info.json`
- `ui/modules/apps/redfoxTowPortal/app.js`
- `ui/modules/apps/redfoxTowPortal/app.json`
- `ui/modules/apps/redfoxTowPortal/portal.html`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`
- `ui/modules/apps/redfoxTowPortal/assets/css/portal.css`

## Archive

- File: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_6_0_UnifiedPublicCompanyImmediateNativeCareerClaimRuntimeSlim.zip`
- SHA-256: `1641ba350b6c90e2fb65a9938c35dba51eba889495d9ff1321810a9f0e854ce8`
- Runtime files: 16
- Duplicate ZIP paths: none

## Static checks

- ZIP integrity: passed
- Lua syntax: passed with `loadfile` under LuaTeX
- JavaScript syntax: passed with Node `--check`
- JSON parsing: passed
- Cache tokens: updated to `0460`

Runtime behavior is unproven until tested in BeamNG/RLS on West Coast USA.
