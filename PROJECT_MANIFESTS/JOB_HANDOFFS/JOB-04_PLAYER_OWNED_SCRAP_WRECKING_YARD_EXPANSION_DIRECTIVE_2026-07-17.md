# JOB-04 — Player-Owned Scrap / Wrecking Yard Expansion Directive

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Feature owner:** JOB-04 — Scrap Yard / Wrecking Yard  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** OWNER-APPROVED LONG-TERM DIRECTION — IMPLEMENT IN PHASES  
**Current runtime state:** CURRENT JOB-04 WEUI/BACKEND CANDIDATE STILL REQUIRES RECOVERY AND TESTING

---

## 1. Core direction

The Scrap Yard / Wrecking Yard should not remain only an online vehicle shop.

It should eventually become a player-owned business that can be bought, built, placed, upgraded, and operated.

The final concept may support:

- buying an existing Scrap/Wrecking Yard;
- building or placing a yard on a suitable player-selected property;
- owning multiple yards later if the save/property system supports it safely;
- receiving vehicles from Tow/Recovery jobs;
- buying damaged, abandoned, salvage, or unwanted vehicles;
- reselling complete vehicles;
- dismantling vehicles for usable parts;
- processing worthless shells through a car crusher;
- selling recovered parts;
- selling loose or processed scrap;
- hauling processed scrap to another buyer or another map;
- legal disposal work;
- illegal disposal of stolen or questionable vehicles as an optional high-risk gameplay path;
- underground parts sales and disposal contracts;
- higher margins because the player owns the yard and cuts out the NPC middleman.

---

## 2. Immediate priority must not change

Do not start with property ownership, crusher simulation, illegal disposal, or cross-map freight.

The first requirement remains:

```text
PROVE THE EXISTING SCRAP YARD BACKEND
```

Required first-stage proof:

1. Open the JOB-04 development WEUI/test panel.
2. Load real RLS/BeamNG vehicle-shopping data on explicit request.
3. Show useful stock and error information.
4. Open the real stock/RLS purchase menu for a selected vehicle.
5. List real owned Career vehicles.
6. Use the real inventory sell path for an explicitly selected owned vehicle.
7. Work without West Coast-only map assumptions.
8. Produce logs proving which calls succeeded or failed.
9. Use the same backend functions that the final website will call.
10. Do not add a startup Career module, map-load generator, fake money, fake ownership, or fake storage.

Only after this stage is stable may JOB-04 begin player-owned-yard systems.

---

## 3. Staged implementation plan

### Phase 1 — Backend and phone/PC parity

Goal:

```text
One proven Scrap Yard backend used by WEUI, phone, and PC.
```

Required behavior:

- backend separated from every UI;
- WEUI can force and inspect operations;
- phone and PC call the same operations and payloads;
- one canonical JOB-01 destination;
- real JOB-02 transactions only;
- no duplicate phone/PC business logic;
- no website integration until the backend passes.

### Phase 2 — Player-owned yard record

Goal:

```text
The player can acquire or establish a Scrap/Wrecking Yard business.
```

Possible acquisition methods:

- purchase a predefined property where supported;
- convert an owned suitable property into a yard;
- place a yard boundary/office marker at the player's selected location on any map;
- use a virtual property record first when a map lacks supported real-estate facilities.

Initial safe target:

- one player yard record per Career profile or per map;
- player-selected yard name;
- map and position record;
- purchase/build cost;
- legal/operating status;
- storage capacity;
- equipment/upgrades;
- yard cashflow and transaction history;
- ability to relocate only through an explicit action;
- no automatic map-load object generation until that pattern is proven safe.

JOB-04 owns the yard-specific gameplay and capability requirements. It must not silently invent a project-wide property system. Any shared property ownership contract requires JOB-00 approval and coordination with the relevant Career/finance jobs.

### Phase 3 — Legal yard operation

Goal:

```text
Operate a legitimate salvage, wrecking, parts, and scrap business.
```

Vehicle intake sources may include:

- vehicles purchased through the Scrap Yard marketplace;
- player-owned vehicles deliberately sold or transferred to the yard;
- abandoned vehicles delivered by JOB-09;
- insurance or total-loss vehicles if future approved contracts expose them;
- direct customer disposal jobs;
- fleet disposal contracts;
- auction or salvage acquisitions from future approved systems.

Player decisions for each accepted vehicle:

- sell whole;
- repair later;
- store;
- dismantle for parts;
- strip selected valuable components;
- crush the remaining shell;
- export or haul as scrap.

### Phase 4 — Parts and material inventory

Goal:

```text
Recovered value depends on what the player saves before crushing.
```

Potential recoverable categories:

- engines;
- transmissions;
- transfer cases;
- differentials;
- wheels and tires;
- suspension assemblies;
- body panels;
- lights and glass;
- interior parts;
- electronics;
- batteries;
- catalytic/exhaust components where represented as fictional game items;
- reusable generic parts bundles;
- ferrous scrap;
- non-ferrous scrap;
- crushed vehicle bales.

Implementation rule:

