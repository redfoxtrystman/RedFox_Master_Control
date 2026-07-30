# QuickScan v0.4.7.1 Source Baseline and Verification

## Baseline

- Parent version: v0.4.7 Whole-Window Scroll + Saved Scan Snapshots + Master Catalog
- Source SHA-256: `35f415769d9a52c5d59832927a7d513d715ecfe27afc240cf85534a85780e208`
- Package SHA-256: `b6c3b56292d1bf26c2dfaac3340d449a49c18c027dc309d3817f30001dedd95a`
- Complete editable source is included inside the packaged download as `BeamNG Mod QuickScan.pyw`.

## Verified behavior

- Normal result tabs default to the selected scan folder.
- Explicit All Scanned Folders view combines retained records.
- Master Catalog remains the cross-folder workspace.
- Images extract automatically by default.
- Settings can hide secondary controls and columns.
- Catalog processing state uses one compact labeled four-color field.
- Missing commas between adjacent JSON object fields are safely recovered in memory.
- Extra closing delimiters after a complete top-level object are safely ignored.
- Source ZIPs remain unchanged.
- Unrecoverable metadata causes only that metadata file to be skipped.

## Uploaded metadata regressions

### stpmustang.zip

`vehicles/Mustang67/info_tissma.json`

Recovered by inserting the missing comma before the `0-60 mph` field and removing the trailing comma in Years.

### WSCX_ChevBel-Air.zip

`vehicles/belairkene/info.json`

Recovered by removing the trailing comma and trimming one extra top-level closing brace.

## Tests

```text
PASS compile
PASS all inherited self-tests
PASS new v0.4.7.1 self-test
PASS exact metadata parse tests
PASS complete two-ZIP scan with zero malformed findings
PASS automatic image extraction: six previews
PASS selected-folder GUI: one folder only
PASS All Scanned Folders GUI: both folders
PASS Settings GUI
PASS package CRC and extracted-copy tests
```

## Unproven runtime boundary

David must still test physical Windows display behavior, saved settings across restarts, and a large real mod collection on the D: drive.
