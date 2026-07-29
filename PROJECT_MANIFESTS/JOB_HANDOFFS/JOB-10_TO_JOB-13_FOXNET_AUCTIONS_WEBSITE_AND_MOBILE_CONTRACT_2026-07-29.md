# JOB-10 to JOB-13 — FoxNet Auctions Website and Mobile Contract

**Date:** 2026-07-29  
**Owner:** David / Captain  
**From:** JOB-10 — Visual Design / Real Website Polish  
**To:** JOB-13 — Copart-Style Vehicle Auctions  
**Status:** COORDINATION NOTE — NOT A HANDOFF OF JOB-10 OWNERSHIP

## Current architecture correction

The active RedFox/FoxNet runtime target is phone-only.

```text
PHONE PLATFORM: ACTIVE
PC PLATFORM: HIDDEN / DEFERRED
PC CODE: PRESERVE FOR POSSIBLE FUTURE RETURN
```

JOB-13's original claim contains an older phone/PC parity sentence. That requirement is superseded by:

```text
PROJECT_MANIFESTS/OWNER_PHONE_ONLY_ARCHITECTURE_DIRECTIVE_2026-07-23.md
```

JOB-13 must build and test the auction page for the approved in-game phone host. Do not delete useful PC code, but do not expose, integrate, or treat PC parity as a release requirement.

## Ownership split

### JOB-13 owns

- authoritative auction catalog and persistent lot state;
- real timed and later live bidding;
- NPC bidding;
- proxy/max bidding;
- watchlists and saved lots state;
- membership/registration behavior;
- buyer fees, invoices and settlement;
- real Career/RLS payments through approved shared operations;
- real ownership, garage/storage and delivery integration through owning jobs;
- consignment behavior when enabled;
- all auction-specific Lua/business logic;
- an isolated removable FoxNet Auctions site/app package;
- exact web-facing data and action contract supplied to JOB-10.

### JOB-10 owns

- the visual design and mobile layout of the FoxNet Auctions website;
- Copart-inspired but original FoxNet branding;
- cards, search, filters, category presentation, lot detail presentation, forms, dialogs, navigation, loading/empty/error states and responsive polish;
- the FoxNet Auctions welcome-page card and route link;
- real BeamNG image placement and visual fallback rules;
- final visual QA after JOB-13 supplies stable data/actions.

JOB-13 must not overwrite the IceFox welcome page, shared design system, other websites, or JOB-10 root visuals. JOB-10 must not implement auction money, bids, ownership, invoices or settlement logic.

## Current visual baseline

Reference only:

```text
RedFox_JOB10_Full_Websites_v0_3_2_REALISTIC_WELCOME.zip
SHA-256: fab5913a9d1b580b0ff32d6ea6d53d8f8983fe2b9ddf9110aa79742c7679b5e5
```

The existing FoxNet Auctions page in that package is visual/mock data only. It must not be copied as an authoritative backend. It can be used for layout and style reference.

The final auction site should look like a believable modern salvage/used vehicle auction website, inspired by Copart's information density and workflow but using original FoxNet branding and assets.

## Required mobile website pages

First complete mobile page family:

```text
Auctions Home
Browse All Lots
Categories
Upcoming Auctions / Calendar
Lot Details
Watchlist
My Bids
Won Lots / Invoices
Pickup / Delivery
Membership / Buying Power
Rules and Fees
```

Later phases:

```text
Live Auction Room
Sell / Consign Vehicle
Seller Approval / Counter Offers
Optional West Coast physical-auction branch
```

Every visible button must either:

1. perform a real action through JOB-13's backend contract;
2. navigate to a working page/dialog; or
3. be clearly disabled and labeled unavailable in the current build.

Do not leave important business buttons as silent placeholders.

## Vehicle inventory rules approved by David

- Around 100 active vehicles at one time, not exactly 100.
- A normal target range is roughly 90–110 active listings.
- Inventory and category mix may rotate with the in-game day.
- Do not regenerate the entire pool whenever the page is opened.
- Active bids, invoices, watched lots and unresolved auctions must persist across page closes, save/load and day changes.
- Only eligible replacement slots should rotate when an in-game day advances.
- Category buttons must actually filter the current catalog and display current counts.
- Unsupported/empty categories should honestly show zero or an empty state.
- Inventory must work on every supported map; West Coast may be an optional branch, not a requirement.

## Real vehicle and image rules

David requires real BeamNG vehicles only.

- Use actual stock BeamNG or installed-mod vehicle configurations.
- Use the corresponding real game/config thumbnail or validated BeamNG screenshot.
- Never use cartoon vehicle SVGs, unrelated stock car photos or fake generic vehicle silhouettes as final lot art.
- Mod vehicles/configs must be validated before listing. Broken or incomplete configurations go to an error/quarantine report rather than the auction.
- Every lot must preserve the exact vehicle model/configuration needed to create the won vehicle.
- Image and vehicle identity must never disagree.

JOB-13 should expose image fields that allow JOB-10 to render:

```text
thumbnail
hero image
optional image gallery
vehicle model/config identity
fallback reason when no image is available
```

