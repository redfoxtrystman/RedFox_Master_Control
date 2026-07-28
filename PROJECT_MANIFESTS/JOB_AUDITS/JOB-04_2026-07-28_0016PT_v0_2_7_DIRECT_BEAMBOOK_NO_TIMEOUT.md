# JOB-04 — RedFox Wrecking Yard v0.2.7

## Runtime closure for v0.2.6

Owner test result: **FAILED**.

Observed result:
- Wrecking Yard page opened.
- No vehicle cards completed loading.
- The artificial 10-second cutoff fired and displayed the timeout/failure card.

Decision:
- v0.2.6 is rejected as the active test build.
- The custom JOB-04 cached provider/request path is abandoned for now.
- The next build must use BeamBook's own proven generation/sync path directly and must not impose an artificial timeout.

## Source

- Base ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-27_2211PT_v0_2_6_CACHED_BEAMBOOK_STYLE_100_CAR_POOL_FROM_v0_2_5.zip`
- Base SHA-256: `cb4b1b1424fa5c4fea2d44b4bb413ca03beb6e7a2b2ef0162e71609005d8b87a`
- BeamBook reference: `beamBook(2).zip`

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_0016PT_v0_2_7_DIRECT_BEAMBOOK_NO_TIMEOUT_FROM_v0_2_6.zip`
- SHA-256: `643b93d0c7c5fc480f075dc17a3603b5e36079407a5eb081d101a900c1cf7514`
- Size: `25,238,007 bytes`
- ZIP entries: `958`
- Runtime status: **UNPROVEN**

## Architecture change

v0.2.7 removes the JOB-04 custom Wrecking Yard generator and directly uses the installed BeamBook module:

1. Wrecking Yard loads `career_modules_beamBook` if needed.
2. It calls BeamBook's own `onVehicleShoppingMenuOpened({})` hook.
3. BeamBook performs its normal listing generation and sync into `career_modules_vehicleShopping.getVehiclesInShop()`.
4. Wrecking Yard reads the native shopping data and displays only entries with `sellerId == "beambook"`.
5. No JOB-04 vehicle-generation Lua is used.
6. No artificial timeout is used.
7. All returned BeamBook cars are displayed; the old 80/10/5/5 filtering is deferred until the direct path is proven.
8. Cards render in browser batches of 25 only to keep DOM rendering responsive; this does not limit the BeamBook listing count.
9. `Inspect / Buy` calls `career_modules_inspectVehicle.startInspection(target, true)` on the exact BeamBook shop entry.
10. BeamBook's own inspection patch remaps the seller to the native private-seller flow.

## Removed files

- `lua/ge/extensions/career/modules/redfoxWreckingYardInventory.lua`
- `lua/ge/extensions/redfoxWreckingYardInventoryLoader.lua`
- `scripts/redfoxWreckingYardInventory/modScript.lua`

## Changed files

- `info.json`
- `sites/scrap_yard/index.html`
- `sites/scrap_yard/assets/js/scrap.js`
- `sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- `OPEN_ME_FIRST_JOB-04_Wrecking-Yard_2026-07-28_0016PT_v0_2_7_DIRECT_BEAMBOOK_NO_TIMEOUT.txt`
- `VERIFY_JOB-04_Wrecking-Yard_2026-07-28_0016PT_v0_2_7_DIRECT_BEAMBOOK_NO_TIMEOUT.json`

## Protected behavior

- IceFox welcome page still does not request vehicle/shop data.
- Wrecking Yard name, page design, and rotating welcome tile image remain.
- BeamBook remains separate and continues serving the BeamBook/Facebook marketplace.
- No manual money subtraction, ownership insertion, or vehicle spawning was added.
- Selling and scrapping remain deferred.

## Static verification

All passed:

- Mirrored Wrecking Yard JS identical.
- Mirrored Wrecking Yard HTML identical.
- Mirrored config identical.
- No timeout code or 10-second ceiling remains.
- Direct BeamBook hook present.
- Only `sellerId == "beambook"` cars are selected.
- Native inspection call present.
- Custom provider references removed.
- Custom provider, loader, and modScript removed from the ZIP.
- No listing-count cap is applied to BeamBook cars.
- Batch rendering affects DOM work only.
- JavaScript syntax passed with Node.
- Config JSON parsed successfully.
- Changed HTML local references passed.
- ZIP integrity passed.

## Required runtime test

1. Disable older JOB-04/FoxNet test ZIPs.
2. Keep `beamBook(2).zip` or the installed BeamBook mod enabled.
3. Install v0.2.7.
4. Fully restart BeamNG.
5. Open IceFox and confirm the welcome page remains fast.
6. Open Wrecking Yard.
7. Wait for BeamBook normally; no timeout should appear.
8. Confirm all BeamBook cars appear inside Wrecking Yard, including a 100- or 200-car configured list.
9. Click `Inspect / Buy` on one car.
10. Confirm the native BeamBook/private-seller inspection and purchase flow opens.
11. Reopen Wrecking Yard and confirm BeamBook reuses/syncs its existing valid list.

## Next step after runtime result

- If the direct BeamBook path passes, add lower-end/junk weighting and Joe's Junk/Slop Gear sources on top of the proven BeamBook base.
- If it fails, inspect the BeamNG log for `beamBook`, `career_modules_beamBook`, `getShoppingData`, or `startInspection` errors before making another patch.
