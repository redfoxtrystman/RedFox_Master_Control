# READ FIRST — RLS WEEKLY UPDATE / COMPATIBILITY POLICY

**Date:** 2026-09-08
**Scope:** ALL RedFox BeamNG chats/jobs that touch RLS Career Overhaul APIs, Career inventory, garages, facilities, recovery, businesses, saves, insurance, part inventory, vehicle shopping, or native Career vehicle creation/transfer.
**Status:** MANDATORY CROSS-CHAT ARCHITECTURE POLICY

## Current version picture

- **RLS 2.7.0.1 = current production version in the owner's active environment.**
- **RLS 2.7.1 = new migration target being uploaded/audited now.**
- RLS updates approximately weekly, so RedFox mods must be made easier to migrate instead of scattering direct RLS calls throughout each job.

## Required architecture direction

RedFox business/gameplay logic should not directly own every RLS-specific implementation detail.

Target architecture:

```text
Tow / Car Lot / KoParts / other RedFox business logic
        ↓
Shared RedFox RLS compatibility adapter / native vehicle transaction layer
        ↓
Exact supported RLS native APIs for the installed version
```

The compatibility layer should be the preferred boundary for:

- owned-garage discovery and capacity;
- native Career inventory creation;
- same-inventory-ID moves between normal garages and RedFox pseudo-locations;
- part inventory/originalParts completion and verification;
- insurance registration;
- vehicle condition capture and restoration;
- Recovery reward/vehicle-award conversion;
- facilities/property lookup;
- business/account hooks;
- Career save calls and verification;
- rollback/quarantine/idempotent transaction handling.

Do **not** blindly duplicate RLS internals into every job.

## Version-audit requirement

Before claiming compatibility with a new RLS release:

1. inspect the exact old supported RLS source;
2. inspect the exact new RLS source;
3. diff the relevant Career/Recovery/inventory/garage/save/business APIs;
4. classify each dependency as unchanged / moved / behavior-changed / obsolete / replaced by a better native RLS path;
5. update the compatibility adapter first where feasible;
6. then update job-specific code only when necessary;
7. record the result on GitHub before delivery;
8. label runtime status truthfully until owner testing.

## Current JOB-09 / Tow direction

- **Tow v0.5.0.39 remains the fallback/rollback baseline.**
- v40b/v40c are failed branches and must not be used as the foundation.
- Current immediate target is a narrow **Tow custody → selected currently-owned native garage** transaction.
- Do not hardcode `Commercial Garage`; it is only the owner's current preferred garage on one save/map. Enumerate garages actually owned by the current Career save and respect native capacity.
- Tow custody vehicles may behave like KoParts Bought Vehicles before delivery: they can carry a real/exact vehicle identity/configuration/condition without yet being installed as a normal owned Career garage vehicle.
- Once legally claimed/awarded, create/verify the native Career vehicle and only remove the custody record after native registration, destination assignment, save, and verification succeed.
- Already-owned Tow fleet vehicles should later use a Car-Lot-style pseudo-location while preserving the same native Career inventory ID; do not return to the old `businessInventory` delete/recreate architecture.
- Tow Yard custody storage and Tow Fleet owned-vehicle storage remain distinct systems.

## KoParts warning — do not copy transfer code blindly

Current KoParts 64A has approximately 15 owner-reported vehicles stuck in the **Bought Vehicles** list that cannot be transferred.

Known diagnosis to verify directly in source before reuse:

- some purchases reach Career inventory before RLS native parts/original-parts/insurance/value lifecycle is complete;
- current repair can become circular by trying to rebuild missing `originalParts` from missing native Part Inventory;
- a vehicle can therefore be partly real/native but remain incomplete/stuck in KoParts delivery state.

Before using KoParts as a reference, audit the full state machine:

```text
auction won → paid → vehicle spawned → native inventory created →
parts/originalParts/insurance/value verified → destination selected →
Car Lot/garage transfer verified → Bought Vehicles source entry cleared
```

Good native-creation code may be reusable; broken delivery/recovery assumptions are not.

## Car Lot proven pattern

Current Car Lot 64A contains a proven business pseudo-location pattern that preserves the exact native Career inventory record rather than deleting/recreating it.

Conceptually:

```text
nativeVehicle.location = redfox business pseudo-location
nativeVehicle.niceLocation = business display name
mark native vehicle dirty
save
```

This is the preferred reference for future Tow Fleet storage.

## RLS Recovery system priority

RLS 2.7.1 contains newer Recovery behavior that may preserve the live vehicle's actual damaged/current part condition and may award that vehicle into the player's Career inventory/garage.

Before writing a new RedFox vehicle-reconstruction system, inspect and prefer the exact native RLS Recovery award lifecycle if it safely provides:

1. recovery vehicle spawn;
2. live condition tracking;
3. damage-during-recovery capture;
4. payout reduction by damage;
5. exact part-condition snapshot;
6. native owned-Career vehicle award;
7. originalParts / Part Inventory creation;
8. insurance registration;
9. garage assignment;
10. save verification;
11. full-garage/failure handling;
12. retry/rollback protection.

This may become the common safe path for Tow custody awards and KoParts hard rebuilds.

## Cross-chat migration rule

Do not spend substantial time polishing version-specific code that is expected to be discarded during the 2.7.1 migration. Get the architecture/data boundaries correct on 2.7.0.1, then migrate through the shared adapter.

UI polish, employee/NPC systems, and broader business progression should remain decoupled from RLS where possible.

## Future employee systems

Tow and Car Lot employee RPG systems should live primarily in RedFox-owned data and should not depend heavily on RLS internals. Planned Tow roles may include dispatchers, tow operators/drivers, recovery specialists, heavy/rotator operators, yard staff, service technicians, and operations/service managers, with skills, bonuses, negatives, wages, portraits/dossiers, and XP/level progression. Actual NPC driving/towing should be staged later after business/storage/vehicle transactions are reliable.

## Progression / startup to-do

Future saves should not automatically receive fully operational Tow, Car Lot, and KoParts money-making businesses for free. Add startup/unlock costs or progression requirements later, after transfer/storage reliability is proven.

## Required compatibility status records

Maintain a durable compatibility table as RLS updates arrive, for example:

```text
RLS 2.7.0.1 — current production baseline
RLS 2.7.1   — migration audit in progress
future RLS  — audit pending
```

No chat may call a RedFox mod compatible with a new RLS release until the exact release has been directly audited and the owner has runtime-tested the relevant candidate.
