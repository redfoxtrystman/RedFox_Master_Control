# JOB-09 End-of-Chat Handoff and Full Roadmap

Date: 2026-07-27

Job: `19 — JOB-09-RedFox_TowRecoveryDispatch`

Module ID: `redfox_tow_recovery_dispatch`

Repository issue: `#4 — [JOB-09] CLAIMED — Tow / Recovery / Dispatch transferred to regular chat`

## 1. Current exact build

Current distributed test build:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_1_RLSTowShopGarageBridge.zip`

SHA-256:

`662db67fc190ede9c529391c39570e93883c2c7024ebb2edb8c700837f5c4aec`

Build-time status was `BUILT — RUNTIME UNTESTED`.

After David's runtime test, the property/garage portion is now:

**FAILED — STOPPED**

The dispatch and unrelated existing features are not automatically marked failed, but the v0.3.1 company-garage/property design must be replaced before further company fleet testing.

## 2. What is being tested right now

Nothing else needs to be tested in v0.3.1.

The current test is complete. It proved the following failure:

- v0.3.1 created a separate artificial tow-yard garage called `Tow Yard 1`.
- The purchased service-station property already has the real RLS garage ID `servicestationGarage` and its own computer.
- The artificial tow-yard garage did not match the computer's RLS garage ID.
- RLS therefore treated the vehicle as remote and offered the stock $5,000 Deliver action with an approximately 120-second delay.
- The generated RedFox Fleet Computer was not the correct property management access point.

David should stop testing this transfer path until the focused replacement patch is built.

## 3. Immediate owner decision

When a purchased property is designated as a tow yard:

> The existing property garage becomes the tow yard. No second garage is created.

The RedFox record should point to the existing RLS property and garage:

```text
RedFox yard ID: redfox_tow_yard_001
Custom name: RedFox Main Yard
RLS garage ID: servicestationGarage
Map: west_coast_usa
Existing computer: computer facility linked to servicestationGarage
```

The RedFox yard ID and custom name control tow-business identity and tow-specific records.

The existing RLS garage ID controls:

- My Vehicles location
- owned-vehicle capacity
- retrieve/store behavior
- garage computer access
- parking spots
- physical spawning
- normal RLS ownership and inventory behavior

## 4. Immediate next patch

Suggested version:

`v0.3.2 — Existing Property Tow Yard Computer`

This patch must be focused. Everything else remains on hold.

### Required scope

1. Remove or bypass the separate artificial `redfox_towshop_*` garage design for existing properties.
2. Let a purchased RLS property be designated as a RedFox tow yard.
3. Save the property's real RLS garage ID on the RedFox yard record.
4. Detect the existing computer facility linked to that garage ID.
5. Add RedFox actions to the existing computer without replacing stock RLS actions.
6. Allow the user to rename the tow yard.
7. Add a working Tow Yard Management menu.
8. Add a working Company Fleet menu using normal owned RLS vehicles.
9. Add a Tow Yard Inventory entry point for separate non-owned custody records, even if the first patch initially shows only the existing records and capacity summary.
10. Migrate old artificial Tow Yard 1 vehicle assignments back to the property's real RLS garage.
11. Remove the stock $5,000 fee and 120-second delay from RedFox same-property fleet movement.
12. Preserve inventory ID, ownership, configuration, paint, condition, mileage, insurance information, and thumbnail.
13. Remove or safely disable the artificial v0.3.1 Fleet Computer after migration.
14. Keep the normal RLS computer functions available.

### Existing computer menu target

The existing property computer should keep all normal RLS options and add a RedFox section such as:

```text
My Vehicles
Vehicle and Parts Management
Insurance Management

