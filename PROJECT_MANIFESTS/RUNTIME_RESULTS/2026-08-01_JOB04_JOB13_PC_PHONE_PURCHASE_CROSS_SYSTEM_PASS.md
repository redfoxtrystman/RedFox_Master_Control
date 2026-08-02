# JOB-04 + JOB-13 Cross-System Runtime Pass — PC and Phone Purchases

**Owner report time:** 2026-08-01 21:46 PT

## Exact paired builds

- JOB-04: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_4_1_AUCTION_ROUTE_MY_VEHICLES_NATIVE_SELL_WHOLE_SCRAP.zip`
  - SHA-256: `0d177d5d940ac3c24ca7f6008a93ad9f548a046078a755b3ea25d4319a9f514f`
- JOB-13: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_1_UNIQUE_FOXNET_ROUTE.zip`
  - SHA-256: `74c7a786253f088b90a2ab78a75d8ec61b3fd9c2d1a471b3f311d5e6771b4bcb`

## Owner runtime result

David confirmed the following in BeamNG Career/RLS runtime:

- FoxNet on PC can open and purchase from the Wrecking Yard.
- FoxNet on phone can open and purchase from the Wrecking Yard.
- FoxNet on PC can open and purchase from JOB-13 Auctions.
- FoxNet on phone can open and purchase from JOB-13 Auctions.
- The JOB-04/JOB-13 route collision is no longer reproducing in this pairing.
- Purchased vehicles reach the garage; no shipping delay was observed in the latest Wrecking Yard purchase, which the owner accepts for now.
- Both mods may continue to be used together as the current integration baseline.

## What changed architecturally

- JOB-04 no longer bundles the obsolete copied `foxnet_auctions/**` website trees.
- JOB-04 Welcome/phone/legal routes point to `redfox_job13_auctions/index.html?v=0181`.
- JOB-13 owns the unique Auction website route in both required website roots.
- Static comparison previously confirmed zero overlapping file paths between this JOB-04 and JOB-13 pair.

## Current status matrix

```text
JOB-04 Welcome Page ................. PASS
JOB-04 Wrecking Yard on PC .......... PASS
JOB-04 Wrecking Yard on phone ....... PASS
JOB-04 Wrecking Yard purchase ....... PASS
JOB-13 Auction route on PC .......... PASS
JOB-13 Auction route on phone ....... PASS
JOB-13 Auction purchase on PC ....... PASS
JOB-13 Auction purchase on phone .... PASS
Cross-mod route collision ........... NOT REPRODUCED
Use together ........................ APPROVED AS CURRENT BASELINE
```

## Still pending separate confirmation

This report does **not** claim completion of:

- JOB-04 native **Sell Vehicle** runtime test;
- JOB-04 **Scrap Whole Vehicle** runtime test;
- duplicate-payment/removal behavior in live BeamNG runtime;
- strip/scrap shell, returned parts, sell part, catalytic-converter scrapping;
- auction export from JOB-04 to JOB-13.

No code or ZIP was changed for this result. This file records owner runtime evidence only.
