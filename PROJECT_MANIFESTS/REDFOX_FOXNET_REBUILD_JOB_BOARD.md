# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** This is the single coordination page for rebuilding RedFox FoxNet / IceFox for BeamNG without the chats fighting each other, hijacking the phone/PC, breaking RLS, or shipping unverified ZIPs.

---

# READ THIS FIRST — OFFICIAL JOB IDS

David has added a new job slot. The official job IDs are now:

```text
JOB-00 through JOB-12
```

That is **13 total jobs** because the list starts at `JOB-00`, not `JOB-01`.

Do **not** translate `JOB-09` into “the ninth chat.”  
Do **not** translate `JOB-12` into “12 total chats.”  
Do **not** renumber jobs based on how many chats David opens.

## Official job map

| Job ID | Job name | Status | Owner / notes |
|---|---|---|---|
| JOB-00 | Coordinator / Integration / Verification | CLAIMED | This chat / Sol. Assigns jobs, verifies integration, keeps board honest. |
| JOB-01 | Phone + PC Platform Core | AVAILABLE | Owns phone/PC app/page shells only. |
| JOB-02 | Shared RLS / Career Bridge | AVAILABLE | Owns shared bridge contract only. |
| JOB-03 | RedFox App Store / Play Store | AVAILABLE | Owns install/enable/open/update app store. |
| JOB-04 | Scrap Yard / Wrecking Yard | AVAILABLE | Online buy/sell page first. |
| JOB-05 | BeamBook Marketplace | AVAILABLE | BeamBook social/marketplace storefront. |
| JOB-06 | Import / Export Yard | AVAILABLE | Import/export online page first. |
| JOB-07 | Classics / Collector Exchange | AVAILABLE | Buy-now collector/classic page. |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | AVAILABLE | Support/status pages only. |
| JOB-09 | Tow / Recovery / Dispatch Integration | CLAIMED | Claimed by Tow/Recovery/Dispatch chat. |
| JOB-10 | Visual Design / Real Website Polish | AVAILABLE | CSS/layout/art only. |
| JOB-11 | QA / Logging / Failure Triage | AVAILABLE | Logging, testing matrix, failure reports. |
| JOB-12 | Reserved New Job Slot / David Assignment Pending | BLOCKED | This is the new slot David said exists. Do not claim until David gives its exact scope/name. |

## Direct answers

- `JOB-00` is Coordinator / Integration / Verification.
- `JOB-09` is Tow / Recovery / Dispatch Integration.
- `JOB-12` exists now, but it is **BLOCKED** until David names its scope. No chat may invent the scope of JOB-12.

---

# HOW MANY CHATS ARE NEEDED?

## Minimum workable setup: 8 chats

The minimum eight chats are not consecutive job IDs. QA/logging is `JOB-11`, but it is needed early.

Use these first:

1. `JOB-00` — Coordinator / Integration / Verification
2. `JOB-01` — Phone + PC Platform Core
3. `JOB-02` — Shared RLS / Career Bridge
4. `JOB-03` — RedFox App Store / Play Store
5. `JOB-04` — Scrap Yard / Wrecking Yard
6. `JOB-05` — BeamBook Marketplace
7. `JOB-06` — Import / Export Yard
8. `JOB-11` — QA / Logging / Failure Triage

## Ideal setup before JOB-12 is named: 12 chats

Use `JOB-00` through `JOB-11`.

## Full setup after JOB-12 is named: 13 chats

Use `JOB-00` through `JOB-12`.

Until David names `JOB-12`, it stays blocked and does not count as an assignable build job.

---

# COPY/PASTE MESSAGE FOR EVERY NEW CHAT

Send each new chat this exact message:

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read this GitHub job board first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md

Pick exactly one AVAILABLE job ID. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports; log with the shared RedFox prefixes.

