# RF-PSI14 v0.3.2 All-4 / Axle Hint Audit

Source baseline: `14-RedFox_PSIController_v0_3_1_BeamNG039LowPSIVisual.zip`
Output ZIP: `14-RedFox_PSIController_v0_3_2_All4_AxleHintAudit.zip`
Output size: `55042` bytes
Output SHA-256: `998ef6819ef80312eead68f6f44f94bae4cc9926ebd9eeb376c8fbdba4e408df`
Final file count: `17`

## David report

D-Series compact GM UI appeared mapped wrong: Front acted like left side and Rear acted like right side. David also asked for a compact UI checkbox/button so changing one front/rear pressure can apply to all four tires.

## Changed files

- `ui/modules/apps/redfoxPSIQuickControls/app.js`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`
- `ui/modules/apps/redfoxPSIController/app.json`
- `lua/ge/extensions/redfoxPSIController.lua`
- `lua/vehicle/extensions/auto/redfoxPSIController.lua`

## Patch summary

- Added `All 4` checkbox to compact GM UI header.
- When `All 4` is ON, compact F/R plus/minus commands send `airUpAll` / `airDownAll` instead of front/rear-only commands.
- When `All 4` is ON, compact Set sends `setAllPSI` so both targets are the same and all tire groups receive the same target in one user action.
- Added GE commands: `airUpAll`, `airDownAll`, and `setAllPSI`.
- Added vehicle export `setTargetAllPSI` for a direct backend all-tire command path.
- Tightened `pressureAxleHint()` so generic `_R` / right-side text is no longer treated as rear axle. This is intended to reduce side-split tires being mislabeled as front/rear.

## Verification

- Final ZIP reopened: PASS
- `zip.testzip()`: PASS
- Final ZIP extracted: PASS
- File list matches expected output tree: PASS
- JSON validation errors: `[]`
- JavaScript syntax errors: `[]`
- Anti-spam scan counts: `{'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0}`

## Important limitation

Lua was statically scanned only; this environment does not have Lua/luac installed. BeamNG runtime still needs David test.

## Test focus

1. Disable older PSI zips.
2. Install only v0.3.2.
3. Test D-Series compact UI with `All 4` OFF: check whether F/R no longer maps left/right from the generic `_R` hint.
4. Turn `All 4` ON and use F/R plus/minus and Set: all four tires should receive the same target.
5. Confirm no idle console spam.
6. Confirm low-PSI visual behavior from v0.3.1 is preserved.
