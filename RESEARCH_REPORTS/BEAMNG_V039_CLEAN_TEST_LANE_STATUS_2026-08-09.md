# BeamNG v0.39 RedFox Clean Test Lane Status

Date/time: 2026-08-09 23:14 PDT  
Scanner: Codex local RedFox workspace  
Runtime status: awaiting_user_test

## Purpose

This is a follow-up to `BEAMNG_V039_REDFOX_RECOVERY_REPORT.md`.

The earlier report captured the broken/stale state seen in the latest BeamNG logs. After that report, a backed-up clean test lane was prepared so David can launch BeamNG with only the first controlled RedFox recovery pair active.

## Verification Labels

- static_checked: current active mod folder, user mod cache folder, active ZIP metadata, action JSONs, and local BeamNG Vue UI mod README were inspected.
- code_compared: not applicable in this status note; no mod code was edited.
- zip_integrity_checked: active Hub and RaceBuilder ZIPs were opened and inspected for expected metadata/action files.
- awaiting_user_test: BeamNG has not been launched by David after this clean-lane setup.

## Backups Preserved

User state backup:

`D:\RedFoxMods\backups\beamng_v039_user_state_pre_recovery_20260809_230211.zip`

User mod-cache quarantine:

`D:\RedFoxMods\backups\beamng_v039_user_cache_quarantine_20260809_230455`

Former active mods hold folder:

`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822`

Manifest:

`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\active_mods_hold_and_test_install_manifest.csv`

Report copy:

`D:\RedFoxMods\reports\beamng_v039_update_scan_20260809\active_mods_hold_and_test_install_manifest_20260809_230822.csv`

## Current Active BeamNG Mods Folder

Folder:

`D:\Games\Steam\steamapps\common\BeamNG.drive\mods`

Only these RedFox test ZIPs are active:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

Non-mod files still present:

- `beam_manager.bmc`
- `desktop.ini`
- `download.png`
- `folderico-red.ico`
- `IMG_4250.webp`

The previous top-level mod folders and third-party map ZIPs were moved into the hold folder, not deleted.

## User Mod Cache Current State

Folder:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods`

Current visible entries:

- `mod_manifests`
- `repo`

The stale `db.json`, old `mod_manifests`, and `ModConflictResolutions` folder were moved to the quarantine backup. This was done because the latest log and mod database referenced many RedFox ZIPs that no longer existed in the active folder.

## Active ZIP Evidence

Garage Hub ZIP:

`D:\Games\Steam\steamapps\common\BeamNG.drive\mods\1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`

Observed:

- `info.json` version: `0.5.11-race-manager-link`
- Contains action file: `lua/ge/extensions/core/input/actions/redfox_modules_hub.json`
- Provides action: `toggleRedFoxModulesHub`
- Purpose stated by ZIP metadata: fixes `msg()` scope in the module scanner and links Race/Event menu buttons to Race Manager bridge functions.

RaceBuilder ZIP:

`D:\Games\Steam\steamapps\common\BeamNG.drive\mods\37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

Observed:

- `info.json` version: `0.4.16.5`
- Contains `_redfox_dev_notes/`
- Contains action file: `lua/ge/extensions/core/input/actions/redfox_race_manager.json`
- Provides action: `toggleRedFoxRaceManager`
- Contains Hub manifest: `lua/ge/extensions/redfox/modules/redfox_race_manager/redfox_module.json`
- Hub manifest keeps `moduleId` as `redfox_race_manager` and `windowId` as `RedFoxRaceManager`

## Remaining Known Risk Before Runtime Test

The live keyboard binding file still includes RedFox actions for mods that are not currently installed in the clean lane.

File:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\inputmaps\keyboard.diff`

Expected valid in this clean lane:

- `toggleRedFoxModulesHub`
- `toggleRedFoxRaceManager`

Expected stale until their owning mods are reintroduced:

- `redfoxInventoryToggleUI`
- `propCarryToggle`
- `redfox_tow_recovery_toggle`
- `openPhone`
- `redfox_spawner_toggle`
- `rf_skyride_open_ui`
- `redfox_winch_extend`
- `redfoxPlayerMovementToggleUI`
- `SkyRidetoggle`
- `SkyRideModeToggle`
- `redfoxGravityToggleUI`
- `randomevents_toggle_menu`
- `redfox_career_dev_toggle_launcher`
- `redfox_winch_pull`

Do not edit this keyboard file yet unless David approves a backed-up keybind cleanup. If the next BeamNG launch still spams missing actions, the safe next action is to make a copy of `keyboard.diff`, keep only Hub/RaceBuilder bindings for the clean lane, and preserve the original in backups.

## v0.39 UI Direction

Local BeamNG README confirms supported Vue UI mods now live under:

`/ui/ui-vue/mods/%mod_name%/`

The README documents:

- Vue Single File Components
- Composition API
- Lua bridge usage
- pause menu button/tab registration through `ui_pause_actions`
- standalone route registration through `window.bngRoutes.add` and `ui_router_routeManager.registerModRoutes`

Official BeamNG v0.39 notes also identify v0.39 as the update that added Vue UI mod support.

Do not repair RedFox web by overriding `ui/ui-vue/dist/index.js`. Use a small RedFox-owned Vue adapter instead.

## David Runtime Test Needed

Launch BeamNG with the current clean lane and test only the installed pair first:

1. Start BeamNG.
2. Confirm the main menu loads.
3. Open the RedFox Garage Hub.
4. Click Hub Scan / Modules.
5. Confirm RaceBuilder appears as `RedFox Race Manager`.
6. Open RaceBuilder from Hub.
7. Test the RaceBuilder basics:
   - set start
   - add checkpoint
   - set finish
   - start race
   - finish race
   - view score card
   - save/load a race if possible
8. Exit BeamNG and send the new `beamng.log`.

## What This Proves Or Does Not Prove

If this works, it proves only that the Hub + RaceBuilder clean lane survives v0.39 far enough for the next recovery step.

It does not prove Tow/FoxNet, Surface Studio, Project 43 movement/weapons, Winch, Spawner, PSI, SkyRide, or third-party career stacks are fixed.

Runtime status remains `awaiting_user_test` until David tests in BeamNG.

## Next Repair Order After This Test

If Hub + RaceBuilder pass:

1. Bring back Surface Studio alone with Hub + RaceBuilder.
2. Bring back Material Proving Grounds only after Surface Studio is stable.
3. Bring back Tow/FoxNet using the v0.39 Vue adapter plan.
4. Bring back Project 43 movement/weapons only after restoring or guarding `core_redfoxPlayerMovementLab`.
5. Bring back Winch/Spawner/PSI/SkyRide/other keybind mods one at a time.

If Hub + RaceBuilder fail:

1. Do not add more mods.
2. Compare the new `beamng.log` against the pre-cleanup log.
3. If missing action spam dominates, do a backed-up clean-lane `keyboard.diff` filter.
4. If Hub scan fails, inspect only the active Hub ZIP and RaceBuilder manifest bridge before editing anything.
