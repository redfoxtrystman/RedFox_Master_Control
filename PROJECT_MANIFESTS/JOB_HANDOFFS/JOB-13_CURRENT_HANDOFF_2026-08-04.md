# JOB-13 — FoxNet Online Vehicle Auctions

## Authoritative recovery handoff

**Updated:** 2026-08-04
**Branch:** `job13-online-auctions`
**Primary issue:** #40 `[JOB-13] CLAIMED — FoxNet Online Vehicle Auctions`

This file is the current authoritative handoff if the active ChatGPT conversation ends. Do not rename, merge, or move JOB-13 into another job.

---

## 1. Latest build awaiting runtime testing

**ZIP:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_1_RECOVERY_FILTERS_CALMER_NPCS_MULTI_CONSIGNMENTS.zip`

**SHA-256:** `178648f5b3b4588ba76350e53e9954c0aab979b4db5b9ef73149b17aac170ff7`

**Base:** v0.1.9.0, SHA-256 `58debecc1e7c2eb2257dcbb9d70e7c7265090063276159ebfa6129c10fbfefa0`

v0.1.9.1 passed static triple verification. It is **not BeamNG-runtime-proven** until the user tests this exact ZIP.

### v0.1.9.0 runtime result

Partial pass:

- bank-backed buying power appeared functional;
- varied vehicles worked;
- player seller screen worked;
- starting bid and private reserve worked;
- player vehicle entered the next auction;
- reserve-not-met behavior appeared on the listing.

Runtime failures/defects:

- auction state did not restore after Career/game reload;
- both native dropdowns still failed in BeamNG CEF;
- NPC bidding was too aggressive on too many lots;
- seller screen needed clearer current RLS market value;
- one-vehicle consignment limit was rejected by the user;
- recent Wrecking Yard purchases could show `Unknown / legacy record`.

Do not tell the user to keep testing v0.1.9.0 recovery.

---

## 2. Runtime-proven architecture that must not regress

The user has proved:

- JOB-04 Wrecking Yard, JOB-09 Tow, and JOB-13 Auction remain separate ZIPs.
- The shared FoxNet Welcome Page routes to JOB-13's unique Auction path.
- PC and phone open the same JOB-13 website.
- Auction purchases can enter Career inventory.
- Wrecking Yard purchases continue working beside JOB-13.
- Tow website is operational.
- Different installed/modded vehicles can appear.
- Player consignments and reserve UI can be created.

Known runtime-safe Wrecking Yard route base:

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`

Do not combine the jobs and do not modify JOB-04 or JOB-09 for v0.1.9.1 testing.

---

## 3. v0.1.9.1 changes

### 3.1 Recovery-first repair

v0.1.9.0 stored recovery state in a global settings path and used strict catalog validation. A written snapshot could be discarded and replaced with a new market when the current catalog differed.

v0.1.9.1 now stores state per active Career save:

- `<currentSavePath>/career/rls_career/redfox_job13/auction_state_v0191.json`
- `<currentSavePath>/career/rls_career/redfox_job13/account_profile_v2.json`
- `<currentSavePath>/career/rls_career/redfox_job13/auction_ledger_v2.json`

The old global v0.1.9.0 files are read only as a one-time migration fallback.

Recovery validation is structural. It verifies that the snapshot contains usable lots and times instead of rejecting the whole auction because the installed catalog changed.

Every completed snapshot is immediately read back and the snapshot serial is verified. Failure keeps the state dirty and logs the exact path.

Lifecycle coverage includes:

- extension load after a Career save path is available;
- Career activation/modules activation;
- save-slot selection/change;
- Career save-slot commit;
- Career deactivation;
- clean extension unload.

On restore, active and future lot times shift by offline duration so the auction freezes while the game is closed.

### 3.2 Save-frequency rules preserved

- Full auction snapshot every 30 seconds only while active and dirty.
- No recurring idle writes.
- NPC bids mark state dirty; they do not force a full save.
- Player bids/cancellations do not each force a full snapshot.
- Critical boundaries may save immediately: lot close, purchase, sale, delivery, save-slot commit, clean deactivation/unload.
- Catalog cache is not rewritten with each auction snapshot.

### 3.3 Dropdown repair

The two native HTML `<select>` controls were removed from the main Auction filters. BeamNG CEF-safe custom button menus now handle:

- vehicle/category filter;
- ending soon;
- current price low-to-high;
- current price high-to-low;
- lot number.

The saved-search category selector also uses the custom menu system.

### 3.4 Calmer NPC bidding

Defaults now target varied activity rather than a fight on nearly every vehicle:

- minimum bidders: 0;
- maximum bidders: 3;
- no-bid chance: 35%;
- aggression: 35%;
- early bidding: 12%;
- substantially longer bid delays;
- player bids only sometimes wake NPCs immediately;
- rare hot lots may still produce larger contests.

