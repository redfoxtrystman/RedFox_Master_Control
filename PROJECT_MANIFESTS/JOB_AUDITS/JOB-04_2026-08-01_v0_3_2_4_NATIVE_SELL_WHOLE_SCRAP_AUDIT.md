# JOB-04 v0.3.2.4 — My Vehicles, Native Sell, and Whole-Vehicle Scrap Audit

**Date:** 2026-08-01  
**Owner:** JOB-04 — RedFox Wrecking Yard / FoxNet Welcome Hub  
**Runtime source accepted by David:** v0.3.2.3 website-preserving cleanup

## Locked source

- Source ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_3_STEP03_KEEP_ALL_WEBSITES_REMOVE_RECORDS_FROM_v0_3_2_2.zip`
- Source SHA-256: `8b238d50b3254b336c9665cd712082cae5e81cd16fab67e79dc6e8614f39ca48`
- Owner result: Wrecking Yard works; other retained pages are backed up and may be handed to their owning chats later.

## Final artifact

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-01_v0_3_2_4_STEP04_MY_VEHICLES_NATIVE_SELL_WHOLE_SCRAP_FROM_v0_3_2_3.zip`
- SHA-256: `d6f6795a84acddd694b8ea1a8f76b490e10aa51bc58a2e7891c26a318558499a`
- Size: 16,969,119 bytes
- Files: 835
- Status: **STATIC/HARNESS VERIFIED — BEAMNG RUNTIME TEST REQUIRED**

## Narrow implemented scope

1. Added a lazy `My Vehicles & Scrap` section.
2. Owned Career/RLS inventory is requested only after that section is opened.
3. Basic cards show exact inventory ID, vehicle name, estimated native value, mileage, storage location, and thumbnail/fallback.
4. **Sell Vehicle** calls the native Career/RLS inventory sale API using the exact inventory ID.
5. The wrapper does not rewrite the native sale price and does not manually credit sale money.
6. The native sale is accepted only after the exact inventory record is verified absent.
7. **Scrap Whole Vehicle** calculates and displays a lower scrap quote.
8. Whole scrap removes the exact inventory record before one payout is attempted.
9. Persistent request IDs and transaction checkpoints prevent duplicate removal and duplicate payout.
10. A failed whole-scrap payout is retained as a pending transaction with one controlled retry action.

## Deliberately deferred

- installed-parts enumeration
- Strip & Scrap Shell
- Returned Parts storage
- Sell Part
- Scrap Cat / catalytic-converter processing
- auction export
- browse-inventory tuning
- purchase/delivery changes
- Welcome Page changes beyond routing Wrecking Yard to the new versioned page
- changes to other website implementations

The old v0.3.3 build enumerated installed parts for every owned vehicle while loading its dashboard. That work was removed from this pass to avoid reintroducing the previous lag risk.

## Native sale verification basis

The current public RLS inventory source at commit `e31433e5c2ed6e4780ac1d0daf94f9780669f47d` exposes:

- `career_modules_inventory.sellVehicleFromInventory(inventoryId)`
- `career_modules_inventory.sellVehicle(inventoryId)`

The native sale path calculates native value, triggers the sale hook, credits Career money, removes the exact inventory record, logs, and saves. Its UI wrapper does not provide a useful success return, so JOB-04 verifies the before/after inventory record instead of trusting the return value.

## Changed-file boundary

Exactly seven existing files changed:

