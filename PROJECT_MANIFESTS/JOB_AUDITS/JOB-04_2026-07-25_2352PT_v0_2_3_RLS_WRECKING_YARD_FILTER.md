# JOB-04 Audit — v0.2.3 RLS Wrecking Yard Filter

**Date:** 2026-07-25 2352PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Build:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_2352PT_v0_2_3_RLS_WRECKING_YARD_FILTER_FROM_v0_2_1.zip`  
**Base:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_1246PT_v0_2_1_ROLLBACK_TO_v0_1_9_LAST_STOCK_LOADING.zip`

## Reason

David reported that v0.2.2 opened every store in the game. The owner direction was corrected:

```text
Use the same RLS vehicleShopping stock source the normal car market uses, but only show cars that belong in a wrecking yard / salvage yard, with occasional better finds.
Do not open every store.
```

## Bad Builds Not Used

```text
v0.2.0 = first bad for stock loading
v0.2.2 = bad because it opened every store
```

## Scope

This patch returns to the rollback base and keeps the Scrap Yard page using the existing RedFox/RLS data bridge instead of opening the broad stock marketplace.

The patch filters the RLS `vehiclesInShop` list before rendering:

```text
- Joe's Junk / discounted / junk / salvage / scrap / wreck / auction / used / abused / parts sellers
- cheap vehicles
- high-mile vehicles
- parts/scrap/junk text
- strong salvage-score vehicles
- one occasional better find from the same RLS stock pool
```

It also blocks aircraft/helicopter/prop listings from the yard list and fixes the false `Bus` classification caused by matching `bus` inside `abused`.

## Code Files Changed

```text
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
```

## Not Touched

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
phone bridge
PC bridge
RLS Lua
money system
inventory/storage system
delivery/purchase completion path
sell/scrap/strip systems
regional import system
timers/refresh limits
```

## Verification

```text
Source ZIP integrity: PASS
Output ZIP integrity: PASS
JavaScript syntax: PASS
Code changed files expected only: PASS
No v0.2.2 broad open-all-stores marker: PASS
Uses RedFoxRequestCareerData / RLS vehiclesInShop source: PASS
Keeps RedFoxScrapYardOpenPurchaseMenu buy path: PASS
Wrecking-yard filter present: PASS
Bus/abused false-positive fix present: PASS
Full-car image CSS present: PASS
ui/ui-vue/dist/index.js unchanged: PASS
phone bridge unchanged: PASS
PC bridge unchanged: PASS
No redfoxScrapYardDirect startup module: PASS
```

## Output Hash

```text
SHA256: a34c4823946e11912394c9b10705da5883386dd7fd01cfdd6774d544ddd05f05
Entry count: 932
```

## Runtime Status

Unproven until David tests this exact ZIP in BeamNG.
