# JOB-04 → JOB-13 Wrecking Yard Online Auction and Shared Sell-Inventory Handoff

**Date:** 2026-07-29  
**Owner:** David / Captain  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**JOB-04 issue:** #30  
**JOB-13 issue:** #40  
**Purpose:** Prevent JOB-13 from repeating the Wrecking Yard price, identity, ownership, cache, loading, purchase, duplication and settlement mistakes; define how legally owned Wrecking Yard vehicles can appear on both the Sell page and the online auction page.

---

## 1. Current JOB-04 source of truth

Use this owner-edited archive as the current JOB-04 source:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_v0_3_1_REDFOX_BROWSER_ICON_ONLY- new phone icon.zip
SHA-256: eafbe5618f6e97a14e872d071528f9fd8f450586dc9f7ff28ba55063bda1f4b2
```

The only difference from the prior v0.3.1 archive is:

```text
ui/entrypoints/main/tiles/foxnet-browser.svg
```

All Wrecking Yard HTML, JavaScript, CSS, configuration and mirrored site files were verified byte-for-byte unchanged.

Current runtime evidence from David:

```text
PASS: varied native prices display
PASS: old/high-mileage/project-looking vehicles display
PASS: native listing IDs display
PASS: negotiation availability survives on cards
PASS: Show Different Cars changes the visible selection immediately
PASS: current pool loads quickly once the page is opened
PASS: RedFox Wrecking Yard branding displays
UNPROVEN: final completed phone purchase
UNPROVEN: final completed PC purchase
UNPROVEN: auction export/settlement, because it does not exist yet
```

---

## 2. Important distinction: browse stock versus owned stock

JOB-04 currently has two different concepts that must never be mixed:

### A. Browse/purchase listings

These are native listings originating from BeamBook/private listings and selected dealerships such as:

```text
Joe's Junk
Slop Gear Garage
Smash Rollers
Trusted Auto Sales
Private / BeamBook
Jefferson Motors
Soliad Online Dealership
Import Dealership
```

They can be displayed and purchased online using their native shop/listing ID.

They are **not owned by the Wrecking Yard before purchase** and therefore must not be exported as seller-owned auction inventory.

### B. Owned Wrecking Yard inventory

These are vehicles for which the Wrecking Yard, player or company has a real authoritative Career/RLS inventory record and legal ownership/claim status.

Only this group may be offered to:

```text
Sell Directly
Send to Online Auction
Relist After No Sale
Return to Yard Stock
Strip for Parts
Scrap Whole Vehicle
```

This distinction is mandatory. A dealership/BeamBook card appearing on the Wrecking Yard browse page does not make the yard its owner.

---

## 3. Yes, this should also increase legitimate Sell-page inventory

JOB-04 should expose one shared owned-vehicle disposition provider rather than separate incompatible lists for Sell, Auction, Strip and Scrap.

Recommended JOB-04 surface:

```lua
M.getDispositionCandidates(filter)
M.getDispositionVehicle(inventoryId)
M.prepareDisposition(inventoryId, action, requestId, options)
M.confirmDisposition(inventoryId, action, externalRef, requestId)
M.cancelDisposition(inventoryId, action, externalRef, requestId)
M.settleDisposition(inventoryId, action, settlement, requestId)
M.rollbackDisposition(inventoryId, action, externalRef, requestId)
```

Suggested candidate shape:

```lua
{
  inventoryId = 12345,
  ownershipId = "career_inventory_12345",
  sourceSystem = "redfox_wrecking_yard",
  sourceType = "yard_owned_vehicle",
  sourceRecordId = "yard_vehicle_...",
  model = "covet",
  config = "covet_dx_M",
  displayName = "1986 Ibishu Covet",
  mileage = 204742,
  estimatedValue = 4300,
  condition = {...},
  damagedParts = {...},
  missingParts = {...},
  foxFacts = {...},
  ownershipStatus = "owned_clear",
  claimStatus = "clear",
  eligibleActions = {
    directSale = true,
    auction = true,
    relist = true,
    strip = true,
    scrap = true
  }
}
```

The Sell page can use `eligibleActions.directSale`. JOB-13 can use `eligibleActions.auction`. This adds more owned vehicles to the Sell page without inventing ownership or copying dealership listings.

---

## 4. JOB-13 online-auction requirements from David

The auction is online only.

Do not add:

```text
physical transport to an auction yard
auction-yard intake gameplay
pickup appointments
buyer pickup process
physical inspection trip
reserve-price UI
```

For JOB-04 exports:

```text
transport.required = false
```

David requested no reserve price. JOB-13 must either:

1. support a no-reserve listing profile and make `reserve` optional in a later contract version, or
2. use `reserve = 0` internally while never presenting a reserve to the player.

Do not silently reintroduce a hidden positive reserve.

Required flow:

```text
Wrecking Yard legally owns vehicle
→ JOB-04 marks exact owned inventory record eligible
→ JOB-04 prepares export with unique request ID
→ JOB-13 imports it as an online lot
→ JOB-13 confirms it accepted responsibility for the lot
→ bidding finishes
→ buyer funds/delivery destination are preflighted through JOB-02/Career/RLS
→ winner pays or funds are reserved exactly once
→ source vehicle/record is removed or transferred exactly once
→ seller proceeds are credited exactly once
→ vehicle is delivered/shipped to winner through authoritative Career/RLS flow
→ both jobs persist the final result
```

No step may rely only on a browser card or synthetic listing ID.

---

## 5. Required auction export data

JOB-04 should export at least:

```text
contract version
unique request ID
exact Career/RLS inventory ID
exact Wrecking Yard owned-record ID
ownership ID / source reference
model
configuration
vehicle display name
year, if known
mileage
condition summary
actual damaged parts
actual missing parts
wear values, if available
ownership/claim/title status
estimated value
minimum suggested opening bid
Fox Facts / damage / tow / claim history
thumbnail or preview reference
seller identity
eligible fallback actions
source save revision or generation number
```

Do not claim physical damage from age or mileage alone. JOB-04 previously labeled cars as projects using age/mileage heuristics; that is useful for browsing but is not an authoritative missing/damaged-parts report.

If real part-condition data is unavailable, export:

```text
condition.dataAvailable = false
```

rather than fabricating damage.

Suggested auction request extending `redfox.auction.bridge.v1`:

```json
{
  "contractVersion": "redfox.auction.bridge.v1",
  "requestId": "job04-auction-unique-id",
  "sourceSystem": "redfox_wrecking_yard",
  "sourceType": "external_inventory",
  "sellerType": "company",
  "sourceRef": {
    "inventoryId": 12345,
    "yardId": "redfox_wrecking_yard",
    "garageId": "authoritative_garage_id",
    "sourceRecordId": "yard_vehicle_12345"
  },
  "vehicle": {
    "name": "1986 Ibishu Covet",
    "model": "covet",
    "config": "covet_dx_M",
    "estimatedValue": 4300,
    "mileage": 204742,
    "condition": {
      "dataAvailable": true,
      "damagedParts": [],
      "missingParts": [],
      "wear": {}
    }
  },
  "sale": {
    "reserve": 0,
    "startingBid": 500,
    "buyNow": null,
    "durationSeconds": 86400,
    "sellerMinimum": null
  },
  "transport": {
    "required": false
  },
  "metadata": {
    "foxFacts": [],
    "ownershipStatus": "owned_clear",
    "claimStatus": "clear",
    "fallbackActions": ["return_to_yard", "relist", "strip", "direct_sale"]
  }
}
```

JOB-13 owns any formal schema update. JOB-04 must not independently fork the shared contract.

---

## 6. Required ownership and settlement states

Recommended JOB-04 source-record states:

```text
owned_available
auction_prepare_pending
auction_prepared
auction_export_pending
auction_active
auction_ended_pending_settlement
auction_settlement_processing
auction_sold
auction_no_sale
auction_cancelled
auction_settlement_failed
auction_rollback_pending
returned_to_yard
```

Recommended JOB-13 listing states remain aligned with the existing JOB-09 handoff:

```text
draft
prepared
export_pending
active
ended_reserve_met
ended_reserve_not_met
settlement_requested
settlement_processing
sold
no_sale
cancelled
settlement_failed
```

For no-reserve JOB-04 listings, the reserve-met names may later be generalized by JOB-13. Do not create a competing state machine in JOB-04.

---

## 7. Two-phase export and exactly-once rules

Every mutation must be idempotent using a persistent `requestId`.

Required JOB-04 adapter surface:

```lua
M.getAuctionExportCandidates()
M.prepareAuctionExport(inventoryId, auctionHouseId, options, requestId)
M.confirmAuctionExport(inventoryId, externalListingId, requestId)
M.cancelExternalAuction(inventoryId, externalListingId, requestId)
M.settleExternalAuction(inventoryId, externalListingId, amount, requestId)
M.returnExternalAuctionNoSale(inventoryId, externalListingId, requestId)
M.rollbackExternalAuction(inventoryId, externalListingId, requestId)
```

Rules:

1. `prepareAuctionExport` locks the exact owned record but does not delete it.
2. JOB-13 creates/persists the lot.
3. `confirmAuctionExport` records JOB-13's listing ID and changes the source state to active.
4. Repeating the same request ID returns the stored result.
5. A different request cannot export an already locked/active inventory ID.
6. Settlement must verify exact inventory/source ownership immediately before removal or transfer.
7. Seller proceeds are not credited unless exact source removal/transfer succeeds and is verified.
8. A failed credit or delivery must trigger a persistent rollback/recovery state, not silently lose money or vehicle ownership.
9. No-sale returns the same exact inventory ID and metadata to owned yard inventory.
10. Never create a second source record for relisting; reuse the authoritative record and increment a listing generation/revision.

---

## 8. Lessons from JOB-04 that JOB-13 must not repeat

### 8.1 Do not invent synthetic shop/inventory IDs

JOB-04 v0.2.8 created temporary synthetic IDs. The UI could display/click the cars, but native final purchase could not reliably resolve the record.

JOB-13 must keep:

```text
exact source inventory ID
exact source record ID
exact auction listing ID
unique request ID
```

as separate fields.

### 8.2 Do not clone native records and overwrite all price fields

JOB-04's conversion layer caused the all-$500 failure by selecting the wrong value field and then applying a minimum price to copied records.

JOB-13 must not rewrite source estimated value, opening bid, high bid, seller proceeds and buyer total into one shared `Value` field.

Use explicit fields and validate positive numbers.

### 8.3 Preserve native authoritative data

The working JOB-04 path improved when it stopped rewriting native price, mileage, shop ID and negotiation values.

For auction consignments, preserve the source snapshot and store auction pricing separately.

### 8.4 No broad shop-opening calls

JOB-04 v0.2.2 used:

```lua
openShop(nil, nil, 'buying')
```

and opened every dealership.

JOB-13 must open only its own route/window/lot and must not use a broad native shop call as a discovery mechanism.

### 8.5 No startup inventory load

The welcome page must remain instant.

Do not generate auction lots, enumerate Career inventory, load all dealerships or request source exports when IceFox/phone/PC first opens.

Load auction data only when the Auction page opens, then cache/persist it.

### 8.6 Do not add arbitrary timeout ceilings

JOB-04's 10-second cutoff hid a still-running load and created false failure cards.

Use explicit state and completion/error messages. Do not turn a slow but valid operation into a false hard failure without evidence.

### 8.7 Avoid polling/retry storms

One deliberate request, one response, and user-controlled retry. Persist longer operations in Lua rather than starting repeated browser timers.

### 8.8 Version browser assets

BeamNG WebUI cache repeatedly served old JOB-04 JavaScript after a new ZIP was installed.

Use versioned asset filenames or version query strings, for example:

```text
auction_v001.js
auction_v001.css
auction_config_v001.json
```

Show a small visible version badge during testing so David can prove which build is active. Remove or minimize it for release.

### 8.9 Do not expose development/debug wording in finished UI

JOB-04 displayed source counts, native shop-ID wording, bridge status and testing explanations. David correctly requested their removal.

Developer information belongs in the WEUI/developer panel or logs, not the customer-facing auction page.

### 8.10 Keep Cycle and Refresh conceptually separate

JOB-04 learned:

```text
Show Different Cars = rotate the visible subset from already loaded data; instant
Refresh Yard Stock = reload/rebuild source data; slower
```

JOB-13 should similarly distinguish:

```text
Browse More Lots = change visible page/filter only
Refresh Auction Data = request current persisted auction state
Create New Auction Session = explicit developer/admin action only
```

Do not make two buttons that appear to do the same thing.

### 8.11 Do not fabricate condition

Age, mileage and a damaged-looking configuration name are not proof of missing parts or mechanical damage.

Use actual condition/part data when available. Otherwise say condition details are unavailable.

### 8.12 Keep phone and PC bridges consistent

JOB-04 required careful handling because browser postMessage values can convert numeric IDs to strings. The PC relay was improved by converting numeric IDs back before native calls.

JOB-13 must normalize IDs at every boundary and test both phone and PC separately.

### 8.13 Never manually duplicate money/vehicle ownership logic in the browser

The browser is presentation and request routing only.

JOB-02/Career/RLS remains authoritative for:

```text
funds
ownership
inventory IDs
garage capacity
vehicle creation/removal
save writes
refunds
```

---

## 9. Online direct-buy pattern learned from JOB-04

JOB-04 preserved a useful native online-buy pattern for dealership listings:

```lua
career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)
```

This can inform JOB-13's Buy Now flow, but JOB-13 must not assume an auction lot is automatically a native dealership shop entry.

For auctions, JOB-13 needs its own persistent lot and JOB-02-backed settlement/delivery transaction. Do not create a temporary fake native shop ID merely to reuse the menu.

The useful general pattern is:

```text
phone/PC page
→ postMessage
→ IceFox/Angular host
→ bngApi.engineLua
→ persistent GE Lua module
→ authoritative Career/RLS action
→ guihooks/state response
→ page update
```

---

## 10. No-sale and alternative disposition behavior

A no-sale vehicle must remain available for exactly one of these owner-selected actions:

```text
Return to Wrecking Yard inventory
Relist in the next online auction
Strip for parts
Sell directly through the Wrecking Yard store
Scrap whole vehicle
```

No-sale must not:

```text
create a duplicate inventory record
lose damaged-part history
clear mileage/year/configuration
change the source inventory ID
credit seller proceeds
charge buyer funds
```

Relisting should create a new external auction listing ID and request ID while retaining the same source inventory ID and incrementing a source revision/generation.

---

## 11. Minimum shared Sell-page design

The Sell page should call the shared disposition provider and group vehicles by ownership/source, for example:

```text
My Personal Vehicles
Wrecking Yard-Owned Vehicles
Company Vehicles
Tow/Lien Vehicles With Clear Title
No-Sale Auction Returns
```

Each vehicle should show only actions it is actually eligible for.

Examples:

```text
owned_clear → Direct Sell / Auction / Strip / Scrap
auction_active → View Auction only
auction_no_sale → Return / Relist / Direct Sell / Strip / Scrap
claim_pending → no sale or auction actions
not_owned_browse_listing → Buy only; never Sell/Auction
```

This shared design is how the auction handoff helps put more cars on the Sell page safely.

---

## 12. Required handoff ZIP from JOB-13

JOB-13 should make a handoff ZIP similar to JOB-09's, containing at least:

```text
README / OPEN_ME_FIRST
exact current source filename and SHA-256
auction listing persistence format
JSON schema or contract version
JOB-04 adapter expectations
JOB-09 adapter expectations
personal/company inventory adapter expectations
ownership-removal procedure
damaged/missing-part data format
money settlement sequence
buyer delivery sequence
idempotent request-ID behavior
no-sale return/relist behavior
rollback procedure
PREVIEW / TEST / LIVE modes
phone and PC bridge details
runtime test matrix
known failures and unproven paths
file tree and changed-files report
```

The ZIP must explicitly explain how it prevents:

```text
vehicle duplicated
source vehicle removed twice
winner charged twice
seller paid twice
vehicle removed but seller not paid
winner paid but vehicle not delivered
no-sale vehicle lost
rollback creating a second copy
```

---

## 13. Minimum runtime tests before LIVE

1. Read-only preview of JOB-04 owned disposition candidates.
2. Confirm browse-only dealership/BeamBook listings are excluded.
3. Create/cancel TEST auction listing.
4. Reload Career and confirm lot persists once.
5. Repeat same create request ID and confirm no duplicate lot.
6. No-sale returns same source inventory ID unchanged.
7. Relist uses new external listing ID but same source inventory ID.
8. Direct Sell and Auction cannot lock the same vehicle simultaneously.
9. Failed source removal pays seller nothing.
10. Failed seller credit enters rollback/recovery state.
11. Insufficient buyer funds changes nothing.
12. Full destination garage changes nothing and releases/refunds funds.
13. Successful sale charges once, removes/transfers source once, credits once and delivers once.
14. Reload after successful sale does not repeat settlement.
15. Phone and PC produce the same result.
16. Version badge/assets prove the intended build is active.

---

## 14. Order of implementation

```text
1. JOB-13 persistent PREVIEW/TEST auction database and WEUI
2. Shared schema review with existing redfox.auction.bridge.v1
3. JOB-04 read-only disposition-candidate provider
4. Sell page consumes shared candidates
5. JOB-04 prepare/confirm/cancel/no-sale adapter
6. JOB-13 TEST listing import from JOB-04
7. Idempotency and reload persistence tests
8. JOB-02 LIVE buyer funds/delivery and seller settlement
9. Phone/PC UI registration through JOB-01
10. Only after stable: damaged-part detail, Fox Facts, strip/parts integration
```

Do not build all settlement, parts stripping, damage reconstruction and auction UI in one untested patch.

---

## 15. Final boundary statement

JOB-04 owns Wrecking Yard browsing, owned yard inventory/disposition eligibility, direct-yard sale actions, strip/scrap options and its source-record state.

JOB-13 owns online auction lots, bidding, countdowns, bidders, auction history, online winner checkout and auction settlement orchestration.

JOB-02/Career/RLS owns authoritative money, inventory, ownership, garage, vehicle creation/removal, save and rollback operations.

JOB-01 owns phone/PC/IceFox hosting and routing.

No job may bypass another job's authority by editing its save file directly or inventing replacement IDs.