Exact old v0.1.9.0 default settings migrate automatically to the calmer profile. Intentional custom settings remain preserved.

### 3.5 Seller screen and multiple consignments

Seller cards now show:

- current RLS market value;
- suggested opening bid;
- suggested reserve;
- acquisition source and original price when known.

The fixed one-car consignment limit is removed. Each exact Career inventory ID is independently locked. Seller vehicles fill generated slots in future groups of ten; extra vehicles spill into later prepared groups rather than being rejected.

### 3.6 Wrecking Yard acquisition lookup

JOB-13 reads `settings/redfox/career_web_state.json` read-only and matches `scrapYardPurchases` by exact Career inventory ID. When that record exists, seller UI can show:

- `RedFox Wrecking Yard`;
- original price;
- purchase date/reference.

JOB-04 was not modified. Older purchases that were never recorded with the exact inventory ID may still remain unknown.

---

## 4. Existing features to preserve and re-test

- wallet plus eligible personal bank buying power;
- purchase settlement and garage delivery;
- PC and phone routes;
- membership/watchlist/max-bid persistence;
- stable Fox Facts and bid history;
- varied installed/mod vehicle catalog;
- player seller reserve behavior;
- purchased/sold/no-sale records;
- exact inventory ID safety;
- no full catalog scan at Career startup/page open.

Vehicle photo management remains owned by Dev Manager. JOB-13 should consume Career thumbnails.

---

## 5. Triple verification

### Gate 1 — before editing

PASS:

- exact v0.1.9.0 ZIP and SHA verified;
- 19 files;
- zero duplicate paths;
- zero unsafe paths;
- JOB-04, JOB-09, and shared FoxNet protected.

### Gate 2 — after editing

PASS:

- 12 JOB-13 files changed;
- no files added or removed;
- all JSON parsed;
- all JavaScript passed `node --check`;
- all Lua files compiled through Lua 5.4 syntax loading;
- three JOB-13 HTML mirrors are byte-identical;
- custom menus present and native main dropdowns absent;
- per-Career state paths and lifecycle hooks present;
- snapshot write/readback verification present;
- no fixed consignment limit;
- calmer NPC defaults present;
- no JOB-04/JOB-09 files included.

The pre-edit scope was expanded only to JOB-13 app-shell/cache metadata so BeamNG CEF does not retain v0.1.9.0 UI. No shared file was changed.

### Gate 3 — after ZIP creation

PASS:

- ZIP CRC/integrity;
- zero duplicate/unsafe paths;
- fresh extraction file list and every SHA-256 matched edited tree.

Artifacts:

- `JOB-13_v0_1_9_1_PRE_EDIT_BASELINE.txt`
- `JOB-13_v0_1_9_1_TRIPLE_VERIFICATION_AUDIT.md`
- `JOB-13_v0_1_9_1_FILE_MANIFEST_SHA256.csv`
- `JOB-13_v0_1_9_1_TEST_CHECKLIST.txt`

Static verification is not runtime proof.

---

## 6. Exact next runtime test order

Install only v0.1.9.1 for JOB-13. Disable all older JOB-13 ZIPs. Keep current JOB-04 and JOB-09 ZIPs unchanged. Fully restart BeamNG.

### Recovery must be tested first

1. Open Auction from PC.
2. Place one inexpensive bid and set a confidential maximum.
3. Record auction number, lot number, visible bid, maximum, and remaining time.
4. Wait at least 35 seconds.
5. Close BeamNG normally, restart, and reopen the same Career save.
6. Confirm exact same auction/lot, bid, maximum, bid history, and frozen/resumed timer.
7. Confirm one-time `Interrupted auction restored` notice.

If any part fails, stop testing and report it before testing other features.

### After recovery passes

8. Test category and all four sort menu choices.
9. Observe multiple lots: some quiet/no-bid, some moderate, rare bidding fights.
10. Confirm seller cards show current RLS value and suggestions.
11. Submit two or three vehicles and confirm no fixed one-car limit.
12. Check a recent Wrecking Yard vehicle for source/original price.
13. Confirm PC/phone purchases still deliver once and money is deducted once.

Stop immediately if money duplicates, a vehicle duplicates/disappears, phone/PC locks, or Career becomes stuck.

---

## 7. Protected rules

- Never claim runtime success before exact-ZIP user testing.
- Keep JOB-04, JOB-09, and JOB-13 separate.
- Do not edit shared FoxNet/browser files without permission.
- Do not spam saves.
- Do not scan the full catalog at Career startup/page open.
- Use exact Career inventory IDs for custody and settlement.
- Never create a permanent duplicate vehicle.
- Keep GitHub handoff and issue #40 current after every test.
