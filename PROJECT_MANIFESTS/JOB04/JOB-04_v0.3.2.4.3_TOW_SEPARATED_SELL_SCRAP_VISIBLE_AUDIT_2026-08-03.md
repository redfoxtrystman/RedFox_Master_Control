# JOB-04 v0.3.2.4.3 — Tow-Separated Sell/Scrap Visible Audit

**Date:** 2026-08-03  
**Owner:** David / Captain  
**Job:** JOB-04 — Wrecking Yard + current FoxNet Welcome host  
**Status:** BUILT — STATIC/HARNESS VERIFIED — BEAMNG RUNTIME UNPROVEN

## Owner-reported failures

1. JOB-04 v0.3.2.4.2 still contained and linked the obsolete bundled `redfox_recovery` website, preventing the new separate JOB-09 Tow website from being visible.
2. Selling was still not visible to the owner.

## Exact source

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-02_v0_3_2_4_2_CACHE_PROOF_SELL_WHOLE_SCRAP_ROUTE_FROM_v0_3_2_4_1.zip`

SHA-256: `751501c31f2acafb5dc79a4965d7bda77818445e0c1308b7135dc9a6468b7391`

## Route-separation reference

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-02_v0_3_2_3_2_TOW_ROUTE_TO_JOB09.zip`

SHA-256: `6a13b65e666461317b9c809af313cfc231d11958feca50ae35880c97436b1cab`

Only its proven Tow route surgery was used. Its older Wrecking Yard page/backend was not substituted.

## Output

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-03_v0_3_2_4_3_TOW_SEPARATED_SELL_SCRAP_VISIBLE_FROM_v0_3_2_4_2.zip`

SHA-256: `f7344a33d0fd50d9643a570ab6590a98d5adf14b7a7a6389da7b88eb5c413b7a`

Size: **16,860,262 bytes**  
Files: **665**

## Exact change boundary from v0.3.2.4.2

- Added: **6 files**
- Changed: **22 files**
- Removed: **70 files**
- Unchanged: **637 files**

### Removed

Seventy obsolete Tow/Recovery content files under:

- `sites/redfox_recovery/**`
- `ui/modModules/redfoxCareerWeb/sites/redfox_recovery/**`

### Stale-route protection retained

Only two minimal compatibility files remain:

- `sites/redfox_recovery/index.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_recovery/index.html`

They contain no Tow business page. They immediately redirect an old cached JOB-04 route to:

`redfox_job09_towing/index.html?v=0480`

### Current Tow links changed

PC, phone, route configuration and both Legal Portal mirrors now open the separate JOB-09 route. The Welcome tile is labeled **RedFox Towing**.

### Selling made cache-unique and immediately visible

Added in both website mirrors:

- `index_v03243.html`
- `assets/js/scrap_v03243.js`
- `assets/css/scrap_v03243.css`

Every known older Wrecking Yard entry page redirects to:

`index_v03243.html?v=03243-tow-separated-sell-visible`

The new page:

- displays build badge `v0.3.2.4.3`;
- opens **SELL / SCRAP MY VEHICLES** first;
- automatically loads the owned Career/RLS vehicle list;
- visibly exposes **Sell Vehicle** and **Scrap Whole Vehicle** on each eligible vehicle;
- keeps **BUY FROM YARD** available as the other top tab.

## Protected behavior

The following are byte-identical to v0.3.2.4.2:

- all `lua/ge/extensions/redfox/career/**` Wrecking Yard transaction modules;
- `lua/ge/extensions/redfoxWreckingYardPurchase.lua`;
- native Career/RLS sale implementation;
- whole-vehicle scrap transaction and idempotency logic;
- purchase and garage-delivery adapter;
- Wrecking Yard inventory/config/data/assets not listed in the manifest;
- JOB-13 unique Auction route and unrelated websites.

## Compatibility results

Exact companion archives checked:

### JOB-09

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_8_0_SEPARATE_FOXNET_ROUTE_PUBLIC_COMPANY_TOW_PAYMENT_CHOICES.zip`

SHA-256: `fc229ee77d89df220d7762643dcd76f1321f309b0b511e45ca549c155608ada3`

### JOB-13

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_1_UNIQUE_FOXNET_ROUTE.zip`

SHA-256: `74c7a786253f088b90a2ab78a75d8ec61b3fd9c2d1a471b3f311d5e6771b4bcb`

Path overlap:

- JOB-04 vs JOB-09: **0**
- JOB-04 vs JOB-13: **0**
- JOB-09 vs JOB-13: **0**

Both JOB-09 route targets exist in the JOB-09 archive.

## Verification

Passed:

- ZIP integrity
- no duplicate ZIP paths
- fresh extraction: 665/665 files
- fresh extraction byte-identical to working tree
- JSON parsing
- JavaScript syntax with `node --check`
- Lua syntax with `texlua`
- mirrored site identity
- changed/added/removed scope boundary
- protected Wrecking Yard backend hashes
- old Tow route reference scan
- external JOB-09 and JOB-13 target checks
- modified/new HTML reference checks
- transaction harness:
  - owned dashboard lists vehicles
  - native sale removes exact vehicle
  - native-sale replay is idempotent
  - scrap quote is positive
  - whole scrap removes exact vehicle
  - whole scrap pays once
  - replay does not duplicate payment

Harness result: `JOB04_TRANSACTION_HARNESS_PASS`

## Runtime test gate

Disable all older JOB-04, JOB-09 and JOB-13 ZIPs. Install only:

1. JOB-04 v0.3.2.4.3
2. JOB-09 v0.4.8.0
3. JOB-13 v0.1.8.1

Clear BeamNG WebUI cache and restart.

Test:

1. Wrecking Yard from PC opens at **SELL / SCRAP MY VEHICLES** and shows `v0.3.2.4.3`.
2. Wrecking Yard from phone does the same.
3. Owned vehicles load and show **Sell Vehicle** and **Scrap Whole Vehicle**.
4. **BUY FROM YARD** still opens the purchasing inventory.
5. RedFox Towing opens the JOB-09 v0.4.8.0 website from PC and phone.
6. An intentionally stale `redfox_recovery/index.html` route redirects to JOB-09 rather than displaying an old Tow page.
7. Auctions still open from PC and phone.
8. Only after the pages are correct, sell one inexpensive vehicle and verify one removal/one native payment.

Do not mark runtime working until David tests this exact ZIP trio.