JOB-12 exists but is BLOCKED until David names its exact scope. Do not claim JOB-12 unless David explicitly assigns it.
```

---

# CLAIM PROTOCOL

Each chat must do this before building anything:

1. Read this file.
2. Pick exactly one `AVAILABLE` job.
3. Say hello to the other chats on this page or in a GitHub handoff note.
4. Report:
   - chosen Job ID,
   - files/folders it will inspect,
   - files/folders it may edit,
   - protected files/folders it will not touch,
   - dependencies on other jobs,
   - verification plan,
   - expected output.
5. Do **not** edit outside the claimed job.
6. Do **not** build an integrated ZIP until `JOB-00` approves integration.
7. Do **not** claim `JOB-12` until David names its scope.

If a chat needs a shared file from another job, it must ask on GitHub and wait. It must not invent its own copy.

---

# RULES OF OPERATIONS — EVERY CHAT MUST FOLLOW

## 1. Inspect first, edit second

No chat may jump straight to building. It must inspect the baseline and list exact planned edits first.

## 2. One job, one scope

A chat owns only its job. It may not fix phone, PC, bridge, app store, Scrap Yard, BeamBook, Import/Export, Classics, QA, visuals, tow, or future JOB-12 work unless that is its claimed job.

## 3. Do not hijack the phone or PC

Apps/pages must install into the existing phone and PC systems like real apps/pages. Do not replace the whole phone, PC, launcher, or browser shell.

## 4. Phone and PC share one backend contract

Phone and PC layout can differ, but backend messages must be the same. Do not make a separate guesswork PC bridge.

## 5. Use the game/RLS systems, not fake systems

Do not hand-roll:

- money,
- inventory,
- garage,
- storage,
- insurance,
- vehicle ownership,
- fake vehicle spawning as purchase success.

Use existing BeamNG/RLS functions only after inspection proves the correct path.

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

- `CHANGE_SCOPE_*.txt`
- `OPEN_THIS_VERIFICATION_REPORT_*.txt`
- `OPEN_THIS_VERIFICATION_REPORT_*.html`
- `VERIFY_*.json`
- `VERIFY_*_FILE_INVENTORY.csv`
- `FILE_TREE_*.txt`
- `LOGGING_AND_TESTING_README.txt`
- `LOGGING_AND_TESTING_README.html`

JSON alone is not acceptable.

## 10. Runtime is unproven until David tests it

Static checks do not prove BeamNG runtime. Do not write “fixed,” “working,” “done,” or “safe” unless David tested it in BeamNG.

## 11. If a check fails, stop

Do not ship a “mostly passed” ZIP. If a required check fails, stop and report failure.

## 12. JOB-12 is blocked until named

No chat may make up what JOB-12 means. If David says the scope, `JOB-00` must update this board before any chat claims it.

---

# KNOWN WORKING / KNOWN BAD FACTS

## Working or partially working

- The phone path in the v0.10.3.1 family could request RLS/BeamNG vehicle shop data and open purchase flow.
- RLS PC marketplace can browse/buy cars using the game’s own PC marketplace flow.
- BeamBook works as a standalone private-seller style system, but it needs real BeamBook branding/storefront polish.

## Broken / unsafe — do not use as base

```text
RedFox_ScrapYard_Direct_v0_1_0.zip
RedFox_ScrapYard_Direct_v0_1_1_ONLINE_ONLY_SAFE.zip
RedFox_ScrapYard_Direct_v0_1_2_NO_EARLY_DEP_SAFE_TEST.zip
```

These tried to create a Scrap Yard career module and caused severe loading/freezing risk.

## Duplicate install warning

Do not install multiple versions of these at the same time:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1...zip
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7...zip
any other zzzz_RedFox_FoxNet_Web_Ecosystem...zip
```

