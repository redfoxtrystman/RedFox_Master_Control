# SUPPORT-01 — Cross-Map Prefab Placement Architecture Investigation

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Support lane:** SUPPORT-01 — Cross-Map 3D Asset Conversion / Prefab / Placement  
**Status:** PROVISIONAL ARCHITECTURE — MINIMAL RUNTIME PROOF REQUIRED

## Owner question

David found promising Scrap/Wrecking Yard models and asked whether the models must be injected into every map or whether they can be delivered through one installed mod so users can place/use the yard on multiple maps.

## Current conclusion

The preferred design is a standalone asset/placement mod. Permanent edits to every map should not be the default.

BeamNG officially supports:

- `TSStatic` as the main class for individually placed buildings and static props;
- reusable Prefab objects that load groups of static objects from `.prefab` or `.prefab.json` files;
- prefabs that can be loaded or unloaded while a level is running;
- mod ZIPs containing top-level `art`, `lua`, `ui`, and other content domains when packed correctly.

This makes the following architecture plausible:

```text
One installed RedFox asset/placement mod
-> carries unique yard meshes, materials and prefab files
-> loads one reusable yard prefab into the current level scene
-> player selects position/rotation on a suitable flat area
-> mod saves placement data outside the original map archive
-> mod recreates the prefab when that map/profile loads again
```

The official documentation proves the scene-object, prefab, static-mesh and package capabilities. It does not fully document the exact Lua runtime creation function needed for this RedFox workflow. Therefore the architecture remains provisional until a minimal two-map runtime proof is built and David tests it.

## Why permanent map injection is rejected for Phase 1

Do not begin by modifying every map's:

```text
levels/<map>/main/items.level.json
map ZIP
terrain files
original prefab files
```

That approach creates problems:

- every official and third-party map needs a separate patch;
- map updates may overwrite or conflict with changes;
- redistribution of altered maps is unacceptable;
- users have different map collections;
- uninstalling becomes difficult;
- duplicate map files can break loading or tests;
- other mod creators cannot easily support the feature.

## Intended package concept

Candidate package name:

```text
RedFox_CrossMap_Yard_Assets_Placement_v0_1_0
```

Candidate domains:

```text
art/redfox_scrapyard/models/
art/redfox_scrapyard/textures/
art/redfox_scrapyard/materials/
art/redfox_scrapyard/prefabs/
lua/ge/extensions/redfox/
ui/... only if a placement UI is needed
```

Exact paths must be proven from the packed ZIP. The BeamNG asset system changed in version 0.37 and official shared static meshes are moving toward a central assets structure, so SUPPORT-01 must not assume an untested path convention.

## Prefab design

The full yard should be one reusable Prefab containing relative child transforms.

Possible child objects:

- office/shop building;
- fence segments and gates;
- yard sign;
- static vehicle stacks;
- scrap piles and bins;
- crusher pad or crusher visual;
- lights;
- loading area markers;
- tow entrance/drop-zone markers;
- future work-zone markers.

Use `TSStatic` for the building and large unique props. Use simplified repeated decorative objects for background stacks. Do not use dozens of active BeamNG vehicles merely as scenery.

## Placement-state concept

The first implementation should save only scenery placement data:

```json
{
  "schemaVersion": 1,
  "placements": [
    {
      "placementId": "unique-id",
      "mapId": "current-level-id",
      "prefabId": "redfox_scrapyard_visual_yard_v0_1",
      "prefabVersion": "0.1.0",
      "position": [0, 0, 0],
      "rotation": [0, 0, 0, 1],
      "scale": [1, 1, 1],
      "createdAt": "timestamp",
      "enabled": true
    }
  ]
}
```

This is a proposed support-owned placement record only. It is not the JOB-04 player-owned business record and must not contain money, ownership, inventory, parts, crusher payouts or illegal-state data.

## Placement validation

Before confirming placement, inspect where possible:

- terrain/ground hit exists;
- slope is within a configurable limit;
- required footprint is reasonably clear;
- no obvious overlap with roads, buildings, water or spawn points;
- entrance is reachable;
- prefab bounds fit;
- height is adjusted to prevent floating or burial.

Do not claim automatic perfect flat-site discovery on every custom map. Manual preview and adjustment should remain available.

## First proof

Phase 0 test package:

```text
1 simple building
1 material set
1 collision mesh
1 small prefab
1 placement control
1 save record
1 reload restore
1 delete operation
```

Test on:

```text
1 official map
1 second official or third-party map
```

Success requires:

- no original map files modified;
- asset loads from a packed ZIP;
- materials and collision work;
- prefab places, moves, rotates and deletes;
- placement survives reload;
- second map placement works from the same ZIP;
- clean uninstall does not damage either map;
- logs identify the map, prefab, transform and failure reason.

## Possible fallback

If runtime prefab creation proves unavailable or unsafe, the fallback order is:

1. use a supported World Editor extension/tool that places the RedFox prefab without bundling map files;
2. export/import a small user placement record per map;
3. create an optional adapter for a specific map only when unavoidable;
4. never redistribute a complete modified map merely to add the yard.

## Official references checked

```text
https://documentation.beamng.com/modding/levels/level_classes/prefab/
https://documentation.beamng.com/modding/levels/level_formats/prefab/
https://documentation.beamng.com/modding/levels/level_classes/tsstatic/
https://documentation.beamng.com/world_editor/tools/prefabs/
https://documentation.beamng.com/modding/mod-support/mod_packing/
https://documentation.beamng.com/modding/levels/level_creation/section5/
https://documentation.beamng.com/modding/levels/assets/
```
