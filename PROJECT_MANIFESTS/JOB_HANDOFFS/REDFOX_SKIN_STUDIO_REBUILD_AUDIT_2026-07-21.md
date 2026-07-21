# RedFox Skin Studio — Rebuild Audit and Owner Directive

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Status:** PARTIAL — v0.1.0 exists, but the owner reports that the core workflow is not reliable or understandable enough for use.

## Why this audit exists

David asked for one BeamNG skin-making application that combines the useful parts of the supplied livery/skin tools and image editors. The first RedFox Skin Studio beta was presented as more complete than it actually was. David reports that it does not reliably load skins for editing, does not clearly or reliably create the intended BeamNG mod, and its editor workflow is confusing. The first beta therefore does **not** satisfy the request and must not be represented as finished or working.

The owner explicitly instructed that this failure be documented honestly, including that the initial application was half-finished/half-assed relative to the promised scope, and that future work must follow an inspect-design-build-test-audit order instead of claiming completion early.

## Owner requirements for the rebuild

The replacement is a portable-first Windows desktop application combining:

1. A Forza-style object/layer livery editor.
2. Raster painting tools similar in purpose to Paint.NET/Krita.
3. Vector/sign-program behavior for editable decals, text, shapes, groups, and transformations.
4. A guided beginner wizard plus a direct advanced workspace.
5. A movable 3D vehicle preview that updates from the active skin.
6. BeamNG vehicle/mod discovery from configured game, user, and mod-storage folders.
7. Correct BeamNG skin and mod creation, including colorable RGB/palette-map workflows.
8. Safe creation, reading, editing, backing up, and rebuilding of mod ZIP files.
9. Named projects containing many skins and multiple versions.
10. Ability to add skins to an existing third-party vehicle or skin-pack ZIP, with safer companion-pack mode available.

## Mandatory editing behavior

Every imported image, decal, text item, stripe, number, shape, dirt/mud mark, brush stroke group, or vector element must be an independently selectable object or layer where appropriate.

Selected-object operations must include:

- move
- rotate
- uniform scale
- independent horizontal/vertical stretch
- skew/distort
- horizontal flip
- vertical flip
- duplicate
- group/ungroup
- recolor/tint
- opacity
- layer order
- locking/hiding
- snapping/alignment
- copy to opposite vehicle side
- linked or unlinked left/right mirroring

Whole-texture flip is not an acceptable substitute for selected-object transforms.

Text and logos copied to the opposite side must support readable mirroring rules rather than automatically becoming backward. Vehicle profiles must store side-to-side mapping/orientation data when automatic UV correspondence is not sufficient.

## Decal and design library

The application needs a built-in, extensible library including at minimum:

- geometric primitives
- gradients
- stripes and pinstripes
- numbers and letters
- racing icons
- flames
- tears/claw marks
- paint splatters
- hazard chevrons
- police/fire/rescue/utility layouts
- mud, grime, dust, rust, scratches, rivets, seams, and wear overlays
- user-imported PNG/JPEG/JPG/WebP/BMP/TIFF/GIF-static/SVG assets

Raster formats must be converted internally as needed. Vector assets must remain vector-editable where practical and be rasterized only for final texture output.

## Paint workspace

The raster editor must include practical built-in skin painting tools:

- brush presets with size, opacity, hardness, spacing, and stabilization controls
- pencil/pixel brush
- soft/hard round brushes
- airbrush/marker/texture brushes
- eraser
- fill bucket
- gradients
- lines and shapes
- rectangular/lasso selections
- color picker
- blur/smudge/clone where technically stable
- layers, masks, blend modes, undo/redo, and non-destructive editing where practical

## BeamNG and 3D requirements

The setup wizard must store paths for:

- BeamNG installation
- BeamNG user folder
- active mods folder
- one or more external mod-storage folders
- RedFox Skin Studio workspace folder

The indexer must inspect vehicle `.dae` models, JBeam/configuration data, materials JSON, textures, UV/template images, and skins from unpacked folders and ZIP mods. When a template image does not exist, the system should attempt to derive a UV guide from model UV data. Unusual mods need a manual mapping wizard rather than an endless queue or silent failure.

