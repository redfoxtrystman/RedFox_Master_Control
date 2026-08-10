# BeamNG v0.39 Morning Handoff Summary

Generated local time: 2026-08-10

Purpose:
Give David and RedFox worker chats one compact recovery start point for the next runtime test.

## Status

This is a documentation/coordination summary only.

No BeamNG game files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.
No files were moved, deleted, or renamed by this summary step.

Verification labels:

- `static_checked`
- `code_compared`
- `zip_integrity_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## Current Runtime Evidence

No fresh BeamNG runtime log exists after the clean-lane setup.

Latest observed log:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

Latest observed log time:
2026-08-09 10:36:48 AM

That log predates the current clean-lane setup and must not be treated as proof that the clean lane passes or fails.

## Current Active Mod Lane

Current active BeamNG mods folder:
`D:\Games\Steam\steamapps\common\BeamNG.drive\mods`

Active RedFox test ZIPs:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

No RLS, Tow, JOB04/FoxNet, JOB09, JOB13, RLS maps, or tow vehicle packs should be added until the clean lane is tested.

Important caveat:
The BeamNG user repo folder still contains:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\repo\ModConflictResolver.zip`

That may still load unless BeamNG tracks it disabled elsewhere.

## Test 1: Clean Lane

David should test:

1. Launch BeamNG.
2. Choose Freeroam.
3. Choose Small Grid.
4. Do not enter Career.
5. Do not open the RLS phone.
6. Do not press old RedFox Tow/spawner/winch/player movement/gravity/PSI hotkeys.
7. Open/check GarageHub if it appears.
8. Click Hub Scan once if available.
9. Open/check RaceBuilder basic visibility.
10. Exit BeamNG.
11. Let Codex inspect the fresh `beamng.log`.

Why Freeroam Small Grid first:

- Career UI layout still references inactive RedFox apps.
- Input maps still reference inactive RedFox actions.
- RLS phone layout still has `redfox-browser`.
- Last remembered level is `redfox_jump_grid`.

Those can create noise unrelated to the active GarageHub/RaceBuilder lane.

## If Clean Lane Is Noisy

Do not clean user state automatically.

Use the approval-only plan:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\APPROVAL_READY_USER_STATE_CLEANUP_PLAN_2026-08-10.md`

If David approves cleanup, do one layer per test/log cycle:

1. Disable/move user-side `ModConflictResolver.zip`.
2. Filter stale inactive RedFox input bindings, preserving active Hub/RaceBuilder bindings.
3. Filter stale inactive Career UI apps.
4. Address RLS phone layout only after Freeroam clean lane passes.

## Test 2: Isolated RLS Base

Only after clean lane passes.

Use only:

- `rls_career_collection_release.zip`
- `rls_career_overhaul_2.7.0.zip`
- `rls_repo_mod_manager.zip`

Held source folder:
`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\CAREER NEW`

Do not add:

- RLS maps
- RLS RaceTab
- RLS RealCargo
- RLS non-repo mod collection
- RLS tanker hotfix
- RedFox Tow
- JOB04/FoxNet
- JOB13 Auctions
- tow vehicle packs

RLS 2.7.0 appears intentionally adapted for BeamNG v0.39 routing, but it has a broad override surface and 61 same-path collisions with current BeamNG files. It must be tested by itself.

## Test 3: RedFox Tow

Only after clean lane and isolated RLS base are understood.

Best Tow web repair baseline:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip`

Do not use the next repair baseline:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_7_PC_PHONE_TYPED_BRIDGE_MERGED.zip`

Reason:
The single-relay build keeps the portal page talking to the parent app, and the parent app talks to BeamNG Lua. The merged build reintroduced direct page-side Lua, typed proxy probing, and ancestor messaging, which is likely why PC/phone behavior split.

All inspected JOB09 Tow ZIPs still lack:

`ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`

Add a small loader/adapter only if a fresh runtime log proves BeamNG still requests that path.

## Key Reports

Full scan and roadmap:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\FULL_SCAN_RLS_TOW_RECOVERY_ROADMAP_2026-08-09.md`

Runtime log triage helper:
`D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1`

Runtime log triage helper README:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\LOG_TRIAGE_HELPER_README_2026-08-10.md`

Clean-lane static assessment:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\CLEAN_LANE_STATIC_ASSESSMENT_2026-08-10.md`

Morning runtime checklist:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\MORNING_RUNTIME_TEST_CHECKLIST_2026-08-10.md`

RLS base preflight:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\RLS_BASE_PREFLIGHT_STATIC_ASSESSMENT_2026-08-10.md`

Tow bridge supplement:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\TOW_WEB_BRIDGE_SUPPLEMENTAL_FINDINGS_2026-08-10.md`

Tow single-relay decision:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\TOW_SINGLE_RELAY_BASELINE_DECISION_2026-08-10.md`

Tow v0.4.9.6 to v0.4.9.7 surgical diff:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\TOW_0496_TO_0497_SURGICAL_DIFF_REPAIR_PLAN_2026-08-10.md`

RLS version and map surgical test plan:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\RLS_VERSION_AND_MAP_SURGICAL_TEST_PLAN_2026-08-10.md`

User-state pollution check:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\USER_STATE_CLEAN_LANE_POLLUTION_CHECK_2026-08-10.md`

Approval-ready cleanup plan:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\APPROVAL_READY_USER_STATE_CLEANUP_PLAN_2026-08-10.md`

## Do Not Do Yet

- Do not edit Hub files.
- Do not start from scratch.
- Do not merge JOB04/JOB09/JOB13 broadly.
- Do not ship global `ui/ui-vue/dist/index.js` or `index.css` overrides.
- Do not add multiple versions of the same RedFox mod for normal testing.
- Do not mark any build stable until David tests it in BeamNG and reports it working.
