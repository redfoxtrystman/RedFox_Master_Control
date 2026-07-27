# JOB-04 Audit — v0.2.4 Native RLS Joe's Junk / No Startup Load

**Date:** 2026-07-27 1226PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Assistant:** Sol / ChatGPT  
**Base:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_1246PT_v0_2_1_ROLLBACK_TO_v0_1_9_LAST_STOCK_LOADING.zip`  
**RLS reference inspected:** `1(2).zip` — uploaded RLS v2.6.8 beta reference, not packaged into this patch  
**Output:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1.zip`

## Reason for Patch

David reported that the RedFox / IceFox welcome page itself was taking 20–30 seconds to load, and Scrap Yard could take over a minute and still not show stock. Failed prior attempts proved that the slow RedFox web-card clone and broad RLS shop opening are not acceptable.

This patch returns to the rollback base and removes startup vehicleShopping work from the phone/browser welcome page. Scrap Yard now hands off to the native RLS Joe's Junk seller only.

## Explicit Failed Builds Not Used

```text
v0.2.0 = first bad for stock loading
v0.2.2 = opened all stores because it used openShop(nil, nil, 'buying')
v0.2.3 = slow/no stock because it still used custom RedFox web-card filtering
```

## Main Technical Change

The native RLS target is:

```lua
career_modules_vehicleShopping.openShop('joesJunkDealership', nil, 'buying')
```

This is intended to open Joe's Junk only, not the full marketplace and not every store.

## Changed Code Files

```text
assets/js/icefox_front.js
sites/scrap_yard/assets/css/scrap.css
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
ui/ui-vue/dist/index.js
```

## Not Touched

```text
RLS Lua files
career inventory/money/delivery logic
RedFoxScrapYardDirect startup modules
sell/scrap/strip/import systems
all unrelated site content
```

## Startup Load Changes

Removed/avoided:

```text
forceShopRefresh:true at welcome/frame startup
setTimeout(rfSendCareerData, 750)
setTimeout(rfSendCareerData, 2500)
onLoad: rfSendCareerData
Scrap Yard page retry delays / SHOP_RETRY_DELAYS
Scrap Yard page auto vehicleShopping requests
```

## Verification

```text
ZIP integrity: PASS
Entry count: 941
JavaScript syntax checks: PASS
No startup forceShopRefresh:true in touched web files: PASS
No Scrap Yard retry delays left: PASS
Phone frame forwards RedFoxScrapYardOpenJoesJunk: PASS
PC bridge has Joe's Junk native open call: PASS
Vue route has Joe's Junk native open call: PASS
Vue route no longer auto-runs rfSendCareerData on load/timeouts: PASS
No RedFoxScrapYardDirect startup module: PASS
Output SHA256: 83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
```

## Runtime Status

Unproven until David tests this exact ZIP in BeamNG.

Expected test:

```text
1. Install this JOB-04 test ZIP plus RLS.
2. Open phone browser.
3. Welcome page should no longer wait 20–30 seconds on vehicleShopping.
4. Open Scrap Yard.
5. Click Open Joe's Junk.
6. It should open Joe's Junk only, not every store.
```

## Notes for Next Work

If this works, next step is not regional import yet. Next step is to confirm buy ownership/delivery/storage path through the native RLS seller and then add owned-vehicle sell/scrap flow using stock inventory data.
