# RF-PSI14 v0.3.5 RLS 2.7.0.1 Tire Compatibility Safe Mode Audit

Status: NEEDS TEST — static/package verification only

## Source baseline

- PSI baseline: `14-RedFox_PSIController_v0_3_4_SaveSync_FloatVisibleAudit.zip`
- LRS/RLS inspected archive: reassembled from split upload as `/mnt/data/rls_2701_work/combined.zip`
- RLS archive entries inspected: 4,955

## RLS 2.7.0.1 findings relevant to PSI

RLS now includes a full tire/wear/maintenance stack:

- `lua/common/rls_tire_model.lua`
- `lua/ge/extensions/career/modules/tireSystem.lua`
- `lua/vehicle/extensions/auto/rlsTireProvider.lua`
- `lua/vehicle/extensions/burnoutTireWear.lua`
- `lua/ge/extensions/career/modules/maintenanceComputer.lua`
- `lua/ge/extensions/career/modules/maintenanceMode.lua`
- `lua/ge/extensions/vehicleMaintenance.lua`
- `lua/vehicle/extensions/maintenanceManager.lua`
- `lua/vehicle/extensions/individualRepair.lua`
- `lua/ge/extensions/overrides/career/modules/partShopping.lua`

Important behavior found:

- RLS `rlsTireProvider` can deflate tires through `beamstate.deflateTire(index)`.
- RLS keeps tire `flat` state in its own wheel state and reports it to `career_modules_tireSystem.receiveVehicleState(...)`.
- RLS can re-apply stored flat state: when RLS state says a tire is flat but Beam says it is not physically flat, it calls `beamstate.deflateTire(index)` again.
- RLS sends tire context with `rlsTireProvider.configure(...)` from the career tire system.
- RLS flushes/resets tire provider during vehicle ownership/part changes and maintenance operations.

## Compatibility risk

RedFox PSI self-sealing/repair tries to clear Beam flat/leak flags and restore tire pressure. Under RLS 2.7.0.1, RLS may immediately re-deflate the tire from its stored tire state. That can cause repair loops, hiss/green sealant returning, settings confusion, and pressure seeming to change only a little.

## v0.3.5 patch scope

Changed file:

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`

Changes:

- Added RLS tire provider detection for `rlsTireProvider`.
- Added RLS compatibility mode, default ON.
- When RLS tire provider is active, RedFox automatic self-sealing is paused.
- When RLS tire provider is active, RedFox leak-flag clearing is skipped.
- When RLS tire provider is active, RedFox repair hold is skipped.
- When RLS tire provider is active, hard tire restore becomes pressure-only and does not pretend to repair the RLS tire state.
- Pressure setting remains available.
- All 4, UI settings, and BeamNG 0.39 HUD changes are preserved from prior builds.
- Water float code is unchanged from v0.3.4; no new float claims are made.

## Output ZIP

- Output: `14-RedFox_PSIController_v0_3_5_RLS2701_TireCompatSafeMode.zip`
- Size: 63317 bytes
- SHA-256: `1ca4b25f17e8847d27913e9f561bdabe12365ff208f55885a636b4126c08f244`
- File count: 17

## Verification

- Final ZIP opened: PASS
- Final ZIP extracted: PASS
- ZIP integrity: PASS
- JSON validation errors: []
- JavaScript syntax errors: []
- Anti-spam scan: `{'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0}`
- `rlsOwnsTireFlatState` present: True
- `M.setRlsTireCompatMode` export present: True

Lua runtime syntax checker is unavailable in this environment. Static source/package checks only.

## Runtime test needed

Install only this PSI zip with RLS 2.7.0.1. Test pressure-only changes first. Then test RLS maintenance tire repair/replacement separately. RedFox self-sealing should not fight RLS tire state while RLS tire provider is active.
