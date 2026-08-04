# JOB-13 — FoxNet Online Vehicle Auctions

## Current recovery handoff

**Updated:** 2026-08-04
**Branch:** `job13-online-auctions`
**Primary issue:** #40 `[JOB-13] CLAIMED — FoxNet Online Vehicle Auctions`

This file is the current authoritative handoff for JOB-13 if the active ChatGPT conversation ends. Do not rename, merge, or move JOB-13 into another job.

---

## 1. Current working integration

The following architecture has been runtime-proven by the user:

- JOB-04 Wrecking Yard remains a separate ZIP.
- JOB-13 Auction remains a separate ZIP.
- The shared FoxNet Welcome Page routes to JOB-13's unique Auction website path.
- The PC and phone both open the same JOB-13 Auction website.
- Auction purchases can deliver real vehicles into Career inventory.
- Wrecking Yard purchases also continue working.
- The old Lemon Zest / native dealership page no longer replaces JOB-13 when the corrected route package is used.

Known route pair used during successful testing:

- `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`
- JOB-13 unique-route builds based on v0.1.8.x

The newer Wrecking Yard v0.3.2.4.1 route build also exists, but the older v0.3.2.3.1 base was the user-confirmed runtime-safe choice.

**Do not combine JOB-04 and JOB-13 during development.**

---

