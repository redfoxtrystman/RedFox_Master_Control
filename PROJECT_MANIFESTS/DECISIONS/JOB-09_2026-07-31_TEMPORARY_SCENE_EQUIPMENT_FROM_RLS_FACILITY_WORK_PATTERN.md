# JOB-09 Decision — Temporary Scene Equipment from the RLS Facility-Work Pattern

**Date:** 2026-07-31
**Owner:** David / Captain
**Applies to:** JOB-09 Scene Manager / Roadside Equipment
**Status:** APPROVED DESIGN DIRECTION — DEFERRED UNTIL AFTER v0.4.4.8

## Confirmed RLS reference

RLS facility work spawns quarry/loading materials with `core_vehicles.spawnNewVehicle(model, { config, pos, rot, autoEnterVehicle = false })`. It tracks the resulting BeamNG object IDs in temporary job/session tables and deletes those objects during cleanup or when the configured persistent-object limit is exceeded.

These objects are BeamNG vehicle-class physics objects internally, but they are not automatically made Career-owned inventory records or assigned to purchased garages.

## JOB-09 design

Add a simple Scene Manager **Equipment Palette** for temporary roadside equipment:

- traffic cones;
- road signs;
- barricades and barrels;
- flare/marker objects;
- debris and lost-load objects;
- arrow-board/light-board trailers;
- other owner-approved installed spawnable model/config pairs.

## Required behavior

1. Spawn the exact installed model/config with `autoEnterVehicle = false`.
2. Tag every spawned object with JOB-09 scene ID, role and cleanup ownership.
3. Save reusable templates using model, config, relative transform, role and optional settings—not transient object IDs.
4. Replay by spawning new objects and rebuilding the scene roster.
5. Delete only JOB-09-owned temporary objects when a scene is rejected, completed, abandoned or cleaned up.
6. Never add temporary scene equipment to Career inventory, garage ownership, lien, custody or company-fleet records.
7. Keep arrow-board trailers and similar vehicle-like equipment usable as temporary scene support even though the engine represents them as BeamNGVehicle objects.
8. Add object-count and spawn-retry limits to prevent call-time performance problems.
9. Keep third-party JBeam, prop and controller files untouched.
10. Keep manual teaching/mapping for unknown installed equipment.

## UI goal

The user should not need to understand the existing technical Scene Builder controls. The palette should provide clear categories, one-click spawn near the scene anchor, select/move/rotate, include/exclude from saved template, duplicate, and delete.

## Boundary

This feature is not part of v0.4.4.8. The owned-garage map selector and relinking repair must be completed and tested first.
