# JOB-02 — Shared RLS / Career Bridge — Camping Pause Audit

**Date:** 2026-07-17  
**Timestamp:** 2026-07-17 10:11 PDT (America/Los_Angeles)  
**JOB:** JOB-02 — Shared RLS / Career Bridge  
**Owner:** Shared RLS / Career Bridge regular chat / Sol, under David / Captain  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Audit type:** OWNER-REQUESTED PROJECT PAUSE RECORD — NOT A HANDOFF  
**Pause reason:** David / Captain is leaving for camping and requested every project job to preserve a complete GitHub state record for continuation after he returns.  
**Ownership state:** RETAINED BY THE ACTIVE JOB-02 REGULAR CHAT  
**Current technical status:** PARTIAL / BLOCKED — CONTRACT DRAFTS AND REQUIRED BASELINE ARCHIVES ARE NOT PRESENT; NO RUNTIME BRIDGE BUILD EXISTS

---

## 1. Sound-off

JOB-02 is present, claimed, and paused without transferring ownership.

This job remains exactly:

```text
JOB-02 — Shared RLS / Career Bridge
```

JOB-02 is a cross-mod/shared-system lane. It does not own a standalone marketplace or website mod. It owns the one shared UI-to-Lua Career/RLS operation contract and eventual removable adapter that JOB-01 and the individual app jobs must consume.

This audit is a pause checkpoint only. It does not release the claim, appoint a new owner, authorize another job to modify JOB-02 files, or represent a completed handoff.

---

## 2. Scope owned by JOB-02

JOB-02 owns:

- one shared phone-and-PC UI-to-Lua Career/RLS message contract;
- Career capability and data requests;
- RLS/BeamNG vehicle-shopping data requests;
- requests to open the existing stock/RLS purchase menu;
- owned Career inventory vehicle listing requests;
- requests to use the existing Career inventory sell flow;
- validation, explicit unavailable/failure/success result structures, correlation rules, compatibility/version rules, and bridge logging;
- approved future sponsor, mail, text, tow, reward, or other cross-app bridge operations only after formal review and versioning;
- JOB-02-owned schemas, fixtures, compatibility documentation, tests, verification reports, and eventual dedicated removable bridge adapter.

JOB-02 does not own:

- the RLS phone shell or controller;
- the RLS PC/computer shell;
- the IceFox browser, launcher, navigation, route registry, theme, or responsive host owned by JOB-01;
- the App Store owned by JOB-03;
- Scrap Yard, BeamBook, Import/Export, Classics, Insurance/Finance/Garage/Storage, Tow/Recovery, SponsorHub, FoxMail, FoxText, Visual Design, or QA feature implementations;
- stock RLS/BeamNG Career modules;
- direct money, garage, storage, ownership, insurance, inventory, reward, or save mutation systems.

---

## 3. Work completed before this pause

### 3.1 Original JOB claim and ownership boundaries

The original JOB-02 lane was claimed and documented on 2026-07-13.

