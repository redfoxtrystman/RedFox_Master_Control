# RF-PSI14 v0.3.6 Tire Remove / Rim Restore Audit

Source baseline: `14-RedFox_PSIController_v0_3_5_RLS2701_TireCompatSafeMode.zip`
Output ZIP: `14-RedFox_PSIController_v0_3_6_TireRemove_RimRestoreAudit.zip`
Output size: `58768` bytes
Output SHA-256: `29812469fb1c6f79f75e7cac789cbd1fc3463bddb31e22dbad6cad9c93165605`
Final file count: `17`

## Reason

David reported that rims and tires do not remove anymore and that only Pop Tire works.

Static inspection confirmed the current v0.3.5 code still carried the v0.3.0 safe-mode behavior:

- Full Wheel/Rim returned unsupported instead of trying a wheel/rim breakGroup.
- Tire Only only deflated/softened the tire instead of physically removing tire beams.

## Changed file

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`

## Behavior change

- Restored Tire Only physical removal by breaking the selected wheel's tire/sidewall/tread/periphery/reinforcement beams.
- Restored Full Wheel/Rim mode using the older exact wheel/rim breakGroup path.
- Full Wheel/Rim still does not fall back to axle, suspension, or chassis beam breaking. If no safe wheel/rim breakGroup is found, it reports unsupported instead of breaking random vehicle structure.
- Preserved v0.3.5 RLS 2.7.0.1 tire compatibility safe mode for self-sealing/leak repair conflicts.
- Preserved pressure setting, All4, 0.39 HUD app work, settings sync, and no background polling.

## Verification

- Final ZIP reopened/extracted: PASS
- ZIP integrity: PASS
- JSON validation errors: `[]`
- JavaScript syntax errors: `[]`
- Anti-spam/static scan counts: `{'setInterval': 0, 'requestAnimationFrame': 0, 'setTimeout(fetchStats)': 0, 'No wheels with pressure groups found': 0, 'Safe mode: full wheel/rim remove disabled': 0}`

## Runtime warning

This is static/package verification only. Full Wheel/Rim is inherently riskier than Tire Only because it modifies wheel/rim break groups. Test on D-Series first, then rockbouncer. If the rockbouncer returns `Error loading vehicle`, stop using Full Wheel/Rim on that vehicle and keep to Tire Only / Pop.
