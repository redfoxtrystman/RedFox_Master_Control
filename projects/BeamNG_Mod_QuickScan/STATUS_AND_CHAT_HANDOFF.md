# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.7.1 Folder Focus + Metadata Recovery + Settings + Solid Status Lights  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_7_1_FOLDER_FOCUS_METADATA_SETTINGS.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_7_1/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_OPERATIONS_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.7.1 release records
5. v0.4.7.1 verification
6. `projects/BeamNG_Mod_QuickScan/REQUIREMENTS/v0_4_8_CATALOG_GALLERY_WIZARD_REDESIGN_2026-07-30.md`
7. This file

## Current truth

- v0.4.7 is the exact verified baseline used for v0.4.7.1.
- v0.4.7.1 is a focused hotfix; it does not replace the planned v0.4.8 visual gallery redesign.
- Normal result tabs default to the currently selected scan folder.
- `View: All scanned folders` explicitly enables combined results.
- Master Catalog remains the cross-folder duplicate/conflict workspace.
- Image extraction is automatic by default and controlled through Settings.
- Settings can hide scan tuning, summary cards, Catalog actions, progress/history/DRM/Safe columns, and change row compactness.
- Four separated shaded status cells are replaced by one compact labeled field: yellow ZIP, red DUP, blue IMG, green CAR.
- The tolerant metadata parser now handles comments, trailing commas, missing commas between adjacent object fields, and surplus closing delimiters after a complete top-level value.
- `stpmustang.zip` and `WSCX_ChevBel-Air.zip` both recover successfully with no malformed-metadata findings.
- A truly unrecoverable metadata file is skipped individually; the rest of the ZIP is still scanned.
- Source ZIPs are never rewritten during ordinary scans or metadata recovery.
- Existing duplicate organizer, version-only rename, image extraction, Career wizard, Tow Catalog, Previous Scans, Master Catalog, DRM, pause/resume, quarantine, backups, and Undo remain present.
- Physical Windows D-drive/DPI/large-library behavior remains David's required test.

## Exact hashes

```text
v0.4.7 source
11f685c8f4d7d59dfd5fe54bb65512280fd8b01336c9905b7053fbeb1ea2501c

v0.4.7.1 source
35f415769d9a52c5d59832927a7d513d715ecfe27afc240cf85534a85780e208

v0.4.7.1 package
b6c3b56292d1bf26c2dfaac3340d449a49c18c027dc309d3817f30001dedd95a
```

## Folder scope law

```text
NORMAL TABS SHOW THE SELECTED FOLDER BY DEFAULT.
ALL-SCANNED-FOLDERS VIEW MUST BE EXPLICITLY REQUESTED.
MASTER CATALOG IS THE CROSS-FOLDER VIEW.
PREVIOUS SCANS RETAIN EACH FOLDER/RUN SNAPSHOT.
```

Folder-scoped normal tabs:

- Findings
- Duplicate Review
- Catalog / Rename
- Career Data
- DRM Details
- Previous Scans
- Tow Catalog

## Metadata recovery law

- Safe recovery happens in memory only.
- Every repair is recorded in the metadata-recovery report.
- Missing commas are inserted only between an obviously completed JSON value and a following quoted object key.
- A suffix is trimmed only when a complete top-level JSON value has already parsed and the suffix contains closing delimiters/whitespace only.
- If still invalid, only that metadata file is skipped.
- Normal scans do not modify source ZIPs.

Exact uploaded results:

```text
stpmustang.zip / vehicles/Mustang67/info_tissma.json
PASS inserted missing comma + removed trailing comma

WSCX_ChevBel-Air.zip / vehicles/belairkene/info.json
PASS removed trailing comma + trimmed surplus top-level brace

Complete two-ZIP scan
PASS 2/2 completed
PASS 6 previews extracted
PASS 0 malformed-metadata findings
PASS 0 yellow findings
```

## Progress colors

```text
🟨 ZIP — filename/version checked
🟥 DUP — duplicate audit completed
🟦 IMG — image extraction completed
🟩 CAR — Career check completed
✓ clear
! attention needed
```

## Preserved laws

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
- Moves and quarantine are manifest-backed and undoable.

### Tow safety

- Exact model + exact configuration remains the Tow identity.
- New/runtime entries start Unreviewed.
- Manual exact-config reviews survive rescans.
- Catalog-only work does not rewrite source ZIPs.

## Verification

```text
PASS source compile
PASS inherited v0.4.4/v0.4.5/v0.4.6/v0.4.7 tests
PASS v0.4.7.1 self-test
PASS exact uploaded metadata recovery
PASS exact complete two-ZIP scan
PASS automatic image extraction
PASS selected-folder GUI scope
PASS explicit all-folder GUI scope
PASS Settings GUI construction
PASS compact progress display
PASS final package CRC/reopen
PASS packaged compile/self-tests/GUI smoke
```

## What David should test

1. Extract v0.4.7.1 into a new folder and confirm the title.
2. Scan one small folder and confirm Catalog, Career, Findings, DRM, Tow, and Previous Scans show that folder only.
3. Switch View to All scanned folders and confirm combined records appear.
4. Confirm Master Catalog still shows all retained folders and cross-folder findings.
5. Open Settings and hide/show scan tuning, cards, Catalog actions, and optional columns.
6. Confirm image extraction runs without checking a main-screen box.
7. Confirm the Progress field shows labeled yellow/red/blue/green jobs close together.
8. Rescan the Mustang and Bel-Air ZIPs and confirm no malformed-metadata yellow findings.
9. Report physical Windows/DPI and large-library behavior.

## Next version boundary

```text
v0.4.8 — Ellexium-assisted visual vehicle/configuration gallery, compact searchable catalog, guided wizards, hover help, wrapped layouts
v0.4.9 — Tow online enrichment and representative JOB-09 proof set
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
v0.4.7.1 release: 8526a90209f2f95f541ae045d5f4a9230200db58
v0.4.7.1 verification: 5c97b1ae0bf7681b03e66de39825c646c433d008
Status: this commit
```
