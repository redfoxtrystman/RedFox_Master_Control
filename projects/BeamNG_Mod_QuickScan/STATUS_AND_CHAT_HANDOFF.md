# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.8 Usability + Vehicle Gallery  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_8_USABILITY_VEHICLE_GALLERY.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_8/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_OPERATIONS_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.8 release records
5. v0.4.8 verification
6. This file

## Current truth

- v0.4.7.3 is the exact verified baseline used for v0.4.8.
- Filename-only rename remains strict manifest-only: no second ZIP, image, or report copy.
- v0.4.8 fixes owner-reported thick separator rows, unclear status shades, broken folder focus, empty Previous Scans details, giant Career/Tow forms, missing hover help, and nonfunctional Tow double-click behavior.
- Normal result tabs show the selected folder only.
- All-folder results must be explicitly requested.
- Master Catalog remains the cross-folder duplicate/conflict workspace.
- Previous Scans lists all retained runs and immediately shows the selected run's exact saved ZIPs and findings.
- Artificial separator rows are removed from Catalog, Career, Tow, and history detail lists.
- Catalog uses four tightly grouped true on/off image lights: yellow ZIP, red duplicate audit, blue images, green Career.
- A new Vehicles tab shows model/source-ZIP image cards and exact configuration cards.
- Left-click a model card opens all `.pc` configurations.
- Double-click a configuration opens Career Wizard; right-click provides Career, Tow/JOB-09, source, and exact-ID actions.
- Career and Tow editors are compact page-by-page wizards.
- Hovering fields or `?` buttons explains meaning, examples, blank behavior, and allowed values.
- Clicking `?` opens official BeamNG documentation where available.
- Settings can hide tabs, cards, scan tuning, Catalog actions, and optional columns without deleting scan data.
- Automatic image extraction remains enabled by default.
- Physical Windows DPI and full-library performance remain David's required tests.

## Exact hashes

```text
v0.4.8 source
4aa75d06eb9928659f29ee05d2bb8af8a89c6aac49584da806a25c8e52494cc0

v0.4.8 package
6382a98c776f0d2c664b9c86a946405cb9100886ada6e3600d6de670a0c2cd82
```

## UI laws

```text
NORMAL TABS SHOW THE SELECTED FOLDER.
ALL-FOLDER VIEW IS EXPLICIT.
MASTER CATALOG IS CROSS-FOLDER.
PREVIOUS SCANS SHOW SAVED RUN CONTENTS.
NO FAKE SEPARATOR ROWS.
LIGHTS MUST BE BRIGHT ON / DARK OFF, NOT AMBIGUOUS SHADES.
HOVER HELP MUST EXPLAIN WHAT TO ENTER.
```

## Visual vehicle workflow

```text
SCAN ZIP
→ VEHICLE MODEL CARD
→ LEFT-CLICK FOR EXACT CONFIGURATIONS
→ DOUBLE-CLICK CONFIG FOR CAREER
→ RIGHT-CLICK FOR CAREER / TOW / SOURCE / IDS
```

Vehicle identity remains source ZIP + model. Tow identity remains source ZIP hash + exact model + exact configuration.

## Career help law

- Do not invent values.
- Preserve internal metadata where available.
- Population is relative selection weight, not a percentage.
- Performance Class should be preserved or obtained from BeamNG testing rather than guessed.
- Config Type uses common BeamNG values such as Factory, Police, Race, Custom, Service, Rally, and Powerglow.
- Vehicle-group records use exact model and recommended exact config IDs.
- RedFox shop/Tow planning fields must not be presented as universal native BeamNG fields.

## Rename safety law

```text
RENAME THE EXISTING ZIP IN PLACE.
CREATE NO SECOND ZIP COPY.
WRITE ONLY PATHS, SHA-256, TIMESTAMP, WARNING, AND UNDO HISTORY.
```

## Verification

```text
PASS Python compilation
PASS complete inherited self-test chain
PASS selected-folder and explicit combined-folder scope
PASS two retained folders and Previous Scans detail contents
PASS stoplight images and no separator rows
PASS Career and Tow double-click wizards
PASS visual vehicle/configuration gallery
PASS preview matching
PASS Settings/tab visibility
PASS real Mustang/Bel-Air metadata regression
PASS final ZIP CRC and extracted-package tests
PASS package contains no uploaded user mod ZIPs
```

## What David should test

1. Extract v0.4.8 into a completely new folder.
2. Scan one copied folder and confirm Catalog, Career, Tow, Findings, and Vehicles show only that folder.
3. Scan a second folder and switch between them through the Folder selector.
4. Open Previous Scans and confirm each run shows its own ZIPs and findings.
5. Confirm the four Checks lights are visibly bright/dark and tightly grouped.
6. Open Vehicles, left-click a model, then double-click and right-click exact configurations.
7. Hover Career/Tow fields and click `?` documentation links.
8. Use Settings to hide and restore screens/columns.
9. Report Windows DPI, JPG rendering, and large-library performance.

## Next version boundary

```text
v0.4.9 — Tow online enrichment and representative JOB-09 proof set
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
v0.4.8 release: dd3f018b3d5c9dd91d22bf73ca8e164cb81624b4
v0.4.8 verification: 0f53332a3ff3201f74948cfc1f4313bba9bdd4ed
Status: this commit
```
