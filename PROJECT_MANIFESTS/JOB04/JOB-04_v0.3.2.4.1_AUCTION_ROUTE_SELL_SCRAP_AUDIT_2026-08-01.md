# JOB-04 v0.3.2.4.1 — Auction Route + My Vehicles / Native Sell / Whole Scrap Audit

## Runtime context

David runtime-tested the paired route baseline:

- JOB-04 v0.3.2.3.1 Auction Route to JOB-13
- JOB-13 v0.1.8.1 Unique FoxNet Route

Observed:

- FoxNet Welcome Page opened.
- Wrecking Yard opened and listed vehicles.
- Wrecking Yard purchase completed and the vehicle appeared in the garage.
- JOB-13 Auction route worked.
- No shipping delay was observed; immediate garage availability was accepted.
- My Vehicles / Sell / Scrap was absent because v0.3.2.3.1 still points to `index_v032.html`.

## Source

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_4_STEP04_MY_VEHICLES_NATIVE_SELL_WHOLE_SCRAP_FROM_v0_3_2_3.zip`

SHA-256: `d6f6795a84acddd694b8ea1a8f76b490e10aa51bc58a2e7891c26a318558499a`

## Route reference

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`

SHA-256: `e4cf49a1adf4d86d996a7c1f098fe19dc1db670f0b53094435486844e58389b1`

## Output

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_4_1_AUCTION_ROUTE_MY_VEHICLES_NATIVE_SELL_WHOLE_SCRAP.zip`

SHA-256: `0d177d5d940ac3c24ca7f6008a93ad9f548a046078a755b3ea25d4319a9f514f`

Files: 723

## Exact changes from v0.3.2.4

- Removed 112 obsolete copied Auction files under only:
  - `sites/foxnet_auctions/**`
  - `ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/**`
- Changed exactly seven route files:
  - `assets/config/routes.json`
  - `assets/js/icefox_front.js`
  - `pages/legal/index.html`
  - `ui/modModules/redfoxCareerWeb/assets/config/routes.json`
  - `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
  - `ui/modModules/redfoxCareerWeb/pages/legal/index.html`
  - `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js`
- All Auction routes now target:
  - `sites/redfox_job13_auctions/index.html?v=0181`
  - phone-relative equivalent

## Preserved byte-for-byte from v0.3.2.4

- `index_v0324.html` in both Wrecking Yard mirrors
- `scrap_v0324.js` and `scrap_v0324.css` in both mirrors
- My Vehicles lazy-loading behavior
- Native Career/RLS Sell Vehicle relay
- Whole Vehicle Scrap transaction and duplicate protection
- Wrecking Yard purchase adapter
- Yard listings, prices, mileage, negotiation and purchase behavior
- Welcome styling, icon and unrelated websites

## JOB-13 compatibility

Compared with:

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_1_UNIQUE_FOXNET_ROUTE.zip`

SHA-256: `74c7a786253f088b90a2ab78a75d8ec61b3fd9c2d1a471b3f311d5e6771b4bcb`

Results:

- JOB-13 provides both required `redfox_job13_auctions/index.html` targets.
- Overlapping file paths between JOB-04 v0.3.2.4.1 and JOB-13 v0.1.8.1: 0.
- Old `foxnet_auctions/index.html` route references remaining in JOB-04: 0.

## Static verification

- ZIP integrity: PASS
- Duplicate paths: 0
- Unsafe paths: 0
- Exact diff boundary: 112 removals + 7 route changes only
- JavaScript syntax for changed route scripts: PASS
- JavaScript syntax for both `scrap_v0324.js` mirrors: PASS
- Wrecking Yard sell/scrap runtime files unchanged from v0.3.2.4: PASS
- BeamNG runtime: UNPROVEN for this exact v0.3.2.4.1 ZIP

## Required runtime test

Install only this JOB-04 v0.3.2.4.1 ZIP and JOB-13 v0.1.8.1. Confirm:

1. Welcome Page opens.
2. Wrecking Yard opens with badge v0.3.2.4.
3. `My Vehicles & Scrap` appears.
4. Yard purchase still reaches Career inventory/garage.
5. Auction opens through JOB-13.
6. Native Sell Vehicle removes one selected vehicle and credits once.
7. Scrap Whole Vehicle removes the selected vehicle and pays once with no returned parts.
8. No lag, crash, duplicate vehicle, double payment or route regression.
