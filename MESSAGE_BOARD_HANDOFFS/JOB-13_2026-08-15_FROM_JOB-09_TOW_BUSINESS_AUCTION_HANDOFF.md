# JOB-13 Handoff from JOB-09 — Tow Business / Custody Auction Flow

Date: 2026-08-15
From: JOB-09 — RedFox Tow & Recovery Dispatch
To: JOB-13 — FoxNet Online Auctions
Priority: High before JOB-09 Auction action is re-enabled

## Required correction

Tow Company must NOT create its own internal countdown auction, reserve, or auto-selected sale value.

`Send to FoxNet Online Auction` must open JOB-13's real Sell Vehicle / consignment workflow so the player controls the reserve and listing choices.

## Required external-consignment contract

JOB-13 should be able to accept a Tow business/custody asset without forcing permanent conversion into the player's personal Career garage.

Minimum identity payload:

- RedFox Tow record ID
- RLS business ID, when present
- RLS business vehicle ID, when present
- RedFox yard ID
- RedFox yard storage key
- vehicle model/config snapshot
- mileage/condition/value snapshot
- thumbnail/image reference when available

## State ownership

1. JOB-09 owns the Tow/custody record before listing.
2. JOB-13 owns listing/bids/reserve/timing while the consignment is active.
3. JOB-09 marks the source asset `auction_locked` so it cannot simultaneously be scrapped, sold elsewhere, transferred, or duplicated.
4. If sold, JOB-13 reports exact completion and proceeds to JOB-09, then JOB-09 releases/removes the source asset exactly once.
5. If no-sale/cancelled, JOB-13 returns the exact same asset identity to the original Tow yard/storage state.
6. Once RedFox Tow becomes a formal RLS business, auction proceeds should go to the Tow/RLS business account rather than a fake JOB-09 wallet.

## Native RLS auction distinction

RLS 2.7.0.1 includes a native used-car auction/consignment system, but the preserved source audit indicates its normal listing path expects Career inventory identity. That is appropriate for personally owned Career vehicles but should not be used as a reason to convert RedFox Tow business-storage assets into personal inventory.

FoxNet remains the intended online-auction path for Tow Company business/custody vehicles.

## JOB-09 status

JOB-09 v0.5.0.23/v0.5.0.24 keeps Auction disabled for the new business-storage lifecycle until JOB-13 has this handoff. Do not reintroduce the old fake internal Tow auction.
