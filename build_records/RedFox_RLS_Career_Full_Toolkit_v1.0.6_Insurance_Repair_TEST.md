# RedFox RLS Career Full Toolkit v1.0.6 — Insurance Repair Test

## Base

Built from `RedFox_RLS_Career_Full_Toolkit_v1.0.5_RedFox_Tow_Teleport_TEST.zip`.

## User-save diagnosis used as reference

The uploaded original `Profile 3.zip` was inspected only to determine the failure pattern. The source save was not bundled or modified by this build.

Confirmed pattern:

- Career inventory IDs 28 and 52 exist as owned Gavril D-Series vehicles.
- Those IDs are absent from RLS `insurance.invVehs`.
- The normal RLS insurance UI therefore has no vehicle insurance record to enroll.

## Changes

Added an `INSURANCE` page to the integrated Dev Toolkit with:

- Scan current Career vehicle insurance structure.
- Repair current Career vehicle insurance structure.
- Scan the entire garage.
- Repair all structurally missing/broken insurance records.
- Detection of missing record, `insuranceId`, class, and coverage-option structures.
- Repairs create the minimum eligible-but-uninsured state (`insuranceId = -1`).
- The normal RLS insurance UI remains responsible for selecting/purchasing a policy.

Insurance class selection order:

1. Valid class from another owned vehicle with the same model.
2. Insurance metadata already present on the vehicle.
3. Existing Daily Driver class object from the same Career save.

## Files changed

- `lua/ge/extensions/redfox/careerDevUnlocker.lua`
- `mod_info.json`
- `README.txt`
- `CHANGELOG.txt`
- Added `VERIFY_v1.0.6.json`

## Preserved behavior

Existing money, XP, Node Grabber, vehicle, garage, photo, and teleport feature entry points were retained.

## Safety

The repair logic does not intentionally change:

- money
- installed parts
- vehicle configuration
- mileage
- damage
- ownership
- purchase history

## Runtime status

Built and statically verified; runtime untested.

## Artifact

`RedFox_RLS_Career_Full_Toolkit_v1.0.6_Insurance_Repair_TEST.zip`

SHA-256: `be6b573d4b02aba85ebc98806e47dbcf2912545959b77bb89a99b17c53d55f9c`

## Test plan

Use the original unmodified Profile 3 save:

1. Enter the broken Gavril D-Series.
2. Open `INSURANCE`.
3. Press `SCAN CURRENT VEHICLE`.
4. Verify it reports `MISSING RECORD` or another structural defect.
5. Press `REPAIR CURRENT VEHICLE`.
6. Open the normal RLS insurance screen and assign a policy.
7. Save and reload Career.
8. Confirm the vehicle remains recognized by insurance.
