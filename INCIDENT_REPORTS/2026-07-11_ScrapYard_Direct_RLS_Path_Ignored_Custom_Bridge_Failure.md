# 2026-07-11 — ScrapYard Direct RLS/BeamNG Path Ignored / Custom Bridge Failure

## Status

Recorded as a project/process failure for RedFox / IceFox / BeamNG web shop work.

This report is intentionally blunt because the user repeatedly asked for the Scrap Yard / auction pages to use the same existing RLS/BeamNG shop data and purchase path that the stock shop already uses. Later builds moved away from the only path that was proven in-game and introduced custom RedFox Lua/web bridge calls that were not requested and were less reliable.

## User-visible failure

The user later found that `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_RLS_SHOPDATA_ON_EXISTING_BRIDGE_STATIC` was the best/partly working version:

- Scrap Yard page showed real cars for sale.
- User bought a cop car through the stock purchase flow.
- User stripped the bought car.
- Refresh worked several times in the same game session.
- Later it stopped loading new cars, likely due to timeout/TTL/cache/refresh behavior.

Later builds regressed by routing shop requests through custom methods such as:

- `getRlsShopDataJson`
- `getScrapYardShopDataJson`
- `openScrapYardPurchaseMenuJson`

These produced user-facing failures such as:

- `redfoxCareerWeb method unavailable`
- `No reply from RedFox Lua bridge`

## Core mistake

The assistant did not stay on the user-requested direct path:

```text
Use the existing RLS/BeamNG shop data and purchase systems that the stock shop already uses.
Do not hand-roll buying, money, storage, garage, or fake inventory behavior.
```

The working-ish v0.10.3 pattern was:

```text
Page sends RedFoxRequestCareerData
→ existing Vue wrapper handles request
→ Lua_default.career_modules_vehicleShopping.updateVehicleList(true)
→ Lua_default.career_modules_vehicleShopping.getShoppingData()
→ page receives vehiclesInShop/shopData
→ purchase button calls career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)
```

That path is close to what the stock shop uses and was proven by the user in-game.

The later custom bridge path was unnecessary for the user’s stated goal and caused avoidable regression.

## Relevant user instructions / intent to preserve

The user stated, in substance and in later complaint, that the requested target was:

```text
"It was reading the same RLS/BeamNG shop data that the stock shop uses."
```

The user objected that they did not ask for a custom bridge and wanted direct linkage to existing systems.

Other standing RedFox/BeamNG rules that apply:

- Do not fake working systems.
- Do not hand-roll career buying, money, inventory, storage, or garage movement when BeamNG/RLS already has these systems.
- Prove behavior against actual files before packaging.
- Label runtime behavior unproven unless David tests it in BeamNG.
- Preserve the last known working path instead of replacing it with a new architecture.

## Technical comparison summary

### v0.10.3 partly worked because

- It used the existing phone/Vue wrapper path.
- It asked `career_modules_vehicleShopping` for shop data.
- It used `openPurchaseMenu("instant", shopId)` for purchase.
- It did not depend on a custom `redfoxCareerWeb.getScrapYardShopDataJson` method being available inside the iframe/page.

### Later versions regressed because

- They introduced custom RedFox Lua extension bridge methods for shop data and purchase.
- The web page then depended on methods that were not reliably available from phone/PC iframe contexts.
- The user saw bridge-unavailable/no-reply errors.
- This wasted time and obscured that the stock/RLS path was already partly working.

## Suspected remaining v0.10.3 issue

The best current hypothesis for why v0.10.3 works initially and then stops loading/refreshing is:

```text
slow RLS shop generation + short JS/web timeout + TTL/cache/sold-list refresh behavior + repeated forced refresh
```

BeamBook/RLS-related timeout/TTL clues:

- BeamBook uses an offer TTL pattern around `OFFER_TTL = 10 * 60`.
- RLS vehicle shopping has offer/sold/refresh timing behavior.
- v0.10.3 page has JS waits/timeouts that may be too short for heavy shop generation.
- The page sorts/selects low-price junk repeatedly, causing repeated listings.

## Required next technical direction

Do not continue custom RedFox shop-data bridges for this feature unless the user explicitly requests them.

Next fix should be based on the v0.10.3 direct path:

1. Preserve the direct Vue/`Lua_default.career_modules_vehicleShopping` request path.
2. Increase/adjust async waiting so slow generation does not look like failure.
3. Add better refresh/rotation logic.
4. Avoid repeatedly selecting the same cheapest cars.
5. Add Copart/FoxNet auction page as a separate test page using the proven direct path.
6. Add weighted categories:
   - parts car / scrap only
   - salvage rebuildable
   - runs and drives
   - police/seized
   - fleet damage
   - rare/collector
   - small unicorn chance for higher-end/decent cars listed by mistake
7. Keep purchase opening through `career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)`.

## Accountability note

This was an assistant process failure. The user’s request was to connect to the systems already used by BeamNG/RLS. The assistant instead introduced custom bridge methods and then debugged those custom bridge failures, wasting time and producing regressions.

Do not repeat this pattern.
