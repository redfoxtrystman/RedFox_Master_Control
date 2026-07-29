# RedFox Skin Studio v0.2.9 — Decal Catalog + Layered Vehicle Skin Audit

Date: 2026-07-29
Status: **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**

## Artifact

- File: `RedFox_Skin_Studio_v0_2_9_DECAL_CATALOG_LAYERED_SKINS_BUILT_RUNTIME_UNTESTED.zip`
- SHA-256: `be0dc3be6cb914cc15db42ca49293a5e7092f6243a7a22adb0430ce48749c353`

## Version synchronization

The central application version, visible editor version, launch metadata, build metadata, README, start guide, changelog and validation record were updated to `0.2.9`.

## Decal catalog implementation

- Added targeted scan of configured BeamNG locations for loose files and ZIP entries under `art/dynamicDecals/textures`.
- Added private local caching under the shared RedFox workspace. No BeamNG stock artwork is bundled in the public application ZIP.
- Added SHA-256 duplicate collapsing, source provenance, categories, tags, image dimensions and missing-file tracking.
- Added Keep List / Whitelist, Hide List / Blacklist, Pending Review and Everything filters.
- Added persistent reversible catalog history and `Undo Catalog Change`.
- Added default hiding of technical normal/data/metallic/roughness/opacity maps while preserving manual review.
- Added first-run automatic BeamNG scan and manual rescan.
- Added private `Decals/Inbox` staging folder.
- Added files/folder import, recursive folder intake, native desktop drag/drop and embedded editor import streaming.
- Added support for PNG, SVG, JPG/JPEG, WEBP, BMP, TIFF, GIF and DDS in RedFox.
- Added BeamNG-style `.dynDecalTexture.json` metadata generation for user imports.
- Added a 64 MB per-file safety limit for scan/import intake.
- Added an embedded category-filtered decal library with double-click and canvas drag/drop placement.

## Vehicle-scoped layered skin storage

- Saving a project skin now also archives a self-contained layered master under `Workspace/Vehicles/<vehicle>/Editable_Skins/<skin>/`.
- Added `skin.rfskin`, `preview.png`, `skin_manifest.json`, `source_assets/`, `revisions/` and `exports/`.
- Local file-backed image layers are copied and embedded into the layered master so deleting the original source does not break the saved skin.
- Added revision snapshots only when the layered master changes.
- Added `Open Vehicle Layered Skin` and `Open Vehicle Skin Folder` actions.

## Tests completed

- `python -m compileall -q .`
- `node --check web_editor/script.js`
- `python self_test.py`
- Synthetic BeamNG ZIP scan with dynamic-decal texture path and sidecar metadata
- Technical-map auto-hide behavior
- Keep-list update and catalog undo
- SVG user import and generated sidecar
- Vehicle layered archive, preview and self-contained asset embedding
- ZIP integrity test

## Tests not completed

- Windows PySide6 GUI launch
- Native Windows drag/drop behavior
- Full scan of David's BeamNG installation and mod storage
- BeamNG runtime decal use
- BeamNG in-game live-preview bridge

## Known limitations

- SVG is supported in RedFox but must be converted to PNG for direct use in BeamNG's current dynamic-decal texture workflow.
- DDS support depends on Pillow/browser decoder coverage for the DDS compression used by a particular file.
- Hiding a decal changes catalog visibility; it does not delete the private cached file.
- Catalog undo is separate from canvas undo.
