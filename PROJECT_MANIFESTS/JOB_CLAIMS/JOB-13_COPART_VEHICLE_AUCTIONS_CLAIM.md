# JOB-13 — FoxNet Online Vehicle Auctions — Active Claim

**Updated:** 2026-07-31 06:49 PDT  
**Owner:** David / Captain  
**Active development chat:** current regular ChatGPT JOB-13 chat  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Status:** ACTIVE EARLY DEVELOPMENT — v0.1.4 APPROVED-POOL PERFORMANCE PATCH BUILT — RUNTIME UNTESTED

## Ownership

David explicitly assigns and retains this chat as the active owner of:

```text
JOB-13 — FoxNet Online Vehicle Auctions
```

This claim does not transfer ownership of JOB-01, JOB-02, JOB-04, JOB-09, or any shared browser/core system.

## Locked scope

JOB-13 owns an online-only timed vehicle auction system with:

- multiple simultaneous vehicle lots;
- staggered closing times;
- watchlists and multiple active player bids;
- ordinary bidding and confidential maximum/proxy bidding;
- reusable NPC bidder competition;
- player bid cancellation before the lot timer reaches zero;
- no positive reserve prices and no seller-approval flow;
- No Sale and controlled relisting;
- membership tiers, buying-power limits, buyer fees, and shipping discounts;
- Fox Facts, mileage, condition, damaged parts, missing parts, and starts/runs/drives information;
- shipment/In Transit after a completed purchase;
- one previous-auction results archive;
- WEUI settings for TEST tuning before release.

## Online-only boundary

JOB-13 does not use or require:

- a physical auction lane;
- vehicles driving into or out of an auction building;
- an auction-yard intake job;
- a preview/inspection trip;
- physical pickup;
- reserve prices;
- dealership negotiation or Buy Now behavior.

## Approved-pool performance rule

The auction page must never scan dealerships, all installed BeamNG vehicles, RLS `vehicleShopping`, or every vehicle configuration when the page opens.

Required architecture:

1. Load a small JOB-13-owned approved vehicle pool once in Lua.
2. Build/cache the auction lots before the browser requests them.
3. Reuse persisted approved lots on revisit.
4. Send only a small visible catalog summary to the browser.
5. Load full condition and bid history only when one lot is opened.
6. Do not render or transmit 100–200 full listings at once.
7. Do not use retry storms or forced shop refreshes.

Current approved pool contract:

```text
Pool ID: redfox.job13.approved.v1
Packaged entries: 21
Visible initial lots: 12
Dealership scans on page open: 0
Vehicle/config scans on page open: 0
```

## Shared Sell-page boundary

Only legally owned vehicles may be disposition candidates:

```text
Direct Sell
Send to Auction
Relist
Strip for Parts
Scrap
Return to Yard
```

Eligible sources include personal Career vehicles, company-owned vehicles, JOB-04 Wrecking Yard-owned vehicles, clear-title JOB-09 lien vehicles, and exact no-sale returns. Browse listings are not owned merely because they are visible.

## Cross-job boundaries

- JOB-01 owns phone/PC/IceFox routing and the shared Browser Core.
- JOB-02/Career/RLS owns money, ownership, inventory, storage, and delivery authority.
- JOB-04 owns Wrecking Yard inventory and source-record removal/return.
- JOB-09 owns tow-yard custody, lien/title acquisition, and its source records.
- JOB-13 must not independently package or replace their shared/core files.

JOB-13 will not package:

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfoxCareerWeb.lua
ui/modModules/redfoxCareerWeb/**
```

## Current test artifact

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_4_APPROVED_POOL_PATCH.zip
SHA-256: 56c4143cbb3233dd187bfe22aafeca48b5024e917cd3e1d4a25626033402c84f
```

v0.1.4 is an early TEST build, not release-ready. It must be tested by David before the bidding, purchasing, or shipping behavior is accepted.

## Current known external dependency

The standalone JOB-13 UI App uses the corrected v0.1.4 page. A shared phone auction icon can still open an older copied FoxNet auction site until JOB-01/Browser Core points that route to the JOB-13 page. JOB-13 will not silently overwrite the shared browser to force that change.

## Next runtime gate

1. Remove or disable all older JOB-13 ZIPs.
2. Install only v0.1.4.
3. Add the new `FoxNet Online Auctions — JOB-13` v0.1.4 UI App.
4. Time opening the standalone app.
5. Expected target: usable approved catalog within 10 seconds.
6. Only after the catalog passes should membership, bidding, cancellation, invoice, and shipping TEST behavior be exercised.
