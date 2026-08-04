# JOB-04 Wrecking Yard Completion Ledger

**Date:** 2026-08-04  
**Owner:** David / Captain  
**Primary build ledger:** issue #30  
**Emergency continuity issue:** #55

## Current runtime baseline

Current tested candidate:

```text
JOB-04 v0.3.2.4.3
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-03_v0_3_2_4_3_TOW_SEPARATED_SELL_SCRAP_VISIBLE_FROM_v0_3_2_4_2.zip
SHA-256: f7344a33d0fd50d9643a570ab6590a98d5adf14b7a7a6389da7b88eb5c413b7a
```

Runtime result:

- New Wrecking Yard sale/scrap controls are visible.
- JOB-09 Tow route is separated; old bundled Tow pages no longer own the active Tow site.
- Buy flow remains available.
- Current sale/scrap pricing and product definitions are not accepted.
- `Sell Vehicle` currently calls normal RLS/Career sale and does not represent a Wrecking Yard instant offer.
- Current whole-scrap payout uses an obsolete low placeholder formula.
- Current displayed estimate can differ from actual RLS sale value because the page does not consistently use the final RLS vehicle-sell market multiplier.
- Buying must be the default Wrecking Yard page; selling/scrapping must be secondary.

Classification:

```text
PARTIAL RUNTIME PASS — ROUTES/UI VISIBLE; PRICING, PRODUCT DEFINITIONS, RECEIPTS, AND PART RETURN NOT ACCEPTED
```

## Correct website layout

Default opening page:

```text
BUY FROM YARD
```

Top-right status/actions:

```text
Today's Scrap Rate: $___ per short ton
RLS Vehicle Market: [condition/index]
[ Sell / Scrap My Vehicles ]
```

The Sell/Scrap page shows owned Career vehicles grouped by garage/location.

## Correct Wrecking Yard products

### 1. Sell Complete Vehicle to Yard

- Instant transaction.
- Yard receives the complete vehicle and all installed parts.
- Reference value must be the actual RLS vehicle sell value including current RLS market multiplier.
- Offer is only slightly below waiting for an ordinary marketplace buyer.
- Proposed initial discount rule:

```text
4% of actual RLS reference value
minimum discount $250
maximum discount $1,000
```

- Exact inventory vehicle removed once.
- Money credited once.
- Full receipt created.

### 2. Auto-Strip Good Parts + Scrap Remainder

- Good usable parts return to the existing RLS parts inventory.
- Any part whose name contains `junk` remains with the chassis/remainder and counts toward scrap value.
- Unresolved or unsupported mod-vehicle parts remain with the remainder unless positively confirmed as returned.
- One combined dismantling labor charge; no separate fluids/disposal micro-fees.
- Vehicle is not removed until returned parts are stored and verified.
- Receipt lists every returned, junk, and unresolved part.

Warning shown before confirmation and on receipt:

> Some mod vehicles do not report every removable part or slot consistently. Unresolved parts will remain with the vehicle remainder and count toward scrap unless confirmed as returned.

### 3. Scrap Current Remainder / Frame

For a vehicle already manually stripped in the garage:

- Pay for chassis/frame, remaining body, remaining installed junk parts, and other installed leftovers.
- No dismantling labor charge.
- Optional later checkbox:

```text
[ ] Include all stored parts containing "junk"
```

## RLS-linked daily scrap rate

- RLS exposes a persistent vehicle-market index, vehicle sell multiplier, part multiplier, phases, history, and news.
- No dedicated public scrap-metal API was confirmed.
- JOB-04 therefore derives a RedFox scrap-metal rate from the RLS market index.
- Snapshot once per in-game Career day.
- Keep fixed for that whole game day.
- Persist through reload.
- Normal movement should be only a few dollars per ton.
- Store day ID, source RLS index, rate, prior rate, and daily change.
- Same authoritative rate appears on Welcome, PC, phone, Wrecking pages, quotes, ads, and receipts.

## Receipt popup and history

Every completed transaction opens a realistic RedFox Wrecking Yard invoice/receipt and stores it in persistent Receipt History.

Required fields:

```text
RedFox yard name and physical location, when configured
Receipt/transaction number
Career inventory ID
Vehicle model/configuration/year
Mileage
Current storage/garage
Original acquisition method
Original acquisition source/site
Original acquisition map/location
Original acquisition transaction/listing ID, when available
Original purchase/prize value, when available
Actual RLS reference value
Daily scrap rate and source market index
Instant-sale discount OR dismantling labor charge
Returned good parts: name, slot, condition when exposed, value
Junk parts retained: name, slot, value
Unresolved parts included with remainder
Chassis/remainder value
Final cash payment
Destination account
Completed/pending/failed status
In-game date/time
```

