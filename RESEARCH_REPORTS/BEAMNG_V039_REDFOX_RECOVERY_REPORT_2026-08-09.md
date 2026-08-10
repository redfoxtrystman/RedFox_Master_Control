# BeamNG v0.39 RedFox Recovery Scan

Date/time: 2026-08-09 22:47 PDT  
Scanner: Codex local RedFox workspace  
Scope: read-only scan of BeamNG install, active mod folder, current user folder logs/cache, and official BeamNG update notes.  
Runtime status: awaiting_user_test

## Verification Labels

- static_checked: BeamNG install files, current user logs, mod cache/database, active mod ZIP metadata, and official update notes were inspected.
- code_compared: not yet; no mod code was edited in this scan.
- zip_integrity_checked: not yet; no new ZIP was built in this scan.
- awaiting_user_test: no BeamNG runtime repair has been tested by David yet.

## Installed Game Baseline

- Steam app manifest: `D:\Games\Steam\steamapps\appmanifest_284160.acf`
- Steam build id: `24617469`
- Launcher log version: `0.39.4.0 - x86 - build 20972 - 2026-08-09 10:26:15 -0700`
- Active user path from launcher log: `D:\Games\Steam\steamapps\common\----new mods folder-----\current\`
- BeamNG install root: `D:\Games\Steam\steamapps\common\BeamNG.drive`

## Official v0.39 Changes That Matter To RedFox

Official BeamNG v0.39 notes add a new Vue UI mod system:

- New Vue UI mods live under `/ui/ui-vue/mods/%mod_name%/`.
- New route/button registration uses `ui_router_routeManager.registerModRoutes`, `ui_pause_actions.registerModTab`, and `ui_pause_actions.registerModButton`.
- BeamNG now ships `D:\Games\Steam\steamapps\common\BeamNG.drive\ui\ui-vue\mods\README.md`.
- v0.39 moved more UI behavior into the Vue route/pause/menu system.
- v0.39 also changed career mission placement expectations and added new career/repository mod support.

Official source: https://www.beamng.com/game/news/patch/beamng-drive-v0-39/

Local README evidence:

- `D:\Games\Steam\steamapps\common\BeamNG.drive\ui\ui-vue\mods\README.md`

## Scan Artifacts Written Locally

All scan outputs are in:

`D:\RedFoxMods\reports\beamng_v039_update_scan_20260809`

Files:

- `active_mod_risk_summary.csv`
- `exact_core_override_providers.csv`
- `mounted_mods_from_log.csv`
- `mounted_zip_ui_conflict_scan.csv`
- `mounted_zip_pattern_hits.csv`
- `mounted_zip_scan_errors.csv`
- `redfox_db_entries.csv`
- `BEAMNG_V039_REDFOX_RECOVERY_REPORT.md`

## Current Active Folder State

Current `D:\Games\Steam\steamapps\common\BeamNG.drive\mods` no longer contains:

`rf current mods temp--------`

Only these top-level folders currently exist there:

- `career maps`
- `CAREER NEW`
- `TOW`

This matters because the latest `beamng.log` still references many RedFox ZIPs from `rf current mods temp--------`, but the folder is not present now. The log and current filesystem are not the same state.

## BeamNG User Mod Database Problem

The user-folder mod database still marks 16 RedFox entries active even though their live ZIP paths are currently missing.

Database:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\db.json`

Export:

`D:\RedFoxMods\reports\beamng_v039_update_scan_20260809\redfox_db_entries.csv`

Examples marked active:

- `/mods/rf current mods temp--------/1-RedFox_GarageHub_v0_7_0_RebuildPass1.zip`
- `/mods/rf current mods temp--------/19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_0_NativeRepoGenerationPurchaseFinalizationRuntimeSlim WORK GOOD BEFORE WEB SPLIT.zip`
- `/mods/rf current mods temp--------/19-JOB-09-RedFox_TowRecoveryDispatch_v0_5_0_7_JOB09_ONLY_UGLY_NATIVE_READ_TEST.zip`
- `/mods/rf current mods temp--------/43_RedFoxUnicycleWeapons_v2_4_7_gravity_off_default_career_guard_test.zip`
- `/mods/rf current mods temp--------/RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_5_SAVE_ISOLATION_SINGLE_OWNER.zip`
- `/mods/rf current mods temp--------/zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-07_v0_3_2_5_3_JOB04_TOW_LEGACY_CLEANUP_FROM_v0_3_2_5_1.zip`

