# RedFox VTOL Drive — Master Handoff v70 to v73

Date updated: 2026-08-27 22:56 PT
Project: BeamNG current mods / RedFox VTOL Drive
Former source names seen in files or UI: SkyRide, SkyRider Ultimate, FlyingCar, FLYRIDE.
Current visible/public name target: **RedFox VTOL Drive**.

## Critical process rules

- Do not stack unrelated changes into flight tests.
- Inspect baseline ZIP before editing.
- Preserve old working hover/flight/landing core unless the user explicitly asks for a flight patch.
- After editing, inspect diffs and reopen the final ZIP.
- Runtime status must remain **static/package verified only** until David tests in BeamNG.
- Install only one VTOL ZIP at a time.
- Do not broadly rename internal Lua module paths unless isolated and tested; previous full rename broke loading.
- Public UI/listing name should be RedFox VTOL Drive, but required license/attribution credits should not be deleted if the original mod requires them.

## Current latest test build

Latest delivered package:

`RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST.zip`

Runtime proof status: **not proven yet by David at the time of this handoff**.

v73 was created after v72 caused loss of flight authority / sinking after switching from hover into flight mode. The intended v73 goal is to preserve the good parts of v71 and remove the bad default behavior from v72.

## Current known runtime observations from David

### v70 NPC hover

David reported that NPC hover worked.

Observed behavior:

- NPC vehicles could hover.
- Most hovered and moved from about 1 ft to 20 ft above ground.
- At least one NPC spun.
- NPC hover needs adjustment.

Important decision:

- NPC hover is currently part of RedFox VTOL Drive, not a standalone mod.
- It may later become its own module, likely `RedFox Traffic VTOL` / `redfox_traffic_vtol`, after the behavior is stable.

### v71 Structural Assist

David reported v71 made VTOL work a lot better:

- Vehicles break apart less.
- Larger vehicles improved especially.
- Still not perfect.

### v72 Gravity Relief + Anti-Rock

David reported a regression in v72:

- Thruster/fire visual seemed gone or weak.
- Nothing seemed to fly correctly.
- Vehicle could hover to a good height, but switching into flight mode caused it to float/drop back down violently.

Likely cause recorded:

- Gravity Relief default ON reduced effective gravity while plane lift calculation also depended on current gravity.
- Adaptive Anti-Rock default `Rock Force Soften` reduced node/thruster force authority during rocking detection.
- Combined effect reduced flight authority.

### v73 Heavy Load Stabilizer

v73 was built to fix v72’s regression by restoring flight authority and making heavy vehicles/trailers less destructive.

David had not yet confirmed v73 runtime when this handoff was written.

## Important non-VTOL observations

### Police/siren issue

David reported constant police vehicles driving around with sirens/alarms, approaching him, sitting with alarms, then leaving.

VTOL code review conclusion:

- No evidence RedFox VTOL Drive creates police, sirens, pursuits, arrests, wanted behavior, or emergency AI.
- Experimental NPC hover can affect existing traffic vehicles if enabled, but should not spawn police or command sirens.
- Treat police/siren issue as likely from another mod, traffic system, career/RLS behavior, or game state.

### F11 World Editor issue / tire removal issue

David reported F11 did not work and tire/rim removal issues.

Prior log review conclusion:

- No evidence RedFox VTOL Drive caused the F11 / World Editor problem.
- Log pointed to RedFox PSI Controller:
  - `redfoxPSIController.lua:1094`
  - `attempt to call global 'spikeStripPopWheel' (a nil value)`
  - `Full wheel/rim detach could not find safe wheel/rim breakGroup`
- Treat tire/rim detach failures as PSI/tire mod issues, not VTOL.

## v58 BeamNG 0.39.4 fatal bug

Confirmed runtime bug from BeamNG 0.39.4 log:

- `RedFox_VTOL_Drive_v58_EBRAKE_START_WARNING_ONLY.zip` auto-loaded `lua/vehicle/extensions/kanderman/skyride.lua`.
- Then `lua/vehicle/extensions/kanderman/skyride/skydros.lua` line around 97 called `pairs()` with nil during `onExtensionLoaded`.
- This caused a FATAL LUA ERROR on every vehicle reload and could trigger generic “Error loading vehicle” popups for unrelated vehicles.

Required patch behavior:

- Guard/initialize collections before any `pairs()` call in `skydros.lua`.
- Guard `loadSkyride.lua` or equivalent loader so Skyride/VTOL does not auto-load on vehicles without the required Skyride data.
- Preserve behavior for configured VTOL vehicles.

