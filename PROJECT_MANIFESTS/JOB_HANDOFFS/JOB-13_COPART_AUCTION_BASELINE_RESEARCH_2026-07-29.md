# JOB-13 — Copart / Bar None Auction Baseline Research

**Date:** 2026-07-29 12:22 PDT  
**Job:** JOB-13 — Copart-style Vehicle Auctions  
**Status:** RESEARCH COMPLETE — IMPLEMENTATION NOT STARTED — NO JOB-13 ZIP EXISTS

## Purpose

Define how a realistic FoxNet vehicle-auction website should work in BeamNG by comparing current Copart, Bar None Auction / HiBid behavior with the uploaded BeamNG/RLS auction source and existing FoxNet website prototype.

## External auction patterns selected

### Copart patterns to retain

- searchable salvage/used vehicle inventory
- auction calendar and location/branch identity
- watchlist and saved searches
- preliminary bids before the live sale
- live auction room with dynamic countdown
- standard increment bids and larger manual bids
- Buy It Now on selected lots
- Pure Sale, Minimum Bid / Reserve, and Seller Approval statuses
- buying-power exposure across active bids
- invoice and pickup/delivery workflow after winning
- visible title, damage, keys, run/drive status, odometer, lot number, location, sale time, and estimated value

### Bar None / HiBid patterns to retain

- auction-specific registration
- catalog grouped by categories and lot numbers
- online-only timed event
- inspection/preview period
- confidential maximum/proxy bid
- automatic incremental bidding only as high as needed to stay ahead
- published bid-increment schedule
- soft close / anti-snipe extension
- buyer premium added to hammer price
- invoice after auction completion
- pickup deadline and storage fees
- as-is/where-is and inspection emphasis

## Recommended FoxNet auction formats

JOB-13 should support two formats through one backend:

### 1. Timed Public Auction

Best first implementation target.

- catalog opens for pre-bidding
- each lot has a scheduled closing time
- confidential max bids
- automatic proxy bidding
- soft-close extension when a late bid arrives
- invoice generated when the lot closes
- works on every map without physical site assets

### 2. Live Lane Auction

Second implementation target.

- lots run in sequence
- pre-bids transfer into the live event
- NPC bidders compete in real time
- circular countdown / going-once presentation
- live bid can defeat an equal pre-bid if the selected sale rule uses Copart-style tie handling
- optional physical West Coast Vault presentation

## Uploaded BeamNG implementation findings

### Existing physical auction engine

The uploaded `1.zip` includes a strong backend foundation:

- `usedCarAuction.lua` — session state, lot flow, payments, inventory settlement, UI data, site triggers, save hooks
- `usedCarAuctionLots.lua` — eligible vehicle generation, auction categories, mileage/value/year filters
- `usedCarAuctionNpcs.lua` — bidder personalities, budgets, interest, FOMO/time pressure, bid timing and increments
- `ui/modModules/usedAuction/*` — functional Angular auction UI

Current categories include Anything Goes, Budget, Salvage Special, Vintage, Truck Night, Touge Nights, Autobahn After Dark, American Allstars, Modern Daily, Sports Weekend, Work Fleet, Rare Finds, and High Rollers.

The current engine uses a 30-second live lot and an anti-snipe window/extension. It validates player balance, prevents bidding on the player's own consignment, requires garage space, charges through `career_modules_payment`, adds won vehicles through `career_modules_inventory`, moves them to a garage, and can pay the player for an NPC-purchased consignment.

### Physical West Coast venue

`west_coast_usa.zip` supplies:

- Auction House / Vault map objects
- entry and counter triggers
- auction lane spawn/block/path/return/despawn spots
- active lights, sound emitters, and win effects
- auction vehicle filters

This venue can become an optional JOB-13 branch. It cannot be the only auction implementation because JOB-13 must operate on every supported map.

### Existing FoxNet Auctions mockup

`RedFox_JOB10_Full_Websites_v0_3_2_REALISTIC_WELCOME.zip` supplies a useful visual reference:

- FoxNet Auctions route
- catalog cards
- search, category, condition, and sort controls
- paginated listings
- membership modal
- lot-detail modal and FoxFax link

It is not functional auction code:

- inventory is random mock data
- state is localStorage/browser state
- registration does not charge real Career money
- no real bid records, max bids, reserves, invoices, ownership, garage storage, or delivery
- the auction page is embedded in a shared root JavaScript file instead of an isolated app/site

### BeamBook reference

`beamBook.zip` is useful only for:

- eligible-vehicle/config generation
- persistent listing generation
- mileage/value variation
- seller-style metadata
- inspection-location concepts

Its startup monkey-patching of `vehicleShopping` must not be copied into JOB-13.

## Required backend refactor

Do not directly wire the FoxNet webpage to the current physical `usedCarAuction.lua`. Extract or adapt its reusable domain behavior into an authoritative auction service.

### Suggested logical modules

Exact paths remain subject to JOB-01/JOB-02 integration contracts.

- auction catalog generator
- auction event scheduler
- lot repository and serializer
- bid/proxy-bid engine
- NPC bidder adapter
- fee calculator
- invoice/settlement service
- ownership/delivery adapter
- consignment service
- FoxNet bridge adapter
- optional West Coast physical-lane adapter

### Authoritative lot state machine

```text
DRAFT
SCHEDULED
PREBID_OPEN
LIVE_OR_CLOSING
PENDING_SELLER
WON_AWAITING_INVOICE
INVOICE_DUE
PAID_PICKUP_READY
DELIVERY_PENDING
DELIVERED
NO_SALE
RELISTED
CANCELLED
```

Every transition must be checked in Lua and persisted.

## Bid engine rules

### Bid record

Each accepted bid should store:

