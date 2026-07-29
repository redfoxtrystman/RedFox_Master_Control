# JOB-09 v0.4.4 Build Audit — 2026-07-29

## Build

`RedFox Tow & Recovery Dispatch v0.4.4`

Primary scope:

- scan all installed BeamNG model/config entries exposed by the vehicle/config generator, including vehicle-style props;
- one-at-a-time exact model/config role classification through the JOB-09 WEUI;
- immediate persistent catalog saves at `settings/redfox/tow_vehicle_spawnable_catalog.json`;
- per-item live Scene Builder reclassification;
- police-configured semi and emergency/support target protection;
- spreader bar, recovery equipment, and traffic-control prop target protection;
- external Edge/Chrome JSON manager for the catalog, settings, and saved scenes;
- saved-scene enable/disable control;
- Random Events 2.1-compatible detection, warm-up, Timber Spill, and RV Trouble scene imports.

## Static and mocked verification

- 53/53 source verification checks passed.
- All Lua files compile under `texlua`.
- Main Lua extension loads under the JOB-09 mock environment.
- All JavaScript passes `node --check`.
- External manager embedded JavaScript passes `node --check` after extraction.
- All JSON parses successfully.
- Mocked classification verifies:
  - `fp_spreaderbar/short` -> `equipment_prop`, not a tow target;
  - police semi -> `police_support`, not a normal tow target;
  - dry van -> `trailer_target`;
  - civilian semi -> `semi_tractor`.
- Mocked catalog scan and persistent role switching pass.
- Mocked Random Events 2.1 detection and comma-separated `prewarmEvents` call pass.
- Uploaded Random Events 2.1 ZIP contains 75 event modules and the required manager, incident, dispatch, spawning, map-scanner, Timber Spill, and RV Trouble modules.

## Boundaries

- No Random Events file was copied, edited, or overridden.
- No stock Career/RLS core file was replaced.
- Runtime behavior remains unproven until David tests the exact ZIP in BeamNG with only one JOB-09 version and only Random Events 2.1 enabled.
