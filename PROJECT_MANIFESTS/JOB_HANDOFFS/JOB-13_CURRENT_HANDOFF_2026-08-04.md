# JOB-13 — FoxNet Online Vehicle Auctions

## Authoritative recovery handoff

**Updated:** 2026-08-04
**Branch:** `job13-online-auctions`
**Primary issue:** #40 `[JOB-13] CLAIMED — FoxNet Online Vehicle Auctions`

This file is the current authoritative handoff if the active ChatGPT conversation ends. Do not rename, merge, or move JOB-13 into another job.

---

## 1. Latest build awaiting runtime testing

**ZIP:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_0_BANK_RESERVE_SELLING_CRASH_RECOVERY.zip`

**SHA-256:** `58debecc1e7c2eb2257dcbb9d70e7c7265090063276159ebfa6129c10fbfefa0`

**Base build:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_3_STABLE_STATE_CAMERA_THUMBNAIL_RETAKE.zip`

**Base SHA-256:** `9c1789d5d8013d783cb2d14f0bc4fb48bd7319afa45d5df66531cb454499015a`

v0.1.9.0 passed static triple verification and a mocked Lua integration harness. It is **not BeamNG-runtime-proven** until the user tests this exact ZIP.

Do not claim the bank, seller, reserve, invoice, or crash-recovery systems are proven before that runtime test.

---

## 2. Runtime-proven architecture that must not regress

The user already proved:

- JOB-04 Wrecking Yard, JOB-09 Tow, and JOB-13 Auction remain separate ZIPs.
- The shared FoxNet Welcome Page routes to JOB-13's unique Auction path.
- PC and phone open the same JOB-13 Auction website.
- Auction bidding can behave competitively with NPC bidders.
- Different installed/modded vehicles appear.
- Auction purchases can enter Career inventory.
- Wrecking Yard purchases continue working beside JOB-13.
- Tow website is operational.

