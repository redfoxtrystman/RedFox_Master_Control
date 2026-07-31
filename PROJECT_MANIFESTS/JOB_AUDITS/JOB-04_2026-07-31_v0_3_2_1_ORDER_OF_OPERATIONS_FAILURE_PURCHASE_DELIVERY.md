# JOB-04 v0.3.2.1 — Order-of-Operations Failure Report

**Date:** 2026-07-31  
**Owner:** JOB-04 — Wrecking Yard + FoxNet Welcome Hub  
**Status:** RUNTIME FAILURE CONFIRMED — PURCHASE TEST INSTRUCTION WAS INVALID

## Runtime result

David confirmed that a Wrecking Yard purchase did not ship to a garage and instead spawned beside the player.

## Exact archives reviewed

### v0.3.2 visual/performance baseline

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_2120PT_v0_3_2_JUNK_FOCUSED_JOES_UNDESIREABLES_FROM_ICON_v0_3_1.zip`

SHA-256: `874f817f61bf7c32498d92f0a29d2c34ff1b5d6a01203a3ec94729d86e03cf76`

### v0.3.2.1 Step 01 cleanup build

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_1_STEP01_TEMP_BACKUP_UNUSED_PAGES_RECORDS_FROM_v0_3_2.zip`

SHA-256: `c709444eb71f088a97eb25a04f9d572d81eab5c83609e76f1491c7f9b76bb129`

### v0.3.4 reference that actually contains the garage-delivery adapter

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1430PT_v0_3_4_NATIVE_PURCHASE_FORCED_GARAGE_DELIVERY_FROM_v0_3_3.zip`

SHA-256: `e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75`

## Confirmed technical cause

The Step 01 cleanup preserved all live v0.3.2 files byte-for-byte. That preserved the good welcome page, correct FoxNet icon, fast loading, junk inventory and original purchase path. It also preserved the v0.3.2 purchase limitation.

The active v0.3.2/v0.3.2.1 flow:

1. Posts `RedFoxScrapYardOpenPurchaseMenu`.
2. Writes `redfoxForceGarageDeliveryPurchase` and `redfoxForceGarageDeliveryShopId` to browser session storage.
3. No active code reads those values.
4. Directly calls `career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)`.
5. Does not force `options.makeDelivery = true` on the native purchase submission.

The Step 01 archive does not contain:

`lua/ge/extensions/redfoxWreckingYardPurchase.lua`

The later v0.3.4 archive contains that adapter. It explicitly sets:

`forcedOptions.makeDelivery = true`

and the v0.3.4 Wrecking Yard JavaScript invokes that adapter.

Therefore Step 01 did not newly remove the garage-delivery repair. The selected v0.3.2 baseline never contained the later repair.

## Confirmed order-of-operations failures

### 1. Baseline capability gate was not enforced

Before Step 01, the assistant had already identified that v0.3.2 predates the forced-garage adapter and initially advised against using it for purchase testing. That limitation should have remained a hard build gate.

### 2. Final test instructions contradicted the known limitation

The cleanup build was correctly limited to moving unused files. However, the final delivery instructions told David to test one inexpensive purchase as though the archive contained the v0.3.4 delivery fix. It did not.

### 3. Required-feature matrix was not checked before delivery

A pre-delivery matrix should have shown:

- Welcome page: present
- Correct icon: present
- Junk inventory: present
- Fast loading: present
- Native varied prices: present
- Garage-delivery adapter: absent
- Selling/scrapping/returned parts: absent

The missing garage-delivery adapter should have blocked the purchase test instruction.

### 4. Post-edit verification proved parity but not required behavior

The verification confirmed that Step 01 matched v0.3.2. That was useful for cleanup safety but insufficient for purchase testing. It did not require:

- active `redfoxWreckingYardPurchase.lua`
- active `makeDelivery = true`
- active adapter invocation from the live Wrecking Yard JavaScript
- completion callback and garage-assignment path

### 5. Runtime test gate failed

David confirmed the exact previously known failure: the vehicle spawned near the player rather than being delivered to a garage.

## Status decisions

- v0.3.2: KEEP as the last confirmed good visual/performance/junk-inventory baseline.
- v0.3.2.1: KEEP only as a cleanup experiment; REJECT for purchase testing.
- v0.3.4: reference source for the garage-delivery adapter only; not automatically accepted as the new full baseline.
- No replacement ZIP is authorized by this report.

## Mandatory order of operations before the next ZIP

1. Freeze exact source and rollback hashes.
2. Approve a narrow purchase-repair-only scope.
3. Compare all active purchase-related files in v0.3.2.1 and v0.3.4 before editing.
4. Record the exact files allowed and forbidden to change in GitHub before the build.
5. Port only the verified native garage-delivery adapter and required caller changes.
6. Verify the active archive contains:
   - `redfoxWreckingYardPurchase.lua`
   - `makeDelivery = true`
   - live Wrecking Yard JavaScript adapter invocation
   - native shop-ID preservation
   - no manual money subtraction
   - no manual inventory insertion
   - no manual loose-vehicle spawn path
7. Verify the welcome page, icon, styling, junk selection and performance files remain unchanged.
8. Run the purchase adapter harness for Purchase, Cancel, invalid ID, duplicate click and native-function restoration.
9. Extract the final ZIP to a fresh folder and rerun all checks against the packaged files.
10. Give David exactly one inexpensive purchase test with stop conditions:
    - money deducted once
    - purchase screen closes
    - vehicle appears once in Career inventory
    - vehicle has a real garage location
    - no loose duplicate remains beside the player

## Compliance acknowledgment

This incident is a confirmed failure to follow the required order of operations. The archive integrity and cleanup checks were completed, but the assistant failed to connect the known baseline limitation to the final runtime test instructions. That caused avoidable owner testing and reintroduced a known failure.
