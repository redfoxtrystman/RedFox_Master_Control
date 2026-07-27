# JOB-09 Canonical Roadmap After Audit

**Date:** 2026-07-27  
**Job:** `19 — JOB-09-RedFox_TowRecoveryDispatch`  
**Module:** `redfox_tow_recovery_dispatch`  
**Primary issue:** #4

## 1. Canonical current state

### Current tested build

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_1_RLSTowShopGarageBridge.zip`

SHA-256:

`662db67fc190ede9c529391c39570e93883c2c7024ebb2edb8c700837f5c4aec`

Property/garage status:

**FAILED — STOPPED**

Confirmed runtime failure:

- v0.3.1 created a separate artificial `Tow Yard 1` garage;
- the actual purchased service property already used `servicestationGarage`;
- the normal property computer therefore treated the company vehicle as remote;
- the UI offered the stock $5,000 Deliver action;
- the stock approximately 120-second delivery delay was applied;
- the generated Fleet Computer was not the correct property-management access point.

### Quarantined version

`v0.3.2` has conflicting GitHub records. Some commits claim it was built and distributed, while a later canonical handoff says v0.3.1 remained current and v0.3.2 was still next.

Status:

**PROVENANCE CONFLICT — QUARANTINED**

Do not reuse or distribute v0.3.2 until the exact artifact and full source are recovered and matched.

### Next allowed version

`v0.3.3`

The next patch must not be named v0.3.2.

## 2. Completed and attempted development history

### v0.2.0 — Call chooser and yard baseline

- Core tow dispatch UI and call selection.
- Early tow-yard support.
- Transferred concern: abandoned call lacked a usable route/location.

### v0.2.1 — Rollover scenes and multiple yards

- Added rollover and multi-yard work.
- Runtime accident test exposed unrealistic scene placement and oversized targets in a compact lot.

### v0.2.2 — Passenger-only accident fit guard

- Added passenger filtering and adjacent parking-space placement.
- Rejected because mixed heavy accident targets were valid and the real issue was scene footprint/location.

### v0.2.3 — Roadside mixed scenes

- Moved accident and recovery scene anchors to roads, shoulders, and roadside areas.
- Restored mixed target classes.
- Added scene plans for lane collisions, rollovers, jackknifes, semi crashes, heavy wrecks, and rare bus crashes.
- Added random-event provider evidence probe.

### v0.2.4 — Cataloged history

- Reorganized tow history into useful categories.
- Preserved older records.
- Added richer record details.

### v0.2.5 — Fleet identity and hazard sites

- Added Tow Fleet Book identity records.
- Added roles, callsigns, model/config, and paint capture.
- Added map-aware road, intersection, curve, and grade scanning.

### v0.2.6 — Multiple unbumped states

- Police impound/emergency-scene work.
- Selection and spawn repairs.
- Pause/read-first addenda.
- Audit finding: version identifier was reused.

### v0.2.7 — Multiple unbumped states

- RLS progression and personal-claim work.
- Later Spam Guard / Dispatch Variety build.
- Audit finding: version identifier was reused.

### v0.2.8 — Multiple unbumped states

- Career-day clock and asset-manager work.
- Later Temporary Vehicle Spawn Lab.
- Audit finding: version identifier was reused.

### v0.2.9 — Multiple unbumped states

- Active-call recovery work.
- Later Company Fleet Garage / Yard Organization build.
- Audit finding: version identifier was reused.

### v0.3.0 — Catalog overrides and yard test storage

- Added target/config corrections and blacklist behavior.
- Added broader category handling.
- Added yard search and test-storage work.
- Runtime company transfer design proved unsafe: vehicles could disappear from normal owned access and ownership could break.

### v0.3.1 — RLS tow-shop garage bridge

- Attempted to keep company vehicles as one owned RLS inventory record.
- Added five company slots and ten custody slots.
- Added transfer, reverse, undo, and legacy recovery concepts.
- Runtime test proved the artificial garage/computer architecture wrong for an existing purchased property.

### v0.3.2 — Quarantined records

- GitHub records describe an existing-property computer patch.
- Exact current artifact is unavailable and repository status is contradictory.
- No runtime claim is accepted.

## 3. Owner-approved architecture

## 3.1 Existing property is the tow yard

When an accessible RLS property is designated as a tow yard:

- its existing RLS garage ID becomes the company garage location;
- its existing property computer is the management computer;
- RedFox stores a separate tow-business yard ID and custom name;
- no second artificial garage is created;
- no second fake computer is required.

Example:

```text
RedFox yard ID: redfox_tow_yard_001
Custom name: Belasco Tow & Recovery
RLS garage ID: servicestationGarage
Map: west_coast_usa
Computer ID: existing computer linked to servicestationGarage
```

## 3.2 Two inventories at one property

### Normal RLS owned inventory

Contains company-owned vehicles:

- tow trucks;
- rollbacks;
- wreckers;
- rotators;
- service trucks;
- company tractors and trailers.

Rules:

- one normal RLS inventory record;
- same inventory ID;
- `owned=true` remains unchanged;
- garage movement changes location only;
- Company Fleet is a filtered view plus RedFox metadata.

### Separate RedFox custody inventory

Contains vehicles not owned by the player/company:

- abandoned vehicles;
- police impounds;
- unpaid customer vehicles;
- lien-eligible vehicles;
- other recovered custody records.

These do not appear in normal My Vehicles until the player performs a lien claim or another approved ownership conversion.

## 3.3 Starting capacity

Every tow yard begins with:

- 5 company fleet slots;
- 10 universal custody slots.

Paid expansion is later work.

## 4. Immediate v0.3.3 scope — Property computer foundation

Everything else remains on hold until this passes.

### Required behavior

1. Designate the current purchased/accessible RLS property as a tow yard.
2. Save the existing RLS garage ID instead of creating `redfox_towshop_*`.
3. Detect the existing computer linked to that garage.
4. Add RedFox functions through the normal computer-function hook.
5. Preserve all stock RLS computer options.
6. Allow the user to rename the tow yard.
7. Open a Tow Yard Management screen from the existing computer.
8. Open a Company Fleet screen from the existing computer.
9. Open a Tow Yard Inventory summary from the existing computer.
10. Migrate old artificial Tow Yard 1 owned-vehicle locations to the real property garage ID.
11. Keep the same inventory ID and `owned=true`.
12. Do not charge $5,000 for a RedFox same-property transfer.
13. Do not apply the stock 120-second delivery delay.
14. Make a vehicle already assigned to the property show Retrieve/Replace rather than Deliver.
15. Remove or disable the v0.3.1 artificial Fleet Computer only after safe migration.
16. Do not add business insurance, property sale, physical door animation, or new emergency scenes in this focused patch.

### Existing computer target menu

```text
Normal RLS functions
- My Vehicles
- Vehicle and Parts Management
- Insurance Management
- Other property functions

