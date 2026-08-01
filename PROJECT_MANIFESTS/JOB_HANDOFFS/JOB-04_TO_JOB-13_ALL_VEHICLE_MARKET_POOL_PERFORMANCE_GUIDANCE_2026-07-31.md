# JOB-04 → JOB-13 Guidance: All-Vehicle Auction Market Without Full-Catalog Loading

**Date:** 2026-07-31  
**Source owner:** David / Captain  
**Coordinator:** JOB-04 Welcome Page + Wrecking Yard  
**Target:** JOB-13 Online Auctions / Auction Yard  
**Status:** Architecture and repair guidance only — no JOB-13 source edited here

## Owner report

The Auction Yard previously loaded quickly but exposed too few vehicles. After it was changed to include all vehicles while showing only 10 at a time, the long-loading problem returned.

The intended result is:

```text
Auction may eventually select from every installed, loadable vehicle/configuration
BUT
only 10 active market lots are created, hydrated, sent to the browser, and rendered at one time.
```

The critical distinction is:

```text
"Access to every vehicle" != "fully load every vehicle before selecting 10"
```

## What JOB-04 proved

The Wrecking Yard stopped its long-loading problem by enforcing these boundaries:

1. The FoxNet welcome page performs zero vehicle inventory work.
2. Vehicle discovery starts only after the feature page is opened.
3. The page requests a bounded listing set, not every dealership and every vehicle.
4. The browser receives only the data required for the visible cards.
5. No retry storm, repeated full scan, or preload of every image/configuration.
6. The selected listing uses native Career/RLS purchase completion instead of duplicating the whole market system in the webpage.

JOB-13 should apply the same separation to Auction.

## Required target architecture

### Layer 1 — compact catalog index

Create a lightweight index of installed, loadable vehicle/config IDs. Each catalog row should contain only compact metadata needed for selection, for example:

```text
catalogId
modelKey
configKey
displayName
vehicleType/category
thumbnail key/path hint
value hint or pricing category
installed/loadable flag
tags/eligibility flags
source/mod fingerprint
```

Do not store or resolve full parts trees, JBeam data, damage, full images, detailed descriptions, or instantiated vehicles for the entire catalog.

### Layer 2 — persistent market pool

The market pool should contain catalog IDs or small market-candidate records, not fully hydrated vehicle objects.

It may cover all eligible installed vehicles while remaining cheap to keep in memory and on disk.

The pool should support:

- weighted/random selection;
- category limits;
- duplicate prevention;
- seen/recently-used tracking;
- optional damaged/junk/rare weighting;
- modded vehicle inclusion only when BeamNG confirms the config is loadable.

### Layer 3 — exactly 10 active lots

Maintain only 10 active auction lots by default.

When one sells, expires, or is removed:

1. choose one replacement catalog ID;
2. hydrate only that selected vehicle;
3. append one new lot;
4. mark state dirty;
5. persist once through the normal debounced save path.

Do not regenerate or rehydrate the entire catalog to replace one lot.

### Layer 4 — lazy hydration

Only the 10 active lots should resolve the heavier fields needed by the webpage, such as:

```text
model/config display data
price and bid values
condition summary
mileage
thumbnail/image
seller/source
damage or history fields
```

If useful, hydrate in small batches, such as two to five lots per frame/tick, while the page remains responsive.

The browser must never receive hundreds or thousands of hidden vehicle cards.

## Cache and first-run behavior

The catalog should be cached and versioned using a fingerprint based on the game version and installed vehicle/mod set.

Recommended behavior:

```text
Auction page opens
  -> send cached active 10 lots immediately
  -> render page immediately
  -> if catalog cache is stale, begin incremental rebuild in the background
  -> do not block the page on the full rebuild
```

On a true first run with no catalog cache:

- show a small safe starter market as soon as possible;
- build the larger catalog incrementally;
- expand future replacement choices as the index becomes available;
- never freeze the page while enumerating every installed configuration.

Provide an explicit owner/debug action such as `Rebuild Vehicle Catalog` rather than rebuilding the entire catalog on every page open.

## Startup and Welcome Page rule

The FoxNet Welcome Page must not load Auction inventory, enumerate vehicle configs, hydrate lots, or start a full catalog scan.

The Welcome Page may show only the Auction card/link and lightweight installed-status information.

Auction work begins only after Auction is opened, and cached active lots should be returned before any background catalog maintenance.

## Persistence rule

JOB-13 already had a confirmed excessive-write defect:

- `onUpdate()` called `tickLots()` every 0.5 seconds;
- `tickLots()` called `saveState(false)` even when nothing changed;
- the state could be written roughly every two seconds, about 1,800 times per hour.

