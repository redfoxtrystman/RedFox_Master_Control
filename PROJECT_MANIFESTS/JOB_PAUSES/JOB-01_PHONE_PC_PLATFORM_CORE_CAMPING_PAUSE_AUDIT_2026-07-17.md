# JOB-01 — Phone + PC Platform Core — Camping Pause Full Status Audit

**Date:** 2026-07-17  
**Timestamp:** 2026-07-17 10:16 PDT (America/Los_Angeles)  
**JOB:** JOB-01 — Phone + PC Platform Core  
**Owner:** David / Captain  
**Active chat:** JOB-01 regular-chat takeover / Sol  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Pause type:** TEMPORARY OWNER-REQUESTED CAMPING PAUSE — NOT A HANDOFF  
**Ownership status:** CLAIMED — OWNERSHIP RETAINED BY THIS JOB CHAT  
**Current implementation status:** BUILT — RUNTIME UNTESTED  
**Current implementation version:** `0.2.0`  
**Current source checkpoint:** draft PR `#3`, branch `agent/job01-platform-core-v0-1`, head `83da4ad165d6347f7b7588a970f9cd1876df1b98`

---

## 1. Sound-off

This chat is and remains exactly:

```text
JOB-01 — Phone + PC Platform Core
```

This document is a pause checkpoint while David / Captain is camping. It is not a transfer of ownership, job closeout, abandoned-work notice, release approval, or handoff to another chat.

Resume this same JOB-01 chat when David returns.

JOB-01 remains responsible only for:

- integrating IceFox into the existing RLS phone;
- integrating IceFox into the existing RLS computer;
- one canonical phone/PC destination registry;
- one shared browser/host contract;
- platform navigation, route registration, host behavior, and responsive presentation;
- map-independent platform routing;
- native-page adapters approved through shared contracts;
- platform-owned source, build tooling, contracts, logs, and verification reports.

JOB-01 does not own:

- Career/RLS transaction authority;
- JOB-02 bridge implementation;
- App Store business logic;
- Scrap Yard, BeamBook, Import/Export, Classics, Insurance/Finance/Garage/Storage, Tow/Recovery, SponsorHub, FoxMail, FoxText, or rewards business logic;
- money, inventory, ownership, storage, garage, insurance, purchase completion, sale completion, missions, rewards, or save mutation;
- replacement of the RLS phone shell;
- replacement of the RLS computer shell.

---

## 2. Current state in one statement

```text
JOB-01 HAS A COMPLETE REDFOX-OWNED v0.2.0 SOURCE CHECKPOINT AND DETERMINISTIC
RLS 2.6.6 PATCH BUILDER IN DRAFT PR #3. STATIC CHECKS WERE REPORTED PASSING.
THE GENERATED ZIP IS NOT STORED IN GITHUB AND NO BEAMNG RUNTIME TEST HAS BEEN
RECORDED. THE MOD MUST REMAIN LABELED BUILT — RUNTIME UNTESTED.
```

The current platform has one built-in destination:

```text
redfox.home
```

The current platform contract is:

```text
job01.platform.v1
```

The currently reserved future bridge contract is:

```text
job02.bridge.v1
```

JOB-01 does not currently implement that bridge.

---

## 3. What has been completed

### 3.1 JOB-01 ownership and architecture established

The central board assigns JOB-01 responsibility for the phone/PC platform core while protecting app business logic and Career/RLS authority from JOB-01 edits.

The accepted architecture is:

- RLS Career Overhaul remains the phone and Career authority;
- IceFox is added to the existing phone rather than replacing it;
- IceFox is added to the existing RLS computer through the supported computer-function hook rather than replacing `computer.lua`;
- phone and PC use the same destination identities and same registry;
- phone and PC layouts may differ responsively, but app/page destinations and business logic do not split;
- individual RedFox websites/apps remain isolated removable add-on mods;
- JOB-01 exposes registration and navigation interfaces but does not absorb another job's application code.

### 3.2 Exact baseline inspection completed

