# JOB-13 / JOB-04 Auction Route Ownership Repair — Triple Verification

Overall result: **PASS**

## Gate 1 — Before editing
- Source ZIP hashes recorded.
- ZIP integrity, path safety and duplicate-path checks passed.
- Both JOB-04 legacy Auction trees confirmed byte-identical.
- Bad route confirmed in desktop, phone and Legal Portal entries.
- Approved allowlist established before changes.

## Gate 2 — After editing
- JOB-04 v0.3.2.3.1: exactly 7 route files changed; exactly 112 legacy Auction files removed; all other files byte-identical.
- JOB-04 v0.3.2.4.1: exactly 7 route files changed; exactly 112 legacy Auction files removed; all other files byte-identical.
- JOB-13 v0.1.8.1: 2 unique route files added, 8 obsolete shared route files removed, 7 metadata/route files changed.
- All 117 JSON files parsed.
- All 74 JavaScript files passed `node --check`.
- Desktop, phone and Legal routes resolve to the unique JOB-13 path.
- JOB-04/JOB-13 active path collisions: 0.
- JOB-13 Quick Bid, max bid, cancellation, watchlist, lot details, Fox Facts, results and membership remain present.
- JOB-13 `openPurchaseMenu` references: 0.

## Gate 3 — After ZIP creation
- Each ZIP passed `testzip`.
- Duplicate internal paths: 0 in every ZIP.
- Unsafe internal paths: 0 in every ZIP.
- Every ZIP entry hash matched its edited build tree.
- Each ZIP was extracted into a fresh folder.
- Every extracted file hash matched the build tree.
- Freshly extracted JOB-04/JOB-13 overlays have zero path collisions.
- Freshly extracted desktop, phone and Legal routes all resolve to JOB-13.

## Output artifacts
- `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`
  - SHA-256: `e4cf49a1adf4d86d996a7c1f098fe19dc1db670f0b53094435486844e58389b1`
  - Files: 717
- `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_4_1_AUCTION_ROUTE_TO_JOB13.zip`
  - SHA-256: `8543523506c75047bfc0f5fe66b81fdf81839687c8e7989d6f6f116255d69cb3`
  - Files: 723
- `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_1_UNIQUE_FOXNET_ROUTE.zip`
  - SHA-256: `74c7a786253f088b90a2ab78a75d8ec61b3fd9c2d1a471b3f311d5e6771b4bcb`
  - Files: 19

## Runtime status
Static and package verification passed. BeamNG runtime behavior remains unproven until David installs the matching JOB-04 and JOB-13 ZIPs together and tests the phone Welcome Page Auction link.

## Lua parser note
A standalone `luac` executable was not available. The only Lua edits were exact route/build-label string replacements; protected Lua logic remained byte-identical.
