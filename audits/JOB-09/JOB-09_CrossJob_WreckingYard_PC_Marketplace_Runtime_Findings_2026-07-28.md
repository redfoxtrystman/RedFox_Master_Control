# JOB-09 Cross-Job Dependency Note — Wrecking Yard PC Marketplace Runtime Findings

Date: 2026-07-28

## Scope

This is a cross-job dependency note only. The Wrecking Yard / Scrap Yard marketplace belongs to JOB-04. JOB-09 depends on the same PC/browser, marketplace, auction, direct-buy, yard inventory, and property-computer bridges, so the runtime findings must remain available to JOB-09 without taking ownership of JOB-04.

## User-confirmed PC behavior

The RedFox Wrecking Yard page opens from the in-game PC/browser and its vehicle cards can be clicked.

Confirmed working:

- Existing FoxNet / IceFox single-browser route reaches the Wrecking Yard page.
- The page renders vehicle cards and thumbnails.
- Mouse interaction reaches the page.
- This proves the PC/browser route and front-end click layer are usable for future JOB-09 Tow Yard, auction, direct-buy, and company-computer pages.

Confirmed broken or incomplete:

- Every listing is priced at $500.
- Inventory does not rotate, expire, refresh, or cycle to new vehicles.
- Stock is too clean/new and does not resemble a real wrecking-yard or scrap-yard mix.
- No damaged, stripped, salvage, or true scrap-car weighting is visible.
- No negotiation or counter-offer workflow exists.
- Buy Online is front-end only and does not complete a Career purchase.
- Clicking Buy does not deduct money, create one owned inventory record, choose a valid garage, or confirm delivery.

## Important source boundary

JOB-09 v0.4.1 does not contain the fixed-$500 Wrecking Yard listing page, pricing generator, or Buy Online implementation. The screenshot is from the FoxNet / JOB-04 Wrecking Yard marketplace path. JOB-09 may reuse the working browser bridge pattern, but must not duplicate or silently replace JOB-04 logic.

## Reusable bridge architecture

The working part is the path:

1. Existing PC or phone opens the single FoxNet / IceFox browser.
2. Browser router opens a local RedFox website page.
3. HTML/JavaScript renders the cards and receives clicks.
4. A page action must be forwarded through the game UI bridge to GE Lua.
5. GE Lua must call the actual Career/RLS marketplace, shop, auction, money, inventory, garage, and delivery functions.
6. Result data must be returned to the page and the card state refreshed.

The current page proves steps 1-3. Steps 4-6 are not complete for Buy Online.

## Previously identified native RLS seller path

Earlier JOB-04 work identified the native RLS seller call:

```lua
career_modules_vehicleShopping.openShop("joesJunkDealership", nil, "buying")
```

This is valuable because the native seller path can supply stock generation, thumbnails, prices, purchase handling, delivery, and current-map facility data. It should remain the reference for a safe native fallback.

A custom RedFox Wrecking Yard page should not invent fake purchase completion. It should either:

- open the native seller directly, or
- receive real seller stock and listing IDs through a proven bridge, then send a real purchase action back to the native Career/RLS backend.

## Required future marketplace behavior

### Dynamic inventory

- Real stock rotation and refresh.
- Listing expiration and replacement.
- Persisted listing IDs.
- No duplicate purchase of the same listing.
- Scrap-yard weighting toward damaged, high-mileage, stripped, non-running, project, work, trailer, commercial, and salvage vehicles.
- Occasional usable bargains and rare valuable finds.

### Pricing

- No global fixed $500 price.
- Price derived from real estimated value, condition, mileage, missing parts, damage, running state, scrap floor, rarity, and seller behavior.
- A minimum scrap value prevents nonsense negative pricing.
- A maximum cap prevents a wrecking-yard listing from being priced like a pristine dealer car unless it is a rare exception.

### Negotiation

- Buy at asking price.
- Make offer.
- Seller accept, reject, or counter.
- Offer cooldown or limited attempts.
- Seller personality and urgency can affect the result.
- Reverse-haggle workflows remain possible for junk-vehicle pickup jobs.

### Purchase completion

Before charging:

- confirm listing still exists;
- confirm money;
- confirm a valid garage slot;
- choose current garage first, then other owned garages on the map, then owned garages on other maps;
- warn before using another garage;
- create exactly one owned record;
- verify ownership and destination;
- remove the listing only after success;
- roll back payment and inventory on failure.

## JOB-09 reuse

JOB-09 can reuse this bridge for:

- Tow Yard Inventory dispositions;
- direct sale;
- Marketplace listing;
- West Coast auction;
- future Copart-style auction;
- salvage and scrap actions;
- Claim and Transfer to My Garage;
- property-computer access to company fleet and custody records.

The marketplace backend remains cross-job work. JOB-09 should expose actions and records but must not fake ownership conversion or purchase success.

## Next evidence needed

- Exact JOB-04 ZIP/version shown in the screenshot.
- GE Lua/UI log from clicking Buy Online.
- Current listing source data and price-generation function.
- Current bridge action name sent by the Buy button.
- Result of the native `joesJunkDealership` fallback on the same PC.

## Current decision

Treat the PC/browser route as a successful proof of access. Treat pricing, stock rotation, negotiation, and purchase completion as unimplemented. Preserve this pattern for auctions and direct-buy integration, but do not ship another fixed-price front-end-only marketplace.
