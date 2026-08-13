# RF-PSI14 v0.3.4 Save Sync / Float Visible Audit

Status: NEEDS TEST — static/package verification only

Source baseline: 14-RedFox_PSIController_v0_3_3_SaveSettings_WaterFloatTest.zip
Output ZIP: 14-RedFox_PSIController_v0_3_4_SaveSync_FloatVisibleAudit.zip
Output size: 62309 bytes
Output SHA-256: 68c69879e4e751779122bf41415fb1d330b6176f1442215383e2c43c88da466e
Final file count: 17

## David report addressed

- Save/All 4/Self-Sealing reset after changing windows or opening the phone.
- Float only appeared in the compact quick UI.
- Float checkbox did not move the vehicle on water.
- Herbie bug mod contains a waterfloat system using water float nodes and water thrusters.

## Changed files

- lua/ge/extensions/redfoxPSIController.lua
- lua/ge/extensions/redfoxPSIControllerNative.lua
- lua/vehicle/extensions/auto/redfoxPSIController.lua
- settings/redfox/psi_controller_settings.json
- settings/redfoxPSIController/config.json
- ui/modules/apps/redfoxPSIController/app.js
- ui/modules/apps/redfoxPSIController/app.json
- ui/modules/apps/redfoxPSIQuickControls/app.js
- ui/modules/apps/redfoxPSIQuickControls/app.json

## Main changes

- Save settings now writes to both RedFox settings paths instead of one path only.
- Full GM UI now shows Save settings, All 4, and Float controls.
- WE/native UI now shows Save settings, All 4, and Water Float Assist controls.
- Compact UI keeps localStorage fallback for Save/All 4/Float/Self-Sealing so a HUD reload has a fallback while the GE core reloads its saved config.
- Float now detects water by checking actual vehicle nodes with obj:inWater(nodeId), based on the Herbie waterfloat pattern.
- Float now tries Herbie-style water thrusters when a vehicle has thrusters with water_thrusters/bug_water_thrusters in the part path.
- Float also tries safe pcall force hooks per underwater node when available.

## Verification

- Final ZIP reopened/extracted: PASS
- ZIP integrity: PASS
- JSON errors: []
- JavaScript syntax errors: []
- Anti-spam scan: {'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0}
- Lua runtime checker: unavailable in this environment; Lua was statically inspected only.

## Runtime warning

This is not BeamNG-proven. Water float may still only work on vehicles that expose compatible water nodes, water thrusters, or force APIs. The Herbie mod proves a waterfloat approach, but its physical float nodes are a vehicle part, not something a PSI UI mod can magically install into every vehicle at runtime.
