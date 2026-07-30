# BeamNG Mod QuickScan v0.4.7.1 — Folder Focus, Metadata Recovery, Settings, and Solid Status Lights

**Date:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Baseline:** exact verified v0.4.7 package/source  
**Status:** `PACKAGED TESTS PASS — WINDOWS LARGE-LIBRARY TEST REQUIRED`

## Owner-reported failures corrected

1. Normal tabs were showing retained mods from other scanned folders.
2. Preview extraction needed to be automatic rather than another visible scan option.
3. Scan tuning and secondary columns needed a Settings area so the normal screens could stay compact.
4. The four processing lights looked like indistinguishable shaded circles and were too far apart.
5. `stpmustang.zip` and `WSCX_ChevBel-Air.zip` produced yellow malformed-metadata findings that QuickScan should safely recover or bypass.

## Folder-focus law

Normal result tabs default to the currently selected scan folder:

- Findings
- Duplicate Review
- Catalog / Rename
- Career Data
- DRM Details
- Previous Scans
- Tow Catalog

`View: All scanned folders` explicitly requests combined results. Master Catalog remains the dedicated cross-folder conflict and duplicate view.

## Metadata recovery

The tolerant in-memory parser now recognizes:

- comments;
- trailing commas;
- a missing comma between adjacent object fields;
- surplus closing delimiters after a complete top-level JSON value.

The original source ZIP is never rewritten during a scan. If a metadata file still cannot be recovered, QuickScan skips only that metadata file and continues scanning the rest of the ZIP.

Exact uploaded results:

```text
stpmustang.zip
vehicles/Mustang67/info_tissma.json
- inserted missing comma before line 18 object field
- removed trailing comma
- valid after safe recovery

WSCX_ChevBel-Air.zip
vehicles/belairkene/info.json
- removed trailing comma
- trimmed extra closing delimiter after complete top-level object
- valid after safe recovery
```

A complete scan of the two uploaded ZIPs produced:

```text
Completed ZIPs: 2
Extracted previews: 6
Unrecoverable metadata findings: 0
Yellow findings: 0
```

## Automatic images

Image extraction is enabled automatically by default. Its destination remains configurable as:

- Beside ZIP + Catalog
- Catalog folder only
- Beside ZIP only

Normal image extraction never rewrites source ZIP contents.

## Settings

The new Settings window can hide or show:

- scan-tuning controls;
- summary cards;
- Catalog action buttons;
- compact progress column;
- Edited/Renamed history;
- DRM column;
- Safe/Review column;
- compact catalog rows.

It also controls automatic image extraction and the default selected-folder/all-folder view.

## Solid progress display

The previous four separated status cells are replaced with one compact labeled field:

```text
🟨 ZIP  🟥 DUP  🟦 IMG  🟩 CAR
```

- ZIP = filename/version check
- DUP = duplicate audit
- IMG = image extraction
- CAR = Career check
- `✓` = completed and clear
- `!` = completed but needs attention

The letters keep the states understandable even when Windows renders color emoji differently.

## Exact hashes

```text
v0.4.7.1 source
35f415769d9a52c5d59832927a7d513d715ecfe27afc240cf85534a85780e208

v0.4.7.1 package
b6c3b56292d1bf26c2dfaac3340d449a49c18c027dc309d3817f30001dedd95a
```

## Verification

```text
PASS source compile
PASS inherited v0.4.4/v0.4.5/v0.4.6/v0.4.7 self-tests
PASS v0.4.7.1 metadata/folder-scope self-test
PASS exact Mustang metadata recovery
PASS exact Bel-Air metadata recovery
PASS exact two-ZIP complete scan
PASS six automatic preview exports
PASS zero malformed-metadata findings on uploaded pair
PASS selected-folder GUI scope
PASS explicit all-folder GUI scope
PASS Settings GUI construction
PASS compact progress columns
PASS final ZIP CRC/reopen
PASS packaged compile/self-tests/GUI smoke
```

## Next boundary

v0.4.8 remains the larger Ellexium-assisted visual vehicle/configuration gallery and wizard redesign. This v0.4.7.1 package is a focused corrective release so those urgent scan and readability failures do not wait for the gallery rewrite.
