# JOB-13 — FoxNet Online Vehicle Auctions

## Authoritative recovery handoff

**Updated:** 2026-08-05
**Branch:** `job13-online-auctions`
**Primary issue:** #40 `[JOB-13] CLAIMED — FoxNet Online Vehicle Auctions`

This is the current authoritative handoff if the active ChatGPT conversation ends. Do not rename, merge, or move JOB-13 into another job.

---

## 1. Latest build awaiting runtime testing

**ZIP:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_4_SINGLE_STATE_PAYMENT_RECOVERY.zip`

**SHA-256:** `285b741b26f30e7eb00011f695e035394d5b65af346249599f2f66251f8ccd12`

**Base:** v0.1.9.3, SHA-256 `c132416b2f654cdce7483a83bf44b7eddccb1e5a0b03784a93990a47a97a342c`

v0.1.9.4 passed all three static verification gates and fresh-extraction verification. It is **not BeamNG-runtime-proven** until the user tests the exact ZIP.

### Important reset decision

v0.1.9.4 uses a new `auction_state_v0194.json` and intentionally does not import v0.1.9.3 active lots, timers, bids, or prepared auctions because v0.1.9.1–v0.1.9.3 could produce cloned/split timelines. Account profile, purchase/sale ledger, and active seller consignments remain separate and may be preserved.

---

## 2. Runtime-proven architecture that must not regress

The user has proved:

- JOB-04 Wrecking Yard, JOB-09 Tow, and JOB-13 Auction remain separate ZIPs.
- The shared FoxNet Welcome Page routes to JOB-13's unique Auction path.
- PC and phone can open the same JOB-13 website.
- Auction purchases can enter Career inventory.
- Wrecking Yard purchases continue working beside JOB-13.
- Tow website is operational.
- Different installed/modded vehicles appear.
- Player consignments, starting bids, and private reserves can be created.
- Bank-backed buying power appeared functional in prior testing.

Known runtime-safe Wrecking Yard route base:

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`

Do not combine the jobs and do not modify JOB-04 or JOB-09 while testing v0.1.9.4.

---

## 3. Why v0.1.9.1–v0.1.9.3 were rejected

User testing showed:

- almost every Auction webpage reload could change timers or show a different timeline;
- lots could restart near 30 minutes, jump forward, or appear already sold;
- PC/phone were not the root cause—the reload itself was enough;
- recurring Lua bridge disconnect warnings appeared;
- old auctions could be loaded as new clones while a new auction was also generated;
- the next auction sometimes did not auto-start;
- unresolved wins could be difficult to pay;
- repeated completion clicks duplicated a won vehicle;
- some purchased records existed without the vehicle being accessible;
- v0.1.9.1 recovery was unsafe and testing was stopped.

Do not tell the user to test v0.1.9.1, v0.1.9.2, or v0.1.9.3 again.

---

## 4. v0.1.9.4 single-state architecture

The user explicitly warned against multiple or redundant save-state systems. v0.1.9.4 therefore enforces:

- exactly one Lua table owns current auction, prepared next auction, bids, timers, consignments, pending wins, and settlement markers;
- exactly one Lua function writes active auction state;
- exactly one code path writes the active auction state file;
- exactly one low-level clock restore implementation;
- every restore request passes through one guarded recovery gate;
- repeated Career activation callbacks use `pauseGeneration` / `resumeGeneration` and cannot restore the same freeze twice;
- re-entrant save requests are coalesced through the same writer;
- extension unload, webpage reload, PC/phone switching, and bridge reconnect do not save, pause, restore, reroll, rotate, or generate auctions;
- process-memory reconnect returns the existing live state only;
- disk recovery occurs only through Career lifecycle startup/reactivation.

Separate account-profile and transaction-ledger files are retained, but they do not own or modify active lots, bids, timers, or prepared auction contents.

### Save policy

- current and next auction snapshot at start/critical transitions;
- 30-second freeze snapshot while an auction is active;
- no full state write on every NPC bid;
- no page-reload save;
- immediate save for seller consignment, delivery claim, lot transition, purchase/sale settlement, and Career lifecycle boundaries;
- last written snapshot is read back and serial-verified.

---

## 5. Payment Pending and duplication recovery

v0.1.9.4 adds payment controls to both:

- `Bought Vehicles`
- `Invoices`

Both call the same idempotent Lua action.

Behavior:

- a saved purchase invoice can reconstruct a missing pending lot;
- if no Career vehicle exists, one saved delivery claim must verify before spawn;
- if a vehicle already exists with `job13AuctionPendingKey`, JOB-13 finalizes payment on that exact inventory vehicle and does not spawn another;
- `job13AuctionDeliveryKey`, `completedDeliveryKeys`, and `deliveryClaims` block duplicate delivery;
- payment gets its own saved `charging` lock before money is deducted;
- if a crash occurs while payment completion is uncertain, JOB-13 stops with verification required rather than charging or spawning again;
- repeated Pay/Complete clicks share one browser action lock and one Lua settlement path.

