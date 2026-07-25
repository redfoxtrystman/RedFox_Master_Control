# JOB-04 Audit — v0.2.2 Use Stock RLS Showrooms

**Date:** 2026-07-25 1625PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Build:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_1625PT_v0_2_2_USE_STOCK_RLS_SHOWROOMS_FROM_v0_2_1.zip`  
**Base:** `v0.2.1_ROLLBACK_TO_v0_1_9_LAST_STOCK_LOADING`  
**Runtime status:** unproven until David tests in BeamNG.

## Reason

David reported that v0.2.0 broke vehicle stock loading completely. The page no longer populated vehicles even after Refresh Yard List. David then directed JOB-04 to stop cloning the marketplace and to use the same RLS car sale/showroom setup and same shop source that career already uses.

## Order of Operations Applied

1. Do not use v0.2.0 as a base.  
2. Use v0.2.1 rollback, which is an exact copy of v0.1.9, as the working baseline.  
3. Inspect RLS `vehicleShopping.lua`.  
4. Confirm RLS opens the stock showroom through `career_modules_vehicleShopping.openShop`.  
5. Patch only the Scrap Yard stock-market handoff.  
6. Do not edit RLS Lua originals.  
7. Verify changed files, JavaScript syntax, ZIP integrity, and absence of the banned Scrap Yard Direct startup module.

## RLS Code Path Confirmed

RLS stock showroom path:

```text
career_modules_vehicleShopping.openShop(nil, nil, "buying")
```

Inside RLS this path:

```text
- calls updateVehicleList() without fromScratch=true
- keeps map-specific vehicle filtering through getCurrentLevelIdentifier()
- triggers ChangeState to vehicleShopping
- uses the stock vehicleShopping UI
- uses stock images, filters, sorting, and purchase/delivery flow
```

## Patch Behavior

The Scrap Yard Buy section now opens the stock RLS/BeamNG vehicle market instead of trying to populate a custom RedFox list that imitates the market.

This was done because the custom RedFox listing path repeatedly caused partial behavior:

```text
- stock loading failures
- cropped/custom vehicle preview layout
- partial buy flow where money could be removed but the vehicle was not properly stored
```

The new direction is to hand the buy/showroom flow back to stock RLS.

## Changed Files

```text
assets/js/icefox_front.js
sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/index.html
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html
ui/ui-vue/dist/index.js
```

## Not Changed

```text
RLS Lua originals
career inventory logic
money logic
vehicle storage logic
garage logic
scrap/sell implementation
regional import/shipping
refresh limits
trailer/cargo warnings
```

## Static Verification

```text
Source ZIP integrity: PASS
RLS openShop found: PASS
RLS openShop uses vehicleShopping state: PASS
RLS openShop updates vehicle list: PASS
JavaScript syntax checks: PASS
Output ZIP integrity: PASS
No redfoxScrapYardDirect startup module: PASS
Scrap page sends RedFoxOpenRlsVehicleShopping: PASS
Phone frame forwards RedFoxOpenRlsVehicleShopping: PASS
PC bridge handles RedFoxOpenRlsVehicleShopping: PASS
Vue phone route handles RedFoxOpenRlsVehicleShopping: PASS
Automatic Scrap Yard stock polling removed from page open: PASS
```

## Output

```text
SHA256: 6194338a6283a32ddb1d87170dea71ff16598a1ac464ec8d0f3d79cb7754653a
Entry count: 932
```

## Test Instructions

1. Remove v0.2.0 from BeamNG mods.  
2. Install v0.2.2.  
3. Keep RLS career overhaul installed.  
4. Full restart BeamNG.  
5. Open phone / IceFox / Scrap Yard.  
6. Click **Open Stock RLS Market**.  
7. Confirm the stock RLS vehicle market opens.  
8. Confirm vehicle listings populate using the current map’s RLS stock.  
9. Buy one vehicle through the stock RLS purchase UI.  
10. Report whether the vehicle goes into inventory/storage correctly.

## Important Note

This is not proven in runtime. It is a static patch that follows David’s direction to stop cloning RLS market behavior and call the actual stock RLS showroom path instead.
