# JOB-09 v0.4.4.8 Build Audit — Changeable Garage Selector and Forced Full Delivery

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Baseline:** v0.4.4.7  
**Status:** STATIC VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Exact artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_8_ChangeableOwnedGarageMapSelectorForceFullDeliveryRuntimeSlim.zip`

- SHA-256: `cdf7aebdaaeb47a8b8a61157eacdf27b249acf478a4fd5ad02dd0f4156f3006e`
- ZIP bytes: `897,747`
- ZIP entries: `16`
- Uncompressed bytes: `1,494,080`

## Implemented

- A linked purchased RLS garage can now be changed or unlinked when no delivery transaction is pending.
- Yard management, Tow Company Garage records, and legacy company records open a full-screen JOB-09 owned-property selector.
- The selector displays exact RLS facility ID, translated facility name, available description/address, used/capacity, full status, distance, map position, nearest owned garage, current-computer garage, and current link.
- Selection can be saved without delivery or saved and delivered immediately.
- Full garages remain selectable. Delivery to a full garage requires the explicit `Force delivery even if full` checkbox.
- Normal RLS movement remains the default. If RLS redirects the item to a different garage, JOB-09 detects the wrong destination and rolls back.
- Forced delivery directly assigns the verified owned inventory record to the selected purchased garage, marks it dirty, removes the physical object, verifies exact location/ownership, and restores the previous location/name if verification fails.
- Relinking changes future delivery destination only. Unlinking does not delete virtual records or move already-delivered Career inventory.
- Pending delivery transactions lock relink/unlink to prevent mismatched transaction destinations.
- Force authorization is transaction-scoped and cannot leak from a failed unrelated attempt.

## Boundaries

No RLS source, Browser Core, JOB-04, JOB-13, Random Events, prop, vehicle, JBeam, controller, shared phone, or shared browser file was changed or packaged. The selector uses RLS garage data but does not override the RLS Real Estate page.

## Verification

- Source static checks: **90 passed / 0 failed**
- Transaction assertions: **16 passed / 0 failed**
- Source total: **106 passed / 0 failed**
- Independently extracted package checks: **55 passed / 0 failed**
- Exact source/package hash matches: **16/16**
- Browser Core active-path overlap: **0**
- JOB-04 slim active-path overlap: **0**
- JOB-13 active-path overlap: **0**

## Runtime status

BeamNG runtime is untested. v0.4.4.7 remains the rollback artifact. Saved-job Resume and the temporary Scene Manager roadside-equipment palette remain deferred.
