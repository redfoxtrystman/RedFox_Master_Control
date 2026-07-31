# JOB-13 v0.1.7 — Quick Bid Tile Pre-build Scope

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Source: RedFox_JOB13_FoxNet_Online_Auctions_v0_1_6_NATIVE_BIDDING_GARAGE_DELIVERY.zip

## Owner request

Add a Quick Bid button directly to each active auction vehicle tile so the player can watch and bid on multiple auctions without opening every lot detail page.

## Locked implementation scope

- Reuse the existing JOB-13 `place_bid` backend action.
- Quick Bid always uses the backend-calculated current next valid bid.
- Keep the existing watchlist star on each tile.
- Stop click propagation so Quick Bid and Watch do not open the lot modal.
- Refresh the cached catalog after the action so all tiles show updated leaders/prices.
- Show Quick Bid only while a lot is active.
- Do not add a second bid ledger, second NPC engine, or second settlement path.
- Do not change native Career/RLS purchase or garage delivery behavior.
- Do not expand the vehicle/prop pool in this build.
- Do not edit Wrecking Yard, Tow/Recovery, BeamBook, Welcome/Home, or any other website.

## Verification gate

Before packaging:

1. JavaScript syntax pass.
2. Lua syntax pass.
3. Quick Bid click maps only to `place_bid` with the selected lot ID.
4. Watch click maps only to `toggle_watch`.
5. Card background still opens lot details.
6. Closed lots have no Quick Bid control.
7. v0.1.6 native purchase/delivery calls remain unchanged.
8. ZIP contains no shared core UI or unrelated site files.
9. Exact file manifest and source diff generated.

Runtime remains unproven until David tests the exact output ZIP in BeamNG.