Preserved records:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md
```

The boundary states that JOB-01 owns the phone/PC/browser/navigation/registry platform, JOB-02 owns the Career/RLS operation contract and adapter, each app job owns only its app/page, and JOB-00 owns integration approval.

### 3.2 Shared bridge target recorded

The initial operation names preserved on the central job board and claim are:

```text
RedFoxRequestCareerData
RedFoxCareerData
RedFoxOpenVehiclePurchase
RedFoxVehiclePurchaseResult
RedFoxGetOwnedVehicles
RedFoxOwnedVehicles
RedFoxSellInventoryVehicle
RedFoxSellInventoryVehicleResult
RedFoxLogEvent
```

These names remain the working target unless JOB-02 deliberately publishes a versioned replacement. Other jobs must not invent competing Career/RLS operation names.

### 3.3 RLS Career Overhaul 2.6.6 API evidence inspected previously

The inaccessible original Work chat recorded inspection of these interfaces:

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

Existing restrictions preserved from that inspection:

- `updateVehicleList(true)` may be called only by an explicit, throttled request; it must not run at startup or from a repeating timer.
- `openPurchaseMenu("instant", shopId)` proves only that the stock/RLS purchase menu was requested. It does not prove that the player completed a purchase.
- Inventory selling must use the existing Career inventory sell authority and must not accept a custom JOB-02 sale price.
- JOB-02 must not spawn a vehicle as purchase success.
- JOB-02 must not create ownership, insert storage, alter money, or create a custom Scrap Yard Career module.
- Phone and PC callers must use identical backend operation names and payload semantics.
- A failed, unavailable, rejected, or timed-out request must never be translated into success.

### 3.4 Baseline-freeze input supplied to JOB-00

On 2026-07-14, JOB-02 committed:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-00_BASELINE_FREEZE_INPUT_2026-07-14.md
```

Commit:

```text
b9fc5c3ec8a7ec2903ac7b1cfbddd5873f9d9079
```

That record identified two exact archives previously inspected:

| Purpose | Filename | Size | SHA-256 |
|---|---|---:|---|
| Authoritative RLS/Career source evidence | `rls_career_overhaul_2.6.6.zip` | 40,035,328 bytes | `b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b` |
| RedFox behavioral reference only | `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_RLS_SHOPDATA_ON_EXISTING_BRIDGE_STATIC(2).zip` | 24,370,607 bytes | `284d10c0ad3221f52a718878866f57d218ecd354a8f181136fc44251c85b397d` |

The RedFox v0.10.3 archive is not an approved modular source base. It contains overlapping/copied platform paths and rejected legacy bridge behavior. It may be inspected only as behavioral evidence.

### 3.5 Work-chat to regular-chat migration completed

On 2026-07-14, this regular chat took over the unchanged JOB-02 lane after the original ChatGPT Work chat became inaccessible because of the separate Work-chat usage limit.

Takeover records:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_ALL_JOBS_REGULAR_CHAT_MIGRATION_STATUS_2026-07-14.md
```

Takeover-related commits:

```text
9631d9f560d0a7dd7ea0f7b8bb1c0230e61acc93
2b7943ca86307e3d3fdb269956fd4a3a3e856d00
e610ece0cf272ba8cf322cfe4203e36e7809d24e
```

The full Work-chat transcript and attachments were not recovered. Recovery was partial and based on GitHub evidence. No full recovery was claimed.

### 3.6 GitHub state rechecked for this pause

On 2026-07-17, JOB-02 rechecked the repository before creating this audit.

Findings:

- No JOB-02 implementation commits occurred after the 2026-07-14 regular-chat takeover.
- No branch matching `job02` exists.
- No dedicated JOB-02 pull request exists.
- No dedicated JOB-02 runtime source directory exists.
- No JOB-02 Lua adapter exists.
- No JOB-02 test ZIP or release candidate exists.
- The previously referenced contract/schema/fixture draft filenames still do not appear in GitHub search.

---

## 4. Work tried and recovery attempts

### 4.1 Shared Work-chat recovery

The supplied old shared-chat URL was attempted during the takeover. The available reader could not retrieve the complete conversation and returned a fetch/cache failure.

Not recovered from that chat:

- the complete transcript;
- chat-only attachments;
- local generated files;
- hidden tool activity;
- local validation scripts and console output;
- any uncommitted contract/schema/fixture drafts.

### 4.2 Missing draft packet search

The previous JOB-02 chat reported preparing these files locally:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CONTRACT_v0.1.0-draft.1.md
PROJECT_MANIFESTS/SCHEMAS/JOB-02_SHARED_RLS_CAREER_BRIDGE_SCHEMA_v0.1.0-draft.1.json
PROJECT_MANIFESTS/TEST_FIXTURES/JOB-02_SHARED_RLS_CAREER_BRIDGE_FIXTURES_v0.1.0-draft.1.json
```