RedFox functions
- Tow Yard Management
- Company Fleet
- Tow Yard Inventory
```

### Tow Yard Management first-pass content

- custom yard name;
- map;
- linked RLS garage ID;
- linked property/computer ID;
- company slots used / 5;
- custody slots used / 10;
- rename yard;
- migrate old artificial yard records;
- refresh current data;
- open Company Fleet;
- open Tow Yard Inventory.

Detailed money, insurance, upgrades, and employee systems remain placeholders until their owning systems are defined.

## 5. v0.3.3 focused test gate

Use one noncritical owned vehicle and the Belasco service property.

### Property link

1. Enable only v0.3.3.
2. Back up the Career save and `settings/redfox/`.
3. Load West Coast.
4. Use the existing service-property computer.
5. Designate or link the property as the tow yard.
6. Confirm the saved garage ID is `servicestationGarage`.
7. Confirm no artificial `redfox_towshop_*` garage or second Fleet Computer appears.
8. Rename the yard.
9. Save, reload, and confirm the name remains.

### Computer access

1. Reopen the existing property computer.
2. Confirm all normal RLS options remain.
3. Confirm Tow Yard Management appears.
4. Confirm Company Fleet appears.
5. Confirm Tow Yard Inventory appears.
6. Confirm each opens for the correct linked yard.

### Company vehicle transfer

1. Record one vehicle's inventory ID, ownership, current garage, configuration, paint, condition, mileage, insurance, and thumbnail.
2. Use RedFox Transfer to This Tow Yard.
3. Confirm no money is charged.
4. Confirm no 120-second delay starts.
5. Confirm the same inventory ID remains.
6. Confirm ownership remains true.
7. Confirm one copy appears under `servicestationGarage` in My Vehicles.
8. Confirm Retrieve or Replace appears at the property computer.
9. Retrieve and store it successfully.

### Stop immediately when

- vehicle disappears;
- duplicate appears;
- ownership becomes false;
- inventory ID changes;
- stock computer options disappear;
- RedFox opens for the wrong garage;
- $5,000 is charged;
- delivery countdown starts;
- artificial Tow Yard 1 remains active;
- vehicle retrieves at the wrong location.

## 6. Ordered future roadmap

## Phase A — Property and computer foundation

- Complete v0.3.3 scope.
- Stable property/garage/computer linking.
- Custom tow-yard naming.
- Safe v0.3.1 migration.

## Phase B — Company Fleet management

- Filter normal owned RLS vehicles by RedFox company assignment.
- Callsign, role, yard, notes, availability.
- Personal garage to tow yard, tow yard to tow yard, and tow yard to personal transfers.
- Immediate save and one-step undo.
- Global `Move to Tow Yard` action only after the safer computer flow works.

## Phase C — Custody Tow Yard Inventory

- Non-owned abandoned/impound/customer/lien records.
- Search, sort, categories, history, thumbnails.
- Transfer between tow yards.
- No normal Career ownership until lien claim.

## Phase D — Storage routing and capacity

- Ten universal custody slots accept every category.
- Five company slots.
- Full yard automatically recommends another owned yard.
- Universal storage prevents losing a job.
- Temporary overflow is the final safety net.

## Phase E — Dedicated storage upgrades

- trailer;
- heavy vehicle;
- boat;
- aircraft/oversize;
- secure impound;
- salvage.

Routing order:

1. matching dedicated storage at selected/closest yard;
2. matching dedicated storage at another yard on current map;
3. universal storage at selected/closest yard;
4. universal storage at another yard;
5. temporary overflow.

When dedicated storage is bought, matching vehicles automatically use it first. When full, they use universal overflow.

## Phase F — Three-day lien and disposition

- Lien eligibility after three Career days.
- Player claim cost capped at tow charge plus exactly three storage days.
- Waiting 100 days does not increase the player's claim cost.
- Leave in storage, claim, NPC Marketplace, NPC auction, salvage, scrap, or transfer.
- Lien history added permanently to the vehicle-history/Carfax-style record after conversion.
- No courts or paperwork simulator.
- No player-to-player sales.

## Phase G — Yard sale, closing, and relocation

- Cannot sell/close a yard while company or custody vehicles remain.
- Nothing is dumped into personal storage.
- Move vehicles to other yards first.
- Full-shop paid relocation option.
- Manual loaded relocation on the current map.
- Cross-map loaded-manifest transport only after reliable reconstruction exists.

## Phase H — Physical bays and yard objects

- Investigate the five numbered garage doors on the service property.
- Reuse or add safe parking spots.
- Map five starting company slots to valid bays/areas when possible.
- Keep heavy vehicles outside when needed.
- Determine whether doors are animated objects, swappable objects, or part of a combined model.
- Door animation is not required before the computer and inventory systems work.

## Phase I — Dispatch, scenes, and emergency integration

- Continue catalog/coupler correction.
- Better mixed crash scenes.
- Police/fire/EMS placement.
- Cones, flares, barriers, traffic control, cleanup.
- Inspect external emergency-lighting/sound mods only after the property-computer foundation is stable.

## Phase J — Business and connected platform integration

- Tow-business money view.
- Storage revenue and disposition income.
- Later business insurance.
- Website/phone/PC pages through the shared platform.
- Employees and passive business income only through the assigned Business Manager architecture.

## 7. Mandatory release sequence for v0.3.3 and later

1. Read this canonical roadmap and the audit.
2. Reserve one unused version number.
3. Commit the exact full unpacked source snapshot.
4. Build only from that commit.
5. Run static verification.
6. Create one release manifest containing source SHA, ZIP hash, size, and status.
7. Update issue #4 before user-facing delivery.
8. Deliver the exact ZIP.
9. Record David's runtime result against that exact hash.
10. Update this canonical status before beginning another version.
11. Never reuse a version number.
