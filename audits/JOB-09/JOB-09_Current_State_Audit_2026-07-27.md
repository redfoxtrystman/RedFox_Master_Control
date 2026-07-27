# JOB-09 Current-State Audit — Property Computer Priority

**Date:** 2026-07-27  
**Job:** `19 — JOB-09-RedFox_TowRecoveryDispatch`  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Primary coordination issue:** `#4`

## 1. Audit purpose

This record preserves the latest owner decisions, runtime evidence, version status, and immediate development priority so the work is not lost during chat handoff.

This audit is documentation only. It does not claim that any new runtime patch was built or tested from the latest discussion.

## 2. Repository state found during audit

The repository already contained:

- a complete JOB-09 end-of-chat handoff and roadmap;
- a v0.3.1 property/garage runtime-failure record;
- v0.3.2 property-computer build records and static-verification notes;
- an artifact-recovery record preserving v0.3.0 and v0.3.1 hashes;
- the JOB-09 coordination issue with prior runtime findings.

The v0.3.2 artifact is recorded as:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_2_PropertyTowYardComputer.zip`

- SHA-256: `c01965e54174572235a4c419c6b7557d58f6d7940435b2f43330c51f6cf8cee1`
- Size: 237,789 bytes
- Static status: PASS
- Runtime status: not established in this chat

The user-confirmed rollback baseline remains v0.3.0. The v0.3.1 artificial-garage property design is failed and stopped.

## 3. Runtime evidence that must remain attached to the project

### v0.3.1 property/garage failure

Observed behavior:

- The mod created an artificial garage called `Tow Yard 1`.
- The purchased Belasco service property already used the real RLS garage ID `servicestationGarage`.
- The vehicle could show `Location: Tow Yard 1`, while the computer at the actual property treated it as remote.
- The normal RLS computer offered **Deliver** for `$5,000`.
- Accepting Deliver started the normal approximately 120-second delivery delay.
- This proved the artificial RedFox garage and actual property computer were not the same RLS location.

Status:

**FAILED — STOPPED for property/company-garage use.**

### Fleet Computer access problem

The generated marker displayed:

`Tow Yard 1 Fleet Computer`

and showed `Use Computer`, but the user reported that the computer could not be accessed or used correctly.

This generated Fleet Computer must not be considered a working property-management interface.

## 4. Owner-approved tow-yard architecture

When the player buys or controls an RLS property and designates it as a tow yard:

> The property’s existing RLS garage is the tow yard. No second garage is created.

Required linkage:

```text
RedFox yard ID: stable RedFox business record
Custom yard name: user editable
RLS property ID: existing property
RLS garage ID: existing garage such as servicestationGarage
Computer ID: existing computer linked to that garage
Map ID: current level
```

The RedFox yard ID controls business identity, history, custody records, upgrades, and custom naming.

The existing RLS garage ID controls normal owned-vehicle location, My Vehicles grouping, capacity, parking, retrieval, storage, spawning, and computer access.

## 5. Immediate development priority

Everything else is on hold until the property computer works correctly.

The next focused work must provide a dependable management point for:

- tow-yard money and later business finances;
- company vehicles;
- custody storage;
- yard capacities and upgrades;
- transfers between yards;
- later business insurance;
- property designation and yard renaming.

Do not spend the next patch on additional crash scenes, new calls, scene decoration, auction expansion, or unrelated UI cleanup.

## 6. Existing computer behavior required

Use the existing RLS property computer when possible.

Preserve all stock RLS functions and add a RedFox section through a safe hook such as `onComputerAddFunctions`.

Target menu:

```text
My Vehicles
Vehicle and Parts Management
Insurance Management

