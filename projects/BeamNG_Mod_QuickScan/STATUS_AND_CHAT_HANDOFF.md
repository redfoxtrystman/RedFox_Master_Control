# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.7.2 Storage Hotfix  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_7_2_STORAGE_HOTFIX.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_7_2/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_OPERATIONS_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.7.2 release records
5. v0.4.7.2 verification
6. `projects/BeamNG_Mod_QuickScan/REQUIREMENTS/v0_4_8_CATALOG_GALLERY_WIZARD_REDESIGN_2026-07-30.md`
7. This file

## Current truth

- v0.4.7.1 is the exact verified baseline used for v0.4.7.2.
- David reported that 160 filename-only renames created about 1.6 GB of backup ZIPs.
- The cause was a complete `shutil.copy2()` of every ZIP before a rename that did not alter the ZIP contents.
- v0.4.7.2 changes filename-only renames to manifest-only storage by default.
- Manifest-only records original/new path, SHA-256, timestamp, warning, Undo database row, and JSONL history.
- Optional `Full ZIP copy` remains available through Storage.
- Full backups remain mandatory for any operation that rewrites files inside a ZIP.
- Storage measures and can clean old rename backups, previews, reports, database backups, and copied catalog files.
- Existing folder focus, metadata recovery, automatic images, solid status colors, duplicate organizer, Career, Tow Catalog, Previous Scans, Master Catalog, DRM, pause/resume, quarantine, reports, and Undo remain present.
- Physical Windows D-drive/large-library cleanup behavior remains David's required test.

## Exact hashes

```text
v0.4.7.1 source
35f415769d9a52c5d59832927a7d513d715ecfe27afc240cf85534a85780e208

v0.4.7.2 source
4dd5224ee6fdc633e01b18095285fb560036bfa643e2ce9c5dd4086c99815c7f

v0.4.7.2 package
a6def9ddd2a4f39a6708cb614825d923298a309862edb1855ebf2ec866e425e2
```

## Filename-only rename storage law

```text
DEFAULT:
MANIFEST ONLY — NO SECOND ZIP COPY.

STORE:
- original path
- new path
- SHA-256
- timestamp
- warning
- Undo database record
- JSONL history

OPTIONAL:
FULL ZIP COPY, ONLY WHEN THE USER SELECTS IT.

ZIP-CONTENT REWRITES:
COMPLETE BACKUP REMAINS REQUIRED.
```

Existing v0.4.7.1 backups are normally under:

```text
RedFoxTools/BeamNG Mod QuickScan/backups/renames/
```

They may be cleaned after confirming the renamed ZIPs still exist. This removes the emergency second-copy fallback; normal Undo continues to rename the current file back while it remains present.

## Folder scope law

```text
NORMAL TABS SHOW THE SELECTED FOLDER BY DEFAULT.
ALL-SCANNED-FOLDERS VIEW MUST BE EXPLICITLY REQUESTED.
MASTER CATALOG IS THE CROSS-FOLDER VIEW.
PREVIOUS SCANS RETAIN EACH FOLDER/RUN SNAPSHOT.
```

## Metadata recovery law

- Safe recovery happens in memory only.
- Repairs are recorded.
- Missing commas and surplus final closing delimiters are repaired only in structurally safe cases.
- If still invalid, only that metadata file is skipped.
- Normal scans do not modify source ZIPs.

## Progress colors

```text
YELLOW ZIP — filename/version checked
RED    DUP — duplicate audit completed
BLUE   IMG — image extraction completed
GREEN  CAR — Career check completed
✓ clear
! attention needed
```

## Preserved safety laws

### ZIP naming

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD OR UPDATE A REAL VERSION TOKEN.
NEVER REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
DO NOT INVENT A VERSION.
```

### Duplicate safety

- Generic folders or similar names alone are not identity proof.
- Matching images are supporting evidence, not sole proof.
- Variants with changed functional files remain review-only.
- Moves and quarantine remain manifest-backed and undoable.

### Tow safety

- Exact model + exact configuration remains the Tow identity.
- New/runtime entries start Unreviewed.
- Manual exact-config reviews survive rescans.
- Catalog-only work does not rewrite source ZIPs.

## Verification

```text
PASS source compile
PASS inherited v0.4.4-v0.4.7 tests
PASS v0.4.7.2 storage self-test
PASS final package CRC/reopen
PASS packaged compile/self-test
PASS Storage GUI smoke
PASS filename-only rename with no full ZIP backup
PASS SHA-256 unchanged
PASS hash-verified Undo
```

## What David should test

1. Extract v0.4.7.2 into a new folder and confirm the title.
2. Open Storage and note the size of Old filename-only ZIP backups.
3. Confirm the renamed ZIPs still exist at their current names.
4. Clean the old rename-backup folder.
5. Rename a small copied batch in Manifest-only mode.
6. Confirm storage increases only by a small manifest/database amount.
7. Test Undo on one renamed file.
8. Continue testing selected-folder scope, automatic images, metadata recovery, and Master Catalog.

## Next version boundary

```text
v0.4.8 — Ellexium-assisted visual vehicle/configuration gallery, compact searchable catalog, guided wizards, hover help, wrapped layouts
v0.4.9 — Tow online enrichment and representative JOB-09 proof set
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
v0.4.7.2 release: 980b79d1580e15f90441369aba69d2aa272f04c2
v0.4.7.2 verification: 4bf2abbf61b4d75d65b02e9279685ad3908fc2d6
Status: this commit
```