Likely effect:

- BeamNG and/or mod conflict tooling may still carry stale mod metadata, stale conflict resolutions, and stale action bindings after the update.
- Before code edits, make a backup of `current\mods\db.json`, `current\mods\mod_manifests`, and RedFox settings, then test a clean/controlled mod cache state.

## Critical Runtime Errors From Latest Log

Log:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

### 1. RedFox web module 404

Evidence:

```text
request_fail | reason=NOT_FOUND url=ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js
module failed to load: 'redfoxCareerWeb'
```

Meaning:

- The UI boot system tries to import `ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`.
- The file is not mounted/found.
- Old RedFox web pages under `ui/modModules/redfoxCareerWeb/sites/...` are not enough by themselves.

Repair lane:

- Do not patch `ui/ui-vue/dist/index.js`.
- Build a small v0.39 adapter under `/ui/ui-vue/mods/redfoxCareerWeb/`.
- Register stable Vue routes/buttons that open or bridge existing RedFox web content.
- Keep phone and PC access using one shared data module/relay, with separate view adapters only where BeamNG requires it.

### 2. Project 43 movement fatal

Evidence:

```text
extension unavailable: "core_redfoxPlayerMovementLab" at location: "core/redfoxPlayerMovementLab"
*** FATAL LUA ERROR: attempt to index field 'core_redfoxPlayerMovementLab' (a nil value)
while executing: if not extensions.core_redfoxPlayerMovementLab then extensions.load('core/redfoxPlayerMovementLab') end extensions.core_redfoxPlayerMovementLab.toggleProne()
```

Meaning:

- A binding/console command calls `extensions.core_redfoxPlayerMovementLab.toggleProne()`.
- The extension is not currently available.
- This can crash Lua when the key/command fires.

Repair lane:

- Locate the last working Project 43 movement ZIP/source.
- Either restore the extension at the expected path or change the command to guard the function call.
- If the extension is not meant to load right now, remove/disable the stale keybind from a backed-up copy of `settings\inputmaps\keyboard.diff`.

### 3. Missing RedFox actions

