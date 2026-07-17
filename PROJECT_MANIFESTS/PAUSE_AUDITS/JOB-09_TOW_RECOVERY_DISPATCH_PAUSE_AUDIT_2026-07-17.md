# JOB-09 — Tow / Recovery / Dispatch Camping Pause Audit

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Chat role:** JOB-09 regular-chat workstation / Sol  
**Status:** **PAUSED while David is camping. This is not a handoff. Resume this same JOB-09 chat when David returns.**

---

## Sound off

This chat is and remains:

```text
JOB-09 — Tow / Recovery / Dispatch
```

Permanent module identity:

```text
redfox_tow_recovery_dispatch
```

Visible title:

```text
RedFox Tow & Recovery Dispatch
```

Primary repository:

```text
redfoxtrystman/RedFox_Master_Control
```

Primary coordination issue:

```text
GitHub issue #4 — JOB-09 Tow / Recovery / Dispatch
```

This pause does **not** transfer ownership, rename the job, merge it into another job, or authorize another chat to replace completed work.

---

## JOB-09 ownership boundary

JOB-09 owns:

- Tow and recovery call generation.
- Abandoned vehicle recovery.
- Standard vehicle towing.
- Rolled-car recovery.
- Semi and trailer rollover recovery.
- Multi-vehicle accident cleanup.
- Roadway and roadside crash-scene generation.
- Tow-yard placement, routing, and multiple-yard records.
- Tow-yard impound and abandoned-vehicle records.
- Tow History Book and Tow Fleet Book.
- JOB-09-specific save data, settings, logs, reports, and compatibility hooks.
- Future tow-specific AI transport commands after the current standalone mod is stable.
- Future tow-specific manual multi-wrecker/winch controls after assignment and planning.

JOB-09 does **not** own:

- JOB-00 Coordinator / Integration / Verification.
- JOB-01 Phone + PC Platform Core.
- JOB-02 Shared RLS / Career Bridge.
- JOB-03 App Store.
- JOB-04 Scrap Yard / Wrecking Yard.
- JOB-05 BeamBook Marketplace.
- JOB-06 Import / Export Yard.
- JOB-07 Classics / Collector Exchange.
- JOB-08 Insurance / Finance / Garage / Storage pages.
- JOB-10 global visual design.
- JOB-11 shared QA/logging core.
- JOB-12 SponsorHub / FoxMail / FoxText / rewards.
- A full general-purpose business-management system.
- Direct edits to stock BeamNG Career or RLS Career Overhaul source files.

---

## David's current direction

The current owner direction is:

1. Finish and stabilize the **standalone Tow / Recovery mod first**.
2. Make it usable for small test videos before waiting for the final IceFox/FoxNet website.
3. Focus on reliable missions, believable scenes, tow yards, fleet names, fleet paint records, and history.
4. Keep future business gameplay simple and separate.
5. Do not turn this into a permits, tax, accounting, zoning, employee-schedule, or legal-compliance simulator.
6. Do not add unfinished AI towing or autonomous winching into the current video-test build.
7. Do not guess undocumented RLS or random-event APIs.
8. Preserve completed work unless runtime testing proves it broken.

The latest discussion after v0.2.5 was brainstorming only. No new Tow mod code was changed after v0.2.5 for the cross-map repo-carrier idea.

---

# Current active JOB-09 build

## Exact candidate

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
```

Current chat/container path:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
```

Identity:

```text
Size: 95,645 bytes
SHA-256: 52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
Source baseline: v0.2.4 Cataloged History
Status: BUILT — RUNTIME UNTESTED
```

Static checks completed before release:

- ZIP integrity: PASS.
- Packaged JSON parse: PASS.
- Lua syntax: PASS through `texlua loadfile`.
- Lua main-chunk local-variable limit: PASS.
- Protected Career/shared-platform path scan: PASS.
- Required scope, verification, inventory, file-tree, logging, and testing reports: PRESENT.

Important:

- The actual installable ZIP exists in this chat/container.
- The installable binary ZIP was **not** uploaded into the GitHub repository.
- GitHub contains handoffs, source-change summaries, research, issue comments, and this pause audit.
- Do not claim v0.2.5 is working in BeamNG until David tests this exact ZIP.

