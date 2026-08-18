# RF-PSI14 v0.3.7 Active Vehicle Tire Remove Safety Audit

Status: NEEDS TEST — static/package verification only

Source baseline: `14-RedFox_PSIController_v0_3_6_TireRemove_RimRestoreAudit.zip`
Output ZIP: `14-RedFox_PSIController_v0_3_7_ActiveVehicle_TireRemoveSafety.zip`
Output size: `59257` bytes
Output SHA-256: `3afb6cc89c559aa05de06a6257ba411caedec07c6b76b918de6553b85e7596b7`
Final file count: `17`

## Reason for patch

David reported two serious tire service problems:

1. Tire Only remove still did not work.
2. Remove All removed rims/tires from all owned cars instead of only the current vehicle.

## Root causes found statically

- `breakWheelTireBeams()` used `count = count + ...` without declaring `local count = 0`, which can stop Tire Only / Full Wheel remove paths while Pop Tire still works.
- Full GM UI `removeAllDetected()` iterated every entry in `wheelTargets`. `wheelTargets` can include nearby/extra vehicle wheel layouts, so Remove All could send remove commands to more than the active vehicle.
- GE command handling accepted destructive tire service with arbitrary `targetVehId` from the UI.

## Files changed

- `lua/ge/extensions/redfoxPSIController.lua`
- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `ui/modules/apps/redfoxPSIController/app.js`
- `ui/modules/apps/redfoxPSIController/app.json`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`

## Safety changes

- Added active/player vehicle guard for destructive wheel service commands.
- `detachWheel`, `popWheel`, and `detachAllWheels` now use `sendActiveVehicleCommand()` instead of accepting non-active target vehicles.
- Full GM UI `removeAllDetected()` now filters wheel targets to the active vehicle only.
- Bulk button labels now say active vehicle to make the scope visible.
- Added `activeVehId` / `playerVehId` to stats for UI filtering.

## Tire remove changes

- Added missing `local count = 0` in `breakWheelTireBeams()`.
- Added `safeBreakBeam()` helper that tries beam `cid`, `id`, and list key so tire beam references have a better chance of matching BeamNG's expected breakBeam identifier.

## Preserved

- RLS 2.7.0.1 tire compatibility safe mode from v0.3.5.
- v0.3.6 wheel/rim exact breakGroup path.
- Pressure setting, All4, 0.39 HUD icons, settings sync, and no background polling.
- No mod_info folder added.

## Verification

- Final ZIP opened/extracted: PASS
- ZIP integrity: PASS
- JSON validation errors: `[]`
- JavaScript syntax errors: `[]`
- Anti-spam scan: `{'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0}`

## Runtime warning

Static checks do not prove BeamNG runtime behavior. Test first on D-Series with older PSI zips disabled. Do not use Remove All in a career save until active-vehicle scoping is confirmed by David.
