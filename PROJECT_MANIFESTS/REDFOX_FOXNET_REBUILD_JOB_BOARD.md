# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** Coordinate multiple ChatGPT chats so the RedFox phone, PC, web pages, app store, and RLS/career pages are rebuilt in the correct order without each chat hijacking the others.

---

## Current decision

We are starting again from a clean plan.

The phone and PC must work like real devices:

- **Phone:** real app launcher, installable apps, notifications/messages where useful, apps open in phone-sized UI.
- **PC:** real browser/desktop pages, pages open in PC-sized UI.
- **Both:** use the same shared backend/bridge rules for career data, buying, selling, inventory, logging, and app registration.
- **Apps/pages:** install into the existing phone and PC systems like real apps/pages. Do **not** replace or hijack the whole phone/PC shell.
- **Store:** create a RedFox app store/play store style app where RedFox apps can be discovered, installed/enabled, disabled, updated, and opened.

---

## How many chats are needed?

### Minimum workable setup: **8 chats**

1. **Coordinator / Integration / Verification**
2. **Phone + PC Platform Core**
3. **Shared RLS/Career Bridge**
4. **RedFox App Store / Play Store**
5. **Scrap Yard / Wrecking Yard**
6. **BeamBook Marketplace**
7. **Import / Export Yard**
8. **QA / Logging / Failure Triage**

### Better setup: **12 chats**

Add these four extra focused chats:

9. **Classics / Collector Exchange**
10. **Insurance / Finance / Garage / Storage Pages**
11. **Tow / Recovery / Dispatch Integration**
12. **Visual Design / Theme / Real Website Polish**

### Best rule

Use **8 chats minimum**, **12 chats ideal**.  
Do not create 20 random chats. Too many chats will cause more conflicts unless the Coordinator keeps the job board updated.

---

## Claim protocol for each chat

When a chat starts, send it this file and tell it:

> Read `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`. Pick exactly one AVAILABLE job. Do not edit outside that job. Update the job row or leave a GitHub note saying what you claimed, what files you will touch, and what files you will not touch.

Each chat must report:

- Job ID chosen.
- Exact files/folders it will inspect.
- Exact files/folders it may edit.
- Exact files/folders it must not touch.
- Whether it needs another chat's output before building.
- Verification steps it will run.

No chat should build a final ZIP until its job is stable and the Coordinator approves integration.

---

## Global hard rules

These rules apply to every job below.

1. **Inspect first. Edit second.**
2. **Do not replace the phone or PC shell.** Add apps/pages into them.
3. **Do not create startup career modules unless specifically approved.** Previous Scrap Yard Direct career-module builds caused severe loading/freezing risk.
4. **Do not hand-roll BeamNG/RLS money, inventory, garage, insurance, or storage.** Use the existing game/RLS functions.
5. **Do not patch `vehicleShopping` at startup.** Career/shop data must be requested only when a page/app opens or when the approved bridge requests it.
6. **Only one FoxNet/Web Ecosystem ZIP may be installed during tests.** Duplicate zips with the same `ui/modModules/redfoxCareerWeb/` paths are invalid tests.
7. **Phone and PC must share the same bridge contract.** No separate guesswork bridge for PC.
8. **Every build must include TXT + HTML verification reports.** JSON alone is not enough.
9. **Runtime is unproven until David tests in BeamNG.** Do not write “fixed” unless the game test proves it.
10. **If a check fails, stop. Do not ship.**

---

## Known working / known bad facts

### Working or partially working

- The phone path can request RLS/BeamNG vehicle shopping data and open purchase flow from the FoxNet page.
- v0.10.3.1 phone side was the last known useful Scrap Yard/FoxNet baseline.
- BeamBook works as a standalone private-seller style injection pattern, but it lacks proper BeamBook branding/storefront polish.
- RLS PC marketplace can browse and buy cars using the game’s own marketplace flow.

### Broken / unsafe