---

## Packaged v0.2.5 source and report tree

Core runtime files:

```text
scripts/redfox_tow_recovery_dispatch/modScript.lua
mod_info/redfox_tow_recovery_dispatch/info.json
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/core/input/actions/redfox_tow_recovery_dispatch.json
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
```

Main player-facing documents:

```text
README.md
CHANGELOG.md
TESTING_CHECKLIST.md
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
```

Mandatory v0.2.5 audit/report files:

```text
CHANGE_SCOPE_JOB09_v0_2_5.txt
OPEN_THIS_VERIFICATION_REPORT_JOB09_v0_2_5.txt
OPEN_THIS_VERIFICATION_REPORT_JOB09_v0_2_5.html
VERIFY_JOB09_v0_2_5.json
VERIFY_JOB09_v0_2_5_FILE_INVENTORY.csv
FILE_TREE_JOB09_v0_2_5.txt
```

Development/research records packaged in the ZIP:

```text
_redfox_dev_notes/PATCH_v0_2_1_TO_v0_2_3.diff
_redfox_dev_notes/REAL_WORLD_SCENE_DESIGN_REFERENCE_v0_2_3.md
_redfox_dev_notes/PATCH_v0_2_3_TO_v0_2_4.diff
_redfox_dev_notes/MAP_HAZARD_AI_PAINT_RESEARCH_v0_2_5.md
_redfox_dev_notes/PATCH_v0_2_4_TO_v0_2_5.diff
```

---

# Current mod behavior in full

## 1. Standalone Career-safe structure

The mod is a standalone GE Lua extension.

Rules preserved:

- No replacement of stock Career files.
- No direct overwrite of RLS Career Overhaul files.
- No duplicate phone or PC shell.
- No custom fake Career save system.
- No fake money, garage, or ownership claims.
- Career rewards are queued through available Career payment systems when present.
- Freeroam use is developer-gated rather than silently pretending Career state exists.

---

## 2. Call generation and call chooser

Current enabled job types:

```text
abandoned
  Abandoned Vehicle Recovery

tow_car
  Standard Car Tow

recovery_car
  Roadside Rolled-Vehicle Recovery

recovery_semi
  Semi / Trailer Rollover Recovery

accident
  Roadway Accident Scene Cleanup
```

The player can:

- Receive scheduled random calls.
- Enable or disable each call type.
- Manually request specific call types.
- Accept or decline an offered call.
- Adjust call intervals and offer lifetime.
- Automatically open the Tow window when a call arrives.

Default scheduling values in v0.2.5:

```text
Minimum call interval: 300 seconds
Maximum call interval: 540 seconds
Offer lifetime: 120 seconds
Auto-open on call: enabled
```

---

## 3. Tow yards

The current mod supports:

- Placing a tow yard at the player's current location.
- Multiple persistent tow yards per map.
- Moving an existing yard.
- Naming/selecting yard records through the current UI.
- Navigating to a selected yard.
- Choosing the closest usable yard for yard-bound calls.
- Retrieving stored yard vehicles into a world slot.
- Returning yard-spawned vehicles when the level/session ends.
- Per-Career-profile yard records.

Default yard capacity:

```text
20 stored records
```

Current design note:

- Testing yards are manually placed and do not yet require property purchase.
- Future property-to-tow-yard conversion belongs to a separate simple business/property system and must not block current Tow testing.

---

## 4. Roadway and roadside crash scenes

v0.2.3 corrected the earlier parking-lot direction.

Current road-scene rules:

- Accident, rolled-car, and semi-rollover scenes use road-graph anchors.
- Scenes may use travel lanes, shoulders, roadside offsets, curves, or intersections.
- Mixed vehicle classes remain valid.
- Passenger cars, semis, trailers, buses, heavy wreckers, and rotators may appear where the selected plan can support them.
- Directional impact velocity creates fresh crash damage.
- Road width and usable segment length are considered.
- A clear error is returned when no suitable road segment is available.

Current procedural accident plans inherited from v0.2.3:

```text
two_vehicle_lane_collision
three_vehicle_chain
shoulder_secondary_collision
semi_trailer_jackknife
shoulder_semi_trailer_collision
heavy_cross_lane
bus_multi_vehicle
```