- `info.json`
- `lua/ge/extensions/redfox/career/scrapyardBridge.lua`
- `lua/ge/extensions/redfox/career/scrapyardCef.lua`
- `lua/ge/extensions/redfox/career/scrapyardStorage.lua`
- `assets/js/icefox_front.js` — route string only
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js` — route string only
- `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js` — route string only

Exactly six new files were added: versioned HTML, JavaScript, and CSS in both required Wrecking Yard mirrors.

No source file was removed.

Full manifest:
`JOB-04_v0.3.2.4_CHANGED_FILES_MANIFEST.csv`

## Protected behavior/hash verification

The following remained byte-identical to v0.3.2.3:

- Welcome Page root
- owner-selected FoxNet/Wrecking Yard card image
- global Vue bundle
- `lua/ge/extensions/redfoxWreckingYardPurchase.lua`
- accepted v0.3.2.2/v0.3.2.3 purchase adapter behavior
- old `index_v032.html` and `scrap_v032.js` in both mirrors
- all other website implementation files

All ten website directories remain present in both required site trees. Both entire site trees match byte-for-byte, including the new v0.3.2.4 files.

## Verification results

### Pre-package

- Scope/hash boundary: PASS
- Existing files changed: 7 exactly
- New files: 6 exactly
- Removed files: 0
- JavaScript syntax: PASS
- Lua syntax: PASS
- JSON parsing: PASS
- HTML local references: PASS
- CSS local references: PASS
- Mirror equality: PASS
- Protected hashes: PASS
- No installed-parts enumeration in active bridge: PASS
- No Strip/Returned Parts/Cat UI in v0.3.2.4: PASS
- Wrecking Yard purchase adapter unchanged: PASS

### Transaction harness

- Dashboard returns basic owned vehicles without parts payload: PASS
- Native sale succeeds despite the native wrapper returning `nil`, but only when inventory removal is verified: PASS
- Native sale replay with the same request ID does not call native sale twice: PASS
- Native sale that fails to remove the vehicle is rejected and does not add custom money: PASS
- Native sale exception preserves the vehicle: PASS
- Whole-scrap quote is positive: PASS
- Whole scrap removes the exact vehicle once: PASS
- Whole scrap pays once: PASS
- Whole-scrap replay does not remove or pay twice: PASS
- Failed payout records a pending transaction after verified removal: PASS
- Pending-payment retry pays once: PASS
- Completed retry cannot pay twice: PASS
- Loaners are excluded and cannot be scrapped: PASS
- A second different request cannot scrap an already removed vehicle: PASS

### Lazy-page harness

- Owned inventory calls before opening `My Vehicles & Scrap`: 0 — PASS
- Dashboard calls after opening it: 1 — PASS
- Dashboard call targets `scrapyardCef`: PASS

### Exact packaged ZIP

- ZIP integrity: PASS
- Unsafe paths: 0
- Duplicate paths: 0
- Final extraction: 835 files
- Fresh extraction matches the pre-package tree byte-for-byte: PASS
- Packaged validation: 781 checks passed
- Packaged transaction harness: 11 checks passed
- Packaged lazy UI harness: PASS

## Records-only backup

- Archive: `RedFox_JOB-04_v0_3_2_4_CHANGED_ORIGINALS_RECORDS_ONLY_2026-08-01.zip`
- SHA-256: `9569787be6905a7281eb412fba463f14efdefbad8bf77e2892cd3ad39ae83a1d`
- Purpose: exact v0.3.2.3 originals for the seven replaced files plus the change manifest
- Installation status: **DO NOT INSTALL IN BEAMNG**

## Required runtime gate

Use a backed-up Career save and disable every older JOB-04 or separate Browser Core test ZIP.

1. Confirm Career, FoxNet, Welcome Page, and Wrecking Yard browse/purchase still operate normally.
2. Open `My Vehicles & Scrap`; confirm it opens without a lag spike.
3. Choose one inexpensive, expendable owned vehicle and test **Sell Vehicle**.
4. Confirm the vehicle disappears once and Career money changes once by the native sale amount.
5. Restart/reopen the page and confirm the sold vehicle remains absent.
6. Choose a second inexpensive, expendable vehicle and test **Scrap Whole Vehicle**.
7. Confirm the displayed quote, exact vehicle removal, no returned parts, and one payout.
8. Reopen/restart and confirm no duplicate payout and no reappearing vehicle.
9. Stop on the first failure and preserve `beamng.log` and the save backup.

Do not begin Strip/Parts/Catalytic Converter restoration until both native sale and whole-vehicle scrap pass this exact runtime gate.
