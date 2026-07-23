# JOB-04 Scrap Yard / Wrecking Yard — v0.1.5 Performance + PC/Phone Parity Audit

**Date/time:** 2026-07-23 1433PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Build:** `zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PERFORMANCE_PC_PHONE_PARITY_2026-07-23_1433PT_v0_1_5.zip`  
**Baseline:** `zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PHONE_PC_BRIDGE_2026-07-22_2222PT_v0_1_4_FROM_PHONE_WORKING_CURRENT_RLS_UI.zip`

## User-tested state before this patch

David tested v0.1.4 and reported:

```text
IT WORKS AND I CAN BUY A CAR
```

Runtime facts from David:

```text
- Scrap Yard opened.
- Buy flow opened.
- David bought a Mustang.
- Page switching was very slow.
- Clicking pages could show white/grey for up to about 30 seconds.
- Sell flow was not tested.
- Seller patience did not appear to change during haggling.
```

## Goal of v0.1.5

Do not rebuild the working purchase path. Patch only performance and PC/phone page parity.

```text
- Keep working buy path from v0.1.4.
- Stop heavy RLS/vehicleShopping data refresh on every page open.
- Make Scrap Yard draw immediately.
- Make yard stock load only when Refresh Yard List is clicked.
- Cache the yard stock during the session.
- Mirror PC and phone Scrap Yard page files so PC is not using a second/different Scrap Yard copy.
```

## Files changed

```text
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
sites/scrap_yard/index.html
sites/scrap_yard/assets/css/scrap.css
```

## What changed in Scrap Yard page JS

```text
- Removed automatic RLS refresh calls on Scrap Yard page init.
- Removed the page-open chain:
  setTimeout(requestCareerData,150)
  setTimeout(requestCareerData,3500)
  setTimeout(requestCareerData,12000)
- Shortened shop wait from 45 seconds to 12 seconds.
- Reduced retry delays from [0,2500,8000,16000,30000] to [0,1500,5000].
- Added sessionStorage cache under redfox_scrap_cached_shopdata_v015.
- Added [RedFox][SCRAP][PERF] console timing logs.
- Changed no-data text to explain stock does not auto-load on page open.
```

## What changed in PC shell JS

```text
- Removed automatic career/RLS refresh on DOMContentLoaded.
- Removed automatic startup refresh at 500ms.
- Removed 30-second retry storm inside requestNow.
- requestNow now forwards cached data quickly and only asks RLS when a nested page requests data.
- Added [RedFox][SCRAP][PERF][PC] console timing logs.
```

## What changed in phone shell JS

```text
- Removed automatic RLS refresh on every route/frame load.
- Removed automatic startup refresh/retry timers.
- Kept nested-page message forwarding.
- Phone and PC now both rely on the nested Scrap Yard page sending RedFoxRequestCareerData when Refresh Yard List is clicked.
```

## PC/phone parity fix

The duplicated Scrap Yard copies were mirrored:

```text
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
```

and the duplicated PC front scripts were mirrored:

```text
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
```

This is intended to stop PC from using an older/different Scrap Yard page copy than the phone/browser path.

## Static checks run

```text
ZIP integrity: PASS
ZIP reopened/testzip: PASS
JavaScript syntax checks: PASS
No __pycache__ / .pyc: PASS
No redfoxScrapYardDirect entries: PASS
No startup Scrap Yard career module added: PASS
PC and UI Scrap Yard JS identical: PASS
PC and UI IceFox front JS identical: PASS
Old 30-second retry strings removed from active target files: PASS
Scrap Yard auto requestCareerData on page open removed: PASS
```

## ZIP facts

```text
ZIP name: zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PERFORMANCE_PC_PHONE_PARITY_2026-07-23_1433PT_v0_1_5.zip
Entry count: 945
SHA256: 698abb25bbd4e239ee38cad7ca193a993cc18a2d432d13071cf53868a93baa71
```

## Install rule

Use only:

```text
RLS Career Overhaul 2.6.6
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PERFORMANCE_PC_PHONE_PARITY_2026-07-23_1433PT_v0_1_5.zip
```

Remove/disable:

```text
old JOB-04 v0.1.0
old JOB-04 v0.1.1
old JOB-04 v0.1.2
old JOB-04 v0.1.3
old JOB-04 v0.1.4
all other zzzz_RedFox_FoxNet... zips
all RedFox_ScrapYard_Direct... zips
```

## Expected test behavior

```text
- BeamNG title/loading screen should not be grey-broken.
- Phone IceFox should still appear if v0.1.4 did.
- PC IceFox should still appear if v0.1.4 did.
- Browser pages should paint faster because they no longer auto-refresh RLS data on every page open.
- Scrap Yard should open immediately with a message saying to click Refresh Yard List.
- Clicking Refresh Yard List should request RLS/shop data and populate yard stock.
- Buy flow should remain the same working path as v0.1.4.
```

## Still unproven

```text
- v0.1.5 runtime speed improvement until David tests it.
- Sell flow.
- Seller patience behavior.
```

## Important note

This patch intentionally does not chase seller patience yet. The buy UI opened and a car was purchased through the currently working path, so performance/page-load behavior is the immediate blocker.
