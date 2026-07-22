# RedFox Skin Studio v0.2.1 — Vehicle Library and Editor Usability Hotfix

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_1_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `7402125eeaca928cd587bcaf0d75d39df00b58b879d58e07d679af84b672cf48`

## Why this corrective build was required

David tested v0.2.0 and reported the following urgent defects/missing requirements:

- The embedded Vehicle Setup dropdown did not populate.
- Old artwork/skins could not be conveniently saved and transferred to another vehicle.
- There was no persistent album for logos, photographs, decals and reference images.
- The editor still looked and behaved too much like the inherited source application.
- Undo/redo needed a visible named history.
- UV wire grids must never be flattened into saved/exported skins.
- The program must scan all configured stock and mod vehicles.
- Selecting D-Series or another vehicle should show existing skins plus blank and alternate cab/bed/body texture candidates.
- The built-in painting workflow must be clearer and closer in organization to a normal paint editor.

These were valid application issues. This hotfix addresses them directly; it is not a claim of full Paint.NET, Krita or Forza parity.

## Implemented in v0.2.1

### Working vehicle/source catalog path

- The PySide desktop host now generates the real indexed vehicle/source catalog and sends it into the embedded editor.
- The broken inherited local-manifest-only dropdown path is no longer used for desktop operation.
- Each vehicle can expose separately labeled:
  - `Existing skin` sources, opened as editable/exported artwork
  - `Blank UV guide` sources, opened as reference-only
  - `Body variant UV` candidates, generated from likely paintable DAE materials

### Complete configured-folder index action

- Added `Full Index: All Vehicles, Skins + Body Variants`.
- Scans configured stock vehicle archives from the BeamNG installation.
- Scans active mod and external mod-storage ZIPs.
- Scans unpacked mod folders.
- Deep mode generates DAE UV candidates even when a basic UV template exists, so alternate cab, bed, sleeper and body meshes can appear.
- Removed broad `uv1` template classification because it incorrectly treated real stock skin textures as UV grids.

### Existing-skin discovery

- Material JSON is inspected for skin texture references.
- Existing stock/mod skin textures are extracted under each vehicle profile's `Existing_Skins` folder.
- Existing skins are listed before blank/generated UV guides in the native and embedded source menus.

### Asset Album

- Added a persistent workspace `Asset_Album`.
- Supports PNG, JPG/JPEG, WebP, BMP, TIFF, GIF first frame and DDS.
- Native thumbnail album includes Import Images and Add to Canvas.
- Embedded album supports double-click insertion and dragging onto the canvas.
- DDS assets are converted by the host for thumbnails/insertion.

### Reusable Design Vault

- Added persistent workspace `Design_Vault`.
- `Save Current Design` stores all non-base/non-guide layers as `.rfdesign`.
- `Load on Vehicle` places the design over another vehicle/template while preserving existing work.
- Source coordinates, sizes and font sizes are scaled to the new texture dimensions.
- Supports importing `.rfdesign`, `.rfskin` and compatible JSON design files.

### Editor and history improvements

- Added visible labels for Select, Pan, Brush, Erase, Shapes, Fill, Gradient, Pick, Text, Path and Line tools.
- Added RedFox-owned logo/favicon/guide and removed the inherited external project link/branding from the editor help.
- Removed external font dependencies.
- Added a visible 100-state History panel with named entries, clickable state navigation, undo/redo action descriptions and clear-history control.
- Existing paint presets remain: hard round, soft airbrush, marker, spray, splatter/mud and square/pixel.

### UV grid export protection

- Blank and generated UV sources are opened with `excludeFromExport=true`.
- They receive a visible `NOT EXPORTED` guide badge.
- Final PNG/DDS flattening skips `excludeFromExport` layers.
- Reusable-design serialization also excludes the vehicle base/UV guide.

## Fixture evidence

### Stock Wigeon

Fast scan:

- 1 supplied UV guide
- 3 existing stock skin textures
- 2 DAE models
- 6 likely body/material targets
- `paint_design` slot detected

Deep scan:

- 2 total UV candidates after adding the generated main-shell candidate
- all 3 existing stock skin textures retained as editable sources

### Modded Jerrdan — fast scan

- `jerrdan`: 29 DAE files, 7 likely paint/body targets, 11 paint-related slots
- `spreaderbar`: no likely paint target/UV; remains a manual-mapping case instead of being falsely marked ready

## Static and automated tests passed

- Python compile-all
- Embedded JavaScript syntax validation with Node
- Isolated backend self-test
- Asset Album import/list test
- Design Vault import/list test
- Test mod ZIP generation
- Strict generated JBeam/material JSON parsing
- Matching `.color.png` and optional `.color.dds` archive references
- HTML structure check for vehicle/source menus, album, history and 11 labeled tool controls
- Wigeon fast/deep scanner tests
- Jerrdan fast scanner test
- Final downloadable ZIP archive integrity test

## Not proven

- PySide6/QWebEngine live GUI interaction was not executed in the Linux build container because PySide6 was unavailable there.
- Windows `install.bat` and `run.bat` remain untested here.
- Windows drag/drop and GPU/WebGL preview remain untested here.
- BeamNG in-game detection/rendering of a mod made by this exact build remains untested.
- Automatic mapping cannot be guaranteed for every unusual third-party cab/bed/body material; manual candidate selection remains available.

No one may relabel this build as working until David tests this exact archive on Windows and in BeamNG.