The files were checked through exact path fetches and repository search. They were not found.

The prior chat reported the following static results, but the actual files and output are missing:

- JSON schema compiled successfully;
- nine valid fixtures were accepted;
- ten prohibited or invalid fixtures were rejected;
- protected-path scan found no platform, RLS core, or app files;
- no runtime implementation was produced;
- no ZIP was produced.

These claims remain historical notes, not reproducible evidence, until the files are recovered or reconstructed and validation is rerun.

### 4.3 Current JOB-01 dependency check

JOB-01 draft PR `#3`, titled `JOB-01: IceFox phone + PC platform core v0.2`, was rechecked on 2026-07-17.

Current PR state:

```text
OPEN
DRAFT
NOT MERGED
Head branch: agent/job01-platform-core-v0-1
Head SHA: 83da4ad165d6347f7b7588a970f9cd1876df1b98
Platform contract: job01.platform.v1
Built-in destination: redfox.home
Runtime status: UNTESTED
```

JOB-01 v0.2 explicitly contains no Career action forwarding. Its documented boundary reserves `job02.bridge.v1` for JOB-02 after JOB-02 publishes an exact contract and commit.

### 4.4 Baseline decision search

No later JOB-02 contract publication, canonical baseline-freeze approval, or `job02.bridge.v1` publication was found after the JOB-02 baseline-freeze input.

JOB-02 therefore does not assume that JOB-00 has frozen a baseline merely because candidate archives were identified.

---

## 5. Work not done

The following work has not been completed:

- no final `job02.bridge.v1` contract;
- no committed JSON schema;
- no committed valid/invalid fixture set;
- no capability/version handshake specification;
- no correlation ID specification finalized;
- no timeout, retry, or idempotency behavior finalized;
- no normalized error-code catalog finalized;
- no transaction-log payload finalized;
- no dedicated Lua bridge adapter;
- no JOB-01 host transport binding;
- no proof of actual purchase-completion callbacks;
- no proof of inventory sale completion callbacks;
- no phone/PC parity runtime test;
- no West Coast plus second-map runtime test;
- no removal/uninstall test;
- no duplicate-install contamination test;
- no JOB-11 runtime verdict;
- no build ZIP;
- no release candidate.

---

## 6. Current state of the cross-mod bridge

### Status label

```text
CLAIMED — PAUSED BY OWNER REQUEST
PARTIAL — ARCHITECTURE, BOUNDARIES, INITIAL EVENTS, AND RLS API EVIDENCE RECORDED
BLOCKED — REQUIRED BASELINE ARCHIVES AND PREVIOUS DRAFT PACKET ARE NOT PRESENT
NO RUNTIME IMPLEMENTATION OR ZIP EXISTS
```

### What currently exists

- JOB ownership and boundaries;
- initial event-name target;
- known RLS/Career API evidence;
- prohibited implementation rules;
- baseline archive filenames, sizes, and hashes;
- JOB-01 platform boundary and host contract through draft PR #3;
- Work-chat migration and incident audit records;
- this complete pause-state record.

### What currently does not exist

- an installable bridge mod;
- a Lua runtime adapter;
- a published contract version apps can safely depend upon;
- runtime proof that any Career request works through both phone and PC;
- a proven purchase completion result;
- a proven online sell completion result.

No other job should report JOB-02 as built, working, safe, or integrated.

---

## 7. Known problems and risks

