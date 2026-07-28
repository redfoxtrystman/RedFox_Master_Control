# RedFox Skin Studio v0.2.5 — Editor Artifact, Layer, Image Cleanup and 3D Preview Fix

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_5_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `80d36617bac49143b13add12a38aae5185d6649302ee26a314754d514c30193c`

## Owner test findings

David tested v0.2.4a and reported four concrete failures:

1. Moving or editing objects caused large black/checkerboard tile artifacts across the editor surface.
2. Imported RedFox logo artwork could not remove its white background and could not be practically recolored in the built-in editor.
3. Layer locking was not usable enough, and duplicated/mirrored text objects continued moving together instead of acting as independent copies.
4. The live 3D preview loaded the selected helicopter geometry but remained white and did not visibly apply the current skin. The BeamNG model also appeared sideways because of coordinate-system orientation.

These are valid application defects. The artifact behavior shown in screenshots is not part of the skin texture and is not user error.

## Fixes implemented

### QWebEngine/canvas artifact mitigation

- Disabled `QWebEngineSettings.Accelerated2dCanvasEnabled` for the editor view only.
- Kept WebGL available for the separate 3D preview.
- Removed the editor's second manual device-pixel-ratio canvas transform and now uses CSS-pixel backing coordinates, because Qt 6 already handles high-DPI WebEngine scaling.
- Disabled the browser context menu in the embedded editor.

This targets stale accelerated-canvas tile corruption without disabling the 3D preview's WebGL renderer.

### Layer locking and independent copies

- Added a visible lock/unlock button to every layer row.
- Layer lock/unlock is now written into named history.
- Fixed Duplicate and Paste retaining `mirrorLayerId`, `mirrorOf`, `mirrorAxis`, and `hasMirror` metadata.
- Duplicates now move independently and begin unlocked.
- Paint-layer duplicates receive a separate copied canvas instead of sharing the same drawing buffer.
- Mirror Copy now creates an independent mirrored object by default.
- Added a separate explicit Linked Mirror operation.
- Added Unlink controls in the properties panel, layer row, context menu, and desktop action panel.
- A locked mirror partner is no longer changed when the other linked object moves, rotates, scales, or changes properties.

### Basic logo/image editing

Added selected-image controls inside the built-in editor:

- Remove White Background.
- Remove Chosen Color.
- Adjustable removal tolerance with antialias feathering.
- Colorize Logo.
- Clear Tint.
- Convert selected image into a Paint Layer for manual erasing.

The color-removal operation edits only the selected image layer and preserves transparency in PNG/DDS/mod exports.

### 3D preview

- The DAE-to-OBJ stage already filters the preview model when a body/material target is chosen. The viewer no longer performs a second mismatched material-name filter.
- The live exported skin is now assigned to every mesh in the selected/filtered preview OBJ.
- Live reload updates every preview mesh and reports the number updated.
- BeamNG Z-up OBJ geometry is rotated into Three.js Y-up orientation before camera fitting.
- Texture loading failures remain visible in the preview status instead of silently appearing as an untextured white model.

## Research basis

Official Qt documentation states that Accelerated 2D Canvas uses an OpenGL framebuffer and can be disabled per WebEngine view. Qt also documents that high-DPI support is already enabled in Qt 6. The fix therefore disables only accelerated 2D canvas for the editor while leaving WebGL enabled for the separate 3D preview.

## Tests completed

- Python `compileall`: passed.
- Editor JavaScript syntax check with Node: passed.
- Backend self-test: passed.
- Stock Wigeon ZIP scan: passed.
- Wigeon DAE-to-OBJ preview generation: passed; generated OBJ contains texture coordinates and faces.
- New image-control IDs and layer-control code: statically verified.
- Final archive integrity test: passed.

## Not proven

- Artifact correction on David's exact Windows GPU/driver.
- Live lock/unlink/duplicate behavior in QWebEngine on Windows.
- Background removal quality on David's exact RedFox logo.
- Live texture display on the Bell 407 helicopter mod.
- BeamNG runtime rendering of a mod produced by this exact build.

No one may change the status to working until David tests this exact archive.