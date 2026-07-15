# JOB-09 — Used Car Generator Compatibility Intake

**Date:** 2026-07-15  
**Owner:** JOB-09 regular-chat workstation  
**Status:** REFERENCE INSPECTED — OPTIONAL COMPATIBILITY PLANNED

## Uploaded reference

`barnfindgenerator.zip`

- BeamNG resource title: `Used Car Generator`
- Author: `Cedminer66`
- Embedded version: `0.8.2`
- Size: 8,037,600 bytes
- SHA-256: `c94a16a6059a11707ffbe22f60cca415de5c7901cf074c25ee1d3e8cad423658`
- ZIP integrity: PASS
- Native DLL/EXE payloads: none
- Main source files:
  - `lua/ge/extensions/barnfindGenerator.lua`
  - `lua/vehicle/extensions/barnfindGenerator.lua`
  - `ui/modules/apps/UsedCarGenerator/*`

## License and redistribution boundary

Both Lua source files carry the BeamNG bCDDL 1.1 source notice. The uploaded archive does not contain a local copy of the referenced license text.

JOB-09 will therefore **not** copy, rename, bundle, or redistribute the original Lua/UI/image files inside a RedFox ZIP. The safe integration path is:

1. detect the separate mod at runtime;
2. call only its exported public function when present;
3. keep RedFox fully functional when it is absent;
4. credit `Cedminer66 / Used Car Generator` in compatibility documentation; and
5. implement any future native RedFox condition system independently rather than copying formulas or UI.

## Useful exported behavior

The GE extension exports:

- `spawnBarnfind`
- `applyWear`
- `setupPaint`
- `respawnPrev`
- `reapplyWear`
- `loadSettings`
- `saveSettings`

The most useful JOB-09 hook is:

`extensions.barnfindGenerator.applyWear(conditionConfig, vehicleObject)`

When the separate mod is installed, JOB-09 can apply deterministic mileage and condition profiles to a specific spawned recovery target without using the Used Car Generator UI or its random-location spawner.

## Useful systems for JOB-09

### Vehicle selection

- population-weighted factory configurations;
- optional modded vehicles;
- maximum model year;
- deterministic generation and wear seeds;
- random factory paint selection.

### Vehicle condition

The source supports more than 25 condition inputs, including:

- paint, body panels, fixtures;
- tires, brakes, suspension;
- radiator, coolant, oil pan, exhaust;
- crankshaft, fuel pump, spark plugs, idle controller, starter;
- head gasket, piston rings, connecting rods;
- turbocharger and supercharger components;
- fuel level, fuel tank leakage, battery charge;
- clutch components, gearbox, torque converter;
- electric-motor output.

Possible physical effects include flat tires, broken suspension/fixtures/exhaust, reduced braking, rough/no-start engines, cooling/oil/fuel leaks, damaged transmissions, low fuel, and dead batteries.

## JOB-09 uses

The strongest uses are for non-collision recovery work:

- abandoned vehicles with believable age, mileage, and neglect;
- disabled-vehicle calls with one or more mechanical faults;
- non-runners requiring winching rather than ordinary driving;
- locked, flat-tired, leaking, or suspension-damaged impounds;
- stored-yard vehicle condition records and later appraisal;
- repeatable condition seeds stored in Tow History;
- future equipment recommendations such as flatbed, wheel-lift, dollies/skates, heavy wrecker, or rotator;
- future job subtypes such as barn find, long-abandoned vehicle, seized engine, dead battery, fuel leak, cooling failure, and transmission failure.

## What JOB-09 will not borrow

- The mod's random road-node placement is too simple for RedFox accident scenes because it chooses a random node and random heading. JOB-09 keeps its road-segment/shoulder scene placement.
- Its experimental deformation option is not suitable as the main crash-scene damage system; the resource description warns that it can produce strange behavior or vehicle explosions. JOB-09 keeps its own directional crash impacts and hand-built scenes.
- The Used Car Generator UI, art, settings window, and files will not be embedded in RedFox.

## Known upstream limitations to respect

The resource author has acknowledged that some balanced-wear override values can be inaccurate and that body-panel wear requires deformation to be enabled. Therefore RedFox should use broad condition profiles rather than promise exact percentage accuracy for every part.

## Planned RedFox compatibility architecture

Keep `v0.2.3 RoadsideMixedScenes` as the active scene-placement test candidate. Do not stack this condition integration into the same first road-placement test.

The next condition-focused candidate should add:

1. an optional condition-provider registry:
   - `registerVehicleConditionProvider`
   - `unregisterVehicleConditionProvider`
   - `getVehicleConditionProviderContract`
2. automatic detection of `extensions.barnfindGenerator.applyWear`;
3. RedFox-owned condition profiles:
   - `roadside_breakdown`
   - `neglected_abandoned`
   - `long_abandoned_nonrunner`
   - `impound_worn`
4. condition application by default only to `abandoned` and `tow_car` targets;
5. no mechanical-wear injection into accident/rollover targets unless explicitly enabled later;
6. target metadata for condition profile, mileage, condition seed, provider, and requested faults;
7. storage of that metadata in Tow History and temporary-yard records;
8. clear fallback behavior when the separate Used Car Generator mod is not installed.

## Runtime evidence needed before implementation is called working

- v0.2.3 road/shoulder placement test must be completed first.
- With Used Car Generator installed separately, a later candidate must prove that one abandoned target receives the requested condition and remains towable.
- Without Used Car Generator installed, the same candidate must load and generate jobs without errors.
- No claim of exact part-condition accuracy will be made without BeamNG inspection and David testing.
