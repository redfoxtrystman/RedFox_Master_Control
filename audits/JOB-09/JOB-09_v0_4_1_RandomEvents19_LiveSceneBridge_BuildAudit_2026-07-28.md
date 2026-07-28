# JOB-09 v0.4.1 — Random Events 1.9 Live Scene Bridge Build Audit

**Date:** 2026-07-28  
**Job:** JOB-09 — RedFox Tow & Recovery Dispatch  
**Artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_1_RandomEvents19LiveSceneBridge.zip`  
**SHA-256:** `155652c772fba16eb6025d52af81fe0fc0e48d21d41b3672f9f00ed452a0a2a7`  
**Status:** STATIC VERIFIED — BEAMNG / RANDOM EVENTS 1.9 RUNTIME TEST REQUIRED

## Scope

This build adds a live bridge to installed Random Events 1.9.0.0 scene modules. JOB-09 calls selected source event modules directly, adopts the returned live vehicles/props into a paid tow workflow, and retains the original source module/instance for final cleanup and road-drivability restoration.

## Imported source scenes

- Multi-Car Crash
- Serious Accident Scene
- Secondary Pileup
- Overturned Passenger Car
- Overturned Heavy Truck
- Overturned Semi and Trailer
- Lost Load / Cargo Spill
- Vehicle Fire Recovery
- Stalled Vehicle
- Flat Tire Tow
- Lane-Blocking Breakdown
- Tow Already in Progress
- Police Traffic-Stop Impound

## Equipment learning

Random Events cones, barriers, delineators/signs, barrels/debris, police, ambulance, fire, and tow-support configurations are learned automatically. The player may also spawn any BeamNG vehicle-style prop and teach its exact model/configuration to a quick Scene Builder role.

Persistent mapping file:

`settings/redfox/tow_scene_equipment_mappings.json`

## Boundaries

- No Random Events file copied, modified, or overridden.
- No stock BeamNG or RLS protected path modified.
- JOB-09 does not force-enable Random Events' autonomous scheduler.
- Company garage movement, custody Claim & Transfer, title/lien billing, auctions, and NPC-driver execution remain safety-locked/planned.

## Verification

Passed on source and re-extracted artifact:

- ZIP CRC/integrity and duplicate-path check
- Lua syntax and mocked module load
- JavaScript syntax
- JSON parsing and metadata version
- Random Events source-module contract for all 13 imported scenes
- Portal action bridge
- Garage Hub contract
- Image manifest and dimensions
- Protected-path and executable-payload scan
- No copied Random Events source paths

Runtime testing must verify source-scene spawn, full cleanup, road-drivability restoration, delayed Secondary Pileup adoption, semi/trailer roster preservation, and equipment mapping persistence.