Added in v0.2.5:

```text
intersection_tbone
sharp_curve_rollover
```

Real-world scene-design rules recorded for future scene refinement:

- Minor movable crashes may be moved to a shoulder.
- Larger incidents may block one or more lanes.
- Police/fire vehicles should shield the work area.
- A clear buffer and tow access corridor should remain.
- Cones/barrels/tapers are more useful than lights alone.
- Major incidents can justify a full road closure.

---

## 5. Map-aware hazard-site classification

v0.2.5 scans the current map navigation/road graph and catalogs:

```text
ordinary road segments
intersections
sharp curves
steep grades
```

Current heuristic uses available road-graph information such as:

- Node positions.
- Road direction.
- Connectivity/branch count.
- Direction change through a node.
- Width.
- Segment length.
- Elevation change and estimated grade.

Current uses:

- Intersections can be preferred for T-bone scenes.
- Sharp curves can be preferred for rollover/secondary-impact scenes.
- Steep grades are recorded for future brake-failure and hill-recovery jobs.
- Ordinary road scenes remain fallback behavior.

Diagnostic log line:

```text
[RedFox][TOW][SITE_SCAN] level=... roadSegments=... intersections=... sharpCurves=... steepGrades=...
```

Known limitation:

- Map navigation quality varies.
- Some custom maps may have incomplete or unusual navgraph data.
- Semantic site selection has not yet been tested across David's installed map set.

---

## 6. Realistic procedural vehicle paints

v0.2.5 adds weighted realistic paint selection for procedurally spawned scene vehicles.

The default palette favors common road colors such as:

- White.
- Black.
- Gray.
- Silver.
- Blue.
- Red.

Less common colors remain possible at lower weight.

The system stores or applies PBR-style paint values including:

- Base color.
- Metallic value.
- Roughness.
- Clear coat.
- Clear-coat roughness.

Setting:

```text
Realistic Weighted Scene Paints: enabled by default
```

It can be disabled without disabling call generation.

---

## 7. Tow Fleet Book

v0.2.5 adds a Tow Fleet Book.

Workflow:

1. Configure a tow truck in BeamNG.
2. Paint it in BeamNG.
3. Enter that truck.
4. Register the current vehicle in Tow Fleet Book.

Each fleet record stores:

- Player-editable unit name.
- Automatic call sign.
- Fleet role.
- Vehicle model.
- Exact part configuration.
- Three captured paint palettes.
- PBR paint values.
- Map and time of capture.

Available roles:

```text
Light-Duty Tow
Flatbed / Rollback
Heavy Wrecker
Rotator
Support / Service
```

Current Fleet Book actions:

- Register current vehicle.
- Rename selected unit.
- Cycle/change selected role.
- Update selected record from the current configured/painted vehicle.
- Remove the Fleet Book record without deleting the real vehicle.

Explicit current limitation:

- Fleet records do not yet spawn trucks.
- Fleet records do not hire drivers.
- Fleet records do not make a truck drive automatically.
- Fleet records currently provide identity/configuration/paint persistence only.

---

## 8. Tow History Book

v0.2.4 replaced the single flat history list with catalogs.

Current catalogs:

```text
All Records
Abandoned Vehicles
Accident Scenes
Rollovers / Recovery
Standard Tows
Impound / Unpaid
Paid / Released
Cancelled
```

A record can appear under both its call category and its outcome category.

Examples:

- An abandoned vehicle placed on hold can appear under **Abandoned Vehicles** and **Impound / Unpaid**.
- A paid accident scene can appear under **Accident Scenes** and **Paid / Released**.

Existing older history records are categorized dynamically and are not rewritten or deleted.

Newer history details include:

- Primary catalog.
- Outcome.
- All recorded scene vehicles.
- Map.
- Scene source.
- Scene site.
- Scene plan.
- Payer.
- Quoted amount.
- Paid amount.
- Outbound distance.
- Tow distance.
- Destination.

Current limits:

```text
Up to 500 history records per Career profile
Newest 20 matching records shown per selected catalog
```

---

