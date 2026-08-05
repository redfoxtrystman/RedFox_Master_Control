# RF-PSI14 v0.2.8 Working-Code Clean Release Audit

Source baseline: `14-RedFox_PSIController_v0_2_6_APlusTirePressureCompat.zip`
Source SHA-256: `93d20b6d5dc9ee7c3e430b6e67f3a6a949fd5d723d8707348161be0d6eb97d65`

Output ZIP: `14-RedFox_PSIController_v0_2_8_WorkingCode_CleanRelease.zip`
Output size: `47740` bytes
Output SHA-256: `b9175e31e4e9a0fea2c9a8bcd4a2d7815efc7744eadad14e6e12760bf987fa69`
Final file count: `15`

## Rule for this build

This package is a rollback-style cleanup from the last working code package. It does **not** add new metadata folders, icon files, image placeholders, release-audit files, or README rewrites inside the mod. It only removes development diff artifacts from v0.2.6.

## Removed files

- `REDFOX_DIFF_REPORT_v0_2_0.html`
- `REDFOX_DIFF_REPORT_v0_2_1.html`
- `REDFOX_DIFF_REPORT_v0_2_2.html`
- `REDFOX_DIFF_REPORT_v0_2_3.html`
- `REDFOX_DIFF_REPORT_v0_2_4.html`
- `REDFOX_DIFF_REPORT_v0_2_5.html`
- `REDFOX_DIFF_REPORT_v0_2_6.html`
- `REDFOX_DIFF_SUMMARY_v0_2_0.txt`
- `REDFOX_DIFF_SUMMARY_v0_2_1.txt`
- `REDFOX_DIFF_SUMMARY_v0_2_2.txt`
- `REDFOX_DIFF_SUMMARY_v0_2_3.txt`
- `REDFOX_DIFF_SUMMARY_v0_2_4.txt`
- `REDFOX_DIFF_SUMMARY_v0_2_5.txt`
- `REDFOX_DIFF_SUMMARY_v0_2_6.txt`
- `REDFOX_DIFF_ui_modules_apps_redfoxPSIQuickControls_app.js.txt`
- `REDFOX_DIFF_ui_modules_apps_redfoxPSIQuickControls_app.json.txt`

## Kept files

- `RedFox_PSI_Controller_README.txt`
- `lua/ge/extensions/core/input/actions/redfoxPSIController.json`
- `lua/ge/extensions/redfox/modules/redfox_psi_controller/redfox_module.json`
- `lua/ge/extensions/redfoxPSIController.lua`
- `lua/ge/extensions/redfoxPSIControllerNative.lua`
- `lua/ge/extensions/redfoxTireSealant.lua`
- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `lua/vehicle/extensions/redfoxpartrepair.lua`
- `scripts/redfoxPSIController/modScript.lua`
- `settings/redfox/psi_controller_settings.json`
- `settings/redfoxPSIController/config.json`
- `ui/modules/apps/redfoxPSIController/app.js`
- `ui/modules/apps/redfoxPSIController/app.json`
- `ui/modules/apps/redfoxPSIQuickControls/app.js`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`

## Final verification

- Final ZIP reopened: PASS
- `zip.testzip()`: PASS
- Final ZIP extracted and file hashes compared to clean tree: PASS
- JSON validation errors: `[]`
- JavaScript syntax errors: `[]`
- Required files missing: `[]`
- Unexpected `mod_info/` files: `[]`
- Anti-spam scan counts: `{'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0}`

## Important limitation

Lua was statically scanned only; no `lua`/`luac` runtime is installed in this environment. BeamNG runtime is still unproven until David tests the exact ZIP.
