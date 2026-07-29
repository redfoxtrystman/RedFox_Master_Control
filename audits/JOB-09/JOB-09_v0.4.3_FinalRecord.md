# JOB-09 v0.4.3 Final Artifact Record

**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Version:** 0.4.3  
**Date:** 2026-07-29  
**Status:** STATIC AND MOCK-INTEGRATION VERIFIED — RUNTIME UNTESTED

## Artifact

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_3_PerYardStorageShopTransferLienClaimsSalesAuctionsScrap.zip
```

```text
SHA-256: 19ca72c6ccaa36610425d26a2e0e9d775dfe338f8d728b6bc2fbe226038ab6f1
Size: 1,619,761 bytes
Entries: 127
```

## Verification summary

- Archive CRC: PASS
- Duplicate entries: NONE
- Unsafe paths: NONE
- Executable/native payloads: NONE
- Protected stock/RLS override paths: NONE
- Lua syntax: PASS
- Mocked Lua load: PASS
- JavaScript syntax: PASS
- JSON parse: PASS
- Portal action parity: PASS
- Direct-sale integration mock: PASS
- Auction integration mock: PASS
- Insufficient-money rollback mock: PASS
- Source/package non-verification-file comparison: IDENTICAL
- Total verifier checks: 42 PASS

## Main feature set

- independent per-yard custody, company/shop, and sales-staging capacity;
- paid Career-money upgrades;
- safe link to existing purchased RLS garage;
- same-inventory-ID owned shop-truck transfers;
- return and undo garage movement;
- lien acquisition with three-day storage cap and title fee;
- Shop / Resale Inventory;
- direct market sale;
- Copart-style persistent auction;
- scrap;
- dynamic native Career sale/offers launcher;
- persistent business ledger;
- preserved v0.4.2.1 mission-generation emergency correction.

## Required first runtime proof

Do not mark this version working until David verifies, in order:

1. Abandoned Vehicle mission accepts normally.
2. Only the selected yard changes after one paid capacity upgrade.
3. A real purchased RLS garage can be linked.
4. One shop truck moves while preserving its Career inventory ID and ownership.
5. An insufficient-money lien claim keeps the custody record and does not charge.
6. A successful claim creates one owned vehicle and charges the displayed total.
7. Direct sale removes the exact vehicle before payment.
8. Auction state persists and cancel/accept behave correctly.
9. Scrap removes the exact vehicle before payment.
10. Native sale/offers does not cause duplicate RedFox payment.

## Runtime boundaries

- Cross-map vehicle movement is not included.
- Node Grabber/cable restoration is not included.
- Installed private RLS API behavior remains unproven until runtime testing.
- No official/documented native auction API is assumed; Copart-style auction is the built-in fallback/primary auction workflow.