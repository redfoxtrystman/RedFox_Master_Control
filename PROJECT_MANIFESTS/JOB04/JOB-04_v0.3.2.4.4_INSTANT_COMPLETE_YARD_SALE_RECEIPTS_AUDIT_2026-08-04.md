# JOB-04 v0.3.2.4.4 — Instant Complete-Vehicle Yard Sale + Receipts Audit

**Date:** 2026-08-04  
**Owner:** David / Captain  
**Job:** JOB-04 — RedFox FoxNet Welcome Hub + Wrecking Yard  
**Runtime status:** **STATIC/HARNESS VERIFIED — NOT YET PROVEN IN BEAMNG RUNTIME**

## Source and output

Source baseline:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-03_v0_3_2_4_3_TOW_SEPARATED_SELL_SCRAP_VISIBLE_FROM_v0_3_2_4_2.zip
SHA-256: f7344a33d0fd50d9643a570ab6590a98d5adf14b7a7a6389da7b88eb5c413b7a
```

Installable candidate:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-04_v0_3_2_4_4_INSTANT_COMPLETE_YARD_SALE_RECEIPTS_FROM_v0_3_2_4_3.zip
SHA-256: e4352bffe0e9742bf754e99d189c3c2cac4bad3de2a3a79d03f0b6660d439fe8
Size: 16,885,202 bytes
Files: 671
```

Companion path-compatibility checks:

```text
JOB-09 Tow v0.4.8.0
SHA-256: fc229ee77d89df220d7762643dcd76f1321f309b0b511e45ca549c155608ada3

JOB-13 Auction v0.1.8.1
SHA-256: 74c7a786253f088b90a2ab78a75d8ec61b3fd9c2d1a471b3f311d5e6771b4bcb
```

## Owner-reported problem addressed

The v0.3.2.4.3 runtime test proved that controls appeared, but also proved that the products and prices were wrong:

- old **Sell Vehicle** called ordinary RLS/Career sale instead of a distinct instant Wrecking Yard offer;
- page displayed a raw/misleading estimate instead of the authoritative RLS sell-value function;
- old percentage whole-scrap formula was not worthwhile;
- selling loaded before buying;
- no persistent invoice-style receipt existed;
- original acquisition source/location was absent.

## v0.3.2.4.4 behavior

### Default page

Wrecking Yard opens on **BUY FROM YARD**. The top market bar displays the RedFox scrap-metal rate, RLS vehicle-market index/phase, and a **Sell / Scrap My Vehicles** button.

### Active sale product

Only one disposition transaction is active:

```text
Sell Complete Vehicle to Yard
```

It is a distinct instant Wrecking Yard transaction. The authoritative reference is:

```lua
career_modules_valueCalculator.getInventoryVehicleSellValue(inventoryId)
```

Offer formula:

```text
RLS sell reference
- 4% instant-service discount
- minimum normal discount: $250
- maximum discount: $1,000
- cheap-vehicle safety cap: no more than 15% of reference
= instant yard payout
```

The quote is recalculated at confirmation time. The exact Career inventory vehicle is removed, absence is verified, and then one custom payout is credited.

### Transaction protection

Persistent states:

```text
prepared
removed_pending_payment
payment_attempting
complete
```

- removal failure preserves vehicle and changes no money;
- payment failure after removal remains retryable;
- uncertain payment attempts are not automatically repeated;
- replaying a completed request does not remove/pay twice;
- a different request cannot resell a removed inventory ID;
- Career money is saved after payout before the transaction is marked complete.

### Receipt popup and history

Every completed instant complete-vehicle yard sale creates one persistent receipt and opens it as an invoice-style popup.

Receipt fields include exact inventory ID; vehicle/config/year/mileage/storage; best-effort original acquisition method/source/location; source transaction/listing and original price when available; RLS reference; discount; quote; actual credited amount; destination account label; parts disposition; daily scrap-rate/RLS market snapshot; and completion status.

Legacy vehicles without saved origin data display `Unknown / legacy record`.

Future shared registry paths are read without editing stock RLS files:

```text
settings/redfox/vehicle_origins_v1.json
settings/redfox/vehicle_origins.json
```

### Daily scrap-rate display

