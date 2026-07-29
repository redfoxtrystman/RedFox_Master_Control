# JOB-09 v0.4.2 Build Audit — Protected Dispatch, Police Roadblocks, Active Job Recovery

**Job:** JOB-09 — RedFox Tow / Recovery / Dispatch  
**Owner:** David / Captain  
**Build date:** 2026-07-28  
**Artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_2_ProtectedDispatchPoliceRoadblocksActiveJobRecovery.zip`  
**SHA-256:** `34d781728aa72b367645e48a56a2db9247f0829b0dc5e5e8742ae5c148aebbcf`  
**Size:** 1,594,522 bytes  
**ZIP entries:** 120  
**Status:** STATIC VERIFIED — BEAMNG / INSTALLED RLS / RANDOM EVENTS RUNTIME UNTESTED

## Runtime findings that caused this build

- Abandoned and normal tow-call acceptance could pause for roughly 5–10 seconds and then fail to create a job.
- The offer could remain stuck because scene construction ran synchronously without a protected failure boundary.
- Random Events roadway and tunnel scenes could activate without police traffic control.
- A tunnel recovery with two heavily stripped vehicles and cable towing preceded a complete computer crash.
- David requested persistent unfinished-job recovery after a crash or game restart.
- David approved a staged recovery design: restore the same-map job, tow truck, targets, support vehicles, props, route, and phase first; leave Node Grabber/cable restoration and cross-map transfer for a separate experiment.

## Implemented changes

### Protected dispatch acceptance

- Call construction now runs through a protected `xpcall` boundary.
- A failed primary build clears partial scene objects and retries once using procedural-only fallback generation.
- If both builds fail, the dispatcher unlocks and writes a structured failure report instead of leaving a frozen offer.
- Failure data is stored under `settings/redfox/tow_call_failure_reports.json`.
- Primary log marker: `[RedFox][TOW][CALL_FAILURE]`.

### Mandatory roadway police roster

- Roadside and roadway calls now require police traffic control before activation.
- Ordinary roadside scenes require at least one police blocker.
- Major, multi-target, semi, tunnel, or highway-like scenes require at least two.
- Existing imported police vehicles count toward the minimum; fire and ambulance vehicles do not.
- Modern police configurations are preferred, with a fallback to any installed police-marked configuration.
- Emergency lights and hazards are requested on restored/spawned police support.
- If the minimum police roster cannot be produced, the road scene fails safely rather than starting incomplete.
- Primary log marker: `[RedFox][TOW][POLICE_ROSTER]`.

### Same-map active-job recovery

- Active job snapshots are stored under `settings/redfox/tow_active_job_recovery.json` by Career profile key.
- Snapshots save the call type, payout, phase, pickup/drop-off, route data, player tow truck identity and transform, target identities/transforms, and managed support vehicles/vehicle-style props.
- The player-owned tow truck is restored before target and support vehicles.
- Career inventory ID is used when available to avoid spawning a duplicate personal truck.
- Recovery is same-map only in this version.
- The user can Resume Saved Job or Abandon Saved Job from the dispatch UI/portal.
- Autosaves occur at acceptance, scene readiness, phase transitions, Career save, mission end/unload, and an interval-gated active-job timer.
- Saved Random Events live-module references are deliberately not serialized; a resumed scene becomes JOB-09-owned for cleanup.
- Primary markers: `[RedFox][TOW][ACTIVE_JOB_SAVE]` and `[RedFox][TOW][ACTIVE_JOB_CLEAR]`.

### Rolling-chassis handling

- Actual configurations whose metadata/name contains `Rolling Chassis` are excluded from RedFox rollover vehicle selection.
- They remain eligible for other suitable towing, abandoned, salvage, or hazard calls.
- Damage-stripped or wheel-less Random Events crash vehicles remain valid rollback targets.
- Primary marker: `[RedFox][TOW][ROLLOVER_FILTER]`.

## Deliberate exclusions

- Node Grabber cable, chain, rope, or winch attachment restoration.
- Exact deformation and missing-part reconstruction.
- Cross-map connected transport.
- Any modification of Random Events source files.
- Any JOB-04 Wrecking Yard/marketplace changes.

## Verification performed on source and exact re-extracted ZIP

- ZIP CRC/testzip: PASS.
- Duplicate ZIP entries: 0.
- Unsafe/absolute/traversal paths: 0.
- Protected Random Events/Career override paths: 0.
- Native/executable payloads: 0.
- Lua syntax compilation: PASS.
- Mocked Lua module load: PASS.
- Portal JavaScript syntax: PASS.
- BeamNG app JavaScript syntax: PASS.
- All JSON parsed: PASS.
- Static contract suite: 56/56 PASS.
- Source versus re-extracted package hashes: MATCH for all non-regenerated verification files.
- Image readability and manifest dimensions: PASS.
- Random Events 1.9 required scene-module contract: PASS.

## Mandatory runtime tests

1. Request and accept an Abandoned Vehicle call.
2. Confirm failure does not leave a locked offer and that fallback/error reporting works.
3. Test one ordinary roadside scene and verify at least one police blocker with lights.
4. Test a major/tunnel/semi/multi-target scene and verify at least two police blockers.
5. Accept a job, move the tow truck and target, exit normally, reload the same Career/map, and resume.
6. Verify the owned tow truck is restored without duplication, before targets/support.
7. Reconnect cables manually and finish the resumed job.
8. Watch for Random Events cleanup conflicts and crash stability on large scenes.

No BeamNG runtime success is claimed until David completes these tests.