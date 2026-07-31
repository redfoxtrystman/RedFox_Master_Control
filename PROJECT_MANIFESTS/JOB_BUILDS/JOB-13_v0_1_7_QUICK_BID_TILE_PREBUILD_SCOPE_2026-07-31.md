# JOB-13 v0.1.7 — Quick Bid, Upcoming Auction and Phone Notification Pre-build Scope

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Source: RedFox_JOB13_FoxNet_Online_Auctions_v0_1_6_NATIVE_BIDDING_GARAGE_DELIVERY.zip

## Owner requests

1. Add a Quick Bid button directly to each active auction vehicle tile so the player can watch and bid on multiple auctions without opening every lot detail page.
2. Add a way to preview the next auction's items and scheduled start so the player can plan.
3. Fire phone notifications when the next auction is getting close to starting.

## Locked implementation scope

### Quick Bid

- Reuse the existing JOB-13 `place_bid` backend action.
- Quick Bid always uses the backend-calculated current next valid bid.
- Keep the existing watchlist control on each active tile.
- Stop click propagation so Quick Bid and Watch do not open the lot modal.
- Refresh the cached catalog after the action so all tiles show updated leaders/prices.
- Show Quick Bid only while a lot is active.

### Upcoming Auction

- Generate the next auction's preview once in Lua and persist it with the auction state.
- Do not scan dealerships, installed vehicles or configuration lists when the Upcoming tab opens.
- Show upcoming lot cards, expected opening bids, condition, scheduled start and countdown.
- Upcoming cards are planning-only: no bidding before the scheduled start.
- When the next auction starts, promote the already-prepared lots instead of rebuilding them in the browser.
- Prepare a new following-auction preview after promotion.

### Phone notifications

- Use the existing RLS phone dispatcher `ui_phone_layout.fireNotification`.
- Use namespaced notification channels so the phone's Notifications settings can mute JOB-13 independently.
- Provide a configurable pre-start notification threshold in WEUI.
- Fire each scheduled notification once and persist the sent state to prevent repeated alerts after reload.
- Use `toastrMsg` only as a fallback when the phone notification dispatcher is unavailable.
- Do not create a second notification framework.

### Preserved behavior and boundaries

- Do not add a second bid ledger, NPC engine, settlement path, wallet, invoice, ownership, shipping or garage system.
- Do not change the v0.1.6 native Career/RLS purchase and garage-delivery path.
- Do not expand the vehicle/prop pool in this build; purchase proof remains the current gate.
- Do not edit Wrecking Yard, Tow/Recovery, BeamBook, Welcome/Home or any other website.

## Verification gate

Before packaging:

1. JavaScript syntax pass.
2. Lua syntax pass.
3. Quick Bid maps only to `place_bid` with the selected lot ID.
4. Watch maps only to `toggle_watch`.
5. Card background still opens lot details.
6. Closed and upcoming lots have no Quick Bid control.
7. Upcoming tab reads only the cached/persisted preview.
8. Promotion reuses the prepared upcoming lots.
9. Phone notification routes through `ui_phone_layout.fireNotification` with a namespaced channel.
10. A notification threshold fires once, not once per update tick.
11. v0.1.6 native purchase/delivery calls remain unchanged.
12. ZIP contains no shared core UI or unrelated site files.
13. Exact file manifest and source diff generated.

Runtime remains unproven until David tests the exact output ZIP in BeamNG.