The JOB-01 baseline records identify:

```text
Authoritative build input:
rls_career_overhaul_2.6.6.zip
SHA-256: b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b
JOB-01 recorded size: 43,066,347 bytes
Policy: exact deterministic build input
```

```text
Phone-working behavioral reference only:
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX.zip
SHA-256: 4dac614a4b14d423c069dccc8bdb5e0e511ee208f7414d3e6ed50a86a7903597
Recorded size: 24,510,848 bytes
Policy: inspect only; unsafe as modular platform baseline
```

```text
Better Career visual/behavior reference only:
better_career_mod_v050.zip
SHA-256: 3fb6bad89926d5d71cdd1e52a4b7538f46abc202c71c5ccf1e7054fd54a3c7a1
Recorded size: 28,174,063 bytes
Policy: inspect only; no source copied
```

Important discrepancy to verify when David returns:

- JOB-01's baseline hash record lists the exact RLS archive as `43,066,347` bytes.
- Some later cross-job audit text lists a different byte size while repeating the same SHA-256.
- The same SHA-256 cannot belong to two different byte-for-byte file sizes.
- The SHA-256 pinned by the JOB-01 builder is authoritative; the actual uploaded archive size must be measured again and the incorrect cross-job size corrected without changing history.

### 3.3 Initial platform source created

The first implementation checkpoint established:

- one ordinary RedFox GE extension;
- one platform registry;
- one phone application manifest;
- one phone route;
- one PC route;
- one RLS computer function registered through `onComputerAddFunctions`;
- one built-in `redfox.home` destination;
- one browser implementation shared by phone and PC;
- one deterministic builder pinned to the exact RLS archive hash.

### 3.4 Visual revision v0.2 completed

The original branch implementation was revised according to David's direction.

Completed visual changes:

- removed the temporary generic fox mark;
- restored the original orange-and-white IceFox fox-head logo;
- used that logo for the RLS phone tile, PC launch card, browser title bar, and home branding;
- created dark browser chrome;
- added a coastal-road hero image;
- added weather and RedFox-news visual panels;
- added registry-driven quick-access cards;
- added RedFox finance and listing ad artwork;
- added non-transactional vehicle listing preview art;
- added a PC start screen and taskbar;
- kept the phone and PC on the same browser JavaScript, CSS, registry, destinations, and assets;
- used responsive CSS rather than a separate phone business-logic implementation.

Original IceFox logo identity recorded by PR:

```text
SHA-256: 27561d917df7885ffb6023fe51e71844aa7f5fc68986e5b71f06965dee76ba8b
```

### 3.5 Platform contracts published on the draft PR branch

The following contracts and handoffs exist in draft PR #3:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_APP_MANIFEST_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_BASELINE_HASHES.csv
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_BASELINE_INVENTORY.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_DUPLICATE_PATH_REPORT.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_IMPLEMENTATION_PLAN_v0_2.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PHONE_PC_HOST_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PLATFORM_OWNED_FILES.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PROTECTED_FILES.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_ROUTE_AND_DESTINATION_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_ALL_APP_CHATS_REGISTRATION_HANDOFF.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_JOB-02_BRIDGE_BOUNDARY.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_JOB-03_STORE_REGISTRY_HANDOFF.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_VISUAL_REVISION_v0_2.md
```

These files are source checkpoints on an open draft PR. They are not a merged verified release.

### 3.6 Static verification reported complete

The draft PR records passing static checks for:

- exact RLS baseline SHA-256 before patching;
- one phone manifest;
- one phone route;
- one PC route;
- exact saved-layout migration insertion;
- no replacement of `computer.lua`;
- common `job01.platform.v1` registry use by phone and PC;
- original IceFox logo identity;
- JavaScript parsing;
- SVG XML parsing;
- ZIP CRC;
- duplicate archive-path detection;
- no JOB-01 money, inventory, ownership, storage, insurance, reward, purchase, mission, or save mutation;
- required TXT and HTML reports.

No GitHub Actions or CI status checks are attached to the current PR head. The recorded verification came from the local deterministic builder/static verification process.

### 3.7 Work-chat migration and audit completed

The original Work chat became inaccessible on July 14, 2026 because the project was unintentionally placed under the separate Work-chat usage limit. The replacement regular chat:

- accepted the exact unchanged JOB-01 assignment;
- attempted to recover the shared Work-chat link;
- truthfully recorded that the complete transcript and attachments could not be retrieved;
- inspected GitHub and recovered draft PR #3;
- recorded the current source, branch, build hash, baseline hash, scope, limitations, and required files;
- added a regular-chat takeover record;
- added the project-wide Work-chat interruption incident record.

Takeover/audit commits:

```text
94566f1470b73a391ce84e6ec1f122a95977bd7f
JOB-01: record regular-chat takeover after Work-chat lockout

