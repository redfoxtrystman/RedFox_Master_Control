# RF-PSI14 v0.3.0 BeamNG 0.39 Safe Tire / Pressure Patch Audit

Status: NEEDS TEST — static/package verification only

## User report

David reported that after the BeamNG 0.39 update:

- taking tires/wheels off a vehicle caused an `Error loading vehicle` popup on vehicle `rockbouncer`;
- tire PSI still did not visibly drop to the requested value such as 2 PSI;
- pressure moved a little but not enough;
- the code needs review.

Screenshot observed: BeamNG popup says `Error loading vehicle`, vehicle `rockbouncer`, possible reasons `Broken or outdated mods` / `Corrupted files`.

## Source baseline

Input ZIP: `14-RedFox_PSIController_v0_2_9_BeamNG039Hotfix.zip`

## Changed files

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `lua/ge/extensions/redfoxPSIController.lua`

## What was found

### 1. Destructive tire/wheel removal risk

The vehicle Lua could still break tire beams or wheel/rim break groups directly:

- tire-only remove broke tire beam lists;
- full wheel/rim remove attempted break-group removal.

On some vehicles/mods, especially rock crawler / rock bouncer style vehicles, breaking those beams from a UI button can corrupt enough vehicle structure to trigger BeamNG's `Error loading vehicle` behavior.

### 2. PSI change was too dependent on the throttled update loop

Set front/rear PSI stored a pressure target and relied on the update loop to walk toward the target over time. With manual-action throttling and odd pressure-group styles, that could result in only a small pressure movement instead of the requested visible change, such as going to 2 PSI.

## What v0.3.0 changes

### Safe tire service behavior

- Full wheel/rim removal is disabled in safe mode.
- Full wheel/rim removal now reports unsupported instead of breaking hub/suspension/rim groups.
- Tire-only remove no longer breaks tire beams.
- Tire-only remove now uses the existing spike-strip-style deflate/soften path instead of destructive beam removal.

This is less visually aggressive but much safer for BeamNG 0.39 and mod vehicles.

### Immediate PSI apply behavior

- Added `applyPressureNowToList()`.
- `setTargetFrontPSI()` now classifies wheels and applies the requested pressure immediately to front pressure groups.
- `setTargetRearPSI()` now classifies wheels and applies the requested pressure immediately to rear pressure groups.
- Shared pressure groups still apply to both front and rear.
- The manual-action throttle remains; no background polling was added.

### UI result message

- GE `onVehicleDetachResult()` now has a specific `unsupported` message so full wheel/rim removal safe-mode refusal is not shown as “target does not exist.”

## Verification performed

- Final ZIP reopened: PASS
- Final ZIP extracted: PASS
- ZIP integrity check: PASS
- JSON validation: PASS
- Full GM UI JavaScript syntax: PASS
- Quick GM UI JavaScript syntax: PASS
- No `setInterval`: PASS
- No `requestAnimationFrame`: PASS
- No `setTimeout(fetchStats)`: PASS
- Old `No wheels with pressure groups found` spam string absent: PASS
- No `mod_info/` folder added: PASS

Lua runtime syntax checker was unavailable in this environment, so Lua was text/static checked only.

## Final output

Output ZIP: `14-RedFox_PSIController_v0_3_0_BeamNG039SafeTirePressure.zip`

Size: 58,490 bytes
SHA-256: `289493b1c4237aac72d4378d612b4cfc18a9fdc9239d33fc065d1acdb4252b03`
File count: 17

## David test checklist

1. Disable all older PSI zips.
2. Install only `14-RedFox_PSIController_v0_3_0_BeamNG039SafeTirePressure.zip`.
3. Load a normal vehicle first.
4. Open/add RedFox Tire Control and RedFox PSI Quick Controls from HUD Apps.
5. Click Refresh.
6. Set front/rear PSI to 2 PSI and confirm the UI and tire behavior drop immediately or much more visibly.
7. Try tire-only remove/pop on a normal vehicle.
8. Try rockbouncer tire-only remove/pop and confirm no `Error loading vehicle` popup.
9. Do not expect full wheel/rim removal to work in this build; it is intentionally disabled in safe mode.
10. Test A+ Gladiator tires separately.
11. Watch console for idle spam.

## Important limitation

This build intentionally prioritizes not corrupting vehicles over full visual wheel removal. Full wheel/rim removal needs a vehicle-specific safe remover before it should be enabled again.
