# JOB-04 — RedFox Wrecking Yard v0.2.8

## Runtime closure for v0.2.7

Owner test result: **PARTIAL PASS / REJECTED AS FINAL**.

What worked:
- The direct BeamBook generation/sync path returned a very large number of cars.
- The no-timeout approach allowed the list to complete.

What failed:
- A transient `career_modules_beamBook unavailable` message flashed before the cars arrived.
- Visible cards identified the source/seller as BeamBook instead of RedFox Wrecking Yard.
- Unsuitable stock appeared, including listings around $700,000 and low-mileage/good-quality bargains that did not fit a wrecking yard.
- `Inspect / Buy` started a private-seller location/inspection flow instead of the standard online purchase page.

Decision:
- Preserve BeamBook only as the proven hidden generation source.
- Do not alter BeamBook's own marketplace records.
- Create separate temporary RedFox Wrecking Yard native-shop clones for filtering, branding, pricing, and online purchase.

## Source

- Base ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_0016PT_v0_2_7_DIRECT_BEAMBOOK_NO_TIMEOUT_FROM_v0_2_6.zip`
- Base SHA-256: `643b93d0c7c5fc480f075dc17a3603b5e36079407a5eb081d101a900c1cf7514`
- BeamBook remains a separate enabled mod and is not modified.

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_1051PT_v0_2_8_FILTERED_REDFOX_ONLINE_BUY_NO_FLASH_FROM_v0_2_7.zip`
- SHA-256: `32afdc475a599f1b3b9e8c5c3ae6623b1010f46dbbdd3424ddf88e0ce470b7cf`
- Size: `25,383,218 bytes`
- File count: `961`
- ZIP entries including directories: `1,415`
- Runtime status: **UNPROVEN**

## Exact changes

1. BeamBook still generates and synchronizes its own normal private-sale entries.
2. JOB-04 removes prior temporary `redfoxWreckingYard` clones from the native `vehiclesInShop` table before rebuilding.
3. JOB-04 reads only the original `sellerId == "beambook"` entries as source data.
4. JOB-04 deep-copies eligible source cars into temporary native-shop clones:
   - `sellerId = "redfoxWreckingYard"`
   - `sellerName = "RedFox Wrecking Yard"`
   - unique temporary shop IDs beginning at `5000001`
   - original BeamBook IDs/names are preserved in RedFox metadata fields
5. BeamBook's own listings remain unchanged for its separate BeamBook/Facebook marketplace.
6. Default general-car filter:
   - minimum 100,000 miles
   - original source value no more than $180,000
   - Wrecking Yard price capped at $35,000
7. Default tow/work/special filter:
   - minimum 50,000 miles
   - original source value no more than $750,000
   - Wrecking Yard price capped at $100,000
8. Clone prices use configurable mileage-sensitive yard discounting.
9. Tow, wrecker, rollback, flatbed, recovery, truck, semi, trailer, utility, service-body, crane and similar keywords remain eligible and are visually prioritized.
10. Visible cards use RedFox Wrecking Yard branding only.
11. Card action is now **Buy Online**.
12. Buying sends `RedFoxScrapYardOpenPurchaseMenu` through the existing host bridge, which calls native `career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)`.
13. The Wrecking Yard page no longer calls `career_modules_inspectVehicle.startInspection` and does not start map travel or location inspection.
14. Module readiness is treated as a neutral loading/pending state with one quiet 750 ms retry timer. The transient unavailable error card/text was removed.

## Changed files

- `info.json`
- `sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- `sites/scrap_yard/assets/js/scrap.js`
- `sites/scrap_yard/index.html`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html`
- `OPEN_ME_FIRST_JOB-04_Wrecking-Yard_2026-07-28_1051PT_v0_2_8_FILTERED_REDFOX_ONLINE_BUY_NO_FLASH.txt`
- `OPEN_THIS_VERIFICATION_REPORT_JOB-04_Wrecking-Yard_2026-07-28_1051PT_v0_2_8.html`
- `VERIFY_JOB-04_Wrecking-Yard_2026-07-28_1051PT_v0_2_8_FILTERED_REDFOX_ONLINE_BUY_NO_FLASH.json`

## Protected files confirmed unchanged

- `ui/ui-vue/dist/index.js`
- `ui/ui-vue/dist/index.css`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
- `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js`

The existing host purchase bridge is reused without editing those protected files.

## Static verification

PASS:
- mirrored Wrecking Yard JS identical
- mirrored Wrecking Yard HTML identical
- mirrored Wrecking Yard config identical
- Node JavaScript syntax check
- JSON parse
- changed HTML local references
- no inspection/startInspection path in Wrecking Yard JS
- online purchase bridge present
- RedFox clone seller ID/name present
- original BeamBook source filter present
- temporary-clone cleanup present
- pending state is neutral
- old `career_modules_beamBook is unavailable` flash text removed
- old visible BeamBook seller/card labels removed
- price and mileage limits present in config
- protected host/global files byte-identical to v0.2.7
- ZIP integrity

## Required runtime test

1. Disable v0.2.7 and all older JOB-04/FoxNet test ZIPs.
2. Keep BeamBook enabled.
3. Install this exact v0.2.8 ZIP and fully restart BeamNG.
4. Open IceFox and confirm the welcome page remains fast.
5. Open Wrecking Yard and confirm no red unavailable/error message flashes.
6. Confirm listings identify the seller as RedFox Wrecking Yard, not BeamBook.
7. Confirm general listings stay at or below $35,000 under the default config.
8. Confirm tow/work/special listings stay at or below $100,000 under the default config.
9. Confirm high-mileage/project cars and tow/work vehicles still appear.
10. Click **Buy Online** and confirm the standard native online purchase page opens without teleporting to inspect the vehicle.
11. Complete one inexpensive purchase and verify money, delivery, ownership, inventory and storage.
12. Open BeamBook separately and confirm its original seller names and prices remain unchanged.

## Deferred

- Joe's Junk and Slop Gear mixing
- adjustable 80/10/5/5 source percentages
- actual damage generation
- selling and scrapping

## Workflow incident note

Two accidental empty/temporary GitHub issues (#34 and #35) were created during connector operation and immediately closed as `not planned`. They contain no project work. The active JOB-04 ledger remains issue #30.