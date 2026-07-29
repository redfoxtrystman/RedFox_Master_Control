# JOB-04 — RedFox Wrecking Yard v0.3.0 Build Audit

**Build time:** 2026-07-28 23:17 PT  
**Runtime status:** UNPROVEN  

## Source

- Source ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_1936PT_v0_2_9_NATIVE_IDS_REAL_PRICES_CYCLE_NEGOTIATION_FROM_v0_2_8.zip`
- Source SHA-256: `246cf5ca47274ebc8686eab6b5cdd6edbfd7247dd7c817e6ca44e8890958beb2`
- Source runtime decision: REJECTED — David still observed every listing at $500 and no meaningful inventory change.

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_2317PT_v0_3_0_DIRECT_NATIVE_PRICES_VERSIONED_ASSETS_CYCLING_FROM_v0_2_9.zip`
- SHA-256: `b8809bce620e2d66e58b2f18cd6be8c17df5463a3c111d2af9c0519f91114d71`
- Size: `25,290,733 bytes`
- ZIP entries: `983`
- ZIP integrity: PASS
- Duplicate internal paths: `0`

## Confirmed pre-edit finding

BeamBook itself generates varied asking prices and stores them in `Value`. It also retains varied mileage, year, native `shopId`, and `negotiationPossible = true`.

The flat $500 behavior came from JOB-04 v0.2.8's conversion/clone layer. v0.2.9 source attempted to correct it, but runtime still behaved like v0.2.8 and reused the same WebUI asset paths. The replacement therefore removes the conversion layer and uses never-before-used page, JavaScript, and config paths.

## Architecture

v0.3.0:

- calls BeamBook's normal generation/sync hook
- reads native entries from `career_modules_vehicleShopping.getShoppingData()`
- filters only `sellerId == "beambook"`
- displays native `Value` unchanged
- preserves native `shopId`
- preserves native `negotiationPossible`
- creates no synthetic listing
- writes no price field
- rewrites no seller ID
- applies RedFox Wrecking Yard branding only in the webpage
- filters visible inventory toward older, higher-mileage, lower-priced and work/special vehicles
- rotates the visible subset locally
- can explicitly expire the current BeamBook source pool and request a new pool
- normalizes numeric native shop IDs in the PC purchase bridge

## Cache/runtime proof

- Versioned page: `sites/scrap_yard/index_v030.html`
- Versioned script: `sites/scrap_yard/assets/js/scrap_v030.js`
- Versioned config: `sites/scrap_yard/assets/config/wrecking_yard_mix_v030.json`
- Visible badge: `JOB-04 v0.3.0`
- PC and phone IceFox routes now point to `index_v030.html`.
- Compatibility copies of `index.html`, `scrap.js`, and `wrecking_yard_mix.json` were also replaced with the v0.3.0 content.

## Changed files — 25

```text
OPEN_ME_FIRST_JOB-04_Wrecking-Yard_v0_3_0_DIRECT_NATIVE_PRICES.txt
assets/js/icefox_front.js
docs/job04_v030_direct_native_prices/JOB-04_v0.3.0_INCIDENT_AMENDMENT.md
docs/job04_v030_direct_native_prices/OPEN_THIS_VERIFICATION_REPORT_JOB-04_v0.3.0.html
docs/job04_v030_direct_native_prices/VERIFY_JOB-04_v0.3.0.json
docs/job04_v030_direct_native_prices/VERIFY_JOB-04_v0.3.0.txt
info.json
sites/scrap_yard/assets/config/wrecking_yard_mix.json
sites/scrap_yard/assets/config/wrecking_yard_mix_v030.json
sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/assets/js/scrap_v030.js
sites/scrap_yard/index.html
sites/scrap_yard/index_v030.html
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/docs/job04_v030_direct_native_prices/JOB-04_v0.3.0_INCIDENT_AMENDMENT.md
ui/modModules/redfoxCareerWeb/docs/job04_v030_direct_native_prices/OPEN_THIS_VERIFICATION_REPORT_JOB-04_v0.3.0.html
ui/modModules/redfoxCareerWeb/docs/job04_v030_direct_native_prices/VERIFY_JOB-04_v0.3.0.json
ui/modModules/redfoxCareerWeb/docs/job04_v030_direct_native_prices/VERIFY_JOB-04_v0.3.0.txt
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix_v030.json
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap_v030.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index_v030.html
```

## Protected files not changed in v0.3.0

- `ui/ui-vue/dist/index.js`
- BeamBook files
- RLS vehicleShopping source files
- native inventory/purchase implementation

## Static and packaged verification

PASS:

- all active/compatibility Scrap Yard JavaScript files pass `node --check`
- PC and phone IceFox JavaScript pass `node --check`
- config and `info.json` parse as JSON
- mirrored Scrap Yard JavaScript, HTML, and config are identical
- mirrored PC shell JavaScript is identical
- versioned PC and phone routes are present
- visible `JOB-04 v0.3.0` badge is present
- active script reads `Value` first
- active script contains no `minimumPrice`
- active script contains no `redfoxYardPrice`
- active script contains no synthetic `5000000` listing ID
- active script contains no RedFox seller-ID rewrite
- active script contains no negotiation disable
- PC bridge calls `openPurchaseMenu('instant', nativeShopId)` after numeric normalization
- changed HTML local references resolve
- ZIP passes `unzip -t` and Python `testzip()`
- duplicate ZIP entry count is zero
- fresh extraction of the final ZIP passes the same syntax and architecture checks

## Exact packaged JavaScript fixture test

The exact `scrap_v030.js` extracted from the final ZIP was executed in a Node VM with 100 simulated BeamBook records.

PASS:

- `Value = 12345` overrides `finalValue = 500`
- zero `Value` falls through to positive `marketValue`
- an actual native `$500` listing remains `$500`
- 36 displayed fixture vehicles retained 36 unique prices
- cycle 1 produced a different visible selection than cycle 0
- all selected `shopId` values remained native

## Runtime test

1. Remove or disable every older JOB-04 ZIP.
2. Keep BeamBook and RLS enabled.
3. Install the exact v0.3.0 ZIP.
4. Fully restart BeamNG.
5. Open IceFox and enter Wrecking Yard.
6. First confirm the visible `JOB-04 v0.3.0` badge. If the badge is absent, stop: the correct page is not active.
7. Confirm prices vary and are not all $500.
8. Confirm most ordinary cars are older, high-mileage, or lower-priced.
9. Confirm work/tow/special vehicles can still appear.
10. Press `Cycle Yard Inventory` and confirm the visible cars change.
11. Press `Generate New Source Pool` and confirm BeamBook creates a different source pool.
12. Open a negotiable car and verify negotiation appears.
13. Complete one phone purchase and one PC purchase.
14. Verify money, delivery, ownership, inventory, storage, and no duplicate spawn.

## Hard gate

No v0.3.1 until the exact v0.3.0 runtime result is recorded in issue #30.
