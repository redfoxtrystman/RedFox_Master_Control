# JOB-13 v0.1.3 Slim Dirty-State Patch — Build Record

**Date/time:** 2026-07-30 20:38 PDT  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Owner:** David / Captain  
**Status:** BUILT — STATICALLY VERIFIED — RUNTIME UNTESTED

## Owner request

Create a narrow patch before considering a restart. Remove unnecessary runtime material, correct the constant state-file rewrite behavior, preserve the current bidding screen, update GitHub, and do not modify another job or shared website.

## Source

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip
SHA-256: 1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071
```

## Output

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_3_SLIM_PATCH.zip
SHA-256: 660f6fb5eae9f54cae4173590ac08d1de7655ca3ccfc7e14b8fa7f72ed2dee1e
ZIP size: 421,722 bytes
Runtime files: 34
Uncompressed runtime data: 485,786 bytes
```

## Exact corrections

1. Replaced the unconditional approximately two-second `state.json` rewrite with dirty-state persistence.
2. Idle `onUpdate()` timer checks now perform zero state-file writes.
3. Ordinary dirty changes are batched to no more than one state write every 30 seconds.
4. Critical bid, membership, invoice, auction generation/rotation, manual TEST-time advance, and unload operations still save immediately.
5. Prevented duplicate writes when TEST-time advancement calls the lot tick and then performs a forced save.
6. Removed startup loading of `redfoxJob13AuctionSettings`; WEUI now lazy-loads only when opened.
7. Removed the duplicate host-side five-second full-state polling loop.
8. Reduced the site safety refresh from five seconds to 30 seconds.
9. Removed runtime-irrelevant audit documents, behavior harness, generic root README, and embedded development manifest.
10. Kept the established `redfoxJob13Auctions_v012` internal path for route compatibility while updating cache tags and visible metadata to v0.1.3.

## Removed from runtime ZIP

```text
FILE_MANIFEST_SHA256.csv
README_OPEN_FIRST.txt
docs/BUILD_AUDIT_2026-07-29.md
docs/JOB13_INTEGRATION_MANIFEST.md
docs/TEST_PLAN.md
docs/V0_1_2_BIDDING_SCREEN_CORRECTION.md
docs/WEUI_SETTINGS_REFERENCE.md
docs/v012_behavior_harness.lua
```

A namespaced runtime note remains under:

```text
mod_info/RedFoxJOB13/RUNTIME_NOTE.txt
```

## Files modified

```text
lua/ge/extensions/redfoxJob13Auction.lua
scripts/redfox_job13_online_auctions/modScript.lua
ui/modules/apps/redfoxJob13Auctions_v012/app.html
ui/modules/apps/redfoxJob13Auctions_v012/app.js
ui/modules/apps/redfoxJob13Auctions_v012/app.json
ui/modules/apps/redfoxJob13Auctions_v012/site/app.js
mod_info/RedFoxJOB13/info.json
```

## Files deliberately not modified or packaged

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfoxCareerWeb.lua
ui/modModules/redfoxCareerWeb/**
JOB-01 files
JOB-02 files
JOB-04 files
JOB-05 files
JOB-07 files
JOB-09 files
shared FoxNet phone/browser route files
```

## Static verification

```text
ZIP integrity: PASS
Duplicate internal paths: 0
Forbidden shared/core paths: 0
JavaScript syntax: PASS
Lua syntax via texlua loadfile: PASS
JSON parsing: PASS
Real vehicle images retained: 21
```

Persistence behavior harness:

```text
Initial state creation: 1 state write
120 seconds of idle updates: 0 additional state writes
One dirty flush after the 30-second interval: 1 write
Continued clean updates: 0 additional writes
```

## Runtime status

```text
UNTESTED IN BEAMNG
EARLY TEST PATCH
NOT RELEASE READY
LIVE CAREER/RLS TRANSACTIONS LOCKED
```

## Required test

1. Disable or remove JOB-13 v0.1.2.
2. Install only the exact v0.1.3 ZIP for JOB-13.
3. Clear BeamNG WebUI cache if v0.1.2 assets remain visible.
4. Open the JOB-13 UI App.
5. Leave it idle for at least two minutes and check for stutter or continuous write/log activity.
6. Activate a TEST membership.
7. Watch a lot, place a bid, cancel a bid, and reopen the page.
8. Confirm state persists without continuous rewriting.
9. Record keep/reject/rollback before another version.

## Known problems not claimed fixed

- The shared phone icon may still point to an older marketplace-style auction site owned by the shared browser package.
- LIVE money, ownership, inventory, garage, and shipping integration is not connected.
- Vehicle catalog and classifications remain early test data requiring runtime review.
- Three-mod compatibility remains unproven until the slim JOB-04/JOB-09 packages and shared browser route are tested together.