## 2. Latest JOB-13 test build known in this conversation

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_3_STABLE_STATE_CAMERA_THUMBNAIL_RETAKE.zip`

SHA-256:

`9c1789d5d8013d783cb2d14f0bc4fb48bd7319afa45d5df66531cb454499015a`

This build was packaged and statically triple-verified, but not every intended runtime fix has been conclusively proven by the user. Do not treat all v0.1.8.3 fixes as runtime-confirmed.

The user later paused JOB-13 work while JOB-09 Tow was brought online. The user has now confirmed the Tow site is working and authorized continuation of JOB-13.

---

## 3. Runtime-proven JOB-13 behavior

Proven by user testing:

- PC Auction page opens.
- Phone Auction page opens.
- Auction bidding behaves competitively with NPC bidders.
- The user can be repeatedly outbid and bid the price upward like a real auction.
- Different installed/modded vehicles can appear in the auction pool.
- Real Auction purchases can enter Career inventory.
- Purchased vehicle thumbnails can be generated, though framing can be bad if the camera/player is near a wall.
- Wrecking Yard and Auction can coexist and buy vehicles in the same Career save.

Do not regress these items.

---

## 4. Known defects and unfinished behavior

### 4.1 Buying power ignores bank balance

When the user deposited all wallet cash into the RLS bank, JOB-13 displayed:

`Not enough available buying power`

Current buying power appears to use wallet cash only.

Required behavior:

`available buying power = wallet cash + bank balance - active committed bids`

Settlement must use verified RLS banking APIs and must not double-charge. Preferred deduction order is wallet first, bank second for the remainder, unless the native banking system has a safer authoritative transaction function.

### 4.2 Selling is not implemented

The next patch must add a seller/consignment system.

There must be one JOB-13 Sell Vehicle backend reachable from:

1. FoxNet Auction on PC.
2. FoxNet Auction on phone.
3. JOB-09 Tow Yard `Send to Auction` action.

The Tow Yard must not implement separate auction logic. It must pass the exact vehicle/custody identifier to JOB-13 and open JOB-13's seller page.

### 4.3 Reserve price required

The seller must be able to set a reserve price.

- If highest bid is below reserve at closing: vehicle does not sell.
- Result should show `Reserve Not Met` / `No Sale`.
- Seller should be offered return or relist.
- No seller payout and no buyer transfer occurs below reserve.
- Reserve value should not be disclosed to bidders unless the design explicitly chooses to show only `Reserve Met` / `Reserve Not Met`.

### 4.4 Seller custody and duplication safety

When a vehicle is submitted:

- It must be tied to the exact Career inventory ID or exact Tow Yard custody ID.
- It must be locked from driving, selling elsewhere, scrapping, or duplicate submission.
- It should enter the **next prepared auction group**, not an auction already in progress.
- If sold, transfer ownership and pay the seller after fees.
- If reserve is not met or there are no bids, safely return or relist it.
- Never create a duplicate permanent vehicle.

### 4.5 Purchase/sale history and invoices

Add permanent Auction account records:

- `Purchased Vehicles`
- `Sold Vehicles`
- optional combined `Invoices / Transactions`

Purchase record should preserve:

- lot number
- vehicle/model/config
- image
- hammer price
- buyer fee
- shipping
- total paid
- delivery status
- exact Fox Facts / FoxFax text shown during bidding

Sale record should preserve:

- lot number
- vehicle/model/config
- reserve
- highest bid
- sale/no-sale result
- seller fee
- payout
- original purchase cost when known
- profit/loss when calculable

Records must be written before any native delivery/menu transition closes the Auction page.

### 4.6 Crash-safe freeze and resume

The user's PC crashed while bidding on three vehicles. Future JOB-13 must restore interrupted auctions.

Restore:

- same active lots
- remaining times
- player bids
- confidential maximum bids
- NPC bids
- bid history
- Fox Facts and condition
- committed buying power
- membership/watchlist/seller consignments

On next Career load, show a one-time `Interrupted auction restored` message.

#### Save-frequency requirement

Do **not** spam the save system.

Locked design:

- full atomic auction snapshot every **30 seconds** only while an auction is active and dirty;
- no repeating saves while idle;
- NPC bids mark state dirty and wait for the next snapshot;
- player bids/cancellations use a small coalesced delayed save, not repeated full writes;
- immediate save only for critical boundaries: clean Career exit, lot close, purchase, sale, delivery, or auction-state transition;
- catalog cache must not be rewritten with every auction snapshot;
- use temporary/staging file plus atomic replacement and preserve last-known-good snapshot on failure.

A total hard crash may lose events after the latest completed snapshot. Target normal loss window is at most about 30 seconds, while preserving the player's most recent bid through a lightweight coalesced action save when practical.

### 4.7 Prior UI/state defects to preserve/fix carefully

Earlier runtime reports included:

- recurring green `Loaded 10 preapproved auction lots...` bar;
- full refresh replacing detailed lots with summary-only copies;
- Fox Facts and bid history disappearing;
- max-bid input resetting during typing;
- membership not persisting;
- watchlist not persisting;
- filters/dropdowns not working;
- old starter pool repeating only Covet/Hopper/Wendover.

The broader varied catalog later worked. Preserve that improvement.

Before claiming the prior state-reset fixes are complete, re-test them in the next patch.

---

## 5. Vehicle photo ownership decision

A permanent general-purpose vehicle photo tool has been delegated to the Dev Manager job.

Required Dev Manager concept:

- select exact Career inventory vehicle;
- position normal BeamNG camera, including Shift+C free camera;
- press `Take Vehicle Picture`;
- hide UI for capture;
- save image to that exact inventory ID;
- refresh garage/Auction consumers.

JOB-13 should read the resulting Career thumbnail. Do not build a second competing full photo-management system in JOB-13.

The temporary JOB-13 camera-retake code in v0.1.8.3 may remain only if harmless, but future ownership belongs to Dev Manager.

---

## 6. Tow integration status

The user has confirmed the Tow website is now working.

Future JOB-09 integration is only for `Send to Auction`:

- JOB-09 passes exact Tow Yard custody/vehicle ID and source metadata.
- JOB-13 opens the same seller form used by PC and phone.
- JOB-13 owns reserve, consignment, auction insertion, sale settlement, history, and payout.
- Do not modify JOB-09 until JOB-13's seller API/contract is implemented and documented.

Provide the Tow chat with the exact message/action name, payload schema, success response, failure response, and retry/idempotency behavior after the seller backend exists.

---

## 7. Next patch scope

The next JOB-13 patch must be JOB-13-only unless an explicit, documented integration change is genuinely required.

Priority order:

1. Preserve current working PC/phone route and vehicle purchase/delivery.
2. Add bank-backed buying power safely.
3. Add crash-safe 30-second snapshot/resume system.
4. Add seller/consignment UI and backend for owned Career vehicles.
5. Add reserve-price behavior.
6. Add purchased/sold/invoice records.
7. Define Tow Yard `Send to Auction` API, but do not alter JOB-09 yet.
8. Re-test prior state persistence, max bid, watchlist, membership, green bar, filters, and detail stability.

Do not combine unrelated large refactors into this patch.

---

## 8. Required verification process

The user requires triple verification:

### Gate 1 — before editing

- inventory source tree and hashes;
- verify exact base build;
- identify approved file scope;
- record protected JOB-04/JOB-09/shared files;
- confirm no duplicate ZIP paths.

### Gate 2 — after editing

- exact changed-file diff;
- Lua/JS/JSON syntax checks;
- state/schema migration review;
- route and bridge checks for PC and phone;
- prove no protected files changed;
- static tests for reserve, bank, seller lock, history, and recovery paths.

### Gate 3 — after ZIP creation

- fresh extraction;
- rehash every file against edited tree;
- duplicate/unsafe path check;
- verify package contains only intended JOB-13 files;
- produce SHA-256 and test checklist.

Do not claim runtime success until the user tests the exact ZIP.

---

## 9. Next runtime test plan

No new patch is currently available from the latest scope discussion. The user should not be told to test crash recovery, bank-backed buying power, selling, reserve, Tow handoff, or invoice history until a new ZIP is actually built.

When the next patch is delivered, test in this order:

1. Open Auction from PC and phone.
2. Confirm existing active auction restores after a controlled Career restart.
3. Place a bid, wait at least 30 seconds, restart Career, confirm bid/max/history restore.
4. Deposit wallet money into bank and confirm buying power includes it.
5. Win one inexpensive vehicle and confirm wallet/bank deduction is exact and single.
6. Submit one owned vehicle from PC/phone with a reserve.
7. Confirm it enters the next auction, not the current one.
8. Test reserve-not-met and successful-sale outcomes.
9. Confirm purchase and sale records persist after restart.
10. After JOB-13 seller API is proven, test one Tow Yard `Send to Auction` handoff.

---

## 10. Safety and process rules

- Never claim a runtime fix is proven before exact-ZIP testing.
- Keep JOB-04, JOB-09, and JOB-13 separate.
- Do not edit shared FoxNet/browser files without explicit permission.
- Do not replace working purchase/delivery code casually.
- No high-frequency save loop.
- No full catalog scan at Career startup or phone/page open.
- No full state rebuild every second.
- Preserve last-known-good catalog and auction snapshot.
- Be direct and honest about what is untested.