Evidence:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\inputmaps\keyboard.diff`

Current bindings include actions that BeamNG cannot find:

- `redfoxInventoryToggleUI`
- `toggleRedFoxModulesHub`
- `redfox_tow_recovery_toggle`
- `toggleRedFoxRaceManager`
- `openPhone`
- `redfox_spawner_toggle`
- `rf_skyride_open_ui`
- `redfox_winch_extend`
- `redfoxPlayerMovementToggleUI`
- `redfoxGravityToggleUI`
- `randomevents_toggle_menu`
- `redfox_career_dev_toggle_launcher`
- `redfox_winch_pull`

Meaning:

- The action JSON/Lua providers for these actions are not loaded in the current state.
- This may be because RedFox ZIPs are missing, renamed, not mounted, or incompatible with v0.39 action loading.

Repair lane:

- Do not edit the live keyboard file without backup.
- For each RedFox mod, verify it includes correct `lua/ge/extensions/core/input/actions/...` definitions or new v0.39-compatible action registration.
- Reinstall only one version of each RedFox mod at a time.

### 4. Garage Hub manifest rejects

Evidence:

```text
Manifest rejected: lua/ge/extensions/redfox/modules/redfox_race_manager/redfox_module.json :: jsonReadFile failed
Manifest rejected: lua/ge/extensions/redfox/modules/redfox_surface_studio/redfox_module.json :: jsonReadFile failed
Manifest rejected: lua/ge/extensions/redfox/modules/redfox_winch_core/redfox_module.json :: jsonReadFile failed
...
```

Meaning:

- Garage Hub is scanning for RedFox module manifests and failing to read them.
- Possible causes: stale DB/cache entries, old mount paths, malformed JSON, or files no longer present after active folder changes.

Repair lane:

- Do not edit Hub until David explicitly asks.
- First verify whether the referenced module manifests exist in the actual mod ZIPs being tested.
- If they exist and are valid, add/repair a bridge/adaptor in the target module, not the Hub.

### 5. RLS career/UI high-risk overrides

Exact active override provider scan found:

```text
lua/ge/extensions/ui/phone/layout.lua | rls_career_overhaul_2.7.0.zip
```

Mounted ZIP pattern scan found:

- `rls_career_overhaul_2.7.0.zip` has 57 legacy `ui/modModules` entries, 4 `ui/ui-vue/mods` entries, and a phone layout override.
- `rls_repo_mod_manager.zip`, `backAlley.0.2.2-alpha.zip`, and `holas_rls_addons.zip` also use legacy `ui/modModules`.

Meaning:

- RLS career mods are deeply involved in old Angular-style `ui/modModules` and phone layout behavior.
- v0.39 introduces a supported Vue mod path. Old modules may still partly load, but routes/buttons/overlays can break.
- RedFox web fixes must not depend on cloning or replacing RLS core UI files.

Repair lane:

- Test RedFox web pages with a minimal career stack first.
- Keep RLS core override changes isolated from RedFox feature jobs.
- Avoid packaging any `ui/ui-vue/dist/index.js` global bundle.

## Immediate Safe Recovery Order

1. Back up current user state:
   - `D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\db.json`
   - `D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\mod_manifests`
   - `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\inputmaps\keyboard.diff`
   - `D:\Games\Steam\steamapps\common\----new mods folder-----\current\settings\redfox`

2. Create a clean test lane:
   - Use one controlled test folder/set.
   - Install only one version of each RedFox mod.
   - Start with GarageHub + one target mod only.

3. First runtime sanity test:
   - No RedFox web/Tow/FoxNet yet.
   - Confirm BeamNG boots with no stale missing RedFox actions.
   - Confirm Hub scan does not fatal.

4. Repair action definitions:
   - RaceBuilder action.
   - TowRecovery action.
   - Movement/Project 43 action or remove stale binding.
   - Winch/Spawner/Gravity/PSI action providers as each mod is brought back.

5. Repair RedFox web for v0.39:
   - Build a `/ui/ui-vue/mods/redfoxCareerWeb/` adapter.
   - Keep existing working pages/assets where possible.
   - Use one shared Lua data provider for PC and phone views.
   - Do not use `ui/ui-vue/dist/index.js`.

6. Repair project mods in priority order:
   - GarageHub baseline and module manifest scanning.
   - RaceBuilder.
   - SurfaceStudio / Material Proving Grounds.
   - TowRecovery + FoxNet only after UI adapter approach is proven.
   - Project 43 movement/weapons crash guard.
   - Winch/Spawner/PSI/other keybind-driven mods.

## Last Known Good / First Bad / Current Safe Point

Last known good:

- Not fully proven in this scan.
- For TowRecovery, the file name `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_0_NativeRepoGenerationPurchaseFinalizationRuntimeSlim WORK GOOD BEFORE WEB SPLIT.zip` is marked by David/file naming as good before web split, but it must be re-tested under BeamNG v0.39.
- Earlier rollback notes also reference `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip` and `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-05_v0_3_2_4_9_SINGLE_TOW_RELAY_FROM_v0_3_2_4_8.zip` as safer than the failed merge, but they are not currently present in the active `BeamNG.drive\mods` folder.

First bad:

- v0.39 update exposed/magnified breakage; exact first bad RedFox build differs by mod.
- The failed Codex merged Tow/FoxNet build was already rolled back and should not be reused.

Current safest point:

- Read-only state plus this report.
- No mod code edited in this scan.
- Next safe action is a backed-up cache/test-lane cleanup and one-mod-at-a-time reinstall, not another broad merge.

Unknowns requiring David testing:

- Whether a clean user mod cache with only one RedFox mod installed boots cleanly.
- Which RedFox ZIPs are the latest user-confirmed working versions under v0.39.
- Whether old `ui/modModules` pages can still be loaded directly after a Vue adapter is added.

## Do Not Do

- Do not start from scratch.
- Do not rewrite working RedFox systems just because v0.39 changed UI internals.
- Do not edit Hub files unless David explicitly approves a Hub change.
- Do not package global `ui/ui-vue/dist/index.js` overrides for feature jobs.
- Do not install multiple versions of the same RedFox mod at the same time except for an explicit conflict test.
- Do not call anything stable/working until David tests it in BeamNG.

## Next Needed Human Decision

Approve or reject this first repair operation:

Make a backup of the current user mod database/cache/input bindings, then create a clean controlled BeamNG test state where only one RedFox mod lane is reintroduced at a time.

Recommended first target:

GarageHub + RaceBuilder, because they are core RedFox workflow mods and the log already shows missing `toggleRedFoxRaceManager`.