Do not pretend every BeamNG part automatically exists as a tradable Career item. JOB-04 must inspect available vehicle part/configuration data and create a controlled salvage record format. Shared inventory mutations must use approved JOB-02 or other owner-approved contracts.

### Phase 5 — Car crusher gameplay

Goal:

```text
Give the in-game car crusher a real economic purpose.
```

Required crusher safeguards:

1. Confirm a valid target vehicle is inside the crusher/work zone.
2. Require the vehicle to be stationary and not the active player vehicle unless explicitly confirmed.
3. Record model, configuration, ownership, source, value, and legal status before destruction.
4. Prevent processing the same vehicle twice.
5. Prevent duplication through save/reload or failed destruction.
6. Remove or finalize the vehicle only after the transaction record succeeds.
7. Produce a calculated scrap/material output.
8. Preserve any parts already removed from the vehicle.
9. Log the complete transaction.
10. Provide a recoverable failure state if processing stops midway.

Possible outputs:

- loose scrap weight/value;
- one or more crushed bales;
- reusable parts already removed;
- disposal certificate for legal work;
- hidden disposal record/heat change for illegal work.

The car crusher must not merely delete a vehicle and award arbitrary money.

### Phase 6 — Player-owned profit model

The player-owned yard should pay more than selling to an NPC Scrap Yard because the player removes the middleman.

Balance should come from:

- property acquisition or build cost;
- crusher and equipment upgrades;
- transport costs;
- storage capacity;
- processing time or explicit work steps;
- risk of holding unsold vehicles/parts;
- market variation;
- reduced whole-vehicle value after stripping parts;
- legal fees or disposal costs where appropriate;
- illegal heat/risk where applicable.

Basic value choices:

```text
Sell immediately to NPC yard = lowest payout, fastest and simplest.
Sell whole from player yard = higher margin if a buyer exists.
Dismantle and sell parts = potentially highest value but more work/storage.
Crush shell and sell scrap = reliable final value after parts recovery.
Haul processed scrap to a distant buyer = higher payout with freight effort.
```

### Phase 7 — Illegal disposal and underground parts

Goal:

```text
Optional high-risk/high-reward gameplay connected to UndergroundNet.
```

Possible jobs:

- dispose of a stolen vehicle;
- destroy a vehicle tied to a criminal contract;
- strip valuable parts before disposal;
- sell questionable parts through an underground market;
- store a hot vehicle temporarily;
- falsify or obscure the public-facing yard record only as fictional game-state mechanics;
- accept rush disposal deadlines;
- hide evidence from fictional inspections or heat systems.

Required boundaries:

- keep legal and illegal transactions separately tagged;
- illegal vehicle intake must come from an approved gameplay source/contract, not arbitrary real-world instructions;
- include fictional heat, reputation, inspection, and payout consequences;
- risk must increase with repeated illegal use;
- legal customers and insurance/fleet contracts may be harmed by a dirty reputation;
- no illegal system should be required for normal yard progression;
- do not expose real-world crime guidance; this is game-specific fictional behavior only.

Potential integrations:

- UndergroundNet pages;
- future Chop Shop / Parts Exchange backend;
- stolen-vehicle missions;
- JOB-09 recovery/delivery contracts;
- future police/heat/paperwork systems;
- JOB-12 notifications or messages if approved.

### Phase 8 — Cross-map scrap trucking

Goal:

```text
Process scrap on one map and haul it to a buyer on another map.
```

Because BeamNG map changes do not reliably preserve arbitrary world vehicles and cargo physically, the initial cross-map design should use a saved cargo manifest.

Recommended pattern:

1. Load crushed bales or scrap cargo at the player yard.
2. Record cargo type, weight, value, origin map, origin yard, destination, and carrier vehicle/trailer.
3. Leave the origin map through an approved travel/freight action.
4. Load the destination map.
5. Recreate or validate the cargo at the destination entry point.
6. Deliver to a mill, export yard, foundry, recycler, port, or buyer.
7. Pay only after destination validation.
8. Mark the manifest complete to prevent duplication.

Potential destination owners:

- JOB-06 Import / Export Yard for port/export buyers;
- a future freight/logistics owner for mills and industrial buyers;
- JOB-04 for Scrap Yard-owned internal transfers;
- JOB-09 for special recovery-haul contracts.

First cross-map version should use one controlled cargo type and one destination contract before adding multiple materials.

---

## 4. Yard upgrades and equipment

Possible upgrades, implemented only after core ownership works:

- larger vehicle storage;
- parts racks and warehouse capacity;
- vehicle lift;
- dismantling bay;
- engine/transmission storage;
- tire storage;
- fluid-drain station as fictional gameplay state;
- weigh scale;
- car crusher;
- scrap loader/forklift support;
- truck scale;
- office/computer upgrades;
- security and lighting;
- legal compliance upgrade path;
- hidden underground storage;
- additional yard lots;
- export loading area.

Upgrades should unlock capability, capacity, speed, or better margins rather than being decorative only.

---

## 5. Cross-job ownership

### JOB-04 owns

