# JOB-09 v0.4.2 Final Artifact Record

**Job:** JOB-09 — RedFox Tow / Recovery / Dispatch  
**Artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_2_ProtectedDispatchPoliceRoadblocksActiveJobRecovery.zip`  
**Built:** 2026-07-28  
**SHA-256:** `34d781728aa72b367645e48a56a2db9247f0829b0dc5e5e8742ae5c148aebbcf`  
**Size:** 1,594,522 bytes  
**ZIP entries:** 120  
**Status:** STATIC VERIFIED — BEAMNG / INSTALLED RLS / RANDOM EVENTS RUNTIME UNTESTED

## Included

- Protected call acceptance with one procedural-only fallback.
- Structured call-failure records.
- Mandatory police traffic control for every roadway/roadside scene.
- One-unit ordinary roadside minimum; two-unit major/tunnel/semi/multi-target minimum.
- Same-map active-job autosave and resume/abandon controls.
- Player-owned tow-truck restoration before target/support restoration.
- Target/support/vehicle-prop restoration, route restoration, and job-phase restoration.
- Actual `Rolling Chassis` configuration exclusion from RedFox rollover selection only.
- Random Events stripped or wheel-less crash vehicles remain valid rollback jobs.

## Not included

- Node Grabber, cable, chain, rope, or winch-link restoration.
- Exact deformation/missing-part reconstruction.
- Cross-map continuation.
- Runtime proof.

## Verification

- Exact ZIP CRC: PASS.
- Exact ZIP duplicate entries: 0.
- Exact ZIP unsafe paths: 0.
- Exact ZIP protected paths: 0.
- Exact ZIP executable/native payloads: 0.
- Lua syntax: PASS.
- Mocked Lua load: PASS.
- JavaScript syntax: PASS.
- JSON parsing: PASS.
- Static tests: 56/56 PASS.
- Source/re-extraction hash match: PASS.

## First required runtime sequence

1. Disable v0.4.1 and all older JOB-09 ZIPs.
2. Enable this v0.4.2 ZIP and Random Events 1.9.
3. Request and accept Abandoned Vehicle.
4. Test an ordinary road scene for one police blocker.
5. Test a tunnel/semi/multi-target scene for two police blockers.
6. Start a tow, reposition the player's truck/target, exit normally, reload the same map, and use Resume Saved Job.
7. Confirm no owned-truck duplicate and reconnect towing cables manually.

The artifact must remain marked runtime-unproven until David reports results.