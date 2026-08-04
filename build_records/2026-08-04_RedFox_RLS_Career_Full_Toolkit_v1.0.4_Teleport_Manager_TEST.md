# RedFox RLS Career Full Toolkit v1.0.4 — Teleport Manager Test

## Status

Built and statically verified. Runtime testing by David is still required.

## Base

- Source build: `RedFox_RLS_Career_Full_Toolkit_v1.0.3_Vehicle_Photo_Manager_TEST.zip`
- New build: `RedFox_RLS_Career_Full_Toolkit_v1.0.4_Teleport_Manager_TEST.zip`

## Artifact SHA-256

`0fffebf3aff97c84e53241db9e24764aab8280de2ec3602a6144a9b7d7ec152b`

## Added

- TELEPORT top tab
- Teleport controlled vehicle/convoy to current camera
- Teleport controlled vehicle/convoy to selected map destination
- Configurable nearby-vehicle convoy radius
- Convoy preview by BeamNG vehicle object ID
- Save named vehicle positions
- Save named camera positions
- Persistent saved-location database
- Same-map saved-location teleport
- Cross-map saved-location travel proof using RLS Career `switchCareerLevel()`
- Pending destination reapplied after the destination map reaches ready state

## Preserved

- Career development tools
- Economy controls
- RLS XP tabs and controls
- Integrated Node Grabber
- Force-add vehicle to garage
- Vehicle Photo Manager
- Garage Hub theme support

## Known limits

- Runtime is unproven until David tests this exact ZIP.
- Nearby convoy selection currently targets BeamNG vehicle objects.
- Loose cargo props are not guaranteed to move.
- Complex trailer orientation may require a follow-up correction.
- Cross-map travel prioritizes retaining vehicles over duplicate prevention.
- Duplication is acceptable in this proof stage if required to avoid missing vehicles.

## Verification completed

- Source ZIP integrity checked
- Existing feature tokens checked after edit
- Teleport feature tokens checked after edit
- All JSON files parsed
- Final ZIP reopened
- Final packaged Lua rechecked for required and preserved functions

## Test order

1. Back up the Career save.
2. Disable older toolkit, standalone Cheat Tool, and standalone Grabber ZIPs.
3. Test current vehicle to camera.
4. Test current vehicle to map destination.
5. Enable nearby convoy and test a trailer or hauled vehicle.
6. Save and reload a same-map location.
7. Test cross-map travel last with noncritical vehicles.

## Rollback

Disable v1.0.4 and restore the last confirmed working toolkit ZIP.