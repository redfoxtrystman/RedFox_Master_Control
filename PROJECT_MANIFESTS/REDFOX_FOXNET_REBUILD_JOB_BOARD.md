# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** Single coordination page for rebuilding RedFox FoxNet / IceFox for BeamNG without chats fighting each other, hijacking phone/PC, breaking RLS, or shipping unverified ZIPs.

---

# ROLLCALL / CURRENT ASSIGNMENT CORRECTION

David confirmed the current control-room chat is:

```text
JOB-00 — Coordinator / Integration / Verification
```

This chat / Sol is now treated as `JOB-00` for assignment tracking, GitHub board maintenance, integration order, verification enforcement, and failure triage.

The mod work this chat was doing before the reset was mostly:

```text
Scrap Yard / Wrecking Yard
phone buying
PC page broken
RLS marketplace bridge
garage/storage purchase problem
online sell owned vehicles
bad ScrapYard Direct career-module cleanup
```

That technical work now belongs to:

```text
JOB-04 — Scrap Yard / Wrecking Yard
```

Important: `JOB-00` should **not** keep building Scrap Yard code. `JOB-00` preserves the history, coordinates the handoff, blocks bad architecture, and verifies future outputs. A separate `JOB-04` chat should claim Scrap Yard if David wants the rebuild split cleanly.

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
| JOB-00 | Coordinator / Integration / Verification | CLAIMED | Claimed by this control-room Coordinator chat / Sol. |
| JOB-01 | Phone + PC Platform Core | AVAILABLE | Owns phone/PC app/page shells only. |
| JOB-02 | Shared RLS / Career Bridge | CLAIMED | Claimed by Shared RLS / Career Bridge chat / Sol. |
| JOB-03 | RedFox App Store / Play Store | AVAILABLE | Owns install/enable/open/update app store. |
| JOB-04 | Scrap Yard / Wrecking Yard | AVAILABLE | Online buy/sell page first. This is the work we were doing before reset, but it now needs its own job chat. |
| JOB-05 | BeamBook Marketplace | AVAILABLE | BeamBook social/marketplace storefront. |
| JOB-06 | Import / Export Yard | CLAIMED | Claimed by Import / Export Yard chat / Sol. Import/export online page first. |
| JOB-07 | Classics / Collector Exchange | CLAIMED | Claimed by Classics / Collector Exchange chat / Sol. |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | AVAILABLE | Support/status pages only. |
| JOB-09 | Tow / Recovery / Dispatch Integration | CLAIMED | Claimed by Tow/Recovery/Dispatch chat. |
| JOB-10 | Visual Design / Real Website Polish | CLAIMED | Claimed by Visual Design / Real Website Polish chat / Sol. |
| JOB-11 | QA / Logging / Failure Triage | AVAILABLE | Logging, testing matrix, failure reports. |
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards | CLAIMED | Claimed by Sponsor System chat. |

## Taken right now

```text
JOB-00 — Coordinator / Integration / Verification
JOB-02 — Shared RLS / Career Bridge
JOB-06 — Import / Export Yard
JOB-07 — Classics / Collector Exchange
JOB-09 — Tow / Recovery / Dispatch Integration
JOB-10 — Visual Design / Real Website Polish
JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

## Available right now

```text
JOB-01 — Phone + PC Platform Core
JOB-03 — RedFox App Store / Play Store
JOB-04 — Scrap Yard / Wrecking Yard
JOB-05 — BeamBook Marketplace
JOB-08 — Insurance / Finance / Garage / Storage Pages
JOB-11 — QA / Logging / Failure Triage
```

---

# COPY/PASTE MESSAGE FOR EVERY NEW CHAT

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read this GitHub job board first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md

Pick exactly one AVAILABLE job ID. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports; log with the shared RedFox prefixes.

Already claimed: JOB-00 Coordinator / Integration / Verification, JOB-02 Shared RLS / Career Bridge, JOB-06 Import / Export Yard, JOB-07 Classics / Collector Exchange, JOB-09 Tow / Recovery / Dispatch Integration, JOB-10 Visual Design / Real Website Polish, and JOB-12 SponsorHub / FoxMail / FoxText / Sponsor Rewards. Do not claim those again.
```

---

# CLAIM PROTOCOL

Each chat must do this before building anything:

1. Read this file.
2. Pick exactly one `AVAILABLE` job.
3. Say hello to the other chats on this page or in a GitHub handoff note.
4. Report chosen Job ID, files/folders it will inspect, files/folders it may edit, protected files/folders it will not touch, dependencies on other jobs, verification plan, and expected output.
5. Do **not** edit outside the claimed job.
6. Do **not** build an integrated ZIP until `JOB-00` approves integration.
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

