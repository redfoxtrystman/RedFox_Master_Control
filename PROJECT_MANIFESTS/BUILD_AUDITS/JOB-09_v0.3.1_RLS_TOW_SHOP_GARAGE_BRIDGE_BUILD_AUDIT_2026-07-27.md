# JOB-09 v0.3.1 — RLS Tow-Shop Garage Bridge Build Audit

Date: 2026-07-27

## Artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_1_RLSTowShopGarageBridge.zip`

- SHA-256: `662db67fc190ede9c529391c39570e93883c2c7024ebb2edb8c700837f5c4aec`
- Size: 218,778 bytes
- ZIP integrity: PASS
- Duplicate ZIP entries: none
- Metadata version: 0.3.1
- Status: **BUILT — RUNTIME UNTESTED**

## Static checks

- Lua syntax and main-chunk local-variable limit: PASS
- JSON parsing: PASS
- Exact ZIP re-extraction and repeat syntax/JSON check: PASS
- Protected stock Career/RLS path scan: PASS
- Runtime boundary: only JOB-09 extension plus its loader script
- Direct per-frame console-log/save-write scan: PASS
- Required garage bridge, move, rollback, undo, and legacy-recovery markers: PASS

## Runtime scope

This build replaces v0.3.0's failed separate Company Fleet Garage model. It attempts to register each saved RedFox tow yard as a runtime RLS-style garage location and moves the same normal owned RLS inventory vehicle by changing its garage location through `career_modules_inventory.moveVehicleToGarage`.

The ZIP does **not** contain or overwrite:

- RLS `inventory.lua`
- RLS `garageManager.lua`
- RLS `freeroam/facilities.lua`
- stock BeamNG Career files
- any other RedFox job module

## Safety behavior

- Refuses company assignment when the current truck is not a normal owned RLS vehicle.
- Verifies requested destination and `owned ~= false` after every move.
- Rolls the record back to its prior location/metadata when verification fails.
- Stores the physical object only after successful location verification.
- Keeps one-step undo for the most recent verified move.
- Retains v0.3.0 separate-company records until explicit recovery.
- Backs up a legacy record before rebuilding or reconnecting it.
- Removes a legacy record only after one owned RLS vehicle is verified.

## Required runtime proof

1. Register one existing tow yard as an RLS garage location.
2. Move one noncritical owned truck into it.
3. Verify the same inventory ID and `owned=true` in My Vehicles.
4. Retrieve through normal RLS behavior at the tow shop.
5. Move back and test Undo without duplication.
6. Recover one legacy v0.3.0 record only when such a record exists.

No DAVID-TESTED WORKING claim is made.