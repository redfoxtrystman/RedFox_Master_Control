# READ FIRST — MODULAR BROWSER CORE + ISOLATED FEATURE MODULE ARCHITECTURE

**Date:** 2026-07-30  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Runtime target:** Phone only; PC runtime remains deferred  
**Status:** OWNER-APPROVED ARCHITECTURE — COMPATIBILITY TEST REQUIRED BEFORE REFACTOR

## 1. Owner decision

The RedFox/FoxNet web system will use:

```text
ONE shared RedFox FoxNet Browser Core mod
+ ONE isolated module for each webpage/job
+ ONE shared Career/RLS operation contract
```

Do not rebuild one giant JOB-04 package. Do not allow every feature job to ship its own copy of the phone browser, global Vue bundle, phone layout, shared route host or common bridge.

## 2. Exact current candidates

### Shared Browser/Core compatibility test

```text
RedFox_FoxNet_Browser_Core_v0_1_0_COMPAT_TEST_FROM_JOB04_v0_3_4.zip
SHA-256: d731f364328b1f17761117793331be85c0f6e1f7577bfcdff1eb609f57fa8fc3
Files: 51
ZIP bytes: 1,240,469
Uncompressed bytes: 5,902,462
```

### JOB-04 — Scrap Yard / Wrecking Yard slim module

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1902PT_v0_3_5_SLIM_MODULE_REQUIRES_BROWSER_CORE_FROM_v0_3_4.zip
SHA-256: 358f663e2fd2ce35f8b720c1d07f5db57393135247efc6fd6cb40215e1238bd5
Files: 34
ZIP bytes: 75,748
Uncompressed bytes: 281,128
```

### Unchanged comparison modules

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_3_ExactYardGarageLinkPerformanceRepair.zip
SHA-256: 61f870dbe354cda5ad6ff15b3f1a6a81c2376250108b4a7bc82d17c23fc9201e

RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip
SHA-256: 1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071
```

### Records-only archive

```text
RedFox_JOB-04_v0_3_4_REMOVED_EXTRAS_RECORDS_ONLY_2026-07-30.zip
SHA-256: 57225e44a0bb...
```

The records archive is not installable. Every path is nested under:

```text
RECORDS_ONLY_DO_NOT_INSTALL/
```

## 3. Coordinator audit result

The old JOB-04 v0.3.4 archive contained 1,047 active files and carried shared Browser/Core, obsolete Auction and Tow/Recovery website copies, unrelated websites, old versions, root mirrors, reports and development records.

The split reduced active files to 85 across Browser Core + JOB-04 slim. The exact Browser Core, JOB-04 slim, JOB-09 and JOB-13 packages have zero shared active content paths when required root `info.json` files are excluded.

This proves the package split is real and worth preserving.

It does **not** prove Career runtime compatibility.

## 4. Critical limitation of Browser Core v0.1.0

Browser Core v0.1.0 is separated by archive path, but it is not yet a clean generic host.

It still includes JOB-04-specific behavior inside shared files, including:

- Wrecking Yard route wiring;
- `RedFoxScrapYard...` message handling;
- purchase-menu and sell relays;
- direct `career_modules_vehicleShopping` integration;
- Scrap Yard-specific iframe forwarding;
- PC-era page/assets despite the phone-only owner direction.

Therefore:

```text
Browser Core v0.1.0 = COMPATIBILITY TEST HOST ONLY
NOT a final shared core
NOT the template for mass-converting BeamBook, Tow Yard or Auction
```

## 5. Permanent ownership boundaries

### JOB-01 — Phone + PC Platform Core

Current active responsibility is phone Browser Core. PC remains deferred.

Owns only:

- phone browser shell;
- phone tile/icon and lifecycle;
- shared route host;
- generic feature registry;
- generic iframe/message relay;
- common navigation/theme/shared assets;
- installed/missing-module behavior;
- core version diagnostics;
- global UI compatibility files when explicitly approved;
- clean disable/removal behavior.

JOB-01 must not implement Wrecking Yard purchase/sell, Tow dispatch, Auction bidding, BeamBook listings or other feature business logic.

### JOB-02 — Shared RLS / Career Bridge

Owns shared authoritative Career/RLS operations and contracts for money, ownership, inventory, garage/storage, purchase, sale, transfer and settlement.

### Feature jobs

Each feature job owns:

