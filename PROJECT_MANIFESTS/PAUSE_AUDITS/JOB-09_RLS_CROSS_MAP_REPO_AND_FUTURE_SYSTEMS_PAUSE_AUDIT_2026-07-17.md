# JOB-09 — RLS Cross-Map Repo Transport and Future Systems Pause Audit

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Related job:** JOB-09 — Tow / Recovery / Dispatch  
**Status:** **BRAINSTORM / RESEARCH PAUSED while David is camping. This is not a handoff and this work is not implemented in the current Tow ZIP.**

---

## Purpose of this separate audit

This document preserves the cross-mod and future-system discussion without mixing it into the current JOB-09 v0.2.5 runtime claim.

The current Tow mod must be stabilized first.

No cross-map repo-carrier code, AI transport code, business-manager code, or multi-winch overlay code was added after this brainstorming discussion.

---

# Owner direction: keep future systems simple

David rejected a complicated business simulator.

The desired business loop is only:

```text
Buy a property or business.
Convert it to the desired business type.
Hire employees.
Go do other gameplay.
Receive income.
```

Examples of supported future business types:

- Tow yard.
- Scrap yard.
- Store/shop.
- Other simple businesses added later.

Owner rules:

- Any purchased property may be converted, even if it is a small house or an unrealistic site.
- Fun and visible ownership matter more than zoning realism.
- Do not require detailed zoning suitability.
- Do not add permits, taxes, legal paperwork, schedules, skill trees, banking ledgers, or detailed accounting.
- Do not require a manager hierarchy before passive income works.
- Do not block Tow gameplay behind an oversized business setup.

This belongs in a separate future mod/job assigned by JOB-00.

Coordinator request already created:

```text
GitHub issue #5
[JOB-00 ASSIGNMENT REQUEST] Simple Business Manager and future Tow Support controls
```

---

# RLS correction and research result

An earlier statement treated BeamNG maps as unrelated isolated worlds and suggested only simulating the cross-map trip.

David correctly rejected that statement because RLS Career Overhaul provides a continuing multi-map Career system.

Correct RLS behavior established from official source inspection:

1. Compatible maps register with RLS through the map system.
2. A Map Switcher trigger opens the level-switch UI.
3. The player chooses another compatible installed map.
4. RLS saves the active Career.
5. RLS loads the selected map.
6. The same Career save and Career modules resume on the destination map.
7. The active map is stored in the Career save.

Therefore, the planned repo-carrier system should use the real RLS map-switch workflow rather than merely pretending the load travelled elsewhere.

---

## Official RLS source files inspected

Research used the public RLS Career Overhaul repository source around commit:

```text
e31433e5c2ed6e4780ac1d0daf94f9780669f47d
```

Important inspected files:

```text
lua/ge/extensions/overhaul/maps.lua
lua/ge/extensions/career/modules/switchMap.lua
lua/ge/extensions/overrides/career/career.lua
ui-vue-src/modules/career/views/LevelSwitch.vue
levels/west_coast_usa/main/MissionGroup/RLS_EDITS/MapSwitcher/items.level.json
lua/ge/extensions/gameplay/repo.lua
ui-vue-src/modules/career/views/PhoneRepo.vue
lua/ge/extensions/overrides/career/modules/inventory.lua
lua/ge/extensions/overrides/career/modules/delivery/general.lua
```

What those files establish:

- `overhaul/maps.lua` maintains compatible maps and receives map registrations.
- `switchMap.lua` finds map-switch triggers and calls Career level switching.
- `LevelSwitch.vue` lists compatible destination maps and starts travel.
- `career.lua` saves before switching and resumes Career after loading.
- `repo.lua` generates current RLS repossession jobs and pays/deletes the delivered target.
- `inventory.lua` saves vehicle configuration, `partConditions`, and spawned-player-vehicle transforms.
- `delivery/general.lua` maintains persistent logistics state and game time.

Important version rule:

- Public online RLS source may be newer than David's installed ZIP.
- The last exact project reference was RLS Career Overhaul 2.6.6.
- Public information later indicated 2.6.7.
- Before implementation, inspect David's exact installed RLS ZIP and do not assume online source is byte-for-byte identical.

---

# Current RLS repossession behavior

The inspected RLS repo module currently:

