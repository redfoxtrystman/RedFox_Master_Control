# RedFox Skin Studio v0.2.4 — External Editors and Live 3D Preview Audit

**Date:** 2026-07-23  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_4_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `5e4cf0fa8e712cb1b4a0774088b2449449d1e3f57a49fa1d8f9a76021a78574e`

## Owner request

David asked that the current built-in editor be preserved, but that RedFox Skin Studio stop depending on it for advanced image-editing parity. The app must open the current skin in installed external editors such as Krita, Paint.NET, Paint 3D and other available editors, then bring saved changes back into RedFox. David also requested a live movable 3D vehicle view, preferably similar to the game, plus the ability to open the vehicle and live skin in Blender.

## Implemented in v0.2.4

### External image-editor round trip

- Detects and offers buttons for:
  - Krita;
  - Paint.NET;
  - Microsoft Paint;
  - legacy Paint 3D when installed;
  - GIMP.
- Adds `Open in Another Installed Editor` for any selected Windows editor executable.
- Exports the current visible skin to a shared PNG using the existing grid-excluding final-flatten path.
- Stores round-trip files under the shared `External_Edit` workspace folder.
- Uses a Windows/Qt file watcher to detect external saves.
- Delays reload briefly because many editors replace the file during save.
- Automatically reloads the saved PNG into RedFox as one external raster result layer.
- Hides but does not delete the original editable RedFox layers.
- Adds `Return to Editable Layers` to hide the external raster result and restore the original object/layer visibility.
- Adds manual `Reload Saved External File` as a fallback.

### Live built-in 3D preview

- Replaces the blocking one-shot preview dialog with a non-modal preview window.
- The user can keep editing while the preview remains open.
- Editor history changes notify the desktop host.
- Completed edits are debounced before exporting a replacement preview PNG.
- The Three.js preview exposes a live texture-reload function and refreshes the texture without closing/reopening the window.
- Automatic preview exports occur only while the preview window is visible or a launched Blender process remains active.

### Blender live preview

- Detects Blender from PATH and common Windows installation folders; also allows manual executable selection.
- Uses RedFox's generated preview OBJ instead of relying on Blender's legacy COLLADA importer.
- Exports a shared live PNG.
- Generates a Blender Python helper script in the shared workspace.
- The script imports the OBJ, builds a material, assigns the live PNG to the meshes, saves a reusable `.blend` file and registers a timer that reloads the image when its modification time changes.
- RedFox checks the launched Blender process and stops automatic Blender texture exports when Blender closes.

## Preserved behavior

- Existing built-in editor and projects remain available.
- UV/base guide layers remain excluded from exported PNG/DDS textures.
- Existing asset album, design vault, selected-object transforms, history, project/mod building, ZIP injection and backups are retained.
- External-editor work does not overwrite the `.rfskin` project unless the owner explicitly saves the skin to the project.

## Technical limitations recorded honestly

- A universal PNG cannot preserve RedFox's independent layer/object structure in Krita, Paint.NET, Paint, Paint 3D or GIMP. Externally saved changes return as one flattened raster layer, while original RedFox layers remain recoverable.
- Paint 3D was retired by Microsoft. Existing installations are detected on a best-effort basis, but direct file activation is unreliable on some Windows builds and may only open the app.
- The built-in and Blender previews are approximate. They do not reproduce every BeamNG UV1/material/shader/custom-part behavior, damage or deformation.
- This build does not inject a texture live into a running BeamNG session. BeamNG remains the final runtime test after building the mod.

## Static/backend verification passed

- Python compile-all.
- Web editor JavaScript syntax validation with Node.
- Existing backend self-test.
- Blender helper script Python syntax compilation.
- External editor detection executes without error on the build host.
- Static assertions for external-editor UI/actions, file watching, external result restore API, document-change signal, live preview update path and Blender launch path.
- Final ZIP archive integrity test.

## Not proven

- Windows external app launching for David's exact installed versions.
- Paint 3D direct file opening.
- Windows save-event behavior for every editor.
- PySide6 live GUI operation.
- WebGL live texture refresh.
- Blender startup, OBJ import and image reload on David's machine.
- BeamNG in-game loading/rendering.

No one may relabel this build as working until David tests this exact archive.
