# BeamNG Mod QuickScan v0.4.5 — Results Workspace, Previous Scans, Career Wizard

**Date:** 2026-07-29 PDT  
**Owner:** David / Captain  
**Baseline:** exact packaged v0.4.4 source  
**Status:** `STATIC/SELF-TEST VERIFIED — PACKAGED COPY VERIFIED — WINDOWS REAL-LIBRARY TEST REQUIRED`

## Exact hashes

```text
v0.4.5 source SHA-256
35d24dda45ae14ed7169f6ebe7862c11403d3f45c6326736cfd0d96eb684fa2b

v0.4.5 final package SHA-256
0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939
```

## Delivered behavior

### Results workspace

- `Maximize Results Area` hides the upper scanner controls so Findings, Duplicate Review, Catalog, Career Data, DRM Details, and Previous Scans fill the window.
- `Restore Full Window` brings the scanner controls back.
- Findings use stable category colors and visible separators.
- Catalog and Career tables include horizontal/vertical scrolling and row separators.

### Previous scans

A new `scan_runs` SQLite table preserves folder-by-folder runs with:

- folder path;
- date/time and status;
- total/completed mods;
- red/yellow findings;
- duplicate count;
- career ready / needs info / not ready / reviewed totals;
- complete result JSON.

Sort options:

- newest;
- oldest;
- folder A-Z;
- most red findings;
- most duplicates;
- most career-ready configurations.

### Catalog status lights

Each mod row reports:

- name/version check;
- duplicate check;
- preview/icon extraction;
- career readiness;
- edited and renamed history.

Colors:

- green — completed/clear;
- yellow — completed but needs attention;
- red — missing or confirmed problem;
- blue — manually reviewed/corrected or images extracted.

### Duplicate delete safety

`Delete Selected Duplicate (Quarantine)`:

- refuses to delete the chosen keeper;
- moves the selected redundant/older ZIP into `_QuickScan_Deleted_Duplicate_Quarantine`;
- appends `_DELETED_DUPLICATE` to the ZIP and matching image names;
- writes a manifest before/after each operation;
- uses the existing hash-verified Undo path.

The red-dot folder icon is now best-effort. A denied/locked `desktop.ini` no longer aborts cleanup. QuickScan clears Windows file attributes when possible and writes `RED_DOT_REVIEW_FOLDER.txt` when icon customization cannot be applied.

### Career readiness and wizard

Readiness colors:

- green — spawn-ready and important career metadata present;
- yellow — likely to work but important information is missing;
- red — model/config/.pc spawn requirement missing;
- blue — manually reviewed and complete.

The wizard includes native BeamNG configuration fields:

- Configuration and Description;
- Value and Years;
- Population;
- Drivetrain, Fuel Type, Propulsion, Transmission;
- Performance Class and Config Type;
- Body Style, Derby Class, Induction Type, Country;
- Power, Torque, Weight, Top Speed;
- default paint names.

RedFox planning fields are clearly separated:

- traffic policy and generated vehicle-group name;
- dealership/filter intent and optional facility id;
- library category override;
- user notes.

Each field has an explanation popup.

### Non-destructive career patches

The wizard can create:

```text
RedFoxTools/BeamNG Mod QuickScan/career_patches/RedFox_CareerPatch_*.zip
```

A patch may contain:

- `vehicles/<model>/info_<config>.json` with user-approved native values;
- a valid `vehicleGroups/*.vehGroup.json` using native `model` and `config` when explicit traffic grouping is requested;
- `redfox/career_plan.json`;
- a removal/undo README.

The original mod ZIP is not rewritten.

Dealership intent is not falsely written as a made-up per-vehicle shop field. Current BeamNG dealership facilities select inventory through filter data, including fields such as `Config Type`.

## Official documentation checked

- `https://documentation.beamng.com/modding/file_formats/vehicle_groups/`
- `https://documentation.beamng.com/world_editor/windows/vehicle_groups_editor/`
- `https://documentation.beamng.com/modding/vehicle/tutorials/configs/`
- `https://documentation.beamng.com/modding/levels/level_formats/facilities/`

## Verification

```text
PASS  exact v0.4.4 baseline compile
PASS  exact v0.4.4 full self-test
PASS  v0.4.5 compile
PASS  inherited full scanner/duplicate/image/version self-test
PASS  v0.4.5 extended self-test
PASS  invalid/locked desktop.ini fallback
PASS  scan-history persistence
PASS  career override storage/export
PASS  career patch ZIP and vehicle-group generation
PASS  duplicate delete-to-quarantine
PASS  hash-verified duplicate undo
PASS  GUI construction
PASS  results maximize/restore
PASS  final ZIP reopen/CRC
PASS  packaged compile
PASS  packaged inherited and extended self-tests
PASS  packaged GUI smoke
PASS  packaged career-patch integration
PASS  packaged quarantine/undo integration
```

## Not yet proven

- physical Windows DPI and mouse interaction;
- real Windows Explorer icon refresh on David's computer;
- full-size library behavior with hundreds/thousands of mods;
- game-runtime behavior of every generated career patch;
- every third-party vehicle's nonstandard metadata.

## Next version boundary

v0.5.0 is reserved for the Incoming-folder automatic sorter: vehicles by make/model, maps and map add-ons, UI, AI/traffic, career/gameplay, duplicate and older-version handling, images, and final processing lights. The later v0.6.0 boundary remains installed/storage mod management and video mod packs.