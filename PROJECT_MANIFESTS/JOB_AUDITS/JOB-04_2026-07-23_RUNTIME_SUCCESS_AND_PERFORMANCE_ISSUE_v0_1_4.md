# JOB-04 Runtime Audit — v0.1.4 Buy Works, Navigation Very Slow

**Date:** 2026-07-23  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** runtime partly proven by David, performance problem remains

---

## Build under test

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PHONE_PC_BRIDGE_2026-07-22_2222PT_v0_1_4_FROM_PHONE_WORKING_CURRENT_RLS_UI.zip
```

## David's runtime result

David reported:

```text
IT WORKS AND I CAN BUY A CAR BUT ITS VERY SLOW.
```

Additional detail:

```text
- Clicking pages causes a white or grey screen.
- Page hang can last up to about 30 seconds.
- David bought a Mustang successfully.
- Sell flow was not tested yet.
- Seller patience did not change on one attempted buy; David suspects this may be a game/RLS bug rather than this mod.
```

This is the first confirmed runtime report for the current repaired JOB-04 line where the Scrap Yard purchase flow can successfully buy a vehicle.

---

## Current confirmed state

```text
Phone/PC/Scrap Yard access: at least partly working
Buying vehicle through Scrap Yard flow: runtime confirmed by David
Selling owned vehicle: not tested yet
Performance/page switching: broken or unacceptable, hangs up to 30 seconds
Grey/title-screen fatal UI break from earlier builds: not reported on v0.1.4 in this result
```

---

## Likely performance cause

The likely problem is not the final purchase bridge itself, because buying succeeded.

Likely causes to inspect next:

```text
1. Each page navigation may be doing a full iframe/page reload.
2. Scrap Yard and/or IceFox pages may request live RLS shop data immediately on load.
3. Some pages may wait for direct RedFoxCareerData / vehicleShopping responses before painting the UI.
4. The PC/phone wrapper may be retrying or timing out around the 30-second mark.
5. Heavy RLS vehicle shop refresh calls may be running too often instead of only when the user clicks Refresh Yard List.
6. Root and mirrored copies of IceFox front scripts may still not behave identically.
```

---

## Next planned fix

Do not change purchase behavior yet. The buy path is currently proven enough to preserve.

Next patch should focus only on speed and page-loading behavior:

```text
- Keep v0.1.4 buy path intact.
- Add lightweight loading shell so page contents appear immediately.
- Stop auto-refreshing heavy shop data on every navigation.
- Cache the most recent RLS shop data in JS memory for the session.
- Only call updateVehicleList/getShoppingData when user clicks Refresh Yard List or the cache is empty/stale.
- Add timing logs around page load, bridge request start, bridge response, and render complete.
- Add a non-blocking timeout message instead of leaving a blank white/grey page.
```

Suggested log prefixes:

```text
[RedFox][SCRAP][PERF]
[RedFox][SCRAP][LOAD]
[RedFox][SCRAP][BRIDGE]
[RedFox][SCRAP][BUY]
[RedFox][SCRAP][SELL]
```

---

## Preserve these working pieces

Do not rewrite or discard:

```text
- The v0.1.4 current RLS UI compatibility approach unless proven to still break title/menu UI.
- The working buy/open-purchase path.
- The phone-working baseline logic that v0.1.4 restored.
- The PC mirror bridge that allows Scrap Yard to reach the same behavior.
```

---

## Do not reintroduce banned pieces

```text
- No redfoxScrapYardDirect.
- No startup Scrap Yard career module.
- No map-load parking/shop generation.
- No fake money.
- No fake storage.
- No fake garage insert.
- No fake ownership.
- No full stale ui-vue/dist/index.js from old builds.
```

---

## Next user request likely

David wants the page switching / white-grey hang fixed. Build should be named with date/time for tracking, for example:

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PERF_PATCH_2026-07-23_<TIME>PT_v0_1_5.zip
```

Runtime success must still be separated by feature:

```text
Buy: proven by David on v0.1.4
Sell: unproven
Performance: bad, needs patch
```