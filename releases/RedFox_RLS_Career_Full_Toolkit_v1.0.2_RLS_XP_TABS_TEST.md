# RedFox RLS Career Full Toolkit v1.0.2 — RLS XP Tabs Test

## Status

BUILT — RUNTIME UNTESTED

## Base

- `RedFox_RLS_Career_Full_Toolkit_v1.0.1_INTEGRATED_UI_TEST.zip`

## Artifact

- `RedFox_RLS_Career_Full_Toolkit_v1.0.2_RLS_XP_TABS_TEST.zip`
- SHA-256: `e70752eb069544649c9d2f81ec6ee45263a79a99eccd1a37d39484a0ac58f5c1`

## Changes

- Added top navigation tabs: Tools, Economy, XP, and Vehicle.
- Added an RLS-aware XP page.
- XP categories are discovered from the active Career branch registry through `career_branches.getSortedBranches()`.
- Added current XP display for each detected progression attribute.
- Added selected-category Add, Remove, Set, Zero, and Max controls.
- Added Add XP To All, Set All XP, and Max All XP controls.
- Added current Money and Voucher displays.
- Preserved integrated Node Grabber controls.
- Preserved Garage Hub theme support.

## Known RLS progression fallbacks

The runtime scanner can also recognize these known keys when present:

- `beamXP`
- `logistics-delivery`
- `careerSkills-police`
- `careerSkills-bus`
- `careerSkills-paramedic`
- `careerSkills-taxi`
- `careerSkills-repo`
- `careerSkills-gambling`
- `careerSkills-stamina`
- `careerSkills-civilService`

## Testing requirements

1. Back up the Career save.
2. Disable older standalone Cheat Tools, Node Grabber, and Full Toolkit ZIPs.
3. Enable only v1.0.2.
4. Confirm all four tabs open.
5. Confirm the XP page lists active RLS branches and current values.
6. Test one small Add XP operation first.
7. Confirm the visible branch value and level change.
8. Test selected Set/Zero/Max only on a copied save.
9. Test All XP operations last because they may immediately trigger many level rewards and unlocks.
10. Confirm Node Grabber still works while seated in a vehicle.

## Static verification

- ZIP integrity: PASS
- Tab functions present: PASS
- Dynamic branch discovery present: PASS
- Selected XP actions present: PASS
- All-XP actions present: PASS
- Integrated Node Grabber functions present: PASS

## Rollback

Disable or remove v1.0.2 and restore v1.0.1. Do not test XP modification on an irreplaceable Career save.