## Stable lot IDs and purchase warning

Do not repeat the display-only synthetic-ID problem seen during Wrecking Yard experiments.

Every auction lot needs a stable persisted lot ID tied to a validated vehicle configuration and authoritative auction record. A display card is not a purchasable vehicle by itself.

A won lot is only complete after:

```text
one real invoice
one real charge
one real ownership record
one real inventory vehicle
one valid storage/delivery result
one saved settlement state
```

Repeated UI callbacks must not duplicate charges or vehicles.

## Required card data

Each catalog card should expose at minimum:

```text
stable lot number
real vehicle thumbnail
year / make / model / configuration
current bid
next required bid
bid count
sale type/status
primary damage
title/document status
keys present
run/drive/intake status
odometer
location/branch
closing or live time
watch status
Buy It Now status when applicable
```

## Required lot-detail data

```text
image gallery
vehicle identity and configuration
current bid / next bid
confidential max-bid form
bid history summary
countdown and soft-close notice
Pure Sale / Reserve / Seller Approval status
estimated value
primary and secondary damage
keys
starts / runs / drives / unknown intake observation
odometer
seller type
inspection notes
as-is/where-is notice
buyer premium and estimated total
pickup/delivery options
FoxFax link when a legal history report is available
```

FoxNet Auctions is a legal auction site. FoxFax may be offered when history data is available. Stolen/UndergroundNet vehicle rules do not belong in JOB-13.

## Registration and membership

David previously requested a real registration flow:

```text
open Register
review membership/registration terms and cost
confirm payment
charge real Career money once
activate bidding access
show success or recoverable failure
```

Fees and tiers must be configurable and shown before confirmation. Do not use localStorage as the authority and do not fake payment success.

## Auction behavior required from JOB-13

First playable target should prioritize timed online auctions:

- persistent events and lots;
- pre-bidding;
- confidential maximum/proxy bids;
- NPC competition;
- configurable increments;
- soft close / anti-snipe extension;
- watchlist;
- My Bids state;
- one real invoice and settlement path;
- one real owned vehicle added exactly once;
- all-map operation;
- no physical auction-yard requirement.

Later add live-lane bidding, pre-bid transfer, player consignment and physical venue integration.

## Data/action contract JOB-13 must provide to JOB-10

Before final visual integration, provide one versioned contract containing:

### Read/state operations

```text
getCapabilities
getAuctionHome
getAuctionEvents
getCatalog
getCategories
getLotDetails
getWatchlist
getMyBids
getWonLots
getInvoices
getMembership
getBuyingPower
getPickupDeliveryOptions
```

### Mutation/action operations

```text
registerMembership
watchLot
unwatchLot
placeBid
setMaxBid
buyNow
payInvoice
selectPickupOrDelivery
acknowledgeRules
```

Later:

```text
consignVehicle
setReserve
acceptSellerApproval
rejectSellerApproval
enterLiveRoom
placeLiveBid
```

Exact names may differ, but JOB-13 must publish the final names, payloads, result schemas, idempotency keys and error codes.

### Required UI states

```text
loading
empty
not registered
insufficient buying power
outbid
leading
reserve not met
seller approval pending
won
invoice due
payment failed
full garage / no destination capacity
delivery pending
delivered
network/bridge unavailable
invalid or quarantined vehicle configuration
```

## Route and packaging contract

Preferred canonical destination:

```text
https://auctions.foxnet.redfox
```

JOB-13 should deliver an isolated route/site/app that the phone host can register without copying the entire FoxNet root application.

Do not package or overwrite unless specifically approved:

```text
shared phone shell
shared compiled phone UI
shared FoxNet welcome page
shared root assets/js/app.js
JOB-04 Wrecking Yard files
JOB-05 BeamBook files
JOB-07 Collector Exchange files
JOB-08 garage/storage/insurance files
JOB-09 Tow files
JOB-10 design-system files
JOB-02 shared bridge files
```

If a shared file change is truly required, stop and coordinate with its owning job before packaging it.

## Visual handback required from JOB-13

When the backend prototype is stable, send JOB-10:

1. exact ZIP name, size and SHA-256;
2. exact route/app identity;
3. changed-file inventory;
4. full data/action contract;
5. sample payloads for every page;
6. all success, empty, loading and failure states;
7. real vehicle-thumbnail field/path behavior;
8. buttons/actions currently functional;
9. buttons/actions intentionally deferred;
10. phone viewport dimensions and host constraints;
11. screenshots/video of the working debug UI if available;
12. logs proving real bid, invoice, payment, ownership and storage behavior.

JOB-10 will then adapt the approved mobile FoxNet Auctions visuals to the real contract without replacing JOB-13's business logic.

## Verification reminders

- Phone-only release target.
- Preserve PC code but hide/defer PC pages.
- No claim of working until David tests the exact ZIP.
- No fake money, ownership, inventory, garage or invoices.
- No startup monkey-patch of vehicleShopping.
- No full catalog regeneration on every page open.
- No cartoon or unrelated vehicle imagery.
- No silent buttons.
- No duplicate charge or duplicate vehicle on repeated callback.
- No West Coast-only dependency.