The full-catalog repair must not reintroduce this pattern.

Required persistence behavior:

```text
mark dirty only when a lot, bid, timer boundary, catalog version, sale, settlement, or setting actually changes
save through one debounced/event-driven path
no unconditional save from a half-second scan
no full catalog rewrite for every timer tick
```

Persist active lots and compact catalog/cache data separately if that prevents rewriting a large catalog whenever one bid changes.

## Do not do these things

- Do not enumerate and fully hydrate all installed vehicles before selecting 10.
- Do not load all thumbnails into the DOM and hide all but 10.
- Do not query every dealership/shop as a way to discover every vehicle.
- Do not rebuild the catalog every time the Auction page opens.
- Do not poll the entire catalog every 0.5 seconds.
- Do not write unchanged auction or catalog state every two seconds.
- Do not spawn vehicles merely to inspect them for market selection.
- Do not fake native shop IDs, ownership, money, inventory, or delivery.
- Do not let Auction loading delay the Welcome Page.

## Suggested control flow

```text
onAuctionPageOpen()
  load activeLots cache
  return up to 10 active lots immediately

  if catalog cache missing/stale and not already building:
    beginIncrementalCatalogBuild()

  hydrate only missing details for activeLots

onLotSoldOrExpired(lotId)
  settle/remove the exact lot once
  replacementId = marketPool.nextEligible()
  replacementLot = hydrateOne(replacementId)
  append replacementLot
  markDirty("activeLots")

onCatalogBuildStep()
  inspect a bounded number of configs
  append compact catalog rows
  yield until next safe update
  when complete, store new fingerprint and mark catalog cache complete
```

The exact BeamNG/RLS APIs must be confirmed from the source JOB-13 is using. Do not guess function names or replace working native operations blindly.

## RLS market comparison

David wants Auction to behave like its own RLS-style market:

- a broad eligible source pool;
- a small rotating active stock;
- persistent listings;
- replacement stock generated only when needed;
- native Career/RLS money, ownership, inventory, and delivery remain authoritative.

JOB-13 should inspect how the current RLS market/shop code separates candidate stock from visible active stock and reuse the bounded-stock concept where compatible. Do not copy every RLS market file or open every RLS shop to achieve coverage.

## Required test gates

### Performance

- Welcome Page opens with no Auction vehicle loading.
- Auction page displays cached active lots quickly.
- Hard maximum target: usable Auction page within 10 seconds.
- Preferred cached target: visible active lots within about 1–2 seconds.
- Exactly 10 active lots are sent/rendered by default.
- No hundreds/thousands of hidden cards in the browser.
- Closing and reopening Auction does not rebuild the full catalog.

### Catalog coverage

- Catalog can eventually contain all eligible installed/loadable configs.
- Modded configs are included only when confirmed loadable.
- Hidden/test/broken configurations can be filtered through explicit eligibility rules.
- Refresh/replacement can draw vehicles not shown in the first 10.
- Repeated replacements prove the pool is broader than the initial page.

### Persistence

- Idle Auction causes no repeated full-state writes.
- One bid changes only the needed auction state.
- One sale/removal creates one replacement lot and one debounced save sequence.
- Catalog cache is not rewritten because an unrelated bid timer advanced.

### Correctness

- No duplicate lot IDs.
- No duplicate purchase, delivery, charge, seller payment, or ownership transfer.
- No lost no-sale vehicle.
- No catalog rebuild alters active ownership records.
- Browser code never edits money, ownership, inventory, or save files directly.

## Coordination with JOB-04 Welcome Page

JOB-04 owns the FoxNet Welcome Page and its Auction link/card. JOB-13 owns the Auction page and auction business logic.

When JOB-13 has a fast runtime-tested build, provide JOB-04 with:

```text
exact Auction page path
exact ZIP name and SHA-256
visible version/build ID
required Lua extension name
installed/missing behavior
card title and image/icon path
minimum compatibility requirements
```

JOB-04 will update only the Welcome Page link/integration after the JOB-13 page is proven fast and stable.

## Immediate JOB-13 repair order

1. Revert or isolate the change that blocks the page while loading all vehicles.
2. Preserve the previous working Auction UI and transaction behavior.
3. Measure where full catalog enumeration/hydration occurs.
4. Separate compact catalog discovery from active-lot hydration.
5. Return the existing/cached 10 active lots before catalog maintenance.
6. Build or refresh the broad catalog incrementally.
7. Repair the unconditional idle-save loop if not already fixed.
8. Test with only JOB-13 first.
9. Then test through the JOB-04 Welcome Page link.
10. Only after that test with JOB-09 and other modules.