Static checks do not prove BeamNG runtime. Do not write “fixed,” “working,” “done,” or “safe” unless David tested it in BeamNG.

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

---

# KNOWN WORKING / KNOWN BAD FACTS

## Working or partially working

- The phone path in the v0.10.3.1 family could request RLS/BeamNG vehicle shop data and open purchase flow.
- RLS PC marketplace can browse/buy cars using the game’s own PC marketplace flow.
- BeamBook works as a standalone private-seller style system, but it needs real BeamBook branding/storefront polish.
- Sponsor communications had already been discussed as a separate system from FoxFax.

## What the previous active work was

Before the job-board reset, the active technical work in the Coordinator chat was mostly Scrap Yard / Wrecking Yard related:

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

That work is now assigned to:

```text
JOB-04 — Scrap Yard / Wrecking Yard
```

`JOB-00` keeps the failure history and coordinates the handoff. `JOB-04` should do future Scrap Yard implementation.

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
**Owner:** this control-room Coordinator chat / Sol  
**Role:** foreman/control room, not feature mechanic.

### Owns

Assignments, this board, integration order, final ZIP approval, verification report enforcement, failure/incident reports, blocking chats that edit outside scope, and preserving history from the failed Scrap Yard attempts.

### May edit

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/*FoxNet*
INCIDENT_REPORTS/*
final handoff/readme files
```

### Must not edit

App code unless doing final approved integration. Scrap Yard implementation files except to inspect/report or final integration after approval.

---

## JOB-01 — Phone + PC Platform Core

**Status:** AVAILABLE

Owns phone shell/app launcher, PC shell/browser/homepage, app/page registry hooks, shared navigation rules, and responsive phone-vs-PC layout rules.

Must not edit Scrap Yard page logic, BeamBook page logic, SponsorHub/FoxMail/FoxText page logic, RLS marketplace logic, or Career modules.

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

**Status:** AVAILABLE

Owns App Store web page/app, app manifests, installed/enabled state, store categories, app cards, install/open/update buttons, and safe app fingerprinting rules.

---

## JOB-04 — Scrap Yard / Wrecking Yard

**Status:** AVAILABLE  
**Important handoff:** this is the technical work that was active before the reset.

Owns Scrap Yard web page, realistic wrecking-yard UI, online buy listings, online sell owned vehicles, and future sell-zone UI placeholder.

`JOB-04` must inspect the baseline and report exact planned edits before touching code. It must read the Scrap Yard incident report and this board first.

Must not create startup career module, map load work, parking spot generation, `redfoxScrapYardDirect` package, SponsorHub/FoxMail/FoxText work, fake money/storage/garage/inventory.

Acceptance test: phone page opens, PC page opens, buy button opens stock/RLS purchase flow, Sell Online lists owned vehicles, sell button calls stock inventory sell function, runtime success is not claimed until David tests.

---

## JOB-05 — BeamBook Marketplace

**Status:** AVAILABLE

Owns BeamBook web page, marketplace storefront, listing card UI, seller/profile/post feel, and better branding.

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

**Status:** AVAILABLE

Owns insurance links/pages, finance/loans/payments pages, garage/storage status pages, and purchase flow help pages. Must not fake garage inventory.

---

## JOB-09 — Tow / Recovery / Dispatch Integration

**Status:** CLAIMED  
**Owner:** Tow/Recovery/Dispatch chat.

Owns tow call app links, recovery job UI, future deliver-to-yard flow, and standalone catalog-19 Tow/Recovery mod files if that chat owns them.

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

**Status:** AVAILABLE

Owns logging instructions, in-game debug page, test matrix, failure report template, and how to collect BeamNG logs.

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

Do not build everything at once.

1. `JOB-00` Coordinator starts/maintains assignment and final integration approval.
2. `JOB-11` QA/logging creates the shared test format.
3. `JOB-01` Platform and `JOB-02` Bridge define shared app/page and backend contracts.
4. `JOB-03` Store creates app registry and store page.
5. `JOB-04` Scrap Yard builds on shared bridge.
6. `JOB-05` BeamBook builds on shared bridge/store.
7. `JOB-06` Import/Export builds page only.
8. `JOB-07` Classics builds page only.
9. `JOB-08` and `JOB-09` connect support pages and tow links.
10. `JOB-12` SponsorHub/FoxMail/FoxText/Sponsor Rewards builds app pages against the published Store/Platform/Bridge contracts.
11. `JOB-10` polishes visuals after functions are stable.
12. `JOB-00` approves final integration only after reports pass.

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
- lets `JOB-00` keep building feature code instead of coordinating and verifying.
