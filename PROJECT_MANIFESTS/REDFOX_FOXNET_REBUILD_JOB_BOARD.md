# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** Single coordination page for rebuilding RedFox FoxNet / IceFox for BeamNG without chats fighting each other, hijacking phone/PC, breaking RLS, or shipping unverified ZIPs.

---

# OWNER START DIRECTIVE / NEUTRAL ROLLCALL

The active owner directive is:

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
```

Every chat must read that directive before new implementation work. It defines the shared IceFox phone/PC architecture, same-destination rule, all-map requirement, isolated app-mod packaging, real Scrap Yard ownership/storage requirement, exact build order, honest status labels, and permission boundaries.

Central-board rule: do not write “this chat / Sol” as an owner without the exact job/chat title. Per-chat identity belongs in a unique claim file. This board must remain neutral.

## Git claim audit — 2026-07-13

### Active claimed jobs

```text
JOB-00 — Coordinator / Integration / Verification
JOB-01 — Phone + PC Platform Core
JOB-02 — Shared RLS / Career Bridge
JOB-03 — RedFox App Store / Play Store
JOB-04 — Scrap Yard / Wrecking Yard
JOB-05 — BeamBook Marketplace
JOB-06 — Import / Export Yard
JOB-07 — Classics / Collector Exchange
JOB-08 — Insurance / Finance / Garage / Storage Pages
JOB-10 — Visual Design / Real Website Polish
JOB-11 — QA / Logging / Failure Triage
JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

### Unclaimed jobs

```text
JOB-09 — Tow / Recovery / Dispatch Integration
```

### Historical claim corrections

- JOB-00 was temporarily claimed in commit `2d220d6`, released in `4a7d831`, and is now officially claimed by the central coordination chat after David confirmed that coordinating this rebuild is this chat's actual job. Active claim record: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-00_COORDINATOR_INTEGRATION_VERIFICATION_CLAIM.md`; claim commit: `e6f4b2845f922c6dc8ba4a13a8ccccfea404f749`.
- JOB-01 has two historical claim commits (`006f840` and `9106d3f`). The board recognizes one active JOB-01 lane only. Any chat later reassigned to JOB-02 or another job must not also work JOB-01.
- JOB-03's earlier temporary claim was released, but David later assigned a dedicated JOB-03 chat. Active claim record: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-03_REDFOX_APP_STORE_PLAY_STORE_CLAIM.md`; claim commit: `cdd7d875dd053caa73b4ea1ebc253d07518bab2a`.
- JOB-04 had temporary assignment changes; commit `4a7d831` establishes the active Scrap Yard chat.
- JOB-05 is claimed by the exact chat title `5 — JOB-05 — BeamBook Marketplace`. Claim record: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_CLAIM.md`; claim commit: `6426a95d0d058d0c12c1f63a0b37732b13b5d596`.
- JOB-09's earlier claim was released when David confirmed that the same chat is actually JOB-00. JOB-09 is AVAILABLE for a separate Tow / Recovery / Dispatch chat.
- Git shows one active claim each for JOB-00, JOB-01, JOB-02, JOB-03, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-10, JOB-11, and JOB-12.
- No active double ownership is authorized. If two chats believe they own the same job, both stop until David resolves it.

---

# READ THIS FIRST — OFFICIAL JOB IDS

Official job IDs are now:

```text
JOB-00 through JOB-12
```

That is **13 total jobs** because the list starts at `JOB-00`, not `JOB-01`.

Do **not** translate `JOB-09` into “the ninth chat.”  
Do **not** translate `JOB-12` into “12 total chats.”  
Do **not** renumber jobs based on how many chats David opens.

---

# OFFICIAL JOB MAP

| Job ID | Job name | Status | Owner / notes |
|---|---|---|---|
| JOB-00 | Coordinator / Integration / Verification | CLAIMED | Claimed by the central RedFox FoxNet coordination chat / Sol. |
| JOB-01 | Phone + PC Platform Core | CLAIMED | One active Phone + PC Platform Core chat; historical duplicate claim is not a second active owner. |
| JOB-02 | Shared RLS / Career Bridge | CLAIMED | Claimed by Shared RLS / Career Bridge chat / Sol. |
| JOB-03 | RedFox App Store / Play Store | CLAIMED | Claimed by JOB-03 App Store chat; implementation remains deferred until JOB-01 publishes the platform registry. |
| JOB-04 | Scrap Yard / Wrecking Yard | CLAIMED | Claimed by this Scrap Yard / Wrecking Yard chat / Sol. |
| JOB-05 | BeamBook Marketplace | CLAIMED | Claimed by `5 — JOB-05 — BeamBook Marketplace`; implementation waits for the frozen baseline and JOB-01/JOB-02/JOB-11 contracts. |
| JOB-06 | Import / Export Yard | CLAIMED | Claimed by Import / Export Yard chat / Sol. |
| JOB-07 | Classics / Collector Exchange | CLAIMED | Claimed by Classics / Collector Exchange chat / Sol. |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | CLAIMED | Claimed by Insurance / Finance / Garage / Storage Pages chat / Sol. |
| JOB-09 | Tow / Recovery / Dispatch Integration | AVAILABLE | Released when its former chat was confirmed as JOB-00; needs a dedicated Tow/Recovery chat. |
| JOB-10 | Visual Design / Real Website Polish | CLAIMED | Claimed by Visual Design / Real Website Polish chat / Sol. |
| JOB-11 | QA / Logging / Failure Triage | CLAIMED | Claimed by QA / Logging / Failure Triage chat / Sol. |
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards | CLAIMED | Claimed by Sponsor System chat. |

## Taken right now

```text
JOB-00 — Coordinator / Integration / Verification
JOB-01 — Phone + PC Platform Core
JOB-02 — Shared RLS / Career Bridge
JOB-03 — RedFox App Store / Play Store
JOB-04 — Scrap Yard / Wrecking Yard
JOB-05 — BeamBook Marketplace
JOB-06 — Import / Export Yard
JOB-07 — Classics / Collector Exchange
JOB-08 — Insurance / Finance / Garage / Storage Pages
JOB-10 — Visual Design / Real Website Polish
JOB-11 — QA / Logging / Failure Triage
JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

