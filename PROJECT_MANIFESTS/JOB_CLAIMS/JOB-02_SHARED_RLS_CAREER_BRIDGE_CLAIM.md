# JOB-02 — Shared RLS / Career Bridge — Claim Record

**Status:** CLAIMED — PAUSED BY OWNER REQUEST — PARTIALLY RECOVERED  
**Owner:** Shared RLS / Career Bridge regular chat / Sol  
**Original claim date:** 2026-07-13  
**Regular-chat takeover:** 2026-07-14 12:44 PDT  
**Camping pause recorded:** 2026-07-17 10:11 PDT  
**Repository:** redfoxtrystman/RedFox_Master_Control

## Hello to the other RedFox chats

Hello JOB-00, JOB-01, JOB-03 through JOB-12. This chat has claimed exactly one job: **JOB-02 — Shared RLS / Career Bridge**. I will publish the shared Career/RLS message contract and compatibility rules, and I will not build or take ownership of your platform shells, stores, apps, pages, visual work, or feature logic.

## Scope owned by JOB-02

- One shared phone-and-PC UI-to-Lua message contract.
- Career data and capability requests.
- RLS/BeamNG vehicle-shopping data requests.
- Requests that open the existing stock/RLS purchase flow.
- Owned career-inventory vehicle listing requests.
- Requests that use the existing inventory sell flow.
- Stable success, failure, unavailable, and validation response payloads.
- Approved sponsor, mail, text, tow, and other cross-app bridge messages after review.
- Shared bridge logging rules and compatibility/version documentation.

JOB-02 provides the shared backend contract. It does not own the phone shell, PC shell, browser, launcher, navigation, app registry, or any individual app/page.

## Baseline files and folders to inspect before any implementation

- PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
- PROJECT_MANIFESTS/JOB_CLAIMS/
- PROJECT_MANIFESTS/JOB_HANDOFFS/
- INCIDENT_REPORTS/2026-07-11_ScrapYard_Direct_RLS_Path_Ignored_Custom_Bridge_Failure.md
- INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md
- INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md
- Current RedFox phone/PC UI bridge callers, for inspection only.
- Current add-on Lua extension/bridge files, if present.
- Existing RLS/BeamNG vehicleShopping and inventory interfaces, for inspection only.
- Current baseline ZIP inventories and verification reports.

Exact runtime files to edit will not be named or changed until baseline inspection proves the correct add-on paths.

## Files JOB-02 may edit

- JOB-02 claim, handoff, contract, schema, compatibility, changelog, test, and verification documentation.
- A dedicated RedFox shared-bridge add-on file or files after baseline inspection confirms their paths.
- JOB-02-owned bridge tests and fixtures.
- The main job board only for this claim/status and JOB-02 contract links explicitly requested by David.

## Protected files and systems JOB-02 will not edit

- Existing BeamNG/RLS phone shell.
- Existing BeamNG/RLS PC shell.
- Browser core, app launcher, navigation, website registry, and shared platform UI owned by JOB-01.
- App Store implementation owned by JOB-03.
- Scrap Yard, BeamBook, Import/Export, Classics, Insurance/Finance/Garage/Storage, Tow/Recovery, Visual Design, QA UI, SponsorHub, FoxMail, FoxText, Sponsor Rewards, FoxFax, DMV, and Dark Web DMV app/page files.
- Stock BeamNG/RLS Career modules.
- Money, garage, storage, inventory, insurance, and vehicle-ownership implementations.
- Any other job's files or branch.

JOB-02 will not create a startup Career module, patch vehicleShopping at map load, spawn a vehicle as fake purchase success, hand-roll money/storage/garage/inventory, or package duplicate phone/PC/FoxNet cores.

## Dependencies and coordination

- JOB-00 approves integration and final combined ZIP work.
- JOB-01 publishes the phone/PC registration, navigation, theme, storage, and UI event adapter contract.
- JOB-03 consumes stable manifests and bridge permissions.
- JOB-11 defines the shared runtime logging/test matrix.
- Individual app jobs propose new events to JOB-02 and wait for contract approval before depending on them.
- Phone and PC must use the same backend message names and payloads even when their layouts differ.

