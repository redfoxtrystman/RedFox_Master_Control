# David Start Here Runtime Test

Generated local time: 2026-08-10

Purpose:
Give David the shortest safe morning test path for the BeamNG v0.39 recovery.

## Do This First

Do not add RLS yet.

Do not add Tow yet.

Do not re-enable the old mod stack yet.

Current active test lane should only be:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

## Test 1

1. Start BeamNG.
2. Load Freeroam.
3. Pick Small Grid.
4. Wait until the vehicle is fully loaded.
5. If GarageHub appears, open it.
6. If Hub Scan is available, click it once.
7. If RaceBuilder appears, open it only far enough to see whether it loads.
8. Do not enter Career.
9. Do not open the RLS phone.
10. Do not press old RedFox Tow, spawner, winch, player movement, gravity, or PSI hotkeys.
11. Exit BeamNG.
12. Tell Codex what happened.

## Tell Codex These Five Things

- Did BeamNG open?
- Did Small Grid load?
- Did GarageHub appear?
- Did Hub Scan work, error, freeze, or crash?
- Did RaceBuilder appear?

Also say if BeamNG gave a fatal error, froze, or crashed.

## What Codex Does Next

After David exits BeamNG, Codex reads the fresh log:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

Then Codex runs the clean-lane log helper:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode clean
```

## If Test 1 Passes

Only then move to isolated RLS base:

- `rls_career_collection_release.zip`
- `rls_career_overhaul_2.7.0.zip`
- `rls_repo_mod_manager.zip`

Do not add RLS maps yet.

Do not add RedFox Tow yet.

## If Test 1 Fails

Do not add more mods.

Do not clean user state automatically.

Codex reads the fresh log first and fixes the clean lane before RLS or Tow.

## Truth Rule

Runtime status remains:

`awaiting_user_test`

Nothing is stable until David tests it in BeamNG and says it works.