## Available right now

```text
JOB-09 — Tow / Recovery / Dispatch Integration
```

---

# COPY/PASTE MESSAGE FOR EVERY NEW CHAT

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read both owner documents first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md

Pick exactly one AVAILABLE job ID. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports; log with the shared RedFox prefixes.

Already claimed: JOB-00 Coordinator / Integration / Verification, JOB-01 Phone + PC Platform Core, JOB-02 Shared RLS / Career Bridge, JOB-03 RedFox App Store / Play Store, JOB-04 Scrap Yard / Wrecking Yard, JOB-05 BeamBook Marketplace, JOB-06 Import / Export Yard, JOB-07 Classics / Collector Exchange, JOB-08 Insurance / Finance / Garage / Storage Pages, JOB-10 Visual Design / Real Website Polish, JOB-11 QA / Logging / Failure Triage, and JOB-12 SponsorHub / FoxMail / FoxText / Sponsor Rewards. Do not claim those again.
```

---

# CLAIM PROTOCOL

Each chat must do this before building anything:

1. Read this file.
2. Pick exactly one `AVAILABLE` job.
3. Say hello to the other chats on this page or in a GitHub handoff note.
4. Report chosen Job ID, files/folders it will inspect, files/folders it may edit, protected files/folders it will not touch, dependencies on other jobs, verification plan, and expected output.
5. Do **not** edit outside the claimed job.
6. Do **not** build an integrated ZIP until `JOB-00` approves integration, unless David explicitly tells that individual job chat to make a standalone inspection/test package.
7. If a chat needs a shared file from another job, it must ask on GitHub and wait. It must not invent its own copy.
8. If a chat finds the board is wrong, it must report the exact mismatch instead of silently working around it.

---

# RULES OF OPERATIONS — EVERY CHAT MUST FOLLOW

## 1. Inspect first, edit second

No chat may jump straight to building. It must inspect the baseline and list exact planned edits first.

## 2. One job, one scope

A chat owns only its job. It may not fix phone, PC, bridge, app store, Scrap Yard, BeamBook, Import/Export, Classics, QA, visuals, tow, or SponsorHub/FoxMail/FoxText work unless that is its claimed job.

## 3. Do not hijack the phone or PC

Apps/pages must install into the existing phone and PC systems like real apps/pages. Do not replace the whole phone, PC, launcher, or browser shell.

## 4. Phone and PC share one backend contract

Phone and PC layout can differ, but backend messages must be the same. Do not make a separate guesswork PC bridge.

## 5. Use the game/RLS systems, not fake systems

Do not hand-roll money, inventory, garage, storage, insurance, vehicle ownership, or fake vehicle spawning as purchase success. Use existing BeamNG/RLS functions only after inspection proves the correct path.

## 6. No startup career modules for Scrap Yard

Do not create or package:

```text
lua/ge/extensions/career/modules/redfoxScrapYardDirect.lua
```

or any startup-loaded Scrap Yard career module. Previous versions caused severe load/freezing risk.

## 7. Do not patch `vehicleShopping` at startup

Career/shop data must be requested only when an approved app/page opens or when the shared bridge asks for it. No automatic marketplace patch at map load.

## 8. No duplicate FoxNet ZIPs during tests

Only one FoxNet/Web Ecosystem ZIP may be installed at a time. Duplicate zips can mix old and new files.

## 9. Reports are mandatory

Every build must include:

```text
CHANGE_SCOPE_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.html
VERIFY_*.json
VERIFY_*_FILE_INVENTORY.csv
FILE_TREE_*.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
```

JSON alone is not acceptable.

## 10. Runtime is unproven until David tests it

Static checks do not prove BeamNG runtime. Do not write “fixed,” “working,” “done,” or “safe” unless David tested the exact build in BeamNG.

Required status labels are:

```text
DAVID-TESTED WORKING
BUILT — RUNTIME UNTESTED
PARTIAL
BLOCKED
FAILED — STOPPED
MOCKUP / PLACEHOLDER — NOT FUNCTIONAL (only with David's approval)
```

Do not say “should work.” A spawned vehicle is not a completed purchase when ownership/storage still requires a developer cheat.

## 11. If a check fails, stop

Do not ship a “mostly passed” ZIP. If a required check fails, stop and report failure.

## 12. JOB-04 Scrap Yard must not repeat the old Direct-module failure

`JOB-04` owns the Scrap Yard web/page/app work, but it must not create a startup career module, map-load generator, parking-spot generator, or custom money/garage/storage path.

The first stable Scrap Yard target is:

```text
Online Scrap Yard page
Online buy using stock/RLS purchase flow
Online sell owned career inventory vehicles using stock inventory sell flow
Future physical sell-zone placeholder only, not runtime yet
```

## 13. JOB-12 Sponsor System has extra boundaries

`JOB-12` owns SponsorHub, FoxMail, FoxText, and Sponsor Rewards. These must register as add-on apps/pages through the shared platform contracts.

`JOB-12` must not replace phone shell, PC shell, browser shell, App Store core, shared bridge, Career systems, RLS systems, money/inventory/garage/storage, Scrap Yard, BeamBook, Import/Export, Classics, or Tow/Recovery.

FoxFax remains the vehicle-history / Carfax parody site. It is **not** the messaging app and must not be turned into FoxMail/FoxText.


## 14. Same destination and all-map rule

Phone and PC must use one canonical page identity, one canonical destination, and the same backend contract. Presentation may differ, but business logic and data/action messages may not.

All RedFox page routes must open on every map. No app may hard-code West Coast-only shop, dealer, facility, parking, mission, garage, or storage assumptions.

## 15. Separate app-mod rule

The IceFox/FoxNet platform core is the shared front door. Each app/page is developed as an isolated add-on mod with unique paths and IDs. App mods must not copy shared phone, PC, browser, registry, bridge, or another app's files.

A combined release is assembled only after individual verification and JOB-00 approval.

## 16. App Store and future-games rule

JOB-03 is optional for the first working milestone. The existing phone IceFox entry and new PC IceFox entry may use the shared registry without an App Store UI.

Snake and other small games are future backlog only. No chat may build them now without David's permission.

---

# KNOWN WORKING / KNOWN BAD FACTS

## Working or partially working

- The phone path in the v0.10.3.1 family could request RLS/BeamNG vehicle shop data and open purchase flow.
- RLS PC marketplace can browse/buy cars using the game’s own PC marketplace flow.
- BeamBook works as a standalone private-seller style system, but it needs real BeamBook branding/storefront polish.
- Sponsor communications had already been discussed as a separate system from FoxFax.

## What the previous active work was

Before the job-board reset, the active technical work in this chat was Scrap Yard / Wrecking Yard related:

```text
Scrap Yard page
phone buying
PC page broken
RLS marketplace bridge
vehicle purchase spawning but not storing
garage/storage purchase problem
online sell owned vehicles
bad ScrapYard Direct career-module cleanup
```

That work belongs to:

```text
JOB-04 — Scrap Yard / Wrecking Yard
```

## Broken / unsafe — do not use as base

```text
RedFox_ScrapYard_Direct_v0_1_0.zip
RedFox_ScrapYard_Direct_v0_1_1_ONLINE_ONLY_SAFE.zip
RedFox_ScrapYard_Direct_v0_1_2_NO_EARLY_DEP_SAFE_TEST.zip
```

These tried to create a Scrap Yard career module and caused severe loading/freezing risk.

## Duplicate install warning

Do not install multiple FoxNet/Web Ecosystem zips at the same time. They contain overlapping paths such as:

```text
ui/modModules/redfoxCareerWeb/
ui/ui-vue/dist/index.js
assets/js/icefox_front.js
sites/scrap_yard/
```

Mixed installs are invalid tests.

---

# INCIDENT REPORTS / HISTORY THAT CHATS MUST READ

Before editing phone, PC, Scrap Yard, bridge, RLS, or app store code, read:

```text
INCIDENT_REPORTS/2026-07-11_ScrapYard_Direct_RLS_Path_Ignored_Custom_Bridge_Failure.md
INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md
INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md
INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md
```

`JOB-04` must read the Scrap Yard incident report before touching any Scrap Yard code.

`JOB-12` must read these too before touching anything that depends on phone/PC/shared bridge/App Store.

---

# SHARED BRIDGE CONTRACT TARGET

`JOB-02` owns the final bridge, but all app/page jobs must design around this message set:

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

Known game/RLS functions to inspect and use when appropriate:

```text
career_modules_vehicleShopping.updateVehicleList(true)
career_modules_vehicleShopping.getShoppingData()
career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)
career_modules_inventory.getVehicles()
career_modules_inventory.sellVehicleFromInventory(inventoryId)
career_modules_inventory.sellVehicle(inventoryId)
```

Do not invent alternative bridge names unless `JOB-02` changes the shared contract on this board.

`JOB-12` may need new messages later, but must propose them to `JOB-02` first. Example future sponsor messages may include:

```text
RedFoxSponsorMessageReceived
RedFoxSponsorOfferAccepted
RedFoxSponsorRewardClaimed
RedFoxFoxMailSend
RedFoxFoxTextSend
```

Those are **proposals only** until `JOB-02` approves the shared contract.

---

# LOGGING RULES

Every job must log with clear prefixes:

```text
[RedFox][PHONE]
[RedFox][PC]
[RedFox][BRIDGE]
[RedFox][BUY]
[RedFox][SELL]
[RedFox][STORE]
[RedFox][SCRAP]
[RedFox][BEAMBOOK]
[RedFox][IMPORT_EXPORT]
[RedFox][CLASSICS]
[RedFox][TOW]
[RedFox][SPONSOR]
[RedFox][FOXMAIL]
[RedFox][FOXTEXT]
[RedFox][QA]
```

BeamNG log path seen in David’s setup:

```text
D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log
```

Also check:

```text
beamng.1.log
beamng.2.log
beamng.3.log
beamng-launcher.log
```

Search terms:

```text
RedFox
ScrapYard
FoxNet
IceFox
RedFoxRequestCareerData
RedFoxCareerData
RedFoxOpenVehiclePurchase
RedFoxVehiclePurchaseResult
RedFoxSellInventoryVehicle
RedFoxSellInventoryVehicleResult
vehicleShopping
openPurchaseMenu
buyFromPurchaseMenu
inventory
storage
garage
career_modules_inventory
career_modules_vehicleShopping
no active vehicle
dependencies not resolved
JOB-04
JOB-12
SponsorHub
FoxMail
FoxText
Sponsor Rewards
```

---

# APP STORE / PLAY STORE TARGET

The RedFox Store should feel like a real phone app store and PC app/page manager.

## Store tabs

- Home
- Installed
- Updates
- Vehicle Markets
- Services
- Jobs
- Tools
- Experimental
- Developer / Logs

## App buttons

- Install
- Enable
- Disable
- Open
- Update
- View permissions
- View logs

## App permissions

Apps declare permissions before using them:

```text
careerData
vehicleShopping
inventorySell
notifications
mapLocation
yardSellZone
experimentalProps
mail
textMessages
sponsorRewards
```

---

# JOB DETAILS

## JOB-00 — Coordinator / Integration / Verification

**Status:** CLAIMED  
**Owner:** central RedFox FoxNet coordination chat / Sol  
**Claim date:** 2026-07-13  
**Previous assignment:** JOB-09 released; this chat does not hold two jobs.

Claim record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-00_COORDINATOR_INTEGRATION_VERIFICATION_CLAIM.md
```

