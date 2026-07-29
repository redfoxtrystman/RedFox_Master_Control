# JOB-09 → JOB-13 Copart-Style Auction Yard Handoff

**Date:** 2026-07-29  
**Owner:** David / Captain  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**JOB-09 issue:** #4  
**JOB-13 issue:** #40

## Current JOB-09 source

Active artifact:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_3_PerYardStorageShopTransferLienClaimsSalesAuctionsScrap.zip
SHA-256: 19ca72c6ccaa36610425d26a2e0e9d775dfe338f8d728b6bc2fbe226038ab6f1
```

GitHub commits:

- build audit `2fc567fe59bba03fcaf0f432ea3786db99e82ea6`
- source summary `cd29446bf992a04b032212d940580fdb78853dd6`
- exact artifact record `536907d2a1a1725e021f76f0774a46a1d720644e`

## Ownership boundaries

JOB-13 owns auction listings, bids, reserves, countdowns, auction-yard intake, purchase/delivery UI, seller settlement UI and auction history.

JOB-09 owns tow-yard custody, legal hold/lien eligibility, lien/title acquisition, per-yard shop inventory and safe removal/payment for JOB-09 vehicles at settlement.

JOB-02/Career/RLS remains authoritative for money, Career inventory IDs, ownership, garage capacity, vehicle creation/removal and save writes.

JOB-01 remains authoritative for the phone/PC/IceFox browser host and routing.

**JOB-13 must not directly edit** `settings/redfox/tow_recovery_dispatch_yard.json`.

## Existing JOB-09 v0.4.3 read/action surface

Read state:

```lua
local state = extensions.redfoxTowRecoveryDispatch.getWebPortalState()
```

Contract:

```text
redfox.tow.web.v1
```

Useful fields:

```text
state.shopInventory
state.auctions
state.inventory
state.yards
state.businessLedger
state.businessMoney
```

Existing actions:

```text
claim_yard_vehicle     {recordId}
shop_sell_direct       {shopId}
shop_start_auction     {shopId}
shop_scrap             {shopId}
shop_native_sale       {shopId}
auction_accept         {listingId}
auction_cancel         {listingId}
buy_yard_upgrade       {yardId, upgradeType}
link_yard_garage       {yardId, garageId}
transfer_fleet_to_yard {unitId, yardId}
```

Call form:

```lua
extensions.redfoxTowRecoveryDispatch.webPortalActionJson(action, jsonPayload)
```

The current JOB-09 auction is only a temporary internal simulation. Defaults are 300 seconds, 60% reserve, 45%–115% generated high bid and 2–14 generated bidders. JOB-13 should replace/bypass this when its external bridge is available.

## Supported vehicle sources

### Tow-yard lien vehicle

1. Complete legal hold.
2. JOB-09 confirms disposition eligibility.
3. Company pays tow lien, storage capped to three days and title fee.
4. JOB-09 creates and verifies one normal owned Career vehicle.
5. Same inventory ID moves to the yard's linked real RLS garage.
6. JOB-09 creates `shopInventory` record with `available_for_sale`.
7. JOB-13 accepts it as auction consignment.

Do not auction an unclaimed custody record unless David later approves a separate statutory-lien-auction workflow.

### Personal vehicle

Store the exact Career inventory ID and source garage. At settlement verify the vehicle still exists and is owned, remove it, verify removal, then credit proceeds. Failed removal means no payment.

### Company/shop vehicle

Preserve company assignment, prior garage, yard link and exact inventory ID. Cancel/no-sale must return it unchanged.

### Player purchase

Use two-phase delivery: preflight funds/garage, reserve or deduct funds, create one owned vehicle, verify inventory and garage, commit; on failure remove the created vehicle and refund.

## Proposed interface

Contract:

```text
redfox.auction.bridge.v1
```

JOB-13 exports:

```lua
M.isAvailable()
M.createListing(request)
M.cancelListing(listingId, requestId)
M.getListing(listingId)
M.getListings(filter)
M.openWindow(section, listingId)
M.requestPlayerPurchase(listingId, destinationGarageId)
M.requestSellerSettlement(listingId)
```

JOB-09 next integration patch should export:

```lua
M.getAuctionExportCandidates()
M.prepareAuctionExport(shopId, auctionHouseId, options)
M.confirmAuctionExport(shopId, externalListingId, requestId)
M.cancelExternalAuction(shopId, externalListingId, requestId)
M.settleExternalAuction(shopId, externalListingId, amount, requestId)
M.returnExternalAuctionNoSale(shopId, externalListingId, requestId)
```

Until those exist, JOB-13 may read `getWebPortalState().shopInventory` for preview only. It must not mutate or sell a JOB-09 vehicle directly.

## Required listing states

```text
draft
prepared
export_pending
transport_pending
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

Every action must be idempotent using a persistent `requestId`. Repeating a completed request returns the stored result instead of executing twice.

## WEUI testing

Open JOB-09's existing legacy WEUI:

```lua
extensions.redfoxTowRecoveryDispatch.openLegacyWindow()
```

JOB-13 should use the same `ui_imgui` + `im.BoolPtr` + `onUpdate()` pattern and provide:

```text
PREVIEW   no money, ownership or inventory changes
TEST      persistent fake listings; no real Career writes
LIVE      real Career/RLS transactions with verification and rollback
```

Recommended WEUI sections:

```text
Auction Dashboard
Create/Test Listing
Tow-Yard Intake
Personal Vehicles
Active Auctions
Settlement Queue
Purchase/Delivery Tests
Transaction Log
Developer Controls
```

Every test must show request ID, listing ID, inventory ID, source/destination garage, money before/after, expected/actual result, rollback result and PASS/FAIL.

## Phone/PC bridge

Use JOB-09's proven pattern:

```text
iframe page → postMessage → BeamNG Angular app → bngApi.engineLua → GE Lua action → guihooks state update → iframe render
```

## Tow-yard transport to auction yard

1. JOB-13 accepts listing and assigns auction-yard intake.
2. JOB-13 sends JOB-09 listing ID, exact inventory ID, origin and destination.
3. JOB-09 creates an `Auction Yard Transport` dispatch job.
4. Player transports the exact vehicle.
5. JOB-09 verifies arrival and reports `vehicle_received`.
6. JOB-13 changes `transport_pending` to `active`.

Cross-map transport must use persistent handoff state and destination-map respawn/verification. Do not attempt to preserve node-grabber cables across map load.

## Minimum runtime tests

1. Preview JOB-09 shop inventory without mutation.
2. Create/cancel TEST listing.
3. Reload Career and confirm one persistent listing.
4. Reserve-not-met returns vehicle unchanged.
5. Seller settlement removes exact inventory ID before payment.
6. Failed removal pays nothing.
7. Insufficient-funds purchase changes nothing.
8. Full-garage purchase changes nothing and refunds reserved money.
9. Successful purchase creates one vehicle and deducts once.
10. Repeated request ID does not duplicate money or vehicles.

## Build order

1. WEUI PREVIEW/TEST harness and persistent listing database.
2. Read-only JOB-09 shop preview.
3. Personal-vehicle preview.
4. Auction engine and reload persistence.
5. Formal JOB-09 export/settlement adapter.
6. Real auction-yard transport jobs.
7. LIVE purchase/settlement through JOB-02/RLS.
8. Phone/PC registration through JOB-01.
