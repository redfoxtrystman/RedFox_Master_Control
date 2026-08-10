# User State Clean-Lane Pollution Check

Generated local time: 2026-08-10

Purpose:
Check whether the BeamNG user folder still contains old mod state that could pollute the first clean-lane runtime test.

## Status

This was a read-only inspection.

No BeamNG game files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.

Verification labels:

- `static_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## Runtime Evidence Check

No fresh BeamNG runtime log exists after the clean-lane setup.

Latest observed log:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

Latest observed log time:
2026-08-09 10:36:48 AM

## Active Steam/Common Mod Lane

Current active BeamNG mod folder:
`D:\Games\Steam\steamapps\common\BeamNG.drive\mods`

Active RedFox test ZIPs:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

No RLS, Tow, FoxNet, JOB04, JOB09, or JOB13 ZIP is currently in that active Steam/common mods folder.

## User-Folder Mod State

BeamNG user folder:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current`

The user-side `mods\mod_manifests` folder is empty.

The user-side repo mods folder still contains:

`mods\repo\ModConflictResolver.zip`

Its mod info identifies:

- title: `Mod Conflict Resolver`
- tagid: `M6CZKT7NV`
- version string: `0.5.1`
- filename: `ModConflictResolver.zip`

Current `settings\cloud\mods-optout.json` contains:

`MK4P6ER2H`, `MT1HJRZ2E`, `MR9HXTC4O`

It does not list:

`M6CZKT7NV`

Important conclusion:
`ModConflictResolver.zip` may still be enabled from the user repo folder unless BeamNG tracks its disabled state somewhere else. This means the first clean-lane test is probably "GarageHub + RaceBuilder + possible Mod Conflict Resolver", not a perfectly pure two-mod test.

Do not move or disable it without David's approval.

## Leftover RedFox Input Bindings

Current keyboard input map still references inactive RedFox actions:

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

Current controller input map still references inactive RedFox actions:

- `redfox_psi_airUpFront`
- `redfox_psi_airDownFront`
- `redfox_psi_airUpRear`
- `redfox_psi_resetPressure`
- `redfoxTurboBoost`
- `redfox_psi_airDownRear`

Important conclusion:
These bindings may create missing-action log noise while only GarageHub and RaceBuilder are active. They do not prove a mod is installed by themselves.

Do not clean input maps without David's approval.

## Leftover UI Layout State

Freeroam UI layout did not show RedFox hits in the targeted search.

Career UI layout still references inactive RedFox UI apps:

- `redfoxTurboBoost`
- `redfoxTowHookHelper`
- `redfoxPsiQuickControls`
- `redfoxPhantomCloak`

Important conclusion:
The first clean-lane test should be done in Freeroam on Small Grid, not Career. Opening Career may produce stale UI app errors unrelated to GarageHub or RaceBuilder.

Do not clean UI layouts without David's approval.

## Leftover RLS/RedFox Data State

The user settings folder still contains old RedFox data, including GarageHub, JOB13 auctions, scrapyard, spawner catalog, Tow dispatch, and other project settings.

The user settings folder also contains:

`settings\RLS\phoneLayout.json`

That RLS phone layout includes:

- version: 8
- installed app ids: `settings`, `app-store`, `skills`, `market-watch`
- page app: `redfox-browser`

Current cloud game state also reports the last level as:

`redfox_jump_grid`

Important conclusion:
These are saved data/settings files, not active mod ZIPs. They are still useful context, but they can make logs noisy if the wrong mode or old layout is opened during a clean-lane test.

## Morning Test Adjustment

For the first clean-lane test:

1. Use Freeroam.
2. Use Small Grid.
3. Do not enter Career yet.
4. Do not open the RLS phone yet.
5. Do not press old Tow/spawner/winch/player movement/PSI hotkeys.
6. Test only Hub Scan and RaceBuilder open/basic visibility.
7. Exit BeamNG.
8. Let Codex read the fresh `beamng.log`.

If the clean-lane log still shows unexplained errors, ask David for approval before changing user-side files. The first likely candidates are:

1. Temporarily disabling or moving `mods\repo\ModConflictResolver.zip`.
2. Backing up and filtering stale RedFox input bindings.
3. Backing up and filtering stale Career UI layout entries.

Do not call the clean lane stable until David tests it in BeamNG.