Later packages after this were expected to include nil guards in `skydros.lua`, safer `loadSkyride.lua`, and safer `skyride.lua` initialization.

## v70 details — NPC Hover Toggle Test

Package:

`RedFox_VTOL_Drive_v70_NPC_HOVER_TOGGLE_TEST.zip`

Purpose:

- Add an experimental NPC/traffic hover section inside RedFox VTOL Drive.
- Do not split into standalone module yet.

Added UI:

- `NPC / Traffic VTOL Hover`
- `Make NPC / traffic vehicles hover`
- `NPC Hover Height Above Road`
- `NPC Scan Interval`
- `Also affect my current/player vehicle` default OFF
- `Apply NPC Hover Now`

Defaults:

- NPC hover height about 10 ft.
- NPC scan interval about 3 seconds.

Known v70 behavior:

- NPC hover worked but needs mode logic, anti-spin, and path/obstacle awareness.

## NPC / Traffic VTOL planned behavior

Future safer state machine:

- 0–10 ft above ground = Low Hover / Road Follow.
- 10–20 ft = Cruise Hover.
- Above 20 ft with clear space = Flight Mode.
- Ceiling / tunnel / overpass detected = force Low Hover.
- Spinning / unstable = Recovery Hover.

Important rule:

- Road speed should not decide hover vs flight because BeamNG road speeds are inconsistent.
- Use altitude, obstacle clearance, path shape/lookahead, and stability.

Needed future features:

- NPC anti-spin recovery.
- NPC height bands.
- NPC path/lookahead from road/navgraph if possible.
- Slow before sharp corners using path curvature, not speed limits.
- Tunnel/overpass safety using raycasts / ceiling detection.
- Optional future standalone module: `RedFox Traffic VTOL` / `redfox_traffic_vtol`.

## v71 details — Structural Assist Test

Package:

`RedFox_VTOL_Drive_v71_STRUCTURAL_ASSIST_TEST.zip`

Purpose:

- Reduce vehicle self-destruction in hover/flight.
- Use ideas from `liftoff_1.0.0.0.zip` conceptually, without merging that mod directly.

Added / changed:

- Flight Structural Assist.
- Body Lift Share.
- Angular Damping Assist.
- Auto-Level Assist.
- Max Angular Assist.
- High-Speed Structural Extra.
- Metadata/listing cleanup to RedFox VTOL Drive.
- Nil-safe loader/skydros initialization guards from v58 bug.

Concept from Liftoff reference:

- Liftoff uses vehicle-side flight controller and `thrusters.applyAccel(...)` style whole-body acceleration / attitude control.
- Liftoff does not make vehicles invincible and explicitly allows normal crash/deformation.
- Useful concepts: better attitude damping, angular acceleration cap, auto-level, surface-relative hover height, vehicle-switch safety, simpler UI.

Do not directly merge Liftoff:

- Its auto-load path `lua/vehicle/extensions/auto/flightSystem.lua` has the same class of risk as prior auto-load problems if not guarded.

## v72 details — Gravity Relief + Anti-Rock Test

Package:

`RedFox_VTOL_Drive_v72_GRAVITY_RELIEF_ANTI_ROCK_TEST.zip`

Purpose:

- Try making vehicles fly more safely by reducing effective gravity while VTOL is active.
- Add adaptive anti-rock response.

Added:

- VTOL Gravity Relief default ON in v72.
- Gravity Relief Scale default around 0.70.
- Adaptive Anti-Rock.
- Rock Force Soften.
- Rock Body Share Boost.
- Rock Damping Boost.

Result:

- Regressed flight authority for David.
- Thruster/fire visuals seemed absent or weak.
- Switching from hover to flight caused sinking / violent float-down.

Conclusion:

- Gravity Relief should not be default ON.
- Anti-Rock should not cut lift by default.
- Keep the idea only as optional/manual or later retuned feature.

## Dynamic Gravity mod review/fix

Uploaded reference/fix files:

- `dynamicGravity_0_39_4_fixed.zip`
- `dynamicGravity.zip`
- `dynamicGravity gpt.zip`

Observed UI error screenshot:

- Dear ImGui popup: `In window 'Dynamic Gravity v.0.2': Missing End()`

A separate fixed package was produced:

`dynamicGravity_0_39_4_DEAR_IMGUI_GUARD_v2.zip`

Purpose:

- Guard Dear ImGui `Begin/End` so `im.End()` still runs if UI errors.
- Guard gravity/environment calls.
- Fix calculation slider min/max order.
- Keep vehicle gravity behavior unchanged.

Testing note:

- Do not install Dynamic Gravity at the same time as VTOL test builds until VTOL is validated alone.

## v73 details — Heavy Load Stabilizer Test

Package:

`RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST.zip`

Purpose:

- Restore v71-like flight authority.
- Keep structural assist.
- Disable risky v72 defaults.
- Add heavy-load/trailer stabilization for semis, tow trucks, buses, trailers, and long-frame vehicles.

Changed files in v73:

- `mod.json`
- `mod_info/MXFWH19SP/info.json`
- `lua/ge/extensions/redfoxSkyRideUI.lua`
- `lua/vehicle/extensions/kanderman/skyride/flight.lua`
- `RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST_README.txt`

v73 code changes recorded:

- `gravityRelief` default OFF (`0.0`).
- `gravityReliefScale` default set around `0.85` but unused unless Gravity Relief is enabled.
- `rockForceSoften` default set to `0.00` so rocking detection no longer cuts lift by default.
- Added / used:
  - `heavyLoadStabilizer = 1.0`
  - `heavyLoadYawReduction = 0.55`
  - `heavyLoadRollReduction = 0.35`
  - `planeLowSpeedLiftFloor = 0.65`
- Plane mode low-speed lift floor should reduce the hover-to-flight sinking problem.
- During rocking, Heavy Load Stabilizer reduces hard yaw/roll/pitch correction rather than removing lift.

v73 suggested initial settings:

- Gravity Relief: OFF.
- Adaptive Anti-Rock: ON.
- Rock Force Soften: 0.00.
- Heavy Load / Trailer Stabilizer: ON.
- Heavy Load Yaw Reduction: 0.55.
- Heavy Load Roll Reduction: 0.35.
- Plane Low-Speed Lift Floor: 0.65.
- Flight Structural Assist: ON.
- Body Lift Share: 0.35–0.50.
- Angular Damping Assist: 2.25–3.50.

## Semi/trailer issue requiring future work

David tested semi truck with 52-foot trailer in earlier build and observed:

- It could hover and get off the ground.
- Cab, frame, and trailer rocked against each other.
- Cab would go left while trailer went right, repeatedly.
- Oscillation continued until the gas tank ruptured and the vehicle fell from the sky.

Core problem:

- Multi-body / articulated vehicles are not the same as a single rigid car.
- The cab and trailer need to remain level and stable while still allowing turns and trailer articulation.
- Current controller does not truly know about attached trailer bodies/couplers.

Future solution direction:

- Add coupled-vehicle/trailer awareness if BeamNG APIs expose attached trailers safely.
- Detect multiple connected vehicle objects or coupler relationships.
- Stabilize cab and trailer independently but coordinate yaw/roll correction.
- Avoid turning the whole combination into one rigid object; it must still turn.
- Possibly lower yaw/roll correction on trailer combos and increase whole-body lift share.
- Add per-vehicle/preset system: Small Car, Large Truck, Semi/Trailer, Bus, Experimental.

## Road/path/NPC lookahead planning

David asked if NPCs can use mapped roads/AI paths to know what is ahead.

Planned idea:

- Use road/navgraph/path shape if accessible.
- Use curvature/lookahead rather than speed limits.
- Detect upcoming sharp corners.
- Slow/lower hover before sharp turns.
- Add anti-spin if yaw rate exceeds threshold.
- Tunnels/bridges may not be tagged as such, so use raycasts/ceiling detection rather than relying on road metadata labels.

## Structural/invincibility discussion

David wants vehicles not to rip apart while flying.

Current conclusion:

- There is no clean universal “make every BeamNG vehicle one unbreakable object” switch.
- JBeam deformation/breaking can be made tougher per vehicle/part, but universal invincibility is unsafe and not guaranteed.
- Better current approach is controller-side Structural Assist:
  - reduce violent angular acceleration;
  - soften force spikes;
  - share lift through body acceleration;
  - damp yaw/roll/pitch oscillation;
  - landing shield / tire/suspension protection near ground;
  - per-vehicle presets.

Possible later work:

- Optional Flight Structural Assist part or JBeam support for vehicles that support it.
- Do only after controller stability is proven.

## Metadata / naming issue

David showed mod manager still listing:

- `SkyRider Ultimate`
- `Make almost any car fly!`

Needed/partially done:

