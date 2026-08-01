# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-31 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.8.1 Visible Career/RLS Dropdowns  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_8_1_VISIBLE_CAREER_DROPDOWNS.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_8_1/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_OPERATIONS_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.8.1 release records
5. v0.4.8.1 verification
6. This file

## Current truth

- v0.4.8 is the exact verified baseline used for v0.4.8.1.
- Filename-only rename remains strict manifest-only: no second ZIP, image, or report copy.
- All dropdowns now use a high-contrast popup window instead of a native menu/combobox that may render invisible on Windows.
- Popup windows contain search, visible option list, scrollbars, exact stored value, explanation, Use Selected, and Custom only where safe.
- Career fixed-choice fields use controlled BeamNG tokens instead of blank free-text boxes.
- Config Type choices: Factory, Custom, Race, Police, Service, Powerglow, Rally.
- Common drivetrain/fuel/propulsion/transmission/induction choices follow BeamNG documentation; existing real nonstandard values may be preserved.
- Fuel Type uses Battery for electric energy metadata; Propulsion uses Electric.
- Performance Class defaults to blank/BeamNG automatic testing rather than guessing.
- Population is relative, not a percentage. 500 and 10000 are included as owner-supplied community examples and are not labeled official limits.
- Career/RLS marketplace readiness separately checks Value, Population, and Config Type; Years is recommended.
- The owner-supplied `info_Coupe LHD [B].json` has a trailing comma. QuickScan recovers it while scanning and writes strict valid patch JSON.
- v0.4.8 folder focus, Previous Scans, stoplights, Vehicles gallery, Career/Tow wizards, hover help, Settings, and Master Catalog remain preserved.
- Physical Windows DPI/multi-monitor, full-library performance, and in-game RLS/Career marketplace behavior remain David's required tests.

## Exact hashes

```text
v0.4.8.1 source
77987e21a4f9049d6ee8c1bb4c06a0a04f7f60d0f44ce65ea656853834b81e01

v0.4.8.1 package
0df54be70aa9a44f32bc9073b9c77a87ba56f7d89921f29a597e386bae50ed92
```

## Visible choice law

```text
FIXED-CHOICE FIELDS MUST NOT BE BLANK FREE-TEXT BOXES.
CHOICES MUST OPEN IN A HIGH-CONTRAST WINDOW.
OPTIONS, SEARCH, SCROLLBARS, STORED VALUE, AND EXPLANATION MUST BE VISIBLE.
SELECTED VALUES MUST REMAIN READABLE AFTER CLOSING THE POPUP.
DO NOT INVENT FIXED CHOICES FOR VEHICLE-SPECIFIC OR MEASURED NUMBERS.
```

## Career/RLS field law

- Dropdown: Drivetrain, Fuel Type, Propulsion, Transmission, Induction Type, Config Type, Body Style, Population, Performance Class handling, traffic policy, dealership policy.
- Numeric/text validation: Value, Years, Power, Torque, Weight, Top Speed.
- Value, Population, and Config Type are marketplace readiness checks based on the supplied tested workflow.
- Years is recommended.
- Performance Class is measured by BeamNG's automatic test; leave blank instead of guessing.

## Folder and UI laws preserved

```text
NORMAL TABS SHOW THE SELECTED FOLDER.
ALL-FOLDER VIEW IS EXPLICIT.
MASTER CATALOG IS CROSS-FOLDER.
PREVIOUS SCANS SHOW SAVED RUN CONTENTS.
NO FAKE SEPARATOR ROWS.
STOPLIGHTS MUST BE BRIGHT ON / DARK OFF.
```

## Rename safety law preserved

```text
RENAME THE EXISTING ZIP IN PLACE.
CREATE NO SECOND ZIP COPY.
WRITE ONLY PATHS, SHA-256, TIMESTAMP, WARNING, AND UNDO HISTORY.
```

## Verification

```text
PASS Python compilation
PASS complete inherited self-test chain
PASS visible-choice self-test
PASS high-contrast popup GUI
PASS search and scrollbars
PASS option foreground/background contrast
PASS Career powertrain and classification dropdowns
PASS supplied template recovery
PASS strict generated JSON
PASS Career/RLS readiness fields
PASS final ZIP CRC and extracted-package tests
PASS package contains no uploaded mod ZIPs/images
```

## What David should test

1. Extract v0.4.8.1 into a completely new folder.
2. Scan one small copied folder.
3. Open Career Data and double-click an exact configuration.
4. Open every purple Choose field and confirm all options remain visible at the current Windows scale.
5. Select Config Type, drivetrain, fuel, propulsion, transmission, induction, and Population.
6. Confirm the selected value remains readable after each popup closes.
7. Build one test patch and verify Free Roam sidebar price plus RLS/Career marketplace behavior.
8. Report Windows scaling/multi-monitor and large-library behavior.

## Next version boundary

```text
v0.4.9 — Tow online enrichment and representative JOB-09 proof set
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
v0.4.8.1 release: c16620bf951b7798ac7fb2170fbeb732493c404a
v0.4.8.1 verification: 12db1ed49f1e2159f4c9a94ee1fa7ef7f6af4871
Status: this commit
```
