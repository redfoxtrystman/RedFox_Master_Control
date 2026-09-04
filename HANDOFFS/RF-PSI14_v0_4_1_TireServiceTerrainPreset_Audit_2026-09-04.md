# RedFox PSI Controller v0.4.1 Tire Service / Terrain Preset Audit

Status: NEEDS TEST. Static/package checks only. Lua runtime checker unavailable.

## Source
- Baseline ZIP used in this container: `14-RedFox_PSIController_v0_3_5_RLS2701_TireCompatSafeMode.zip`
- Baseline SHA-256: `1ca4b25f17e8847d27913e9f561bdabe12365ff208f55885a636b4126c08f244`
- Rollback baseline preserved: use `14-RedFox_PSIController_v0_3_5_RLS2701_TireCompatSafeMode.zip` if v0.4.1 misbehaves.

## Output
- Output ZIP: `14-RedFox_PSIController_v0_4_1_TireServiceTerrainPreset_Audit.zip`
- Output SHA-256: `20c08da4dcbf0b5694baec0880baabd48a097e5f078379a9ce6225713fc1c349`
- Output size: `63702` bytes

## RLS 2.7.0.3 status
The actual RLS 2.7.0.3 archive was not present in this runtime, so this build does not claim RLS 2.7.0.3 compatibility. Keep RLS 2.7.0.1 as the working baseline until the 2.7.0.3 ZIP is uploaded and byte-for-byte compared.

## Exact changed paths
- `lua/ge/extensions/redfoxPSIController.lua`
- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `ui/modules/apps/redfoxPSIController/app.js`
- `ui/modules/apps/redfoxPSIController/app.json`
- `ui/modules/apps/redfoxPSIQuickControls/app.js`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`

## Findings before edit
1. Current tire-only path in the available baseline had been changed to non-destructive pop/deflate behavior, so it could not visually remove the rubber from the rim.
2. Earlier nil `spikeStripPopWheel` reports match a Lua scoping problem when a helper is called before its local declaration; v0.4.1 adds a forward declaration and makes the helper visible to earlier code.
3. Full UI bulk removal iterated all `wheelTargets`. That is dangerous if cached/nearby/owned vehicle wheel layouts are included. v0.4.1 limits destructive bulk service to the active/player vehicle.
4. The compact app had no terrain pressure presets.

## Changes
- Restored physical Tire Only visual-removal attempt using only tire beam lists: `sideBeams`, `treadBeams`, `peripheryBeams`, `reinfBeams`, and `pressuredBeams`.
- Full Wheel/Rim uses only exact wheel/rim breakGroup logic. It does not fall back to hub/axle/chassis beam breaking.
- Remove All is active/player-vehicle scoped in GE and UI.
- If All 4 is checked in the full UI, Apply Selected now performs the selected service mode across all active vehicle wheels.
- Compact UI gained manual terrain PSI presets: Asphalt 34, Dirt 26, Mud 18, Rock 12, Sand 14.
- Preset click sets both front and rear target PSI and enables All 4 for the quick app.

## Preserved
- RLS 2.7.0.1 tire-provider safe-mode logic from the available baseline.
- Pressure setting and All 4 PSI behavior.
- BeamNG 0.39 HUD app structure.
- Save/settings sync paths.
- No `mod_info` folder added.
- No background polling added.

## Static checks
- Output ZIP opened/extracted: PASS
- ZIP integrity test: PASS
- JSON validation: PASS
- Full GM UI JS syntax via `node --check`: PASS
- Quick GM UI JS syntax via `node --check`: PASS
- No `setInterval`: PASS
- No `requestAnimationFrame`: PASS
- No `setTimeout(fetchStats)`: PASS
- Old no-pressure spam string absent: PASS

## BeamNG runtime checklist
1. Disable all older PSI ZIPs.
2. Install only v0.4.1.
3. Stay on RLS 2.7.0.1 unless testing a separate RLS 2.7.0.3 audit build.
4. Spawn a simple 4-wheel D-Series outside Career first.
5. Open full PSI UI and confirm wheel buttons are selectable without toggling Rim Race Assist.
6. Select Tire Only and remove one front tire; confirm rubber visually leaves the rim and the truck does not unload.
7. Select a rear tire and remove it; confirm rear tire behavior matches front.
8. Check All 4, select Tire Only, click Apply Selected; confirm all active vehicle tires are targeted.
9. Select Full Wheel/Rim, check All 4, click Apply Selected; confirm only the active vehicle is targeted.
10. Open compact PSI and click Asphalt/Dirt/Mud/Rock/Sand presets; confirm front/rear targets update and Set pressure works.
11. Do not run Remove All in a real Career save until the active-vehicle scope passes in freeroam.
12. If MD/RLS trucks unload on physical tire remove, stop and send logs; that vehicle needs a vehicle-specific JBeam adapter, not more broad beam-breaking.
