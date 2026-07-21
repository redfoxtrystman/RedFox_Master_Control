# RedFox Skin Studio 0.2.0

**Status: BUILT — RUNTIME UNTESTED**

RedFox Skin Studio is a portable Windows-first BeamNG livery, decal, paint, project, and mod-pack editor. Version 0.2.0 replaces the unreliable one-skin export path from 0.1.0 with a project system and an exporter based on the vehicle's scanned material definitions.

## What 0.2.0 does

- Guided beginner wizard or direct advanced workflow.
- Named projects that can contain many skins and more than one vehicle.
- Scan stock vehicle ZIPs, third-party vehicle/mod ZIPs, extracted mod folders, configured BeamNG folders, and extra mod-storage folders.
- Load supplied UV templates or generate UV candidates from DAE geometry when a mod does not provide one.
- Open a UV as a non-exporting guide, or open an existing skin texture as editable artwork.
- Import common raster/vector image formats and DDS, then convert final output into BeamNG-ready texture files.
- Independent decal/layer transforms: move, resize, stretch, rotate, duplicate, horizontal/vertical flip, and mirrored copy. These actions affect the selected object rather than the whole skin.
- Text, vector paths/shapes, gradients, imported logos, and raster paint layers.
- Brush presets: hard round, soft airbrush, marker, spray paint, splatter/mud, and square/pixel.
- Preset generators for random liveries, generic police/emergency layouts, mud/grime, and racing numbers.
- Fixed-color skins and three-channel RGB colorable-mask skins.
- Save editable `.rfskin` projects and reopen them later.
- Build one BeamNG mod ZIP containing all skins in the selected project.
- Add/project-inject skins into an existing ZIP while preserving the original externally and backing up overwritten files inside `.redfox_backup/`.
- Analyze broken/existing skin ZIPs for invalid JBeam/material JSON and missing referenced textures.
- Approximate movable 3D preview using the selected BeamNG DAE converted to a cached OBJ, with orbit, zoom, lighting, and wireframe controls.
- Portable workspace and cache location, plus cache cleanup and previous-install cleanup.

## Install and run

The downloadable source package includes `install.bat`, `run.bat`, all editor files, templates, and vendored offline 3D dependencies. Extract it to the drive where the app should live, run `install.bat` once, then run `run.bat`.

The workspace defaults to `Workspace` beside the application. Use Settings to move projects, vehicle indexes, UV maps, preview caches, backups, logs, and builds to another drive.

## Why 0.1.0 produced NO TEXTURE

The three supplied 0.1.0 output ZIPs had two exporter defects:

- their JBeam files were malformed JSON because a comma was missing;
- their material files referenced texture names that did not exist in the ZIP.

Version 0.2.0 writes strict JSON/JBeam, derives replacement materials from the scanned vehicle, uses matching packaged texture names, and runs a static reference validator before producing a ZIP.

## Important limitations

- Windows and BeamNG runtime are not yet tested by David.
- The 3D preview is approximate and does not reproduce every BeamNG shader or third-party material.
- Direct brush projection onto the 3D model is not implemented; editing occurs on the 2D texture and the 3D window previews it.
- Full Forza feature parity is not claimed.

See the dated build handoff under `PROJECT_MANIFESTS/JOB_HANDOFFS/` for exact validation evidence and SHA-256.
