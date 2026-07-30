# BeamNG Mod QuickScan v0.4.6 — JOB-09 Tow Catalog Foundation

**Date:** 2026-07-29 PDT  
**Owner:** David / Captain  
**Baseline:** exact packaged v0.4.5 source  
**Status:** `STATIC/SELF-TEST VERIFIED — REAL CARAVAN VALIDATION PASS — WINDOWS/JOB-09 RUNTIME NOT YET PROVEN`

## Ownership boundary

QuickScan owns ZIP scanning, exact-configuration inventory, preview extraction, classification UI, online-source provenance, Career repair UI, and writing `catalog_v2.json`. JOB-09 owns reading the approved catalog, call generation, year filters, lien/found-property behavior, tow-yard custody, scene systems, and writing `runtime_observed.json`.

## Preserved behavior

v0.4.6 keeps the v0.4.5 scanner, duplicate/version/conflict workflows, version-only naming, duplicate organizer/quarantine/Undo, image extraction, Career wizard, DRM indicators, previous scans, status lights, pause/resume, checkpoints, and one-ZIP-at-a-time operation.

## Added Tow Catalog module

- Separate Tow Catalog tab.
- Exact identity is source ZIP SHA-256 + model + configuration.
- Separate physical type, service type, lien/property type, and 17 independent call/use permissions.
- New entries and runtime-observed entries start Unreviewed.
- Police/emergency/trailer/equipment/prop/race suggestions include evidence and confidence.
- Exact configuration previews are extracted when present.
- Save & Next, Previous, Skip, Unreviewed, Never Use, Copy to Selected, Apply to Model, Undo, Search Online, Open Source ZIP, and View Internal Files.
- Bulk operations warn first and skip manually reviewed exceptions.
- Manual exact-configuration values survive rescans.
- Online source name, URL, checked date, confidence, and David approval are stored.
- Normal Tow Catalog work does not rewrite source ZIPs.

## Output

`<Selected BeamNG User Folder>/settings/redfox/tow_catalog/`

- `catalog_v2.json`
- `runtime_observed.json`
- `scan_manifest.json`
- `previews/`
- `backups/`

Safe write order: write `catalog_v2.json.new`, parse and validate it, back up the old catalog, replace `catalog_v2.json`, and retain the timestamped backup.

## Hashes

```text
v0.4.5 baseline package
0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939

v0.4.6 source
b9577c76d86a33b9b4b05425f5337dd3cdab7859c004dff2d13455ade9261ae4

v0.4.6 package
436527a8fbbb610104618061c652add4ada96537b6877e95355794292a8b917d
```

## Verification

```text
PASS  v0.4.5 baseline compile and full self-test
PASS  v0.4.6 compile and inherited tests
PASS  v0.4.6 Tow Catalog self-test
PASS  exact model/config separation
PASS  manual review survives rescan
PASS  runtime_observed import
PASS  safe catalog validation/replacement and timestamped backup
PASS  GUI/Tow Catalog construction
PASS  real caravan four-configuration inventory
PASS  real caravan exact configuration image selection
PASS  real caravan source ZIP unchanged
PASS  final ZIP reopen/CRC
PASS  extracted packaged compile/self-tests/GUI smoke
```

## Not yet proven

- David's real Windows D-drive path interaction;
- physical DPI and long-library behavior;
- JOB-09 reading and enforcing the catalog;
- the full requested proof set of police semi, spreader bar, crane attachment, mobile crane, rolling chassis, props, race configs, and year profiles;
- automatic online enrichment beyond browser-assisted search and stored provenance.