The full platform/app boundary message is recorded in:

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md

## Initial shared bridge contract to inspect and preserve unless deliberately versioned

~~~text
RedFoxRequestCareerData
RedFoxCareerData
RedFoxOpenVehiclePurchase
RedFoxVehiclePurchaseResult
RedFoxGetOwnedVehicles
RedFoxOwnedVehicles
RedFoxSellInventoryVehicle
RedFoxSellInventoryVehicleResult
RedFoxLogEvent
~~~

No proposed sponsor/mail/text/tow message becomes official merely by appearing in an app. JOB-02 must review, document, version, and test it first.

## Verification plan

Before any release, JOB-02 will verify:

1. The same message contract is used by phone and PC callers.
2. Existing phone, PC, RLS apps, and FoxNet sites are not replaced.
3. All requests validate payloads and return explicit results or errors.
4. Career data is requested on demand, not patched at startup.
5. Purchase requests enter the existing stock/RLS purchase menu.
6. Vehicle lists come from the existing Career inventory.
7. Sell requests use the existing Career inventory sell path.
8. No custom money, storage, garage, ownership, or spawn-as-purchase logic exists.
9. Removing the bridge add-on does not damage RLS or leave modified core files.
10. No duplicate event IDs, Angular/module/window IDs, or shared files are packaged.
11. Required TXT, HTML, JSON, CSV, file-tree, scope, logging, and verification reports are included.
12. Static checks are labeled static; runtime behavior remains unproven until David tests it in BeamNG.

## Expected outputs

- Versioned shared bridge contract and payload schema.
- Capability/version handshake documentation.
- Dedicated add-on bridge adapter using proven existing RLS/BeamNG functions.
- Phone/PC adapter instructions for JOB-01.
- Event proposal and approval procedure for every app chat.
- Compatibility requirements, changelog, migration notes, and minimal fixtures.
- Required verification reports and file inventory.
- No integrated ZIP until JOB-00 approves it.

## Regular-chat takeover and recovery trail — 2026-07-14 12:44 PDT

The original Work chat became inaccessible because the separate Work-chat usage limit was reached. David reported that access was blocked on July 14, 2026 until July 20, 2026. The supplied shared link could not be retrieved through the available web reader, so no full-chat recovery is claimed.

Active takeover record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
```

Takeover commit:

```text
9631d9f560d0a7dd7ea0f7b8bb1c0230e61acc93
```

Current honest status:

```text
PARTIAL — three previously prepared contract/schema/fixture draft files are missing from GitHub
BLOCKED — two exact baseline ZIPs are not present in the replacement chat
NO RUNTIME IMPLEMENTATION OR ZIP EXISTS
```

Required next action is to verify the exact RLS 2.6.6 and RedFox v0.10.3 behavioral-reference archives, recover or reconstruct the missing draft packet, and publish `job02.bridge.v1` before any runtime adapter is built.

## Owner-requested camping pause — 2026-07-17 10:11 PDT

David / Captain requested a complete GitHub audit before leaving for camping so every project chat has a durable restart point.

Full JOB-02 pause audit:

```text
PROJECT_MANIFESTS/JOB_AUDITS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CAMPING_PAUSE_AUDIT_2026-07-17.md
```

Pause-audit commit:

```text
f8bf8c7aaad2f1c8e231524c91d94a7da36797a6
```

This is not a handoff. JOB-02 ownership remains with this active regular chat. No implementation work occurred after the 2026-07-14 takeover. The pause audit records completed work, attempted recovery, current dependencies, missing files, known risks, protected paths, and the exact restart plan.

Pause status:

```text
CLAIMED — PAUSED BY OWNER REQUEST
PARTIAL — CONTRACT AND ARCHITECTURE EVIDENCE ONLY
BLOCKED — REQUIRED ARCHIVES AND PREVIOUS DRAFT PACKET MISSING
NO RUNTIME IMPLEMENTATION, TEST BUILD, OR RELEASE CANDIDATE EXISTS
```

## Current action

JOB-02 is paused until David returns from camping. The next technical action remains recovery or reconstruction of the contract/schema/fixture packet and publication of `job02.bridge.v1` before any runtime adapter is built.