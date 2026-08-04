# JOB-13 v0.1.9.0 — Bank, Reserve, Selling, and Crash Recovery

**Date:** 2026-08-04
**Status:** Packaged and triple-verified; awaiting BeamNG runtime testing
**Branch:** `job13-online-auctions`
**Issue:** #40

## Deliverable

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_0_BANK_RESERVE_SELLING_CRASH_RECOVERY.zip`

SHA-256:

`58debecc1e7c2eb2257dcbb9d70e7c7265090063276159ebfa6129c10fbfefa0`

ZIP size: 174,780 bytes
File count: 19

Base:

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_3_STABLE_STATE_CAMERA_THUMBNAIL_RETAKE.zip`

Base SHA-256:

`9c1789d5d8013d783cb2d14f0bc4fb48bd7319afa45d5df66531cb454499015a`

## Implemented scope

- Personal RLS bank balance included in buying power.
- Wallet/bank-backed payment path using the existing player-attribute charge after withdrawing only the needed bank deficit.
- PC and phone seller/consignment UI.
- Exact Career inventory ID locking.
- Starting bid and private reserve.
- Seller listing enters the next auction group, not the live group.
- Reserve-not-met returns the exact vehicle with no payout.
- Successful sale removes the exact vehicle and pays hammer minus seller fee.
- Purchased/sold/no-sale ledger and invoice records.
- Crash-safe active-auction freeze/resume.
- Dirty full snapshot every 30 seconds only while active.
- No idle save loop and no full state write for every bid/NPC bid.
- `redfox.auction.bridge.v1` contract for later Tow Yard integration.
- No JOB-04, JOB-09, or shared FoxNet route files changed.

## Important limitations

- RLS exposes one native `listedForAuction` inventory lock at a time, so this build permits one active personal consignment.
- Tow Yard `Send to Auction` is not connected yet; the bridge contract is present but must wait for standalone seller runtime proof.
- Hard-crash recovery can lose events newer than the last completed snapshot, normally up to approximately 30 seconds.
- Runtime success is unproven until the user tests this exact ZIP.

## Save policy

- Full atomic snapshot every 30 seconds only when active and dirty.
- NPC and player bid changes mark state dirty without forcing a full immediate write.
- Critical boundaries may save immediately: lot close, purchase, sale, delivery, clean Career exit, and state transitions.
- No repeated state writes while idle.
- Catalog cache is not rewritten with each auction snapshot.

## Changed files

12 approved JOB-13 files changed:

- `lua/ge/extensions/redfoxJob13Auction.lua`
- `lua/ge/extensions/redfoxJob13AuctionSettings.lua`
- `mod_info/RedFoxJOB13/RUNTIME_NOTE.txt`
- `mod_info/RedFoxJOB13/info.json`
- `sites/redfox_job13_auctions/index.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job13_auctions/index.html`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.html`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.js`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.json`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.css`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.js`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/index.html`

7 source files remained byte-identical.

## Triple verification

### Gate 1 — pre-edit

PASS:

- exact source hash;
- ZIP integrity;
- 19 files;
- zero duplicate/unsafe paths;
- protected cross-job baseline recorded.

### Gate 2 — post-edit

PASS:

- exact changed-file scope;
- JSON parse;
- JavaScript syntax;
- Lua syntax;
- CSS/HTML structural checks;
- route-copy identity;
- no Wrecking Yard overlap;
- no JOB-09 files;
- no immediate full save per player/NPC bid.

Mock harness PASS for:

- bank-backed membership/bidding;
- one dirty save at 30 seconds;
- simulated five-minute outage recovery;
- bank-backed purchase and invoice;
- reserve-not-met exact vehicle return;
- successful exact-inventory sale and payout.

### Gate 3 — final ZIP

PASS:

- ZIP integrity;
- fresh extraction matched work tree byte-for-byte;
- 19 files;
- zero duplicate/unsafe paths;
- JSON/JS/Lua/harness re-run from fresh extraction.

## Verification artifact hashes

- Triple audit: `61acc1dd88159bc69edd18e8032c1ab682f2b2c1160603b16a6e35884f635875`
- File manifest: `1658e290e4393c8bf6ba16e4daefa5ddedcc70af843f42def96ef034e92bcc31`
- Test checklist: `d1772694832bee7d71beb368efd3ac96065d10e99a02da9bf8ae9dd971bfd688`

## Required runtime order

1. Disable older JOB-13 ZIPs and install only v0.1.9.0.
2. Keep working JOB-04 and JOB-09 unchanged.
3. Verify PC/phone and prior UI-state fixes.
4. Verify bank buying power and one inexpensive purchase.
5. Verify controlled restart recovery after waiting at least 35 seconds.
6. Verify high-reserve no-sale and exact vehicle return.
7. Verify reachable-reserve sale and exact payout/removal.
8. Verify Wrecking Yard and Tow regressions.
9. Connect Tow Yard only after standalone seller runtime proof.

Stop immediately on duplicate charge, duplicate/lost vehicle, locked UI, or corrupted Career state.