13b11cb4c4c225a38efd03812ae7d39a82f2e9fd
AUDIT: document Work-chat limit interruption and manual migration
```

---

## 4. What was tried and what happened

### Attempt 1 — Recover the old shared Work-chat transcript

Shared link:

```text
https://chatgpt.com/share/6a568d2f-ef04-83e8-b2b4-4d161bd3318d
```

Result:

```text
FAILED TO RECOVER COMPLETE CONTENT
```

Unavailable through the replacement chat:

- full transcript;
- chat-only attachments;
- exact generated ZIP attachment;
- hidden tool activity;
- local build console output;
- any uncommitted changes after the last PR head;
- any runtime test performed only inside the locked chat.

No claim of full recovery was made.

### Attempt 2 — Recover committed work from GitHub

Result:

```text
SUCCESSFUL FOR COMMITTED SOURCE AND CONTRACTS
```

Recovered:

- draft PR #3;
- 48 changed files;
- two implementation commits;
- exact current branch/head;
- platform Lua source;
- builder;
- phone and PC hosts;
- browser JavaScript and CSS;
- original logo and RedFox-owned SVG artwork;
- baseline records;
- contracts and handoffs;
- generated local ZIP hash;
- required runtime test checklist.

### Attempt 3 — Determine whether runtime was tested

Result:

```text
NO VALID JOB-01 v0.2 RUNTIME EVIDENCE FOUND
```

Not found:

- v0.2 `beamng.log`;
- phone screenshots;
- PC screenshots;
- West Coast test results;
- second-map test results;
- controller test results;
- JOB-11 runtime verdict;
- exact installed-mod fingerprint for a v0.2 run.

### Attempt 4 — Static code review after takeover

Result:

```text
PARTIAL SUCCESS — SEVERAL TEST-HARDENING ISSUES IDENTIFIED
```

Identified before runtime testing:

1. Maximize, Privacy, and Menu browser buttons are rendered but have no action handlers.
2. The project rules prohibit visible controls that do nothing unless clearly labeled as placeholders.
3. The displayed address is `https://icefox.redfox/<destination>`, but submitting the unchanged full address does not normalize the `icefox.redfox/` host before registry matching.
4. The weather panel is hard-coded as `Leaf Springs, CA`, `72°F` and can be mistaken for live map-aware information.
5. Current logs are too sparse for fast diagnosis of host, route, registry, destination, map/session, and return behavior.
6. No visible diagnostic/version panel proves which platform build is actually loaded.
7. The current generated ZIP is missing from GitHub and the replacement chat.

No source was changed during this pause audit.

---

## 5. Current implementation and file inventory

### Runtime source

```text
JOB-01_PLATFORM_CORE_SOURCE/lua/ge/extensions/redfoxPlatformCore.lua
JOB-01_PLATFORM_CORE_SOURCE/mod_info/redfox_icefox_platform_core/info.json
JOB-01_PLATFORM_CORE_SOURCE/scripts/redfox_icefox_platform_core/modScript.lua
JOB-01_PLATFORM_CORE_SOURCE/tools/build_rls_2_6_6_patch.py
```

### Phone and PC host files

