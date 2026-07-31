# JOB-13 v0.1.5 Phone Route + RLS-Derived Bidding Patch

**Date:** 2026-07-31 PT  
**Owner:** David / Captain  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions

## Input

- `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_4_APPROVED_POOL_PATCH.zip`
- SHA-256: `56c4143cbb3233dd187bfe22aafeca48b5024e917cd3e1d4a25626033402c84f`

## Output

- `zzzz_RedFox_JOB13_FoxNet_Online_Auctions_v0_1_5_PHONE_ROUTE_BIDDING_PATCH.zip`
- SHA-256: `543458cb819676c112d91aeb6b25bafc4a0b916699f8029ba64d473e3cb453ad`
- Runtime files: 39
- ZIP bytes: 429,740
- Runtime: **UNTESTED**

## Owner-reported failure

- FoxNet Auctions still required approximately 2–5 minutes to load.
- Selecting a vehicle opened the native dealership Purchase Information menu.
- The menu exposed Negotiate Price, Trade-In, Insurance and Purchase instead of auction bidding.

## Root cause

JOB-13 v0.1.4 did not call `vehicleShopping`; its standalone page already had the lightweight 12-lot bidding UI. The screenshot therefore proved the phone/browser auction route was still opening the obsolete copied marketplace/purchase page rather than JOB-13.

## Implemented

1. New versioned app/site path: `ui/modules/apps/redfoxJob13Auctions_v015/**`.
2. New versioned state/settings paths so v0.1.5 does not parse previous oversized or stale auction data.
3. Four small JOB-13-owned compatibility shims for the two known FoxNet Auctions feature roots; they redirect only the auction destination to the v0.1.5 bidding page.
4. No native purchase, negotiation, trade-in, insurance or dealership actions.
5. Approved local pool remains 21 vehicles; browser receives 12 lightweight summaries.
6. Full lot details and bid history load only when a lot opens.
7. RLS-derived timed NPC behavior: private maximums, scheduled bids, one due bid per lot tick, 250/500/1000/5000-style increments, time-pressure acceleration, player-bid wakeups and soft-close extension.
8. Dirty-state persistence remains; simulated 120 seconds idle produced zero extra state writes.

## Not touched

- `ui/ui-vue/dist/index.js`
- `ui/ui-vue/dist/index.css`
- `lua/ge/extensions/ui/phone/layout.lua`
- `lua/ge/extensions/redfoxCareerWeb.lua`
- shared Browser Core JavaScript
- JOB-04, JOB-09, BeamBook, FoxFax or unrelated sites
- stock/RLS `vehicleShopping`
- LIVE Career money/ownership/delivery

## Static verification

- ZIP integrity: PASS
- Lua syntax: PASS
- JavaScript syntax: PASS
- JSON parsing: PASS
- Duplicate ZIP paths: 0
- Byte-identical duplicate files: 0
- Forbidden shared/core overrides: 0
- Approved pool: 21
- Initial visible lots: 12
- Native purchase-action search: none
- Behavior harness: PASS
- `open_purchase` rejected as `UNKNOWN_ACTION`: PASS

## Required runtime test

1. Remove/disable all older JOB-13 ZIPs.
2. Install only the `zzzz_`-prefixed v0.1.5 package.
3. Clear BeamNG WebUI cache and fully restart.
4. Open phone FoxNet Auctions and time it.
5. Confirm the native Purchase Information menu does not appear.
6. Register TEST membership, open a lot, place a normal bid, set a maximum bid and cancel before close.
7. Capture screenshot and `beamng.log` if the obsolete purchase page remains.