## 9. Impound, abandoned storage, and disposition

Current default settings:

```text
Default impound hold: 3 real-time days
Daily storage rate: $75
Hold adjustment range in UI: 1 to 30 real-time days
Storage-rate adjustment: $0 to $1,000 per day in $25 steps
```

Current record fields include:

- Vehicle model/configuration/name.
- Estimated/market value.
- Stored time.
- Legal status.
- Hold days.
- Eligible disposition time.
- Tow lien.
- Daily storage rate.
- Yard identifier.
- Source/reason.
- Asking-price mode/manual price.

Current abandoned-vehicle flow:

- Deliver to yard.
- Enter a decision phase.
- Choose to place it on abandoned-vehicle hold or use immediate salvage sale.

Current unpaid normal tow flow:

- The vehicle is automatically placed into an impound/lien record.
- Storage charges accrue.
- The job records an unpaid outcome.

David discussed a future setting direction:

- Hold enabled by default.
- Adjustable/override hold time.
- Optional immediate disposition override for abandoned vehicles.

That additional polished setting workflow is **not implemented** beyond the current test controls. David later said the existing behavior is acceptable for now and should remain a future option rather than blocking current testing.

Important time limitation:

- The current hold uses `os.time()` and real elapsed days.
- It does not yet use a confirmed shared RLS in-game calendar.

---

## 10. Scene templates and scene-provider integration

The mod can capture the current generated target layout before towing begins.

Captured templates store target-relative placement and can be reused for matching call types.

Current scene selection settings:

```text
Scene mode: Prefer Saved
Saved matching scene weight: 0.80
Random/event provider weight: 0.35
Roadside scene chance: 0.38
```

Current public provider API:

```text
registerSceneProvider(providerId, callback, priority)
unregisterSceneProvider(providerId)
getSceneProviderContract()
```

Provider request data can include:

- Event type.
- Level/map.
- Site position and rotation.
- Road direction and cross-road direction.
- Road width/length.
- Site type.
- Intersection branch count.
- Curve deflection.
- Grade.
- Road/shoulder preference.
- Police-line preference.

Provider response can include:

- Scene name.
- Target models/configurations.
- Relative positions/rotations.
- Semi/trailer flags.
- Support vehicle IDs.

Random-event evidence probe:

```text
gameplay_events_freeroamEvents
```

Required log line:

```text
[RedFox][TOW][EVENT_LIBRARY] ...
```

Current limitation:

- The mod only probes/logs public function names.
- It does not guess or call undocumented random-event functions.
- A real adapter must wait for the complete log line or exact event source archive.

---

## 11. Routing and destination providers

Current behavior includes:

- Route to pickup.
- Route refresh if the marker/path is lost.
- Route to the required dropoff or nearest tow yard.
- Destination provider registration for future integration.
- Distance tracking for history/payment calculations.

Current destination API:

```text
registerDestinationProvider(providerId, callback)
unregisterDestinationProvider(providerId)
```

Potential future consumers:

- Scrap Yard.
- Auction yard.
- Semi yard.
- Insurance storage.
- RLS dealership/lender destination.

Those destination integrations are not yet implemented in v0.2.5.

---

## 12. UI and accessibility

Current UI includes:

- Main Tow/Recovery window.
- Settings window.
- Readable UI preset by default.
- Multiple size presets from Tiny through Huge.
- Theme selection.
- Garage Hub theme-following support.
- Adjustable font, button, padding, background opacity, and text modes.
- Persistent window layout/settings files.

Current local settings/save paths:

```text
settings/redfox/tow_recovery_dispatch_settings.json
settings/redfox/tow_recovery_dispatch_ui_layout.json
settings/redfox/tow_recovery_dispatch_yard.json
settings/redfox/tow_recovery_dispatch_scenes.json
```

---

# Runtime evidence completed so far

## Confirmed from David's testing of an older candidate

David reported after doing several missions on the then-current build:

- No computer crash during those missions.
- An Abandoned Vehicle Recovery could be completed.
- The returned vehicle appeared in the yard/impound interface.
- The Impound hold display appeared.
- Storage/lien values displayed.
- Tow History records appeared in the older flat list.