Owns neutral assignments, this board, baseline freeze, integration order, contract/handoff tracking, final ZIP approval, verification enforcement, failure/incident reports, truth-status enforcement, and blocking chats that edit outside scope.

May edit:

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-00_*
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_*
PROJECT_MANIFESTS/*FoxNet*
INCIDENT_REPORTS/*
final integration handoff/readme/report files
```

Must not implement app/feature code unless David authorizes final integration work. JOB-00 is the foreman and verifier, not another feature mechanic.

---

## JOB-01 — Phone + PC Platform Core

**Status:** CLAIMED  
**Owner:** one active Phone + PC Platform Core chat / Sol  
**Claim evidence:** commits `006f840` and `9106d3f`; only one active owner is authorized.

Owns the existing-phone integration, new PC IceFox entry, canonical app/page manifest and route contract, shared navigation rules, native-page deep links, and responsive phone-versus-PC host behavior.

Immediate owner-directed target:

- preserve the working phone IceFox icon,
- add IceFox to the existing PC without replacing the PC,
- make both entries open the same canonical IceFox destination,
- publish the manifest/route/owned-file contract,
- ensure routes are not West Coast-specific,
- consume JOB-02's bridge rather than implementing a competing Career/RLS bridge.

Must not edit Scrap Yard page logic, BeamBook page logic, SponsorHub/FoxMail/FoxText page logic, App Store business logic, RLS marketplace logic, money/inventory/garage/storage logic, or Career modules.

Required directive:

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
```

Immediate owner handoff:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_TO_JOB-01_PHONE_PC_FIRST_WORKING_MILESTONE_2026-07-13.md
```

JOB-01 must follow this handoff for baseline intake, shared phone/PC destination design, PC IceFox registration, map-independent routing, deliverables, and the first acceptance gate.

---

## JOB-02 — Shared RLS / Career Bridge

**Status:** CLAIMED  
**Owner:** Shared RLS / Career Bridge chat / Sol  
**Claim date:** 2026-07-13

Owns career data requests, vehicle shopping data requests, open stock purchase menu requests, inventory/owned vehicle listing requests, online sell requests, approved sponsor/mail/text bridge messages after review, and logging prefixes.

Must not create fake money, fake storage insert, hand-rolled vehicle spawn, custom Scrap Yard career module, or startup marketplace patch.

Claim record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_CLAIM.md
```

Required platform/app ownership handoff:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md
```

JOB-01 owns the phone/PC/browser/navigation/registry platform. JOB-02 owns the shared UI-to-Lua Career/RLS message contract. Individual app chats own only their assigned app/page and must use the published JOB-01 and JOB-02 contracts.

---

## JOB-03 — RedFox App Store / Play Store

**Status:** CLAIMED  
**Owner:** JOB-03 — RedFox App Store / Play Store chat / Sol  
**Claim date:** 2026-07-13  
**Implementation status:** BLOCKED/DEFERRED until JOB-01 publishes the canonical platform registry and route contract.

Claim record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-03_REDFOX_APP_STORE_PLAY_STORE_CLAIM.md
```

JOB-03 owns the Store page/app, manifest schema, installed/enabled state, categories, app cards, install/enable/disable/open/update controls, permissions display, and Store-specific verification.

JOB-03 must consume JOB-01's registry and launcher contract. It must not create a competing launcher and must not block the first phone/PC IceFox milestone.

---

## JOB-04 — Scrap Yard / Wrecking Yard

**Status:** CLAIMED  
**Owner:** this Scrap Yard / Wrecking Yard chat / Sol  
**Claim date:** 2026-07-13

### Hello to the other RedFox chats

Hello, fellow RedFox chats. `JOB-04` owns only the Scrap Yard / Wrecking Yard app/page work. I will not touch the phone/PC platform, shared bridge core, App Store core, BeamBook, Import/Export, Classics, Tow, SponsorHub/FoxMail/FoxText, RLS source, stock Career files, money, garage, storage, inventory, insurance, or visual-polish-only files outside my scope. I will use the contracts published by `JOB-01`, `JOB-02`, and `JOB-03`.

### Owns

- Scrap Yard web page.
- Realistic wrecking-yard UI.
- Online buy listings UI.
- Online sell owned vehicles UI.
- Future physical sell-zone UI placeholder only.
- Scrap Yard-specific reports and handoff notes.

### Must inspect before editing

- Current selected FoxNet/IceFox baseline ZIP.
- Last useful phone-working v0.10.3.1 family behavior.
- Shared bridge handoff from `JOB-02`.
- Phone/PC app registration handoff from `JOB-01`.
- App Store manifest handoff from `JOB-03`.
- Scrap Yard incident report:

```text
INCIDENT_REPORTS/2026-07-11_ScrapYard_Direct_RLS_Path_Ignored_Custom_Bridge_Failure.md
```

### May edit after approval

Only after inspecting baseline and listing exact planned edits:

```text
ui/modModules/redfoxCareerWeb/sites/scrap_yard/
sites/scrap_yard/                         only if baseline mirrors root site paths
Scrap Yard app manifest entry             only at the path/schema approved by JOB-03
JOB-04 scoped docs/reports
```

### Protected files/folders

```text
ui/modModules/redfoxCareerWeb/phone/       owned by JOB-01 unless it exposes an app-registration slot
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
assets/js/icefox_front.js
ui/ui-vue/dist/index.js                    bridge/platform owned by JOB-01/JOB-02
lua/ge/extensions/career/modules/
lua/ge/extensions/overrides/career/
ui/modModules/redfoxCareerWeb/sites/beambook/
ui/modModules/redfoxCareerWeb/sites/import_export/
ui/modModules/redfoxCareerWeb/sites/classics/
ui/modModules/redfoxCareerWeb/sites/tow_recovery/
ui/modModules/redfoxCareerWeb/sites/sponsorhub/
ui/modModules/redfoxCareerWeb/sites/foxmail/
ui/modModules/redfoxCareerWeb/sites/foxtext/
FoxFax user-fixed art/background/page files unless David explicitly asks
```

### Must not do

- No startup Career module.
- No map-load work.
- No parking spot generation.
- No `redfoxScrapYardDirect` package.
- No fake money.
- No fake garage insert.
- No fake storage insert.
- No fake vehicle ownership.
- No hand-rolled purchase success.
- No SponsorHub/FoxMail/FoxText work.

### First stable target

```text
Online Scrap Yard page
Phone page opens
PC page opens
Buy button opens stock/RLS purchase flow through the approved shared bridge
Sell Online lists owned career inventory vehicles
Sell button calls stock inventory sell function through the approved shared bridge
Future physical sell-zone appears only as a disabled/placeholder UI note until approved
```

### Verification plan

- Inspect baseline before editing.
- List exact edited files before building.
- Validate all HTML/CSS/JS/JSON touched by JOB-04.
- Verify no protected files changed.
- Verify no RLS/Career files changed.
- Verify no phone/PC shell hijack.
- Verify no money/inventory/garage/storage changes.
- Verify no `redfoxScrapYardDirect` or startup Scrap Yard career module.
- Reopen final ZIP and verify paths/reports.
- Include TXT and HTML verification reports.
- Mark runtime unproven until David tests in BeamNG.

---

## JOB-05 — BeamBook Marketplace

**Status:** CLAIMED  
**Owner/chat title:** 5 — JOB-05 — BeamBook Marketplace  
**Claim date:** 2026-07-13  
**Implementation status:** BLOCKED pending JOB-00 frozen baseline and published JOB-01/JOB-02/JOB-11 contracts.

Claim and coordination record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_CLAIM.md
```

Claim commit:

```text
6426a95d0d058d0c12c1f63a0b37732b13b5d596
```

Owns only the isolated BeamBook add-on: BeamBook web page, Facebook-style Wall/social presentation, Marketplace storefront, listing-card UI, seller/profile/post/comment feel, saved-listings/groups presentation, BeamBook-specific content/assets, and responsive phone/PC presentation for one canonical destination.

JOB-05 must preserve the proven standalone `beamBook.zip` marketplace order of operations through the published shared contracts. It must not copy platform/bridge files, patch Career/RLS internals, create map-specific assumptions, or fake money, ownership, storage, garage, insurance, or purchase completion.

---

## JOB-06 — Import / Export Yard

**Status:** CLAIMED  
**Owner:** Import / Export Yard chat / Sol  
**Claim date:** 2026-07-13

Owns online import/export vehicle page, decent vehicles, buy-now page first, and future export yard/hotlist planning.

Claim record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-06_IMPORT_EXPORT_YARD_CLAIM.md
```

The control repository currently has no Import/Export source or baseline ZIP. JOB-06 may document and plan its scope, but must not begin implementation or build a ZIP until the actual baseline is supplied or located and inspected. JOB-06 must use the published JOB-01 platform, JOB-02 bridge, and JOB-03 Store contracts rather than inventing copies.

---

## JOB-07 — Classics / Collector Exchange

**Status:** CLAIMED  
**Owner:** Classics / Collector Exchange chat / Sol  
**Claim date:** 2026-07-13

Owns buy-now collector/classic dealer page, old vehicles, classics, muscle, rare trims, and collector lots. No auction behavior for now.

Claim and coordination record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-07_CLASSICS_COLLECTOR_EXCHANGE_CLAIM.md
```

JOB-07 will wait for the JOB-01 registration contract, JOB-02 shared purchase/data contract, JOB-03 manifest schema, and JOB-00 baseline approval before editing app code or building a ZIP.

---

## JOB-08 — Insurance / Finance / Garage / Storage Pages

**Status:** CLAIMED  
**Owner:** Insurance / Finance / Garage / Storage Pages chat / Sol  
**Claim date:** 2026-07-13

Owns insurance links/pages, finance/loans/payments pages, garage/storage status pages, and purchase flow help pages. The first design is one Vehicle Services portal with four internally separated sections so David can keep it unified or split it later without rewriting backend integration.

Must not fake money, financing, debt, payments, insurance, ownership, garage inventory/capacity, storage inventory/capacity, or purchase success. Must use the published JOB-01 platform, JOB-02 Career/RLS bridge, and JOB-03 manifest contracts rather than editing their cores or guessing private paths.

Claim and coordination record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-08_INSURANCE_FINANCE_GARAGE_STORAGE_CLAIM.md
```

JOB-08 will not edit runtime files or build a ZIP until the exact baseline and JOB-01/JOB-02/JOB-03 contracts are available and the claim record is amended with exact JOB-08-owned runtime paths.

---

## JOB-09 — Tow / Recovery / Dispatch Integration

**Status:** AVAILABLE  
**Owner:** none currently assigned  
**Release date:** 2026-07-13

The earlier JOB-09 claim was released when David confirmed that its chat is actually the central JOB-00 Coordinator. Earlier JOB-09 notes remain historical only; no active Tow/Recovery implementation ownership transfers to JOB-00.

A new JOB-09 chat must claim this job before working on tow call app links, recovery job UI, future deliver-to-yard flow, or catalog-19 Tow/Recovery integration.

---

## JOB-10 — Visual Design / Real Website Polish

**Status:** CLAIMED  
**Owner:** Visual Design / Real Website Polish chat / Sol  
**Claim date:** 2026-07-13

Owns CSS theme, realistic page layouts, icons/cards/buttons, phone-vs-PC responsive appearance, and App Store visual polish.

Current implementation gate: the control repository does not contain David's current Facebook-style website source or the working BeamBook-style reference mod. JOB-10 will not edit website/mod code or build a ZIP until both baselines are supplied or located, inspected, and followed by an exact edit manifest.

Must not change bridge logic, purchase/sell behavior, or FoxFax art unless explicitly approved.

Claim and coordination record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
```

JOB-05 owns BeamBook marketplace behavior and safe functional integration. JOB-10 owns approved Facebook-style presentation, responsive CSS/layout, cards, buttons, icons, and visual polish after the functional boundary is stable.

---

## JOB-11 — QA / Logging / Failure Triage

**Status:** CLAIMED  
**Owner:** QA / Logging / Failure Triage chat / Sol  
**Claim date:** 2026-07-13

### Hello to the other RedFox chats

Hello, fellow RedFox chats. `JOB-11` owns only shared QA, logging standards, test matrices, package/collision checks, and failure-triage evidence. I will not edit your platform, bridge, Store, app/page, Career/RLS, or visual implementation. I will identify the first provable failing layer and hand the evidence to the job that owns it.

### Purpose

JOB-11 is the project's crash investigator and release-quality checkpoint. It makes failures reproducible, separates phone failures from PC/platform/bridge/app/Career/RLS failures, verifies that packages obey ownership boundaries, and stops a candidate build when a required check fails.

JOB-11 does **not** fix another job's code or claim that runtime works. Runtime remains unproven until David tests it in BeamNG.

### Owns

- Shared logging instructions and prefix format.
- Static and BeamNG runtime test matrices.
- Failure-report and evidence templates.
- ZIP integrity, file-collision, duplicate-ID, forbidden-file, and required-report checks.
- Installed-package fingerprint instructions.
- BeamNG log collection/filtering instructions.
- A future JOB-11-owned debug/log viewer only after JOB-01 and JOB-03 publish the plugin contract.

### May edit

~~~text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_CLAIM.md
JOB-11-owned QA/logging/test/failure documentation
a dedicated QA_LOGGING/ or docs/qa/ folder after repository inspection
a dedicated JOB-11 debug-app folder only after JOB-01/JOB-03 publish its path
this board only for JOB-11 status and links requested by David
~~~

### Protected

JOB-11 must not edit the phone shell, PC shell, browser core, navigation, platform registry, shared bridge implementation, Store implementation, any individual app/page, stock Career/RLS modules, money, inventory, garage, storage, insurance, vehicle ownership, or another job's branch/files.

### Required handoff and contract checks

JOB-11 must enforce the platform/app boundaries already recorded in:

~~~text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md
~~~

That includes testing that apps register into the existing phone/PC, do not bundle copied platform cores, use the shared event API, and use the same versioned JOB-02 backend contract on phone and PC.

### Claim record

~~~text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_CLAIM.md
~~~

### Initial verification plan

1. Confirm exact ZIP, version, baseline, and installed mod list.
2. Detect overlapping FoxNet ZIPs and shared file collisions.
3. Verify required reports and protected-file rules.
4. Test phone, PC, registry/platform, app UI, shared events, JOB-02 bridge, and stock/RLS functions as separate layers.
5. Collect timestamps and BeamNG logs for reproducible failures.
6. Report expected result, actual result, first provable failing layer, evidence, severity, and owning job.
7. Mark the result PASS, FAIL/STOP, BLOCKED, or RUNTIME UNPROVEN.
8. Never mark runtime fixed until David's BeamNG test proves it.

### What JOB-11 needs from the other chats

JOB-11 cannot test guesses. Every owning chat must publish its contract and an evidence handoff before asking JOB-11 to validate its work.

| Job(s) | Required handoff to JOB-11 |
|---|---|
| JOB-00 — Coordinator | Name the canonical baseline and release candidate, integration order, acceptance criteria, blocked jobs, approved exceptions, and exact package that may advance. Resolve ownership disputes; JOB-11 reports them but does not decide them. |
| JOB-01 — Phone + PC Platform Core | Publish the detected RLS/BeamNG phone and PC owners, protected core-file list, plugin/registration API, platform version, manifest-facing fields, navigation/theme/event APIs, removal behavior, expected log messages, and a minimal example app. |
| JOB-02 — Shared RLS / Career Bridge | Publish the versioned message names, request/result payload schemas, validation and error codes, capability handshake, UI-to-Lua route, stock/RLS functions used, expected logs, and test fixtures. Phone and PC must use the same contract. |
| JOB-03 — RedFox App Store / Play Store | Publish the manifest schema, permission meanings, app-ID rules, install/enable/disable/open/update state behavior, persistence locations, compatibility rules, removal behavior, and expected Store logs. |
| JOB-04 through JOB-09 and JOB-12 — Feature/app jobs | Provide the exact Job ID, app/page ID, version, baseline, files changed, protected files, entry points, manifest, permissions, dependencies, messages/events used, expected phone and PC behavior, negative tests, removal test, known limitations, expected logs, and required reports. Do not include copied platform cores. |
| JOB-10 — Visual Design / Real Website Polish | Identify exact CSS/assets/templates changed, supported phone/PC sizes, expected responsive results, before/after evidence, accessibility/contrast checks, and proof that IDs, events, bridge behavior, and app ownership were not changed. |

### Required QA intake packet from every build-producing chat

Before JOB-11 begins a full review, the owning chat must provide one GitHub handoff containing:

~~~text
Job ID and owner:
Candidate name and version:
Git commit/branch:
Baseline package and version:
Exact ZIP name, size, and SHA-256:
Complete files added/changed/removed:
Protected files confirmed untouched:
App/site IDs and entry points:
Manifest path and declared permissions:
Platform API version required:
Bridge API version required:
Messages/events sent and received:
Install, enable, disable, open, update, and removal instructions:
Exact phone test and expected result:
Exact PC test and expected result:
Negative/error tests and expected result:
Expected RedFox log prefixes/messages:
Known limitations:
Runtime-unproven items:
Required TXT/HTML/JSON/CSV/file-tree report paths:
~~~

If a field does not apply, the chat must write `N/A` and explain why. Blank fields, “same as before,” and undocumented runtime changes are not valid evidence.

### Shared test gates

1. **Gate 0 — Ownership:** Job is claimed; files belong to that job; dependencies and protected files are named.
2. **Gate 1 — Static/package:** ZIP opens; structure is correct; reports exist; hashes/file inventory match; no prohibited module, copied core, duplicate ID, or collision is found.
3. **Gate 2 — Contract/integration:** Manifest, platform API, shared events, and JOB-02 messages match their published versions; removal does not overwrite or delete shared systems.
4. **Gate 3 — BeamNG runtime:** David tests the exact candidate with one FoxNet/Web Ecosystem ZIP installed and returns steps, timestamps, result, and logs.
5. **Gate 4 — Regression/removal:** Existing phone, PC, RLS apps, FoxNet sites, enable/disable/update, and clean removal still behave as expected.

Allowed JOB-11 verdicts:

~~~text
PASS — all required static and supplied runtime checks passed
FAIL/STOP — a required check failed; do not ship
BLOCKED — required contract, artifact, dependency, or evidence is missing
RUNTIME UNPROVEN — static checks passed but David has not proven runtime in BeamNG
~~~

`RUNTIME UNPROVEN` is not a failure and is not permission to call the feature fixed.

### Failure return loop

When JOB-11 finds a failure:

1. JOB-11 records the candidate identity, reproduction steps, expected result, actual result, first provable failing layer, timestamps, log evidence, severity, and owning job.
2. The owning job fixes only its own implementation and publishes a new version with a changelog.
3. JOB-11 tests the new candidate from Gate 1 onward and repeats earlier regression checks affected by the change.
4. JOB-00 alone decides whether the candidate advances to integration.

JOB-11 will not silently patch another chat's code, approve an artifact with missing evidence, or move a failure to a different job without proof.

### Current dependencies and blockers

JOB-11 can create shared templates and static checks immediately. Complete integration testing is blocked until:

- JOB-01 publishes the phone/PC platform and plugin-registration contract.
- JOB-02 publishes the versioned Career/RLS bridge contract and expected logs.
- JOB-03 publishes the Store manifest/install-state contract.
- Each app/page job submits the required QA intake packet and test candidate.
- David supplies BeamNG runtime results and logs for the exact candidate.

These are normal dependencies, not permission for JOB-11 to take over another job.

### JOB-11 verification and edit trail

- **2026-07-13 13:10:04 PDT — Live verification:** Verified on GitHub `main` that the official JOB-11 row and JOB-11 section both say `CLAIMED`, owner is `QA / Logging / Failure Triage chat / Sol`, the job number remains `JOB-11`, and JOB-11 is not marked available. Verification read board blob `dd109404103c0d83441b39e03157ccbaa5aa99e8`.
- **2026-07-13 13:10:04 PDT — Section-only documentation edit:** Added other-chat handoff requirements, the QA intake packet, test gates, failure return loop, and current dependencies inside JOB-11 only. No other job section, number, name, status, owner, or implementation file was changed. Reason: David requested a clear audit trail and the inputs JOB-11 needs to make the rebuild testable.

---

## JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Status:** CLAIMED  
**Owner:** Sponsor System chat  
**Claim date:** 2026-07-13

Owns SponsorHub, FoxMail, FoxText, and Sponsor Rewards only.

Must not replace phone, PC, App Store, shared bridge, Career/RLS systems, money, inventory, garage, storage, vehicle ownership, Scrap Yard, BeamBook, Import/Export, Classics, Tow/Recovery, or FoxFax.

Required app IDs:

```text
redfox.sponsorhub
redfox.foxmail
redfox.foxtext
redfox.sponsor_rewards
```

Required log prefixes:

```text
[RedFox][SPONSOR]
[RedFox][FOXMAIL]
[RedFox][FOXTEXT]
```

---

# INTEGRATION ORDER

Do not build everything at once. Full requirements are in `PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md`.

1. `JOB-00` freezes one exact baseline and maintains the neutral integration board.
2. `JOB-11` publishes the shared test matrix and truth-status evidence rules.
3. `JOB-01` and `JOB-02` publish the shared platform/route and Career/RLS bridge contracts.
4. Build the first functional slice: existing phone IceFox + new PC IceFox → the same canonical destination on West Coast and a non-West-Coast map.
5. `JOB-04` repairs Scrap Yard phone/PC/all-map purchasing through the stock/RLS ownership and storage path with no developer cheat.
6. `JOB-05`, `JOB-06`, `JOB-07`, `JOB-08`, `JOB-09`, and `JOB-12` build isolated add-on mods against the published contracts.
7. `JOB-03` App Store is optional/deferred and must consume the JOB-01 registry rather than create a competing launcher.
8. `JOB-10` polishes visuals after function is stable.
9. `JOB-00` integrates only independently verified mods with no duplicate shared paths.

---

# REQUIRED ZIP TEST CHECKLIST

Every future ZIP report must say:

```text
ZIP name:
Baseline ZIP:
Job ID:
Files edited:
Files protected:
ZIP integrity:
No duplicate top folders:
No __pycache__:
No old ScrapYard Direct career module:
No startup career patch:
Phone page path:
PC page path:
Shared bridge file path:
Expected phone test:
Expected PC test:
Expected BeamNG log prefixes:
Known unproven runtime items:
```

For `JOB-04`, also include:

```text
Scrap Yard page path:
Online buy path:
Online sell path:
No redfoxScrapYardDirect module:
No startup career module:
No map-load parking/shop generation:
No fake money/storage/garage/inventory:
```

For `JOB-12`, also include:

```text
SponsorHub path:
FoxMail path:
FoxText path:
Sponsor Rewards path:
No FoxFax edits:
No money/inventory/garage/storage edits:
No Career/RLS file edits:
```

---

# STOP CONDITIONS

Stop immediately if any chat:

- edits outside its claimed job,
- creates `redfoxScrapYardDirect` or any startup Scrap Yard career module,
- hand-rolls money, storage, garage, inventory, insurance, or ownership,
- patches `vehicleShopping` at startup,
- ships without TXT + HTML verification reports,
- claims runtime success without David testing,
- packages multiple overlapping FoxNet versions together,
- rewrites phone/PC shell instead of registering apps/pages,
- edits FoxFax art/page files without explicit David approval,
- changes SponsorHub/FoxMail/FoxText from another job without `JOB-12` coordination,
- lets `JOB-04` edit phone/PC/bridge/App Store/RLS core instead of using the published contracts.