Known runtime-safe Wrecking Yard route base:

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`

Do not combine these jobs during development and do not alter JOB-04 or JOB-09 for the v0.1.9.0 test.

---

## 3. v0.1.9.0 feature scope

### 3.1 Bank-backed buying power

Buying power now includes:

`wallet cash + eligible personal RLS bank balance - committed active bids`

The implementation uses RLS personal bank accounts only. Settlement withdraws only the required deficit from the bank into the existing wallet/player-attribute payment path, then performs the normal charge. It must be tested for exact single deduction and no double charge.

### 3.2 Player-owned vehicle selling

A new JOB-13 seller/consignment system is available from the same Auction website on PC and phone.

Seller flow:

1. Select an exact owned Career inventory vehicle.
2. Set starting bid.
3. Set private reserve.
4. Submit the vehicle.
5. Vehicle is locked using the exact Career inventory ID.
6. Listing enters the next prepared auction group, never the auction currently running.

RLS currently supports one `listedForAuction` inventory lock at a time, so v0.1.9.0 allows one active personal consignment.

Default seller listing fee: `$150`.
Default seller commission: `6%`.

### 3.3 Reserve prices

- Reserve remains private from bidders.
- Below reserve at lot close: `Reserve Not Met` / no sale.
- No buyer transfer occurs.
- Seller receives no payout.
- Exact inventory vehicle is unlocked and returned.
- Seller fee/net/profit record for a no-sale is zero/undefined as appropriate.

At or above reserve:

- exact inventory vehicle is removed only after successful settlement;
- seller receives hammer price minus seller fee;
- sale record is written.

### 3.4 Purchase and sale records

New persistent ledger:

`settings/redfox/job13_online_auctions/auction_ledger_v1.json`

Records include purchased and sold/no-sale vehicles, lot information, hammer price, fees, total/net, delivery or sale status, Fox Facts/FoxFax, reserve result, and profit when original cost is known.

Records are intended to survive Auction page closure and Career restart.

### 3.5 Crash-safe freeze and resume

Schema version is now 9 while retaining the existing state path for migration from v8.

Recovery behavior:

- active auction snapshot is saved only when dirty;
- full snapshot interval is 30 seconds while an auction is active;
- no repeated state writes while idle;
- NPC bids mark state dirty but do not force an immediate full save;
- player bidding/cancellation does not write the full state on every click;
- critical lifecycle boundaries save immediately;
- on reload, active and upcoming lot times are shifted by downtime so the auction resumes rather than expiring while the game was closed;
- player bids, maximums, NPC bids, history, Fox Facts, membership, watchlist, consignments, and committed buying power are restored from the latest completed snapshot;
- a one-time recovery notice reports that the interrupted auction was restored.

A total PC crash can still lose events after the most recent completed snapshot. Target maximum normal loss window is approximately 30 seconds.

### 3.6 Tow Yard bridge contract

JOB-13 now exports a bridge contract for later JOB-09 integration under:

`redfox.auction.bridge.v1`

Important entry points include:

- `M.createListing(request)`
- `M.getSellRoute(inventoryId)`

JOB-09 was **not modified**. Do not connect Tow Yard `Send to Auction` until the standalone PC/phone seller flow passes runtime testing. The future handoff must pass the exact inventory/custody identifier and be idempotent.

### 3.7 Existing UI/state fixes preserved

The build preserves the v0.1.8.3 work intended to address:

- recurring green loaded-state bar;
- full catalog refresh overwriting detailed lots;
- disappearing Fox Facts and bid history;
- max-bid field resetting while typing;
- membership/watchlist persistence;
- working filters/dropdowns;
- clickable enlarged vehicle images;
- varied vehicle selection.

These still require regression testing in the exact v0.1.9.0 build.

Vehicle photo management remains owned by the Dev Manager job. JOB-13 should consume Career thumbnails rather than developing a competing full photo manager.

---

## 4. Save-frequency rules

Locked rules:

- Full state snapshot every 30 seconds only when the auction is active and dirty.
- No repeated state save while idle.
- Do not save the full catalog on every bid.
- Do not save the full state on every NPC bid.
- Critical events may force a save: lot close, purchase, sale, delivery, clean Career exit, or state transition.
- Recovery snapshot interval setting is clamped to 15–120 seconds.
- Preserve last-known-good state if a write fails.

Do not replace this with a high-frequency `onUpdate` write loop.

---

## 5. Triple-verification result

### Gate 1 — before editing

Passed:

- exact v0.1.8.3 source identified and hashed;
- 19 source files;
- ZIP integrity passed;
- zero duplicate or unsafe paths;
- JOB-04, JOB-09, and shared-route files protected.

### Gate 2 — after editing

Passed:

- 12 approved JOB-13 files changed;
- 7 source files remained byte-identical;
- JSON parsing passed;
- JavaScript syntax passed;
- Lua syntax passed;
- CSS and HTML structural checks passed;
- three route HTML copies are byte-identical;
- zero duplicate HTML IDs;
- no Wrecking Yard path overlap;
- no JOB-09 private files changed;
- no recurring full catalog reload;
- no full save on each player or NPC bid.

Mock harness passed:

- bank-funded membership and bidding;
- no immediate full save after a bid;
- exactly one dirty snapshot at 30 seconds;
- five-minute simulated outage restored the same bid and remaining time;
- bank-backed purchase produced exact inventory and invoice record;
- reserve-not-met returned the exact vehicle with no payout;
- successful seller lot removed exact inventory and paid net proceeds.

### Gate 3 — after ZIP creation

Passed:

- final ZIP integrity;
- 19 files;
- zero duplicate/unsafe paths;
- fresh extraction matched the edited tree byte-for-byte;
- JSON, JavaScript, Lua, and mock harness re-ran successfully from the fresh extraction.

Verification artifacts:

- `JOB-13_v0_1_9_0_PRE_EDIT_VERIFICATION.txt`
- `JOB-13_v0_1_9_0_AFTER_EDIT_VERIFICATION.md`
- `JOB-13_v0_1_9_0_TRIPLE_VERIFICATION_AUDIT.md`
- `JOB-13_v0_1_9_0_FILE_MANIFEST_SHA256.csv`
- `JOB-13_v0_1_9_0_TEST_CHECKLIST.txt`
- `JOB-13_v0_1_9_0_MOCK_RUNTIME_HARNESS.txt`

Static verification is not a substitute for BeamNG runtime testing.

---

## 6. Exact next runtime test plan

Install only v0.1.9.0 for JOB-13. Disable all older JOB-13 ZIPs. Keep the currently working JOB-04 and JOB-09 ZIPs unchanged. Restart BeamNG completely.

Test in this order:

1. Open Auction from PC and phone; confirm same active group and normal speed.
2. Confirm varied vehicles, no recurring green bar, stable details, working dropdowns, membership, watchlist, and max-bid field.
3. Put most money in a personal RLS bank account and leave little wallet cash.
4. Place a bid and verify displayed buying power includes bank funds.
5. Win one inexpensive vehicle and verify one exact deduction, delivery, and purchase record.
6. Place bids on two lots, wait at least 35 seconds, close BeamNG normally, reopen Career, and confirm the same auction, bids, max bids, history, and remaining times restore.
7. Only after normal-close recovery passes, test an unexpected termination/crash recovery.
8. Submit one owned vehicle with a high reserve; verify it enters the next group, fails reserve, returns the exact vehicle, and records no payout.
9. Submit one owned vehicle with a reachable reserve; verify exact vehicle removal, seller payout after fee, and sale/profit record.
10. Verify Wrecking Yard and Tow still open and operate normally.

Stop testing immediately if any vehicle duplicates/disappears, money is charged twice, the phone/PC locks, or Career state becomes stuck.

Do not test Tow Yard `Send to Auction` yet; first prove the standalone seller backend.

---

## 7. Protected project rules

- Never claim runtime success before exact-ZIP user testing.
- Keep JOB-04, JOB-09, and JOB-13 separate.
- Do not edit shared FoxNet/browser files without explicit permission.
- Preserve the working purchase/delivery route.
- Do not scan the full vehicle catalog at Career startup or page open.
- Do not rebuild full webpage state every second.
- Do not spam save files.
- Use exact Career inventory IDs for seller custody and settlement.
- Never create a permanent duplicate vehicle.
- Keep a current GitHub build record and issue update for every test ZIP.
