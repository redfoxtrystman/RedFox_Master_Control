# JOB-04 v0.3.2.2 — Step 02 Purchase Repair

**Status:** BUILT — STATIC/HARNESS VERIFIED — BEAMNG RUNTIME UNPROVEN

## Source

- Base: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_1_STEP01_TEMP_BACKUP_UNUSED_PAGES_RECORDS_FROM_v0_3_2.zip`
- Base SHA-256: `c709444eb71f088a97eb25a04f9d572d81eab5c83609e76f1491c7f9b76bb129`
- Adapter reference: v0.3.4 `lua/ge/extensions/redfoxWreckingYardPurchase.lua`

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_2_STEP02_PURCHASE_REPAIR_FORCED_GARAGE_FROM_v0_3_2_1.zip`
- SHA-256: `55668d13385ad996ce0f1b160a9fbb8484e7757489f593ca3f08266a0de33481`
- ZIP bytes: `25,594,891`
- Internal files: `1,026`
- Duplicate paths: `0`
- Unsafe paths: `0`

## Scope

Purchase repair only. The confirmed v0.3.2 icon, welcome page, fast junk inventory, native prices, mileage, negotiation, browser shell and Step 01 backup layout remain unchanged.

Active changed files:

```text
info.json
sites/scrap_yard/assets/js/scrap_v032.js
sites/scrap_yard/index_v032.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap_v032.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index_v032.html
```

Added active file:

```text
lua/ge/extensions/redfoxWreckingYardPurchase.lua
```

Original versions of all five changed files are preserved byte-for-byte under:

```text
REDFOX_TEMP_BACKUP_DO_NOT_LOAD/STEP_02_PURCHASE_REPAIR_ORIGINALS/
```

## Repair

The page now calls the verified native purchase adapter directly through `bngApi.engineLua`. The adapter finds the real listing by native `shopId`, temporarily wraps native Purchase and Cancel, opens the normal `instant` purchase menu, copies the native options table, sets only `makeDelivery=true`, preserves insurance/trade-in/other options, and restores all native functions before native purchase execution or on Cancel/failure/unload.

No manual money, spawn, inventory insertion, garage selection or menu-closing code was added.

## Verification

- 35/35 packaged hash, mirror, ZIP, path, marker, JSON and protected-file checks passed after fresh extraction.
- Both live JavaScript mirrors pass Node syntax checking.
- JavaScript harness proved direct adapter invocation and duplicate-click blocking.
- Lua harness passed JSON bridge, missing ID, missing listing, valid Purchase, numeric/string shop IDs, `makeDelivery=true`, option preservation, caller-table non-mutation, exactly-one native buy call, failed-open restoration, Cancel restoration, superseded request cleanup and unload cleanup.
- Correct owner icon, welcome page, browser shell, phone relay and global Vue bundle hashes match v0.3.2.1.

## Runtime gate

Test one inexpensive purchase only. Pass requires: menu opens once, closes after Purchase, no loose vehicle beside player, exactly one Career inventory record, valid garage assignment, one money deduction and one listing removal. Stop after the first failure and preserve `beamng.log`.
