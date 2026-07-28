# JOB-09 v0.3.4 — Safe Fleet Tow-Yard Assignment Build Audit

Date: 2026-07-27

Job: `19 — JOB-09-RedFox_TowRecoveryDispatch`

Artifact:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_4_SafeFleetTowYardAssignmentNpcDriverReady.zip`

- SHA-256: `b4ea1870ad41e34cb815af02829c65d8ff0d6d5f0dcd536fa96bb25f7a5e8c46`
- Size: 224,539 bytes
- Metadata version: 0.3.4
- Status: **BUILT — STATIC VERIFIED — RUNTIME TEST REQUIRED**

## User-reported problem

The Company Fleet screen showed `Assigned tow yard: Not assigned`, but the selected Fleet Book truck had no button to choose or save a tow-yard assignment.

## Correction

v0.3.4 adds:

- current-map RedFox tow-yard selector;
- Previous Tow Yard / Next Tow Yard when multiple yards exist;
- `ASSIGN THIS TRUCK TO <yard name>`;
- `REMOVE THIS TRUCK'S TOW-YARD ASSIGNMENT`;
- persistent `assignedLevel`, `assignedYardId`, display-name, and timestamp metadata;
- migration-ready `assignedDriverId`, `assignedDriverName`, and `driverAssignmentStatus` fields for the future NPC employee/driver system.

## Safety boundary

This patch saves **RedFox business assignment metadata only**.

The new assignment function does not call:

- `career_modules_inventory.removeVehicle`;
- `career_modules_inventory.moveVehicleToGarage`;
- any vehicle deletion function;
- any vehicle creation or duplication function.

It does not move the normal RLS vehicle, change ownership, change inventory ID, create an artificial garage, charge money, or start a delivery timer.

The failed v0.3.0 company-record movement and v0.3.1 artificial-garage behavior remain safety-locked.

## Static verification

- ZIP CRC/integrity: PASS
- Exact ZIP re-extraction: PASS
- Duplicate ZIP entries: none
- Case-insensitive duplicate paths: none
- Path traversal entries: none
- Lua parse through `texlua loadfile`: PASS
- Lua top-level execution with mocked BeamNG loader globals: PASS
- JSON parsing: PASS
- Main module status version: 0.3.4
- Garage Hub required functions: PASS
- Eight top navigation sections: PASS
- Protected stock Career/RLS paths: none
- Re-extracted inventory hash verification: 69 files PASS
- Main Lua SHA-256: `49984aeb82aaace46aa311907e6acaa856f5275be9f40e89e1eadff3a520f725`

## Runtime proof required

David must verify that assignment persists after UI close and Career reload, while the truck remains exactly once in normal RLS My Vehicles with unchanged ownership, inventory identity, location, and no fee or delivery timer.

NPC driver creation, driving, payroll, schedules, convoy behavior, and autonomous call completion are not implemented or claimed in v0.3.4.