- `RedFox_ScrapYard_Direct_v0_1_0.zip`
- `RedFox_ScrapYard_Direct_v0_1_1_ONLINE_ONLY_SAFE.zip`
- `RedFox_ScrapYard_Direct_v0_1_2_NO_EARLY_DEP_SAFE_TEST.zip`

Do not use those as a base. They tried to create a Scrap Yard career module and caused severe loading/freezing risk.

### Duplicate install warning

Do not install multiple versions of these at the same time:

- `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1...zip`
- `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7...zip`
- any other `zzzz_RedFox_FoxNet_Web_Ecosystem...zip`

They contain overlapping paths and can mix old/new files.

---

## Important incident reports / history

Chats should read these before editing anything related to Scrap Yard, phone, PC, or RLS bridge:

- `INCIDENT_REPORTS/2026-07-11_ScrapYard_Direct_RLS_Path_Ignored_Custom_Bridge_Failure.md`
- `INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`

---

# Job Board

Status values:

- `AVAILABLE`
- `CLAIMED`
- `BLOCKED`
- `READY_FOR_INTEGRATION`
- `DONE`
- `FAILED_STOPPED`

## JOB-00 — Coordinator / Integration / Verification

**Status:** AVAILABLE  
**Recommended chat:** 1 dedicated coordinator chat

### Owns

- This job board.
- Integration order.
- Final ZIP selection.
- Verification reports.
- Failure reports.
- Deciding when the rebuild can start or must stop.

### May edit

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- `PROJECT_MANIFESTS/*FoxNet*`
- `INCIDENT_REPORTS/*`
- final handoff/readme files

### Must not edit

- App code unless doing final approved integration.

### Acceptance test

- Every job has one owner.
- No two jobs claim the same code without coordination.
- Every final package has TXT + HTML verification reports and a file tree.

---

## JOB-01 — Phone + PC Platform Core

**Status:** AVAILABLE

### Goal

Make the phone and PC use the same app/page registration model and the same shared bridge contract.

### Owns

- Phone shell/app launcher.
- PC shell/browser/homepage.
- App/page registry.
- Shared navigation rules.
- Responsive phone-vs-PC layout rules.

### May edit

- `ui/modModules/redfoxCareerWeb/phone/`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
- `assets/js/icefox_front.js`
- shared registry files created for RedFox apps/pages

### Must not edit

- Scrap Yard page logic.
- BeamBook page logic.
- RLS marketplace logic.
- Career modules.

### Required output

A shared registry format like:

```json
{
  "id": "redfox.scrapyard",
  "name": "RedFox Scrap Yard",
  "type": "webapp",
  "phoneEnabled": true,
  "pcEnabled": true,
  "phonePath": "sites/scrap_yard/index.html",
  "pcPath": "sites/scrap_yard/index.html",
  "permissions": ["careerData", "vehicleShopping", "inventorySell"]
}
```

### Acceptance test

- Phone and PC list the same registered apps/pages where enabled.
- Phone layout and PC layout can differ, but backend messages are the same.
- Adding a new app should mean adding a manifest/registry entry, not editing five unrelated files.

---

## JOB-02 — Shared RLS / Career Bridge

**Status:** AVAILABLE

### Goal

Create one safe bridge contract that both phone and PC use.

### Owns

- Career data requests.
- Vehicle shopping data requests.
- Open stock purchase menu requests.
- Inventory/owned vehicle listing requests.
- Online sell requests.
- Logging prefixes.

### Required bridge messages

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

### Must use existing game/RLS functions

Known target functions to inspect and use when available:

```text
career_modules_vehicleShopping.updateVehicleList(true)
career_modules_vehicleShopping.getShoppingData()
career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)
career_modules_inventory.getVehicles()
career_modules_inventory.sellVehicleFromInventory(inventoryId)
career_modules_inventory.sellVehicle(inventoryId)
```

### Must not do

- No fake money.
- No fake storage insert.
- No hand-rolled vehicle spawn.
- No custom Scrap Yard career module.
- No startup marketplace patch.

### Acceptance test

- Same Scrap Yard page can run from phone or PC and receive the same data shape.
- Logs clearly say whether message came from PHONE, PC, VUE, BUY, SELL, or BRIDGE.

