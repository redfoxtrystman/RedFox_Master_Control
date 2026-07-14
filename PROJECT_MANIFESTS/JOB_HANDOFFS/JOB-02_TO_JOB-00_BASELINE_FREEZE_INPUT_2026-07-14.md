# JOB-02 to JOB-00 — Baseline Freeze Input

**Date:** 2026-07-14  
**From:** JOB-02 — Shared RLS / Career Bridge  
**To:** JOB-00 — Coordinator / Integration / Verification  
**Status:** INPUT FOR COORDINATOR DECISION — NOT A FROZEN BASELINE

## Purpose

JOB-00 is now officially claimed. This handoff provides the exact package identities JOB-02 inspected so JOB-00 can approve or reject them as the canonical source baseline. JOB-02 does not freeze the project baseline.

## Exact packages inspected by JOB-02

| Role | Local/uploaded filename | Size (bytes) | SHA-256 |
|---|---|---:|---|
| RLS/Career source evidence | `rls_career_overhaul_2.6.6.zip` | 40,035,328 | `b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b` |
| Current RedFox behavioral reference | `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_RLS_SHOPDATA_ON_EXISTING_BRIDGE_STATIC(2).zip` | 24,370,607 | `284d10c0ad3221f52a718878866f57d218ecd354a8f181136fc44251c85b397d` |

The `(2)` suffix is a local duplicate-download suffix. The content hash, not that suffix, identifies the package.

Both archives passed ZIP integrity inspection during JOB-02 baseline analysis.

## JOB-02 findings that affect the freeze

The RedFox v0.10.3 package is a behavioral reference only. It must not be adopted as the new modular bridge/platform source without separating its copied and overridden shared cores.

It contains or overrides paths including:

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
ui/modModules/backalley/
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
```

It also contains legacy bridge files that JOB-02 rejects as implementation bases:

```text
lua/ge/extensions/redfoxCareerWeb.lua
lua/ge/extensions/redfox/career/scrapyardBridge.lua
```

Those legacy files use custom money, inventory, storage, spawn-as-purchase, or arbitrary method-dispatch behavior that conflicts with the owner directive.

## Proven RLS/Career API evidence

JOB-02 inspected these RLS 2.6.6 interfaces:

```text
career_modules_vehicleShopping.updateVehicleList(false)
career_modules_vehicleShopping.updateVehicleList(true)
career_modules_vehicleShopping.getShoppingData()
career_modules_vehicleShopping.getVehicleInfoByShopId(shopId)
career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)
career_modules_inventory.getVehicles()
career_modules_inventory.getVehicleUiData(inventoryId)
career_modules_inventory.sellVehicle(inventoryId)
```

Contract restrictions:

- `updateVehicleList(true)` is explicit and throttled only; never startup or repeated timers.
- `openPurchaseMenu` acknowledges a stock/RLS menu request only; it does not prove purchase completion.
- `sellVehicle(inventoryId)` receives no custom price.
- No JOB-02 operation spawns a vehicle, creates ownership/storage, or manipulates money directly.

## Current coordinator decision needed

JOB-00 should publish one baseline-freeze record that states:

1. approved source package filenames;
2. exact sizes and SHA-256 hashes;
3. which package is source evidence versus a build candidate;
4. protected files that no job may copy or overwrite;
5. whether the JOB-01 first build is a separate candidate layered on the frozen source baseline;
6. the exact JOB-01 build/source handoff commit to consume.

## Remaining JOB-01 dependency

Git currently records the first JOB-01 phone/PC build as:

```text
BUILT — RUNTIME UNTESTED / GIT BUILD HANDOFF MISSING
```

JOB-02 still requires JOB-01's committed host transport contract, exact source/patch, build identity, protected-file confirmation, and request/result forwarding behavior before binding the browser host to the Career/RLS bridge.

## JOB-02 prepared contract packet

JOB-02 has prepared locally:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CONTRACT_v0.1.0-draft.1.md
PROJECT_MANIFESTS/SCHEMAS/JOB-02_SHARED_RLS_CAREER_BRIDGE_SCHEMA_v0.1.0-draft.1.json
PROJECT_MANIFESTS/TEST_FIXTURES/JOB-02_SHARED_RLS_CAREER_BRIDGE_FIXTURES_v0.1.0-draft.1.json
```

Static status:

- JSON schema compiled successfully.
- Nine valid fixtures were accepted.
- Ten prohibited/invalid fixtures were rejected.
- Protected-path scan found no platform, RLS core, or app files in the draft packet.
- No Lua runtime implementation or ZIP has been produced.
- All runtime behavior remains unproven.

JOB-02 will publish/promote the versioned bridge contract only after JOB-00 freezes the baseline and JOB-01 publishes the matching shared host contract.
