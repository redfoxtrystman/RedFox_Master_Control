# BeamNG Log Triage Helper

Generated local time: 2026-08-10

Purpose:
Prepare the next runtime-test step for the BeamNG v0.39 RedFox/RLS/Tow recovery.

This helper is documentation/tooling only.

No BeamNG files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.

## Helper

Script:

`D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1`

Default log path:

`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

Default report folder:

`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401`

## Use After David Tests

After David launches BeamNG, runs a test, exits BeamNG, and says what happened, run one of these:

Clean lane:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode clean
```

RLS:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode rls
```

Tow:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode tow
```

Everything:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\RedFoxMods\tools\Read-BeamNGRecoveryLog.ps1" -Mode all
```

## Parser Check

The local script passed a PowerShell parser check after creation.

It was not run against the stale BeamNG log during setup because the next meaningful report should come after David's fresh runtime test.

## Truth Rule

This script does not prove a mod works.

It only helps inspect the log after David's BeamNG runtime test.

Runtime status remains:

`awaiting_user_test`
