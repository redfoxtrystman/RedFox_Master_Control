# RedFox Skin Studio v0.2.3 — Portable Setup, Picture Browser and Simple Editor Hotfix

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_3_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `2e82dcb962c6f1715a1bdaf619a6e20affeb64b69ffdd66cd773f03c512b285e`

## Why this hotfix was required

David tested the previous setup direction and correctly reported that it made a ten-to-fifteen-second folder task turn into several minutes of redundant folder navigation. The application separately requested an install folder, workspace, BeamNG installation folder, BeamNG user folder and mod-storage folder even though David keeps every test version inside one master folder. David also reported that scanned vehicle/source choices remained text-heavy and required clicking names one by one, and that the editor still did not feel like a simple Paint 3D, Paint.NET, Krita or vector/sign workflow.

These were application-design failures. The application exists to reduce David's design work, not add setup work.

## Implemented in v0.2.3

### No separate setup maze

- `run.bat` is now the normal entry point.
- The folder containing all `RedFox_Skin_Studio_v*` folders becomes the master root automatically.
- The app creates one `_RedFox_Skin_Studio_Shared` folder inside that master root.
- The shared folder contains the Python runtime, workspace, projects, settings, vehicle profiles, Asset Album, Design Vault, thumbnails, exports, backups and caches.
- Every version inside the same master folder automatically uses that shared location.
- The shared Python runtime is created only when missing. Requirements are installed again only when the requirements-file hash changes.
- The normal launcher no longer uses `FolderBrowserDialog` or asks the owner to choose install/workspace folders.
- A one-time automatic migration attempts to copy the prior LocalAppData-configured RedFox workspace into the new shared master location without deleting the original.

### Remembered and automatically detected BeamNG paths

- BeamNG user-folder detection checks the current-version pointer, newest version folder and older Documents fallback.
- BeamNG installation detection checks Steam registry paths, Steam `libraryfolders.vdf` and common Steam/game locations on all mounted Windows drive letters.
- The active mods folder derives from the detected user folder.
- Existing valid user-selected paths are preserved.
- Folder choices live in the shared workspace and are reused by every version.
- The guided wizard skips folder setup when remembered paths are valid.
- Settings provides one `Auto-Detect BeamNG Folders` button and individual `Choose Folder` buttons only for paths that actually need changing.

### Picture-first vehicle/source chooser

- Added a large vehicle gallery using thumbnail cards instead of relying on text dropdowns.
- A selected vehicle shows thumbnail cards for:
  - existing skins;
  - blank UV/texture guides;
  - generated body-variant UVs.
- Double-clicking a picture opens it in the editor.
- The picture browser opens automatically after a ZIP/folder/full scan by default.
- Transparent and DDS-capable sources are converted into cached preview thumbnails where supported.
- Text-only compatibility dropdowns remain hidden for internal project/wizard compatibility.

### Simpler paint/vector editor

- Removed the visible embedded `Vehicle Setup` dropdown block.
- Added large familiar quick tools:
  - Select / Move;
  - Add Image;
  - Paint;
  - Erase;
  - Fill Color;
  - Shapes;
  - Add Text;
  - Pick Color.
- Enlarged and labeled the vertical toolbox.
- Existing independent image/text/shape/paint layers, selected-object transforms, brush presets, Asset Album, Design Vault, named undo history and UV-guide export protection remain.
- The editor remains a hybrid raster/vector-style workspace and does not flatten UV guides into exports.

## Research basis

The corrective layout was checked against official Krita and Inkscape documentation. Krita separates paint, vector, selection, guide and transform tools and provides layers, undo history, brush presets, palettes and mirrored painting. Inkscape uses selectable objects, draggable handles, shape tools, tool controls, transforms, grouping and stacking order. v0.2.3 adopts these understandable interaction patterns without claiming full parity with Krita, Paint.NET, Paint 3D, Inkscape, Forza or professional sign software.

## Automated/static checks passed

- Python compile-all.
- Embedded JavaScript syntax check with Node.
- Backend self-test.
- Asset Album and Design Vault import/list tests.
- BeamNG skin/mod ZIP generation and strict generated JSON/JBeam parsing.
- Shared-master-folder launcher structure test.
- Startup wizard is not forced by default/migration.
- Simple editor quick-tool IDs and unique HTML IDs verified.
- Normal launcher confirmed to contain no `FolderBrowserDialog`.
- Final downloadable ZIP archive integrity test.

## Not proven

- Windows `run.bat` shared-runtime creation and requirement-hash behavior.
- Automatic migration from David's actual prior workspace.
- Steam/BeamNG folder detection on David's exact drive layout.
- Live PySide6/QWebEngine picture-browser interaction.
- Windows DDS thumbnail display.
- Windows drag/drop and clipboard behavior.
- WebGL 3D preview.
- BeamNG in-game detection/rendering of a mod generated by this exact build.

No one may relabel this build as working until David tests this exact archive on Windows and in BeamNG.