```text
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/phone/index.html
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/pc/index.html
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/shared/platform.css
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/shared/platform.js
```

### Brand/background/advertising assets

```text
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/brand/icefox_head.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/backgrounds/coastal_highway.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/ads/sidebar/list_ride.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/ads/top/loan_banner.svg
```

### Destination/card artwork

```text
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/collector_exchange.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/export_yard.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/foxfax_reports.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/foxnet_auction.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/parts_exchange.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/recovery.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/scrap_yard.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/cards/xxx_insurance.svg
```

### Logo artwork

```text
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/backalley_red.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/beambook.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/export.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/foxfax.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/foxnet.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/insurance.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/parts.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/logos/recovery.svg
```

### Vehicle preview artwork

```text
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/bruckell_bastion.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/civetta_scintilla.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/etk_kseries.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/gavril_dseries.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/hero_car.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/ibishu_hopper.svg
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/assets/vehicles/red_sedan.svg
```

### Contract/audit files on the draft PR branch

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_APP_MANIFEST_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_BASELINE_HASHES.csv
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_BASELINE_INVENTORY.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_DUPLICATE_PATH_REPORT.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_IMPLEMENTATION_PLAN_v0_2.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PHONE_PC_HOST_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PLATFORM_OWNED_FILES.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_PROTECTED_FILES.txt
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_ROUTE_AND_DESTINATION_CONTRACT.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_ALL_APP_CHATS_REGISTRATION_HANDOFF.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_JOB-02_BRIDGE_BOUNDARY.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_TO_JOB-03_STORE_REGISTRY_HANDOFF.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_VISUAL_REVISION_v0_2.md
```

### Exact RLS files patched at build time

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
```

No other RLS file is emitted by the deterministic build.

---

## 6. Current mod behavior

### Phone

The build is intended to:

- keep the existing RLS phone;
- add one `redfox-icefox` manifest;
- place one IceFox icon after Marketplace in the default layout;
- migrate saved layouts that do not already contain the IceFox ID;
- open `/career/phone-redfox-icefox`;
- host the shared IceFox browser from the JOB-01 RedFox-owned phone HTML;
- request the same platform registry used by PC;
- return to the RLS phone route when leaving IceFox.

### PC

The build is intended to:

- keep the existing RLS computer;
- register `IceFox / FoxNet` through `onComputerAddFunctions`;
- remember the originating computer identifier;
- open the `redfox-icefox-desktop` route;
- present a RedFox workstation/start screen;
- launch the same IceFox browser used by the phone;
- return to the originating RLS computer when possible.

### Shared platform registry

The Lua registry:

- accepts versioned destination tables;
- validates canonical IDs;
- validates local `/ui/modModules/` entry paths;
- allows the built-in `internal:redfox.home` destination;
- prevents one owner from overwriting another owner's destination ID;
- supports phone and PC flags;
- supports enabled state, permissions, order, version, icon path, description, and category;
- publishes a sorted snapshot;
- advertises contract `job01.platform.v1`;
- permits only the reserved `job02.bridge.v1` bridge-contract value.

### Current visible IceFox home

The built-in home currently displays:

- original IceFox branding;
- coastal hero artwork;
- an installed-destination search field;
- registry-driven quick access;
- static weather artwork;
- RedFox news/status text;
- RedFox finance/listing advertising artwork;
- visual-only featured vehicle listings;
- an explicit note that JOB-02 transactions are not connected.

The listing and finance artwork do not perform transactions.

---

## 7. Current build identity

Current source version:

```text
0.2.0
```

Current generated local build SHA-256 recorded by draft PR #3:

```text
ba0ac46f5fefa0b3e59be2a651fcc32582a811f525a669d6ca47c8a86c3aa446
```

Most recent retained filename from the migrated project context:

```text
zzzz_RedFox_IceFox_Platform_Core_RLS_2_6_6_v0_2_0.zip
```

Important:

- the filename must be verified against David's local copy;
- the SHA-256 is the stronger identity;
- the generated ZIP is not stored in the GitHub repository;
- no runtime result is attached to that exact hash;
- do not call it working, fixed, safe, completed, or release-ready.

