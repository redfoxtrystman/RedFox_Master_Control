# JOB-04 Audit — v0.2.3 Bad: Slow Web Loading / No Stock / Correct Native RLS Seller Direction

**Date:** 2026-07-26  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Filed by:** Sol / ChatGPT  
**Severity:** High — current RedFox web listing path is not acceptable for gameplay or testing

## Runtime Report From David

David reported that the current line is not usable:

```text
- Welcome page took about 20 seconds to load.
- Scrap page took over a minute to load.
- Scrap page could not load cars.
- Earlier v0.2.2 opened every store in the game.
- v0.2.3 attempted filtered custom cards but still did not solve the core loading problem.
```

## Broken Builds To Avoid

```text
v0.2.0 = first bad for stock loading after forced RLS fast-load edits
v0.2.2 = bad because openShop(nil, nil, "buying") opened all stores
v0.2.3 = bad because web listing/filter still loaded too slowly and did not produce stock
```

## Current Safe Base

```text
v0.2.1 rollback / v0.1.9 last stock-loading base
```

This remains the safe rollback base until a better native RLS approach is proven in BeamNG.

## Corrected Direction

David does not want a custom RedFox web page trying to clone the whole RLS market slowly.

The correct direction is to use the same native RLS vehicle market/showroom system the game already uses, but scoped to a specific wrecking-yard seller / yard stock pool instead of opening every shop.

Do not open every dealership/store.

Do not use:

```lua
career_modules_vehicleShopping.openShop(nil, nil, "buying")
```

as the Scrap Yard button target.

The next attempt must inspect RLS first and find the proper native seller/shop/showroom path, then open only that targeted seller/pool.

## Desired Yard Stock Mix

David clarified the desired long-term wrecking yard stock mix:

```text
80% Joe's Junk / normal wrecking-yard stock
10% random mixed finds
5% possible good vehicles with issues
5% heavy/oddball/special stock: heavy trucks, buses, planes, boats, and similar unusual listings
```

This mix should eventually pull from map-appropriate vehicle pools when possible.

## Required Development Rule

Before another package is built:

```text
1. Inspect RLS vehicleShopping files directly.
2. Identify exact native functions and data structures used by RLS showrooms/market.
3. Identify how RLS targets a specific dealer/seller/shop instead of all shops.
4. Start from v0.2.1 rollback, not from v0.2.0, v0.2.2, or v0.2.3.
5. Do not build another custom card clone as the main solution.
6. Do not touch unrelated web pages.
7. Do not add warnings, timers, regional imports, selling, scrapping, or refresh limits in this repair patch.
8. Package only after verification shows the button routes to one targeted native RLS seller/shop path.
```

## Next Patch Target

Suggested next patch name:

```text
JOB-04 v0.2.4 TARGET_NATIVE_RLS_WRECKING_YARD_SELLER_FROM_v0.2.1
```

Primary goal:

```text
Open a targeted native RLS vehicle-shopping seller/pool for wrecking-yard stock, not all stores and not a slow RedFox custom listing clone.
```

Runtime remains unproven until tested in BeamNG.
