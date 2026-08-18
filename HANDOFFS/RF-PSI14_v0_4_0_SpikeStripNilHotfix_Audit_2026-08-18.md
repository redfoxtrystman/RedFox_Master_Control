# RF-PSI14 v0.4.0 SpikeStrip Nil Hotfix Audit

Source baseline: `14-RedFox_PSIController_v0_3_9_PhysicalRemoveToggle_Audit.zip`

Output ZIP: `14-RedFox_PSIController_v0_4_0_SpikeStripNilHotfix.zip`

## User-reported evidence checked

The log diagnosis reported `redfoxPSIController.lua:1094` crashing with:

```text
attempt to call global 'spikeStripPopWheel' (a nil value)
```

while `rlsTireProvider` was active.

## Confirmed cause

In the vehicle auto extension, `safeTireOnlyDisable()` called `spikeStripPopWheel(w, false)` before the helper was declared. In Lua, a later `local function spikeStripPopWheel(...)` is not visible to earlier functions unless the local is forward-declared first. That made the earlier call resolve as a global, which was nil.

## Changed files

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`

## Code change summary

- Added a forward declaration before `safeTireOnlyDisable()`:
  - `local spikeStripPopWheel`
- Changed the later helper definition from local declaration form to assignment form:
  - `function spikeStripPopWheel(w, playSound)`
- Guarded the safe-disable call so the vehicle path falls back to pressure/visual disable instead of crashing if the helper is unavailable.

## Preserved

- RLS 2.7.0.1 tire compatibility safe mode
- Active-vehicle-only bulk service guard
- Physical remove toggle behavior from v0.3.9
- BeamNG 0.39 HUD files
- Save/settings sync
- No background polling
- No `mod_info/` folder

## Static/package verification

- Final ZIP opened/extracted: PASS
- ZIP integrity: PASS
- JSON validation: PASS
- Full GM UI JavaScript syntax: PASS
- Quick GM UI JavaScript syntax: PASS
- Forward declaration present: PASS
- Later helper assignment present: PASS
- Old `local function spikeStripPopWheel` removed: PASS
- Safe-disable call guarded: PASS
- No `setInterval`: PASS
- No `requestAnimationFrame`: PASS
- No `setTimeout(fetchStats)`: PASS
- Old no-pressure spam string absent: PASS

## Limitation

Lua runtime testing was not performed in BeamNG. This is static/package verification only.
