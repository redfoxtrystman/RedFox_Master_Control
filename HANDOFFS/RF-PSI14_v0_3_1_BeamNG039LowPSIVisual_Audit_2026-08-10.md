# RF-PSI14 v0.3.1 BeamNG 0.39 Low-PSI Visual Patch Audit

Status: NEEDS TEST — static/package verification only

## User report

David reported:

- removing tires/wheels caused `Error loading vehicle` on `rockbouncer`;
- PSI changes a little, but not enough;
- tires do not go down to the old squishy / flat look at 2 PSI.

## Source baseline

Source ZIP: `14-RedFox_PSIController_v0_3_0_BeamNG039SafeTirePressure.zip`

v0.3.0 already moved tire-only removal away from destructive beam breaking and disabled destructive full wheel/rim removal. v0.3.1 adds a stronger low-PSI visual assist.

## Changed files

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`

No UI files were changed in v0.3.1.

## What was found

The pressure path could write pressure, but on BeamNG 0.39 and some mod tires the visible tire collapse/squish was weaker than older builds. The old `applySoftening()` thresholds and minimum factors were not aggressive enough for 2 PSI. Also, low pressure visual squish was not being forced immediately from a normal Set PSI action unless the tire was popped/deflated through the spike-strip-style path.

## What changed

### Stronger softening curve

The low-pressure softening constants were strengthened:

- softening starts at 12 PSI instead of 10 PSI;
- knee moved to 7 PSI;
- side/tread/periphery minimum stiffness factors were reduced so low PSI squishes more.

### New low-PSI visual assist

Added:

- `LOW_PSI_FORCE_VISUAL = 5`
- `LOW_PSI_HARD_FLAT = 2.5`
- `applyLowPressureVisual(w, psi)`

When the player intentionally sets 5 PSI or lower, the mod now applies stronger visual tire softening without marking the tire punctured/leaking. This is separate from tire popping, so self-sealing should not fight normal low-PSI tuning.

### Immediate low-PSI application

`applyPressureNowToList()` now:

- applies pressure immediately on click;
- writes the target pressure a small bounded number of times in the same click event for stubborn pressure groups;
- applies low-PSI visual squish immediately when requested PSI is 5 or lower;
- keeps manual-action anti-spam behavior.

### Service window for low PSI

Setting 5 PSI or lower keeps the manual service window active slightly longer so the low-pressure visual state is maintained without adding background spam.

## Preserved from v0.3.0

- Full wheel/rim removal remains disabled in safe mode.
- Tire-only removal remains non-destructive deflate/soften instead of beam breaking.
- BeamNG 0.39 HUD app icons from v0.2.9 remain.
- No `mod_info/` folder was added.
- No release packaging changes were made.

## Final ZIP

Output ZIP: `14-RedFox_PSIController_v0_3_1_BeamNG039LowPSIVisual.zip`

Size: `59186` bytes
SHA-256: `63c25e41246a7ed704bcf2daa36981128accd6b9a56ae9ef1759f94c6e11ea57`
File count: `17`

## Static/package verification

- Final ZIP reopened: PASS
- Final ZIP extracted: PASS
- ZIP integrity check: PASS
- JSON validation: PASS
- Full GM UI JavaScript syntax: PASS
- Quick GM UI JavaScript syntax: PASS
- `setInterval`: 0
- `requestAnimationFrame`: 0
- `setTimeout(fetchStats)`: 0
- old `No wheels with pressure groups found` spam string: 0
- low-PSI visual helper present: PASS

Lua runtime checker was not available in this environment; Lua was statically/text checked only.

## David test checklist

1. Disable all older PSI zips.
2. Install only `14-RedFox_PSIController_v0_3_1_BeamNG039LowPSIVisual.zip`.
3. Load a normal vehicle first.
4. Add/open RedFox Tire Control and RedFox PSI Quick Controls.
5. Click Refresh.
6. Set front/rear PSI to 2 PSI.
7. Confirm the tire visually squishes more than v0.2.9/v0.3.0.
8. Test rockbouncer tire-only remove/pop and confirm no `Error loading vehicle` popup.
9. Confirm full wheel/rim remove reports unsupported / safe mode instead of breaking the vehicle.
10. Test A+ Gladiator tires separately.
11. Watch for idle console spam.

## Important limitation

This is still not runtime-proven. If tires still do not visibly collapse enough, the next step is to inspect the exact tire JBeam and add a vehicle/tire-specific low-pressure adapter instead of guessing more global beam factors.
