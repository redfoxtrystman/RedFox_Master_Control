# JOB-09 Work Chat to Regular Chat Transfer

**Date:** 2026-07-14  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch Integration  
**New active workstation:** 19 — JOB-09 — RedFox Tow / Recovery / Dispatch — Regular Chat Workstation  
**Status:** TRANSFER COMPLETE — v0.2.1 BUILT — RUNTIME UNTESTED

## Transfer authority

David reported that the former JOB-09 conversation was inside a limited Work project and directed this regular chat to take over the entire JOB-09 workstation, update GitHub, and notify all other RedFox chats.

The regular chat is now the sole active JOB-09 owner. The former Work conversation is retained only as historical context.

## Files received in the regular chat

### 1. v0.2.0

`19-RedFox_TowRecoveryDispatch_v0_2_0_CallChooserYard.zip`

- Size: 29,438 bytes
- SHA-256: `217bc62ef0573feb888cf630c4d002fa49996a2fc0aa1cddc06a58e2720cc9ea`
- ZIP integrity: PASS
- Archive entries: 27

Primary content:

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- input action definition
- RedFox module registration
- modScript and mod info
- README, changelog, test checklist
- v0.1.0 and v0.2.0 verification/diff/roadmap notes

Transferred runtime concern:

- David attempted an abandoned-vehicle call and did not receive a location/route to travel to.

This regular chat has not independently reproduced the v0.2.0 result.

### 2. v0.2.1

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_1_RolloverScenesMultiYard.zip`

- Size: 48,909 bytes
- SHA-256: `357c44f4494f7199071282ef3ec7e8e0a2f747ee19c8a12b25ed40da9e0ae2b1`
- ZIP integrity: PASS
- Archive entries: 31
- Status: **BUILT — RUNTIME UNTESTED**

David stated he had not yet tested this candidate.

## Static v0.2.1 change summary

Compared with v0.2.0, v0.2.1 adds or changes:

- delayed and repeated post-spawn crash transforms for rollover scenes
- rotated roadside/impact procedural layouts
- short physics impact passes for visible fresh damage
- capture/delete/reuse of relative crash-scene layouts
- scene modes: Prefer Saved, Procedural Only, Saved Only
- response mileage plus tow mileage in job quotes
- manual route retry controls
- automatic route refresh after marker initialization
- multiple persistent player-selected tow-yard locations per map
- migration of the old single-yard record to Tow Yard 1
- closest-yard selection for yard-bound calls
- refusal to accept yard-bound calls when no yard has been set
- paid versus unpaid test outcomes
- impound lien, daily storage, hold period, market estimate, and asking-price records
- force-next-unpaid test control
- persistent Tow History Book
- local theme/size settings based on Garage Hub presentation patterns
- destination-provider registration API for future approved integrations

## Important behavior change for the missing-location report

v0.2.1 no longer invents or automatically chooses a tow yard for yard-bound calls.

For Abandoned Vehicle Recovery, Multi-Vehicle Accident Cleanup, Rolled Car Recovery, and Semi Rollover Recovery, David must first add at least one tow-yard location on the current map. If no yard exists, the candidate is designed to reject the call with an explicit message rather than accept a call with no usable destination.

This must be verified in BeamNG; static inspection does not prove the UI message or route behavior.

## Minimum first test

1. Disable/remove every older JOB-09 Tow Recovery Dispatch ZIP.
2. Install only `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_1_RolloverScenesMultiYard.zip`.
3. Load the intended Career save and map.
4. Open the dispatcher.
5. Add a tow-yard location at the player's current position.
6. Request and accept an Abandoned Vehicle Recovery call.
7. Confirm the route appears to the target.
8. Press **Route to Current Target** if it does not appear automatically.
9. Move the recovered target more than 10 metres.
10. Confirm the route switches to the chosen yard.
11. Deliver the target and verify the expected decision/history flow.
12. Save/reload and verify the yard and Tow History Book persist.

## Additional tests

- Rolled Car Recovery remains tipped after spawn initialization.
- Semi Rollover Recovery remains tipped and uses a valid semi configuration.
- Multi-Vehicle Accident routes back for additional targets.
- Multiple yards persist and closest-yard selection is sensible.
- Force-next-unpaid creates an impound entry rather than normal payment.
- Route retry buttons recover from delayed map-marker initialization.
- No duplicate JOB-09 ZIP is enabled.

## Evidence requested after test

- BeamNG log from the exact session
- screenshot of dispatcher status when no route appears
- screenshot of map/marker if the route is wrong
- screenshot of rollover scene if the vehicle spawns upright
- steps used before the failure
- active map name
- confirmation that at least one yard existed before accepting a yard-bound call

## Repository boundaries after transfer

The new workstation may maintain JOB-09-owned mod files, documentation, test candidates, and coordination records. It must not edit shared platform, bridge, other app, stock Career/RLS, ownership, money, property, garage/storage, or vehicle-shopping files.

## Coordination notice

All RedFox chats must treat:

`PROJECT_MANIFESTS/JOB_CLAIMS/JOB-09_TOW_RECOVERY_DISPATCH_CLAIM.md`

as the active JOB-09 claim. Questions or requested interfaces should be posted to the JOB-09 GitHub coordination issue. Runtime status remains **BUILT — RUNTIME UNTESTED** until David tests the exact v0.2.1 ZIP.