1. Requires a configured RLS repo vehicle.
2. Chooses a random eligible target.
3. Spawns the target at a reservable parking spot.
4. Chooses an eligible dealership destination.
5. Routes the player to the target and dealership.
6. Tracks distance/time/value.
7. Pays the player after delivery.
8. Deletes the delivered repo target.
9. Records repossession progression/statistics.

This current one-vehicle-to-dealership loop is the foundation David wants to expand.

Do not edit RLS's original `repo.lua` directly for the RedFox project. A RedFox compatibility/provider layer should extend or consume public behavior without replacing RLS source.

---

# Proposed RedFox repo-chain gameplay

## Local repossession stage

Instead of every recovered vehicle disappearing immediately at a dealership:

1. Accept an RLS/RedFox repossession call.
2. Recover the target vehicle.
3. Deliver it to the player's local RedFox tow/repo yard on the current map.
4. Add it to a persistent **Repossession Holding** catalog.
5. Keep its vehicle identity, condition, and destination contract information.

Possible holding states:

```text
Awaiting local pickup
Recovered to local yard
Ready for bulk transport
Loaded on carrier
In cross-map transit
Arrived at destination map
Delivered to lender/dealership/auction
Failed or damaged shipment
```

---

## Bulk transport trigger

After accumulating a configured batch such as:

```text
5 vehicles
8 vehicles
10 vehicles
```

The player can create a bulk transport shipment.

Potential destinations:

- West Coast dealership/lender yard.
- East Coast compatible destination.
- Italy destination.
- Another RLS-compatible map.
- Auction yard.
- Copart-style salvage destination.
- Semi yard.
- Import/export terminal.

The shipment should be a real persistent Career task rather than a temporary freeroam visual.

---

## Player transport workflow

Desired player-driven loop:

1. Select repo vehicles from holding inventory.
2. Load them physically onto a car carrier.
3. Secure the vehicles.
4. Drive the loaded tractor/trailer to the RLS Map Switcher.
5. Choose the destination map through the normal RLS interface.
6. Preserve the shipment across the map transition.
7. Resume with the loaded carrier on the destination map.
8. Drive to the destination yard/dealership/auction.
9. Unload or complete the marked delivery.
10. Receive payment.
11. Return the carrier to the player's fleet/storage.

This is expected to make useful video content and give individual repo missions a larger purpose.

---

# Damage, vehicle, trailer, and cargo persistence research

David pointed out that current Career/RLS vehicle selection already saves damage states.

The inspected RLS inventory source confirms that inventory vehicle files load a serialized:

```text
partConditions
```

The inventory save also stores a table of:

```text
spawnedPlayerVehicles
```

with saved transforms/locations for spawned inventory vehicles.

This means RLS may already preserve much of the needed data for:

- Tractor identity.
- Trailer identity.
- Loaded repo-car identity.
- Model/configuration.
- Paint/configuration.
- Individual vehicle damage/part conditions.
- Saved world position and rotation.

The unresolved question is whether it preserves the **relationships** between the vehicles:

- Tractor-to-trailer coupling.
- Car-to-carrier securement.
- Node/coupler relationships.
- Deck/ramp position.
- Relative transforms as one connected shipment.
- Multiple inventory vehicles restored as a connected group.

No claim has been made that couplers or loaded cargo survive until David performs the runtime test.

---

# Required native RLS persistence test

This test should happen before any shipment reconstruction code is written.

## Test setup

Use:

- One inventory tractor.
- One inventory car-carrier trailer.
- One damaged inventory car.

Load and secure the car as normally as possible.

## Test A — same-map save/reload

1. Save Career with the loaded carrier present.
2. Return to menu or reload the same Career/map.
3. Check all objects and relationships.

Record:

- Did all three vehicles return?
- Did the damaged car retain damage?
- Did the tractor retain damage/configuration/paint?
- Did the trailer retain configuration/paint?
- Is the tractor still coupled to the trailer?
- Is the car still secured?
- Are positions and rotations correct?
- Did any object shift, drop, explode, or spawn separately?

## Test B — RLS map switch

1. Start with the loaded carrier on River Highway or another compatible map.
2. Use the normal RLS Map Switcher.
3. Select a destination map.
4. Check the same points after the destination loads.

## Test C — full game restart

