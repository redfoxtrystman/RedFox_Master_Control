# JOB-13 v0.1.4 — Approved-Pool Performance Patch

**Date/time:** 2026-07-31 06:49 PDT  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Owner:** David / Captain  
**Status:** BUILT — STATIC/HARNESS PASS — BEAMNG RUNTIME UNTESTED

## Runtime report that triggered this patch

David reported that opening the auction system still required approximately 2–5 minutes, matching the earlier Wrecking Yard/Scrap Yard inventory-generation failure. Bidding and purchasing could not yet be tested because the catalog did not become usable quickly enough.

## GitHub evidence reused from JOB-04

JOB-04 issue #30 documents the accepted no-lag pattern:

- generate/cache the larger candidate pool in Lua;
- do not open dealerships or force full shop refreshes;
- reuse the cached pool on revisit;
- send only a small visible page, approximately 12–24 listings;
- do not render 100–200 complete cards at once;
- no retry storm.

The JOB-13 patch applies that architecture without copying JOB-04 code or editing JOB-04 files.

## Exact input

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_3_SLIM_PATCH.zip
SHA-256: 660f6fb5eae9f54cae4173590ac08d1de7655ca3ccfc7e14b8fa7f72ed2dee1e
```

## Exact output

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_4_APPROVED_POOL_PATCH.zip
SHA-256: 56c4143cbb3233dd187bfe22aafeca48b5024e917cd3e1d4a25626033402c84f
Files: 35
Compressed size: 424,268 bytes
```

## Changes

- State schema increased from 2 to 3.
- Added `data/redfox_job13/approved_vehicle_pool_v1.json`.
- Pool ID: `redfox.job13.approved.v1`.
- Approved entries: 21 explicitly named and categorized vehicles.
- Each approved entry points to one packaged real vehicle image.
- Any legacy schema-2, oversized, or unapproved catalog is discarded on first load.
- A new 12-lot catalog is created once from the approved pool.
- Page open performs no dealership, `vehicleShopping`, installed-mod, or configuration scan.
- Browser receives 12 lightweight catalog summaries initially.
- Full Fox Facts, damaged/missing parts, invoice, shipping, and bid history load only after one lot is opened.
- Duplicate initial bridge requests removed.
- Safety refresh reduced to once per 60 seconds.
- Images use lazy loading and asynchronous decoding.
- New versioned WebUI path `redfoxJob13Auctions_v014/**` prevents stale v0.1.2/v0.1.3 page assets.
- v0.1.3 dirty-state persistence remains in place; idle state is not continuously rewritten.

## Static verification

```text
ZIP integrity: PASS
JavaScript syntax: PASS
Lua syntax: PASS using LuaTeX loadfile compiler
JSON parsing: PASS
Behavior harness: PASS
Legacy schema-2 migration: PASS
Approved pool count: 21
Approved image references: 21/21 valid
Initial visible summaries: 12
120-second simulated idle writes: 0 additional writes
Duplicate ZIP paths: NONE
Forbidden shared/core paths: NONE
Heavy shop/config scan call search: NONE
```

## Files deliberately not included

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfoxCareerWeb.lua
ui/modModules/redfoxCareerWeb/**
JOB-04 Wrecking Yard files
JOB-09 Tow/Recovery files
shared Browser Core route files
```

## Critical route note

The standalone v0.1.4 UI App loads the new page. A phone icon owned by JOB-01/Browser Core may still open an older copied `foxnet_auctions` site. This patch does not silently modify that shared route. Test the standalone v0.1.4 UI App first to separate JOB-13 catalog performance from an obsolete phone route.

## Required owner test

1. Disable/remove all older JOB-13 ZIPs.
2. Install only v0.1.4.
3. Add the new v0.1.4 JOB-13 UI App.
4. Time catalog load; target is under 10 seconds.
5. Confirm exactly 12 visible approved lots.
6. Confirm Register and Search do not cause a long pause.
7. Only then test membership, bidding, bid cancellation, timer closing, invoice, and shipping in TEST mode.

## Keep/reject rule

- If the standalone app opens within 10 seconds, keep v0.1.4 and coordinate the shared phone route separately.
- If the standalone app still takes minutes, capture `beamng.log` immediately and reject the current backend rather than layering another patch blindly.