This is useful partial evidence for the inherited core, but it does **not** certify v0.2.4 or v0.2.5.

The exact build in that report was from the v0.2.3-era test sequence before the current v0.2.4/v0.2.5 changes.

## v0.2.4 runtime status

```text
BUILT — RUNTIME UNTESTED
```

Cataloged history was not yet confirmed in BeamNG before v0.2.5 replaced it as the active candidate.

## v0.2.5 runtime status

```text
BUILT — RUNTIME UNTESTED
```

No runtime claim is authorized yet for:

- Tow Fleet Book persistence.
- Fleet paint capture.
- Intersection scene selection.
- Sharp-curve scene selection.
- Site-scan counts.
- v0.2.4 history migration inside v0.2.5.
- v0.2.5 scene paints.
- v0.2.5 map-by-map stability.

---

# Version history and decisions

## v0.1.0 — Foundation Prototype

Added:

- Standalone Career-safe dispatch foundation.
- Abandoned vehicles.
- Yard ledger.
- Random calls.
- Career payments.
- Native Tow UI.

Status:

- Superseded by later builds.

---

## v0.2.0 — Call Chooser and Player Tow Yard

File:

```text
19-RedFox_TowRecoveryDispatch_v0_2_0_CallChooserYard.zip
```

SHA-256:

```text
217bc62ef0573feb888cf630c4d002fa49996a2fc0aa1cddc06a58e2720cc9ea
```

Added:

- Manual call types.
- Semi recovery.
- Per-map yard.
- Retrieval slots.
- Heavy-recovery pay.

Status:

- Superseded.

---

## v0.2.1 — Rollover Scenes and Multiple Yards

File:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_1_RolloverScenesMultiYard.zip
```

SHA-256:

```text
357c44f4494f7199071282ef3ec7e8e0a2f747ee19c8a12b25ed40da9e0ae2b1
```

Added:

- Delayed crash transforms.
- Scene-layout capture.
- Route recovery.
- Response mileage.
- Multiple yards.
- Unpaid impounds.
- Tow History Book.
- Expanded UI settings.

Runtime failure found:

- A multi-vehicle accident generated an impossible compact parking-lot scene containing a long semi trailer and another vehicle.
- The core problem was scene location/footprint, not the fact that heavy vehicles existed.

Status:

- Superseded for accident testing.

---

## v0.2.2 — Accident Scene Fit Guard

File:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_2_AccidentSceneFitGuard.zip
```

SHA-256:

```text
77911a02e279769b7472c242ded1068da4c8016b3d194d6ce795231515bf03f4
```

What it tried:

- Passenger-only accident filtering.
- Adjacent parking-space clusters.
- Exclusion of semis/trailers/buses/heavy equipment from generic accident scenes.

Why it was rejected:

- David clarified that semis, trailers, buses, heavy wreckers, and rotators are valid accident targets.
- The true problem was the parking-lot location and poor scene composition.

Permanent status:

```text
REJECTED — DO NOT USE
```

Do not revive its passenger-only direction.

---

## v0.2.3 — Roadside Mixed Scenes

File:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_3_RoadsideMixedScenes.zip
```

SHA-256:

```text
0a1c7314ca5b896fd639c2d866e3c1053899de8be18e3f981ba7bb7462725721
```

Added/corrected:

- Road/roadside anchors instead of parking spaces.
- Mixed vehicle classes restored.
- Lane collisions, chain collisions, shoulder scenes, jackknifes, heavy scenes, bus scenes.
- Directional procedural damage.
- Scene-provider API.
- Random-event library probe.
- Real-world scene-design research.

Runtime status:

- Partial inherited core evidence from David's mission testing.
- Full roadway/semantic scene test gate was not completed before later builds.

---

## v0.2.4 — Cataloged History

File:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_4_CatalogedHistory.zip
```

SHA-256:

```text
072c882da5f29ae4bf5be816c6ffbe518dee50d2c64674df084042d0bf0d8405
```

Added:

- Cataloged Tow History Book.
- Old-record compatibility.
- Multi-category call/outcome organization.
- More complete record details.

Status:

```text
BUILT — RUNTIME UNTESTED
```

Superseded by v0.2.5 as the active test candidate, but its features are preserved inside v0.2.5.

