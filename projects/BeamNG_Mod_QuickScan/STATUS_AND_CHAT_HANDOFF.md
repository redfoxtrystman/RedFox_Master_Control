# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-29 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.7 Whole-Window Scroll + Saved Scan Snapshots + Master Catalog  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_7_WHOLE_WINDOW_MASTER_CATALOG.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_7/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_OPERATIONS_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.7 release records
5. v0.4.7 verification
6. This file

## Current truth

- v0.4.6 is the exact verified baseline used for v0.4.7.
- v0.4.7 fixes the owner-reported layout failure across the complete app, not only Tow Catalog.
- The header, folder controls, scan controls, status cards, results tools, tabs, and complete active tab now live inside one whole-window scroll region.
- Major toolbars wrap into additional rows rather than clipping controls.
- UI Size is selectable from 100% through 200%; Ctrl+Plus/Ctrl+Minus adjust it.
- F11/Maximize Window and Top controls are present.
- Tow Catalog uses a full-width exact-configuration list and a full-width review editor below it.
- Every scan run now stores a separate exact mod snapshot and finding snapshot.
- Previous Scans displays the exact ZIPs and findings from the selected folder-by-folder run.
- Master Catalog combines every active ZIP retained in the shared database.
- Master Catalog shows cross-folder duplicates/conflicts with both folder paths, both mods, category, severity, and explanation.
- Master Catalog exports JSON and CSV.
- Existing scanner, duplicate organizer, version-only rename, image extraction, Career wizard, Tow Catalog, DRM, pause/resume, backup, quarantine, and Undo behavior remain present.
- v0.4.7 passed inherited self-tests, packaged tests, GUI smoke, synthetic two-folder conflict tests, and a real Roamer exact-duplicate test across two separate folders.
- Physical Windows D-drive/DPI/large-library behavior remains David's required test.

## Exact hashes

```text
v0.4.6 source
b9577c76d86a33b9b4b05425f5337dd3cdab7859c004dff2d13455ade9261ae4

v0.4.7 source
11f685c8f4d7d59dfd5fe54bb65512280fd8b01336c9905b7053fbeb1ea2501c

v0.4.7 package
538d869a4ce05daaa102edb43f2f1f8da3fcbfc76ca4e0e28245b3b1be3b1076
```

## Whole-window layout law

```text
THE COMPLETE APP PAGE MUST SCROLL.
BUTTONS MUST WRAP INSTEAD OF DISAPPEARING OFF SCREEN.
TABLES MAY KEEP THEIR OWN SCROLLBARS FOR LARGE DATA.
THE USER MUST BE ABLE TO SCALE TEXT/CONTROLS FROM 100% THROUGH 200%.
```

## Saved scan law

- Every completed, paused, or cancelled run remains separately identifiable.
- A run stores its source folder, exact ZIP members, metadata snapshot, and findings snapshot.
- Loading one previous run must not silently replace another run's record.
- Folder-by-folder runs feed the shared Master Catalog while remaining separately reviewable.

## Master Catalog law

- The master view is the union of active ZIPs retained in the shared database.
- Mods remain linked to the most specific saved scan folder containing them.
- Cross-folder findings require at least two connected mods from different saved scan folders.
- Exact duplicates, versions, functional duplicates, and path conflicts must remain evidence-based.
- Generic filenames or metadata names alone are never conflict proof.

## Preserved laws

### ZIP naming

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD OR UPDATE A REAL VERSION TOKEN.
NEVER REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
DO NOT INVENT A VERSION.
```

### Duplicate safety

- Generic folders/similar names alone are not identity proof.
- Matching images are supporting evidence, not sole proof.
- Variants with changed functional files remain review-only.
- Moves and quarantine actions are manifest-backed and undoable.

### Tow safety

- Exact model + exact configuration remains the Tow identity.
- New/runtime entries start Unreviewed.
- Manual exact-config reviews survive rescans.
- Catalog-only operations do not rewrite source ZIPs.

## Verification

```text
PASS inherited v0.4.4/v0.4.5/v0.4.6 self-tests
PASS v0.4.7 compile and self-test
PASS two-folder scan registry and exact run snapshots
PASS cross-folder path conflict
PASS master JSON/CSV exports
PASS real Roamer exact duplicate across separate folders
PASS outer scrollregion larger than viewport
PASS responsive toolbar wrap
PASS full-width Tow review
PASS 100–200% UI scaling
PASS Previous Scans exact-content GUI
PASS Master Catalog GUI
PASS final package reopen/extracted tests
```

## What David should test

1. Extract v0.4.7 into a new folder and confirm the title.
2. Confirm the whole-window vertical scrollbar reaches the complete page.
3. Test UI Size at 125%, 150%, and 175%.
4. Resize the window narrower and confirm buttons wrap instead of disappearing.
5. Scan two different D-drive folders.
6. Open Previous Scans and confirm each run shows its own exact ZIPs and findings.
7. Open Master Catalog and confirm all scanned folders/mods appear.
8. Confirm known duplicates/conflicts across different folders appear in the lower table.
9. Test Tow Catalog review fields by scrolling the whole app page.
10. Report physical Windows/DPI and large-library behavior before the automatic sorter starts.

## Next version boundary

```text
v0.4.8 — Tow online enrichment and representative JOB-09 proof set, after Windows v0.4.7 layout test
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
Release: 2a6c8858286a4fa8fd594e1d836401083bfe4720
Verification: 49760be9b71c44cec07cb77f674f357067cc70ab
Status: this commit
```