- Scrap/Wrecking Yard backend;
- player yard business record;
- yard-specific acquisition/build rules;
- yard upgrades and equipment state;
- vehicle intake and disposition decisions;
- dismantling and salvage records;
- crusher processing;
- parts/scrap/bale inventory specific to the yard;
- legal and illegal yard transaction records;
- yard-specific payouts and pricing requests through shared contracts;
- yard website integration;
- WEUI test controls;
- all-map yard behavior;
- Scrap Yard receiving side of Tow/Recovery deliveries.

### JOB-09 owns

- generating and operating Tow/Recovery calls;
- transporting recoveries to a selected Scrap/Wrecking Yard;
- tow-specific mission completion and history;
- handoff of delivered vehicle identity/status to JOB-04.

### JOB-06 may later own

- export buyer/port destinations;
- import/export-specific market presentation;
- export-side receipt of processed scrap cargo.

### JOB-02 owns

- approved shared Career/RLS money operations;
- ownership and inventory operations;
- transaction/result contracts;
- shared error and capability reporting.

### JOB-01 owns

- phone/PC app registration;
- one canonical Scrap Yard destination;
- common host/navigation behavior.

### JOB-08 may later provide

- financing or insurance page integrations for yard property/equipment;
- read-only display of approved property/business policy data;
- no direct ownership of JOB-04 gameplay.

### JOB-10 owns

- final visual presentation of legal Scrap Yard/Wrecking Yard and any approved underground-facing pages.

### JOB-11

- remains intentionally parked until David assigns a specific QA task;
- later validates exact candidates, logs, duplication safeguards, removal behavior, and cross-map manifest integrity.

### JOB-00 owns

- shared property/cargo contract approval;
- dependency order;
- integration gates;
- collision checks;
- final assembly approval.

---

## 6. Required save records

Exact schemas will be designed later, but the system should ultimately preserve:

- yard ID and name;
- Career profile ID;
- map and location;
- acquisition/build method;
- purchase/build cost;
- upgrade/equipment state;
- storage capacity;
- stored vehicles;
- each vehicle's source and legal status;
- removed/recovered parts;
- scrap and bale inventory;
- transaction history;
- crusher history;
- legal disposal certificates;
- illegal disposal records/heat where supported;
- cargo manifests;
- destination and payment state;
- version/migration information.

Every destructive or payout-producing action needs an idempotent transaction identifier to prevent duplicate money, duplicate scrap, or repeated destruction after save/load.

---

## 7. Required development WEUI controls

The development UI should eventually provide separate tabs or sections for:

```text
Backend status
Vehicle shopping data
Owned vehicle list
Yard ownership/status
Stored yard vehicles
Vehicle intake/disposition
Recovered parts
Scrap/material inventory
Crusher test controls
Cargo manifests
Legal/illegal status
Transactions and logs
Capability/errors
```

The WEUI remains a test/developer interface. The final website must call the same backend service functions.

---

## 8. Hard stop rules

Do not:

- create a startup-loaded Scrap Yard Career module;
- scan or generate yards automatically at map load;
- create parking spots or facilities at map load;
- use direct spawning as completed purchase;
- invent fake Career money, ownership, garage, or storage;
- destroy vehicles without first recording identity and transaction state;
- award both whole-vehicle sale value and full parts/scrap value for the same vehicle;
- allow cargo or crusher duplication through save/reload;
- build illegal disposal before the legal backend and yard records work;
- block the current backend proof while designing the full business;
- require West Coast USA;
- overwrite JOB-01, JOB-02, JOB-06, JOB-09, JOB-10, or another job's files.

---

## 9. Restart order

When David returns:

1. Recover or rebuild the current JOB-04 WEUI test ZIP.
2. Reopen and statically verify it.
3. Test the exact ZIP in BeamNG with only one FoxNet ecosystem package enabled.
4. Record the backend calls that work and fail.
5. Fix only the backend/WEUI proof first.
6. Prove the same functions from phone and PC.
7. Connect the approved Scrap/Wrecking Yard website.
8. Design the minimum player-owned yard record.
9. Add a non-destructive vehicle intake/storage proof.
10. Add dismantling/material records.
11. Add crusher processing with duplication safeguards.
12. Add legal freight/cargo manifests.
13. Add optional illegal disposal only after the legal loop passes.

---

## 10. Current truth status

```text
PLAYER-OWNED/BUSINESS DIRECTION: APPROVED
BUYABLE OR BUILDABLE YARD: PLANNED
LEGAL SALVAGE LOOP: PLANNED
PARTS MARKET: PLANNED
CAR CRUSHER ECONOMY: PLANNED
ILLEGAL DISPOSAL: PLANNED OPTIONAL PATH
CROSS-MAP SCRAP TRUCKING: PLANNED
CURRENT JOB-04 BACKEND: PARTIALLY HISTORICALLY WORKING / NEW WEUI CANDIDATE RUNTIME UNTESTED
NO NEW RUNTIME IMPLEMENTATION CREATED BY THIS DIRECTIVE
```
