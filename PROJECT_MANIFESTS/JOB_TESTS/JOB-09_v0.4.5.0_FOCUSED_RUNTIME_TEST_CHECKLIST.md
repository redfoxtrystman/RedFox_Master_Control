# JOB-09 v0.4.5.0 Focused Runtime Test Checklist

**Build:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_0_NativeRepoGenerationPurchaseFinalizationRuntimeSlim.zip`  
**Status before testing:** BUILT — STATIC PASS — RUNTIME UNPROVEN  
**Recommended map:** West Coast USA  
**Purpose:** Test future tow targets and claimed-vehicle delivery through RLS's native vehicle lifecycle. This build does **not** contain the v0.4.4.9 stored-vehicle repair control.

## Keep the two builds separate

- Use **v0.4.4.9 only** to attempt repair of the already incomplete test-save vehicles.
- Use **v0.4.5.0 only** for a new tow, lien claim, and garage-delivery test.
- Never enable both versions at the same time. They contain the same extension and WebUI paths.
- After the v0.4.4.9 repair attempt, close BeamNG completely before changing ZIPs.

## Before testing v0.4.5.0

1. Return to West Coast USA.
2. Close BeamNG completely.
3. Back up the current Career save.
4. Disable or remove JOB-09 v0.4.4.9.
5. Install only JOB-09 v0.4.5.0.
6. Keep the exact vehicle mods needed by the test target enabled.
7. Do not have a normal dealership/private-sale inspection or purchase open when delivering a Tow Company vehicle.

## Test A — native tow-target generation

1. Start a new abandoned, recovery, accident, or other lien-capable tow.
2. Confirm the target is an installed, usable vehicle configuration selected by the game's eligible-vehicle/configuration system.
3. Complete the tow normally.
4. At invoice/custody completion, confirm JOB-09 reports that it captured the actual vehicle state.
5. Confirm the target is not duplicated or replaced before it reaches the yard.

### Expected result

- The spawned target is a real installed vehicle/configuration.
- JOB-09 preserves its exact model, configuration, paints, plate, mileage/year where available, and part conditions.
- No Career inventory item is created merely because the vehicle entered tow-yard custody.

## Test B — claim and native RLS garage delivery

1. Let the lien/claim become eligible using the normal JOB-09 flow.
2. Claim the vehicle into the Tow Company Garage.
3. Link the exact tow yard to a purchased RLS garage with space.
4. Press the normal delivery control once.
5. Do not change maps, start another purchase, close BeamNG, or press delivery again while native registration is running.
6. Allow up to two minutes.

### Expected native sequence

1. The exact stored vehicle is spawned.
2. Its saved part conditions are applied.
3. RLS adds that actual world vehicle to inventory.
4. Native part inventory creates the installed-parts records.
5. Native vehicle-shopping finalization creates `originalParts`, `changedSlots`, year/history fields, and the inventory-added hook.
6. Native insurance creates a valid uninsured entry.
7. JOB-09 moves the same inventory ID to the linked garage.
8. RLS saves and JOB-09 verifies the saved record.
9. The physical temporary object is stored through native inventory handling.
10. A second save is verified before the Tow Company source record is removed.

### Immediate pass checks

- Exactly one new Career inventory ID exists.
- The Tow Company source record disappears only after the completion message.
- Insurance lists the vehicle as uninsured instead of ignoring it.
- `originalParts` and `changedSlots` exist through normal parts behavior.
- The vehicle is assigned to the selected linked garage.
- No duplicate vehicle appears in the world or inventory.
- No money is charged for converting the legally claimed Tow Company vehicle.

## Test C — parts and persistence

1. Exit to the main menu normally.
2. Reload the save.
3. Confirm the same inventory ID remains exactly once.
4. Confirm Insurance still recognizes it.
5. Confirm it remains in the linked garage.
6. Spawn it and remove/reinstall one small non-structural part.
7. Save and reload again.
8. Only after that passes, test a major part change.

### Persistence pass checks

- No Lua error or infinite loading screen.
- The vehicle survives both reloads.
- Part changes save normally.
- Paint, configuration, mileage, and preserved damage remain as expected.
- The thumbnail may be the configuration's native preview rather than a photograph of the current paint. A red/default preview for a blue car is not by itself a delivery failure.

## Failure handling

- Stop after the first failure and preserve the newest `beamng.log`.
- Do not press delivery repeatedly.
- A failed transaction should retain or restore the Tow Company source record and avoid a duplicate inventory item.
- If an incomplete inventory item remains, record its inventory ID before selling or removing it on the disposable test save.
- Do not reinstall v0.4.4.9 over an active v0.4.5.0 session; fully close BeamNG first.

## Report back

Provide:

- call type and vehicle;
- final Tow Portal lifecycle message;
- new inventory ID;
- whether Insurance recognizes it;
- whether small part removal works;
- whether it survives reload;
- whether a duplicate or leftover Tow Company record exists;
- newest `beamng.log` after any failure.
