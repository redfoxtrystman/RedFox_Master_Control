# JOB-04 v0.3.2.3.2 + JOB-09 v0.4.8.0 Compatibility Audit

**Audit date:** 2026-08-02  
**Purpose:** Verify that JOB-09's separate FoxNet Tow route did not alter or break the known-working JOB-04 Wrecking Yard baseline.

## Exact files

### Known-working comparison baseline

- `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_3_1_AUCTION_ROUTE_TO_JOB13.zip`
- Bytes: `16,830,590`
- SHA-256: `e4cf49a1adf4d86d996a7c1f098fe19dc1db670f0b53094435486844e58389b1`
- Files: `717`

### Updated JOB-04 host supplied for this audit

- `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-02_v0_3_2_3_2_TOW_ROUTE_TO_JOB09.zip`
- Bytes: `16,789,829`
- SHA-256: `6a13b65e666461317b9c809af313cfc231d11958feca50ae35880c97436b1cab`
- Files: `645`

### Separate JOB-09 Tow module supplied for this audit

- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_8_0_SEPARATE_FOXNET_ROUTE_PUBLIC_COMPANY_TOW_PAYMENT_CHOICES.zip`
- Bytes: `3,097,152`
- SHA-256: `fc229ee77d89df220d7762643dcd76f1321f309b0b511e45ca549c155608ada3`
- Files: `63`

### Existing JOB-13 companion checked for three-mod collisions

- `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_1_UNIQUE_FOXNET_ROUTE.zip`
- Bytes: `158,895`
- SHA-256: `74c7a786253f088b90a2ab78a75d8ec61b3fd9c2d1a471b3f311d5e6771b4bcb`
- Files: `19`

## JOB-04 comparison result

Compared every file path and every file SHA-256 from v0.3.2.3.1 to v0.3.2.3.2.

- Added files: **0**
- Removed files: **72**
- Changed files: **8**
- Byte-identical common files: **637**

### Removed files

Exactly 72 files were removed:

- 36 files under `sites/redfox_recovery/**`
- the same 36-file mirror under `ui/modModules/redfoxCareerWeb/sites/redfox_recovery/**`

No Wrecking Yard, Auction, Welcome shell, phone shell, purchase adapter, Career bridge, or unrelated website file was removed.

### Changed files

Exactly eight files changed:

- `assets/config/routes.json`
- `assets/js/icefox_front.js`
- `info.json`
- `pages/legal/index.html`
- `ui/modModules/redfoxCareerWeb/assets/config/routes.json`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
- `ui/modModules/redfoxCareerWeb/pages/legal/index.html`
- `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js`

The seven route/UI files only replace the obsolete bundled Recovery label/path with:

- Label: `RedFox Towing`
- Unique route: `sites/redfox_job09_towing/index.html?v=0480`
- Phone mirror route: `../sites/redfox_job09_towing/index.html?v=0480`

`info.json` changes only JOB-04's package name/version/description to identify the route-separation build.

### Wrecking Yard protection check

- Wrecking Yard-related paths checked: **78**
- Byte-identical: **78**
- Changed: **0**
- Removed: **0**

Verified byte-identical examples:

- `lua/ge/extensions/redfoxWreckingYardPurchase.lua`
- `lua/ge/extensions/redfox/career/scrapyardBridge.lua`
- `lua/ge/extensions/redfox/career/scrapyardCef.lua`
- `lua/ge/extensions/redfox/career/scrapyardStorage.lua`
- `sites/scrap_yard/index_v032.html`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/index_v032.html`

The Auction route to JOB-13 remains unchanged.

## Cross-mod collision check

Active path overlap counts:

- JOB-04 v0.3.2.3.2 vs JOB-09 v0.4.8.0: **0**
- JOB-04 v0.3.2.3.2 vs JOB-13 v0.1.8.1: **0**
- JOB-09 v0.4.8.0 vs JOB-13 v0.1.8.1: **0**

All three are zero.

JOB-09 does not ship any JOB-04 Wrecking Yard, Auction, shared global Vue bundle, phone layout, `redfoxCareerWeb.lua`, or copied unrelated website paths.

## Route and mirror verification

- JOB-09 provides `sites/redfox_job09_towing/index.html`.
- JOB-09 provides `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/index.html`.
- Those two route files are byte-identical.
- JOB-09's standalone `ui/modules/apps/redfoxTowPortal/portal.html` is also byte-identical to both route entries.
- JOB-04's remaining two website trees contain 272 files each and are byte-identical by relative path.
- No remaining JOB-04 file references the deleted `redfox_recovery` route.
- Combined JOB-04 + JOB-09 + JOB-13 local HTML/CSS references checked: 2,934.
- Missing mod-owned local references: 0.

## Package and syntax checks

For JOB-04 v0.3.2.3.2:

- ZIP entries opened/read: PASS
- Duplicate file paths: 0
- Unsafe/traversal paths: 0
- JSON files parsed: 51 / 51
- JavaScript syntax: 33 / 33
- Lua syntax: 8 / 8

For JOB-09 v0.4.8.0:

- ZIP entries opened/read: PASS
- Duplicate file paths: 0
- Unsafe/traversal paths: 0
- JSON files parsed: 4 / 4
- JavaScript syntax: 2 / 2
- Lua syntax: 2 / 2

## Conclusion

**STATIC COMPATIBILITY PASS.**

The updated JOB-04 v0.3.2.3.2 preserves the known-working v0.3.2.3.1 Wrecking Yard implementation byte-for-byte. The only functional JOB-04 edits are Tow labels/routes, and the only removed content is the obsolete copied Tow website in both mirrors. JOB-09 supplies the unique replacement route separately and has zero file-path overlap with JOB-04 or JOB-13.

This does **not** prove BeamNG runtime behavior. The required runtime gate is:

1. Install only JOB-04 v0.3.2.3.2, JOB-09 v0.4.8.0, and JOB-13 v0.1.8.1 among these jobs.
2. Clear BeamNG WebUI cache and fully restart.
3. Open Wrecking Yard from PC and phone.
4. Purchase one inexpensive Wrecking Yard vehicle and confirm one garage record.
5. Open RedFox Towing from PC and phone.
6. Confirm the Tow public site and Company Portal load.
7. Reopen Auctions from PC and phone.
8. Stop at the first failure and preserve `beamng.log`.

## Important version note

JOB-04 v0.3.2.3.2 is based on the earlier known-working v0.3.2.3.1 line. It intentionally does **not** include the later My Vehicles / Sell / Whole Scrap / Receipts work from v0.3.2.4.x or v0.3.2.5.
