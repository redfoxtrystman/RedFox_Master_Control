# RF-PSI14 v0.3.3 Save Settings / Water Float Test Audit

Date: 2026-08-13
Status: NEEDS TEST — static/package verification only

## Source baseline

- Source ZIP: `14-RedFox_PSIController_v0_3_2_All4_AxleHintAudit.zip`
- Output ZIP: `14-RedFox_PSIController_v0_3_3_SaveSettings_WaterFloatTest.zip`
- Output size: `60708` bytes
- Output SHA-256: `4bba5f1cd0c883aa445f624f4b575a82967bd4faf6c5610132bf8f060f4e4ca6`
- Final file count: `17`

## David report / request

David reported:

- changing windows or bringing up the phone resets self-sealing and All 4;
- he wants a save settings checkbox;
- he asked whether the tires can be made super floaty so he can drive on water.

## Changed files

- `lua/ge/extensions/redfoxPSIController.lua`
- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `ui/modules/apps/redfoxPSIQuickControls/app.js`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`
- `ui/modules/apps/redfoxPSIController/app.json`

## Functional changes

### Compact UI persistence

Added config/stat fields:

- `quickSaveSettings`
- `quickAll4PSI`
- `waterFloatEnabled`

Compact GM UI now has:

- `Save` checkbox
- `All 4` checkbox
- `Float` checkbox

The compact UI now reloads these from shared GE stats instead of local defaults, so reopening/changing windows should not reset them when Save is enabled.

### Self-sealing persistence

Self-sealing already used the GE `runflatEnabled` setting, but the compact UI could visually reset when the Angular/HUD app reloaded. v0.3.3 preserves the displayed compact state by reading it from shared stats on app load/broadcast.

### Experimental water float

Added GE command/stat path and vehicle command:

- GE config: `waterFloatEnabled`
- GE command: `{waterFloatEnabled=true/false}`
- vehicle function: `setWaterFloat(enabled, strength)`

Vehicle Lua adds a guarded experimental float assist:

- only runs when `Float` is enabled;
- only attempts work if available water detection reports water;
- force API calls are feature-detected and wrapped with `pcall`;
- if the needed BeamNG force/water APIs are unavailable on a vehicle, it safely does nothing instead of throwing.

This is not runtime-proven. It may need a vehicle/tire-specific adapter if BeamNG 0.39 does not expose a usable force hook here.

## Preserved

- v0.3.2 All 4 command path
- v0.3.1 low-PSI visual squish path
- v0.3.0 safe tire service behavior
- no full wheel/rim destructive remove
- no `mod_info/` folder
- no background polling loop added

## Static verification

- Final ZIP reopened/extracted: PASS
- ZIP integrity: PASS
- JSON validation: PASS
- Full GM UI JavaScript syntax: PASS
- Quick GM UI JavaScript syntax: PASS
- No `setInterval`: PASS
- No `requestAnimationFrame`: PASS
- No `setTimeout(fetchStats)`: PASS
- Old no-pressure spam string absent: PASS

## Runtime test needed

David should test:

1. Disable all older PSI zips.
2. Install only `14-RedFox_PSIController_v0_3_3_SaveSettings_WaterFloatTest.zip`.
3. Open compact GM UI.
4. Turn `Save` ON.
5. Turn `All 4` ON.
6. Turn `Seal` ON.
7. Switch windows, open/close phone, reload HUD app if needed.
8. Confirm All 4 and Seal do not reset.
9. Turn `Float` ON near water and test if the vehicle gets additional buoyancy.
10. Turn Float OFF and confirm there is no idle spam or unwanted background behavior.

## Important limitation

The water float feature is experimental. It is intentionally gated and safe-wrapped, but the runtime effect cannot be proven without BeamNG. If it does nothing, the next step is a dedicated water-driving adapter for the exact target vehicle/tire JBeam.
