# RedFox VTOL Drive Handoff — v73 Heavy Load Stabilizer Test

Date: 2026-08-24 local user time
Project: BeamNG RedFox VTOL Drive, formerly SkyRide / FlyingCar / FLYRIDE

## Current Status

The latest delivered test build is `RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST.zip`.

Runtime proof status: **static/package verified only** until David tests it in BeamNG.

v71 Structural Assist improved large vehicles and reduced break-apart behavior. v72 added Gravity Relief + Adaptive Anti-Rock, but David reported that in v72 thruster/fire visuals were missing or weak, hover could lift, then switching to flight mode caused the vehicle to float/drop back down violently. The likely cause was v72 default Gravity Relief lowering effective gravity while plane lift also used current gravity, reducing plane lift, plus Adaptive Anti-Rock default node-force softening reducing thruster authority during detected rocking.

## v73 Purpose

Restore practical v71 flight authority while keeping the useful safety improvements. Add a safer heavy-load anti-rock layer aimed at semis, tow trucks, and cab/trailer combinations.

## v73 Changed Files

- `mod.json`
- `mod_info/MXFWH19SP/info.json`
- `lua/ge/extensions/redfoxSkyRideUI.lua`
- `lua/vehicle/extensions/kanderman/skyride/flight.lua`
- `RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST_README.txt`

## v73 Code Changes

### flight.lua

- Header updated to v73.
- `gravityRelief` default changed from `1.0` to `0.0`.
- `gravityReliefScale` default changed from `0.70` to `0.85`.
- `rockForceSoften` default changed from `0.28` to `0.00` so detected rocking no longer cuts lift/thruster node authority by default.
- `rockBodyShareBoost` default set to `0.18`.
- `rockDampingBoost` default set to `1.75`.
- Added:
  - `heavyLoadStabilizer = 1.0`
  - `heavyLoadYawReduction = 0.55`
  - `heavyLoadRollReduction = 0.35`
  - `planeLowSpeedLiftFloor = 0.65`
- Plane mode gravity assist now uses `planeLowSpeedLiftFloor` so switching from hover to plane at low forward speed should not dump lift as hard.
- During detected rocking in hover or plane mode, Heavy Load Stabilizer reduces hard yaw/roll/pitch correction sent to node forces instead of removing lift. This is intended to stop cab/trailer or flexy-frame oscillation where the cab rocks one way and the trailer/frame rocks the opposite way.

### redfoxSkyRideUI.lua

- UI defaults mirror v73 flight defaults.
- Safety/Visuals panel text updated to explain v73.
- Added sliders/toggles:
  - Heavy Load / Trailer Stabilizer
  - Heavy Load Yaw Reduction
  - Heavy Load Roll Reduction
  - Plane Low-Speed Lift Floor
- Gravity Relief text now warns it is default OFF because v72 could reduce plane lift and cause sinking after mode switch.

## What v73 Does Not Do

- Does not claim true vehicle invincibility.
- Does not rewrite JBeam.
- Does not lock cab and trailer into one rigid object.
- Does not remove trailer articulation.
- Does not change NPC hover logic except preserving the existing v70 NPC hover code in the package.
- Does not change unrelated PSI/tire code or police behavior.

## Known Issues / Observations

- Police/siren issue: no evidence RedFox VTOL Drive creates police, sirens, pursuits, wanted behavior, arrests, or emergency AI. Experimental NPC hover can affect existing traffic vehicles if enabled, but should not spawn or command police.
- F11 World Editor issue: no evidence VTOL caused it. Prior log pointed to `redfoxPSIController.lua:1094` calling nil `spikeStripPopWheel` and wheel/rim detach breakGroup failures.
- v58 BeamNG 0.39.4 fatal bug: `skydros.lua` called `pairs()` on nil during `onExtensionLoaded`. Patches after that guarded `skydros.lua`, `loadSkyride.lua`, and `skyride.lua` initialization paths.

## Test Plan for David

Install only one VTOL ZIP at a time. Clear BeamNG cache after swapping builds.

For v73 first pass:

1. Test a normal car: hover, plane mode, landing.
2. Test the large tow truck that improved in v71.
3. Test semi tractor plus 52-foot trailer.
4. Keep Gravity Relief OFF.
5. Keep Heavy Load / Trailer Stabilizer ON.
6. If semis still rock:
   - Raise Angular Damping Assist.
   - Raise Body Lift Share.
   - Raise Heavy Load Yaw Reduction.
   - Raise Heavy Load Roll Reduction.
   - Keep Rock Force Soften at 0 unless the frame still tears apart before lifting.
7. If flight mode still sinks after hover:
   - Raise Plane Low-Speed Lift Floor gradually from 0.65 toward 0.75.
   - Do not turn Gravity Relief on for the first test.

## Build Verification Performed

- Final ZIP reopened with `unzip -t`.
- ZIP integrity passed.
- Reopened archive showed expected files:
  - `lua/ge/extensions/redfoxSkyRideUI.lua`
  - `lua/vehicle/extensions/kanderman/skyride/flight.lua`
  - `mod.json`
  - `mod_info/MXFWH19SP/info.json`
  - `RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST_README.txt`

Again: this is static/package verification only, not BeamNG runtime proof.

## Next Planned Work

If v73 restores flight but semis/trailers still rock:

- Add a true coupled-vehicle awareness pass if BeamNG APIs expose attached trailers safely.
- Consider a per-vehicle preset system: Small Car, Large Truck, Semi/Trailer, Bus, Experimental.
- Consider an optional Flight Structural Assist part or per-vehicle JBeam support only after the controller is stable.
- Keep old working player VTOL core preserved; do not stack unrelated UI/Hub changes into flight tests.
