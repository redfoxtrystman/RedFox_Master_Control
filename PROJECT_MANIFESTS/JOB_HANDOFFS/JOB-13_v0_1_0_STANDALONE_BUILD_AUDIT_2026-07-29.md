# JOB-13 v0.1.0 Standalone Build Audit

**Date/time:** 2026-07-29 17:51–18:10 Pacific  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Owner:** David / Captain  
**Build:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_0_STANDALONE.zip`  
**SHA-256:** `cc972c6a92b9754d315669fce8f8b394967646dd86087edd880adda5264c31a2`  
**Status:** Static verification passed; BeamNG runtime testing required.

## Why this build exists

David authorized JOB-13 to begin as a standalone BeamNG mod so online-auction development can continue without editing or replacing websites and shared files owned by other jobs. The standalone package is intended to be merged into the combined FoxNet package later through the JOB-01/shared-browser owner.

## Files and namespaces added

```text
lua/ge/extensions/redfoxJob13Auction.lua
lua/ge/extensions/redfoxJob13AuctionSettings.lua
scripts/redfox_job13_online_auctions/modScript.lua
ui/modules/apps/redfoxJob13Auctions_v010/
mod_info/RedFoxJOB13/
docs/
```

Isolated namespaces:

```text
extensions.redfoxJob13Auction
extensions.redfoxJob13AuctionSettings
redfoxJob13AuctionsV010
settings/redfox/job13_online_auctions/
```

## Completed features

- Standalone BeamNG UI App for FoxNet Online Auctions.
- Online-only auction flow; no physical auction lane, yard intake, preview trip or pickup.
- Multiple timed vehicle lots active simultaneously.
- Staggered closing times.
- Separate timer, bid state and bid history for each lot.
- Watchlist and multiple simultaneous player bids.
- Confidential maximum/proxy bidding.
- Player bid cancellation before the lot timer reaches zero.
- NPC bidders, no-bid lots and No Sale results.
- No positive reserves.
- Controlled relisting.
- Membership plans, buying-power limits, active-bid limits, buyer fees and shipping discounts.
- TEST invoices and simulated In Transit shipping.
- Fox Facts, mileage, damage, missing parts and start/drive status.
- One previous-auction results archive.
- Persistent settings and TEST state.
- WEUI fine-tuning interface for timing, lot count, NPC behavior, fees, memberships, shipping, relisting and safety mode.
- 21 real supplied BeamNG screenshots used as listing images; no AI or unrelated stock vehicle art.

## Safety modes

```text
PREVIEW — read-only bidding/transaction safety mode.
TEST    — persistent simulated balance, bidding, invoices and shipping.
LIVE    — intentionally locked until JOB-02/Career/RLS integration exists.
```

## Files deliberately not changed

- JOB-01 phone/PC/IceFox host files.
- JOB-02 Career/RLS bridge and stock Career files.
- JOB-04 Wrecking Yard files and records.
- JOB-05 BeamBook.
- JOB-07 Collector Exchange.
- JOB-09 Tow/Recovery files and yard JSON.
- JOB-10 combined websites package.
- FoxFax, Wrecking Yard, BeamBook or other website source files.

## Verification performed

- JavaScript syntax: PASS (`node --check`).
- JSON syntax: PASS.
- Lua parse-only validation: PASS (`texluac -p`).
- Standalone Lua behavior harness: PASS.
- Required listing-image validation: PASS, 21 of 21 files present.
- ZIP integrity: PASS.

## Known limitations

- No BeamNG runtime test has been completed yet.
- LIVE Career money, inventory, ownership and garage delivery are not connected.
- JOB-04 and JOB-09 candidate/export adapters remain future integration work.
- Exact damaged-vehicle renders are not generated dynamically; this build uses real supplied BeamNG screenshots.
- NPC budgets are currently independent per lot; shared NPC exposure across simultaneous lots remains a later engine pass.
- The standalone UI App is not yet registered in the shared IceFox/FoxNet browser.

## Required next steps

1. Install and enable the standalone ZIP.
2. Add the `FoxNet Online Auctions — JOB-13` UI App.
3. Open WEUI Settings and switch from PREVIEW to TEST.
4. Test multiple simultaneous bids, bid cancellation, NPC bids, staggered closing, no-sale, relisting, invoice payment, shipping and previous results.
5. Record BeamNG runtime logs and screenshots in JOB-13 issue #40.
6. Do not begin LIVE integration until standalone TEST behavior is accepted.

## Migration/context note

JOB-13 was created after the earlier project Work chats became inaccessible due to the separate Work-chat usage limit. This standalone checkpoint preserves the rebuilt context and avoids additional cross-job file conflicts while the project continues in regular chats.