---

## 8. Known problems, risks, and incomplete work

1. The exact v0.2 generated ZIP is not available in the replacement chat or GitHub.
2. No BeamNG runtime test has been preserved.
3. Draft PR #3 is open, draft, unmerged, and currently marked non-mergeable.
4. No CI/check-run status is attached to the PR head.
5. Maximize, Privacy, and Menu controls are visible without implemented actions.
6. Full displayed IceFox addresses are not correctly normalized when submitted unchanged.
7. Hard-coded weather can appear live even though it is decorative/static.
8. Runtime logging is insufficient for efficient diagnosis.
9. No visible build fingerprint proves the loaded package version/hash.
10. The PC return path has not been tested against actual RLS computers.
11. The saved-layout migration has not been tested on an existing save.
12. The icon position has not been tested against current RLS phone layouts.
13. Controller navigation has not been tested.
14. UI scaling and phone responsiveness have not been tested in BeamNG.
15. Cross-map behavior has not been tested.
16. Duplicate old FoxNet ZIPs can overwrite or mix the same RLS UI paths.
17. Better Career can introduce a second phone/computer/controller path and invalidate the test.
18. No individual RedFox website/app is currently integrated into the platform proof build.
19. JOB-02 has not published a final runtime bridge build.
20. JOB-03 Store integration is not part of the current platform proof.
21. No JOB-11 runtime verdict exists.
22. The original Work-chat-only discussion and attachments remain incomplete.
23. The RLS archive byte-size discrepancy across project audits must be resolved by measuring the actual hash-matching file.

---

## 9. Cross-job dependency state

### JOB-00 — Coordinator / Integration / Verification

Needed later:

- approve final integration order;
- approve merge/release after runtime evidence;
- prevent competing platform copies;
- freeze a canonical tested baseline.

### JOB-02 — Shared RLS / Career Bridge

JOB-01 needs JOB-02 to publish and implement:

- final `job02.bridge.v1` message contract;
- Career data request/results;
- purchase-menu request/results;
- ownership/inventory request/results;
- online sell request/results;
- exact error, timeout, correlation, and logging behavior.

JOB-01 must not implement a competing bridge while waiting.

### JOB-03 — App Store

JOB-03 will consume the final JOB-01 registry/manifest contract. Store integration must not block the basic phone/PC platform proof.

### App jobs

JOB-04 through JOB-09 and JOB-12 must register isolated destinations after the platform proof succeeds. They must not copy JOB-01 platform source into their app packages.

### JOB-10 — Visual Design

JOB-10 may propose visual improvements but must not replace the platform behavior or bypass JOB-01 ownership.

### JOB-11 — QA / Logging / Failure Triage

JOB-11 must review:

- package inventory;
- overlapping files;
- runtime logs;
- phone and PC screenshots;
- West Coast and second-map evidence;
- controller/navigation failures;
- duplicate-mod contamination;
- honest status labeling.

---

## 10. Exact files required when David returns

### Required first

```text
1. zzzz_RedFox_IceFox_Platform_Core_RLS_2_6_6_v0_2_0.zip
   Expected SHA-256: ba0ac46f5fefa0b3e59be2a651fcc32582a811f525a669d6ca47c8a86c3aa446
   Purpose: recover and compare the exact last generated build.
```

```text
2. rls_career_overhaul_2.6.6.zip
   Required SHA-256: b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b
   Purpose: deterministic build input and exact RLS compatibility source.
```

