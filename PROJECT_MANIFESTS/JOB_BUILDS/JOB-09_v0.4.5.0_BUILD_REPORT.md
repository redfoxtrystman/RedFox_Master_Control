# JOB-09 v0.4.5.0 Build Report

**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Owner:** David / Captain  
**Build time:** 2026-08-01 11:11 PT  
**Status:** BUILT — STATIC PASS — RUNTIME UNPROVEN

## Owner direction

Use the game and RLS systems that already generate repo vehicles and finalize purchased vehicles instead of reconstructing partial Career records. Keep v0.4.4.9 only as a disposable-test-save repair experiment for existing broken vehicles. The next normal version must exclude that repair control.

## Source

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_9_FullNativeLifecycleStoredVehicleRepairRuntimeSlim.zip
Bytes: 908,890
SHA-256: 5fe0f2be81a02f6cab49b83ad341d0fd5bd2624a43154ffe0ca6ebe35a6f36d1
```

## Output

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_0_NativeRepoGenerationPurchaseFinalizationRuntimeSlim.zip
Bytes: 904,138
SHA-256: fce8acd452f03eb807caf1e1fab070e270c9a3263506a55aff97f5cffc76afef
Archive members: 16
```

## Architecture

### Tow generation and custody

- Uses installed eligible vehicle configurations from `util.configListGenerator`.
- Uses the native weighted selection behavior for the filtered candidate pool.
- Spawns an actual game vehicle.
- Captures the exact live configuration, paints, plate, mileage/year where available, and part conditions before the tow target is removed.
- Tow-yard custody remains virtual until legal claim/garage delivery.

### Legal claim and garage delivery

- Spawns the exact stored vehicle and reapplies its saved conditions.
- Passes that actual world object to `career_modules_inventory.addVehicle`.
- Waits for native `onVehicleAdded`, part-inventory generation, `onAddedVehiclePartsToInventory`, vehicle-shopping finalization, and `onVehicleAddedToInventory`.
- Uses the native insurance hook to create a real uninsured record.
- Moves the same inventory ID to the linked purchased RLS garage.
- Verifies the first native save, stores the physical object through native inventory handling, then verifies a second save.
- Deletes the Tow Company source record only after both verification stages pass.
- Rolls back or retains the source record on failure instead of knowingly creating a duplicate.

### Purchase-context isolation

The current RLS vehicle-shopping finalizer keeps purchase data in private Lua upvalues. JOB-09 assigns a zero-cost Tow Company context for the exact target and clears it after completion/failure. Delivery is blocked while a normal vehicle inspection/purchase is active. If the required native finalizer/debug access is unavailable, the transaction fails safely before ownership conversion.

## Deliberately excluded

- The v0.4.4.9 **Audit & Repair Next Stored Vehicle** control.
- Automatic repair of legacy partial inventory records.
- Forced custom thumbnail generation. Native RLS may use the configuration preview, whose paint can differ from the actual vehicle.
- Stock/RLS Career override files.

## Changed runtime files

```text
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
```

Ten runtime files remain byte-identical to v0.4.4.9. The archive contains the same 16 paths as the source.

## Static verification

```text
ZIP integrity: PASS
Lua parse: PASS via liblua5.4 luaL_loadfilex
JavaScript syntax: PASS via node --check
JSON parse: PASS
Path parity: PASS
Duplicate ZIP members: NONE
Forbidden Career/RLS override paths: NONE
Junk, backup, or temporary files: NONE
```

## Runtime gate

Test on West Coast USA with only one JOB-09 version enabled. First use v0.4.4.9 separately for the old-car repair experiment. Then fully close BeamNG, remove v0.4.4.9, install v0.4.5.0, and run one fresh lien-capable tow through claim, linked-garage delivery, Insurance, parts, and two reloads.

Do not promote the cross-job master-help draft to proven guidance until this exact lifecycle passes runtime testing.