Original acquisition methods include:

```text
Dealership/shop purchase
FoxNet Auction win
Classic/Collector purchase
Wrecking Yard purchase
Tow/lien claim
Found in vehicle crate
Spawned then claimed
Prize/competition win
Gift
Import
Unknown / legacy record
```

Older vehicles may legitimately show `Unknown / legacy record`. Never invent an origin.

## Acquisition-origin data contract

Future JOB-04/JOB-07/JOB-09/JOB-13 and crate/prize adapters should append a lightweight origin record keyed to exact Career inventory ID. Do not replace stock Career/RLS files. Preserve source job, source record/transaction ID, method, original location, price/value, and in-game timestamp.

Tracking: issue #57.

## Temporary auto-strip comparison recorder

Before auto-strip is accepted, build a temporary read-only test app/mod so David does not need to hand-record hundreds of parts while tired.

Required workflow:

1. Spawn/claim or otherwise obtain two same-model/same-configuration Career vehicles.
2. Select control inventory ID and test inventory ID.
3. Capture both vehicles before work.
4. David manually strips the control vehicle.
5. JOB-04 auto-strips the test vehicle.
6. Capture both after states.
7. Produce on-screen comparison plus persistent JSON and CSV.

Required comparison:

- exact inventory IDs;
- model/config/mileage;
- before installed-parts list;
- manual-strip returned parts;
- auto-strip returned parts;
- name/slot/value/condition where exposed;
- `junk` classification;
- missing, extra, duplicate, and unresolved parts;
- frame/remainder quote;
- labor charge;
- final payment;
- pass/fail summary.

The test tool must not change money, vehicles, parts, garages, or transactions. Tracking: issue #54.

## First-load image and rotating tile work

- Current Wrecking Welcome image pool is populated only after entering Wrecking Yard once, causing generic images on first load.
- Auction exhibits a similar first-render symptom and must be traced by JOB-13.
- Implement shared visual manifest and static first-load image pool.
- Wrecking, Auction, Classic, and Tow Welcome tiles rotate 3-8 module-owned 640x360 images.
- Do not rotate unrelated pictures inside a specific vehicle listing.
- Shared standard: `PROJECT_MANIFESTS/INTERFACES/FOXNET_VISUAL_ASSET_AND_ROTATING_TILE_STANDARD_v1_2026-08-04.md`.
- Tracking: #53 and #56.

## Physical scrapyards and optional prefab

After pricing, receipts, and auto-strip are stable:

- Allow multiple persistent scrapyards per map.
- Player chooses current world position and names yard.
- Settings per yard:

```text
[ ] Spawn full 3D scrapyard prefab
[ ] Marker only
[ Adjust placement ]
[ Move yard here ]
[ Remove yard ]
```

- Spawn optional movable prefab; allow Shift+C inspection and F11 adjustment.
- Store final prefab transform per map/yard.
- Drive vehicles/chassis into marker to open sell options.
- Exact world vehicle must resolve to exact Career inventory ID.
- Tow yards and scrapyards must be at least 1 mile / 1,609 meters apart using initial straight-line world distance.
- Shared fields only: yard ID, name, map, coordinates. Tow and Wrecking business logic remain separate.

## Duplicate taxi investigation

Two old taxi records were observed with different inventory IDs, mileages, and storage locations. Do not auto-delete or merge. Add origin/transaction logs first, then trace Auction, purchase, crate, spawn/claim, prize, and delivery history. Tracking: #58.

## Remaining implementation order

1. Restore Buy From Yard as default.
2. Use actual RLS sell reference value and correct instant complete-vehicle offer.
3. Add full receipt popup/history including acquisition origin.
4. Add authoritative daily RLS-linked scrap rate everywhere.
5. Fix first-load image pool and rotating Wrecking tile.
6. Build temporary auto-strip comparison recorder.
7. Implement and test Auto-Strip Good Parts + Scrap Remainder.
8. Implement already-stripped frame/remainder plus optional stored junk parts.
9. Add physical scrapyard placement and optional prefab.
10. Final PC/phone/cross-job regression audit.

## Near-complete definition

JOB-04 is nearly complete when:

- purchases remain reliable;
- all three Wrecking sale products work and pay exactly once;
- good parts return correctly;
- junk and unresolved parts retain value;
- receipts persist and explain every value/part;
- daily scrap rate is RLS-linked and shown everywhere;
- first-load imagery and rotating tiles work on PC and phone;
- physical yard marker/prefab placement works without conflicting with Tow yards;
- no duplicate vehicles, parts, payments, routes, or active ZIP paths occur.