### Helpful but not required for the first v0.2.1 platform-proof build

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX.zip
better_career_mod_v050.zip
acb58920-5214-479f-9eeb-e174177e166c.png
```

They are useful only for regression/visual comparison. They are not approved build baselines.

### Required after the first runtime test

- complete `beamng.log` from game start through phone and PC testing;
- screenshot of the RLS phone before opening IceFox;
- screenshot of the IceFox phone icon placement;
- screenshot of IceFox open on phone;
- screenshot of the RLS computer function list showing `IceFox / FoxNet`;
- screenshot of the RedFox PC start screen;
- screenshot of IceFox open on PC;
- screenshot or log of returning to the RLS computer;
- equivalent phone/PC launch evidence on a non-West-Coast map;
- exact BeamNG version;
- exact enabled-mod list;
- exact map names;
- whether mouse/keyboard and controller were each tested;
- whether the save already existed before installing the test build;
- whether UI cache was cleared;
- any crash, freeze, missing icon, blank screen, console, or Lua error.

---

## 11. Working idea for when David returns

The next useful result should be a small, instrumented platform-proof build rather than another large redesign.

Proposed version:

```text
JOB-01 v0.2.1 — Platform Proof and Diagnostics
```

### Goal

Prove one fact cleanly:

```text
THE EXISTING RLS PHONE AND EXISTING RLS COMPUTER CAN BOTH OPEN THE SAME
REDFOX.HOME DESTINATION THROUGH JOB01.PLATFORM.V1 ON WEST COAST USA AND ONE
SECOND MAP WITHOUT REPLACING RLS OR REQUIRING ANY OTHER REDFOX APP.
```

### Planned v0.2.1 changes

1. Preserve the v0.2 architecture and all working source unless testing proves a failure.
2. Rebuild only from the exact hash-pinned RLS 2.6.6 archive.
3. Remove visible controls that do nothing, or implement only truthful platform-level behavior.
4. Fix address normalization so these forms resolve consistently:

```text
redfox.home
icefox://redfox.home
https://icefox.redfox/redfox.home
IceFox Home
```

5. Mark static weather and listing content clearly as visual/demo content, not live Career data.
6. Add a small platform diagnostics/status panel showing:

```text
JOB-01 version
platform contract
host: phone or pc
active destination
registry destination count
registry success/failure
current map/session identifier when safely available
origin computer identifier presence
last navigation action
last error
```

7. Add consistent logging with a JOB-01 prefix for:

```text
extension load
built-in destination registration
registry request/result
phone launch
PC launch
active destination change
return to phone
return to computer
close
validation rejection
missing extension
missing destination
map/session identifier
```

8. Embed a visible build/version identity in the UI and reports so screenshots prove which build was tested.
9. Keep only `redfox.home`; do not connect transactions or individual app jobs yet.
10. Run static verification and JOB-11 package audit before David installs it.
11. Generate one separate removable ZIP with install, rollback, verification, file tree, and hash reports.
12. Test West Coast first, then one second map.
13. Correct only failures proven by the log/screenshots.
14. After the platform proof passes, freeze `job01.platform.v1` and allow one isolated app at a time to register.

### Why this approach is most likely to work

- It limits the test to one phone icon, one computer entry, one registry, and one destination.
- It removes app transactions and Career business logic from the first failure surface.
- It leaves RLS as the only phone, computer, and Career authority.
- It provides enough diagnostics to determine whether a failure is loading, routing, registry delivery, rendering, map-specific behavior, or duplicate-mod contamination.
- It avoids another all-in-one package.
- It gives every other job a stable platform contract only after runtime proof.

---

## 12. Exact restart sequence

When David returns, continue in this order:

1. Upload the exact v0.2 ZIP and RLS 2.6.6 ZIP.
2. Compute size and SHA-256 for both.
3. Compare the v0.2 ZIP against draft PR #3 and identify any uncommitted difference.
4. Preserve a copy of the exact v0.2 package for regression comparison.
5. Implement only the v0.2.1 hardening items listed above.
6. Run deterministic build and static checks.
7. Run JOB-11 package audit.
8. Produce the exact test ZIP and record its SHA-256.
9. Disable all older FoxNet/Web Ecosystem packages and Better Career.
10. Keep only RLS 2.6.6 plus JOB-01 v0.2.1 enabled for the first proof.
11. Clear BeamNG UI cache if required.
12. Test the existing RLS phone on West Coast USA.
13. Test the existing RLS computer on West Coast USA.
14. Test back, forward, reload, home, search, close/minimize, and return-to-computer behavior.
15. Confirm Marketplace and another original RLS app still open.
16. Repeat phone and PC launch on one non-West-Coast map.
17. Save logs and screenshots.
18. Send evidence to JOB-11.
19. Fix only evidence-backed failures.
20. Mark `DAVID-TESTED WORKING` only after the exact package passes.

---

## 13. Required first test matrix

### Clean environment

- one RLS 2.6.6 archive;
- one JOB-01 test ZIP;
- no old FoxNet all-in-one ZIP;
- no duplicate JOB-01 ZIP;
- Better Career disabled;
- UI cache cleared if stale bundle remains.

### West Coast USA

- start or load RLS Career;
- confirm existing phone opens;
- confirm existing phone apps remain;
- confirm one IceFox icon appears;
- confirm original IceFox logo renders;
- open IceFox;
- confirm `redfox.home` and diagnostics render;
- test navigation controls;
- open RLS computer;
- confirm `IceFox / FoxNet` appears;
- open RedFox PC start screen;
- launch same `redfox.home` destination;
- return to RLS computer;
- verify Marketplace and another original RLS app still work.

### Second map

- repeat phone launch;
- repeat PC launch where an RLS computer is available;
- confirm same destination identity;
- confirm platform does not silently substitute West Coast-only data;
- record unavailable dependencies honestly.

### Failure evidence

For every failure record:

- exact step;
- screenshot;
- `beamng.log` section;
- map;
- host;
- visible build version;
- installed mods;
- whether failure repeats after cache clear/reload.

---

## 14. Work explicitly not planned for the first return build

Do not add these to v0.2.1:

- Scrap Yard purchases;
- vehicle ownership/storage insertion;
- BeamBook transactions;
- Import/Export transactions;
- Classics transactions;
- insurance or finance actions;
- Tow dispatch integration;
- SponsorHub/FoxMail/FoxText business logic;
- App Store install/enable/update behavior;
- fake weather service;
- fake money or Career data;
- games;
- replacement phone shell;
- replacement RLS computer shell;
- large redesign;
- merged all-in-one FoxNet package.

Those items come only after the platform proof and their owning jobs' contracts.

---

## 15. Files affected by this pause audit

This audit adds:

```text
PROJECT_MANIFESTS/JOB_PAUSES/JOB-01_PHONE_PC_PLATFORM_CORE_CAMPING_PAUSE_AUDIT_2026-07-17.md
```

A separate short pause note is added to the active JOB-01 takeover/claim record, and a sound-off comment is added to draft PR #3.

No runtime source, RLS archive, generated ZIP, phone shell, PC shell, app business logic, Career module, or another job's files are changed by this pause documentation.

---

## 16. Migration note preserved

The original JOB-01 chat was unintentionally created as a ChatGPT Work chat. David was not aware that the entire project would be subject to a separate Work-chat usage limit. On July 14, 2026, the original chat became inaccessible and showed access blocked until July 20, 2026.

This caused:

- interrupted development;
- missing chat-only attachments;
- potential context loss;
- manual reconstruction work;
- duplicate-work risk;
- testing-history risk;
- coordination delay.

The replacement regular chat recovered the committed GitHub source and contracts but did not recover the complete original transcript or attachments. This factual criticism and impact record must remain in the project audit trail.

---

## 17. Resume marker

When David returns, the first message/action for JOB-01 is:

```text
RESUME JOB-01 FROM THE 2026-07-17 CAMPING PAUSE AUDIT.
VERIFY THE v0.2 ZIP AND RLS 2.6.6 HASHES, THEN BUILD THE SMALL v0.2.1
PLATFORM-PROOF AND DIAGNOSTICS PACKAGE. DO NOT START A REDESIGN OR ADD APP
TRANSACTIONS BEFORE THE PHONE/PC PLATFORM TEST PASSES.
```

Ownership remains with this JOB-01 chat during the pause.