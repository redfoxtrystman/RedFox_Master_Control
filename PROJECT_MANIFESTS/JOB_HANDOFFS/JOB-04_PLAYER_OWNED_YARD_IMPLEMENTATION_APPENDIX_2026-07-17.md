# JOB-04 — Player-Owned Yard Implementation Appendix

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Applies to:** JOB-04 — Scrap Yard / Wrecking Yard  
**Companion to:** `JOB-04_PLAYER_OWNED_SCRAP_WRECKING_YARD_EXPANSION_DIRECTIVE_2026-07-17.md`

---

## 1. Cross-map scrap trucking

The final business should allow processed scrap to be hauled from the player's yard to a buyer on another map.

BeamNG map changes may not safely preserve arbitrary physical cargo or world vehicles. The first implementation should therefore use a saved cargo manifest rather than pretending the same physical object survived the map change.

Recommended flow:

1. Load crushed bales or another approved scrap cargo at the yard.
2. Record cargo type, weight, value, origin map, origin yard, destination, carrier vehicle/trailer, and a unique transaction ID.
3. Leave the origin map through an approved travel/freight action.
4. Load the destination map.
5. Recreate or validate the cargo at the destination entry point.
6. Deliver to a mill, recycler, port, foundry, export yard, or other approved buyer.
7. Pay only after destination validation.
8. Mark the manifest complete before allowing another payout.

Potential owners and endpoints:

- JOB-04: Scrap Yard-owned internal transfers and origin cargo creation.
- JOB-06: port/export buyer and export-market destination.
- JOB-09: special recovery-haul or yard-delivery contracts.
- Future freight/logistics system: industrial delivery framework if one is formally assigned.

The first cross-map proof should use one cargo type and one destination contract.

---

## 2. Yard upgrades and equipment

Possible upgrades after yard ownership works:

- vehicle storage expansion;
- parts racks and warehouse capacity;
- vehicle lift;
- dismantling bay;
- engine/transmission storage;
- wheel and tire storage;
- weigh scale;
- car crusher;
- scrap loader or forklift support;
- truck scale;
- office/computer upgrade;
- security and lighting;
- legal compliance upgrade;
- hidden underground storage;
- additional yard lots;
- export loading area.

Upgrades should unlock capabilities, capacity, processing options, or better margins rather than being decoration only.

---

## 3. Cross-job ownership

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
- yard-specific pricing and payout requests through approved shared contracts;
- yard website integration;
- WEUI test controls;
- all-map yard behavior;
- Scrap Yard receiving side of Tow/Recovery deliveries.

### JOB-09 owns

- generating and operating Tow/Recovery calls;
- transporting recoveries to the selected yard;
- tow-specific mission completion and history;
- handing delivered vehicle identity/status to JOB-04.

### JOB-06 may later own

- export buyer/port destinations;
- export-market presentation;
- export-side receipt of processed scrap cargo.

### JOB-02 owns

- approved Career/RLS money operations;
- shared ownership and inventory operations;
- transaction/result contracts;
- shared error and capability reporting.

### JOB-01 owns

- phone and PC registration;
- one canonical Scrap Yard destination;
- host/navigation behavior.

### JOB-08 may later provide

- financing or insurance page integrations for yard property/equipment;
- read-only display of approved property/business policy data;
- no direct ownership of JOB-04 gameplay.

### JOB-10 owns

- final visual presentation for legal and approved underground-facing yard pages.

### JOB-11

- remains intentionally parked until David assigns an exact QA task;
- later validates candidates, duplication safeguards, removal behavior, logging, and cross-map manifest integrity.

### JOB-00 owns

- shared property/cargo contract approval;
- dependency order;
- integration gates;
- collision checks;
- final assembly approval.

---

## 4. Required save records

The eventual save format should preserve:

- yard ID and name;
- Career profile ID;
- map and location;
- acquisition/build method;
- purchase/build cost;
- equipment and upgrade state;
- storage capacity;
- stored vehicles;
- vehicle source and legal status;
- removed/recovered parts;
- scrap and bale inventory;
- transaction history;
- crusher history;
- legal disposal certificates;
- illegal disposal/heat records where supported;
- cargo manifests;
- destination and payment state;
- schema version and migrations.

Every destructive or payout-producing action requires an idempotent transaction identifier so save/load cannot duplicate money, parts, scrap, cargo, or vehicle destruction.

---

## 5. Required development WEUI sections

The test UI should eventually expose:

```text
Backend status
Vehicle shopping data
Owned vehicle list
Yard ownership/status
Stored yard vehicles
Vehicle intake/disposition
Recovered parts
Scrap/material inventory
Crusher controls
Cargo manifests
Legal/illegal status
Transactions and logs
Capabilities and errors
```

The WEUI is a developer/test interface. The final website must call the same backend services.

---

## 6. Hard stop rules

Do not:

- create a startup-loaded Scrap Yard Career module;
- scan or generate yards automatically at map load;
- create parking spots or facilities at map load;
- treat direct spawning as a completed purchase;
- invent fake Career money, ownership, garage, or storage;
- destroy vehicles without recording identity and transaction state first;
- award whole-vehicle value plus full parts and scrap value for the same vehicle;
- allow crusher or cargo duplication through save/reload;
- build illegal disposal before the legal backend and yard records work;
- block the immediate backend proof while designing the complete business;
- require West Coast USA;
- overwrite another job's files.

---

## 7. Restart order

When work resumes:

1. Recover or rebuild the current JOB-04 WEUI test ZIP.
2. Reopen and statically verify it.
3. Test the exact ZIP with only one FoxNet ecosystem package enabled.
4. Record which backend calls work and fail.
5. Fix the backend/WEUI proof first.
6. Prove the same functions from phone and PC.
7. Connect the approved Scrap/Wrecking Yard website.
8. Design the minimum player-owned yard record.
9. Add a non-destructive vehicle intake/storage proof.
10. Add dismantling and material records.
11. Add crusher processing with duplication safeguards.
12. Add legal cargo manifests and one cross-map destination.
13. Add optional illegal disposal only after the legal loop passes.

---

## 8. Current truth status

```text
PLAYER-OWNED BUSINESS DIRECTION: APPROVED
BUYABLE OR BUILDABLE YARD: PLANNED
LEGAL SALVAGE LOOP: PLANNED
PARTS MARKET: PLANNED
CAR CRUSHER ECONOMY: PLANNED
ILLEGAL DISPOSAL: PLANNED OPTIONAL PATH
CROSS-MAP SCRAP TRUCKING: PLANNED
CURRENT JOB-04 BACKEND: HISTORICALLY PARTIAL / NEW WEUI CANDIDATE RUNTIME UNTESTED
NO NEW RUNTIME IMPLEMENTATION CREATED BY THIS APPENDIX
```
