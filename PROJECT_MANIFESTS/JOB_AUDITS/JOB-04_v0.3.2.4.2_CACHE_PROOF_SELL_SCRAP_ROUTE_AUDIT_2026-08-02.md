# JOB-04 v0.3.2.4.2 — Cache-Proof Sell / Whole Scrap Route Audit

## Source

- Source ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_4_1_AUCTION_ROUTE_MY_VEHICLES_NATIVE_SELL_WHOLE_SCRAP.zip`
- Runtime finding: PC and phone buying work, but BeamNG continued showing the older inventory-only Wrecking Yard page with no Sell Vehicle or Scrap Whole Vehicle section.

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-02_v0_3_2_4_2_CACHE_PROOF_SELL_WHOLE_SCRAP_ROUTE_FROM_v0_3_2_4_1.zip`
- SHA-256: `751501c31f2acafb5dc79a4965d7bda77818445e0c1308b7135dc9a6468b7391`
- Files: 729
- Runtime: untested

## Narrow change

- Added newly named `index_v03242.html`, `scrap_v03242.js`, and `scrap_v03242.css` in both required Wrecking Yard website roots.
- Updated desktop, mirrored desktop, and phone Welcome routes to the new page with query token `03242-cache-proof-route`.
- Converted legacy Wrecking Yard entry pages (`index.html`, `index_v030.html`, `index_v031.html`, `index_v032.html`, and `index_v0324.html`) in both roots into compatibility redirects to the new page.
- Updated `info.json` package identity.

## Protected unchanged behavior

- Wrecking Yard inventory selection and rendering logic.
- Forced-garage native purchase adapter.
- Native Career/RLS Sell Vehicle logic.
- Whole-vehicle scrap removal, payout, retry, and duplicate protection.
- JOB-13 unique Auction route `redfox_job13_auctions/index.html?v=0181`.
- All unrelated websites and Lua/business logic.

## Verification

- ZIP integrity: PASS
- Duplicate paths: 0
- Unsafe paths: 0
- Fresh extraction: PASS
- Added files: exactly 6 expected files
- Changed files: exactly 14 expected route/redirect/metadata files
- Removed files: 0
- JavaScript syntax: PASS
- Both Wrecking Yard mirrors contain My Vehicles & Scrap, Sell Vehicle, and Scrap Whole Vehicle
- Every legacy Wrecking Yard entry redirects to the new page
- JOB-13 overlap: 0 paths

## Required runtime test

1. Disable every older JOB-04 ZIP.
2. Keep JOB-13 v0.1.8.1 installed.
3. Install only JOB-04 v0.3.2.4.2.
4. Clear WebUI cache and restart BeamNG.
5. Open Wrecking Yard from PC and phone.
6. Confirm badge `v0.3.2.4.2` and visible `My Vehicles & Scrap` tab.
7. Test one native vehicle sale and one whole-vehicle scrap only after the new page is visible.

Receipts are deferred to a separate patch after this visibility test passes.
