# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.7.3 Strict Manifest-Only Rename  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_7_3_STRICT_MANIFEST_ONLY_RENAME.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_7_3/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_OPERATIONS_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.7.3 release records
5. v0.4.7.3 verification
6. `projects/BeamNG_Mod_QuickScan/REQUIREMENTS/v0_4_8_CATALOG_GALLERY_WIZARD_REDESIGN_2026-07-30.md`
7. This file

## Current truth

- v0.4.7.2 is the exact verified baseline used for v0.4.7.3.
- David rejected the optional full-ZIP-copy choice for filename-only renames.
- v0.4.7.3 removes that option completely.
- A filename-only rename hashes the source, renames the same file, verifies the target hash, and writes only a database Undo row plus JSONL manifest.
- No ZIP, preview image, report, or catalog copy is created for a rename.
- Undo renames the same current file back after hash verification.
- If that file is manually deleted or moved later, the manifest cannot recreate it because no second copy exists.
- Storage measures tiny rename manifests and legacy rename backups separately.
- Legacy backups created by older versions can be cleaned after confirming renamed ZIPs remain present.
- Existing folder focus, metadata recovery, automatic images, solid status colors, duplicate organizer, Career, Tow Catalog, Previous Scans, Master Catalog, DRM, pause/resume, quarantine, reports, and Undo remain present.
- Physical Windows D-drive and large-library behavior remain David's required tests.

## Exact hashes

```text
v0.4.7.3 source
4e7c7d6a66327de5b76a23d257bf1677bd12315f540b9339fde7a979c859e98a

v0.4.7.3 package
470811b9819e9a9edceffa6d1a0c2520c0e1c6058d86141bad651dcd7b064a57
```

## Filename-only rename storage law

```text
RENAME THE EXISTING ZIP IN PLACE.
CREATE NO SECOND ZIP COPY.
CREATE NO IMAGE OR REPORT COPY.
WRITE ONLY PATHS, SHA-256, TIMESTAMP, WARNING, AND UNDO HISTORY.
THERE IS NO FULL-BACKUP OPTION.
```

Undo succeeds only while the same renamed ZIP remains present and unchanged.

## Separate ZIP-content changes

A Career repair or another operation that changes files inside a ZIP must create a separate patched ZIP or preserve the original through that operation's explicit workflow. It is not part of filename-only rename Undo.

## Folder scope law

```text
NORMAL TABS SHOW THE SELECTED FOLDER BY DEFAULT.
ALL-SCANNED-FOLDERS VIEW MUST BE EXPLICITLY REQUESTED.
MASTER CATALOG IS THE CROSS-FOLDER VIEW.
PREVIOUS SCANS RETAIN EACH FOLDER/RUN SNAPSHOT.
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
- Duplicate movement and quarantine remain manifest-backed and undoable.

### Tow safety

- Exact model + exact configuration remains the Tow identity.
- New/runtime entries start Unreviewed.
- Manual exact-config reviews survive rescans.
- Catalog-only work does not rewrite source ZIPs.

## Verification

```text
PASS Python compilation
PASS inherited v0.4.4-v0.4.7.2 self-tests
PASS strict v0.4.7.3 self-test
PASS live filename-only rename with no backup directory
PASS JSONL backup_created=false and empty backup path
PASS empty database backup path
PASS hash-verified Undo using the same file
PASS Storage GUI has no backup-mode selector
PASS final ZIP reopen, compile, self-test, GUI and live integration tests
PASS package contains no uploaded user mod ZIPs or images
```

## What David should test

1. Extract v0.4.7.3 into a new folder and confirm the title.
2. Rename a small copied batch.
3. Confirm no `backups/renames` folder is created.
4. Confirm only small manifest/database records appear.
5. Test Undo while the renamed ZIP remains present.
6. Confirm legacy rename backups can be measured and cleaned through Storage.
7. Continue selected-folder, automatic-image, metadata, Master Catalog, Career, and Tow tests.

## Next version boundary

```text
v0.4.8 — Ellexium-assisted visual vehicle/configuration gallery, compact searchable catalog, guided wizards, hover help, wrapped layouts
v0.4.9 — Tow online enrichment and representative JOB-09 proof set
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
v0.4.7.3 release: 3a7f486441bfd622a054347f55ce52e40b433fac
v0.4.7.3 verification: f8abff7d5c8cafc86c2c64019123e7f23517b608
Status: this commit
```
