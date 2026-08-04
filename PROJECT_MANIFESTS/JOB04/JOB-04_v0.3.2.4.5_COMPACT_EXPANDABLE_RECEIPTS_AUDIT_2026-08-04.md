# JOB-04 v0.3.2.4.5 — Compact Expandable Receipts Audit

**Date:** 2026-08-04  
**Owner:** David / Captain  
**Job:** JOB-04 — RedFox FoxNet Welcome Hub + Wrecking Yard  
**Classification:** UI-only candidate; static/harness verified; BeamNG runtime pending

## Owner-accepted source baseline

This build starts from the exact owner-runtime-passed artifact:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-04_v0_3_2_4_4_INSTANT_COMPLETE_YARD_SALE_RECEIPTS_FROM_v0_3_2_4_3.zip
SHA-256: e4352bffe0e9742bf754e99d189c3c2cac4bad3de2a3a79d03f0b6660d439fe8
```

David reported **“all pass”** against the v0.3.2.4.4 runtime gate. That owner result freezes the instant complete-vehicle yard sale, RLS reference pricing, instant discount, exact vehicle removal, one payment, saved receipt, restart persistence, PC/phone access, buying page, Tow route, and Auction route as the accepted transaction baseline.

## New installable candidate

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-04_v0_3_2_4_5_COMPACT_EXPANDABLE_RECEIPTS_FROM_v0_3_2_4_4.zip
SHA-256: 5439f0859fdbe6e9c2c6052f0f80bedafabde63045a6c0b3bd4760e75da18fb9
Size: 16,978,091 bytes
Files: 677
```

## Authorized scope

The owner requested that receipt history appear as compact Rolodex/index cards and expand into the complete receipt.

Implemented behavior:

- Receipt history defaults to compact index-card summaries.
- Each compact card shows receipt number, vehicle, transaction type, date, Career inventory ID, and amount credited.
- Selecting a card expands its complete saved receipt inline.
- Expanding another card closes the previously expanded card.
- The expanded receipt preserves every v0.3.2.4.4 field and wording.
- The immediate post-sale receipt popup remains a complete receipt.
- PC and phone use one cache-unique v0.3.2.4.5 entry.
- All older Wrecking Yard entry files redirect to the new entry.

## Explicitly unchanged

- All Lua files are byte-identical to v0.3.2.4.4.
- RLS reference-value calculation is unchanged.
- Instant-yard-sale discount calculation is unchanged.
- Quote, payment, exact inventory removal, persistence, retry, and idempotency logic are unchanged.
- Wrecking Yard buying behavior is unchanged.
- Receipt data schema and stored receipt records are unchanged.
- JOB-09 Tow route and business logic are unchanged.
- JOB-13 Auction route and business logic are unchanged.
- Auto-strip and remainder/frame sale remain disabled.
- Rotating Welcome images and advertisements remain outside this patch.

## Exact file boundary

```text
Modified existing files: 20
Added files: 6
Removed files: 0
Changed Lua files: 0
```

The 20 modified files are limited to:

- `info.json`
- three PC/phone Welcome route JavaScript files
- eight legacy Wrecking Yard entry/redirect files in each of the two mirrored site trees

The six added files are:

```text
sites/scrap_yard/index_v03245.html
sites/scrap_yard/assets/js/scrap_v03245.js
sites/scrap_yard/assets/css/scrap_v03245.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index_v03245.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap_v03245.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap_v03245.css
```

## Verification performed

- Exact source ZIP SHA confirmed.
- Exact 20-modified / 6-added / 0-removed boundary confirmed.
- Every Lua file compared byte-for-byte with v0.3.2.4.4.
- Critical browser transaction functions compared text-for-text with v0.3.2.4.4.
- Both Wrecking Yard mirrors are byte-identical.
- JOB-09 and JOB-13 active path overlap remains zero, excluding unavoidable root metadata.
- Modified/new JavaScript passed syntax checks.
- All packaged JSON parsed successfully.
- New HTML and CSS local references resolved.
- CSS structural balance passed.
- 143 focused validation checks passed.
- Node receipt UI harness passed compact generation, full receipt generation, acquisition fields, expand/collapse behavior, and ARIA state.
- ZIP integrity, duplicate-path, unsafe-path, and fresh-extraction checks passed.
- Packaged extraction contains 677 files and byte-matches the work tree.

## Runtime test gate

No new vehicle sale is required to test the main change because v0.3.2.4.4 transaction behavior is unchanged and already owner-passed.

1. Disable v0.3.2.4.4 and all older JOB-04 ZIPs.
2. Enable v0.3.2.4.5 with the currently working JOB-09 and JOB-13 companions.
3. Clear BeamNG WebUI cache and restart.
4. Open Wrecking Yard on PC and phone.
5. Confirm badge `v0.3.2.4.5` and Buy From Yard still loads first.
6. Open **Receipts**.
7. Confirm existing receipts appear as compact index cards rather than full receipts.
8. Select one card and confirm the complete receipt expands inline.
9. Select another card and confirm the first closes while the second expands.
10. Confirm all prior receipt fields remain present, including acquisition source/location.
11. Confirm closing and reopening the page does not delete receipt history.
12. Recheck Wrecking Yard buying, Tow, and Auctions from PC and phone.

## Status

**STATIC/HARNESS PASS — BEAMNG RUNTIME PENDING.**  
The accepted transaction baseline remains v0.3.2.4.4 until David confirms the new compact/expandable receipt presentation in runtime.
