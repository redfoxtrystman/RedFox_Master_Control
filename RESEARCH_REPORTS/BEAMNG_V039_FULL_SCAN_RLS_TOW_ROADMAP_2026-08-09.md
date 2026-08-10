# BeamNG v0.39 RLS / RedFox Tow Recovery Roadmap

Timestamp: 2026-08-09 23:48 -07:00
Chat ID: RF-DOC01
Chat Name: Codex Desktop
Message type: read-only scan report / recovery roadmap
Assigned role: recovery coordinator

## Status

Screen status = 🟨 NEEDS TEST

No mod files were edited in this pass.
No BeamNG game files were edited in this pass.
No ZIPs were modified in this pass.

Local full report:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\FULL_SCAN_RLS_TOW_RECOVERY_ROADMAP_2026-08-09.md`

Local scan artifact folder:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401`

Verification labels:

- `static_checked`
- `code_compared`
- `zip_integrity_checked`
- `awaiting_user_test`

No runtime verification has happened after the clean-lane setup. Only David testing inside BeamNG counts as runtime verification.

## I Read / Compared

Current full Steam/common root:
`D:\Games\Steam\steamapps\common`

Old backup full Steam/common root:
`I:\1----Beamng--modding folder--\BEAMNG BACKUP\common`

Current BeamNG game root:
`D:\Games\Steam\steamapps\common\BeamNG.drive`

Old backup BeamNG game root:
`I:\1----Beamng--modding folder--\BEAMNG BACKUP\common\BeamNG.drive`

Current BeamNG user folder:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current`

Old backup BeamNG user folder:
`I:\1----Beamng--modding folder--\BEAMNG BACKUP\common\----new mods folder-----\current`

## Scan Counts

Full current common inventory: 111,553 files.
Full old backup common inventory: 103,924 files.
Full common compare: 39,514 changed path records.

Current BeamNG game inventory: 14,817 files.
Old backup BeamNG game inventory: 20,402 files.
BeamNG game compare: 18,775 changed path records.

Current user folder inventory: 2,541 files.
Old backup user folder inventory: 3,735 files.
User folder compare: 1,651 changed records.

Focused same-path high-risk text/API hash check: 4,368 candidates, 0 changed hashes.

Meaning: this does not look like a simple same-file patch problem. v0.39 changed structure and loader behavior, especially around career/gameplay/UI paths.

## Current Active Mod State

Old active mod stack was moved, not deleted, to:
`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822`

Current active test lane in BeamNG mods folder:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

The quarantined old mod DB showed 61 active RLS/RedFox/Tow-related entries. Do not restore that entire stack at once.

## Main Findings

BeamNG is now `0.39.4.0`, build `20972`. The old backup shows `0.38.6.0`, build `19963`.

v0.39 has official Vue UI mod support under:
`ui/ui-vue/mods/%mod_name%/`

Relevant local files include:

- `lua/ge/extensions/ui/uiMods.lua`
- `lua/ge/extensions/ui/router/routeManager.lua`
- `lua/ge/extensions/ui/pause/actions.lua`
- `ui/entrypoints/main/angularModules.js`
- `ui/ui-vue/mods/README.md`

RLS 2.7.0 is v0.39-aware, but it is a deep career overhaul. It has:

- about 4,802 entries
- 57 legacy `ui/modModules` entries
- 4 Vue mod entries
- a phone layout override
- 61 current-game path collisions

RedFox Tow/FoxNet web breakage likely came from mixing JOB09/JOB04/JOB13/RLS phone/browser layers and from risky builds that ship global BeamNG UI bundle overrides:

- `ui/ui-vue/dist/index.js`
- `ui/ui-vue/dist/index.css`

Do not use global dist overrides for the recovery path.

Also watch for missing legacy loader entry:
`ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`

Some builds contain pages under `ui/modModules/redfoxCareerWeb/sites/...`, but if the top-level module JS is missing, the legacy loader can still fail.

## Recommended Roadmap

1. Pause tonight. Do not edit mods.
2. Tomorrow, David tests the current clean lane once and exits BeamNG.
3. Codex reads the newest `beamng.log` and records actual runtime evidence.
4. If the clean lane is good, test RLS alone.
5. RLS isolated test set should be only:
   - `rls_career_collection_release.zip`
   - `rls_career_overhaul_2.7.0.zip`
   - `rls_repo_mod_manager.zip`
6. Do not add RLS maps until base RLS works.
7. Add one RLS map at a time and check logs after each.
8. Only after RLS works, add RedFox Tow gameplay from:
   - `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_0_NativeRepoGenerationPurchaseFinalizationRuntimeSlim WORK GOOD BEFORE WEB SPLIT.zip`
9. Use these as references only, not blind merge targets:
   - `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip`
   - `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_PC_PHONE_TYPED_BRIDGE.zip`
   - `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-05_v0_3_2_4_9_SINGLE_TOW_RELAY_FROM_v0_3_2_4_8.zip`
10. Avoid these as active baselines:
   - `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_7_PC_PHONE_TYPED_BRIDGE_MERGED.zip`
   - JOB04 builds that ship `ui/ui-vue/dist/index.js` or `ui/ui-vue/dist/index.css`
11. Build RedFox web bridge as one shared Lua/data relay with separate PC/phone views only where BeamNG/RLS requires separate entry points.
12. Use a RedFox-owned v0.39 adapter under `ui/ui-vue/mods/redfoxCareerWeb/`; do not replace stock global UI bundles.

## What The Next Chat Needs To Know

Do not start from scratch.
Do not blindly merge JOB04/JOB09/JOB13.
Do not edit Hub unless David explicitly asks.
Do not claim runtime verification until David tests in BeamNG.
The next action is runtime testing, then log inspection, then isolated RLS, then RedFox Tow.

Coordinator action needed = yes

David needs to test/check:
Start BeamNG with the current clean lane, load a simple map, exit, and let Codex read the fresh log.
