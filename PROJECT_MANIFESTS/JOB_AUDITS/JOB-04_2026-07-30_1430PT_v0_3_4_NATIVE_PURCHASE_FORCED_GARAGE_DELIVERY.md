# JOB-04 v0.3.4 — Native Purchase / Forced Garage Delivery

**Date:** 2026-07-30 14:30 PDT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Source artifact:** `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1129PT_v0_3_3_OWNED_SALES_SCRAP_RETURNED_PARTS_CATS_FROM_v0_3_2.zip`  
**Source SHA-256:** `3ccd8e440c0b74581218cea08c55f72b1480b46b0fbb68d0cbcb6f10af84884f`  
**Final artifact:** `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1430PT_v0_3_4_NATIVE_PURCHASE_FORCED_GARAGE_DELIVERY_FROM_v0_3_3.zip`  
**Final SHA-256:** `e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75`  
**Size:** 25,581,535 bytes  
**ZIP entries:** 1,047  
**Runtime:** UNPROVEN

## Owner runtime failure being fixed

v0.3.3 opened the standard RLS purchase page, but the final Purchase action used the spawn-near-player path. The purchase sound played, the vehicle appeared loose near the player, the purchase page stayed open, and the vehicle was not inserted into Career/RLS garage inventory.

## Confirmed cause

The active JOB-04 page only called:

```lua
career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)
```

The RLS purchase UI later called `buyFromPurchaseMenu` with an options table whose `makeDelivery` value could remain false. The old JOB-04 browser sessionStorage flags were not consumed by RLS and therefore never forced garage delivery.

## v0.3.4 corrective action

Added:

```text
lua/ge/extensions/redfoxWreckingYardPurchase.lua
```

The adapter:

1. Verifies the selected real native `shopId` still exists.
2. Saves the native `buyFromPurchaseMenu` and `cancelPurchase` functions.
3. Temporarily wraps only the next Wrecking Yard purchase request.
4. Opens the standard native purchase page with `openPurchaseMenu("instant", shopId)`.
5. When the player presses Purchase, copies the native options and forces `makeDelivery = true`.
6. Preserves insurance, dealership, negotiation and other native options.
7. Restores the original native functions immediately before calling the real native purchase function.
8. Restores the original functions on Cancel as well.

The adapter contains no manual money subtraction, manual spawn, ownership creation, inventory insertion, garage movement, or vehicle removal logic.

## Active page changes

- Added versioned `index_v034.html` and `scrap_v034.js` in both mirrored site trees.
- PC and phone routes now load `index_v034.html`.
- The Wrecking Yard page calls the GE Lua adapter directly through `bngApi.engineLua`.
- Added an 8-second click lock and disabled purchase buttons while the native menu opens.
- The old postMessage purchase bridge remains only as unused compatibility code; the active v0.3.4 page no longer calls it.

## Preserved unchanged

- v0.3.3 junk-focused listing selection.
- Native prices, seller records, negotiation and real shop IDs.
- Owned vehicle selling.
- Whole vehicle scrap.
- Strip & Scrap Shell.
- Returned parts and catalytic-converter scrap.
- RLS Vue bundle.
- v0.3.3 rollback HTML/JS.
- Owner-edited phone/browser icon.
- Wrecking Yard mix and Undesireables catalog.

## Verification

- JavaScript syntax: PASS.
- Lua syntax: PASS through `luatex --luaonly` / `loadfile`.
- Purchase adapter runtime harness: PASS.
  - native shop validation
  - numeric ID normalization
  - Purchase forces `makeDelivery=true`
  - caller options are not mutated
  - insurance and dealership options preserved
  - native functions restored after Purchase
  - native functions restored after Cancel
  - missing listing blocked
- Manual transaction API scan: PASS.
- Mirrored HTML/JS parity: PASS.
- Owner icon hash: PASS.
- RLS UI bundle protected hashes: PASS.
- Existing v0.3.3 selling/scrap backend hash: PASS.
- ZIP integrity: PASS.
- Duplicate paths: 0.
- Unsafe paths: 0.
- Fresh extraction parity: PASS, 1,047 files.
- Packaged JavaScript/Lua syntax: PASS.
- Packaged purchase adapter harness: PASS.

## Runtime gate

Before any v0.3.5 work:

1. Disable v0.3.3 and all older JOB-04 ZIPs.
2. Install exact v0.3.4 and fully restart BeamNG.
3. Confirm the Wrecking Yard badge says `v0.3.4`.
4. Buy one inexpensive vehicle only.
5. Confirm the vehicle does not remain loose near the player.
6. Confirm the purchase page closes normally.
7. Confirm the vehicle appears exactly once in Career/RLS inventory and a real garage.
8. Confirm money is deducted exactly once.
9. Confirm the purchased listing is removed/marked sold once.
10. If it fails, record whether money changed, whether a loose vehicle spawned, whether the UI stayed open, and capture the BeamNG log before another purchase.

No further purchase attempt should be made on v0.3.3.