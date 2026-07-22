# JOB-09 — Third-Party Tow/Event Compatibility Audit

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Status:** Static package inspection completed; all runtime integrations remain untested in BeamNG.

---

## Purpose

David supplied three mods for inspection to determine whether they can support:

- towing and impound gameplay;
- illegal street-racing impounds;
- police-requested impounds;
- DUI/checkpoint impounds;
- police presence and enforcement;
- richer accident sites;
- future universal rigging/control work.

The packages were inspected as references and optional runtime integration targets. No third-party source or assets were copied into RedFox.

---

## Archive integrity and identity

### Random Events

```text
File: random_events_1.9.0.0(1).zip
Embedded version: 1.9.0.0
Author: Modslab
SHA-256: c35a240356989a23f83df04efecf34a3f41de1144046efdc434f229eb76766e6
Files inspected: 75
Native EXE/DLL payload: none found
```

Relevant event types found include street race, police checkpoint, traffic stop, police chase, stolen-vehicle flee, accident scene, secondary pileup, and overturned-vehicle scenes.

Manager functions found:

```text
getStatusJson
forceSpawn
toggleUI
rescan / forceRescan
teleportTo
```

Important limitation:

`getStatusJson` provides event identity/type/position information but does not provide the actual event vehicle IDs or a supported transfer-of-ownership function. Individual event modules hold references to their vehicles and delete them during event cleanup/despawn.

Result:

- Safe for status display and opening the original UI.
- Potential future source of call ideas and map-event locations.
- Unsafe to silently adopt its currently spawned vehicles as persistent RedFox tow targets.
- A direct integration needs a future official claim/provider API or explicit compatibility contract.

---

### Traffic Reborn Free

```text
File: TrafficReborn_Free_v1.4.0.0(1).zip
Embedded version: 1.4.0.0
Author: Modslab
SHA-256: a666ad1a07d007b64988ea4fec3911745d0d629e2d2929c45b6d8370de350e80
Files inspected: 31
Native EXE/DLL payload: none found
```

Manager functions useful to RedFox:

```text
isRunning
spawn
setPoliceRatio / getPoliceRatio
setEnforce / getEnforce
```

The enforcement system can identify AI traffic offenders and route them into BeamNG police behavior.

Result:

- Useful for ambient police presence and enforcement around RedFox gameplay.
- v0.2.6 provides explicit user-controlled enable/disable actions.
- RedFox does not automatically alter Traffic Reborn when merely detected.
- Traffic Reborn traffic vehicles are not automatically converted into owned impound targets.

Potential later work:

- Receive a supported offender/arrest event through a provider API.
- Convert a completed police stop into a separate RedFox-owned impound call.
- Keep enforcement and towing ownership separate so traffic cleanup cannot delete an active tow target.

---

### Sandbox Tools

```text
File: sandbox_tools_1.1.0.0(1).zip
Embedded version: 1.1.0.0
Author: Modslab
SHA-256: 578d359568a559af18a8ee30a49fc1e069c2a477c890f087402c6f3dd0cf65fd
Files inspected: 8
Native EXE/DLL payload: none found
```

Relevant generic actions found:

- open or close normal vehicle latches/couplers through `core_funstuff`;
- freeze/unfreeze current vehicle;
- spawn traffic, including police traffic;
- run user-supplied Lua commands.

Result:

- Useful as a manual debugging utility.
- Does not expose a supported arbitrary-node tow-rigging system.
- Does not provide a universal tow-truck control abstraction.
- v0.2.6 detects it but does not depend on or call it.

---

## RedFox v0.2.6 decisions

Implemented independently in RedFox:

- Police-Requested Vehicle Impound.
- Street-Racing Vehicle Impound.
- DUI Checkpoint Impound.
- RedFox-owned target vehicles that can safely persist into the yard ledger.
- Agency tow payment.
- Police impound-hold records.
- Police / Enforcement history catalog.
- Basic police/ambulance/cone support scenes.
- Optional Random Events status/UI adapter.
- Optional Traffic Reborn police ratio/enforcement adapter.
- Sandbox Tools presence detection.

Not implemented:

- Claiming active Random Events vehicles.
- Taking ownership of Traffic Reborn traffic offenders.
- Copying any event logic or assets.
- Universal one-to-four-point hook rigging.
- Unified tow-truck controls.
- Settings/Career backup management.

---

## Licensing and redistribution rule

No explicit reusable-source license was found inside these three uploaded ZIPs. The safe project rule is therefore:

```text
Do not copy, rename, modify, package, or redistribute their Lua, UI, models, textures, configurations, or branding inside RedFox.
```

Optional runtime compatibility may call public extension functions when the original mod is installed. Every RedFox feature must continue to operate without those optional mods unless a future dependency is explicitly approved by David.

---

## Required future proof before live offender impounds

A police/enforcement integration that turns another mod's live offender into a tow target must provide all of the following:

1. Stable vehicle ID.
2. Event ownership/lifecycle contract.
3. A claim, detach, or do-not-despawn action.
4. Completion/cancellation callback.
5. Permission to integrate through that API.
6. Safe cleanup if either mod unloads.

Until that exists, RedFox should spawn its own equivalent impound scene after the police event rather than taking over a third-party vehicle.
