# RF-PSI14 v0.3.9 Physical Remove Toggle Audit

Source baseline: `14-RedFox_PSIController_v0_3_8_MDTruckSafeTireDisable_UIEnable.zip`

Output ZIP: `14-RedFox_PSIController_v0_3_9_PhysicalRemoveToggle_Audit.zip`

Output size: `64883` bytes

Output SHA-256: `61ae932c3534f01e7913ce4df5eab92d21b63d598784dc656f4dbe11b5a5c0e5`

## User report

David reported that tire removal still did not actually remove tires after v0.3.8. v0.3.8 safe-disabled tires on RLS/MD/multi-wheel vehicles instead of physically breaking tire beams, because prior physical removal unloaded `md_series`.

## Changed files

- `lua/ge/extensions/redfoxPSIController.lua`
- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `ui/modules/apps/redfoxPSIController/app.js`
- `ui/modules/apps/redfoxPSIController/app.json`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`

## What changed

- Added `forcePhysicalTireRemove` setting in the GE controller.
- Added `setForcePhysicalTireRemove(enabled)` in the vehicle extension.
- Full GM UI now exposes a `Physical tire remove` checkbox with an explicit MD/RLS unload-risk warning.
- Destructive tire service remains locked to active/player vehicle only.
- Default remains safe-disable on RLS/MD/multi-wheel trucks.
- When `Physical tire remove` is ON, tire-only service physically breaks tire beams even on RLS/MD/multi-wheel vehicles. This is risky and may reproduce vehicle unload errors.
- Tire-only physical removal now includes tread, side, periphery, reinforcement, and pressured beam lists.
- Remove All sends the physical-toggle state to the vehicle before running, but remains active-vehicle scoped.

## Verification

- Final ZIP opened/extracted: PASS
- ZIP integrity `testzip`: PASS
- JSON validation: PASS
- Full GM UI JavaScript syntax: PASS
- Quick GM UI JavaScript syntax: PASS
- No `setInterval`: PASS
- No `requestAnimationFrame`: PASS
- No `setTimeout(fetchStats)`: PASS
- Old no-pressure spam string absent: PASS

## Runtime warning

BeamNG runtime is unproven. Physical tire removal on RLS/MD/multi-wheel vehicles previously unloaded the truck. This build exposes it as an explicit opt-in toggle instead of pretending safe-disable is real removal.

## Test order

1. Disable all older PSI zips.
2. Install only v0.3.9.
3. Test a normal 4-wheel vehicle first with Physical tire remove OFF and ON.
4. For MD/RLS/multi-wheel trucks, Physical tire remove OFF will safe-disable only and will not visually remove the tire.
5. To test actual visual tire removal on MD/RLS/multi-wheel trucks, turn Physical tire remove ON and use Tire Service carefully. Stop if `Error loading vehicle` returns.
6. Confirm Remove All still affects active vehicle only.
