# JOB-04 Audit — v0.2.2 BAD: Opened All Stores Instead of Wrecking Yard Stock

**Date:** 2026-07-25  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** BAD / DO NOT USE AS BASE

## User Runtime Report

David reported that v0.2.2 caused every store in the game to pop up instead of showing only vehicles appropriate for a wrecking yard / scrap yard.

## What Went Wrong

The v0.2.2 patch used:

```lua
career_modules_vehicleShopping.openShop(nil, nil, "buying")
```

That was too broad. It opened the stock RLS/BeamNG vehicle shopping interface globally, which can expose all shops/stores rather than a filtered wrecking-yard subset.

## Correct Direction

Do not use global `openShop(nil, nil, "buying")` for JOB-04.

The correct approach is:

```text
Use RLS/BeamNG vehicleShopping data source and purchase flow,
but filter/select only wrecking-yard/salvage/junk/used listings.
```

Required behavior:

```text
- Pull from the same RLS/current-map vehicle shop data source.
- Do not open every dealership/store.
- Show only listings appropriate for a wrecking yard.
- Allow occasional better finds.
- Preserve stock RLS purchase flow for ownership/storage/delivery.
- Do not hand-roll money, spawning, storage, garage, or inventory.
```

## Version Status

```text
v0.2.0 = BAD: stock loading broken/no cars.
v0.2.1 = rollback to v0.1.9 last stock-loading baseline.
v0.2.2 = BAD: opens all stores, too broad.
```

## Next Required Patch Scope

The next patch must be based on v0.2.1 / v0.1.9, not v0.2.0 or v0.2.2.

The next patch must inspect RLS vehicleShopping data and implement a filtered yard view:

```text
Base: v0.2.1 rollback / v0.1.9
Goal: filtered wrecking-yard stock from RLS source
Do not use: openShop(nil,nil,"buying") as the main UI action
Do not touch: unrelated websites, regional import, timers, refresh limits, scrap/sell flow
```

Runtime is unproven until David tests any future patch in BeamNG.