1. The original three contract/schema/fixture drafts were never committed and may be permanently lost.
2. The two exact binary baseline archives are not available in the active replacement chat.
3. The full original Work-chat discussion and attachments remain inaccessible through the recovered evidence.
4. JOB-01 PR #3 is still open, draft, unmerged, and runtime untested.
5. JOB-01 currently has no Career forwarding implementation for JOB-02 to bind to.
6. A stock purchase-menu request is not the same as a completed purchase.
7. Old RedFox bridge files contain custom money/storage/spawn behavior and arbitrary dispatch that must not be reused.
8. Duplicate FoxNet/Web Ecosystem ZIPs can mix overlapping files and invalidate testing.
9. Apps may independently invent operation names or call RLS internals while waiting; this is prohibited and would fragment the shared bridge.
10. Without a canonical JOB-00 baseline decision, jobs may inspect or build against different archives.
11. Runtime behavior can change across BeamNG or RLS versions; the planned adapter must stop safely on incompatible versions.
12. No test evidence currently proves all-map behavior.

---

## 8. Files required when work resumes

### Required before contract/source verification

1. `rls_career_overhaul_2.6.6.zip`
   - expected size: `40,035,328` bytes;
   - expected SHA-256: `b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b`;
   - purpose: authoritative RLS/Career API and extension-loading source evidence.

2. `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_RLS_SHOPDATA_ON_EXISTING_BRIDGE_STATIC(2).zip`
   - expected size: `24,370,607` bytes;
   - expected SHA-256: `284d10c0ad3221f52a718878866f57d218ecd354a8f181136fc44251c85b397d`;
   - purpose: behavior/reference comparison only; not an implementation base.

### Required only if copies survived outside the locked chat

3. `JOB-02_SHARED_RLS_CAREER_BRIDGE_CONTRACT_v0.1.0-draft.1.md`
4. `JOB-02_SHARED_RLS_CAREER_BRIDGE_SCHEMA_v0.1.0-draft.1.json`
5. `JOB-02_SHARED_RLS_CAREER_BRIDGE_FIXTURES_v0.1.0-draft.1.json`

If files 3 through 5 do not exist, JOB-02 will reconstruct new replacement drafts from committed evidence and label them clearly as reconstructed rather than recovered originals.

### Helpful for later integration and testing

- exact JOB-01 v0.2 generated test ZIP, expected SHA-256 `ba0ac46f5fefa0b3e59be2a651fcc32582a811f525a669d6ca47c8a86c3aa446`;
- current BeamNG version;
- current RLS version and exact installed archive identity;
- installed-mod inventory showing only one FoxNet/Web Ecosystem package;
- any old JOB-02 validator scripts or output;
- screenshots and `beamng.log` from old shop-data/purchase-menu behavior;
- JOB-11 logging and runtime test requirements when published or updated.

---

## 9. Cross-job dependencies at pause

### JOB-00 — Coordinator / Integration / Verification

Needed from JOB-00:

- canonical baseline-freeze decision;
- approval of the final integration path;
- confirmation of protected files and combined-release order;
- enforcement that no app invents a competing Career/RLS bridge.

### JOB-01 — Phone + PC Platform Core

Current dependency:

- `job01.platform.v1` exists in draft PR #3;
- phone and PC use the same destination registry;
- JOB-01 must pass canonical destination ID and host context unchanged;
- JOB-01 must deliver requests/results without translating failures into success;
- Career forwarding is not implemented yet.

Needed later:

- a committed host transport envelope and exact forwarding hook compatible with `job02.bridge.v1`;
- source/build identity for integration tests;
- runtime-tested phone/PC launch and message delivery.

### JOB-03 — App Store

JOB-03 may advertise Career/RLS permissions only after JOB-02 publishes stable permission and operation definitions. It must not implement Career actions itself.

### Individual app jobs

Scrap Yard, BeamBook, Import/Export, Classics, Insurance/Finance/Garage/Storage, Tow/Recovery, SponsorHub, FoxMail, FoxText, and other apps must propose required operations to JOB-02. They must not call, patch, or copy Career/RLS internals into their own packages.

### JOB-11 — QA / Logging / Failure Triage

Needed later:

- required logging/test matrix;
- duplicate-path and package-collision verification;
- runtime verdict for phone and PC parity;
- West Coast and non-West-Coast map evidence;
- uninstall/removal safety verdict.