RedFox Tow Yard Management
Company Fleet
Tow Yard Inventory
```

### Tow Yard Management

Must show at minimum:

- custom yard name;
- property and garage IDs;
- company slots used and available;
- custody slots used and available;
- business balance placeholder or approved money bridge status;
- rename yard;
- transfer overview;
- migration/refresh tools;
- future upgrade placeholders clearly labeled unavailable until built.

### Company Fleet

Must use normal owned RLS inventory vehicles only.

- Same inventory ID.
- `owned=true` remains unchanged.
- No delete-and-recreate during normal assignment.
- RedFox company assignment is metadata/filtering on the normal owned record.
- Transfer to the current designated tow yard is free and immediate.
- Do not invoke stock RLS paid Deliver or its delay for RedFox business transfers.

### Tow Yard Inventory

This remains separate RedFox custody storage for vehicles not owned by the player/company.

Custody vehicles must not appear in My Vehicles until the player uses the lien-claim action or another approved ownership-transfer action.

## 7. Vehicle action requirements

At a designated tow-yard computer, normal owned vehicles should gain a RedFox action such as:

- `Transfer to This Tow Yard`
- `Move to Tow Yard`

When the vehicle is already assigned to the current property garage:

- show Retrieve, Replace, or Store as appropriate;
- do not show a RedFox transfer charge;
- do not start a 120-second delivery timer;
- do not duplicate the vehicle;
- do not change ownership;
- do not change inventory ID.

The stock `$5,000` RLS Deliver action may remain for normal RLS use, but RedFox company transfers must not call it.

## 8. Tow-yard naming

The user must be able to rename each yard instead of being limited to `Tow Yard 1`, `Tow Yard 2`, or `Tow Yard 3`.

Examples:

- RedFox Main Yard
- Belasco Tow & Recovery
- Heavy Recovery Yard
- Port Impound Lot

Renaming changes only the RedFox display name. It must not change the stable RedFox yard ID or existing RLS garage ID.

## 9. Starting capacity and later expansion

Every tow yard starts with two separate capacity pools:

- **5 company fleet slots**
- **10 universal custody slots**

Later paid expansions may increase either pool and add dedicated storage.

This is planned work, not currently claimed working.

## 10. Custody storage rules

Custody vehicles include:

- abandoned vehicles;
- police impounds;
- unpaid customer vehicles;
- lien-eligible vehicles;
- future evidence or agency holds;
- development recovery records.

They are not normal Career-owned inventory vehicles.

### Universal storage safety rule

The ten standard custody slots must accept every recoverable category so a job is not lost solely because specialized storage has not been purchased.

### Dedicated storage routing

When dedicated storage is purchased, matching vehicles automatically use it first.

Routing order:

1. Matching dedicated storage at the selected or closest compatible yard.
2. Matching dedicated storage at another yard on the current map.
3. Universal custody at the selected or closest yard.
4. Universal custody at another yard.
5. Temporary overflow only when every regular option is full.

When dedicated storage fills, matching vehicles use universal slots as overflow.

A boat without boat storage uses universal temporary boat storage. A trailer should prefer a yard with trailer storage, but universal storage remains available so the job is not lost.

## 11. Lien and disposition rules

Lien eligibility begins after three Career days.

The player’s claim cost is capped at:

- original tow/recovery charge;
- exactly three days of storage.

Additional days remain visible in the record but do not increase the player’s lien-claim price.

After eligibility, allowed disposition paths are:

- claim to a personal garage;
- claim to a company garage;
- claim and list through the RLS NPC Marketplace;
- claim and consign through the RLS NPC auction;
- salvage sale;
- scrap;
- transfer to another tow yard;
- leave in custody storage.

There is no player-to-player selling.

## 12. Vehicle-history requirement

A vehicle acquired or sold through a tow lien must receive a permanent Carfax-style history event.

The history should record that the vehicle was previously liened and that the lien was satisfied, rather than showing an active unpaid lien after disposition.

Possible fields:

- tow-lien event;
- reason;
- yard;
- lien eligibility day;
- days held;
- capped lien amount;
- disposition method;
- lien status satisfied.

## 13. Yard sale and relocation rules

A tow yard cannot be sold or closed while it contains:

- company-owned vehicles;
- custody vehicles;
- active holds or listings tied to the yard;
- unresolved transfers.

Nothing is automatically dumped into a personal garage.

Company vehicles must move to another company garage. Custody records must move to another compatible tow yard.

Planned relocation modes:

- paid full-shop relocation;
- player-loaded physical relocation;
- later cross-map loaded-manifest reconstruction.

Do not use the stock per-vehicle `$5,000` delivery method as the business-relocation design.

## 14. Physical five-bay building investigation

The purchased shop land contains five numbered garage bays that are currently not usable.

These are a strong physical match for the default five company fleet slots.

Future focused investigation:

- identify whether each door is animated, static, or part of one combined mesh;
- inspect existing zones and parking spots;
- reuse existing facility/site data where safe;
- add mod-owned site data rather than overwriting stock/RLS files;
- map small fleet vehicles to valid indoor spots;
- route heavy wreckers, buses, semi tractors, lowboys, and large trailers to safe outside spots;
- prevent spawning inside doors, walls, or other vehicles.

Door animation is optional. Functional storage/retrieval zones are the first requirement.

## 15. Stored-record refresh and migration

Settings should include a previewable, backed-up refresh/migration tool for older custody and yard records.

It should be able to:

- update old or missing yard links;
- connect artificial v0.3.1 assignments to the real property garage;
- update storage category and current configured rate;
- preserve or recalculate balances only according to an explicit user choice;
- reorganize universal storage into newly purchased dedicated storage;
- preserve original call, lien timer, search result, condition snapshot, and history;
- verify no duplicates before deleting obsolete records;
- support undo or recovery from backup.

## 16. Emergency-scene mod research

The user found an EMS lighting/sound mod and wants it inspected for emergency-scene setup capabilities.

Pending until the actual mod ZIP or link is supplied.

Inspection targets:

- emergency vehicle placement;
- cones, barricades, flares, debris, and road closures;
- traffic control;
- police/fire/ambulance AI response;
- scene spawn and cleanup APIs;
- safe hooks reusable by JOB-09;
- conflicts with RLS traffic or emergency systems.

Do not claim that the mod contains scene-generation logic until the artifact is inspected.

## 17. Focused runtime gate for the property-computer patch

Use one noncritical owned vehicle.

1. Designate the existing purchased property as a tow yard.
2. Confirm the saved real garage ID is `servicestationGarage` or the actual property garage ID.
3. Confirm no active artificial `redfox_towshop_*` garage is created.
4. Open the property’s normal computer.
5. Confirm stock RLS functions remain.
6. Confirm RedFox Tow Yard Management opens.
7. Rename the yard and verify persistence after reload.
8. Transfer one owned vehicle to the current tow yard through the RedFox action.
9. Confirm `$0` charged and no delivery timer.
10. Confirm inventory ID and ownership are unchanged.
11. Confirm exactly one vehicle appears under the property’s real garage in My Vehicles.
12. Retrieve and store it at the property.
13. Verify configuration, paint, condition, mileage, insurance, name, and thumbnail.
14. Run legacy migration for one v0.3.1 artificial assignment and verify exactly one valid owned record remains.

Stop immediately if the vehicle disappears, duplicates, loses ownership, changes inventory ID, uses the wrong garage, charges `$5,000`, starts a 120-second delay, or the property computer loses normal functions.

## 18. Current development status

- v0.3.0: last user-confirmed working baseline for its implemented features.
- v0.3.1 artificial-garage property bridge: **FAILED — STOPPED**.
- v0.3.2 property-computer artifact: recorded and statically verified in GitHub, but its exact runtime status is unresolved in this chat.
- Next priority: property computer and real-property garage integration only.
- Five usable physical bays: planned after the computer and logical garage link are proven.
- Custody storage upgrades, liens, sales, and history: approved roadmap, not yet claimed working.

## 19. Audit limitations

This audit uses the current conversation, supplied screenshots, and accessible GitHub records. It does not claim access to inaccessible chat history or files that were not supplied.

Any statement marked planned, required, pending, or unresolved is not a runtime-success claim.
