# SUPPORT-01 — Regular-Chat Claim and Intake

**Date:** 2026-07-17  
**Regular-chat owner:** Sol (this regular ChatGPT chat), working under David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Feature dependency:** JOB-04 — Scrap Yard / Wrecking Yard  
**GitHub coordination:** Issue #8  
**Status:** CLAIMED — INTAKE AND ARCHITECTURE VERIFICATION; NO RUNTIME BUILD TESTED

## Claim record

The mandatory claim comment was posted to GitHub issue #8 before any SUPPORT-01 repository edit or asset build.

Exact support-lane title:

```text
SUPPORT-01 — Cross-Map 3D Asset Conversion / Prefab / Placement
```

This support lane does not create JOB-13 and does not renumber JOB-00 through JOB-12.

## Required files reviewed

```text
PROJECT_MANIFESTS/SUPPORT_WORKSTREAMS/SUPPORT-01_CROSS_MAP_3D_ASSET_CONVERSION_PREFAB_PLACEMENT.md
PROJECT_MANIFESTS/SUPPORT_WORKSTREAMS/SUPPORT-01_TECHNICAL_ARCHITECTURE_INVESTIGATION_2026-07-17.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_PHYSICAL_YARD_MODEL_AND_BUILD_PLACEMENT_PLAN_2026-07-17.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_PLAYER_OWNED_SCRAP_WRECKING_YARD_EXPANSION_DIRECTIVE_2026-07-17.md
```

## Scope accepted

SUPPORT-01 owns only:

- model-source and license intake;
- conversion into BeamNG-compatible static assets;
- scale, orientation, transforms, UVs, normals, tangents and portable paths;
- materials and textures;
- simplified collision meshes;
- level-of-detail planning and optimization;
- reusable prefab construction;
- developer placement controls;
- placement preview, translation, rotation, confirmation, cancellation, deletion and relocation;
- map-independent placement records;
- save/reload restoration;
- duplicate-load prevention;
- clean disable, uninstall and removal testing;
- SUPPORT-01 reports, hashes, inventories, package records and handoffs.

## Protected ownership boundaries

SUPPORT-01 will not implement or edit ownership of:

- Scrap Yard purchases, sales, business ownership or progression;
- dismantling, parts inventory, crusher payouts or illegal disposal;
- Career money, shared inventory, garage, storage or property systems;
- phone or PC websites;
- Tow / Recovery jobs;
- JOB-04 business backend or WEUI;
- stock or third-party map archives and permanent map content;
- unrelated JOB-00 through JOB-12 implementation files.

JOB-04 remains the Scrap Yard / Wrecking Yard feature and gameplay owner.

## Current truth status

```text
NO THREE-DIMENSIONAL MODEL HAS BEEN APPROVED
NO MODEL ARCHIVE HAS BEEN SUPPLIED TO THIS CHAT
NO MODEL LICENSE OR REDISTRIBUTION PERMISSION HAS BEEN VERIFIED
NO CONVERSION TOOL VERSION HAS BEEN RECORDED
NO PREFAB HAS BEEN RUNTIME TESTED
NO PLACEMENT EXTENSION HAS BEEN RUNTIME TESTED
NO PACKED SUPPORT-01 ZIP HAS BEEN TESTED
NO TWO-MAP RESULT EXISTS
```

The preferred architecture remains provisional: one standalone, removable RedFox asset/placement mod that creates or loads a reusable prefab in the current map without modifying or redistributing the map itself.

## First proof gate

The first candidate must remain limited to:

```text
1 RedFox-authored or clearly redistributable test building
1 material set
1 simplified collision mesh
1 small reusable prefab
1 developer placement control
1 saved placement record
1 reload/restore operation
1 explicit delete/remove operation
1 exact packed ZIP
2-map runtime test by David
```

No business gameplay may be added to this proof.

## Intake record required for every model/archive

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

Paid or restricted source assets must not be committed publicly unless redistribution permission is explicit.

## Tool and version record still required

Before conversion begins, record:

```text
BeamNG.drive version =
Blender version =
Collada/export add-on and version =
Image/material tools and versions =
Source units =
Export units = meters
Axis/orientation settings =
Transform-application settings =
Triangulation settings =
Tangent export settings =
Collision naming/export settings =
LOD naming/export settings =
```

## Verification contract

For the exact packed ZIP, record:

1. ZIP filename, byte size and SHA-256.
2. Complete file inventory.
3. Confirmation that no stock or third-party map files are included or overridden.
4. Asset and material loading result.
5. Scale and orientation result against a BeamNG vehicle.
6. Collision result and collision reload behavior.
7. Placement, rotation and deletion result.
8. Placement save/reload and duplicate-load result.
9. Second-map result from the same ZIP.
10. Disable/uninstall and clean-removal result.
11. Log output and performance observations.

Until David tests the exact packed ZIP on at least two maps, the only permitted candidate status is:

```text
BUILT — RUNTIME UNTESTED
```

The words universal, all-map, working, safe, complete and final are prohibited before that test passes.

## Immediate dependencies

- First candidate model/archive or approval to use a RedFox-authored primitive test building.
- Exact source and license evidence for any third-party model.
- Confirmation of David's available Blender/export toolchain and BeamNG version.
- Two maps selected for runtime testing.
- JOB-00 approval of the final runtime path and placement contract after the minimal proof.
- JOB-04 supplies only future footprint and relative marker requirements; it does not transfer gameplay ownership.
