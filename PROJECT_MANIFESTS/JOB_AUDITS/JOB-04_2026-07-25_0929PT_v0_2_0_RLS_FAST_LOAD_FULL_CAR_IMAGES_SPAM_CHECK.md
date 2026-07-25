# JOB-04 Audit — v0.2.0 RLS Fast Load + Full Car Images + Spam Check

**Date:** 2026-07-25 0929 PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Base ZIP:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-24_2141PT_v0_1_9_REMOVE_UNAPPROVED_WARNINGS_ONLY_FROM_v0_1_8.zip`  
**Output ZIP:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_0929PT_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK_FROM_v0_1_9.zip`  
**SHA256:** `1275cf32e08c53aaa0d5b3179deb40c0043b1a75000834115f5efa52a9d6b896`

## Owner Request

David reported that the Scrap Yard page is still slow and the car preview images are cropped/zoomed weirdly. David also reported heavy BeamNG UI lag while testing multiple mods and asked JOB-04 to check this mod package for spam/loop behavior when not being used.

## Patch Scope

This patch stays inside JOB-04 / Scrap Yard related behavior. It does not apply the JOB-10 visual style to every site, because that is outside this job.

## Files Changed

```text
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/ui-vue/dist/index.js
```

## What Changed

- Vehicle preview images now use `object-fit: contain` instead of `object-fit: cover`, so full car previews should show instead of cropped/zoomed previews.
- Scrap Yard page no longer schedules repeated delayed stock requests on load.
- Removed the old Scrap Yard load retry chain: `0s`, `2.5s`, `8s`, `16s`, and `30s`.
- Scrap Yard page now asks for current RLS/BeamNG `vehicleShopping.getShoppingData()` first without forcing stock rebuild.
- `Refresh Yard List` is the only Scrap Yard UI path that requests a heavy stock rebuild.
- Phone relay no longer forces a shop refresh on frame/page load.
- PC frame load bridge no longer forces a shop refresh on frame/page load.
- RedFox phone Vue route now only calls `career_modules_vehicleShopping.updateVehicleList(true)` when a message explicitly requests `forceShopRefresh=true`.

## What Did Not Change

```text
- Buy button still uses RedFoxScrapYardOpenPurchaseMenu / vehicleShopping.openPurchaseMenu("instant", shopId).
- Sell path was not redesigned.
- No warning banners were added.
- No regional ordering was added.
- No timer system was added.
- No cargo split was added.
- No scrap/strip tool was added.
```

## RLS Reference

RLS exposes the fast shop data path through:

```text
career_modules_vehicleShopping.getShoppingData()
```

RLS only uses the heavier list rebuild path when shop stock needs to be generated/refreshed:

```text
career_modules_vehicleShopping.updateVehicleList(true)
```

This patch changes JOB-04 so the page opens with the fast data-read path first and uses the heavy rebuild path only from the manual refresh action.

## Static Verification

```text
ZIP integrity: PASS
Entry count: 932
No redfoxScrapYardDirect files: PASS
Scrap Yard retry list removed: PASS
Manual refresh path still exists: PASS
Fast initial load path exists: PASS
Phone startup force-refresh removed: PASS
PC frame-load force-refresh removed: PASS
Vue route guards updateVehicleList(true) behind force flag: PASS
Vehicle preview contain CSS exists: PASS
JavaScript syntax checks: PASS
```

## Spam / Idle Scan Summary

- No `while true` loop was found in this package scan.
- No `redfoxScrapYardDirect` startup module was found.
- JOB-04 repeated delayed Scrap Yard refresh requests were removed.
- JOB-04 phone/PC startup force-refresh behavior was removed.
- The package still contains ordinary UI/framework timers from BeamNG/RLS and one BackAlley `setInterval` for pending document refresh. That was not edited here because this patch is JOB-04 focused and not a BackAlley rewrite.

## Runtime Status

Runtime is unproven until David tests this exact ZIP in BeamNG. Static verification only proves the package contents and syntax checks passed.