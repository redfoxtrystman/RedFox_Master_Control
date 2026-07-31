# BeamNG Mod QuickScan v0.4.8 — Usability + Vehicle Gallery

**Date:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Baseline:** exact v0.4.7.3 Strict Manifest-Only Rename

## Release purpose

This release corrects the owner-reported usability failures in v0.4.7.x and adds the requested visual vehicle/configuration workflow.

## Folder and history behavior

- Normal result tabs show the currently selected folder only.
- Combined all-folder results must be explicitly selected.
- Master Catalog remains the cross-folder duplicate/conflict view.
- Previous Scans lists all retained runs and immediately displays the selected run's saved ZIP and finding snapshots.
- Double-clicking a retained run loads a read-only historical snapshot.

## Catalog and stoplights

- Artificial separator rows were removed.
- ZIP rows are compact and no longer separated by thick blank lines.
- Four true on/off image lights are grouped tightly in one `Checks` column:
  - yellow — ZIP name/version check;
  - red — duplicate/version audit;
  - blue — useful image scan;
  - green — Career scan/review.
- Bright means completed; dark means not completed.
- Hovering the lights explains each state for the selected ZIP.

## Visual vehicle catalog

- New `Vehicles` tab.
- One image card per vehicle model/source ZIP.
- Search by vehicle name, manufacturer, model, exact configuration, ZIP, folder, and type.
- Sort by vehicle, manufacturer, source ZIP, or configuration count.
- Paged rendering limits the number of image cards displayed at once for large collections.
- Left-click opens every exact `.pc` configuration.
- Double-clicking a configuration opens the Career wizard.
- Right-click provides Career, Tow/JOB-09, source ZIP, exact-ID, and ZIP-list actions.
- Configuration images are matched by exact model/configuration when available.

## Career and Tow usability

- Giant single-page forms were replaced with compact page-by-page wizards.
- Career pages cover identity/price, powertrain, classification/traffic weight, measured performance, and RedFox traffic/shop planning.
- Tow pages cover physical/service type, year/ownership, permitted calls, and online-source provenance.
- Double-clicking Career or Tow rows opens the matching wizard.
- Hovering labels, fields, or `?` buttons shows plain-language meaning, examples, blank behavior, and allowed values.
- Clicking `?` opens the matching official BeamNG documentation page where one exists.

## Settings

- Settings can hide tabs, summary cards, advanced scan controls, Catalog actions, and optional columns.
- Hidden UI never deletes scan data.
- Automatic image extraction remains enabled by default.

## Preserved safety laws

- Filename-only renames create no backup ZIP, image copy, or report copy.
- Undo stores paths, SHA-256, timestamp, and history only.
- Ordinary scans and metadata recovery do not rewrite source ZIPs.
- Career changes are written to separate patch ZIPs.
- Duplicate movement/quarantine remains manifest-backed and undoable.
- Manual exact-configuration Career/Tow reviews survive rescans.

## Exact hashes

```text
Source SHA-256
4aa75d06eb9928659f29ee05d2bb8af8a89c6aac49584da806a25c8e52494cc0

Package SHA-256
6382a98c776f0d2c664b9c86a946405cb9100886ada6e3600d6de670a0c2cd82
```

## Verification summary

```text
PASS Python compilation
PASS inherited scanner/duplicate/version/image/DRM tests
PASS v0.4.5 Career tests
PASS v0.4.6 Tow Catalog tests
PASS v0.4.7 Master Catalog and scan snapshots
PASS v0.4.7.3 strict manifest-only rename
PASS selected-folder GUI scope
PASS two-folder Previous Scans contents
PASS true stoplight construction and no fake separator rows
PASS Career and Tow double-click wizards
PASS visual model/configuration gallery
PASS Settings and tab visibility
PASS uploaded Mustang/Bel-Air metadata regression
PASS final ZIP CRC and extracted-package tests
PASS package contains no uploaded user mod ZIPs
```

Physical Windows DPI and very-large-library behavior remain owner tests.