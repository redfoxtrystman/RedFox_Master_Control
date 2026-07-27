# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-26 19:39 PDT  
**Owner:** David / Captain  
**Primary chat:** BeamNG Mod QuickScan / Catalog Manager  
**Repository:** redfoxtrystman/RedFox_Master_Control  
**Master record:** `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`  
**Incident record:** `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`

## Read before doing work

Every chat or Codex session must read:

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md`
3. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
4. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
5. This status file.

## Current truth

- v0.2.0 opened and scanned on David's Windows computer.
- Its report contained known false positives.
- v0.3.0 passed Python compilation and a synthetic self-test.
- v0.3.0 large-folder Windows performance is not proven.
- Auto-Pilot, pause/resume, image extraction, ZIP renaming, sorting, XLSX, dependency graph, and repair workflow are roadmap items, not completed features.

## Safe baseline

Current local/source baseline:

```text
BeamNG Mod QuickScan.pyw v0.3.0
```

Label:

```text
STATIC/SELF-TEST VERIFIED
WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN
```

## Next permitted work

Start with Stage 0 and Stage 1 only:

- baseline inventory and hashes;
- false-positive regression tests;
- SQLite schema and migration;
- safe per-ZIP commits;
- unattended queue;
- pause/resume checkpoint design;
- adjustable checkpoint batch size;
- honest live progress;
- Windows test checklist.

Do not start catalog renaming or repair automation until the scanner database and conflict reports are trustworthy.

## Required update after every work session

Update this file with:

- branch or commit;
- files changed;
- tests run;
- static verification;
- David runtime testing;
- known failures;
- current safe baseline;
- next step.

## Handoff format

```text
Project:
Version:
Baseline inspected:
Files changed:
Before-edit checks:
After-edit checks:
Packaged ZIP reopened:
Static tests:
Windows runtime tests by David:
Proven:
Not proven:
Known problems:
GitHub commit:
Next safe step:
```