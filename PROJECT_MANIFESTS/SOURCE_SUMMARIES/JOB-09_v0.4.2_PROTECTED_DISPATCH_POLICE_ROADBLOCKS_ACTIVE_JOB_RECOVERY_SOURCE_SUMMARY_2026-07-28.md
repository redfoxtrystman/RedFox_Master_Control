# JOB-09 v0.4.2 Source Summary

**Job:** JOB-09 — RedFox Tow / Recovery / Dispatch  
**Version:** 0.4.2  
**Date:** 2026-07-28  
**Runtime status:** UNTESTED IN BEAMNG / INSTALLED RLS / RANDOM EVENTS

## Principal files changed

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`
- `ui/modules/apps/redfoxTowPortal/app.json`
- `ui/modules/apps/redfoxTowPortal/portal.html`
- `mod_info/redfox_tow_recovery_dispatch/info.json`
- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
- `README.md`
- `TESTING_CHECKLIST.md`
- `CHANGELOG.md`

## Runtime contracts added

### Recovery data

- File: `settings/redfox/tow_active_job_recovery.json`
- Per-Career-profile snapshot store.
- Saves player tow-truck identity/transform, call state, route state, target vehicles, and managed support objects.
- Restores only on the same map.
- Resumes through `M.activeJobRecovery.resume()`.
- Abandons through `M.activeJobRecovery.abandon()`.

### Failure reporting

- File: `settings/redfox/tow_call_failure_reports.json`
- Protected call-build failures retain event type, stage, error, map, and timestamp.
- Call build entry point: `M.activeJobRecovery.buildEventSafely(eventType)`.

### Police enforcement

- `vehicleRules.minimumPoliceForEvent(event)` determines one- or two-unit minimum.
- `vehicleRules.ensurePoliceBlockers(event, pickup, minimum)` verifies/spawns police and requests emergency lighting.
- Road scenes cannot activate when the required roster is not met.

### Rolling-chassis filter

- `vehicleRules.isRollingChassis(info)` checks actual configuration metadata/name.
- Applied only to rollover selection/replay paths.
- Damage-created stripped vehicles are intentionally not rejected.

## Recovery order

1. Validate same map and stored snapshot.
2. Find the saved player tow truck by Career inventory ID.
3. Restore that owned vehicle's transform; do not spawn a duplicate.
4. Spawn undelivered target vehicles.
5. Spawn support vehicles and vehicle-style props.
6. Re-verify the mandatory police roster.
7. Restore active route and job phase.
8. Save a refreshed recovered snapshot.

## Autosave points

- Call accepted.
- Random Events scene ready.
- Abandoned-vehicle decision phase.
- Next target in a multi-target scene.
- Career save.
- Client mission end.
- Extension unload.
- Interval-gated active-job timer, default approximately 10 seconds.

## Cleanup and ownership boundaries

- Random Events remains an optional live scene provider.
- No Random Events source is copied, patched, or overridden.
- A recovered scene does not serialize a live Random Events module table/reference.
- Resumed targets/support become JOB-09-managed for cleanup.
- This build does not change JOB-04 Wrecking Yard, JOB-01 PC/phone core, or another job owner's source.

## Known limitations

- Cable/Node Grabber/winch attachments must be manually reconnected.
- Exact physical deformation and detached parts are not reproduced.
- Cross-map job continuation is not implemented.
- Police placement, lighting activation, Career inventory lookup, and Random Events cleanup remain runtime-unproven.

## Artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_2_ProtectedDispatchPoliceRoadblocksActiveJobRecovery.zip`

SHA-256: `34d781728aa72b367645e48a56a2db9247f0829b0dc5e5e8742ae5c148aebbcf`  
Size: 1,594,522 bytes  
Entries: 120