RedFox Tow Yard Management
Company Fleet
Tow Yard Inventory
```

Do not replace the entire computer interface.

### Tow-yard renaming

The custom RedFox name must be editable, for example:

- RedFox Main Yard
- Belasco Tow & Recovery
- Heavy Recovery Yard
- Port Impound Lot

The stable RLS garage ID must not change when the user renames the tow yard.

The stock RLS property name may still appear in normal My Vehicles until a safe display-label integration is added. The RedFox menus and records should use the custom tow-yard name immediately.

## 5. Exact v0.3.2 test gate

Use one noncritical owned vehicle and the purchased service-station property.

### Setup

1. Disable every older JOB-09 ZIP.
2. Enable only the focused replacement candidate.
3. Back up the Career save.
4. Back up `settings/redfox/`.
5. Load West Coast and go to the purchased service-station property.

### Property designation

1. Designate the existing property as a tow yard.
2. Confirm the saved RLS garage ID is `servicestationGarage`.
3. Confirm no new `redfox_towshop_*` RLS garage is created.
4. Rename the yard.
5. Save, exit Career, reload, and confirm the custom name remains.

### Existing computer

1. Walk to the property's normal computer.
2. Confirm all stock RLS functions still work.
3. Confirm RedFox Tow Yard Management appears.
4. Open the RedFox menu.
5. Confirm it identifies the correct custom yard name and `servicestationGarage`.

### Company vehicle move

1. Select one normal owned RLS vehicle located at another garage.
2. Record its inventory ID, location, ownership, configuration, paint, and condition.
3. Use the RedFox `Transfer to This Tow Yard` action.
4. Confirm no money is charged.
5. Confirm no 120-second delay is applied.
6. Confirm the same inventory ID remains.
7. Confirm ownership remains true.
8. Confirm the vehicle appears exactly once under the service-station garage in My Vehicles.
9. Confirm the artificial Tow Yard 1 location is gone.

### Retrieval

1. Open normal My Vehicles from the same property computer.
2. Confirm the vehicle shows Retrieve or Replace current vehicle, not Deliver.
3. Retrieve it.
4. Confirm correct configuration, paint, condition, mileage, name, and insurance information.
5. Store it back at the same property with no fee or delay.

### Migration

1. Run the old v0.3.1 Tow Yard 1 migration on one affected vehicle.
2. Confirm it moves to the real property garage.
3. Confirm there is exactly one copy.
4. Confirm the obsolete artificial assignment is removed only after verification.

### Stop immediately when

- the vehicle disappears
- the vehicle appears twice
- ownership becomes false
- the inventory ID changes
- the stock computer loses normal options
- RedFox opens from the wrong computer or garage
- the move charges $5,000
- the move starts the 120-second delivery timer
- the vehicle remains assigned to artificial Tow Yard 1
- retrieval spawns at the wrong garage

## 6. Full development roadmap

The phases below are ordered. A phase does not advance until its focused test gate passes.

---

# PHASE A — Property and Computer Foundation

Priority: immediate

Status: next patch required

## A1. Existing property designation

- Select a purchased or accessible RLS property.
- Designate it as a tow yard.
- Link RedFox yard ID to the existing RLS garage ID.
- Do not create a second garage.
- Save map ID, property ID, garage ID, and computer ID.

## A2. Existing computer integration

- Add RedFox functions through the computer-function hook.
- Preserve stock RLS functions.
- Support properties with one or multiple computers.
- Use the primary computer or allow all linked computers to open tow management.
- Detect and report a missing computer cleanly.

## A3. Custom yard names

- Rename each RedFox tow yard independently.
- Keep permanent internal RedFox yard ID.
- Keep permanent RLS garage ID.
- Use custom name in dispatch, custody records, fleet, history, and website data.

## A4. v0.3.1 migration

- Find artificial `redfox_towshop_*` and `Tow Yard 1` assignments.
- Back up Career and RedFox data.
- Reassign normal owned vehicles to the real property garage.
- Verify one owned record.
- Remove obsolete artificial data only after verification.

Exit gate: full v0.3.2 test gate passes.

---

# PHASE B — Company Fleet on Normal RLS Inventory

Priority: immediately after Phase A

## B1. Single-record rule

Every company vehicle remains one normal owned RLS inventory vehicle.

Never:

- delete it from inventory during a garage move
- create a second company copy
- set `owned=false`
- change inventory ID merely to assign it to the business

## B2. RedFox fleet metadata

Attach or store safely:

- fleet unit ID
- call sign
- role
- assigned RedFox yard ID
- assigned RLS garage ID
- active/inactive company assignment
- notes
- preferred tow-call classes

## B3. Company Fleet computer screen

Show:

- vehicle thumbnail
- normal RLS inventory ID
- custom name
- call sign
- role
- current garage
- condition
- insurance
- availability
- current map

Actions:

- assign to company
- remove company assignment
- transfer to this tow yard
- transfer to another tow yard
- retrieve
- store
- rename unit
- undo last verified transfer

## B4. Free RedFox business transfers

At a designated tow-yard computer:

- `Transfer to This Tow Yard` is immediate and free.
- It changes location and fleet assignment only.
- The stock RLS $5,000 delivery option remains available for normal non-RedFox use but is not used for company transfers.

## B5. Global My Vehicles action

Later, add a safe `Move to Tow Yard` action to the normal owned-vehicle action menu.

The first working implementation may remain inside the Tow Yard Company Fleet computer screen if modifying the stock menu is unsafe.

Exit gate: transfer one vehicle personal -> tow yard -> another tow yard -> personal, with the same inventory ID and no duplication.

---

# PHASE C — Physical Fleet Bays and Retrieval Points

Priority: after company fleet logic is stable

The five numbered service-station bays are a strong physical match for the five starting company vehicle slots.

## C1. Five starting fleet slots

Every new tow yard begins with:

- 5 company fleet slots
- 10 separate universal custody slots

The five numbered bays should eventually map to:

- Bay 1 — company slot 1
- Bay 2 — company slot 2
- Bay 3 — company slot 3
- Bay 4 — company slot 4
- Bay 5 — company slot 5

## C2. Parking-spot registration

- Inspect existing facility sites and parking spots.
- Reuse valid named spots when possible.
- Add mod-owned sites data only when necessary.
- Do not overwrite stock/RLS files.
- Associate parking spots with the existing property garage.

## C3. Vehicle-size routing

Indoor bays:

- light tow trucks
- service trucks
- smaller rollbacks
- normal company vehicles

Outside heavy area:

- heavy wreckers
- buses
- semi tractors
- lowboys
- large trailers

The system must never spawn a large vehicle inside a wall or closed bay.

## C4. Door investigation

Inspect whether each numbered door is:

- a separate animated object
- a separate static object
- part of one combined building model

Possible solutions:

1. use existing animation and trigger
2. swap closed/open objects
3. keep doors visual-only and use functional zones
4. later add custom replacement doors

Door animation is not required for the first physical-bay patch.

Exit gate: retrieve and store small and heavy fleet vehicles at valid physical positions without collision or wall spawning.

---

# PHASE D — Separate Tow Yard Custody Inventory

Priority: after owned fleet is stable

Custody vehicles are not owned Career vehicles.

Include:

- abandoned vehicles
- police impounds
- unpaid customer vehicles
- lien-eligible vehicles
- evidence or agency holds if later supported
- development recovery records

## D1. Separate records

Custody records remain in RedFox Tow Yard Inventory and do not appear in normal My Vehicles.

Each record stores:

- record ID
- model/config identity
- thumbnail or captured image
- original call
- current tow yard
- storage category
- arrival Career day
- lien eligibility day
- capped claim balance
- estimated value
- condition snapshot
- search status
- disposition status
- history

## D2. Tow Yard Inventory screen

Categories:

- All Yard Vehicles
- Police Impound
- Abandoned / Lien
- Customer Storage
- Hold
- Disposition Eligible
- Released / Sold / Scrapped

Search and sort:

- vehicle name
- record ID
- plate
- yard
- arrival day
- days stored
- lien balance
- value
- status

## D3. Starting capacity

Each yard starts with:

- 10 universal custody slots
- 5 company fleet slots

The two capacity pools are separate.

Exit gate: store, transfer, reload, search, and retrieve custody records without adding them to owned inventory.

---

# PHASE E — Storage Routing, Dedicated Storage, and Overflow

Priority: after basic custody inventory

## E1. Universal storage safety rule

Universal custody storage accepts every towable category so a job is never lost solely because a specialized upgrade is missing.

Categories include:

- cars
- trucks
- semis
- trailers
- buses
- boats
- aircraft
- construction equipment
- unusual recoverable objects

## E2. Dedicated storage upgrades

Later upgrades may add:

- trailer storage
- heavy-vehicle storage
- boat storage
- aircraft/oversize storage
- secure police impound
- salvage storage

## E3. Automatic routing order

1. Matching dedicated storage at the selected/closest compatible yard.
2. Matching dedicated storage at another yard on the current map.
3. Universal custody at the selected/closest yard.
4. Universal custody at another yard.
5. Temporary overflow when all normal slots are full.

When dedicated storage exists, matching vehicles automatically use it first.

When it fills, vehicles use universal storage as category overflow.

## E4. Temporary category storage

Example:

- A boat arrives before boat storage is purchased.
- It uses `Universal Custody — Temporary Boat Storage`.
- It remains searchable, transferable, and eligible for disposition.
- Purchasing boat storage allows a reorganize action to move it automatically when space exists.

## E5. Refresh / Migrate Stored Vehicles

Settings action:

- back up records
- preview changes
- repair missing yard IDs
- update old storage code
- update storage categories
- move matching records into new dedicated storage
- preserve lien timers and history
- choose whether old balances are preserved or recalculated
- allow undo of the last migration

Exit gate: category routing and overflow pass with cars, trailers, heavy vehicles, and one unsupported special category.

---

# PHASE F — Three-Day Lien and Disposition

Priority: after custody storage is reliable

## F1. Lien rule

- Lien becomes available after three Career days.
- Claim cost is capped at the tow/recovery charge plus exactly three days of storage.
- Waiting 100 days does not increase the player's claim cost beyond the three-day cap.
- Extra elapsed days remain informational only.
- No automatic rusting or deterioration.

## F2. Disposition choices

After lien eligibility:

- claim to personal garage
- claim to company garage
- claim and list on RLS Marketplace
- claim and consign to RLS used-car auction
- sell to salvage
- scrap
- transfer to another tow yard
- leave in custody storage

There is no sale to another human player.

## F3. Safe ownership conversion

A custody record becomes owned only after the player chooses a valid lien action and pays the capped cost.

Transaction:

1. validate eligibility
2. validate destination capacity
3. save recovery snapshot
4. charge payment
5. create one normal owned RLS inventory vehicle
6. preserve config, paint, condition, mileage, and history where available
7. verify one owned record
8. close custody record only after verification
9. roll back on failure

## F4. Vehicle-history event

Add a permanent Carfax-style history event:

- Tow Lien Recorded
- prior storage/impound reason
- tow company
- yard
- lien eligibility date
- held duration
- capped lien amount
- final disposition
- lien status satisfied

It should say the vehicle previously had a tow lien, not that an active unpaid lien remains.

Exit gate: convert one custody vehicle to owned, then sell one through NPC Marketplace and one through NPC auction without duplicates.

---

# PHASE G — Tow Business Money and Computer Management

Priority: after property, fleet, and custody foundations

The tow-yard computer becomes the main management point.

## G1. Business overview

Show:

- current business balance or shared business account
- tow-call income
- storage income
- lien acquisition costs
- auction/Marketplace/salvage proceeds
- property expenses when the shared business system supports them
- fleet count
- custody count
- available capacity

## G2. Money ownership boundary

JOB-09 may calculate and display tow-specific income/expenses.

The canonical shared Career/business money transaction should use the approved Career/RLS bridge or future Business Manager contract. JOB-09 must not invent a fake unrelated currency.

## G3. Capacity upgrades

Later purchase options:

- +5 custody spaces
- +2 fleet spaces
- trailer storage
- heavy storage
- boat storage
- aircraft/oversize storage
- secure impound
- salvage area

## G4. Insurance

Business and fleet insurance is later integration work. The computer may eventually display and manage it through the proper owner job/module.

JOB-09 should not replace the global insurance system.

Exit gate: every money action is recorded once, survives save/reload, and cannot double-pay.

---

# PHASE H — Property Closure, Sale, and Relocation

Priority: later business expansion

## H1. No sale while occupied

A tow yard cannot be sold or closed while it contains:

- company vehicles
- custody vehicles
- trailers/equipment
- active calls
- active listings tied to the yard

Nothing is automatically dumped into a personal garage.

## H2. Relocation planner

Before closing:

- select destination yards
- verify fleet capacity
- verify custody capacity
- verify specialized storage compatibility
- move company vehicles as owned inventory location changes
- move custody records without changing ownership
- preserve history and lien timers

## H3. Two relocation methods

Commercial full-shop relocation:

- move all selected assets for one configurable company relocation price
- do not charge the stock $5,000 once per vehicle

Player-loaded relocation:

- load and drive vehicles manually on the same map
- cross-map loaded reconstruction remains later research

Exit gate: yard cannot close until empty; relocation produces no lost or duplicated records.

---

# PHASE I — Cross-Map Vehicle and Shop Movement

Priority: later

## I1. Simple virtual move

Move a company vehicle or custody record between maps while preserving the same record.

Physical spawn occurs when the destination map is loaded.

## I2. Full-shop move

Move all yard assets to one or more destination yards for a configurable charge.

## I3. Player-loaded cross-map move

Future manifest approach:

- record tractor
- connected trailer
- loaded vehicles
- cargo/load manifest
- attachment/tie-down state where possible
- transition through map gate/port
- reconstruct at destination
- keep recovery snapshot

Do not promise exact BeamNG deformation or attachment reconstruction until proven.

---

# PHASE J — Dispatch, Calls, and Scene Quality

Priority: resumes after computer/property foundation stabilizes

Existing main call types:

1. Standard Car Tow
2. Rolled Car Recovery
3. Semi Rollover Recovery
4. Multi-Vehicle Accident Cleanup
5. Abandoned Vehicle Recovery

## J1. Active-call interface

Show clearly:

- target
- recommended equipment
- service type
- pickup
- destination
- expected pay
- route target
- route drop-off
- details
- cancel

## J2. Vehicle classification

Build verified capability catalog:

- vehicle class
- actual coupler type
- fifth wheel
- kingpin
- ball
- pintle
- gooseneck
- tongue
- tow capability
- size class

Use manual catalog overrides and blacklist/whitelist corrections.

## J3. Scene variety and recent-memory

- avoid repeating the same call and target configuration back-to-back
- preserve mixed accident types
- validate road/shoulder footprint
- prevent crane-chain and boom props from being selected as vehicles
- allow them as lost-prop/road-hazard calls later

## J4. Cleanup and performance

- cleanup all spawned targets, traffic helpers, emergency vehicles, markers, props, and timers
- avoid per-frame logging and saves
- test long sessions for memory/performance degradation
- preserve `beamng.log` and `.1` on crash

Exit gate: focused calls pass one class at a time; no requirement to retest everything for every patch.

---

# PHASE K — Emergency Scene Integration

Priority: later, after the newly found EMS lighting/sound mod is inspected

Research the EMS mod for:

- scene setup code
- emergency vehicle placement
- cones/flares/barriers
- traffic closure/rerouting
- siren/light activation
- smoke/fire/debris
- responder AI
- cleanup hooks

Possible scene templates:

- minor collision: police + cones + tow
- major accident: police + fire + ambulance + lane closure
- semi rollover: heavy rescue + fire + police roadblock
- vehicle fire: fire response + police perimeter + smoke/fire

Use safe APIs/hooks. Do not copy protected code or replace full RLS/traffic files when an extension hook is possible.

---

# PHASE L — Website, Phone, and PC Integration

Priority: after standalone gameplay is stable

JOB-09 owns tow-specific pages and actions.

Public pages:

- Home
- Request Tow
- Track Call
- Services
- Rates
- Locations
- Claim Impound
- Contact

Employee pages:

- Dispatch
- Calls
- History
- Company Fleet
- Tow Yards
- Tow Yard Inventory
- Impounds
- Abandoned/Lien
- Invoices
- Major Incidents
- Relocation
- Fleet Map
- Settings

JOB-01 owns the shared shell, browser/phone host, sessions, routing, and bridge.

---

# PHASE M — QA, Migration, and Release

## M1. Save safety

- Career-specific RedFox save paths
- automatic backups before destructive migration
- transaction snapshots
- undo last transfer/migration
- no duplicate records
- no silent ownership changes

## M2. Compatibility

Test with:

- stock Career where applicable
- current RLS Career version
- other RedFox jobs through documented bridges
- common tow vehicle mods
- traffic/emergency mods

## M3. Status labels

Use only:

- DAVID-TESTED WORKING
- BUILT — RUNTIME UNTESTED
- PARTIAL
- BLOCKED
- FAILED — STOPPED
- MOCKUP/PLACEHOLDER

## M4. Release gate

A release is not accepted until:

- exact ZIP tested
- exact SHA recorded
- save/reload passes
- no protected stock/RLS paths modified
- migration tested
- money paid once
- ownership preserved
- cleanup confirmed
- log evidence reviewed
- GitHub audit updated

## 7. Current priority order

1. Existing property designation
2. Existing property computer integration
3. Custom tow-yard names
4. Remove artificial Tow Yard 1 garage
5. Migrate affected vehicle assignments
6. Company Fleet management through the property computer
7. Free same-property and company transfers
8. Normal RLS retrieval from the same computer
9. Physical five-bay and heavy-spawn mapping
10. Separate custody Tow Yard Inventory
11. Dedicated storage and overflow
12. Three-day lien and disposition
13. Business money and upgrades
14. Property relocation/sale
15. Cross-map movement
16. Dispatch/scene expansion
17. EMS scene integration
18. Website/phone/PC integration
19. QA and release

## 8. Explicitly deferred from the immediate patch

Do not add these to the computer-foundation patch unless required to make the computer work:

- garage-door animation
- bay-to-bay movement
- storage expansion purchasing
- boat/trailer/heavy dedicated storage
- lien conversion
- auction/Marketplace automation
- business insurance
- full money ledger
- property sale
- cross-map loaded transport
- new crash types
- EMS scene generation
- phone/website integration

## 9. Handoff instruction for the next chat

The next chat must begin by reading:

1. GitHub issue #4 and its latest comments.
2. `PROJECT_SOURCE_PATCHES/JOB-09/v0.3.1_RUNTIME_FINDING_EXISTING_PROPERTY_COMPUTER_AND_FAKE_GARAGE_FAILURE_2026-07-27.md`
3. This document.
4. The v0.3.1 source/build audit already stored in the repository.

It must not claim that v0.3.1 property integration works.

It must not continue testing the artificial Tow Yard 1 garage.

It must build the next patch around the existing purchased property's real RLS garage and existing computer.

No further runtime claims are valid until David tests the exact replacement ZIP.