- Public listing should be `RedFox VTOL Drive`.
- Description should be RedFox-branded, e.g. `RedFox flying vehicle system with hover mode, plane mode, landing assist, shields, presets, and traffic hover tools.`
- Check and update:
  - `mod.json`
  - `mod_info/.../info.json`
  - any visible name/description fields
  - Garage Hub manifest visibleName if present
- Do not delete required author/license credit if original license requires it.

## RedFox Hub / UI laws relevant to this mod

RedFox VTOL Drive must remain standalone and Hub-compatible, not merged into the Hub.

Required module/bridge direction:

- Stable moduleId target: `redfox_vtol_drive`.
- Visible name: `RedFox VTOL Drive`.
- Window ID target: `RedFoxVTOLDrive`.
- Settings path target: `settings/redfox/vtol_drive_settings.json`.
- Open/toggle bridge target: `redfox_vtol_drive.toggleWindow` or equivalent safe bridge.

Required Hub functions eventually:

- `openWindow()`
- `closeWindow()`
- `toggleWindow()`
- `isWindowOpen()`
- `minimizeWindow()`
- `restoreWindow()`
- `openSettingsWindow()`
- `openGameUI()`
- `applyGlobalTheme(themeTable)`
- `applyGlobalFontScale(scale)`
- `applyGlobalButtonScale(scale)`
- `applyGlobalTextColor(color)`
- `applyGlobalButtonTextColor(color)`
- `setUseLocalOverride(enabled)`
- `getModuleStatus()`

Do not work on Hub/accessibility while flight behavior is being repaired unless David explicitly requests it.

## Do-not-regress list

- Do not reintroduce unguarded `pairs(nil)` in `skydros.lua`.
- Do not auto-load Skyride/VTOL on vehicles lacking required data.
- Do not let Gravity Relief default ON again until proven safe.
- Do not let Adaptive Anti-Rock cut lift by default.
- Do not remove NPC hover; David confirmed it worked.
- Do not assume police/sirens are VTOL without logs showing VTOL calls.
- Do not blame VTOL for PSI/tire breakGroup issues unless logs support it.
- Do not claim runtime proof until David tests in BeamNG.

## Recommended next steps

1. David tests v73 alone with no Dynamic Gravity and only one VTOL package installed.
2. If v73 restores flight and improves trailers, tune Heavy Load values only.
3. If v73 still rocks semis/trailers, build v74 with true coupled-vehicle/trailer detection if safe API access is available.
4. If v73 still sinks on hover-to-flight, increase `planeLowSpeedLiftFloor` and inspect plane lift math, not gravity relief.
5. After player flight is stable, return to NPC height bands, anti-spin, road/path lookahead, and optional standalone RedFox Traffic VTOL module.
6. Keep a copy of v71 as known improved baseline for structural assist.
7. Keep a copy of v70 as known NPC hover working baseline.

## Files/builds referenced in this handoff

- `RedFox_VTOL_Drive_v58_EBRAKE_START_WARNING_ONLY.zip`
- `RedFox_VTOL_Drive_v70_NPC_HOVER_TOGGLE_TEST.zip`
- `RedFox_VTOL_Drive_v71_STRUCTURAL_ASSIST_TEST.zip`
- `RedFox_VTOL_Drive_v72_GRAVITY_RELIEF_ANTI_ROCK_TEST.zip`
- `RedFox_VTOL_Drive_v73_HEAVY_LOAD_STABILIZER_TEST.zip`
- `liftoff_1.0.0.0.zip`
- `dynamicGravity_0_39_4_fixed.zip`
- `dynamicGravity.zip`
- `dynamicGravity gpt.zip`
- `dynamicGravity_0_39_4_DEAR_IMGUI_GUARD_v2.zip`

## Current handoff summary for a new chat

Take over RedFox VTOL Drive from v73. David wants flying vehicles to stop ripping themselves apart, especially tow trucks, semis, buses, trailers, and long-frame vehicles. v71 structural assist helped. v72 gravity relief hurt flight. v73 disables gravity relief by default, stops anti-rock from cutting lift by default, and adds heavy-load/trailer stabilizer and plane low-speed lift floor. NPC hover was added in v70 and worked but needs anti-spin, height bands, tunnel/overpass safety, and path lookahead. Police/siren issue is not currently linked to VTOL. F11/tire issues are likely PSI/tire controller, not VTOL. Preserve working flight core, patch one thing at a time, and never claim runtime proof without David testing the exact ZIP.