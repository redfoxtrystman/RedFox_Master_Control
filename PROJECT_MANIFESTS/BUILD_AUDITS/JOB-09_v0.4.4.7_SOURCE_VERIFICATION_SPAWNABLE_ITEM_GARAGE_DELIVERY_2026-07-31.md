# JOB-09 v0.4.4.7 Source Verification — Spawnable Item Garage Delivery Correction

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Baseline:** JOB-09 v0.4.4.6 runtime-slim package  
**Status:** SOURCE VERIFIED — PACKAGE BUILT ONLY AFTER THIS SOURCE GATE  
**BeamNG runtime tested:** No

## Owner correction

`FP Crane Chains 2 rotatable chains` and similar spawnable equipment/props may be stored by BeamNG through the same Career/RLS inventory and garage pipeline used for vehicles. David directed JOB-09 to fix the incorrect garage-delivery block and otherwise leave props alone.

## Exact scope

- Remove the v0.4.4.6 equipment/attachment/prop garage-delivery rejection.
- Permit an exact stored model/config record to attempt the existing native spawn, `addVehicle`, garage placement and verification transaction.
- Leave third-party prop files, JBeams, controllers, classification and spawn behavior untouched.
- Preserve pending inventory IDs, duplicate prevention, identity checks, rollback and final placement verification.
- Keep abandoned/lien call-selection rules separate and unchanged.

## Exact source lineage

- Baseline source commit: `1b4b1496f5e9e9e80627d8baa01dd56ce076f311`
- Verified source commit: `840500b5e2c52c7c5f939afdda5367b7903f9128`
- Exact source patch SHA-256: `6254dc73678bdee6be2ba276374ba3b0d391eda92eebab5f1cac7a4af0191f5c`
- Exact source patch bytes: `15,510`

## Changed runtime files

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
```

No vehicle, prop, equipment, JBeam, Browser Core, JOB-04, JOB-13, Random Events, stock Career/RLS, phone-layout or shared browser files were changed.

## Source changes

- `fleetTools.legacyDeliveryEligibility()` now requires only complete stored model/config identity.
- `M.shop.nativeDeliveryEligibility()` now requires only complete stored model/config identity.
- The native Career transaction remains authoritative: spawn exact model/config, create one inventory ID, place it into the selected purchased garage, verify, then remove the virtual record.
- Failure still rolls back or preserves/locks the pending inventory ID to prevent duplication.
- Real-world title/equipment wording was removed from the delivery-block message.
- Package descriptions were corrected so they no longer claim equipment blocking.
- No new prop classification or inventory metadata was introduced.

## Verification

- Runtime allowlist files: **16**
- Static/source checks: **50 passed / 0 failed**
- Transaction mock assertions: **43 passed / 0 failed**
- Total focused source checks/assertions: **93 passed / 0 failed**

Verified:

- Lua compilation with `texlua --luaconly`;
- both JavaScript files with `node --check`;
- all JSON parsing;
- all images readable;
- all local portal references resolve;
- no shared/core override paths;
- no copied Random Events source;
- no vehicle/prop/JBeam files in the package;
- no `redfoxGameplayClass` or `redfoxSpawnableInventoryItem` metadata added;
- equipment and walking-character exact model/config records pass delivery eligibility;
- missing model/config identity is blocked;
- existing inventory ID adoption remains exactly-once;
- confirmed-removed legacy equipment recreation remains exactly-once;
- source-ID identity conflict remains protected;
- ordinary claimed-vehicle delivery remains working in the mock;
- claimed equipment delivery uses the same exact native pipeline;
- exact model/config identity survives the mock transfer;
- verification still occurs before virtual-record deletion.
