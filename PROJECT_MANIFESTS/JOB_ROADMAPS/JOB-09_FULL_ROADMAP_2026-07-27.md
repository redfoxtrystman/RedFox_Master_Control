# JOB-09 — RedFox Tow & Recovery Dispatch

## Full Roadmap and End-of-Chat Handoff

**Date:** 2026-07-27  
**Owner:** JOB-09 regular ChatGPT workstation  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Coordination issue:** #4  
**Module ID:** `redfox_tow_recovery_dispatch`

---

# 1. Project purpose

JOB-09 owns the RedFox tow, recovery, dispatch, tow-yard custody, and tow-specific business workflow for BeamNG Career and RLS Career.

The system should eventually let the player:

- own and operate one or more tow businesses;
- designate purchased RLS garage properties as tow yards;
- manage tow trucks and company vehicles through normal RLS-owned inventory;
- receive, perform, and complete towing and recovery calls;
- store abandoned, impounded, customer, lien, and recovered vehicles in a separate tow-yard custody system;
- move company vehicles and custody vehicles between yards;
- collect towing and storage revenue;
- claim lien-eligible vehicles after a short gameplay hold;
- sell eligible vehicles through supported RLS NPC systems, salvage, or scrap;
- expand yard capacity and specialized storage later;
- run the business through a working tow-yard computer and later the RedFox web/phone interface;
- build believable police, fire, ambulance, tow, debris, and recovery scenes without replacing protected game or RLS files.

---

# 2. Immutable design rules

## 2.1 Purchased property becomes the tow yard

When the player buys an RLS garage property and designates it as a tow yard, that existing property is the tow yard.

Do not create a second artificial RLS garage beside it.

Example:

- Existing RLS garage ID: `servicestationGarage`
- RedFox tow-yard ID: `redfox_yard_001`
- Display name: player-editable, such as `RedFox Main Yard`

The RedFox tow-yard record points to the existing RLS garage ID.

The existing RLS garage controls:

- My Vehicles grouping;
- owned-vehicle location;
- retrieval and storage;
- garage capacity for company vehicles;
- physical parking and spawn locations;
- computer association;
- normal Career/RLS behavior.

The RedFox tow-yard record controls:

- tow-yard name;
- business assignment;
- custody storage;
- dedicated storage types;
- lien and disposition records;
- yard-specific money, history, and later upgrades.

## 2.2 Company vehicles remain normal RLS-owned vehicles

Tow trucks, wreckers, rollbacks, service trucks, tractors, lowboys, trailers, and other company equipment remain normal RLS-owned Career inventory vehicles.

A company assignment must never:

- delete the owned record;
- replace the inventory ID;
- set ownership to false;
- create a second duplicate vehicle;
- hide the vehicle from My Vehicles;
- force the stock $5,000 delivery action merely to access it at its own yard.

Moving a company vehicle changes only:

- its existing RLS garage location;
- its RedFox company/fleet metadata;
- its assigned yard and previous-yard history.

## 2.3 Custody vehicles are not owned vehicles

Abandoned, impounded, unpaid, customer-storage, evidence-hold, and lien-eligible vehicles are not company-owned and must not appear in normal My Vehicles until a valid ownership transfer is completed.

They live in the RedFox Tow Yard Inventory as custody records tied to a physical tow-yard property.

## 2.4 One physical property, two inventory views

Every designated tow-yard property has:

1. **Company Garage** — normal RLS-owned company vehicles.
2. **Tow Yard Inventory** — non-owned custody vehicles.

The two systems share the property but not ownership.

## 2.5 No protected-file replacement

JOB-09 must not overwrite, fork, or directly edit stock BeamNG or RLS core files.

Integrate through:

- supported APIs;
- extension hooks;
- facility definitions owned by the RedFox mod;
- approved Career/RLS bridge contracts;
- additive computer functions;
- RedFox save files.

## 2.6 No fake claims

Every build and feature must use one of these statuses:

- **DAVID-TESTED WORKING**
- **BUILT — RUNTIME UNTESTED**
- **PARTIAL**
- **BLOCKED**
- **FAILED — STOPPED**
- **MOCKUP/PLACEHOLDER**

---

# 3. Exact status at this handoff

## 3.1 Current distributed build

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_1_RLSTowShopGarageBridge.zip`

SHA-256:

`662db67fc190ede9c529391c39570e93883c2c7024ebb2edb8c700837f5c4aec`

Previous build status was **BUILT — RUNTIME UNTESTED**.

After David's runtime test, the property integration direction is now:

**FAILED — STOPPED**

## 3.2 Runtime findings from v0.3.1

David confirmed:

- the mod created an artificial location named `Tow Yard 1` instead of using the property's real RLS garage;
- the tested vehicle still had a normal RLS inventory ID and remained owned;
- the real property computer was associated with `servicestationGarage`;
- RLS saw the artificial `Tow Yard 1` location as different from the current computer's garage;
- the stock Deliver option therefore charged $5,000;
- the stock delivery path also imposed the normal approximately 120-second delay;
- a separate RedFox fleet-computer prompt appeared but was not usable;
- the property already has a real computer and should receive tow-yard functions instead of creating a separate inaccessible management path.

These findings are sufficient. Do not continue testing the artificial-garage approach.

## 3.3 Deferred visual/property finding

The selected service-station property contains five numbered garage bays that are currently decorative/unusable.

Possible later work:

- make doors functional;
- define interior parking/storage spots;
- tie bays to tow-truck capacity;
- use them for visible company-fleet storage or service operations.

This is explicitly deferred until the computer and property binding work correctly.

## 3.4 Deferred emergency-scene research

David found a mod that improves emergency-vehicle lights and sounds and may contain scene-related systems.

Later work should inspect it for:

- emergency responder spawning;
- cones, flares, barriers, debris, and traffic control;
- police, fire, and ambulance staging;
- reusable scene hooks;
- cleanup/despawn logic;
- safe compatibility with RLS traffic and JOB-09.

No integration claim is allowed until the actual mod is inspected.

---

# 4. What is being tested right now

## Stop testing v0.3.1 property transfers

The v0.3.1 artificial tow-yard garage has already failed the correct-use test.

There is no reason to spend more time testing:

- paid delivery to the artificial Tow Yard 1 location;
- the 120-second stock delivery delay;
- retrieval through the inaccessible separate fleet computer;
- additional vehicles in the artificial garage.

## Next test target

The next patch should be a focused **property computer and tow-yard designation foundation** patch, tentatively v0.3.2.

Only that foundation should be tested before dispatch, scenes, storage expansion, liens, or other large features continue.

---

# 5. Immediate patch — v0.3.2 Property Computer Foundation

## Goal

Turn an existing purchased RLS garage property into a RedFox tow yard without creating a second RLS garage.

## Required changes

### 5.1 Tow-yard designation

Add a safe action that lets the player designate an accessible purchased/rented RLS garage property as a tow yard.

Save:

- RedFox yard ID;
- existing RLS garage ID;
- map ID;
- player-editable display name;
- property/computer association;
- company capacity default;
- custody capacity default;
- active/inactive state.

### 5.2 Rename tow yard

The player must be able to rename every yard.

Examples:

- RedFox Main Yard
- Belasco Service Yard
- Port Recovery
- Heavy Wrecker Yard

Changing the display name must not change the stable RedFox yard ID or the existing RLS garage ID.

### 5.3 Existing computer integration

Add RedFox functions to the property's existing computer rather than relying on a separate inaccessible computer.

Initial computer menu:

- My Vehicles — existing RLS function
- Tow Yard Management
- Company Fleet
- Tow Yard Inventory
- Dispatch
- Settings

For v0.3.2, Tow Yard Management, Company Fleet, Tow Yard Inventory, and Settings may begin as focused functional screens with unavailable future sections clearly labeled.

### 5.4 Free local tow-yard transfer action

At a designated tow-yard computer, owned vehicles should offer:

- Move to This Tow Yard
- Return to Previous Garage
- Move to Another Tow Yard

This must not call the stock $5,000 Deliver function.

It must not apply the stock 120-second delivery delay.

### 5.5 Correct same-yard behavior

When the vehicle location already matches the current property's real RLS garage ID:

- do not show a paid Deliver requirement;
- allow normal Retrieve/Replace/Store behavior;
- show that it is assigned to the current tow yard;
- preserve its inventory ID and ownership.

### 5.6 v0.3.1 migration

Provide a safe migration for artificial `redfox_towshop_*` or `Tow Yard 1` assignments:

1. Back up Career and RedFox data.
2. Identify the RedFox yard's linked real RLS garage.
3. Verify the existing owned inventory record.
4. Change its location to the real property garage ID.
5. Preserve ownership and inventory ID.
6. Verify the vehicle appears exactly once.
7. Remove obsolete artificial-yard assignment only after successful verification.
8. Save immediately.
9. Provide an undo/recovery snapshot.

## v0.3.2 acceptance test

Use one noncritical owned vehicle.

1. Load the purchased service-station property.
2. Designate the real property as a tow yard.
3. Rename it.
4. Open the existing property computer.
5. Confirm Tow Yard Management appears.
6. Move the vehicle to this tow yard.
7. Confirm no $5,000 charge.
8. Confirm no 120-second wait.
9. Confirm the same inventory ID remains.
10. Confirm ownership remains true.
11. Confirm the vehicle appears once in My Vehicles under the property's real garage location.
12. Retrieve it from the same computer.
13. Store it again.
14. Move it back to its previous garage.
15. Re-enter Career and confirm persistence.

Do not move to later phases until this test passes.

---

# 6. Phase roadmap

# Phase 1 — Tow-yard property and computer foundation

Status: **NEXT**

Deliverables:

- designate existing property as tow yard;
- rename yards;
- bind RedFox yard to real RLS garage ID;
- add computer menu;
- free same-business transfers;
- migrate v0.3.1 artificial locations;
- save/undo/recovery protection;
- current-map yard list;
- closest/current property identification.

Release gate:

- one complete round trip between personal garage and tow yard with no loss, duplication, fee, delay, or ownership change.

# Phase 2 — Company Fleet

Deliverables:

- Company Fleet becomes a filtered view of normal RLS-owned inventory;
- assign/remove company status;
- fleet unit ID;
- call sign;
- role: rollback, light wrecker, heavy wrecker, service truck, tractor, trailer, support;
- assigned yard;
- previous yard;
- custom fleet photo later;
- show current RLS garage and map;
- move between tow yards;
- undo last move;
- no duplicate inventory.

Release gate:

- multiple owned vehicles remain visible in My Vehicles and move between two real property garages safely.

# Phase 3 — Tow Yard Inventory foundation

Deliverables:

- separate custody records;
- categories:
  - abandoned;
  - police impound;
  - unpaid/customer storage;
  - lien eligible;
  - evidence/hold;
  - recovered/awaiting pickup;
  - disposition eligible;
  - released/sold/scrapped history;
- yard assignment;
- original call link;
- arrival day/time;
- storage day count;
- tow charge;
- capped lien amount;
- search result/status;
- vehicle config, paint, condition, mileage, thumbnail where available;
- record number and audit history;
- Tow Yard Inventory computer screen;
- search, filters, sort, expandable rows, and close button.

Release gate:

- deliver one abandoned vehicle to custody, save/reload, search it once, and confirm it remains non-owned.

# Phase 4 — Capacity and storage routing

Base capacity for every new tow yard:

- 10 universal custody slots;
- 5 company-vehicle garage slots.

Universal custody slots can accept every supported vehicle category so a job is never lost solely because a specialized upgrade is missing.

Dedicated storage upgrades later include:

- trailer storage;
- heavy vehicle storage;
- boat storage;
- aircraft/oversize storage;
- secure impound;
- salvage storage;
- hazmat storage;
- marine storage.

Routing priority:

1. matching dedicated storage at the selected/closest yard;
2. matching dedicated storage at another current-map yard;
3. universal custody at the selected/closest yard;
4. universal custody at another current-map yard;
5. temporary overflow as the final safety net.

When dedicated storage is purchased, future matching vehicles go there automatically.

A reorganize/refresh action can move old universal records into dedicated storage when capacity exists.

Release gate:

- fill a dedicated category, verify overflow uses universal storage, and verify another compatible yard is recommended when available.

# Phase 5 — Stored-vehicle refresh and migration

Settings action:

**Refresh / Migrate Stored Vehicles**

Functions:

- back up all records;
- preview changes;
- repair missing yard IDs;
- update old yard names;
- migrate old storage categories;
- update location codes;
- update storage rate handling;
- preserve original call/history;
- prevent duplicates;
- log every changed record;
- undo last migration.

Financial choices:

- keep existing balance and use new rate going forward;
- recalculate full balance;
- update records only without changing money.

Release gate:

- migrate old v0.2.x/v0.3.x stored records without loss or duplicate records.

# Phase 6 — Three-day lien and disposition

Lien eligibility:

- after three Career days;
- claim cost includes tow charge plus exactly three days of storage;
- claim amount freezes after the third day;
- a vehicle stored for 100 days does not cost 100 days to claim;
- no rust/deterioration system unless separately approved later.

Actions after eligibility:

- leave in custody;
- claim to personal garage;
- claim to company garage;
- claim and list on RLS Marketplace for NPC offers;
- claim and consign to the RLS used-car auction for NPC bidding;
- sell to salvage;
- scrap;
- transfer to another tow yard.

No player-to-player sales.

Ownership-transfer safety:

1. confirm eligibility;
2. calculate capped cost;
3. confirm destination capacity;
4. back up custody record;
5. create/restore one normal owned inventory record;
6. preserve configuration, paint, condition, mileage, and history where available;
7. verify exactly one owned record;
8. add lien history;
9. remove custody record only after success;
10. roll back on failure.

Vehicle-history/Carfax addition:

- Tow Lien Recorded;
- prior abandoned/impound status where applicable;
- yard and hold duration;
- lien amount;
- final disposition;
- lien satisfied status.

Release gate:

- one vehicle reaches day three, remains capped after additional days, and is safely claimed or disposed without duplication.

# Phase 7 — Tow-yard and business money

Tow-specific financial tracking:

- call revenue;
- towing charges;
- storage revenue;
- lien claim payments;
- Marketplace/auction/salvage/scrap proceeds;
- yard transfer costs;
- yard expansion costs;
- expenses and later insurance integration;
- per-yard and company totals;
- transaction history;
- no duplicate payments.

The computer becomes the first stable business-management entry point.

Future shared business-management work must coordinate with the proper owner job rather than duplicating a global business system.

Release gate:

- one call, one storage charge, and one disposition produce exactly one correct transaction each.

# Phase 8 — Yard closure, sale, and relocation

A tow yard cannot be sold, closed, or liquidated while it contains:

- company vehicles;
- custody vehicles;
- trailers/equipment;
- active calls assigned to it;
- active listings or unresolved holds.

Required relocation workflow:

- show every remaining asset;
- require valid destination yards;
- verify capacity and storage type;
- move company vehicles without ownership change;
- move custody records without resetting lien/history;
- prevent automatic dumping into a personal garage;
- close property only when both company and custody counts reach zero.

Relocation modes:

- paid full-shop commercial relocation;
- player-loaded same-map relocation;
- later loaded cross-map manifest/reconstruction.

Release gate:

- sale is blocked while one record remains and becomes available only after verified relocation.

# Phase 9 — Dispatch and call workflow stabilization

Primary call types:

1. Standard Car Tow
2. Rolled Car Recovery
3. Semi Rollover Recovery
4. Multi-Vehicle Accident Cleanup
5. Abandoned Vehicle Recovery

Standard Tow reasons:

- mechanical breakdown;
- flat tire/wheel problem;
- out of fuel;
- dead battery;
- lockout;
- police impound;
- customer relocation.

Requirements:

- clear pickup and destination;
- recommended equipment;
- expected pay;
- route controls;
- cancel/details;
- no repeated same call/vehicle spam;
- current-map yards first;
- nearest suitable yard first;
- completed job receipt separate from live yard status;
- exact one-time payment;
- development force controls kept separate from normal random behavior.

Release gate:

- one complete end-to-end call of each primary type without missing targets, duplicate payment, or stranded storage record.

# Phase 10 — Vehicle catalog, class correction, and coupler validation

Deliverables:

- catalog inspector;
- blacklist exact configuration;
- approve exact configuration;
- assign/reassign class;
- undo last correction;
- category history;
- future calls use saved correction;
- optional rebuild of current development call;
- class color coding;
- verified coupler/capability evidence:
  - fifth wheel;
  - kingpin;
  - ball;
  - pintle;
  - gooseneck;
  - tongue;
- pair validation for tractor/trailer calls;
- reject unknown pairings rather than guessing.

Release gate:

- bad crane chains/boom props remain excluded and one valid tractor/trailer combination is selected repeatedly.

# Phase 11 — Scene system

Scene sources:

- procedural road/shoulder scenes;
- player-built RedFox scene templates;
- approved external event/scene libraries;
- optional emergency-light/sound mod hooks after inspection.

Scene components:

- police cars;
- fire engines;
- ambulances;
- tow/recovery vehicles;
- cones, flares, barrels, barriers, signs;
- debris and cargo;
- smoke/fire/hazmat effects;
- blocked lanes and traffic control;
- one or more damaged targets;
- believable road footprint;
- cleanup/despawn.

Scene families:

- minor collision;
- lane collision;
- chain-reaction crash;
- shoulder rollover;
- semi jackknife;
- tractor/trailer rollover;
- bus crash;
- heavy-truck/rotator wreck;
- vehicle fire;
- EV fire;
- hazmat;
- pileup;
- boat/aircraft recovery later.

Release gate:

- scenes fit the selected site, do not intersect buildings, and clean up fully after completion/cancellation.

# Phase 12 — Roadside services

Normal gameplay should complete simple roadside jobs automatically when the player arrives nearby, without separate World Editor buttons.

Services:

- jump start;
- fuel delivery;
- tire/wheel assistance;
- lockout;
- simple roadside repair where supported.

Development force buttons may remain in Dev Testing Mode only.

Release gate:

- each service completes once, pays once, records once, and does not spawn an unnecessary tow target.

# Phase 13 — Cross-map support

Current reality:

- RLS can move one owned vehicle for $5,000 with a delay;
- that stock service is not the intended tow-business relocation model;
- loaded cargo/trailer combinations are difficult to preserve across maps.

Roadmap:

1. move company vehicle records between real yard garage IDs;
2. transfer custody records between map yards;
3. add paid whole-shop relocation;
4. add map-gate/port transition points;
5. save tractor, trailer, cargo, and load manifest;
6. reconstruct at destination;
7. verify every asset;
8. retain recovery snapshots.

Release gate:

- no vehicle or custody record is lost during a two-map move.

# Phase 14 — Tow-yard upgrades and physical property use

Later upgrades:

- add custody slots;
- add company garage slots;
- dedicated trailer/heavy/boat/aircraft/secure/hazmat storage;
- additional computers or terminals;
- visible yard parking;
- usable service bays;
- functional doors;
- repair/wash/fleet-prep areas;
- property appearance upgrades.

The five numbered service-station bays should be evaluated here, not before the computer foundation.

Release gate:

- purchased capacity changes are persistent and physical spots match logical capacity where practical.

# Phase 15 — Website and phone integration

JOB-09 pages:

Public:

- Home
- Request Service
- Track Call
- Services
- Rates
- Locations
- Claim Impound
- Contact

Employee/business:

- Dispatch
- Calls
- History
- Fleet
- Drivers
- Yards
- Tow Yard Inventory
- Impounds
- Abandoned/Lien
- Repossessions
- Invoices
- Major Incidents
- Relocation
- Fleet Map
- Settings

Shared shell, browser, login/session, and phone platform remain JOB-01 responsibilities.

Release gate:

- website data matches the in-game tow-yard computer data without creating a second economy or inventory.

# Phase 16 — QA, migration, and release hardening

Every candidate:

- ZIP integrity;
- JSON parse;
- Lua syntax;
- protected-path scan;
- duplicate-path scan;
- file inventory;
- source summary;
- exact SHA-256;
- save migration notes;
- focused runtime checklist;
- rollback instructions;
- status label.

Runtime checks:

- no duplicate vehicles;
- no lost ownership;
- no changed inventory IDs during garage moves;
- no duplicate payment;
- no inaccessible records;
- no uncloseable windows;
- no per-frame save/log spam;
- full cleanup after scenes;
- save/reload persistence;
- map-switch persistence;
- disabled-mod behavior documented.

Release gate:

- all critical paths are David-tested and old saves migrate safely.

---

# 7. Data model target

## Tow-yard property record

- RedFox yard ID
- display name
- existing RLS garage ID
- map ID
- business ID
- property/computer ID
- active state
- primary/secondary flag
- company capacity
- custody capacity
- purchased upgrades
- storage capabilities
- current counts
- transaction totals
- created/renamed history

## Company-fleet metadata

Stored against or linked to the same normal RLS inventory ID:

- company vehicle flag
- fleet unit ID
- call sign
- role
- assigned yard
- previous yard
- photo/thumbnail reference
- assignment history

## Custody record

- custody record ID
- source call ID
- model/config
- paint
- condition
- mileage
- thumbnail
- plate/owner/agency where available
- custody category
- current yard
- storage type
- arrival Career day
- days stored
- lien eligibility day
- capped lien amount
- tow/storage balance
- search status/result
- hold/disposition state
- transfer history
- final disposition
- resulting owned inventory ID when claimed

---

# 8. Save and backup rules

Existing RedFox save files include:

- `settings/redfox/tow_recovery_dispatch_yard.json`
- `settings/redfox/tow_recovery_dispatch_settings.json`
- `settings/redfox/tow_recovery_dispatch_ui_layout.json`
- `settings/redfox/tow_recovery_dispatch_scenes.json`

Future data should be organized by Career save where practical and must not silently mix unrelated careers.

Before destructive migration or transfer:

- back up RedFox files;
- back up affected Career vehicle records;
- write transaction snapshot;
- verify destination;
- preserve undo data;
- never remove source until destination is confirmed.

---

# 9. Current priority order

1. Stop artificial tow-yard garage testing.
2. Build the property computer and designation foundation.
3. Bind the RedFox tow yard to the real RLS garage ID.
4. Add tow-yard rename.
5. Add free Move to This Tow Yard behavior.
6. Migrate v0.3.1 vehicles safely.
7. Confirm normal My Vehicles retrieval/storage at that property.
8. Build Company Fleet as a filtered RLS-owned view.
9. Build Tow Yard Inventory for non-owned custody records.
10. Add capacity and automatic storage routing.
11. Add stored-vehicle migration.
12. Add three-day lien and disposition.
13. Add money/business screens.
14. Return to dispatch and scene expansion.
15. Inspect emergency-scene mod.
16. Make decorative bays usable later.

---

# 10. New-chat starting instruction

The next JOB-09 chat should begin by reading this roadmap and issue #4.

The first coding task is not additional crash calls or yard scenery.

The first coding task is:

> Build v0.3.2 so a purchased existing RLS garage property can be designated and renamed as a tow yard, its existing computer opens Tow Yard Management, and owned vehicles move to that real garage without the $5,000 stock delivery charge or 120-second delay.

Do not claim this works until David tests the exact build.
