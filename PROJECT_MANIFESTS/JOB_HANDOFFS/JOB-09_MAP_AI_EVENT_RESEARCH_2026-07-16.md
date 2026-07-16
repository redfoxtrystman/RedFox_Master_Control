# JOB-09 — Map, AI, Paint, and Event Research

**Date:** 2026-07-16  
**Purpose:** Record usable BeamNG systems and external behavior references without expanding current JOB-09 beyond the standalone Tow test mod.

## Official BeamNG systems

### AI transport feasibility

BeamNG AI provides Manual mode for driving to a determined position, plus Follow, Stopping, and Traffic modes. The Drive Path Editor also demonstrates NavGraph/free-form routes, vehicle-to-path links, route speed, lane following, vehicle avoidance, delayed starts, and multiple vehicles using paths.

This supports the owner's future workflow:

1. player performs hookup, loading, and rigging;
2. AI drives the secured load toward a selected yard;
3. when the exact yard is not reachable through the navigation graph, the AI stops at the closest safe reachable point and waits with hazards/beacons;
4. player finishes parking or unloading.

This workflow is **not implemented in v0.2.5**.

### Map site classification

Positive-drivability DecalRoads contribute to the AI/navigation graph. Road data includes node positions, width, lane direction, and junction connectivity. JOB-09 can therefore infer useful scene types from graph shape:

- node degree 3+ and crossing directions: intersection / T-bone candidate;
- degree 2 with strong direction change: sharp-curve rollover candidate;
- large elevation change over horizontal distance: steep-grade candidate;
- long/wide segment: semi, trailer, bus, and heavy-recovery candidate.

This is a best-effort heuristic. Map navigation quality varies.

### Vehicle paints

BeamNG's paint system uses base color, metallic, roughness, clear coat, and clear-coat roughness. Its traffic paint distribution supports weighted colors to produce a more realistic traffic pool. v0.2.5 follows that concept for procedural scene vehicles and stores captured PBR paint records for player fleet units.

## External mod/resource behavior references

Reference behavior only; no external source or asset is bundled:

- **Used Car Generator:** future optional condition provider for abandoned and disabled vehicles.
- **Police Behaviour:** evidence that roadblock behavior can be layered onto police systems; inspect/public-API adapter required before use.
- **Post Crash Extras:** reference for post-impact details such as stuck horns and engine shutoff.
- **Universal Vehicle Failures:** reference for future breakdown call types such as brake failure, dead engine, puncture, suspension damage, and transmission failure.
- **Pseudo Random Tour / scenario resources:** reference for random route/event placement, not a code source.

## Official documentation reviewed

- `https://documentation.beamng.com/tutorials/ai/`
- `https://documentation.beamng.com/world_editor/tools/drive_path_editor/`
- `https://documentation.beamng.com/world_editor/tools/drive_path_editor/overview/`
- `https://documentation.beamng.com/modding/levels/level_classes/decalorad/`
- `https://documentation.beamng.com/modding/levels/level_formats/map/`
- `https://documentation.beamng.com/modding/vehicle/vehicle_paints/paint_distribution/`
- `https://documentation.beamng.com/modding/vehicle/vehicle_paints/paint_materials_intro/`

## Random-event integration evidence still needed

The current mod safely probes `gameplay_events_freeroamEvents` and logs:

`[RedFox][TOW][EVENT_LIBRARY] ...`

Return that complete line or provide the exact random-event source archive. JOB-09 will then build a narrow provider adapter for existing wreck layouts, cones, barrels, police blockers, emergency vehicles, and debris without guessing undocumented calls.
