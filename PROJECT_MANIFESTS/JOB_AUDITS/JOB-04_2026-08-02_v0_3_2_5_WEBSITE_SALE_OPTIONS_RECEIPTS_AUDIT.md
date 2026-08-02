# JOB-04 v0.3.2.5 — Website Sale Options and Receipts Audit

**Date:** 2026-08-02  
**Owner:** David / Captain  
**Job:** JOB-04 — Wrecking Yard + current FoxNet Welcome host  
**Runtime status:** STATIC/HARNESS VERIFIED — BEAMNG RUNTIME UNTESTED

## Source baseline

- File: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-02_v0_3_2_4_2_CACHE_PROOF_SELL_WHOLE_SCRAP_ROUTE_FROM_v0_3_2_4_1.zip`
- SHA-256: `751501c31f2acafb5dc79a4965d7bda77818445e0c1308b7135dc9a6468b7391`

## Output

- File: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-02_v0_3_2_5_STEP05_WEBSITE_SALE_OPTIONS_RECEIPTS_FROM_v0_3_2_4_2.zip`
- SHA-256: `cf44b77f8e0126c7ad6183934e36561fa5f0fd0868b627fe923de51dc17f5a5a`
- Installable files: 735

## Owner-requested first stage

The Wrecking Yard website now presents the final three-choice disposition layout:

1. **Sell Whole Vehicle** — active; uses the existing native Career/RLS sale transaction.
2. **Auto Strip Good Parts + Scrap the Rest** — visible but disabled in this stage. Its displayed rule reserves good parts for the existing RLS parts inventory while parts whose names contain `junk` remain with the chassis for scrap value. The later labor fee will be one included charge rather than separate fluid/handling line items.
3. **Scrap What Is Left** — active; uses the existing exact-vehicle removal and one-time scrap payout. It can be used on an intact vehicle or a vehicle the player stripped manually.

The page also includes a separate **Recent Sale & Scrap Receipts** section.

## Receipt behavior

- A receipt is created only for a transaction whose state is verified `complete`.
- Whole-scrap receipts store the exact credited payout.
- Native-sale receipts try to store the actual Career account balance increase measured across the native sale.
- If the exact native balance delta is unavailable, the receipt explicitly says Career/RLS handled the amount; it does not invent or substitute an estimated amount.
- Receipt ID equals the persistent request ID, preventing duplicate receipts on replay.
- Existing completed v0.3.2.4 transactions are backfilled into receipts when possible.
- Up to 100 receipts persist in `settings/redfox/scrapyard/storage.json`; the website shows the most recent 30.

## Exact scope

- Changed existing files: 19
- Added new cache-versioned files: 6
- Removed files: 0
- Original versions of all changed files are stored separately in `RedFox_JOB-04_v0_3_2_5_CHANGED_ORIGINALS_RECORDS_ONLY_2026-08-02.zip`.

## Protected behavior preserved

- JOB-13 route remains `redfox_job13_auctions/index.html?v=0181`.
- JOB-04 and JOB-13 active file overlap: **0**.
- Wrecking Yard purchase adapter is byte-for-byte unchanged.
- Global Vue bundle is byte-for-byte unchanged.
- Existing Yard Inventory browse/purchase JavaScript was copied unchanged into the new cache-versioned script.
- Both Wrecking Yard website mirrors are byte-for-byte identical.
- All legacy Wrecking Yard entry pages redirect to `index_v0325.html?v=0325-sale-options-receipts`.

## Explicitly deferred

- Automatic RLS parts transfer
- `junk` part classification in the backend
- Chassis + junk-parts weight/value calculation
- Actual vehicle-mass pricing
- In-game daily per-ton scrap market
- Parts Shop inventory, pricing and random sales
- Purchase receipts

The disabled Auto Strip button does not call Lua and cannot remove a vehicle or parts.

## Verification

- JavaScript syntax: PASS
- Lua syntax (`texluac -p`): PASS
- JSON parse: PASS
- New HTML local references: PASS
- Scope/hash comparison: PASS
- Website mirrors: PASS
- Legacy redirect coverage: PASS
- JOB-13 overlap check: PASS (0 paths)
- ZIP integrity and path safety: PASS
- Fresh extraction byte match: PASS
- Lua transaction/receipt harness: PASS — 26 checks
  - loaner exclusion
  - native sale exact removal
  - native sale exact money-delta receipt
  - native sale replay idempotency
  - exact scrap removal and payout
  - exact scrap receipt
  - scrap replay idempotency
  - auto-strip still disabled
  - receipt persistence after module reload

## Runtime test gate

1. Back up the Career save.
2. Disable v0.3.2.4.2 and every older JOB-04 ZIP.
3. Keep JOB-13 v0.1.8.1 enabled.
4. Install only this JOB-04 ZIP and fully restart BeamNG after clearing WebUI cache.
5. Open Wrecking Yard from PC and phone; confirm badge `v0.3.2.5`.
6. Confirm the three sale-option cards and Receipts tab are visible.
7. Confirm **Auto Strip + Scrap** is disabled.
8. Sell one inexpensive vehicle through **Sell Whole Vehicle**; confirm one removal, one payment and one receipt.
9. Scrap a different expendable vehicle through **Scrap What Is Left**; confirm displayed quote, one removal, one payout and one receipt.
10. Restart Career; confirm both vehicles remain absent and both receipts remain.
11. Confirm PC/phone Wrecking Yard purchases and JOB-13 Auctions still work.
12. Stop at the first failure and preserve `beamng.log` and the save backup.

Do not begin automatic stripping until this exact website/receipt stage passes in BeamNG.