---

## v0.2.5 — Fleet Identity and Hazard Sites

File:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
```

SHA-256:

```text
52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
```

Added:

- Tow Fleet Book.
- Fleet names/call signs/roles.
- Exact configuration and paint capture.
- Map-aware intersections/sharp curves/grades.
- Intersection T-bone scenes.
- Sharp-curve rollover scenes.
- Weighted realistic scene paints.
- Scene site/plan in history.

Current status:

```text
ACTIVE CANDIDATE
BUILT — RUNTIME UNTESTED
```

---

# External mod/resource intake completed

## Used Car Generator / Barn Find Generator

Uploaded reference:

```text
barnfindgenerator.zip
```

File identity:

```text
Title: Used Car Generator
Author: Cedminer66
Version: 0.8.2
Resource ID: 30414
Size: 8,037,600 bytes
SHA-256: c94a16a6059a11707ffbe22f60cca415de5c7901cf074c25ee1d3e8cad423658
ZIP integrity: PASS
```

Useful public runtime hook discovered:

```text
extensions.barnfindGenerator.applyWear(conditionConfig, vehicleObject)
```

Potential future JOB-09 uses:

- Believable abandoned-vehicle neglect.
- Disabled-vehicle calls.
- Non-runners.
- Dead battery.
- Flat tires.
- Fuel/cooling/transmission failures.
- Worn impound/yard records.
- Repeatable condition seeds.

Boundary decision:

- Do not copy, rename, bundle, or redistribute its Lua/UI/images.
- Use only optional runtime compatibility when the separate mod is installed.
- JOB-09 must continue working when it is absent.
- Do not add its mechanical wear to crash/rollover targets by default.

Current status:

```text
RESEARCHED / PLANNED
NOT IMPLEMENTED IN v0.2.5
```

---

## Other behavior references researched

No external source or asset was bundled from these references:

- Police Behaviour — roadblock/police behavior reference.
- Post Crash Extras — stuck horns/engine shutdown reference.
- Universal Vehicle Failures — future breakdown-call reference.
- Random tour/scenario/event resources — random placement reference.
- Official BeamNG AI, path, road, paint, and coupler documentation.

---

# What was tried and intentionally stopped

Do not repeat these failed or rejected directions:

1. **Parking-lot accident scenes for large mixed wrecks**
   - Produced impossible layouts.

2. **v0.2.2 passenger-only filtering as the final fix**
   - Contradicted David's requirement for heavy mixed crashes.

3. **Guessing undocumented random-event functions**
   - Current code only probes and logs public names.

4. **Copying or rebundling external reference mods**
   - Optional compatibility only.

5. **Adding a large business/legal/accounting simulator to JOB-09**
   - Future business system must remain simple and separate.

6. **Adding unfinished AI towing to the current video-test build**
   - Player-rigged AI transport is future work after stabilization.

7. **Fully autonomous winching/rotator rigging as the first AI phase**
   - Future plan is manual player rigging and a shared multi-winch overlay.

8. **Direct edits to RLS Career Overhaul**
   - RLS is inspected as a dependency/reference; RedFox should use narrow compatibility/contracts.

---

# Known open issues and limits

## Runtime gaps

- v0.2.5 has not been runtime tested.
- v0.2.4 catalog migration has not been runtime confirmed.
- Tow Fleet Book persistence has not been runtime confirmed.
- Paint capture accuracy has not been runtime confirmed.
- Intersection and sharp-curve scenes have not been runtime confirmed.
- Map hazard scan has not been tested across David's map collection.

## Scene gaps

- Existing random-event police/cone/barrel/debris scenes are not yet connected.
- Saved RedFox layouts primarily store event targets, not every cone, police car, prop, NPC, or emergency asset.
- Exact live node-and-beam deformation is not serialized by JOB-09.
- Some road graphs may produce poor or no semantic sites.
- Traffic diversion/closure behavior still needs an exact safe adapter.

## Yard/impound gaps

- Hold time is real elapsed time, not confirmed RLS in-game time.
- Abandoned recovery still presents the current Keep/Hold versus immediate salvage decision.
- Yard properties are manually placed and not yet linked to a purchased-property system.
- Yard sections such as customer storage, abandoned storage, heavy storage, and auction staging are not yet visually separated.

## Fleet/AI gaps

- Fleet Book does not spawn recorded trucks.
- No hired dispatcher.
- No hired driver payroll.
- No AI transport to yard.
- No `Follow Me`, `Wait Here`, or `Take Load to Yard` commands.
- No hazards/beacon automatic waiting behavior.
- No manual multi-wrecker winch overlay.

## Integration gaps

- No IceFox/FoxNet website link yet.
- No phone/PC destination registration yet.
- No Scrap Yard/auction/dealership destination adapters yet.
- No Used Car Generator condition provider yet.
- No RLS repo-batch/cross-map carrier system yet.

---

# Required first test when David returns

## Installation

1. Disable/remove every older JOB-09 ZIP.
2. Confirm rejected v0.2.2 is not enabled.
3. Enable only:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
```