---

## JOB-03 — RedFox App Store / Play Store

**Status:** AVAILABLE

### Goal

Create a RedFox Play Store style app where apps/pages can be installed/enabled/disabled/opened.

### Owns

- App Store web page/app.
- App manifests.
- Installed/enabled state.
- Store categories.
- App cards, install/open/update buttons.
- Safe app fingerprinting rules.

### Store categories

- Vehicle Markets
- Services
- Jobs / Towing
- Garage / Storage
- Insurance / Finance
- Social / Messages
- Tools
- Games / Fun
- Experimental

### Required app manifest fields

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

### Safe fingerprinting rule

Use safe metadata only:

- `redfox_store/manifest.json`
- `info.json`
- `mod_info.json`
- ZIP comment
- preview PNG/JPG metadata
- harmless comments in files

Do not fingerprint by editing physics, controllers, JBeam behavior, or game-critical runtime files.

### Acceptance test

- Phone can open Store.
- PC can open Store.
- Store shows Scrap Yard, BeamBook, Import/Export, Classics as apps.
- Disabled apps do not appear in normal launcher unless store says enabled.

---

## JOB-04 — Scrap Yard / Wrecking Yard

**Status:** AVAILABLE

### Goal

Build the realistic Scrap Yard / Wrecking Yard page as an online store first, with future physical sell-point support.

### Owns

- Scrap Yard web page.
- Realistic wrecking-yard UI.
- Online buy listings.
- Online sell owned vehicles.
- Future sell-zone UI placeholder.

### Current required behavior

- Buy cars online from existing RLS/BeamNG shop data.
- Sell owned career inventory vehicles online.
- Use stock purchase/sell paths only.
- No startup career module.
- No map load work.
- No parking spot generation.

### Future sell-point idea

Any building can become a Scrap Yard sell point by placing a sell-circle prop/marker. Player drags/tows/trailers a vehicle into the circle, opens the Scrap Yard app, sees vehicles inside/above the circle, chooses which vehicle to sell.

Do not build the prop runtime until the web-only buy/sell path is stable.

### Acceptance test

- Phone page opens.
- PC page opens.
- Buy button opens stock/RLS purchase flow.
- Sell Online lists owned vehicles.
- Sell button calls stock inventory sell function.
- No old `redfoxScrapYardDirect` module exists in package.

---

## JOB-05 — BeamBook Marketplace

**Status:** AVAILABLE

### Goal

Turn BeamBook into a real Facebook/marketplace-style app and storefront without breaking its working core.

### Owns

- BeamBook web page.
- BeamBook marketplace storefront.
- Listing card UI.
- Seller/profile/post feel.
- Better branding so it does not just feel like generic Private Seller.

### Must preserve

BeamBook’s working order of operations:

- `util_configListGenerator.getEligibleVehicles()`
- `util_configListGenerator.getRandomVehicleInfos()`
- `career_modules_vehicleShopping.getVehiclesInShop()`
- `career_modules_vehicleShopping.getShoppingData()` patch pattern, only if proven safe in BeamBook itself

### Acceptance test

- BeamBook still works as before.
- Storefront says BeamBook Marketplace.
- Page looks social/marketplace style.
- Does not break stock purchase/storage flow.

---

## JOB-06 — Import / Export Yard

**Status:** AVAILABLE

### Goal

Create Import/Export as its own app/page first, then later a yard runtime.

### Phase 1

- Online import/export vehicle page.
- Decent vehicles, not pure scrap.
- Buy-now, not auction.
- Uses shared bridge and stock purchase path.

### Future gameplay

- Physical export yard sell point.
- Hotlist of 10 target vehicles like a Gone in 60 Seconds board.
- Sightings/notifications.
- Bring target vehicle to export yard.
- Sell/export for payout.

### Acceptance test

- Page exists as an installable app.
- No stolen/traffic sell logic until runtime is designed safely.
- Uses shared bridge only.

---

## JOB-07 — Classics / Collector Exchange

