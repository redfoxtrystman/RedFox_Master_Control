# JOB-13 v0.1.6 Native Bidding + Garage Delivery Build Audit

Date: 2026-07-31 PT
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions

## Artifact

- File: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_6_NATIVE_BIDDING_GARAGE_DELIVERY.zip`
- SHA-256: `8fa86d6fa09287bd07ba97dd4281362e8c05950b31bfd57da5dfc0f2cc39cce4`
- Runtime files: 21
- Uncompressed bytes: 242358
- Status: STATIC/HARNESS PASS; BEAMNG RUNTIME UNPROVEN

## Owner order implemented

1. Remove the unauthorized LIVE lock and simulated transaction system.
2. Use the supplied RLS/West Coast timed auction behavior for player/NPC bidding.
3. Build the visible auction from a fixed approved pool before the page opens.
4. On player win, use existing RLS `career_modules_vehicleShopping` purchase and delivery.
5. Do not invent another money, inventory, transit, shipping, or garage system.
6. Do not edit other websites.

## Existing game path used

JOB-13 submits the winning vehicle through:

```lua
career_modules_vehicleShopping.openPurchaseMenu("instant", shopId, -1, true)
career_modules_vehicleShopping.buyFromPurchaseMenu("instant", {
  makeDelivery=true,
  purchaseInsurance=false,
  policyId=0,
  dealershipId="private"
})
```

The supplied RLS `vehicleShopping.lua` then performs Career payment, inventory-capacity checking, vehicle spawning, delayed access, garage selection, and `moveVehicleToGarage`.

## Approved pool / performance

The first runtime proof uses only the three fallback configurations explicitly present in the supplied RLS auction source:

- `/vehicles/covet/covet_tutorial.pc`
- `/vehicles/hopper/classic.pc`
- `/vehicles/wendover/se_v6_A.pc`

They are cycled across 12 lots. The page receives cached summaries and full details only on lot opening. There are no calls to `util_configListGenerator`, dealership refresh, `openShop`, or installed-vehicle scanning in JOB-13.

## Verification performed

- ZIP integrity: PASS
- Duplicate ZIP paths: NONE
- Lua syntax: PASS
- JavaScript syntax: PASS
- JSON parsing: PASS
- Nested-frame direct `bngApi.engineLua` bridge harness: PASS
- 12-lot prebuilt catalog harness: PASS
- Career membership money deduction harness: PASS
- Player maximum bid and winning close harness: PASS
- Native temporary shop-record injection: PASS
- Native exact auction-total deduction confirmation: PASS
- Native `makeDelivery=true` call: PASS
- Native shop-record consumption confirmation: PASS
- 120-second idle update test: 0 additional state writes
- Shared main UI bundle / phone layout / redfoxCareerWeb core overrides: NONE
- Other website content: NONE

## Intentional path mirrors

Only the Auction page is mirrored for the two FoxNet mount styles already observed:

- `sites/foxnet_auctions/**`
- `ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/**`

The two HTML pairs are intentionally identical. No welcome, Wrecking Yard, Tow, BeamBook, or other site is included.

## Known limits

- Runtime is not claimed until David tests this exact ZIP.
- The first proof pool has three unique native configurations repeated across 12 lots.
- Fox Facts/damage currently affect price and bidder interest, but this narrow patch does not yet apply every described missing part to the spawned vehicle.
- If the installed FoxNet host blocks top-frame `bngApi` access, `beamng.log` and the exact host ZIP will still be required; the page now shows an explicit bridge error rather than endless LOADING.