1. Save after loading/arriving.
2. Exit BeamNG completely.
3. Restart BeamNG.
4. Load the same Career.
5. Check the same points again.

Evidence needed:

- Before/after screenshots.
- Exact maps used.
- Whether each vehicle was owned/in inventory.
- Coupler/securement method used.
- `beamng.log` around save, switch, and load.

---

# Implementation decision tree after testing

## Result 1 — all vehicles and couplers survive

Use RLS native persistence as much as possible.

RedFox only needs to save:

- Shipment ID.
- Selected repo records.
- Origin/destination.
- Contract and reward.
- Completion state.

Avoid rebuilding what RLS already handles.

---

## Result 2 — damage and vehicle transforms survive, but couplers do not

Use RLS vehicle/inventory persistence plus a RedFox shipment manifest.

Manifest should store:

- Tractor inventory ID.
- Trailer inventory ID.
- Cargo vehicle inventory IDs.
- Tractor/trailer model and config fallback.
- Each vehicle's part/damage state reference.
- Trailer-relative position and rotation for every loaded car.
- Intended coupler/securement relationships.
- Deck/slot identifier where possible.
- Destination map and destination facility.

After load:

1. Spawn/fetch tractor and trailer.
2. Freeze them.
3. Restore trailer coupling.
4. Spawn/fetch cargo vehicles.
5. Restore relative placement.
6. Restore supported securement/couplers.
7. Settle physics.
8. Unfreeze in a controlled order.

---

## Result 3 — inventory vehicles survive but exact world placement does not

Use a shipment manifest and a predefined destination-map staging point.

Reconstruct the entire load near the map entry point.

Do not assume old world coordinates have meaning on the destination map.

---

## Result 4 — some shipment vehicles disappear unless separately stored

Before map switching:

- Ensure tractor, trailer, and cargo vehicles are valid inventory records.
- Record all inventory IDs.
- Mark them unavailable/in transit so they cannot be duplicated or sold.
- Reconstruct them from inventory at destination.

---

## Result 5 — loaded physics becomes unstable during load

Use the static/frozen staging approach discussed by David.

---

# Static/frozen shipment staging concept

David proposed scanning the loaded truck and cargo and making them static until the destination map finishes loading, then swapping to dynamic vehicles.

This is a strong fallback/stability design.

## Before map switch

Scan/save:

- Tractor.
- Trailer.
- Every cargo vehicle.
- Models and exact configurations.
- Fleet names/call signs/paint records.
- Vehicle/inventory IDs.
- Damage/part-condition records.
- Tractor-to-trailer relationship.
- Vehicle-to-trailer relative transforms.
- Securement/coupler relationship.
- Shipment origin and destination.

Then:

- Freeze the physical group or convert it to a shipment record.
- Save Career through the RLS map-switch workflow.

## Destination-map load

Possible sequence:

1. Create a lightweight static/frozen representation of the loaded carrier at the destination entry/staging area.
2. Allow map assets, road graph, and Career modules to finish loading.
3. Spawn/fetch the real tractor and trailer frozen.
4. Disable or limit collisions during assembly.
5. Restore the tractor/trailer coupling.
6. Spawn/fetch each cargo vehicle frozen.
7. Restore each relative position and rotation.
8. Restore supported securement/couplers.
9. Wait briefly for all vehicles to settle.
10. Remove the placeholder/static representation.
11. Re-enable collisions in a controlled sequence.
12. Unfreeze trailer/cargo/tractor in a safe order.
13. Return player control.

The static representation could be:

- A simplified visual placeholder.
- A frozen group of actual vehicles.
- A temporary preview object if a safe model can be produced.

Do not build a new static mesh-generation pipeline unless needed. First test whether frozen real vehicles are sufficient.

---

## Distance-based static storage idea

A later optimization could keep stored shipments static/frozen while the player is far away.

Example:

- Shipment arrives at a destination yard while the player is elsewhere.
- It exists as a lightweight yard record or static representation.
- Approaching it or selecting **Resume Shipment** swaps it to live vehicles.
- Leaving/storing it converts it back to a lightweight record.

This could reduce physics load with 5–10 loaded vehicles.

This is a later optimization, not a current requirement.

---

# Damage-state expectations

Likely preservable through inventory/part conditions:

- Part condition.
- Mechanical damage state.
- Missing/broken parts represented in saved condition.
- Paint/configuration.
- Mileage/fuel where supported.
- Repair/value state.

Still uncertain:

- Exact node-by-node deformation.
- Exact bent body geometry after full reconstruction.
- Exact beam breaks not represented in `partConditions`.
- Exact coupler state.

Because David states the vehicle-selection screen can save damage states, the first approach should be to reuse that native mechanism rather than invent a replacement damage format.

---

# Future AI tow transport direction

David does not want the AI to perform the complicated recovery setup.

Player responsibilities:

- Hook up the trailer.
- Load the vehicle.
- Secure the cargo.
- Operate the winch.
- Perform recovery/rigging.

AI responsibility:

- Drive the already-secured load toward the chosen yard.
- Follow road navigation.
- Get as close as it safely can.
- Stop at the closest reachable roadside point when the exact yard is off-navgraph.
- Pull to the side where possible.
- Wait with hazard lights and tow/beacon lights.
- Allow the player to finish backing, parking, or unloading.

Desired commands:

```text
Follow Me
Wait Here
Take Load to Yard 1
Take Trailer to Semi Yard
Return to Base
```

Future implementation phases:

1. Follow/wait/stage behavior.
2. Drive an already-secured load to a reachable point.
3. Yard approach and safe roadside waiting.
4. Optional simple backing attempt.
5. Stuck/failure handling and player takeover.

Not the first target:

- Automatic winch hookup.
- Automatic wheel-lift placement.
- Automatic flatbed loading.
- Automatic rotator rigging.
- Universal self-recovery AI.

Current status:

```text
PLANNED / COORDINATOR ASSIGNMENT REQUESTED
NOT IMPLEMENTED IN v0.2.5
```

---

# Future multi-wrecker manual overlay

David's desired approach is not autonomous multi-truck recovery.

The player should control multiple winches manually from one overlay.

Potential overlay contents per participating truck:

- Unit name/call sign.
- Truck role.
- Winch list.
- Cable tension/length if exposed.
- Winch in.
- Winch out.
- Hold.
- Release.
- Select active truck.
- Parking brake/anchor status if safely exposed.

This would allow:

- Two wreckers pulling from different angles.
- Player remaining in one camera or vehicle context.
- Coordinated manual rollover recovery.

Current status:

```text
PLANNED / COORDINATOR ASSIGNMENT REQUESTED
NOT IMPLEMENTED
```

---

# Future police and traffic-control scene integration

Desired scene support:

- Police vehicle upstream as a blocker.
- Fire or emergency vehicle shielding the work area.
- Cones/barrels creating a taper.
- Closed lane or full road closure.
- Slow traffic through an open lane.
- Clear tow staging and recovery buffer.
- Debris and cleanup details.

Current JOB-09 support:

- Map-aware road/intersection/curve selection in v0.2.5.
- Scene-provider API.
- Event-library function probe.

Still needed:

- Exact random-event/public API evidence.
- Safe traffic stop/diversion behavior.
- Police blocker and prop provider.
- Cleanup/removal behavior when the call ends.

Required evidence from v0.2.5 test:

```text
[RedFox][TOW][EVENT_LIBRARY] ...
```

Do not call undocumented event functions until that evidence or the exact source archive is available.

---

# Map-aware accident-placement direction

Already added to v0.2.5:

- Intersection detection.
- Sharp-curve detection.
- Steep-grade detection.
- T-bone plan.
- Curve-rollover plan.

Future semantic scene ideas:

- Sharp curve → semi rollover.
- T-intersection → T-bone accident.
- Wide multi-branch intersection → multi-vehicle collision.
- Steep downhill → brake-failure recovery.
- Long wide segment → semi/trailer jackknife.
- Shoulder/ditch → abandoned or off-road recovery.
- Bridge/tunnel/limited-width road → special closure/recovery restrictions.

All are best-effort because custom-map road data varies.

---

# Simple Business Manager coordination

This future system is separate from JOB-09.

Required minimal state:

- Property ID/location.
- Purchased/not purchased.
- Converted business type.
- Employees hired.
- Passive income timer/rate.
- Link to the relevant business mod.

For Tow:

- Convert purchased property to Tow Yard.
- JOB-09 registers it as a destination.
- Hire dispatcher/driver later through the simple employee list.
- Receive basic passive earnings when employees complete simulated work.

