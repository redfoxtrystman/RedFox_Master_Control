# Approval-Ready Test Lane Switch Plan

Generated local time: 2026-08-10

Purpose:
Define the exact future mod-lane switches for the BeamNG v0.39 RedFox/RLS/Tow recovery without copying, moving, deleting, enabling, or editing any mods yet.

This is a documentation-only plan.

No BeamNG files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.
No active mod lane switch was performed.

Verification labels:

- `static_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## Current Active Lane

Active BeamNG mods folder:

`D:\Games\Steam\steamapps\common\BeamNG.drive\mods`

Current active RedFox clean lane:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

Non-mod files currently present in the active folder:

- `beam_manager.bmc`
- `desktop.ini`
- `download.png`
- `folderico-red.ico`
- `IMG_4250.webp`

Do not add anything else until David tests the clean lane and Codex reads the fresh log.

## Approval Rule

Do not run any lane switch until David explicitly approves that step.

Copying a ZIP into the active BeamNG mods folder counts as enabling a mod.

Moving a ZIP out of the active BeamNG mods folder counts as disabling a mod.

Both require David approval.

## Required Backup Before Any Lane Switch

Before any future lane switch, create a dated lane backup under:

`D:\RedFoxMods\backups`

Recommended name format:

`beamng_v039_lane_switch_pre_<test_name>_<yyyyMMdd_HHmmss>`

The backup should include:

- every active ZIP currently in `D:\Games\Steam\steamapps\common\BeamNG.drive\mods`
- a manifest listing active folder contents before the switch
- a short note saying which test lane is being prepared

Do not delete old backups.

## Test 1: Clean RedFox Lane

Status:
Already installed as the current active lane.

Expected active ZIPs:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

David runtime test:

1. Launch BeamNG.
2. Load Freeroam Small Grid.
3. Check GarageHub visibility.
4. Click Hub Scan once if available.
5. Check basic RaceBuilder visibility.
6. Exit BeamNG.
7. Tell Codex what happened.

Codex next action after test:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode clean
```

Pass condition:

David reports BeamNG loads, Small Grid loads, Hub does not crash, and RaceBuilder does not crash.

If clean lane fails:

- do not add RLS
- do not add Tow
- read the fresh log
- repair clean lane first

## Test 2: Strict Isolated RLS Base

Only run after Test 1 passes.

Important:
For strict isolation, this lane should contain only the three RLS base ZIPs. The current RedFox clean lane should be backed up/held aside before installing RLS base.

Source ZIPs:

- `D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\CAREER NEW\rls_career_collection_release.zip`
- `D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\CAREER NEW\rls_career_overhaul_2.7.0.zip`
- `D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\CAREER NEW\rls_repo_mod_manager.zip`

Destination folder when approved:

`D:\Games\Steam\steamapps\common\BeamNG.drive\mods`

Expected active ZIPs for this test:

- `rls_career_collection_release.zip`
- `rls_career_overhaul_2.7.0.zip`
- `rls_repo_mod_manager.zip`

Do not include:

- RedFox GarageHub
- RaceBuilder
- RLS maps
- RLS RaceTab
- RLS RealCargo
- RLS non-repo mod collection
- RLS tanker hotfix
- RedFox Tow
- JOB04/FoxNet
- JOB13 Auctions
- tow vehicle packs

Codex next action after test:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode rls
```

Pass condition:

David reports RLS/Career loads, phone/routes are not blank, and no fatal error/crash occurs.

If RLS base fails:

- read the fresh log first
- identify whether failure is route/UI, override/load-order, career save, map memory, or user-state pollution
- compare against `rls_career_overhaul_2.7.0_beta.zip` only if the log points at one of the files changed between beta and held
- do not roll back to `2.6.6` blindly because `2.6.6` uses the older global UI override pattern

## Test 3: RLS Map One At A Time

Only run after strict isolated RLS base passes.

Do not add multiple RLS maps at once.

High-memory map candidates already inspected:

The Gap:

`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\career maps\rls_career_overhaul_the_gap_1.1.zip`

Skeleton Coast:

`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\career maps\rls_career_overhaul_skeleton_coast_beta_0.1.2.zip`

Recommended order:

1. RLS base only
2. one smaller/known map if David chooses one
3. The Gap by itself with RLS base
4. Skeleton Coast by itself with RLS base

For The Gap and Skeleton Coast:

- use a normal stock vehicle first
- do not test helicopter first
- do not buy Tow shop/wrecker first
- watch for out-of-memory, D3D, VRAM, texture, autosave-loop, fatal, and crash signs

Codex next action after each map test:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode rls
```

## Test 4: Tow Gameplay Baseline

Only run after clean lane and RLS base behavior are understood.

Use gameplay-safe Tow baseline before web/phone polish if Tow gameplay state is unknown.

Source ZIP:

`D:\Games\Steam\steamapps\common\12345679\rf current mods temp--------\19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_0_NativeRepoGenerationPurchaseFinalizationRuntimeSlim WORK GOOD BEFORE WEB SPLIT.zip`

Expected question before install:

Should Tow gameplay be tested alone, with RLS base, or with the current clean RedFox lane?

Do not assume the answer. This choice affects conflict evidence.

## Test 5: Tow Web/Phone Baseline

Only run after Tow gameplay/state is understood.

Use the single-relay web baseline, not the later merged build.

Source ZIP:

`D:\Games\Steam\steamapps\common\WEB PAGE TESTING DID NOT WANT TO RENAME ALL THE SZIPS\19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip`

Do not use as first repair baseline:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_7_PC_PHONE_TYPED_BRIDGE_MERGED.zip`

Reason:
The v0.4.9.7 merged build makes both the portal page and the host try to own Lua state/action access. The v0.4.9.6 single-relay build keeps the iframe asking the Angular host, and the Angular host talks to BeamNG Lua.

Codex next action after Tow web test:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode tow
```

## Never Do During Normal Testing

- Do not install multiple versions of the same RedFox mod at once.
- Do not mix RLS maps into the base RLS test.
- Do not add Tow while proving RLS base.
- Do not add RLS while proving clean RedFox lane.
- Do not clean user state without David approval.
- Do not edit Hub files unless David explicitly asks.
- Do not start from scratch.
- Do not call anything stable until David tests in BeamNG and reports it working.

## Next Real Step

The next real evidence step is still David's Clean RedFox Lane runtime test.

Until that fresh log exists, runtime status remains:

`awaiting_user_test`