The 3D preview target includes orbit, zoom, pan, panel/part visibility, wireframe/UV view, multiple lighting presets, paint-color testing, and live refresh. It is an editing preview and must not be claimed to reproduce every BeamNG shader, deformation, damage effect, or custom mod material exactly.

## BeamNG export and ZIP safety

The application must support:

- create a new single-skin mod
- create a multi-skin pack for one vehicle
- create a multi-vehicle skin pack
- add a skin to an existing mod ZIP
- clone/edit an existing skin from a ZIP
- create a companion skin-pack ZIP without altering the source mod
- patch an existing ZIP only after explicit confirmation

Before any in-place ZIP patch, the original ZIP must be backed up externally. Replaced files must also be retained in project version history. Internal backup copies may be stored under a non-runtime RedFox backup namespace, but active duplicate paths must never be introduced in a way that confuses BeamNG.

The project database must record source ZIP, file hashes, changed paths, output ZIP, skin IDs, material names, vehicle IDs, backup locations, and version history. ZIP writes must use a rebuild-to-temporary-file then atomic replace strategy; direct destructive mutation is not acceptable.

## Project and storage model

RedFox Skin Studio is portable-first and must allow its workspace to live on a non-C drive. Projects, indexes, caches, previews, temporary builds, exports, backups, logs, and decal libraries must use the selected workspace.

Named projects may contain many versions and many skins, for example one D-Series project containing numerous D-Series skins, a separate Autobello project, or a project that injects/companions skins for a firetruck mod.

Required maintenance tools:

- move workspace
- clean cache
- clean temporary builds
- locate previous install/workspace
- remove previous install-owned files
- preserve/migrate projects
- repair/reset without deleting projects

## Wizard workflow

Beginner wizard order:

1. Select/verify folders and workspace.
2. Choose new project or existing project.
3. Choose stock/modded vehicle or existing ZIP.
4. Choose blank skin, clone existing skin, or add skin.
5. Verify vehicle model/material/UV mapping.
6. Choose fixed-color or three-color BeamNG palette workflow.
7. Edit with decals, paint, text, layers, mirroring, and optional generators.
8. Preview in 3D and run validation.
9. Choose new mod, add to project pack, companion ZIP, or explicit source-ZIP patch.
10. Build to a temporary location, validate contents, create backups, then publish output.

No output may be labeled working until David tests the exact build.

## Research direction recorded

The rebuild is intentionally modeled after:

- Forza's per-side, per-layer vinyl workflow, vinyl groups, text, material/gloss controls, lighting options, uniform scale, and independent stretch.
- Professional vector/sign-editor concepts: raster and vector objects in one document, object handles, precise transform panels, duplicates, groups, layers, alignment, snapping, mirroring, stretching, skewing, and nondestructive effects.
- BeamNG's own material/skin/vehicle formats and its general decal concepts, adapted for vehicle texture generation rather than level decal placement.

## Current implementation status

- The supplied v0.1.0 package has been preserved for inspection only.
- Its backend self-test can generate a basic ZIP containing JBeam, materials JSON, and DDS, but that narrow test does not prove the reported GUI workflow, mod loading, skin editing, third-party ZIP injection, 3D preview, wizard, or game runtime.
- v0.1.0 includes partial canvas/layer/shape/paint code, but it is not the required complete editor architecture.
- No v0.2 build is yet approved as complete.
- Next release status must remain **BUILT — RUNTIME UNTESTED** until David tests it, and only after required automated and manual workflow tests pass.

## Required order of operations for v0.2

1. Inventory and test all supplied applications and source packages.
2. Freeze a written architecture and file format.
3. Build project/workspace and ZIP transaction layers first.
4. Build vehicle indexing/import and diagnostic reporting.
5. Build the object/layer transform editor.
6. Build raster paint tools and decal library.
7. Build wizard and accessibility/help flow.
8. Build BeamNG material/palette exporters.
9. Build 3D preview and vehicle profile/mirroring system.
10. Run automated tests, fixture tests, destructive ZIP safety tests, and packaged Windows smoke tests.
11. Publish only with verification reports and an honest runtime status.

## Audit rule

Every significant implementation change, test result, failure, format decision, and release candidate must be added to this file or a dated successor handoff so all project chats can see the actual status. Claims must distinguish static tests from David-tested BeamNG runtime.