Explicitly excluded:

- Detailed zoning checks.
- Permits.
- Bond/legal simulation as mandatory gameplay.
- Tax returns.
- Separate business bank accounts.
- Complex payroll schedules.
- Employee skill trees.
- Detailed profit/loss accounting.
- Property-size rejection.

A small house may become a tow yard because David prioritizes fun and visible ownership.

---

# Cross-job coordination boundaries

## JOB-00

Should assign ownership for:

- Simple Business Manager.
- General employee/passive-income system.
- AI transport framework if shared by multiple businesses.
- Multi-vehicle control framework if shared.

## JOB-02

Should provide approved RLS/Career bridge contracts when cross-mod persistent state or payment actions are needed.

JOB-09 must not patch RLS internals directly.

## JOB-04

Owns Scrap Yard receiving/scrapping behavior.

JOB-09 may send vehicles to a verified Scrap Yard destination but must not implement Scrap Yard's own backend.

## JOB-08

Owns insurance/finance/garage/storage pages.

The simple business system may query policy state later, but detailed policy administration is not part of JOB-09.

## JOB-01

Owns final phone/PC access and shared route registration.

The standalone Tow backend should remain usable before that integration.

---

# External compatibility/research ideas

## Used Car Generator

Possible future optional condition provider for:

- Abandoned repo vehicles.
- Worn/neglected vehicles.
- Dead batteries.
- Mechanical failures.
- Flat tires.

Do not bundle its source or assets.

## Police Behaviour

Behavior reference for roadblock/police responses.

Do not copy source/assets without permission and compatibility review.

## Post Crash Extras

Behavior reference for crash aftermath such as horns or engine shutdown.

## Universal Vehicle Failures

Behavior reference for future breakdown calls.

## Random event systems

Potential provider for:

- Police blockers.
- Cones/barrels.
- Emergency vehicles.
- Debris.
- Prebuilt crash compositions.

Exact adapter remains blocked on API/source evidence.

---

# What is implemented versus brainstorm only

## Implemented in current v0.2.5

- Standalone Tow call system.
- Five call types.
- Road/roadside scenes.
- Mixed vehicle scenes.
- Map-aware intersections/curves/grades.
- T-bone and curve-rollover plans.
- Tow yards.
- Impound records.
- Cataloged history.
- Tow Fleet Book identity/paint records.
- Scene-provider API.
- Event-library probe.

## Researched/planned but not implemented

- RLS repo vehicle holding inventory.
- Batches of 5/8/10 repo vehicles.
- Car-carrier bulk jobs.
- Cross-map shipment persistence.
- Static/frozen destination reconstruction.
- Native coupler/cargo persistence adapter.
- AI Take Load to Yard commands.
- Dispatcher employee.
- Passive tow-company work.
- Multi-wrecker manual winch overlay.
- Simple Business Manager.
- Police/road-closure provider.
- Used Car Generator condition provider.

---

# Resume order for cross-mod work

Do not begin here first.

Required order after camping:

1. Test JOB-09 v0.2.5.
2. Fix current Tow runtime failures.
3. Obtain SITE_SCAN and EVENT_LIBRARY evidence.
4. Confirm Fleet Book/history/scene stability.
5. Run the native RLS tractor/trailer/damaged-car persistence test.
6. Record whether couplers and loaded cargo survive same-map reload, map switch, and full restart.
7. Inspect David's exact installed RLS ZIP/version.
8. Decide whether native persistence is enough or a shipment manifest is required.
9. Build a tiny proof-of-concept with one tractor, one trailer, and one car before 5–10 vehicle loads.
10. Only after that, design the full repo holding and bulk transport loop.

---

# Hard rules on resume

```text
This is brainstorming/research, not a current runtime feature.
This is a pause, not a handoff.
Do not patch RLS original source files directly.
Inspect David's exact installed RLS ZIP before implementation.
Test native save/map-switch behavior before building reconstruction code.
Use existing partConditions/damage persistence where possible.
Do not promise exact coupler persistence before testing.
Do not promise exact node-by-node deformation restoration.
Keep Business Manager simple.
Player rigs and hooks; AI only drives the secured load.
Current Tow v0.2.5 stabilization comes first.
```
