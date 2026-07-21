# RedFox Skin Studio v0.2.0 — Build Handoff

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Status:** **BUILT — RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_0_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `ef9f5e550aa819303e97613b820f887b74662f077e42c4ce3adcb9d0d03238e1`

## Owner request and v0.1 failure

David requested a Forza/sign-vinyl style BeamNG skin studio with independent decal objects, raster painting, a guided wizard, named multi-skin projects, RGB colorable skins, vehicle/mod scanning, safe ZIP injection/backups, and a movable 3D vehicle preview.

The first v0.1.0 package was described as more complete than testing justified. David's three generated mods showed NO TEXTURE. Inspection confirmed that the v0.1 exporter generated malformed JBeam and material references whose texture names did not match the files actually stored in each ZIP. This was an application failure, not user error.

## Implemented in v0.2.0

- Portable workspace selectable outside the C drive.
- Named projects with multiple skins and multiple vehicles.
- Stock/mod ZIP and extracted-folder scanner with no queue.
- Configured BeamNG install/user/mod-storage folder indexing.
- Vehicle material and paint-slot selection.
- UV-template extraction and DAE UV-candidate generation.
- Independent layer/decal flip, rotate, mirror, duplicate, move, resize, and stretch.
- Image, text, vector/shape, gradient, and raster paint layers.
- Hard round, soft airbrush, marker, spray, splatter/mud, and pixel/square brushes.
- Random-livery, police/emergency, mud/grime, and racing-number presets.
- Editable `.rfskin` project save/reopen.
- Fixed-color and three-channel RGB colorable modes.
- Strict JSON/JBeam writer and generated-texture reference validator.
- Multi-skin project ZIP builder.
- Existing-ZIP injection with external original backup, internal `.redfox_backup`, and `.redfox_manifest` history.
- Broken/existing ZIP diagnostics.
- Approximate DAE-to-OBJ 3D preview with orbit, zoom, lighting, and wireframe.
- Guided wizard, cache cleanup, and previous-install cleanup.

## Uploaded fixtures inspected

### Stock Wigeon

- 4 UV maps detected.
- 2 DAE models detected.
- 6 likely body/material targets detected.
- `paint_design` slot detected.
- Highest scoring body target: `wigeon`, score 285.

### Modded Jerrdan

- Vehicle roots `jerrdan` and `spreaderbar` detected.
- Jerrdan: 30 DAE-generated UV candidates, 29 DAE files, 7 likely materials.
- 11 custom paint slots detected for cab, boom, underlift, outriggers, subframe, and related parts.
- No single obvious finished UV-template image was supplied; exact target/UV choice requires in-game verification.

### Known-good `retro_pickup.zip`

- Diagnostic returned zero errors.

### Broken v0.1 outputs

All three supplied output ZIPs contained invalid JBeam and/or references to texture filenames that were not present. The v0.2 diagnostics detected these failures.

## Automated/static tests passed

- Python compile-all.
- Editor JavaScript syntax check.
- Backend self-test.
- Wigeon and Jerrdan source scanning.
- Two-skin Wigeon project build: one fixed, one RGB colorable.
- Strict parse of generated materials JSON and JBeam.
- Generated texture-reference existence validation.
- Existing-ZIP injection, repeated injection, external backups, internal backups, and edit manifests.
- Known-good and broken-ZIP diagnostics.
- Wigeon DAE conversion to a 13,391,306-byte cached OBJ.
- Qt offscreen MainWindow smoke test.
- Editor serialization/reload round trip.
- Final ZIP archive integrity test.

## Not proven

- Windows installation/runtime.
- Windows WebGL/GPU preview.
- BeamNG in-game loading/rendering of the exact generated ZIP.
- Exact best Jerrdan material/paint-slot/UV candidate.
- Full Forza feature parity or direct brush projection on the 3D vehicle.

No one may change the status to working until David tests this exact package in BeamNG.

## Repository record

The source overview and release notes are under `TOOLS/REDFOX_SKIN_STUDIO_V0_2_0/`. The downloadable artifact supplied to David contains the complete source tree, inherited web editor, templates, and offline 3D dependencies. The binary ZIP itself was not committed through the text-only GitHub connector.
