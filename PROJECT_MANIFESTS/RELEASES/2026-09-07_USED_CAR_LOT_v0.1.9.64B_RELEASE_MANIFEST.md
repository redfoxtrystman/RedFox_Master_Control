# RedFox Used Car Lot v0.1.9.64B Release Manifest

**Status:** BUILT — RUNTIME UNTESTED  
**Date:** 2026-09-07

## Baseline

- `RedFox_Used_Car_Lot_v0_1_9_64A_FULL_ROOT_SAFE--------V_0.39.4.zip`
- SHA-256: `720055ed8b55f417f427f99fff102b92d7d9fbe1c93abc5b42d1c26ffff7fe86`

## Output

- `RedFox_Used_Car_Lot_v0_1_9_64B_FIRST_COUNTER_ASK--------V_0.39.4.zip`
- Size: `108695` bytes
- SHA-256: `fe428fa728226487e61fcb8803e3f8f727002dde7b84a4bdae848ddf60b94430`

## Exact changed paths vs 64A

- `ui/modModules/redfoxUsedCarLot/redfoxUsedCarLot.js`
- `mod_info/RedFoxUsedCarLot/info.json`

## Owner-requested change

The first seller counter now defaults to the exact vehicle asking price. It no longer starts below asking price. Existing later counter suggestions remain the prior $50/$100/$150 downward behavior.

## Protected / verified

- `scripts/redfox_used_car_lot/modScript.lua` byte-identical to 64A.
  - SHA-256: `62bcc000e3ef3a9475ec130ab6544e31c0bfb7eea6584bf2b075153f18a97560`
- `lua/ge/extensions/redfoxUsedCarLotUiRoutes.lua` byte-identical to 64A.
  - SHA-256: `12b935ed2c837fdabcee24c46091687442f3767fdda240e52a5ebaff5aba1435`
- No Car Lot Lua/backend, HTML, CSS, images, startup, or PC-route behavior changed in 64B.
- Final ZIP has direct runtime roots and no wrapper directory.

## Static verification

- ZIP CRC/integrity: PASS
- Duplicate ZIP entries: 0
- Lua `loadfile`: PASS
- JavaScript `node --check`: PASS
- `mod_info` JSON parse: PASS
- Runtime: UNTESTED until David tests the exact SHA above.

## Focused runtime gate

1. Career PC still shows Used Car Lot.
2. Open one new buyer offer.
3. Confirm the first seller counter field equals the exact asking price.
4. Counter once and confirm a later suggested counter steps downward rather than jumping upward.

## Rollback

Remove/disable 64B and reinstall the exact 64A baseline listed above.