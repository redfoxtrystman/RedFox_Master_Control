# JOB-09 — Roadside Mixed Scenes v0.2.3 Handoff

**Date:** 2026-07-15  
**Owner:** JOB-09 regular-chat workstation  
**Status:** **BUILT — RUNTIME UNTESTED**

## Candidate

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_3_RoadsideMixedScenes.zip`

- Size: 75,570 bytes
- SHA-256: `0a1c7314ca5b896fd639c2d866e3c1053899de8be18e3f981ba7bb7462725721`
- ZIP integrity: PASS
- JSON parse: PASS
- Lua syntax: PASS via `texlua loadfile`
- Protected Career-path scan: PASS
- BeamNG runtime: UNTESTED

## Direction correction

The v0.2.1 screenshot was initially misread. The rotator and trailer were spawned crash targets, not David's player tow truck. Mixed heavy/commercial vehicles are wanted. The actual failure was the compact parking-lot location and poor scene composition.

`v0.2.2 AccidentSceneFitGuard` is therefore **REJECTED — DO NOT USE** because it removed semis, trailers, buses, and heavy vehicles from generic crash scenes.

## v0.2.3 behavior

- Accident, rolled-car, and semi-rollover scenes use road-graph roadway or roadside/shoulder anchors instead of parking-space anchors.
- Cars, buses, heavy wreckers/rotators, semis, and trailers remain valid targets.
- Trailers are selected through semi/commercial scene plans instead of acting as an ordinary-car substitute.
- Added real-world-inspired plans:
  - two-vehicle lane collision;
  - three-vehicle chain collision;
  - shoulder rollover with secondary impact;
  - semi/trailer jackknife across lanes;
  - semi/trailer collision partly on the shoulder;
  - heavy truck/rotator cross-lane wreck;
  - rare bus multi-vehicle crash.
- Directional physics impacts are applied for fresh damage.
- Default roadside/shoulder scene chance is 38% and is adjustable.
- Matching player-built RedFox scenes have 80% default priority and are adjustable.
- Registered random-event providers have a 35% chance when no saved scene was selected.

## Random-event and police-line integration

v0.2.3 does not guess undocumented functions. It:

- probes `gameplay_events_freeroamEvents` at runtime;
- logs detected public function names with `[RedFox][TOW][EVENT_LIBRARY]`;
- exports `registerSceneProvider(providerId, callback, priority)`;
- exports `unregisterSceneProvider(providerId)`;
- exports `getSceneProviderContract()`.

A later adapter can use existing random-event crashed cars, police lines, cones, barrels, emergency vehicles, and debris after the exact public API or source files are inspected.

## Required first test

1. Disable v0.2.1 and v0.2.2.
2. Enable only v0.2.3.
3. Use a disposable Career save.
4. Add at least one tow-yard location.
5. Select **Procedural Only**.
6. Run at least five Multi-Vehicle Accident Cleanup calls.
7. Confirm road or roadside/shoulder placement, mixed vehicle classes, visible damage, routing, and yard delivery.
8. Return screenshots and the complete `[RedFox][TOW][EVENT_LIBRARY]` log line.

## Known limits

- Road-graph placement is not yet tested on every map.
- Saved capture records event target vehicles but not every support prop, cone, emergency vehicle, or NPC.
- Exact deformation is not serialized; fresh damage is generated through the impact pass.
- The actual ZIP is retained in the active regular-chat workstation; this GitHub connector records the exact identity and handoff.