# JOB-04 — Scrap Yard / Wrecking Yard — Physical Yard Model and Build/Placement Plan

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Feature owner:** JOB-04 — Scrap Yard / Wrecking Yard  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** OWNER-APPROVED DESIGN DIRECTION — IMPLEMENT AFTER BACKEND PROOF

## Core idea

David intends to obtain or create one or more three-dimensional Scrap Yard / Wrecking Yard model sets. The project may inspect a BeamNG mod that can build/place a house, then either:

- adapt its mechanism when licensing and compatibility permit; or
- create a RedFox-owned placement/build system based on independently understood behavior.

The first physical yard may initially be visual scenery only: a realistic building, fences, gates, stacked cars, equipment areas and props placed on a flat location on any map. The business backend can be connected later.

## Immediate restriction

Do not begin physical-yard implementation until JOB-04 — Scrap Yard / Wrecking Yard proves the current backend through its WEUI test harness.

The first priority remains:

```text
Real shopping data
Real purchase-menu entry
Real owned-vehicle list
Real inventory sale
All-map behavior
Shared WEUI/phone/PC backend
```

## Phase 1 — Model intake

For every candidate model or model pack, record:

```text
Model/file name
Creator/source
License and reuse permission
Whether modification is allowed
Whether redistribution inside a BeamNG mod is allowed
File formats
Texture formats
Approximate polygon count
Available LODs
Collision meshes
Material count
Texture resolution
Model scale
Origin/pivot behavior
Separate or combined components
Known performance concerns
```

Do not use a model merely because it looks good. Confirm the right to edit and redistribute it.

## Phase 2 — Modular yard kit

Prefer modular components instead of one giant fixed scene.

Suggested components:

- office/shop building;
- service bays;
- scale house;
- perimeter fencing;
- gates;
- sign structures;
- car stacks;
- loose vehicle rows;
- crusher shell/area;
- dismantling pad;
- parts-storage racks;
- scrap piles;
- crushed-bale stacks;
- loading area;
- truck turnaround;
- employee/customer parking;
- tow drop-off zone;
- legal intake area;
- optional hidden/illegal intake area;
- lighting and security props;
- containers and storage sheds.

Modularity allows small, medium and large yard layouts and avoids requiring every map to provide the same footprint.

## Phase 3 — Placement-system research

Inspect the supplied house-building/placement mod for:

- licensing and redistribution permission;
- how the player enters placement mode;
- preview/ghost placement;
- position and rotation controls;
- snapping;
- terrain/flatness validation;
- collision checks;
- object-group creation;
- save format;
- load timing;
- map/session handling;
- object removal;
- relocation;
- multiplayer assumptions if any;
- stock files overridden;
- startup extensions;
- performance and cleanup behavior.

Do not copy its code before confirming permission. If the mechanism is unsuitable, document the useful behavior and build a separate RedFox-owned system.

## Phase 4 — Visual-only placement proof

The first working target should be small:

1. Open a development placement panel.
2. Select one yard layout.
3. Show a placement preview.
4. Let the player move and rotate it.
5. Require a reasonably flat and clear location.
6. Confirm placement explicitly.
7. Save map ID, position, rotation and layout ID.
8. Reload the map/session and restore the yard.
9. Remove or relocate it through an explicit action.
10. Produce useful logs and a recoverable error when placement fails.

At this phase, the yard may be scenery only. It does not need to own vehicles, generate money or run the crusher economy.

## Flat-location policy

The system should help the player choose a location, not silently reshape every map.

Initial safe behavior:

- display slope/flatness result;
- require adequate clear footprint;
- show collision or obstruction warnings;
- allow manual rotation and repositioning;
- reject unsafe placement with a reason;
- avoid automatic terrain deformation in the first version;
- avoid placing at map load without an existing saved record;
- avoid hard-coded West Coast USA coordinates.

Possible later options:

- small foundation/slab that hides minor terrain unevenness;
- several footprint sizes;
- modular expansion pieces;
- optional approved terrain-flattening workflow if BeamNG APIs and save safety are proven.

## Model performance requirements

The yard may contain many stacked cars and props, so performance must be treated as a design requirement.

Recommended rules:

- use low-detail static junk-car shells for background stacks;
- do not use dozens of full simulated vehicles as scenery;
- provide LODs for buildings and large props;
- use simplified collision meshes;
- combine materials where practical;
- avoid extremely large textures on repeated props;
- allow decorative-density settings;
- keep interactive vehicles separate from scenery meshes;
- test CPU, GPU and memory impact on David's current PC and future PC.

## Separation of visual structure and business backend

The yard-placement system owns:

- model/layout selection;
- preview;
- position/rotation;
- flatness/collision validation;
- scene-object creation;
- save/load/remove/relocate behavior.

The Scrap/Wrecking Yard business backend owns:

- yard ownership;
- acquisition/build cost;
- vehicle intake;
- storage capacity;
- dismantling;
- parts/material records;
- crusher transactions;
- scrap value;
- legal/illegal state;
- freight manifests;
- payouts and expenses through approved contracts.

The visual model must not contain hidden duplicate business logic. The backend should reference yard IDs and marked zones rather than depend on one specific mesh.

## Interaction-zone plan

After visual placement is stable, add explicit zones/markers for:

- office/business menu;
- tow drop-off;
- vehicle intake;
- dismantling;
- crusher;
- parts storage;
- scrap loading;
- customer pickup;
- legal disposal;
- optional illegal disposal.

Zones should be stored relative to the placed yard layout so the complete layout can move or rotate.

## Multiple model sets

Supporting several yard styles is encouraged:

- small rural wrecking yard;
- medium independent salvage yard;
- large industrial crusher/scrap facility;
- legal modern recycling yard;
- older rough-looking yard;
- optional underground/hidden annex.

All layouts should use the same backend contract. Style and footprint may change; business data and transaction rules should not split into separate implementations.

## Cross-job boundaries

- JOB-04 — Scrap Yard / Wrecking Yard owns yard-specific placement requirements and business gameplay.
- JOB-09 — Tow / Recovery / Dispatch owns tow calls and deliveries to yard intake zones.
- JOB-06 — Import / Export Yard may later own export buyers or freight destinations for processed scrap.
- JOB-08 — Insurance / Finance / Garage / Storage Pages may expose financing/property services through approved contracts but does not own yard gameplay.
- JOB-02 — Shared RLS / Career Bridge owns shared money, ownership, inventory and transaction operations.
- JOB-10 — Visual Design / Real Website Polish owns website presentation, not three-dimensional gameplay placement unless separately assigned.
- JOB-11 — QA / Logging / Failure Triage validates placement/save/removal/performance once an exact candidate exists.
- JOB-00 — Coordinator / Integration / Verification approves shared contracts and final integration.

## Required testing

The physical placement proof must eventually be tested for:

- fresh placement;
- cancel placement;
- invalid slope;
- obstruction;
- rotation;
- save/reload;
- map exit and return;
- relocation;
- removal;
- missing model asset;
- changed model version;
- second map;
- custom map;
- performance with low/medium/high decoration;
- duplicate-load prevention;
- safe cleanup when the mod is disabled.

## Current truth status

```text
NO THREE-DIMENSIONAL YARD MODEL HAS BEEN APPROVED
NO HOUSE-BUILDER MOD HAS BEEN INSPECTED
NO PLACEMENT SYSTEM HAS BEEN SELECTED
NO VISUAL YARD PROOF HAS BEEN BUILT
NO BUSINESS BACKEND HAS BEEN CONNECTED TO A PHYSICAL YARD
```

This document records the intended path so the idea is not lost while the current Scrap Yard backend remains the immediate priority.