No public RLS scrap-metal API was found. JOB-04 derives a separate rate from the RLS vehicle-market index and snapshots it by RLS game day:

```text
RLS game day: floor(globalEconomy.lastUpdate / 1200)
Base: $170 / short ton
Range: $145–$195 / short ton
Maximum normal day-to-day move: $4 / short ton
Small deterministic day noise: -$2 to +$2
```

The rate does not reroll during the same RLS day. It is informational for complete-vehicle sale; weight-based chassis/junk pricing remains deferred.

### Deliberately disabled

- Auto-Strip Good Parts + Scrap Remainder
- Scrap Current Remainder / Frame
- old Wrecking Yard native-sale action
- old percentage whole-scrap action

This prevents premature parts loss before the comparison recorder and parts-transfer work are ready.

## Cache-safe entry and scope

New entry/assets exist in both mirrors under `index_v03244.html`, `scrap_v03244.js`, and `scrap_v03244.css`. Every older Wrecking Yard entry redirects to:

```text
index_v03244.html?v=03244-instant-yard-sale-receipts
```

Compared with v0.3.2.4.3:

```text
Added: 6
Changed: 22
Removed: 0
```

Protected unchanged items include the purchase adapter, purchase behavior, JOB-09 route, JOB-13 route, route config, Legal Portal, and every unrelated website page/asset.

Purchase adapter SHA remained:

```text
9272f07a655f305ae3ffba6dedf4b1737febde2060d17b6e58f40450e0eba860
```

Path overlap:

```text
JOB-04 vs JOB-09: 0
JOB-04 vs JOB-13: 0
```

The first-load rotating-image/ad standard is documented separately and was not activated in this transaction patch, avoiding a startup vehicle-market scan.

Manifest:

```text
JOB-04_v0.3.2.4.4_CHANGED_FILES_MANIFEST.csv
SHA-256: 9ac96b33c039e905c9cfbf7c22cee217345031a2152b3d296ef53b8db6170e10
```

Records-only originals:

```text
RedFox_JOB-04_v0_3_2_4_4_CHANGED_ORIGINALS_RECORDS_ONLY_2026-08-04.zip
SHA-256: 32a387483409422de1aa4225779e4b41be69a9aeb6643972364a15e5fc2b1932
```

Do not install the records ZIP.

## Verification completed

- 2,159 static scope, mirror, route, reference, protected-file, safe-path and overlap checks passed.
- New page mirrors and redirect mirrors are byte-identical.
- Local HTML/CSS refs resolve.
- Welcome PC/phone JS changes are route-only.
- Unrelated sites are byte-identical.
- ZIP has no duplicates/unsafe paths; CRC passed.
- Fresh extraction has 671 files and byte-matches working tree.
- 4 Lua modules passed `texluac -p`.
- New page JS and three Welcome JS files passed `node --check`.
- Mocked browser-start smoke test ran both DOM-ready handlers without scope/startup exception.
- 17/17 transaction checks passed in working tree and fresh package, including exact removal/payment, receipt/origin, replay protection, removal failure, payment retry and persistent receipts.

## Required owner runtime test

Back up the Career save. Enable only current JOB-04/JOB-09/JOB-13 versions, clear WebUI cache, and restart.

1. Open Wrecking Yard from PC and phone.
2. Confirm badge `v0.3.2.4.4`.
3. Confirm **BUY FROM YARD** opens first.
4. Confirm scrap rate and RLS market snapshot.
5. Confirm Wrecking Yard purchasing still works.
6. Open **SELL / SCRAP MY VEHICLES**.
7. Select one inexpensive expendable vehicle.
8. Record RLS reference and instant offer.
9. Confirm sale.
10. Verify exact inventory ID disappears once.
11. Verify exact displayed payout is credited once.
12. Verify receipt popup has matching reference, discount and actual credit.
13. Verify record in **RECEIPTS**.
14. Restart Career and verify vehicle, money and receipt persist.
15. Recheck Tow and Auction on PC and phone.

Stop and preserve `beamng.log` at the first mismatch, duplicate, missing vehicle/payment, stale page, bridge error or route regression.

## Acceptance status

Do not treat v0.3.2.4.4 as accepted until David completes runtime testing. Issue #30 remains open.