# BeamNG v0.39 Clean Lane Static Assessment

Timestamp: 2026-08-10
Chat ID: RF-DOC01
Chat Name: Codex Desktop
Message type: read-only static assessment
Assigned role: recovery coordinator

Screen status = 🟨 NEEDS TEST

No BeamNG game files were edited.
No mod ZIPs were edited.
No files were moved, copied, deleted, or replaced in the active BeamNG mods folder.

Local full report:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\CLEAN_LANE_STATIC_ASSESSMENT_2026-08-10.md`

Verification labels:

- `static_checked`
- `zip_integrity_checked`
- `awaiting_user_test`

Runtime remains `awaiting_user_test` until David tests in BeamNG.

## Active Clean Lane

Active BeamNG mod folder:
`D:\Games\Steam\steamapps\common\BeamNG.drive\mods`

Active RedFox test ZIPs:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

No RLS, Tow, JOB04, JOB09, JOB13, Project 43, or map packs are active right now.

## GarageHub Finding

Active ZIP:
`1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`

Key static findings:

- `redfoxModulesHubAuto.lua` loads only `redfox/modulesHub`.
- `redfox_modules_hub.json` loads `redfox/modulesHub` and calls `extensions.redfox_modulesHub.toggleWindow()`.
- `modulesHub.lua` declares `local msg` before scanner helpers.
- `msg = function(s)` is assigned before `onExtensionLoaded()` calls `scanRedFoxModules()`.
- The known prior crash pattern, `attempt to call global 'msg' (a nil value)`, does not appear present in this active Hub build.

This does not prove Hub Scan works. It only means the known `msg()` nil issue appears patched by static inspection.

## RaceBuilder Finding

Active ZIP:
`37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

Key static findings:

- `redfoxRaceManagerAuto.lua` loads `redfox/raceManager`.
- `redfox_race_manager.json` loads `redfox/raceManager` and toggles `extensions.redfox_raceManager`.
- `redfox_module.json` is valid JSON.
- `redfox_module.json` has `redfoxModule: true`.
- `moduleId` is `redfox_race_manager`.
- Hub bridge functions point to `extensions.redfox_raceManager.*`, matching the extension path `lua/ge/extensions/redfox/raceManager.lua`.

This does not prove RaceBuilder opens or works. It only means the active ZIP has the expected Hub discovery/action structure.

## Next Action

David should run the clean-lane BeamNG test, load a simple map, try Hub/RaceBuilder briefly, exit, then Codex should inspect the fresh `beamng.log`.

Do not add RLS, RedFox Tow, JOB04/FoxNet, JOB13, maps, or tow packs until the clean lane has runtime evidence.

Coordinator action needed = yes
