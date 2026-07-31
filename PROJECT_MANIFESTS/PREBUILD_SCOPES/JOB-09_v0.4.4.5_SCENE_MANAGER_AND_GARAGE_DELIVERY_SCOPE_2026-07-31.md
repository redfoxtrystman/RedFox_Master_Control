# JOB-09 v0.4.4.5 Pre-Build Scope — Scene Manager Clarity and Garage Delivery

**Date:** 2026-07-31
**Owner:** David / Captain
**Source artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_4_ActiveCallPerformanceEmergencyFilterSameYardClaimRuntimeSlim.zip`
**Source SHA-256:** `61b1ef9e746f5978bba2cd7e7a4368aef4c19d2fe17f6c1207142d4fd3a4f6ad`
**Authorized next version:** `v0.4.4.5`

## Owner request

1. Make the Scene Builder / scene manager easier to understand.
2. Finish and clearly expose moving a claimed impound/lien vehicle out of custody and into the garage.
3. Update GitHub before and after the build.

## Locked source scope

Only JOB-09-owned files may change:

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`
- `ui/modules/apps/redfoxTowPortal/portal.html` only if labels/navigation require it
- JOB-09 metadata/version files

No JOB-01 Browser Core, JOB-04, JOB-13, stock Career/RLS, Random Events, or other job files may be edited.

## Scene Manager repair

The Scene Builder will be renamed/presented as **Scene Manager** and changed into a guided workflow:

1. Load or accept a call scene.
2. Turn editing on.
3. Select an object and choose whether it belongs in the saved reusable scene.
4. Adjust position/rotation only when needed.
5. Accept the current live scene for this job.
6. Optionally save the adjusted layout as a reusable template.

Basic controls must appear first. Catalog-role teaching, preferred-equipment mapping, exact transforms, and deletion remain under a clearly marked advanced section. Labels must explain the difference between:

- accepting a scene for the current job;
- including/excluding an object from a future saved template;
- saving a reusable template;
- replaying a saved template;
- rejecting and rerolling a scene.

## Impound/lien to garage repair

The flow must be explicit and safe:

1. Custody/impound record remains on legal hold until eligible.
2. **Claim into Tow Company Garage** pays lien/title costs once and atomically moves the record into the same exact yard's company/shop storage.
3. **Deliver to Linked RLS Garage** is a separate explicit action for a claimed company/shop vehicle.
4. The exact yard must be linked to a purchased RLS garage before delivery.
5. Delivery must preserve/create exactly one Career inventory ID, verify ownership and garage placement, and only then remove the virtual company/shop record.
6. Any failure must leave the vehicle safely in company/shop storage and roll back partial money/ownership/placement changes.
7. UI must show current stage: Custody Hold, Claim Eligible, Tow Company Garage, Transfer Pending, or Linked RLS Garage.

The wording `Send to Personal Storage` is replaced with garage-delivery wording so the intended business flow is unambiguous.

## Deferred and preserved

- v0.4.4.4 remains the rollback build.
- Saved-job resume remains deferred.
- Periodic recovery autosave remains unchanged until David tests call-time performance.
- Existing emergency-vehicle filtering, Random Events payment/location repair, route throttling, same-yard claim transaction, and runtime-slim packaging must be preserved.

## Required verification

- Lua compilation
- JavaScript syntax
- JSON parsing
- exact source diff review
- scene workflow labels/actions and no dead buttons
- claim transaction rollback tests
- linked-garage delivery success/failure/idempotency tests
- no duplicate Career vehicle or duplicate shop record
- no loss of custody/shop record on failure
- runtime allowlist package only
- zero active-path overlap with Browser Core, slim JOB-04, and JOB-13

No runtime behavior may be called proven until David tests the exact v0.4.4.5 ZIP in BeamNG.