4. Use a disposable or backed-up Career/RLS save for first testing.
5. Confirm Mod Manager shows v0.2.5.
6. Confirm Career loads without a crash.

Expected load line:

```text
RedFox Tow & Recovery Dispatch v0.2.5 loaded
```

---

## Tow Fleet Book test

1. Configure and paint one tow truck.
2. Enter that vehicle.
3. Open Tow Fleet Book.
4. Register current vehicle.
5. Confirm model/configuration, role, call sign, and Paint Captured status.
6. Rename it.
7. Change its role.
8. Change paint or configuration and update the selected unit.
9. Close/reopen Tow UI.
10. Save/reload Career.
11. Confirm the record remains.
12. Confirm removing a Fleet Book record does not delete the actual vehicle.

Evidence to return:

- Fleet Book screenshot.
- BeamNG log if any button errors.

---

## History compatibility test

1. Open the same Career profile containing older history.
2. Confirm old records are still present.
3. Confirm abandoned record appears under Abandoned Vehicles and Impound / Unpaid where applicable.
4. Confirm accident records appear under Accident Scenes and Paid / Released where applicable.
5. Confirm no duplicate record appears twice inside one catalog.
6. Complete one new call.
7. Confirm its call category and outcome category.
8. Confirm new accident history records include Scene site and Scene plan.

---

## Map-aware scene test

1. Set at least one tow yard on the current map.
2. Enable Map-Aware Intersections / Sharp Curves.
3. Request multiple Multi-Vehicle Accident Cleanup calls.
4. Confirm ordinary roadway/shoulder scenes still work.
5. Watch for an intersection site and T-bone plan.
6. Watch for a sharp-curve site and rollover/secondary-impact plan.
7. Confirm targets are not neatly parked.
8. Confirm vehicles remain recoverable.
9. Confirm mixed passenger/heavy/semi/trailer/bus scenes remain possible where appropriate.
10. Disable map-aware selection and confirm normal road scenes still work.

Evidence to return:

- Screenshot of intersection or curve scene if generated.
- Exact SITE_SCAN log line.
- Exact EVENT_LIBRARY log line.

---

## Core regression test

Run at least one of each enabled type:

```text
Abandoned Vehicle Recovery
Standard Car Tow
Roadside Rolled-Vehicle Recovery
Semi / Trailer Rollover Recovery
Roadway Accident Scene Cleanup
```

Confirm:

- Offer appears.
- Call accepts.
- Pickup route works.
- Target spawns.
- Target can be moved/towed.
- Destination route works.
- Delivery completes.
- History records outcome.
- Yard/impound records remain intact.
- No computer or game crash.

---

## Logs to collect

Return `beamng.log` when any failure occurs.

Search for:

```text
RedFox Tow & Recovery Dispatch v0.2.5 loaded
[RedFox][TOW][SITE_SCAN]
[RedFox][TOW][EVENT_LIBRARY]
[RedFox][TOW][SCENE_PROVIDER]
No usable road or roadside segment
Vehicle spawn failed
Dispatch Error
attempt to index
stack traceback
redfoxTowRecoveryDispatch
```

---

# Planned work after v0.2.5 testing

Priority order:

1. Test v0.2.5 exactly as packaged.
2. Patch only runtime-proven failures.
3. Finish Tow Fleet naming, roles, and paint-record usability.
4. Improve video-friendly reliability and scene composition.
5. Use the returned EVENT_LIBRARY evidence to build a narrow random-event scene adapter.
6. Add police blockers, road closures, cones/barrels, and emergency staging through a verified provider.
7. Add optional Used Car Generator condition compatibility for abandoned/disabled calls.
8. Expand breakdown call types after condition integration is proven.
9. Consider player-rigged AI transport after the standalone mission loop is stable.
10. Consider the multi-wrecker manual winch overlay after coordinator assignment.
11. Add IceFox/FoxNet phone/PC/web integration later without replacing the standalone backend.
12. Coordinate Scrap Yard, auction, dealership, and cross-map repo shipment destinations only after their contracts exist.

---

# GitHub records already published

## Ownership and transfer records

```text
473dad5575a03a06a20b43ef5b2028494f2052ce — JOB-09 claim
1dd908220d44648c210cde4754f9e8432d23b7d9 — regular-chat transfer
c7c23bfe9301a577408ebb92bb63839e0a08adf1 — read-first ownership/continuity override
```

## v0.2.3 records

```text
c7b10749bb1d06b3514a297bd96c21b48c84794f — v0.2.3 roadside mixed-scene handoff
13be3e6e27f7f84cedb1c3a38ac55318bd595648 — real-world crash-scene research
b35b5526911f45cbbeed0bc86040ecaceffc9325 — v0.2.3 source change summary
```

Known paths:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_ROADSIDE_MIXED_SCENES_v0.2.3_2026-07-15.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_REAL_WORLD_CRASH_SCENE_RESEARCH_2026-07-15.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.3_ROADSIDE_MIXED_SCENES_CHANGE_SUMMARY.md
```

## Used Car Generator intake

```text
81bd8696632f8d30d9cbceee5d9586fccaeefd3d — Used Car Generator compatibility intake
```

Known path:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_USED_CAR_GENERATOR_COMPATIBILITY_INTAKE_2026-07-15.md
```

## v0.2.4 record

```text
a57e08f1ed42390aaa5034e059fdd1a90b33437f — v0.2.4 cataloged history handoff
```

## v0.2.5 records

```text
02b457dc5db60da789b446a54b859c4bc1f77198 — v0.2.5 fleet/hazard-site handoff
4f78ad7f7beea52d5f0099440404fdca8eb1f093 — map/AI/paint/event research
296f7b43f8716c6d7daf5c60e8f55c248964a6a4 — v0.2.5 source change record
```

## Coordinator assignment request

```text
GitHub issue #5
[JOB-00 ASSIGNMENT REQUEST] Simple Business Manager and future Tow Support controls
```

This issue records:

- Simple property/business conversion.
- Hire employees and receive passive income.
- Player-rigged AI transport.
- Nearest-reachable yard waiting with hazards/beacons.
- Future manual multi-wrecker winch overlay.

---

# Hard rules to preserve on resume

```text
This is a pause, not a handoff.
JOB-09 remains Tow / Recovery / Dispatch.
Use v0.2.5 as the active candidate.
v0.2.2 is rejected and must not be used.
Do not claim runtime success without David's test.
Do not upload/copy external mod code or assets without clear permission.
Do not patch stock Career or RLS files directly.
Do not add a complex business simulator to JOB-09.
Do not add unfinished AI towing before current mission stability.
Do not guess undocumented random-event APIs.
Preserve older save/history/yard data unless testing proves it broken.
The actual v0.2.5 ZIP is in the chat/container, not the GitHub repo.
```

---

# Resume point after camping

When David returns, begin with:

```text
1. Confirm/download v0.2.5.
2. Disable all older JOB-09 ZIPs.
3. Test Tow Fleet Book persistence.
4. Test cataloged history compatibility.
5. Run all five call types.
6. Test intersection/sharp-curve scenes.
7. Return SITE_SCAN and EVENT_LIBRARY lines.
8. Patch only proven failures.
```

Do not start cross-map repo transport, business management, hired dispatch, AI transport, or multi-winch work before the current standalone v0.2.5 test results are reviewed.
