# Approval-Ready User State Cleanup Plan

Generated local time: 2026-08-10

Purpose:
Prepare a safe, step-by-step cleanup plan for stale BeamNG user-state noise if David's first clean-lane test still produces confusing errors.

## Status

This is a plan only.

No BeamNG game files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.
No files were moved, deleted, or renamed.

Verification labels:

- `static_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## Why This Exists

The Steam/common active mods folder is clean enough for the first recovery test:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

However, the BeamNG user folder still has stale state that can create misleading log noise.

User folder:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current`

Latest observed runtime log:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

Latest observed log time:
2026-08-09 10:36:48 AM

No fresh post-clean-lane runtime log exists yet.

## Files To Protect Before Any Cleanup

Do not clean anything until David approves it.

Before any user-state cleanup, make a fresh backup of at least these files/folders:

- `D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\repo\ModConflictResolver.zip`
- `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\inputmaps\keyboard.diff`
- `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\inputmaps\xidevice.diff`
- `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\ui_apps\layouts\default\career.uilayout.json`
- `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\RLS\phoneLayout.json`
- `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\cloud\game-state.json`

Existing broad user-state backup from earlier recovery:

`D:\RedFoxMods\backups\beamng_v039_user_state_pre_recovery_20260809_230211.zip`

Even with that existing backup, make a fresh small pre-cleanup backup before touching these files.

## Current Stale/Polluting State

### Possible User-Side Active Mod

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\repo\ModConflictResolver.zip`

- length: 45,591 bytes
- last write: 2026-08-09 10:22:56
- title: `Mod Conflict Resolver`
- tagid: `M6CZKT7NV`
- version: `0.5.1`

Current `settings\cloud\mods-optout.json` contains:

- `MK4P6ER2H`
- `MT1HJRZ2E`
- `MR9HXTC4O`

It does not contain:

- `M6CZKT7NV`

Risk:
This may still load from the user repo folder and may create extra behavior in the clean-lane test.

### Stale RedFox Input Bindings

`keyboard.diff`

- length: 2,307 bytes
- last write: 2026-08-05 09:21:29

`xidevice.diff`

- length: 1,556 bytes
- last write: 2026-08-05 09:21:29

Targeted search found 23 RedFox-related action binding references.

Keyboard references include:

- `redfoxInventoryToggleUI`
- `toggleRedFoxModulesHub`
- `redfox_tow_recovery_toggle`
- `toggleRedFoxRaceManager`
- `redfox_spawner_toggle`
- `redfox_winch_extend`
- `redfoxPlayerMovementToggleUI`
- `redfoxGravityToggleUI`
- `redfox_career_dev_toggle_launcher`
- `redfox_winch_pull`

Controller references include:

- `redfox_psi_airUpFront`
- `redfox_psi_airDownFront`
- `redfox_psi_airUpRear`
- `redfox_psi_resetPressure`
- `redfoxTurboBoost`
- `redfox_psi_airDownRear`

Risk:
These can produce missing-action log noise while only GarageHub and RaceBuilder are active.

### Stale Career UI Layout

`career.uilayout.json`

- length: 6,156 bytes
- last write: 2026-08-09 10:15:36

Stale inactive RedFox UI app references:

- line 142: `redfoxTurboBoost`
- line 179: `redfoxTowHookHelper`
- line 240: `redfoxPsiQuickControls`
- line 252: `redfoxPhantomCloak`

Risk:
Opening Career during the first test may trigger errors for inactive apps unrelated to GarageHub or RaceBuilder.

### RLS Phone Layout State

`settings\RLS\phoneLayout.json`

- length: 546 bytes
- last write: 2026-08-09 10:24:03

Saved layout includes:

- version: 8
- page app: `redfox-browser`

Risk:
Opening the RLS phone during the first test can make the log look like a web/RLS failure even before RLS is being tested.

### Last Level State

`settings\cloud\game-state.json`

- length: 1,063 bytes
- last write: 2026-08-06 23:58:41
- last level: `redfox_jump_grid`

Risk:
If BeamNG tries to resume or remember this level, David should manually choose Freeroam Small Grid for the clean-lane test.

## Approval Gate

Do not do any cleanup before the first clean-lane runtime test unless David explicitly approves it.

First test should still be:

1. Launch BeamNG.
2. Choose Freeroam.
3. Choose Small Grid.
4. Do not enter Career.
5. Do not open the RLS phone.
6. Do not press old RedFox hotkeys.
7. Test Hub Scan once.
8. Open/check RaceBuilder basic visibility.
9. Exit BeamNG.
10. Let Codex inspect the fresh `beamng.log`.

## If The First Test Is Noisy Or Fails

Only after David approves cleanup, try one cleanup layer at a time.

### Cleanup Layer 1: Disable User-Side ModConflictResolver

Goal:
Make the clean-lane test actually be only GarageHub and RaceBuilder.

Suggested safe action:
Move `ModConflictResolver.zip` out of:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\repo`

into a timestamped backup folder under:

`D:\RedFoxMods\backups`

Then rerun Freeroam Small Grid and inspect a fresh log.

### Cleanup Layer 2: Filter Old RedFox Input Bindings

Goal:
Remove missing-action noise for inactive RedFox projects.

Suggested safe action:

1. Back up `keyboard.diff` and `xidevice.diff`.
2. Remove only bindings for inactive RedFox actions.
3. Preserve bindings for active clean-lane mods:
   - `toggleRedFoxModulesHub`
   - `toggleRedFoxRaceManager`

Then rerun Freeroam Small Grid and inspect a fresh log.

### Cleanup Layer 3: Filter Old Career UI Layout

Goal:
Stop Career from trying to load inactive RedFox UI apps when Career testing begins later.

Suggested safe action:

1. Back up `career.uilayout.json`.
2. Remove inactive app entries:
   - `redfoxTurboBoost`
   - `redfoxTowHookHelper`
   - `redfoxPsiQuickControls`
   - `redfoxPhantomCloak`
3. Do not test Career until Freeroam clean lane passes.

### Cleanup Layer 4: RLS Phone Layout Reset Or Filter

Goal:
Prevent stale `redfox-browser` phone layout state from confusing the isolated RLS test.

Suggested safe action:

1. Back up `settings\RLS\phoneLayout.json`.
2. Only modify/reset it after the Freeroam clean lane passes.
3. Do not mix this with Tow or JOB04/FoxNet testing.

## Stop Rule

After each cleanup layer:

1. Run exactly one test.
2. Inspect exactly the fresh `beamng.log`.
3. Do not perform the next cleanup layer unless the log proves it is needed.

Do not mark anything stable until David tests it in BeamNG and reports it working.