- one unique webpage folder;
- its own HTML/CSS/JS/assets;
- its own Lua extension(s);
- its own settings/save paths;
- its own business operations;
- its own logs and version records;
- one feature registration manifest;
- no Browser Core files.

Examples:

```text
JOB-04 — Wrecking Yard page + buying/selling/scrap/parts logic
JOB-05 — BeamBook page + marketplace/social logic
JOB-09 — Tow Yard/dispatch page + Tow logic
JOB-13 — Online Auctions page + auction engine/settlement logic
```

### JOB-10 — Visual Design / Real Website Polish

Owns visual redesign and mobile page handoff, not gameplay operations.

## 6. Proposed generic registration contract

This is an architecture target, not yet a runtime-proven BeamNG API.

Each feature module should expose one unique registration record with fields such as:

```text
featureId
jobId
name
routeId
pagePath
extensionName
capabilities
minimumCoreVersion
minimumBridgeVersion
iconPath
logPrefix
```

The Browser Core should discover or receive installed feature registrations and build its page list dynamically.

Feature requests should use a generic envelope:

```text
featureId
operation
requestId
payload
```

The Browser Core relays the request. The named feature extension executes it. The Browser Core must not know how to buy, sell, scrap, bid, tow or dispatch.

## 7. Immediate test order — no new broad edits

Do not install the records-only archive.

Fully restart BeamNG between combinations.

```text
TEST A: Browser Core + JOB-04 slim
TEST B: Browser Core + JOB-04 slim + JOB-09
TEST C: Browser Core + JOB-04 slim + JOB-13
TEST D: Browser Core + JOB-04 slim + JOB-09 + JOB-13
```

Record for every test:

```text
Career load result
Phone load result
Browser welcome load time
Wrecking Yard page load time
Visible Wrecking Yard version
One inexpensive purchase result
Sell/Scrap result only after purchase is stable
First visible failure
Exact enabled ZIP list
beamng.log from first failing combination
```

Do not change multiple archives before the first failing combination is identified.

## 8. Decision after Test A

### If Browser Core + JOB-04 slim passes

1. Freeze the exact Core and JOB-04 hashes as the first modular runtime baseline.
2. Build a core-only v0.2 cleanup.
3. Remove JOB-04-specific relays and direct vehicle-shopping code from Core.
4. Move all Wrecking Yard business handling to JOB-04-owned JS/Lua.
5. Add one generic registration/request proof using JOB-04 only.
6. Re-test purchase, owned-vehicle list, sell, whole scrap and strip/scrap.
7. Add JOB-13, JOB-09 Tow Yard and JOB-05 BeamBook one at a time.

### If Browser Core + JOB-04 slim fails

Stop. Collect the log. Repair only the smallest Core/JOB-04 boundary. Do not add JOB-09, JOB-13, BeamBook or a new website design yet.

## 9. JOB-09 / JOB-13 / JOB-04 scope overlap

JOB-09 v0.4.4.3 currently contains internal auction, direct-sale and scrap functions. Those functions are not path collisions, but they overlap future authoritative ownership:

- JOB-13 owns online timed auctions;
- JOB-04 owns Wrecking Yard scrap/strip/returned-parts behavior;
- JOB-09 owns Tow custody, lien eligibility, recovery, yard records and source export.

Do not delete JOB-09 behavior during compatibility testing. Freeze new expansion. Later replace competing engines with versioned prepare/confirm handoffs to JOB-13 and JOB-04.

## 10. JOB-13 current build limitation

JOB-13 v0.1.2 is a standalone TEST-mode auction app. It uses simulated money by default and is not yet a LIVE Career/RLS auction module.

Do not treat successful standalone bidding as proof of real buyer charging, seller settlement, source removal, delivery or garage ownership.

## 11. No-trash rule

Do not discard the old working code.

Preserve:

- original JOB-04 v0.3.4 as rollback;
- records-only archive;
- Browser Core v0.1.0 compatibility candidate;
- JOB-04 v0.3.5 slim candidate;
- unchanged JOB-09 and JOB-13 inputs;
- exact hashes and logs.

Refactor only after the compatibility matrix proves which boundary fails.

## 12. Coordination records

```text
Issue #30 — JOB-04 active version ledger
Issue #4 — JOB-09 ownership/coordination
Issue #40 — JOB-13 ownership/coordination
Issue #41 — Shared Browser Core integration ledger
```

All affected chats must read this file before making a new integrated website build.
