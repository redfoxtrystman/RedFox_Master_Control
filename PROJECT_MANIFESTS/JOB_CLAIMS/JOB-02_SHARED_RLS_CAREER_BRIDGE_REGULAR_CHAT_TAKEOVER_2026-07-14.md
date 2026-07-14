# JOB-02 — Shared RLS / Career Bridge — Regular-Chat Takeover Record

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 12:44 PDT (America/Los_Angeles)  
**JOB:** JOB-02 — Shared RLS / Career Bridge  
**Owner:** one active regular ChatGPT JOB-02 chat / Sol, under David / Captain  
**Original Work-chat link:** `https://chatgpt.com/share/6a569142-069c-83e8-b4bf-30a3f6e3179f`  
**Status:** CLAIMED — PARTIALLY RECOVERED — CONTRACT DRAFT FILES MISSING — NO RUNTIME BUILD

## What changed

Ownership continuity for JOB-02 was transferred from the inaccessible ChatGPT Work chat to this replacement regular ChatGPT chat. This record does not create a second JOB-02 owner, rename the job, merge it with another job, or authorize work outside the Shared RLS / Career Bridge lane.

## Why it changed

The RedFox/FoxNet project chats were unintentionally created as ChatGPT Work chats. David was not aware that the coordinated project was subject to a separate Work-chat usage limit. On July 14, 2026, the original chats became inaccessible and showed that access would remain blocked until July 20, 2026. Development across coordinated jobs was interrupted and each job now requires manual transfer, context reconstruction, ownership revalidation, and selective file reupload.

This causes duplicate-work risk, loss-of-context risk, coordination problems, and unnecessary delay. The incident is preserved for inclusion in a report to OpenAI and is not being minimized as ordinary planned migration work.

## Shared-chat recovery result

The supplied ChatGPT share URL could not be fetched by the available web reader and returned a cache/fetch failure. Therefore:

- the full Work-chat transcript was not recovered;
- chat-only attachments were not recovered;
- hidden tool activity and local generated files were not recovered;
- no claim is made that the previous conversation was fully read.

Recovery instead used the GitHub repository, existing project conversation continuity, committed JOB-02 records, and JOB-01 draft PR evidence.

## GitHub state successfully recovered

The following JOB-02 records exist on `main` and do not need reuploading:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-00_BASELINE_FREEZE_INPUT_2026-07-14.md
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
INCIDENT_REPORTS/2026-07-11_ScrapYard_Direct_RLS_Path_Ignored_Custom_Bridge_Failure.md
INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md
INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md
INCIDENT_REPORTS/2026-07-14_ChatGPT_Work_Chat_Project_Lockout_And_Regular_Chat_Migration.md
INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md
```

JOB-01 draft PR `#3`, branch `agent/job01-platform-core-v0-1`, also preserves the current platform boundary and host contract:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_JOB-02_BRIDGE_BOUNDARY.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PHONE_PC_HOST_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_ROUTE_AND_DESTINATION_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_APP_MANIFEST_CONTRACT.md
```

The JOB-01 contract ID is `job01.platform.v1`. It reserves `job02.bridge.v1` for JOB-02 after JOB-02 publishes an exact versioned bridge contract and commit. JOB-01 v0.2 currently implements no Career action forwarding.

## Most recent known JOB-02 development status

The latest committed JOB-02 status is the baseline-freeze input commit:

```text
b9fc5c3ec8a7ec2903ac7b1cfbddd5873f9d9079
```

That record states the previous JOB-02 chat had prepared the following files locally:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CONTRACT_v0.1.0-draft.1.md
PROJECT_MANIFESTS/SCHEMAS/JOB-02_SHARED_RLS_CAREER_BRIDGE_SCHEMA_v0.1.0-draft.1.json
PROJECT_MANIFESTS/TEST_FIXTURES/JOB-02_SHARED_RLS_CAREER_BRIDGE_FIXTURES_v0.1.0-draft.1.json
```

All three paths return `404 Not Found` on GitHub. They were not committed and are currently missing.

The prior status claimed only static draft validation:

- JSON schema compiled successfully;
- nine valid fixtures were accepted;
- ten prohibited or invalid fixtures were rejected;
- protected-path scan found no platform, RLS core, or app files;
- no Lua runtime implementation was produced;
- no ZIP was produced;
- runtime remained unproven.

Therefore the current honest status is:

```text
PARTIAL — CONTRACT DRAFT PREPARED PREVIOUSLY BUT NOT RECOVERED
BLOCKED — REQUIRED LOCAL DRAFT FILES AND BINARY BASELINES NOT PRESENT IN THIS CHAT
NO RUNTIME IMPLEMENTATION OR TEST BUILD EXISTS
```

## Recovered RLS / Career API evidence

The previous JOB-02 inspection recorded these RLS Career Overhaul 2.6.6 interfaces:

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

Contract restrictions already established:

- `updateVehicleList(true)` may be explicit and throttled only; never startup-loaded or repeatedly timer-driven;
- `openPurchaseMenu("instant", shopId)` proves only that the stock/RLS purchase menu was requested, not that purchase completed;
- inventory sell must use the existing Career inventory path and may not accept a custom JOB-02 price;
- JOB-02 must not spawn a vehicle, create ownership/storage, manipulate money, or create a custom Scrap Yard Career module;
- phone and PC must use identical backend operation names and payloads;
- failed or unavailable results must not be translated into success.

## Exact files David must reupload

### Required now

1. `rls_career_overhaul_2.6.6.zip`  
   Expected size: `40,035,328` bytes  
   Expected SHA-256: `b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b`  
   Reason: authoritative RLS/Career source evidence for verifying actual vehicle-shopping, inventory, UI-to-Lua, and extension-loading interfaces.

2. `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_RLS_SHOPDATA_ON_EXISTING_BRIDGE_STATIC(2).zip`  
   Expected size: `24,370,607` bytes  
   Expected SHA-256: `284d10c0ad3221f52a718878866f57d218ecd354a8f181136fc44251c85b397d`  
   Reason: behavioral reference for the previously functioning shop-data path and for identifying legacy bridge behavior that must not be copied into the modular bridge.

3. `JOB-02_SHARED_RLS_CAREER_BRIDGE_CONTRACT_v0.1.0-draft.1.md`, if it was downloaded or saved locally.  
   Reason: preserves the exact previous contract wording and avoids reconstructing it from summaries.

4. `JOB-02_SHARED_RLS_CAREER_BRIDGE_SCHEMA_v0.1.0-draft.1.json`, if it was downloaded or saved locally.  
   Reason: preserves the previously compiled schema and exact accepted/rejected payload rules.

5. `JOB-02_SHARED_RLS_CAREER_BRIDGE_FIXTURES_v0.1.0-draft.1.json`, if it was downloaded or saved locally.  
   Reason: preserves the recorded nine valid and ten prohibited/invalid fixture cases.

If files 3 through 5 do not exist outside the locked Work chat, JOB-02 will reconstruct them from the committed API evidence and publish a clearly labeled replacement draft rather than pretending the original files were recovered.

### Helpful later, not required for initial contract recovery

- Exact JOB-01 v0.2 generated test ZIP with expected SHA-256 `ba0ac46f5fefa0b3e59be2a651fcc32582a811f525a669d6ca47c8a86c3aa446`, for host-to-bridge integration testing after the contract is published.
- Any JOB-02 local validation scripts, console output, protected-path scan report, or draft verification report from the old chat.
- Any screenshots or `beamng.log` evidence showing the old v0.10.3 bridge requesting shop data or opening the RLS purchase menu.
- A current installed-mod list or folder inventory for the exact test environment, to prevent duplicate FoxNet/RLS packages from contaminating results.

## Files that do not need reuploading

- The JOB-02 claim, platform-boundary handoff, and baseline-freeze input listed above.
- JOB-01 PR #3 source and contracts; they are available through GitHub even though the PR is draft and unmerged.
- Project-wide incident, migration, architecture, job-board, and safety documentation already committed.
- Broken Scrap Yard Direct packages are not requested and must not be used as JOB-02 implementation bases.

## Known problems and incomplete features

- The three previously prepared JOB-02 draft files are missing from GitHub.
- No canonical baseline-freeze decision from JOB-00 was found after JOB-02's input commit.
- No dedicated JOB-02 Lua adapter exists.
- No UI-to-Lua transport binding to `job01.platform.v1` exists yet.
- No purchase-completion result callback has been proven; opening the purchase menu cannot be reported as a completed purchase.
- No runtime contract handshake, capability response, idempotency behavior, or transaction result logging has been tested.
- No phone-versus-PC parity test has been run for Career/RLS operations.
- No non-West-Coast map test exists for JOB-02.
- No JOB-11 runtime verdict exists for a JOB-02 build because no build exists.

## Ownership boundaries preserved

JOB-02 owns only the shared UI-to-Lua Career/RLS contract, validation, result/error model, adapter, compatibility rules, and bridge logging. JOB-02 will not modify phone or PC shells, browser/navigation/registry code, app-owned pages, stock RLS Career modules, money, inventory ownership, garage/storage, insurance, or another job's implementation.

## Next concrete action

After the required files are available, JOB-02 will:

1. verify the two ZIP identities by size, SHA-256, and ZIP integrity;
2. recover or reconstruct the missing draft contract, schema, and fixtures;
3. compare every operation against the exact RLS 2.6.6 source interfaces;
4. publish `job02.bridge.v1` as a reviewable contract packet on GitHub;
5. keep runtime implementation blocked until the contract is committed and JOB-00/JOB-01 boundary dependencies are confirmed;
6. then build the smallest removable add-on adapter without copying or patching RLS core files.

## Files affected by this GitHub change

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
```

No BeamNG mod source, RLS source, phone/PC files, app pages, generated ZIPs, or other job-owned files were changed by this takeover record.
