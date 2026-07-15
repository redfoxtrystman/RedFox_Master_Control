# JOB-09 — Accident Scene Fit Guard v0.2.2

**Date:** 2026-07-15  
**Owner:** Regular ChatGPT JOB-09 workstation  
**Status:** BUILT — RUNTIME UNTESTED

## Runtime evidence

David's first v0.2.1 Multi-Vehicle Accident Cleanup test produced an impossible compact parking-lot scene containing a long standalone semi trailer and a passenger car around one parking-space anchor.

## Confirmed v0.2.1 source cause

- Generic accidents could prefer a semi for the first target.
- Every non-T-Series model was accepted as a normal non-semi fallback, allowing standalone trailers and other oversized models.
- All targets were positioned by fixed offsets from one parking-space anchor.

## v0.2.2 correction

- Generic accident calls use a passenger-size-only selection purpose.
- Semis, standalone trailers, buses, RV/caravan models, containers, boats, aircraft, trains, forklifts, and excavators are excluded from generic accident selection.
- Procedural accidents require two or three adjacent parking spaces.
- One target is assigned to each selected space.
- A three-target request downgrades to two when only two adjacent spaces are available.
- No compatible two-space cluster returns a clear dispatch error rather than spawning an impossible scene.
- Dedicated Semi Rollover Recovery retains semi selection.

## Candidate identity

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_2_AccidentSceneFitGuard.zip`

- Size: 62,993 bytes
- SHA-256: `77911a02e279769b7472c242ded1068da4c8016b3d194d6ce795231515bf03f4`
- ZIP integrity: PASS
- JSON parse: PASS
- Lua syntax: PASS via `texlua loadfile`
- Protected-path scan: PASS

## Required first runtime test

1. Disable/remove v0.2.0 and v0.2.1.
2. Enable only the exact v0.2.2 candidate.
3. Set Scene Selection Mode to Procedural Only.
4. Run at least five Multi-Vehicle Accident Cleanup calls.
5. Confirm every target is passenger-size.
6. Confirm one target begins in each adjacent parking space.
7. Confirm no target intersects another target, a building, wall, prop, or an untouched player tow truck.
8. Return the screenshot, target model/config names, map, scene source, and `beamng.log` for any failure.

## Known limits

- Old saved scene templates remain intentionally preserved and may still contain oversized vehicles.
- Dedicated Semi Rollover Recovery still needs a later large-site validation pass.
- Static validation does not prove BeamNG runtime.

## Coordination

GitHub issue: `#4 — [JOB-09] CLAIMED — Tow / Recovery / Dispatch transferred to regular chat`