**Status:** AVAILABLE

### Goal

Convert Classics from auction style into a buy-now collector dealer page.

### Rules

- Old vehicles.
- Classics/muscle/collector/luxury/rare trims.
- Higher price, cleaner than Scrap Yard.
- No auction behavior for now.
- Uses stock purchase path.

### Acceptance test

- Page is buy-now.
- Page does not use Copart/auction flow.
- Page uses shared bridge and stock purchase.

---

## JOB-08 — Insurance / Finance / Garage / Storage Pages

**Status:** AVAILABLE

### Goal

Make the supporting pages that make buying/selling feel complete.

### Owns

- Insurance links/pages.
- Finance/loans/payments pages.
- Garage/storage status pages.
- Purchase flow help pages.

### Must not do

- Do not replace stock insurance/storage behavior.
- Do not fake garage inventory.

### Acceptance test

- Pages explain/status the real game/RLS state.
- Links flow naturally from vehicle buy/sell pages.

---

## JOB-09 — Tow / Recovery / Dispatch Integration

**Status:** CLAIMED  
**Claimed by:** RedFox Tow & Recovery Dispatch chat (Sol)  
**Claim date:** 2026-07-13

### Hello to the other RedFox chats

Hello, fellow RedFox chats. JOB-09 here. I own only tow/recovery/dispatch app links, recovery-job UI, and the future approved deliver-to-yard connection. I will not touch the phone/PC shell, shared Career bridge, App Store core, Scrap Yard core, Import/Export core, RLS files, or stock Career files. Please publish stable contracts and approved paths on this board; I will integrate against them only after the owning jobs are ready.

### Goal

Connect tow/recovery gameplay to Scrap Yard/Import Export later.

### Owns

- Tow call app links.
- Recovery job UI.
- Future “deliver to yard” flow.
- Integration planning for catalog mod 19, permanent module ID `redfox_tow_recovery_dispatch`.

### Files and folders this job will inspect

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- The four incident reports listed in this board before any FoxNet edit.
- The selected catalog-19 Tow/Recovery baseline and its verification reports.
- JOB-01 phone/PC registration contract when published.
- JOB-02 shared RLS/Career bridge contract when published.
- JOB-03 app manifest/store registration contract when published.
- JOB-04 Scrap Yard and JOB-06 Import/Export approved delivery/deep-link contracts when published.
- JOB-11 logging/test format when published.

### Files and folders this job may edit

- Standalone catalog-19 Tow/Recovery mod files only, including `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`, its own input actions, its own RedFox module manifest, metadata, documentation, and verification reports.
- A new job-scoped Tow/Recovery app directory only after JOB-01 and JOB-03 publish the approved registry and path. Expected scope: `ui/modModules/redfoxCareerWeb/sites/tow_recovery/`.
- A Tow/Recovery app manifest entry only at the exact path and schema published by JOB-03.
- This JOB-09 claim/status block in the job board.

### Protected files and folders this job must not edit

- Phone shell/app launcher files owned by JOB-01.
- PC shell/browser/homepage files owned by JOB-01.
- Shared bridge implementation files owned by JOB-02.
- App Store core, shared registry implementation, and other apps' manifests owned by JOB-03.
- Scrap Yard page/core files owned by JOB-04.
- BeamBook files owned by JOB-05.
- Import/Export page/core files owned by JOB-06.
- Classics, insurance, finance, garage, storage, and shared visual-theme files.
- RLS source, stock Career files, `career_modules_inventory`, or `career_modules_vehicleShopping`.
- Any startup-loaded Scrap Yard or Tow career module.

### Dependencies before building

- JOB-01 must publish the shared phone/PC app registration and navigation contract.
- JOB-02 must publish the shared RLS/Career bridge messages and data shapes.
- JOB-03 must publish the app manifest/permissions/install contract.
- JOB-04 and JOB-06 must define any approved yard delivery or deep-link endpoints.
- JOB-11 must publish the shared logging and failure-report format.
- No integrated FoxNet ZIP will be built until these dependencies are stable and JOB-00 approves integration.

