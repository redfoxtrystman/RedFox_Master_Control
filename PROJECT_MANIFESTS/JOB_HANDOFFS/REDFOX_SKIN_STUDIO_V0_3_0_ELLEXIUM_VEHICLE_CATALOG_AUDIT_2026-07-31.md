# RedFox Skin Studio v0.3.0 — Ellexium Vehicle Catalog Integration Audit

Date: 2026-07-31

## Locked baseline

RedFox Skin Studio v0.2.9 was frozen before new work began.

- Package: `RedFox_Skin_Studio_v0_2_9_DECAL_CATALOG_LAYERED_SKINS_BUILT_RUNTIME_UNTESTED.zip`
- SHA-256: `be0dc3be6cb914cc15db42ca49293a5e7092f6243a7a22adb0430ce48749c353`
- Rule: do not replace or silently modify the v0.2.9 package. All new work begins in v0.3.0 or later.

## v0.3.0 package

- Package: `RedFox_Skin_Studio_v0_3_0_ELLEXIUM_VEHICLE_CATALOG_BUILT_RUNTIME_UNTESTED.zip`
- SHA-256: `818ad6ca5294b0817dbba9c98a0a9a28fab7a1bc84c43417031182cfac40169b`
- Status: **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**

## Added from the Ellexium reference workflow

EllexiumModManager 0.2.0 was reviewed under its MIT license. RedFox now contains an independently adapted stage-one vehicle/configuration catalog:

- Read-only scans of configured BeamNG stock vehicle ZIPs, mod ZIPs, extra mod-storage folders and unpacked vehicle folders.
- Detection of `vehicles/<vehicle_id>/` roots.
- Exact `.pc` configuration indexing.
- Parsing of `info.json` and `info_<config>.json` using RedFox's tolerant BeamNG JSON parser.
- Matching configuration preview PNG/JPG/JPEG/WEBP/BMP discovery.
- Shared-workspace thumbnail caching at 480×270.
- Incremental reuse based on source size and modification time.
- Picture-first vehicle cards and exact configuration cards.
- Search by vehicle, configuration, ZIP, source path, description and tags.
- Filter by source ZIP/folder.
- Exact configuration selection saved for the planned BeamNG live-preview bridge.
- Prepared `core_vehicles.spawnNewVehicle(...)` command record.
- Ellexium MIT attribution in `THIRD_PARTY_NOTICES.md` and `third_party/ellexium/LICENSE`.

## Deliberate boundary

Version 0.3.0 does not install or execute a BeamNG bridge. `Prepare BeamNG Spawn Command` writes a record marked `PREPARED_ONLY_NO_LIVE_BRIDGE_INSTALLED`. The application must not claim that exact in-game preview is working until David tests a later bridge build in BeamNG.

## Validation completed

- Python `compileall`: pass.
- JavaScript syntax check: pass.
- Existing backend self-test: pass.
- New fake-vehicle catalog fixture: pass.
- Configuration metadata parsing: pass.
- Preview thumbnail extraction/cache: pass.
- Selected-configuration persistence: pass.
- Prepared spawn-command output: pass.
- Real Wigeon ZIP scan: 1 vehicle, 7 configurations, 7 preview images, no scanner errors.
- Incremental Wigeon cache test: pass.
- Final ZIP integrity test: pass.

## Not tested here

- Live PySide6/Qt interface on Windows.
- David's complete BeamNG and mod-folder scan.
- BeamNG configuration spawning.
- In-game texture refresh/live preview.
- Three.js or Blender preview behavior on Windows.
