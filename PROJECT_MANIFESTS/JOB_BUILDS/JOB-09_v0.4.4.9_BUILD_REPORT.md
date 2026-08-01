# JOB-09 v0.4.4.9 Build Report

**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Owner:** Captain David  
**Status:** BUILT — STATIC PASS — RUNTIME UNPROVEN  
**Related cross-job issue:** #44

## Archive identity

```text
Source:
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_8_ChangeableOwnedGarageMapSelectorForceFullDeliveryRuntimeSlim.zip
Bytes: 897,747
SHA-256: cdf7aebdaaeb47a8b8a61157eacdf27b249acf478a4fd5ad02dd0f4156f3006e

Output:
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_9_FullNativeLifecycleStoredVehicleRepairRuntimeSlim.zip
Bytes: 908,890
SHA-256: 5fe0f2be81a02f6cab49b83ad341d0fd5bd2624a43154ffe0ca6ebe35a6f36d1

Exact source patch:
JOB09_v0_4_4_9_EXACT_SOURCE.patch
SHA-256: 74d36ef6ef4445bfa07dd821c2998d3f300f466267efb250524b3f93cbca7ff7
```

## Owner request

Attempt to repair the partial JOB-09 vehicles in the disposable Profile 3 test save. Preserve the same inventory IDs and avoid duplicates. If a vehicle cannot be repaired safely, leave it available for the owner to sell and move on. If the architecture passes runtime testing, promote it into a reusable master roadmap for other vehicle-producing jobs.

## Implemented changes

### Full tow-intake snapshot

Before abandoned/unpaid lien custody finalization, JOB-09 now captures the actual live vehicle's:

- JBeam/model;
- full Career configuration table;
- canonical configuration identity;
- paints;
- license plate;
- mileage/odometer;
- year/native configuration metadata;
- part conditions and damage state available through the vehicle bridge.

The invoice/custody step waits for the snapshot instead of deleting the vehicle first.

### Full native ownership lifecycle

Garage delivery no longer treats a fixed one-second delay as proof of completion. It now:

1. spawns the exact stored configuration and paint;
2. applies stored part conditions before registration;
3. creates one Career inventory ID;
4. waits for canonical configuration, part conditions, `originalParts`, and `changedSlots`;
5. creates a valid uninsured insurance record;
6. assigns the selected linked garage while the physical object still exists;
7. requests a generated thumbnail;
8. forces and verifies the first save;
9. stores/removes the physical object;
10. forces and verifies a second save;
11. deletes the Tow Company source record only after final read-back succeeds.

### Existing partial-record repair

Added **Audit & Repair Next Stored Vehicle** to the legacy and Web Portal inventory views.

The repair path:

- considers only incomplete RedFox-tagged Career records;
- preserves the same inventory ID;
- spawns the same inventory record;
- re-runs missing native part lifecycle work;
- rebuilds a valid uninsured entry from the exact vehicle, not another inventory record;
- generates a thumbnail;
- saves, stores, saves again, and verifies the saved files;
- does not create a duplicate replacement after failure.

Expected first candidates in the supplied save are inventory IDs 11 and 33.

### Other corrections

- Replaced the stale company-transfer safety-lock warning with the actual same-inventory transfer behavior.
- Added lifecycle status/candidate count to the Tow Portal.
- Added v0.4.4.9 cache-busting to the portal HTML, JavaScript and CSS loading path.
- Preserved the exact 16-file runtime layout; no stock/RLS Career override path was added.

## Exact changed files

```text
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/app.js
ui/modules/apps/redfoxTowPortal/app.json
ui/modules/apps/redfoxTowPortal/assets/css/portal.css
ui/modules/apps/redfoxTowPortal/assets/js/portal.js
ui/modules/apps/redfoxTowPortal/portal.html
```

Eight other runtime files are byte-identical to v0.4.4.8.

## Static verification

```text
ZIP integrity: PASS
Lua parse: PASS via texlua loadfile
JavaScript syntax: PASS via node --check
JSON parsing: PASS
Archive member parity: PASS, same 16 runtime paths
Forbidden Career/RLS override paths: NONE
Backup/junk files: NONE
```

## Runtime gate

This build is not approved or proven until Captain verifies:

1. inventory ID 11 repairs in place;
2. no duplicate Daytona is created;
3. Insurance recognizes the vehicle as uninsured;
4. the generated thumbnail reflects the actual vehicle and persists;
5. parts editing works without the prior Lua failure;
6. save/reload does not lose or duplicate the vehicle;
7. inventory ID 33 can be repaired;
8. one fresh lien tow completes the full snapshot and native delivery path.

## Reusable roadmap

Draft only:

```text
PROJECT_MANIFESTS/MASTER_HELP/REDFOX_MASTER_HELP_NATIVE_VEHICLES_AND_NO_LAG_DRAFT.md
```

Promote the draft only after the runtime gate passes.
