# RF-PSI14 v0.3.8 MD Truck Safe Tire Disable + UI Enable Audit

Source baseline: `14-RedFox_PSIController_v0_3_7_ActiveVehicle_TireRemoveSafety.zip`

Output ZIP: `14-RedFox_PSIController_v0_3_8_MDTruckSafeTireDisable_UIEnable.zip`
Output size: `59728` bytes
Output SHA-256: `a619b9f7a8660ff3734bdc9605f43e2fe4310d38b417f5b3ddc1355795ffd536`
File count: `17`

## User report

David reported that Tire Only now does something but it kills/unloads the MD truck, producing BeamNG `Error loading vehicle: md_series`. He also reported tire/rim controls start dimmed/disabled until toggling Rim Race Assist.

## Changed files

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `ui/modules/apps/redfoxPSIController/app.js`
- `ui/modules/apps/redfoxPSIController/app.json`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`

## Patch intent

- Stop Tire Only from physically breaking heavy/dually/RLS tire beams that can unload the vehicle.
- Keep normal four-wheel non-RLS vehicles on the physical tire-beam path.
- Keep destructive Remove All locked to active/player vehicle from v0.3.7.
- Stop stale `removed` state from disabling wheel selection/buttons until Rim Race Assist is toggled.

## Implementation notes

- Added `redfoxIsMultiWheelTruckLike()` and `safeTireOnlyDisable()` in vehicle Lua.
- When RLS tire provider is active or the vehicle has more than four wheel entries, Tire Only uses the safe deflate/flat/low-PSI visual path and marks that wheel removed in RedFox UI state instead of breaking MD/dually tire beams.
- Four-wheel non-RLS vehicles still physically break tread/side tire beams.
- Full Wheel/Rim path remains exact breakGroup only and remains risky/unsupported on some mod vehicles.
- Full GM UI no longer disables wheel selection just because cached state says a wheel is removed.
- Full GM UI requests a one-shot status refresh on open/load, not background polling.

## Verification

- Final ZIP opened/extracted: PASS
- ZIP integrity: PASS
- JSON errors: `[]`
- JS syntax errors: `[]`
- Anti-spam scan counts: `{'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0}`
- Required patch checks: `{'safe tire disable helper': True, 'multi wheel safe path': True, 'RLS physical break guard': True, 'UI refresh on load': True, 'wheel buttons selectable when removed/stale': True}`

## Limitation

Lua runtime syntax checker is unavailable in this environment. Static/package verification only; BeamNG runtime is still NEEDS TEST.
