# JOB-13 — FoxNet Online Vehicle Auctions

## Authoritative recovery handoff

**Updated:** 2026-08-07
**Branch:** `job13-online-auctions`
**Primary issue:** #40 `[JOB-13] CLAIMED — FoxNet Online Vehicle Auctions`

This is the current authoritative handoff if the active ChatGPT conversation ends. Do not rename, merge, or move JOB-13 into another job.

---

## 1. Latest build awaiting runtime testing

**ZIP:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_5_SAVE_ISOLATION_SINGLE_OWNER.zip`

**SHA-256:** `e003c68eff2ef276685ec8794e2efde6e9d227e9ecfe7dfaf768fc730995eb90`

**Base:** v0.1.9.4, SHA-256 `285b741b26f30e7eb00011f695e035394d5b65af346249599f2f66251f8ccd12`

v0.1.9.5 passed static/fresh-extraction verification. It is **not BeamNG-runtime-proven** until the user tests the exact ZIP across at least two Career saves.

---

## 2. Why v0.1.9.5 exists

Runtime testing of v0.1.9.4 found that a brand-new Career save could show Bought Vehicles / delivery records from another save. The live auction state itself appeared save-specific, but transaction history crossed saves.

Exact cause: `ledgerOps.loadLedger()` still fell back to the old global `settings/redfox/job13_online_auctions/auction_ledger_v1.json` when a new save had no local ledger. The account loader had the same legacy-global fallback risk for membership/watchlist/reminder data.

The user explicitly requested that every JOB-13 part save to the correct Career save and that redundant save-state ownership be removed.

---

## 3. v0.1.9.5 persistence ownership

Career progress now has exactly three per-save persistent domains:

1. **Auction state** — `<save>/career/rls_career/redfox_job13/auction_state_v0194.json`
   - current auction
   - prepared next/future auctions
   - bids/timers
   - seller consignments
   - pending purchase workflow
   - settlement/idempotency keys

2. **Account profile** — `<save>/career/rls_career/redfox_job13/account_profile_v2.json`
   - membership
   - saved searches
   - watchlist
   - next-auction reminder

3. **Transaction ledger** — `<save>/career/rls_career/redfox_job13/auction_ledger_v2.json`
   - Bought Vehicles
   - Sold Vehicles
   - invoices
   - payment/delivery/sale status

The auction snapshot no longer persists `state.account`; `account_profile_v2.json` is the sole persistent owner of account progress.

Ledger and account files are stamped with `careerSavePath`. A file stamped for another save is rejected.

The auction snapshot also validates its saved Career path when present.

---

## 4. Global files allowed

The only intentionally global JOB-13 persistence is non-Career data:

- `settings/redfox/job13_online_auctions/settings_v018.json` — user tuning/preferences.
- installed vehicle/prop catalog cache — installed-content discovery.

These must not contain Career money, bids, wins, consignments, invoices, membership, watchlists, reminders, or transaction history.

Old global JOB-13 account and ledger files are no longer imported into new Career saves.

---

## 5. Additional cross-save protections

- Async purchase/delivery runtime maps are cleared when switching Career save slots so reused inventory IDs cannot leak between saves.
- Purchase records now retain `deliveryKey` for durable reconciliation.
- JOB-04 Wrecking Yard acquisition history is global in older builds. JOB-13 now accepts it only if JOB-04 provides a matching Career-save stamp; inventory ID alone is not trusted across saves.
- Per-save older JOB-13 seller listings may still migrate from older JOB-13 state files in the **same Career save only**.

JOB-04 and JOB-09 were not modified.

---

## 6. Existing runtime defects still under investigation

Do not consider these fixed unless the user proves them in v0.1.9.5:

- auction reload/recovery consistency has been hit-and-miss in prior builds;
- old purchase records can show stale Shipping/Payment Pending status after Career already received the vehicle;
- paying an old invoice previously froze the UI temporarily;
- old auction lots could reappear with timers;
- one truck showed No Sale even though Career received it;
- watchlist catalog search is incomplete;
- recurring bridge errors have occurred.

Do not auto-delete old duplicates created by previous unsafe builds.

---

## 7. Save-frequency and safety rules

- One Lua table owns live auction state.
- One function writes auction state.
- One guarded recovery path restores auction state.
- Page reload, PC/phone switching, and bridge reconnect are display-only.
- 30-second active freeze snapshot only when dirty/active.
- Critical transitions save immediately.
- Seller consignment and delivery claim save immediately.
- Account changes save immediately to the per-save account profile.
- Purchase/sale ledger changes use the per-save ledger and critical transaction updates force save.
- Do not add another writer or another restore path.

---

## 8. Verification result

### Gate 1
PASS — exact v0.1.9.4 base, SHA verified, 19 files.

### Gate 2
PASS — 19 files, 11 changed, no added/removed paths; Lua syntax, JavaScript syntax, JSON parsing, HTML mirror equality; no global legacy account/ledger/state fallback reads; account excluded from auction snapshot; save-stamped account/ledger; save-slot runtime handles cleared.

### Gate 3
PASS — ZIP integrity; fresh extraction 19 files; byte-for-byte match; syntax checks rerun from fresh extraction.

Artifacts:

- `JOB-13_v0_1_9_5_TRIPLE_VERIFICATION_AUDIT.md`
- `JOB-13_v0_1_9_5_SAVE_DOMAIN_AUDIT.md`
- `JOB-13_v0_1_9_5_FILE_MANIFEST_SHA256.csv`
- `JOB-13_v0_1_9_5_TEST_CHECKLIST.txt`

Static verification is not runtime proof.

---

## 9. Exact next runtime test

Install only v0.1.9.5. Keep JOB-04 and JOB-09 unchanged. Fully restart BeamNG.

Test save isolation first:

1. Open Career Save A and note membership, watchlist, Bought/Sold Vehicles, invoices, auction number, and two lot IDs.
2. Switch to a different Career Save B.
3. Save B must not contain Save A's Bought/Sold Vehicles, invoices, membership, watchlist, reminder, bids, consignments, or auction state.
4. Save B should have its own empty transaction history unless that save already had JOB-13 history.
5. Return to Save A and confirm its own data remains.

Stop immediately if cross-save data appears, a vehicle duplicates/disappears, money charges twice, or page reload creates another timeline.

---

## 10. Protected rules

- Never claim runtime success before exact-ZIP user testing.
- Keep JOB-04, JOB-09, and JOB-13 separate.
- Do not edit shared FoxNet/browser files without permission.
- Never reintroduce global Career-progress fallback files.
- Do not add redundant account state back into the auction snapshot.
- Do not add a second auction-state writer or recovery system.
- Use exact Career inventory IDs plus stable delivery keys.
- Never knowingly charge or deliver twice.
- Keep GitHub handoff and issue #40 current after every test.