---

## 10. Protected paths and prohibited behavior

JOB-02 must not modify or package:

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
RLS phone shell/controller files
RLS computer shell files
JOB-01 browser/navigation/registry files
stock RLS/BeamNG Career modules
another job's app/page files
```

JOB-02 must not:

- create a startup-loaded Career module;
- patch `vehicleShopping` at map load;
- use repeating shop-data refresh timers;
- directly modify money;
- insert vehicles into ownership or storage manually;
- spawn a vehicle and call that a completed purchase;
- set a custom inventory sale price;
- report purchase completion from menu-opening success;
- report unavailable or failed operations as successful;
- bundle duplicate phone, PC, browser, or FoxNet cores;
- build a combined release without JOB-00 approval.

---

## 11. Planned work after David returns

The restart order is:

1. Obtain the two exact baseline archives and any surviving draft packet files.
2. Verify archive filenames, sizes, SHA-256 hashes, and ZIP integrity.
3. Reinspect exact RLS 2.6.6 source functions and extension-loading behavior.
4. Recover the previous contract/schema/fixtures or reconstruct replacement drafts.
5. Define a small versioned envelope containing contract version, operation, request ID, canonical destination ID, host, payload, timestamp, and capability information.
6. Define explicit success, accepted/pending, unavailable, validation error, dependency error, timeout, cancelled, and internal-error result forms.
7. Define strict payloads for Career data, shop data, opening the purchase menu, owned inventory lists, and inventory sell requests.
8. Keep purchase-menu acceptance separate from actual purchase completion.
9. Define logging with at least `[RedFox][BRIDGE]`, `[RedFox][BUY]`, and `[RedFox][SELL]` prefixes while avoiding sensitive or excessive state dumps.
10. Recreate and run valid and invalid fixture tests.
11. Publish the reviewable contract packet as `job02.bridge.v1` on GitHub.
12. Request JOB-00 and JOB-01 boundary review.
13. Only after contract approval, build the smallest removable JOB-02 Lua adapter without copying or modifying RLS core files.
14. Produce mandatory scope, verification, inventory, file-tree, logging, JSON, CSV, TXT, and HTML reports.
15. Test with exactly one approved FoxNet/Web Ecosystem package installed.
16. Test phone and PC parity on West Coast USA and at least one non-West-Coast map.
17. Submit logs and screenshots to JOB-11.
18. Keep status runtime untested until David tests the exact build.

---

## 12. Resume checklist

When David returns, begin by reading:

```text
PROJECT_MANIFESTS/JOB_AUDITS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CAMPING_PAUSE_AUDIT_2026-07-17.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CLAIM.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-00_BASELINE_FREEZE_INPUT_2026-07-14.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
```

Then:

- check whether JOB-00 published a baseline decision during the pause;
- check whether JOB-01 PR #3 changed, merged, or was replaced;
- check for new app operation proposals to JOB-02;
- check whether JOB-11 published new test requirements;
- confirm the required archives and files available in the active chat;
- continue from the contract packet, not from runtime code.

---

## 13. Files changed by this pause audit

This pause operation is documentation-only.

Files affected:

```text
PROJECT_MANIFESTS/JOB_AUDITS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CAMPING_PAUSE_AUDIT_2026-07-17.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CLAIM.md
```

No BeamNG mod source, RLS source, phone/PC source, app/page files, runtime Lua, generated ZIP, release candidate, or another job's implementation is changed by this audit.

---

## 14. Final pause statement

JOB-02 remains claimed by the active Shared RLS / Career Bridge regular chat.

This is not a handoff. Development is paused at David's request while he is camping. No technical work should be inferred during the pause, and no other job should take ownership or create a competing bridge.

The exact restart point is contract recovery/reconstruction and publication of `job02.bridge.v1`; runtime adapter development has not started.