Existing duplicates created by old builds are not automatically deleted.

---

## 6. Retained feature scope

v0.1.9.4 retains:

- automatic next-auction transition after a one-minute intermission;
- unresolved wins under My Bids/pending purchases;
- next-auction reminder;
- explicit Add/Remove Watchlist button in vehicle details;
- player consignments saved immediately and placed in early available prepared slots;
- multiple consignments;
- private reserve prices;
- current RLS value/suggested seller pricing from v0.1.9.1;
- calmer NPC settings;
- custom BeamNG-safe dropdown menus;
- wallet plus eligible personal-bank buying power;
- purchase/sale/no-sale records;
- PC iframe/page scrolling;
- current/next vehicle groups protected from webpage rerolling.

JOB-09 `Send to Auction` is not connected yet. JOB-13 must first pass standalone seller/runtime tests.

Vehicle-photo management remains owned by Dev Manager. JOB-13 consumes Career thumbnails.

---

## 7. Triple verification result

### Gate 1 — before editing

PASS:

- exact v0.1.9.3 base and SHA verified;
- ZIP integrity passed;
- 19 files;
- zero duplicate/unsafe paths;
- JOB-04, JOB-09, and shared FoxNet protected;
- scope locked before editing.

### Gate 2 — after editing

PASS:

- 11 approved JOB-13 files changed;
- no files added/removed;
- all JSON parsed;
- all JavaScript passed `node --check`;
- all Lua parsed through Lua 5.4;
- three Auction route HTML copies are byte-identical;
- zero duplicate HTML IDs;
- one state writer/write path and one recovery gate verified;
- webpage/bridge reload is display-only;
- delivery/payment locks save before spawn/charge;
- Bought/Invoices share one payment action;
- unsafe v0.1.9.3 active lots are not migrated.

### Gate 3 — after ZIP creation

PASS:

- ZIP integrity/CRC;
- 19 files;
- zero duplicate/unsafe paths;
- fresh extraction matched edited source byte-for-byte;
- all syntax and structural checks reran successfully;
- final SHA-256 manifest generated.

Artifacts:

- `JOB-13_v0_1_9_4_PRE_EDIT_VERIFICATION.txt`
- `JOB-13_v0_1_9_4_AFTER_EDIT_VERIFICATION.md`
- `JOB-13_v0_1_9_4_STATIC_VERIFICATION.txt`
- `JOB-13_v0_1_9_4_POST_ZIP_VERIFICATION.txt`
- `JOB-13_v0_1_9_4_TRIPLE_VERIFICATION_AUDIT.md`
- `JOB-13_v0_1_9_4_FILE_MANIFEST_SHA256.csv`
- `JOB-13_v0_1_9_4_TEST_CHECKLIST.txt`
- `JOB-13_v0_1_9_3_to_v0_1_9_4_FINAL.diff`

Static verification is not runtime proof.

---

## 8. Exact next runtime test order

Install only v0.1.9.4 for JOB-13. Disable all older JOB-13 ZIPs. Keep current JOB-04 and JOB-09 ZIPs unchanged. Fully restart BeamNG.

### Test 1 — reload consistency first

1. Open Auction and record auction number, three lots, bids, and timers.
2. Reload/open the page at least five times on the same device.
3. Switch PC/phone twice.
4. Confirm the same auction continues without restarting, jumping, selling, or cloning.

If this fails, stop immediately.

### Test 2 — recovery

1. Place one bid and confidential maximum.
2. Wait at least 35 seconds.
3. close BeamNG normally and reload the same Career save.
4. Confirm one restored timeline with the same bid and approximately saved remaining time.

### Test 3 — auto next

Let the auction finish or use the developer finish control once. Confirm the prepared next auction starts automatically after the intermission.

### Test 4 — pending payment

Use Bought Vehicles or Invoices to pay one Payment Pending purchase. Confirm one charge and one vehicle. Clicking again after refresh must report already delivered/in progress and must not duplicate or charge twice.

### Test 5 — watch/reminder/scroll/seller priority

Confirm Add to Watchlist, next-auction reminder, full PC scrolling, and early prepared placement of one test consignment.

Stop immediately if money charges twice, a vehicle duplicates/disappears, page reload changes state, or the bridge repeatedly disconnects.

---

## 9. Protected rules

- Never claim runtime success before exact-ZIP user testing.
- Keep JOB-04, JOB-09, and JOB-13 separate.
- Do not edit shared FoxNet/browser files without permission.
- Do not add a second auction-state writer or recovery system.
- Do not restore auction state from webpage/bridge load.
- Do not scan the full catalog at Career startup/page open.
- Use exact Career inventory IDs and stable delivery keys.
- Never knowingly charge or deliver twice.
- Keep GitHub handoff and issue #40 current after every test.
