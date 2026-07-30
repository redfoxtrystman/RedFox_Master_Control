# BeamNG Mod QuickScan v0.4.7 — Baseline and Verification

## Baseline

- Previous source: v0.4.6 JOB-09 Tow Catalog Foundation
- Previous source SHA-256: `b9577c76d86a33b9b4b05425f5337dd3cdab7859c004dff2d13455ade9261ae4`
- New source SHA-256: `11f685c8f4d7d59dfd5fe54bb65512280fd8b01336c9905b7053fbeb1ea2501c`
- New package SHA-256: `538d869a4ce05daaa102edb43f2f1f8da3fcbfc76ca4e0e28245b3b1be3b1076`

## New protected behavior

1. The complete app surface scrolls vertically as one page.
2. Toolbars wrap into additional rows rather than clipping buttons.
3. UI scaling is selectable from 100% through 200%.
4. Tow Catalog uses a full-width list followed by a full-width review editor.
5. Every scan run stores a separate exact ZIP and finding snapshot.
6. Previous Scans can display the exact contents of the selected run.
7. Master Catalog combines all active ZIPs known to the shared database.
8. Cross-folder findings show conflicts and duplicates that connect different scanned folders.
9. Master Catalog exports JSON and CSV.
10. Existing duplicate, rename, image, Career, Tow, DRM, backup, pause/resume, quarantine, and Undo behavior is preserved.

## Test evidence

```text
PASS source compile
PASS inherited self-tests
PASS v0.4.7 data self-test
PASS two separate scan folders remain separate
PASS each run stores one exact mod in the synthetic two-folder test
PASS each run stores its own findings snapshot
PASS same virtual Lua path with different bytes creates a cross-folder path conflict
PASS master catalog JSON/CSV/conflict exports
PASS real roamerpack_00.zip and roamersadfaw.zip detected as an exact duplicate across separate folders
PASS outer scrollregion larger than viewport
PASS responsive Tow actions wrapped at 1100x700
PASS Tow review panel located below list rather than beside it
PASS 150% UI scale produced enlarged Treeview rows
PASS Previous Scans detail tables
PASS Master Catalog mod/conflict tables
PASS packaged ZIP CRC, extracted compile, full self-test, GUI smoke, and real-pair test
```

## Windows boundary

The build still needs David's physical Windows test for:

- D-drive path persistence;
- monitor DPI and 100–200% scaling;
- mouse-wheel and scrollbar feel;
- thousands-of-mods performance;
- real cross-folder conflict totals.

No source mod ZIP was modified by these tests.
