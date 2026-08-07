# JOB-13 v0.1.9.5 — Save Isolation / Single Persistence Owner

**Date:** 2026-08-07
**Branch:** `job13-online-auctions`

## Build

ZIP: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_5_SAVE_ISOLATION_SINGLE_OWNER.zip`

SHA-256: `e003c68eff2ef276685ec8794e2efde6e9d227e9ecfe7dfaf768fc730995eb90`

Base: v0.1.9.4 SHA-256 `285b741b26f30e7eb00011f695e035394d5b65af346249599f2f66251f8ccd12`

## Reason

v0.1.9.4 runtime testing showed Bought Vehicles/payment history could cross into a new Career save. The live auction state was save-specific, but the ledger loader still imported the old global JOB-13 ledger when a new save had no local ledger. Account profile had the same global fallback risk.

## Changes

- Removed global legacy ledger fallback.
- Removed global legacy account fallback.
- Account and ledger remain per-Career and are stamped with `careerSavePath`.
- Files stamped for a different Career save are rejected.
- Auction snapshot excludes `state.account`; the account profile is the sole persistent owner of membership, saved searches, watchlist, and reminder.
- Auction snapshot validates its Career save stamp when present.
- Save-slot switches clear async purchase/delivery runtime maps.
- Purchase ledger records retain `deliveryKey`.
- JOB-04 global Wrecking Yard acquisition records are ignored unless they carry a matching Career-save stamp.
- Only global JOB-13 stores left are user settings and installed-content cache; no Career progress belongs there.

## Verification

Static triple verification passed:

- 19 files before/after;
- 11 changed; no added/removed paths;
- Lua syntax passed;
- JavaScript syntax passed;
- JSON parsed;
- three route HTML mirrors identical;
- no old global account/ledger/state fallback reads remain;
- final ZIP integrity passed;
- fresh extraction matches edited tree byte-for-byte.

Runtime remains unproven until tested across two Career saves.

## First runtime test

Open Save A, note JOB-13 account/transaction/auction data, then switch to Save B. Save B must not inherit Save A's Bought/Sold Vehicles, invoices, membership, watchlist, reminder, bids, consignments, or auction state. Return to Save A and verify its own data remains.