### Must not do

- Do not edit Scrap Yard core.
- Do not create a yard sell prop until JOB-04 and JOB-02 are stable.
- Do not hijack or replace the phone, PC, shared bridge, RLS, money, inventory, garage, or storage systems.
- Do not hand-roll Career money or ownership for FoxNet integration.
- Do not claim live runtime success until David tests it in BeamNG.

### Verification plan

- Inspect and record the exact baseline before editing.
- Produce a colored side-by-side baseline diff.
- Scan all changed paths against the protected-file list.
- Parse Lua with Lua 5.1 grammar and validate every JSON/manifest.
- Verify permanent module ID, input actions, settings/state paths, and required Hub functions.
- Verify no startup Career module, stock/RLS override, fake money, or Career-inventory insertion is packaged.
- Reopen the final ZIP and verify root structure, file tree, duplicate paths, and required reports.
- Include TXT and HTML verification reports and clearly list unproven runtime items.

### Acceptance test

- App/page exists and can deep-link later.
- No shared file conflicts.
- Standalone Tow/Recovery gameplay continues to use normal Career payment APIs and separate temporary-yard state.
- Phone and PC links use the same shared contract without modifying either shell.

---

## JOB-10 — Visual Design / Real Website Polish

**Status:** AVAILABLE

### Goal

Make the pages look like real web pages, not debug panels.

### Owns

- CSS theme.
- Realistic page layouts.
- Icons/cards/buttons.
- Phone vs PC responsive appearance.
- App Store visual polish.

### Must not do

- Do not change bridge logic.
- Do not change purchase/sell behavior.
- Do not replace FoxFax art or other user-fixed assets unless specifically asked.

### Acceptance test

- Realistic phone and PC page mockups.
- No functional code broken.

---

## JOB-11 — QA / Logging / Failure Triage

**Status:** AVAILABLE

### Goal

Make testing and failure reporting simple.

### Owns

- Logging instructions.
- In-game debug page.
- Test matrix.
- Failure report template.
- How to collect BeamNG logs.

### Required log prefixes

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
```

### BeamNG log path

Current user path seen in logs:

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

### Search terms

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
```

### Acceptance test

- Every build includes `LOGGING_AND_TESTING_README.txt` and `.html`.
- Tester can tell phone vs PC failures apart.
- Tester can prove which ZIPs were installed.

---

# Integration order

Do not build everything at once.

1. JOB-00 Coordinator starts job assignment.
2. JOB-11 QA/logging creates shared test format.
3. JOB-01 Platform and JOB-02 Bridge define shared app/page contract.
4. JOB-03 Store creates app registry and store page.
5. JOB-04 Scrap Yard builds on shared bridge.
6. JOB-05 BeamBook builds on shared bridge/store.
7. JOB-06 Import/Export builds page only.
8. JOB-07 Classics builds page only.
9. JOB-08 and JOB-09 connect support pages and tow links.
10. JOB-10 polishes visuals after functions are stable.

---

# App Store / Play Store target behavior

The RedFox Store should feel like a real phone app store.

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

## App card buttons

- Install
- Enable
- Disable
- Open
- Update
- View permissions
- View logs

## App permissions

Apps must declare permissions before using them:

- `careerData`
- `vehicleShopping`
- `inventorySell`
- `notifications`
- `mapLocation`
- `yardSellZone`
- `experimentalProps`

## Phone/PC behavior

- Phone Store installs/enables phone apps.
- PC Store installs/enables PC pages.
- Same app can support both.
- A disabled app should stay installed but hidden from launcher/home unless Store shows it.

---

# Testing checklist for all future ZIPs

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

# Current first message to send to every new chat

Copy/paste this:

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read this GitHub job board first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md

Pick exactly one AVAILABLE job. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports.
```

---

# Current stop condition

If any chat tries to add a new `lua/ge/extensions/career/modules/redfoxScrapYardDirect.lua` or any startup-loaded Scrap Yard career module, stop that chat. That approach already caused severe loading/freezing risk.