They contain overlapping paths such as:

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
[RedFox][QA]
[RedFox][JOB12]
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
JOB-12
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
```

## App manifest example

```json
{
  "id": "redfox.scrapyard",
  "name": "RedFox Scrap Yard",
  "version": "0.1.0",
  "category": "Vehicle Markets",
  "description": "Online salvage and wrecking yard store.",
  "phoneEnabled": true,
  "pcEnabled": true,
  "entry": "sites/scrap_yard/index.html",
  "icon": "assets/icons/scrapyard.png",
  "permissions": ["vehicleShopping", "inventorySell"],
  "status": "experimental"
}
```

---

# JOB DETAILS

## JOB-00 — Coordinator / Integration / Verification

**Status:** CLAIMED  
**Claimed by:** This chat / Sol  
**Role:** Foreman / control room. No feature coding unless doing approved final integration.

Owns assignment, this board, integration order, verification reports, and stop/go calls.

May edit:

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- `PROJECT_MANIFESTS/*FoxNet*`
- `INCIDENT_REPORTS/*`
- final handoff/readme files

Must not edit feature/app code unless doing final approved integration.

Acceptance test:

- Every job has one owner.
- No two jobs claim the same code without coordination.
- Every final package has TXT + HTML verification reports and a file tree.

---

## JOB-01 — Phone + PC Platform Core

**Status:** AVAILABLE

Goal: Make phone and PC use the same app/page registration model and shared backend contract.

Owns:

- phone shell/app launcher,
- PC shell/browser/homepage,
- app/page registry,
- shared navigation rules,
- responsive phone-vs-PC layout rules.

May edit:

- `ui/modModules/redfoxCareerWeb/phone/`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
- `assets/js/icefox_front.js`
- shared registry files created for RedFox apps/pages.

Must not edit Scrap Yard page logic, BeamBook page logic, RLS marketplace logic, or career modules.

Acceptance test:

- Phone and PC list the same registered apps/pages where enabled.
- Phone layout and PC layout can differ, but backend messages are the same.
- Adding a new app means adding a manifest/registry entry, not editing five unrelated files.

---

## JOB-02 — Shared RLS / Career Bridge

**Status:** AVAILABLE

Goal: Create one safe bridge contract that both phone and PC use.

Owns:

- career data requests,
- vehicle shopping data requests,
- open stock purchase menu requests,
- inventory/owned vehicle listing requests,
- online sell requests,
- logging prefixes.

Must not do:

- fake money,
- fake storage insert,
- hand-rolled vehicle spawn,
- custom Scrap Yard career module,
- startup marketplace patch.

Acceptance test:

- Same Scrap Yard page can run from phone or PC and receive the same data shape.
- Logs clearly say whether the message came from PHONE, PC, VUE, BUY, SELL, or BRIDGE.

---

## JOB-03 — RedFox App Store / Play Store

**Status:** AVAILABLE

Goal: Create a RedFox Play Store style app where apps/pages can be installed/enabled/disabled/opened.

Owns:

- app store web page/app,
- app manifests,
- installed/enabled state,
- store categories,
- app cards,
- install/open/update buttons,
- safe app fingerprinting rules.

Acceptance test:

- Phone can open Store.
- PC can open Store.
- Store shows Scrap Yard, BeamBook, Import/Export, Classics, and future JOB-12 apps only if enabled.
- Disabled apps do not appear in normal launcher unless Store says enabled.

---

## JOB-04 — Scrap Yard / Wrecking Yard

**Status:** AVAILABLE

Goal: Build the realistic Scrap Yard / Wrecking Yard page as an online store first, with future physical sell-point support.

Current required behavior:

- Buy cars online from existing RLS/BeamNG shop data.
- Sell owned career inventory vehicles online.
- Use stock purchase/sell paths only.
- No startup career module.
- No map load work.
- No parking spot generation.

Future sell-point idea:

Any building can become a Scrap Yard sell point by placing a sell-circle prop/marker. Player drags/tows/trailers a vehicle into the circle, opens the Scrap Yard app, sees vehicles inside/above the circle, chooses which vehicle to sell.

Do not build the prop runtime until the web-only buy/sell path and shared bridge are stable.

Acceptance test:

- Phone page opens.
- PC page opens.
- Buy button opens stock/RLS purchase flow.
- Sell Online lists owned vehicles.
- Sell button calls stock inventory sell function.
- No old `redfoxScrapYardDirect` module exists in package.

---

## JOB-05 — BeamBook Marketplace

**Status:** AVAILABLE

Goal: Turn BeamBook into a real Facebook/marketplace-style app and storefront without breaking its working core.

Must preserve BeamBook’s working order of operations:

```text
util_configListGenerator.getEligibleVehicles()
util_configListGenerator.getRandomVehicleInfos()
career_modules_vehicleShopping.getVehiclesInShop()
career_modules_vehicleShopping.getShoppingData()
```

Acceptance test:

- BeamBook still works as before.
- Storefront says BeamBook Marketplace.
- Page looks social/marketplace style.
- Does not break stock purchase/storage flow.

---

## JOB-06 — Import / Export Yard

**Status:** AVAILABLE

Goal: Create Import/Export as its own app/page first, then later a yard runtime.

Phase 1:

- online import/export vehicle page,
- decent vehicles, not pure scrap,
- buy-now, not auction,
- shared bridge and stock purchase path.

Future gameplay:

- physical export yard sell point,
- hotlist of 10 target vehicles like a Gone in 60 Seconds board,
- sightings/notifications,
- bring target vehicle to export yard,
- sell/export for payout.

Acceptance test:

- Page exists as an installable app.
- No stolen/traffic sell logic until runtime is designed safely.
- Uses shared bridge only.

---

## JOB-07 — Classics / Collector Exchange

**Status:** AVAILABLE

Goal: Convert Classics from auction style into a buy-now collector dealer page.

Rules:

- old vehicles,
- classics/muscle/collector/luxury/rare trims,
- higher price, cleaner than Scrap Yard,
- no auction behavior for now,
- stock purchase path.

Acceptance test:

- Page is buy-now.
- Page does not use Copart/auction flow.
- Page uses shared bridge and stock purchase.

---

## JOB-08 — Insurance / Finance / Garage / Storage Pages

**Status:** AVAILABLE

Goal: Make support pages that make buying/selling feel complete.

Owns:

- insurance links/pages,
- finance/loans/payments pages,
- garage/storage status pages,
- purchase flow help pages.

Must not replace stock insurance/storage behavior or fake garage inventory.

Acceptance test:

- Pages explain/status the real game/RLS state.
- Links flow naturally from vehicle buy/sell pages.

---

## JOB-09 — Tow / Recovery / Dispatch Integration

**Status:** CLAIMED  
**Claimed by:** RedFox Tow & Recovery Dispatch chat / Sol  
**Claim date:** 2026-07-13

Goal: Connect tow/recovery gameplay to Scrap Yard/Import Export later.

Owns:

- tow call app links,
- recovery job UI,
- future approved “deliver to yard” flow,
- integration planning for catalog mod 19, permanent module ID `redfox_tow_recovery_dispatch`.

Must not edit Scrap Yard core, phone core, PC core, shared bridge, app store core, RLS source, stock Career files, money, inventory, garage, or storage.

Dependencies before building:

- JOB-01 shared phone/PC registration and navigation contract,
- JOB-02 shared RLS/Career bridge messages and data shapes,
- JOB-03 app manifest/permissions/install contract,
- JOB-04 and JOB-06 approved yard delivery/deep-link contracts,
- JOB-11 shared logging/failure-report format.

Acceptance test:

- App/page exists and can deep-link later.
- No shared file conflicts.
- Standalone Tow/Recovery gameplay continues to use normal Career payment APIs and separate temporary-yard state.


### Coordination hello — JOB-09

Hello, fellow RedFox FoxNet rebuild chats. This is Sol from the Tow / Recovery / Dispatch chat. I have claimed **JOB-09 only**.

- I will own only tow-call app links, recovery-job UI, the future approved “deliver to yard” flow, and later deep-link integration.
- I will wait for the shared contracts from JOB-01, JOB-02, JOB-03, JOB-04, JOB-06, and JOB-11 before integrating with their work.
- I will not edit the phone shell, PC shell, shared bridge, App Store core, Scrap Yard core, Import/Export core, RLS source, stock Career files, money, inventory, garage, or storage.
- No app-code files or ZIP are being changed by this claim. Before building, I will inspect the baseline and publish the exact files to inspect/edit, protected files, dependencies, and verification plan.
- BeamNG runtime will remain **unproven until David tests it**.

---

## JOB-10 — Visual Design / Real Website Polish

**Status:** AVAILABLE

Goal: Make pages look like real web pages, not debug panels.

Owns CSS theme, realistic page layouts, icons/cards/buttons, phone-vs-PC responsive appearance, and app-store visual polish.

Must not change bridge logic, purchase/sell behavior, or user-fixed FoxFax art unless specifically asked.

Acceptance test:

- Realistic phone and PC page mockups.
- No functional code broken.

---

## JOB-11 — QA / Logging / Failure Triage

**Status:** AVAILABLE

Goal: Make testing and failure reporting simple.

Owns logging instructions, in-game debug page, test matrix, failure report template, and how to collect BeamNG logs.

Acceptance test:

- Every build includes `LOGGING_AND_TESTING_README.txt` and `.html`.
- Tester can tell phone vs PC failures apart.
- Tester can prove which ZIPs were installed.

---

## JOB-12 — Reserved New Job Slot / David Assignment Pending

**Status:** BLOCKED  
**Reason:** David said there is now a job 12, but the exact scope/name was not defined in this board yet.

This is an official job slot now, but it is not claimable until David gives it a name and scope.

Rules for JOB-12:

- Do not claim JOB-12 until David names it.
- Do not invent its purpose.
- Do not use JOB-12 as overflow work for another job.
- Once David names it, JOB-00 must update this board with:
  - goal,
  - owns,
  - may edit,
  - must not edit,
  - dependencies,
  - acceptance test.

---

# INTEGRATION ORDER

1. `JOB-00` Coordinator keeps this board updated.
2. `JOB-11` QA/logging publishes shared test/log format.
3. `JOB-01` Platform and `JOB-02` Bridge define shared app/page contract.
4. `JOB-03` Store creates app registry and store page.
5. `JOB-04` Scrap Yard builds on shared bridge.
6. `JOB-05` BeamBook builds on shared bridge/store.
7. `JOB-06` Import/Export builds page only.
8. `JOB-07` Classics builds page only.
9. `JOB-08` and `JOB-09` connect support pages and tow links.
10. `JOB-10` polishes visuals after functions are stable.
11. `JOB-12` integrates only after David names it and the board is updated.
12. `JOB-00` approves final integration ZIP.

---

# REQUIRED ZIP TEST CHECKLIST

Before David tests a ZIP, the build report must say:

```text
ZIP name:
Baseline ZIP:
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

David should test with only one FoxNet/Web Ecosystem ZIP installed at a time.

---

# STOP CONDITIONS

Stop immediately if a chat tries to:

- create a startup-loaded Scrap Yard career module,
- patch `vehicleShopping` at startup,
- replace phone or PC shells instead of installing apps/pages,
- hand-roll money/storage/garage/inventory,
- ship without TXT and HTML reports,
- ship with duplicate FoxNet paths unverified,
- claim runtime success without David testing,
- claim or define `JOB-12` without David’s exact scope.
