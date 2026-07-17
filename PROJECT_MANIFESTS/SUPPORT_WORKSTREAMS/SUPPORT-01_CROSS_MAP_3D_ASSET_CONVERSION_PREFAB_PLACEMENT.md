# SUPPORT-01 — Cross-Map 3D Asset Conversion / Prefab / Placement

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Primary feature dependency:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** NEW SUPPORT LANE — UNCLAIMED UNTIL A DEDICATED CHAT ACCEPTS IT

## Why this is a support lane instead of JOB-13

The official FoxNet rebuild remains JOB-00 through JOB-12. This support lane does not renumber or replace any official job. It exists because cross-map model conversion, material setup, collision, prefab construction, placement, and save/reload are specialized work that should not consume JOB-04's gameplay/backend scope.

## Exact title to use

```text
SUPPORT-01 — Cross-Map 3D Asset Conversion / Prefab / Placement
```

Any dedicated chat accepting this lane must use the full title above in every claim, audit, status report, commit, issue comment, package report, and handoff.

## Scope owned by SUPPORT-01

SUPPORT-01 owns only:

- license and redistribution verification for candidate 3D models;
- source-model intake and inventory;
- conversion into BeamNG-compatible static-mesh formats;
- real-world scale, orientation, pivots, transforms, normals, tangents, UVs, textures, and material definitions;
- low-cost collision meshes;
- level-of-detail planning and performance optimization;
- modular yard components;
- reusable prefab construction;
- runtime or development placement controls;
- placement preview, translate, rotate, confirm, cancel, delete, relocate, and reload behavior;
- map-independent placement records;
- save/reload restoration of placed prefabs;
- clean removal and uninstall behavior;
- SUPPORT-01-specific reports, source notes, hashes, file inventories, and test packages.

## Scope not owned by SUPPORT-01

SUPPORT-01 does not own:

- Scrap Yard purchases, sales, dismantling, crusher economy, parts inventory, illegal disposal, yard ownership, or business progression;
- JOB-04 — Scrap Yard / Wrecking Yard backend or website;
- JOB-01 — Phone + PC Platform Core;
- JOB-02 — Shared RLS / Career Bridge;
- JOB-09 — Tow / Recovery / Dispatch;
- JOB-10 — Visual Design / Real Website Polish;
- JOB-11 — QA / Logging / Failure Triage;
- shared property, money, inventory, garage, storage, or save systems;
- direct permanent edits to every supported map;
- redistribution of models, textures, or source files without permission.

JOB-04 remains the feature owner. SUPPORT-01 delivers a placement/asset service and prefab package that JOB-04 may consume after JOB-00 approves the contract.

## Technical direction

The preferred architecture is one standalone RedFox asset/placement mod rather than a separate edited copy of every map.

Candidate package domains:

```text
art/redfox_scrapyard/...
lua/ge/extensions/redfox/... or another approved unique SUPPORT-01 path
ui/... only when a dedicated placement UI is required
settings/... or an approved Career/profile data path for placement records
```

Exact runtime paths are not frozen until a minimal BeamNG test proves which path works from a packed ZIP on at least two maps.

The asset package should contain:

- unique RedFox-owned or properly licensed static meshes;
- textures and material JSON files;
- dedicated collision meshes;
- one or more reusable yard prefabs;
- optional component prefabs for office, fence, gate, crusher area, vehicle stacks, scrap piles, loading area, lights, signs, and barriers;
- a minimal placement extension or developer tool;
- placement-state serialization;
- verification and removal reports.

## Reusable prefab target

Use a reusable Prefab object/group for the complete yard assembly. Use TSStatic objects for individual buildings and large props. Decorative repeated objects should use low-cost static representations where practical.

First prefab target:

```text
redfox_scrapyard_visual_yard_v0_1
```

Initial contents should be scenery only:

- office/shop building;
- perimeter fence and gates;
- sign;
- static junk-car stacks;
- scrap piles/bins;
- crusher pad or visual crusher placeholder;
- loading and truck maneuvering area;
- simple lights and markers where safe.

No business mechanics, payouts, dismantling, vehicle deletion, inventory mutation, or illegal gameplay may be included in the first placement proof.

## Cross-map placement goal

The intended player flow is:

```text
Load any supported map
-> open developer placement tool
-> select a yard prefab
-> preview at current position or cursor/ground hit
-> rotate and adjust height
-> run flatness/clearance checks
-> confirm placement
-> save map ID + prefab ID + position + rotation + version
-> reload the map/session
-> restore the same prefab without editing the original map files
```

A map may still be incompatible when it lacks enough flat/clear terrain or when its scene/terrain data prevents safe placement. The tool must report that honestly rather than forcing placement.

## Do not inject permanent files into each map for Phase 1

Phase 1 must avoid modifying every map's `items.level.json`, map ZIP, or shipped level content.

Reasons:

- map updates could overwrite or conflict with changes;
- third-party maps vary widely;
- users may not own the same map set;
- redistributing modified maps is not acceptable;
- map-specific patches would be hard to maintain and uninstall;
- duplicate map files can invalidate testing.

A map-specific compatibility adapter may be added later only when runtime placement cannot work on that map and JOB-00 approves the exception.

## Model intake requirements

For every candidate model, record:

```text
Model name =
Source URL/store/creator =
License =
Commercial use allowed = yes/no/unknown
Game-mod redistribution allowed = yes/no/unknown
Modification/conversion allowed = yes/no/unknown
Attribution required =
Original file format =
Original archive filename =
Archive byte size =
SHA-256 =
Texture files =
Polygon/triangle counts =
Known LODs =
Known collision =
Known animations =
Decision = approved / private test only / rejected / clarification required
```

Do not commit purchased or restricted model files to public GitHub. GitHub may store only license notes, hashes, conversion instructions, screenshots permitted by the license, and RedFox-authored source unless redistribution rights are clear.

## Model conversion requirements

- use meters and verify dimensions against a BeamNG vehicle;
- apply transforms before export;
- triangulate where required;
- export tangents when normal maps are used;
- correct flipped normals and non-manifold geometry;
- use portable texture paths;
- create simplified dedicated collision meshes;
- avoid visible-mesh collision except for temporary debugging;
- create useful LODs for buildings and large props;
- keep decorative junk stacks low cost;
- avoid dozens of fully simulated parked vehicles as scenery;
- preserve an editable authoring source outside the release ZIP;
- include exact conversion-tool versions and settings.

## Minimum proof package

The first SUPPORT-01 package must contain only enough to prove the architecture:

```text
1 simple licensed/test building mesh
1 material set
1 simple collision mesh
1 small prefab containing that building and a few props
1 developer placement command or WEUI
1 placement save record
1 map/session reload restore path
1 delete/remove path
required reports
```

Required tests:

1. ZIP installs without altering a stock map archive.
2. Asset appears with correct materials.
3. Collision is present and inexpensive.
4. Prefab can be placed on one official map.
5. Placement can be rotated and deleted.
6. Placement survives session/map reload.
7. Same package can place the prefab on a second map.
8. Uninstall/removal does not damage either map.
9. Missing/incompatible-map conditions produce clear errors.
10. Performance impact is recorded.

## Dependencies

- JOB-00 — Coordinator / Integration / Verification approves boundaries and final integration.
- JOB-04 — Scrap Yard / Wrecking Yard supplies yard requirements and later consumes the placed-yard record.
- JOB-02 — Shared RLS / Career Bridge is required only when business/property records begin; it is not needed for the scenery-only proof.
- JOB-09 — Tow / Recovery / Dispatch later consumes yard destination/entrance/drop-zone data.
- JOB-10 — Visual Design / Real Website Polish may supply logos/signage direction but does not own model runtime conversion.
- JOB-11 — QA / Logging / Failure Triage validates exact packages after a candidate exists.

## Required handoff from SUPPORT-01 to JOB-04

```text
Prefab ID and version =
Supported asset paths =
Placement API/command =
Placement-state schema =
Map ID behavior =
World transform format =
Flatness/clearance result format =
Yard entrance position =
Tow drop-zone position =
Crusher/work-zone positions =
Delete/relocate operations =
Load/unload lifecycle =
Logs and prefixes =
Known limitations =
Exact ZIP filename, byte size and SHA-256 =
David runtime result =
```

## Status language

Until David tests the exact package:

```text
BUILT — RUNTIME UNTESTED
```

No support chat may call placement universal, all-map, working, safe, complete, or final based only on a World Editor demonstration or static inspection.
