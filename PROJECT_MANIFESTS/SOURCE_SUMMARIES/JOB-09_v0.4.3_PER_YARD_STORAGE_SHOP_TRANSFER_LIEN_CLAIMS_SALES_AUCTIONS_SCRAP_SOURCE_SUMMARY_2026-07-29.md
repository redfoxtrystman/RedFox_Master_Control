# JOB-09 v0.4.3 Source Summary

**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Date:** 2026-07-29  
**Version:** 0.4.3  
**Runtime status:** Unproven in BeamNG/RLS; static and mocked integration verified.

## Main runtime

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
```

Version/schema updates:

```text
module version: 0.4.3
settings schema: 10
saved-state schema: 7
```

## Per-yard business state

Every RedFox yard now carries its own:

```text
custodyCapacity
companyCapacity
salesCapacity
upgradeLevels.custody
upgradeLevels.company
upgradeLevels.sales
linkedGarageId
```

Old custody records without a valid yard assignment migrate to the first saved RedFox yard on their map. Capacity checks now use the assigned destination yard rather than one shared global `profile.yard` count.

## Money and ledger

The new business layer uses the installed Career/RLS money attribute API when available and records persistent ledger entries for:

- storage upgrades;
- lien/title acquisitions;
- refunds;
- direct sales;
- auction sales;
- scrap sales.

Insufficient-funds paths stop before acquisition. Failed claims remove any temporary inventory record, retain the original custody record, and do not retain a charge.

## Existing-purchased-garage bridge

A RedFox yard can link only to a facility reported as purchased by the installed garage manager. The implementation does not create a fake garage, alter purchased-property records, or inject stock facilities.

Linking rules:

- current map only;
- one RedFox yard per purchased garage;
- link cannot be removed while company or claimed-sale vehicles still occupy it;
- both RedFox capacity and native RLS garage capacity are checked.

## Shop vehicle transfer

The safe transfer path calls the native inventory garage-move function, then verifies:

- the original Career inventory ID still exists;
- ownership is not false;
- the destination garage matches;
- no duplicate vehicle was created.

The previous garage is stored for return/undo. Cross-map movement remains blocked.

The historical unsafe removal-based function remains in source only for recovery history and has zero live call sites.

## Lien claim flow

Eligible custody records expose:

```text
tow lien
elapsed storage days
charged storage days = min(elapsed, 3)
title fee
total acquisition cost
```

Successful acquisition requires:

1. disposition eligibility;
2. matching current map;
3. linked real purchased garage;
4. available sales-staging slot;
5. available native garage space;
6. sufficient Career money;
7. one created and verified owned inventory record;
8. verified move of that same inventory ID to the linked garage.

Only after those steps does the custody record become a Shop / Resale Inventory record.

## Claimed-shop dispositions

### Direct market sale

Removes and verifies the exact inventory ID, then queues payment at the stored market value.

### Copart-style auction

Persistent listing state includes reserve, high bid, bidder count, start time, and end time. Cancel preserves the vehicle. Accept removes and verifies the exact inventory ID before payment.

### Scrap

Removes and verifies the exact inventory ID before paying the configured scrap percentage.

### Native Career sale/offers launcher

The code dynamically checks safe open/menu functions exposed by installed Career selling, marketplace, shopping, or inventory modules. It does not call an undocumented destructive sale function. If a vehicle disappears through native Career selling, JOB-09 reconciles its shop record without issuing an additional RedFox payment.

## UI surfaces

Legacy Tow Yard Management now includes:

- independent capacities and usage per yard;
- upgrade prices and purchase buttons;
- purchased-garage candidate selection;
- link/unlink controls;
- business money and ledger status.

Legacy Tow Yard Inventory now includes:

- eligible claim breakdown;
- claim-and-transfer action;
- Shop / Resale Inventory;
- direct sale;
- auction list/accept/cancel;
- scrap;
- native sale/offers launcher.

Company Fleet now includes:

- transfer current owned truck to assigned linked shop;
- return to previous garage;
- undo last verified move.

The RedFox Tow Web Portal mirrors these operations through 45 portal actions with matching Lua handlers.

## Preserved v0.4.2.1 behavior

- all-mission `vehicleRules.dispatchClassName(...)` hotfix;
- protected call acceptance and failure records;
- roadway police blockers;
- Random Events 1.9 live scene bridge;
- same-map active-job recovery;
- Rolling Chassis exclusion from ordinary rollover selection;
- teachable equipment roles and Scene Builder.

## Runtime boundaries

Still not implemented:

- cross-map owned-vehicle transfer;
- Node Grabber/cable restoration;
- exact damaged-part/deformation restoration;
- NPC drivers performing jobs;
- a documented native BeamNG auction API.

The internal Copart-style auction is therefore the guaranteed auction workflow. The native sale button is a dynamic launcher for whatever safe menu interface the installed game exposes.