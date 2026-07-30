# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-29 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.6 JOB-09 Tow Catalog Foundation  
**Latest release:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_6_JOB09_TOW_CATALOG_FOUNDATION.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/README_AND_VERIFICATION.md`  
**Tow schema:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_6/TOW_CATALOG_SCHEMA_V2.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.6 release records
5. v0.4.6 verification and Tow Catalog schema
6. This file

## Current truth

- v0.4.5 is the exact verified baseline used for v0.4.6.
- Baseline package hash matched before editing and baseline compile/self-test passed.
- v0.4.6 is additive; it does not replace the scanner, duplicate organizer, image extraction, Career wizard, scan history, or version-only naming.
- QuickScan owns scanning, classification UI, online-source provenance, Career repair, and writing `catalog_v2.json`.
- JOB-09 owns reading the approved catalog, call/year/lien behavior, custody/scenes, and writing `runtime_observed.json`.
- Tow Catalog identity is source ZIP hash + exact model + exact configuration.
- New and runtime-observed entries start Unreviewed.
- Physical type, service type, lien/property type, and 17 permissions are independent.
- Manual exact-configuration reviews survive rescans.
- Bulk actions warn first and skip reviewed exceptions.
- Exact configuration images are preferred over generic mod previews.
- Tow Catalog writes safely under the selected BeamNG user folder on any drive.
- Normal Tow Catalog work does not rewrite source mod ZIPs.
- v0.4.6 passed inherited tests, Tow tests, packaged tests, GUI smoke, and real caravan validation.
- Windows D-drive behavior and JOB-09 runtime integration remain required tests.

## Exact hashes

```text
v0.4.5 baseline package
0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939

v0.4.6 source
b9577c76d86a33b9b4b05425f5337dd3cdab7859c004dff2d13455ade9261ae4

v0.4.6 final package
436527a8fbbb610104618061c652add4ada96537b6877e95355794292a8b917d
```

## Tow Catalog output

```text
<BeamNG User Folder>/settings/redfox/tow_catalog/
├── catalog_v2.json
├── runtime_observed.json
├── scan_manifest.json
├── previews/
└── backups/
```

Safe write: `.new` -> parse/validate -> backup -> atomic replacement.

## Tow Catalog UI

- Rebuild Exact Configurations
- Write catalog_v2.json
- Import runtime_observed.json
- Previous / Save & Next / Skip
- Mark Unreviewed / Mark Never Use
- Copy to Selected / Apply to Model
- Undo
- Search Online with provenance fields
- Open Source ZIP / View Internal Files
- Exact preview panel
- Separate physical, service, lien/property, year, review, and permission controls

## Preserved laws

### ZIP naming

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD OR UPDATE A REAL VERSION TOKEN.
NEVER REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
DO NOT INVENT A VERSION.
```

### Duplicate safety

- Exact/repacked/functional/older-version evidence remains.
- Generic folders or similar names alone are not proof.
- Gameplay variants remain review-only.
- Moves/deletes are reversible and manifest-backed.

### Tow review safety

- Suggestions are not approval.
- Unreviewed entries are not JOB-09 targets.
- Manual exact-config reviews override future suggestions.
- Bulk actions skip reviewed exceptions.
- Catalog-only work never modifies source ZIPs.

## Verification

```text
PASS  v0.4.5 baseline compile/full self-test
PASS  v0.4.6 compile and inherited tests
PASS  Tow Catalog extended self-test
PASS  exact-config inventory and suggestions
PASS  manual override survival
PASS  runtime-observed import
PASS  safe write and backup
PASS  real caravan four configs and four exact images
PASS  source caravan hash unchanged
PASS  final ZIP CRC/extracted compile/self-tests/GUI smoke
```

## Required next tests

1. Extract v0.4.6 into a new folder and confirm the title.
2. Select the D-drive BeamNG user folder.
3. Run a completed copied-folder scan.
4. Rebuild Tow Catalog and review exact configurations.
5. Save one reviewed entry and confirm it survives another scan/rebuild.
6. Write `catalog_v2.json` and inspect backup behavior.
7. Give JOB-09 the schema and test its reader.
8. Have JOB-09 write sample `runtime_observed.json`; import it into Unreviewed.
9. Test representative police semi, trailer, spreader bar, crane attachment, mobile crane, rolling chassis, prop, race, classic, and modern configurations.

## Version boundary

```text
v0.4.7 — Tow Catalog online enrichment and full representative proof set
v0.5.0 — incoming-folder automatic sorter
v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Commits

```text
Release: 3e3806c61267304a7fad0ba6315267829d4ef173
Schema: 3d03ccced4664db955f79234f1a28ea0ca5ff027
Verification: f8673d4e57a62e26df0e46472db7380b7ed488e5
```
