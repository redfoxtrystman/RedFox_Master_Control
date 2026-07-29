# JOB-09 v0.4.3 Build Audit

**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Date:** 2026-07-29  
**Build:** v0.4.3 — Per-Yard Storage, Shop Transfer, Lien Claims, Sales, Auctions, and Scrap  
**Status:** STATIC AND MOCK-INTEGRATION VERIFIED — BEAMNG / INSTALLED RLS RUNTIME UNTESTED

## Scope implemented

- Replaced the misleading shared global yard-capacity behavior with three independent capacities on every saved RedFox yard:
  - custody / impound storage;
  - company fleet / shop bays;
  - claimed-vehicle sales staging.
- Added paid Career-money upgrades per yard and per storage type.
- Added safe linking from a RedFox yard to one real purchased RLS garage on the same map.
- Restored shop-vehicle transfers using the native inventory garage-move path while preserving the same Career inventory ID and ownership.
- Added return-to-previous-garage and undo-last-verified-move operations.
- Added lien/title acquisition after legal hold expiration with:
  - tow lien;
  - storage charged for no more than three elapsed days;
  - title-transfer fee;
  - sales-staging and native-garage capacity checks;
  - insufficient-funds protection;
  - rollback with custody record retained and no charge if vehicle creation or movement fails.
- Added claimed-vehicle disposition methods:
  - direct market-value sale;
  - persistent Copart-style timed auction;
  - scrap;
  - dynamic launcher for a compatible native Career sale/offers or My Vehicles screen.
- Added persistent business ledger, shop inventory, auction listings, portal state, portal actions, and legacy WEUI controls.
- Preserved the v0.4.2.1 all-mission generation correction, police blockers, Random Events live bridge, and same-map active-job recovery.

## Default business values

- Custody upgrade: +5 spaces, starting at $7,500.
- Company/shop upgrade: +2 bays, starting at $15,000.
- Sales-staging upgrade: +3 spaces, starting at $10,000.
- Repeat-upgrade multiplier: 1.40 per yard/type.
- Claim storage charge cap: 3 days.
- Title-transfer fee: $350.
- Direct sale: 100% of stored estimated market value.
- Scrap: 12% of stored estimated market value.
- Copart-style auction duration: 300 seconds.
- Auction reserve: 60% of stored estimated market value.

## Safety boundaries

- No artificial garage/property injection.
- No `addPurchasedGarage` call.
- No stock/RLS override path.
- No vehicle delete-and-copy transfer.
- Shop transfer verifies the same inventory ID at the destination and verifies ownership was not lost.
- Claim cost is not retained unless one owned inventory record is created, verified, and moved successfully.
- Direct sale, auction acceptance, and scrap do not queue payment until the exact inventory vehicle is verified removed.
- One purchased RLS garage cannot be linked to two RedFox yards.
- Garage links cannot be removed while company/shop inventory still uses them.
- Cross-map owned-vehicle movement is not implemented in this build.
- Node Grabber/cable restoration is not implemented in this build.
- The legacy unsafe transfer implementation remains uncalled and is not exposed in the UI.

## Verification completed

The exact source and packaged artifact passed:

- ZIP CRC/test.
- No duplicate ZIP entries.
- No unsafe archive paths.
- No executable/native payloads.
- No protected stock/RLS override paths.
- Lua syntax compilation.
- Mocked Lua module loading.
- Portal JavaScript syntax.
- All JSON parsing.
- Portal image readability.
- Portal-to-Lua action parity.
- Direct-sale integration mock.
- Auction integration mock.
- Insufficient-money rollback mock.
- Source-to-package hash comparison for all non-regenerated verification files.
- 42 total verifier checks.

Mock integration results:

```text
INTEGRATION_OK money=90850 pending=1
AUCTION_INTEGRATION_OK money=90850 pending=1
INSUFFICIENT_ROLLBACK_OK money=1000
```

## Exact artifact

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_3_PerYardStorageShopTransferLienClaimsSalesAuctionsScrap.zip
SHA-256: 19ca72c6ccaa36610425d26a2e0e9d775dfe338f8d728b6bc2fbe226038ab6f1
Size: 1,619,761 bytes
ZIP entries: 127
```

## Required runtime test order

1. Mission-generation regression.
2. One paid capacity upgrade at only one yard.
3. Link one real purchased RLS garage.
4. Transfer one owned shop truck and confirm same inventory ID/ownership.
5. Return and undo transfer.
6. Test insufficient-money lien claim.
7. Test successful lien claim and exact three-day storage cap.
8. Test direct sale.
9. Test auction persistence/cancel/accept.
10. Test scrap.
11. Test native Career sale/offers launcher without duplicate RedFox payment.

Runtime results must be appended to JOB-09 issue #4.