- immutable bid ID
- auction ID
- lot ID
- bidder ID/type
- submitted amount
- confidential maximum amount when applicable
- source: pre-bid, live, buy-now, seller-counter
- game timestamp and sequence number
- previous leader/current leader
- resulting visible bid
- transaction/idempotency key

### Proxy bidding

1. Bidder enters maximum willingness to pay.
2. Maximum remains hidden.
3. Visible bid rises only by the required increment.
4. Existing higher maximum responds automatically.
5. Equal maximum bids should use one documented rule:
   - earliest max bid wins for timed HiBid-style auctions; or
   - live bidder wins an equal pre-bid for Copart-style live auctions.
6. Max bids may be raised, not silently lowered after acceptance.

### Increment schedule

Use a configurable schedule rather than the current fixed `$250/$500/$1,000/$5,000` buttons. A realistic initial schedule can be derived from Bar None but must remain a FoxNet configuration, not a hard dependency on a real company's future fee table.

### Soft close

For timed auctions:

- define a late-bid window
- extend the closing time when a valid bid arrives inside that window
- cap or clearly display repeated extensions
- persist the updated end time before notifying the UI

### Buying power

Do not deduct the full price every time the player bids. Track active exposure:

```text
available buying power = approved limit - highest active obligation per lot - unpaid invoices
```

Losing/outbid lots release their reserved exposure. Winning creates an invoice.

## Settlement and ownership rules

### Invoice formula

```text
hammer price
+ buyer premium
+ auction/processing fee if configured
+ delivery or towing fee if selected
+ storage fee if late
= amount due
```

Real-world tax/legal fees should not be copied literally into the game unless David explicitly wants them. FoxNet fees should be configurable and explained before bid confirmation.

### Safe settlement order

1. Lock the closed lot against further bids.
2. Create exactly one invoice with a unique settlement ID.
3. Validate player money and destination capacity through JOB-02/JOB-08.
4. Charge exactly once.
5. Add exactly one owned inventory vehicle.
6. Assign garage, storage, auction-yard hold, or delivery state.
7. Save.
8. Mark invoice paid and lot settled.
9. Notify UI.

If a later step fails, do not silently lose money or duplicate the vehicle. Record a recoverable pending-settlement state.

### Full garage behavior

The current physical system prevents bidding without a free garage slot. The FoxNet website should be more realistic:

- allow bidding when the player has approved temporary auction-yard storage; or
- block bidding/settlement with a precise capacity explanation; or
- permit delivery to a selected owned garage with space.

The first build should use the simplest verified shared-storage rule and must not fake completion.

## Catalog and lot-detail data

Each vehicle lot should expose:

- stable auction ID and lot number
- sale event and branch/location
- start/end/live time
- year, make, model, configuration, body type
- mileage/odometer
- estimated market or retail value
- current bid and next required bid
- bid count and watch status
- sale status: pure, reserve, approval, buy now
- title/document status
- primary and secondary damage
- keys present
- starts, runs, drives, or unknown status
- inspection notes and disclaimer
- image gallery/thumbnail
- FoxFax history link
- seller type: insurance, fleet, dealer, private consignment, government, rental
- pickup/delivery options
- buyer premium and estimated total before confirmation

`Run and Drive` must be represented as an intake/inspection observation, not a guarantee of future mechanical condition.

## Website pages

- Auctions Home
- Upcoming Auctions / Calendar
- Browse All Lots
- Category Catalog
- Lot Details
- Watchlist
- My Bids
- Live Auction Room
- Won Lots / Invoices
- Pickup / Delivery
- Sell / Consign Vehicle
- Membership / Buying Power
- Rules and Fees

Phone and PC can use responsive layouts but must call the same backend commands.

## Suggested first playable release

### JOB-13 v0.1.0 target

- isolated standalone FoxNet Auctions test app
- all-map timed auction catalog
- persistent generated vehicle lots
- stable lot IDs
- watchlist
- current bid and bid history
- confidential max bid/proxy bidding
- NPC competition
- configurable increments
- soft close
- one real invoice and purchase settlement path
- owned vehicle added once and stored once
- no physical West Coast requirement
- no player consignment yet
- no live-lane mode yet

### Later phases

- v0.2: player consignment and seller reserve/approval
- v0.3: live Copart-style lane and pre-bid transfer
- v0.4: optional West Coast Vault branch, inspection, pickup, and towing integration
- v0.5: advanced membership/buying power, dealer/fleet categories, richer damage/condition simulation

## Known risks

- Current physical engine is heavily coupled to West Coast site data and spawned vehicles.
- Current web prototype is embedded in shared root code and must be separated.
- Existing `finalizePurchasedLot` callback has no explicit transaction/idempotency guard suitable for a web service.
- Current auto-bid exports are compatibility no-ops; proxy bidding must be implemented for JOB-13.
- Current bid validation checks affordability per current lot but does not model active exposure across many online lots.
- Current settlement charges immediately at live-lot close rather than creating a durable invoice.
- Shared bridge and route contracts may still change; do not duplicate them.
- Mod vehicles may contain incomplete metadata or incompatible configs; lot generation needs validation and error quarantine.

## Files affected by this research update

- `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-13_COPART_VEHICLE_AUCTIONS_CLAIM.md`
- `PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-13_COPART_AUCTION_BASELINE_RESEARCH_2026-07-29.md`

No runtime source, ZIP, platform file, bridge file, or another job's work was changed.

## Current status

```text
JOB-13 CLAIMED BY DAVID'S DIRECT ASSIGNMENT
BASELINES INSPECTED
ARCHITECTURE DEFINED
NO JOB-13 BUILD EXISTS
RUNTIME UNTESTED
NEXT: EXACT FILE PLAN + ISOLATED v0.1 AUCTION SERVICE PROTOTYPE
```