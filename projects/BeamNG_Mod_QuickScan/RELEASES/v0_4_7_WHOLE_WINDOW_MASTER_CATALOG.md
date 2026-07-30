# BeamNG Mod QuickScan v0.4.7 — Whole-Window Scroll, Saved Scan Snapshots, and Master Catalog

**Date:** 2026-07-29 PDT  
**Owner:** David / Captain  
**Baseline:** exact verified v0.4.6 source  
**Status:** `PACKAGED SELF-TEST + GUI SMOKE + REAL CROSS-FOLDER DUPLICATE PASS — WINDOWS LARGE-LIBRARY TEST REQUIRED`

## Owner-reported failures corrected

- Every layout was trapped inside small internal areas and could expose only one line or a narrow panel at a time.
- Buttons and text were cut off instead of resizing or wrapping.
- Tow Catalog squeezed the exact-configuration editor into a narrow right-side panel.
- Folder-by-folder runs did not provide a clear exact snapshot for each run.
- There was no dedicated full catalog showing conflicts that connect mods from different scanned folders.

## Whole-window layout law

- The complete application surface is inside one outer vertical scroll region.
- The header, folder controls, scan controls, cards, result tools, tab row, and complete active tab move together.
- Tables keep their own horizontal/vertical scrollbars for large datasets.
- Toolbars use responsive wrapping rows instead of cutting controls off.
- UI Size choices: 100%, 125%, 150%, 175%, and 200%.
- Ctrl+Plus and Ctrl+Minus change UI size.
- F11/Maximize Window toggles main-window size.
- Top returns to the beginning of the whole page.

## Tow Catalog layout

- Exact-configuration list is full width.
- Review editor is full width below the list.
- All fields and all 17 JOB-09 permissions are reached through the whole-window scrollbar.
- Tow Catalog auto-reuses a saved BeamNG user folder when available and auto-loads/rebuilds exact entries when scan data exists.

## Saved scan snapshots

Every scan run stores:

- exact scanned folder;
- exact ZIP list for that run;
- detected name, version, author, SHA-256, and original path;
- findings that affected that folder at that time;
- completion state and counts.

Previous Scans now shows the run list plus exact mod and finding tables for the selected run.

## Master Catalog

The new Master Catalog tab:

- combines every active ZIP retained in the shared QuickScan database;
- filters by scanned folder, conflicts, duplicates, or no findings;
- shows conflict and duplicate counts per mod;
- shows cross-folder conflicts with both folders, both mods, severity, category, and explanation;
- exports `master_mod_catalog.json`, `master_mod_catalog.csv`, and `cross_folder_conflicts.json`.

## Exact hashes

```text
v0.4.6 source
b9577c76d86a33b9b4b05425f5337dd3cdab7859c004dff2d13455ade9261ae4

v0.4.7 source
11f685c8f4d7d59dfd5fe54bb65512280fd8b01336c9905b7053fbeb1ea2501c

v0.4.7 package
538d869a4ce05daaa102edb43f2f1f8da3fcbfc76ca4e0e28245b3b1be3b1076
```

## Verification

```text
PASS inherited v0.4.4/v0.4.5/v0.4.6 self-tests
PASS v0.4.7 compile and self-test
PASS two-folder scan registry
PASS per-run exact mod snapshots
PASS per-run finding snapshots
PASS cross-folder path-conflict detection
PASS master JSON/CSV export
PASS real Roamer exact duplicate across two separate scan folders
PASS whole-window scroll region exceeds viewport
PASS responsive Tow toolbar wraps
PASS full-width Tow review editor
PASS 100–200% UI controls
PASS Previous Scans exact-content GUI
PASS Master Catalog GUI and cross-folder finding table
PASS final ZIP reopen, extracted compile, self-test, and GUI smoke
```

## Required Windows test

- Physical D-drive scan folders and persisted settings.
- Mouse-wheel behavior and visible whole-window scrollbar.
- 100–200% scaling on David's monitor/DPI.
- Large library performance and cross-folder finding totals.
- Tow Catalog full review with real configurations.

No source mod ZIP was modified by the layout, scan-history, or Master Catalog tests.
