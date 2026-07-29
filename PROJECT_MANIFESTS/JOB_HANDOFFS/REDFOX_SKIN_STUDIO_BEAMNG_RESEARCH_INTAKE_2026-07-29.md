# RedFox Skin Studio — BeamNG Renderer and Decal Research Intake

**Date:** 2026-07-29  
**Owner:** David / Captain  
**Status:** RESEARCH REVIEWED — IMPLEMENTATION NOT YET BUILT

## Files reviewed

- `BeamNG_Research_REPORT_MANIFESTS.zip`
- `BeamNG_Research_Vehicle_Example_vivace.zip`
- `BeamNG_Research_CarSkin_Decals.zip`
- `BeamNG_Research_Render_Candidates.zip`
- `manifests.zip`

## Main conclusion

The scan did not find a standalone BeamNG renderer that can simply be copied into RedFox Skin Studio. The useful render systems depend on BeamNG engine objects, vehicle objects, camera APIs, RenderViewManager, Lua extensions, UI bridges, and game asset loading.

It did find enough engine-side code to justify a new architecture:

1. Keep RedFox Skin Studio as the external layered editor and project manager.
2. Add a small BeamNG companion extension for exact live in-game preview.
3. Keep Three.js/Blender as fallback previews only.
4. Use BeamNG's own material, paint-slot, UV, mesh-selection and dynamic-decal behavior as references for correct export and preview mapping.

## Strongest renderer candidates

- `lua/ge/extensions/editor/vehicleDetailViewer.lua`
  - Creates fixed side/front/top render views.
  - Uses `RenderViewManagerInstance:getOrCreateView`.
  - Saves render output to disk.
- `lua/ge/extensions/editor/vehicleEditor/liveEditor/veView.lua`
  - Provides a controllable 3D/orthographic vehicle view.
  - Uses `ImguiRenderViewControl` and focus objects.
- `lua/ge/extensions/render/renderViews.lua`
  - Compact reference for creating a RenderView, assigning camera/frustum/resolution and saving to disk.
- `lua/ge/extensions/ui/liveryEditor/editor.lua`
  - Sets the current vehicle skin to `dynamicTextures`.
  - Creates, loads, saves and applies livery sessions.
- `lua/ge/extensions/editor/api/dynamicDecals.lua`
  - Exposes real BeamNG livery functions for decals, fills, paths, brush strokes, layer stacks, mirroring, UV layer, material selection, mesh enable/disable, texture export and skin export.
- `lua/ge/extensions/editor/api/dynamicDecals/textures.lua`
  - Defines the real decal library root as `/art/dynamicDecals/textures` and reads sidecar metadata/categories.
- `lua/ge/extensions/core/vehicle/partmgmt.lua`
  - Skin slot, configuration and vehicle reload behavior.

## Vivace example findings

The stock Vivace bundle includes a complete useful reference:

- `vivace.dae` and `vivace.cdae`
- `skin_uvs.png`
- main and skin material JSON files
- `vivace_skins.jbeam`
- `dynamicDecals/main.jbeam`
- `dynamicDecals/main.materials.json`
- configurations and preview images
- fixed-color, palette/colorable and metallic skin examples

The dynamic-decals material uses runtime texture targets:

- `@DynamicTextureBaseColor`
- `@DynamicTextureColorPalette`
- `@DynamicTextureMetallic`
- `@DynamicTextureRoughness`

The matching JBeam selects `globalSkin: dynamicTextures`. This confirms that exact live preview is intended to run inside BeamNG, not as a portable external renderer.

## Recommended live-preview implementation

Build a RedFox BeamNG companion mod/extension with this flow:

1. RedFox exports the current flattened preview texture and a small state JSON into a shared preview folder.
2. The BeamNG extension detects changes while the game is running.
3. It selects the configured vehicle and applies a dedicated RedFox preview skin or BeamNG `dynamicTextures` workflow.
4. It refreshes the affected material/skin without changing the layered RedFox master project.
5. The bridge reports vehicle, skin, material and error state back to RedFox.
6. RedFox provides fixed camera buttons and an optional BeamNG screenshot/preview feed.

The first implementation should be file-based and local-only for reliability. A socket or HTTP bridge can be considered later.

## Decal bundle findings

The delivered curated decal bundle contains 107 files:

- 48 `Numbers`
- 43 `Shapes`
- 16 `Stripes`

Many are useful reference assets, but several are full atlases, badges, gauges, normal maps, metallic/data maps or license-plate sheets rather than clean standalone livery stamps.

The report says Flames, Damage/Grime and other groups were included, but those directories are not present in the delivered decal ZIP. The actual BeamNG livery decal library was also not extracted. The renderer code identifies its real location as:

`/art/dynamicDecals/textures`

That directory and its `.json` sidecar files should be the target of the next read-only extraction. It is more likely to contain the real Forza-style categorized decal resources used by BeamNG's livery editor.

## Decal integration rule

Do not bundle BeamNG stock artwork directly into a public RedFox release without permission/license review. RedFox should instead:

- index the user's locally installed BeamNG decal library;
- generate thumbnails and categories locally;
- reference/copy assets into a private user workspace only;
- keep original source paths and hashes;
- let users add their own decal packs.

RedFox-owned original stamps remain safe to distribute.

## Next implementation order

1. Build the vehicle-scoped layered skin library and revisions already requested.
2. Build the BeamNG companion live-preview bridge prototype against the supplied Vivace example.
3. Add exact material/UV/mesh targeting based on the dynamic-decals API references.
4. Re-scan `/art/dynamicDecals/textures` with sidecars and thumbnails.
5. Add a local BeamNG decal-library browser without redistributing stock assets.
6. Keep external Three.js/Blender preview marked experimental until the in-game bridge is proven.

No implementation is claimed complete by this intake audit.