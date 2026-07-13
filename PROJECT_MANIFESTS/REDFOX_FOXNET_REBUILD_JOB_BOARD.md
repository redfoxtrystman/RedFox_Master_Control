# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** This is the single coordination page for rebuilding RedFox FoxNet / IceFox for BeamNG without the chats fighting each other, hijacking the phone/PC, breaking RLS, or shipping unverified ZIPs.

---

# READ THIS FIRST — OFFICIAL JOB IDS

The only official job numbers are `JOB-00` through `JOB-11`.

Do **not** translate `JOB-09` into “the ninth chat.”  
Do **not** renumber jobs based on how many chats David opens.

## Official job map

| Job ID | Job name | Status | Owner / notes |
|---|---|---|---|
| JOB-00 | Coordinator / Integration / Verification | AVAILABLE | Assigns jobs, verifies integration |
| JOB-01 | Phone + PC Platform Core | AVAILABLE | Owns phone/PC app/page shells |
| JOB-02 | Shared RLS / Career Bridge | AVAILABLE | Owns shared bridge contract only |
| JOB-03 | RedFox App Store / Play Store | AVAILABLE | Owns install/enable/open/update app store |
| JOB-04 | Scrap Yard / Wrecking Yard | AVAILABLE | Online buy/sell page first |
| JOB-05 | BeamBook Marketplace | AVAILABLE | BeamBook social/marketplace storefront |
| JOB-06 | Import / Export Yard | AVAILABLE | Import/export online page first |
| JOB-07 | Classics / Collector Exchange | AVAILABLE | Buy-now collector/classic page |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | AVAILABLE | Support/status pages only |
| JOB-09 | Tow / Recovery / Dispatch Integration | CLAIMED | Claimed by Tow/Recovery/Dispatch chat |
| JOB-10 | Visual Design / Real Website Polish | AVAILABLE | CSS/layout/art only |
| JOB-11 | QA / Logging / Failure Triage | AVAILABLE | Logging, testing matrix, failure reports |

**Direct answer:** `JOB-09` is **Tow / Recovery / Dispatch Integration**.

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

## Ideal full setup: 12 chats

Use all official job IDs from `JOB-00` through `JOB-11`.

The four extra beyond the minimum are:

- `JOB-07` — Classics / Collector Exchange
- `JOB-08` — Insurance / Finance / Garage / Storage Pages
- `JOB-09` — Tow / Recovery / Dispatch Integration
- `JOB-10` — Visual Design / Real Website Polish

---

# COPY/PASTE MESSAGE FOR EVERY NEW CHAT

Send each new chat this exact message:

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read this GitHub job board first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md

Pick exactly one AVAILABLE job ID. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports; log with the shared RedFox prefixes.
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

If a chat needs a shared file from another job, it must ask on GitHub and wait. It must not invent its own copy.

---

# RULES OF OPERATIONS — EVERY CHAT MUST FOLLOW

## 1. Inspect first, edit second

No chat may jump straight to building. It must inspect the baseline and list exact planned edits first.

## 2. One job, one scope

A chat owns only its job. It may not fix phone, PC, bridge, app store, Scrap Yard, BeamBook, Import/Export, Classics, QA, or visuals unless that is its claimed job.

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

**Status:** AVAILABLE

Owns assignment, this board, integration order, final ZIP selection, failure reports, and final verification.

May edit:

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/*FoxNet*
INCIDENT_REPORTS/*
final handoff/readme files
```

Must not edit app code unless doing final approved integration.

Acceptance:

- Every job has one owner.
- No two jobs claim the same files.
- Final ZIP has TXT + HTML reports, file tree, and logging readme.

---

## JOB-01 — Phone + PC Platform Core

**Status:** AVAILABLE

Owns phone shell, PC shell, app/page launcher, shared registry loading, responsive phone-vs-PC behavior.

May edit:

```text
ui/modModules/redfoxCareerWeb/phone/
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
assets/js/icefox_front.js
shared app/page registry files
```

Must not edit Scrap Yard, BeamBook, Import/Export, Classics page logic, bridge logic, or career modules.

Acceptance:

- Phone and PC list the same enabled apps/pages.
- Adding an app uses a registry/manifest entry.
- Phone and PC do not use separate backend message contracts.

---

## JOB-02 — Shared RLS / Career Bridge

**Status:** AVAILABLE

Owns shared bridge messages and data shapes for phone and PC.

Must not create startup career modules, fake money, fake storage, fake garage, or custom Scrap Yard career modules.

Acceptance:

- Same page can run from phone or PC and receive the same data shape.
- Logs identify PHONE, PC, BRIDGE, BUY, SELL, VUE/CEF path.

---

## JOB-03 — RedFox App Store / Play Store

**Status:** AVAILABLE

Owns store page/app, app manifests, installed/enabled state, app cards, permissions, install/open/update/disable buttons.

Acceptance:

- Store opens on phone and PC.
- Store lists Scrap Yard, BeamBook, Import/Export, Classics.
- Disabled apps hide from launcher/home but remain visible in Store.

---

## JOB-04 — Scrap Yard / Wrecking Yard

**Status:** AVAILABLE

Owns realistic wrecking-yard page, online buy listings, online sell owned vehicles, and future sell-zone UI placeholder.

Current required behavior:

- Online store first.
- Buy from existing RLS/BeamNG shop data.
- Sell owned career inventory vehicles online.
- Use stock purchase/sell paths only.
- No startup career module.
- No map-load work.
- No parking spot generation.

Future sell point:

Any building can become a Scrap Yard sell point by placing a sell-circle prop/marker. Player drags/tows/trailers a vehicle into the circle, opens the Scrap Yard app, sees vehicles inside/above the circle, and chooses which vehicle to sell.

Do not build the prop runtime until web-only buy/sell path and shared bridge are stable.

Acceptance:

- Phone Scrap Yard opens.
- PC Scrap Yard opens.
- Buy button opens stock/RLS purchase flow.
- Sell Online lists owned vehicles.
- Sell button calls stock inventory sell function.
- No `redfoxScrapYardDirect` career module exists in the ZIP.

---

## JOB-05 — BeamBook Marketplace

**Status:** AVAILABLE

Owns BeamBook social/Facebook-style page and marketplace storefront.

Must preserve BeamBook’s working order of operations and avoid breaking stock purchase/storage.

Acceptance:

- BeamBook still works.
- Page says BeamBook Marketplace.
- Listings feel like posts/sellers instead of generic Private Seller only.

---

## JOB-06 — Import / Export Yard

**Status:** AVAILABLE

Phase 1 only:

- Online import/export vehicle page.
- Decent vehicles, not pure scrap.
- Buy-now, not auction.
- Uses shared bridge and stock purchase path.

Future:

- Physical export yard sell point.
- Hotlist of 10 target vehicles like a Gone in 60 Seconds board.
- Sightings/notifications.
- Bring target vehicle to export yard.
- Sell/export for payout.

Acceptance:

- Page exists as installable app.
- No stolen/traffic sell logic until runtime is designed safely.
- Uses shared bridge only.

---

## JOB-07 — Classics / Collector Exchange

**Status:** AVAILABLE

Convert Classics from auction style into a buy-now collector dealer page.

Rules:

- Old vehicles.
- Classics/muscle/collector/luxury/rare trims.
- Higher price, cleaner than Scrap Yard.
- No auction behavior for now.
- Uses stock purchase path.

Acceptance:

- Page is buy-now.
- Page does not use Copart/auction flow.
- Page uses shared bridge and stock purchase.

---

## JOB-08 — Insurance / Finance / Garage / Storage Pages

**Status:** AVAILABLE

Owns supporting pages that explain or show real game/RLS state for insurance, finance, garage, and storage.

Must not replace stock insurance/storage behavior or fake garage inventory.

Acceptance:

- Pages link naturally from vehicle buy/sell pages.
- Pages do not fake game state.

---

## JOB-09 — Tow / Recovery / Dispatch Integration

**Status:** CLAIMED  
**Claimed by:** RedFox Tow & Recovery Dispatch chat  
**Claim date:** 2026-07-13

Owns tow call app links, recovery job UI, and future approved deliver-to-yard connection.

Must not edit Scrap Yard core, phone shell, PC shell, bridge core, app store core, RLS source, stock Career files, money, inventory, garage, storage, or startup career modules.

Dependencies before building integrated FoxNet work:

- `JOB-01` publishes app/page registration.
- `JOB-02` publishes bridge contract.
- `JOB-03` publishes app manifest/store rules.
- `JOB-04` and `JOB-06` publish approved delivery/deep-link endpoints.
- `JOB-11` publishes logging/test format.

Acceptance:

- App/page exists and can deep-link later.
- No shared file conflicts.
- No fake money or inventory insertion.

---

## JOB-10 — Visual Design / Real Website Polish

**Status:** AVAILABLE

Owns CSS theme, realistic layouts, icons/cards/buttons, phone vs PC visual polish, and Store polish.

Must not change bridge logic, purchase/sell behavior, or user-fixed FoxFax art unless David specifically asks.

Acceptance:

- Pages look like real web pages.
- No functional code broken.

---

## JOB-11 — QA / Logging / Failure Triage

**Status:** AVAILABLE

Owns test matrix, log instructions, failure report template, debug/log page, and install-cleanliness checklist.

Acceptance:

- Every build includes logging readme TXT + HTML.
- Tester can tell phone vs PC failures apart.
- Tester can prove which ZIPs were installed.

---

# INTEGRATION ORDER

Do not build everything at once.

1. `JOB-00` assigns/coordinates.
2. `JOB-11` defines logging and failure-report format.
3. `JOB-01` and `JOB-02` publish shared phone/PC registration and bridge contracts.
4. `JOB-03` builds Store/app manifest system.
5. `JOB-04` builds Scrap Yard using shared bridge.
6. `JOB-05` builds BeamBook using shared bridge/store.
7. `JOB-06` builds Import/Export page using shared bridge/store.
8. `JOB-07` builds Classics page using shared bridge/store.
9. `JOB-08` and `JOB-09` connect support pages and tow links after core contracts are stable.
10. `JOB-10` polishes visuals after functions are stable.

---

# BUILD TEST CHECKLIST FOR EVERY ZIP

Every build report must state:

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

---

# STOP CONDITIONS

Stop immediately if any chat:

- adds `lua/ge/extensions/career/modules/redfoxScrapYardDirect.lua`,
- adds a startup-loaded Scrap Yard career module,
- patches `vehicleShopping` at startup,
- hand-rolls money/storage/garage/insurance,
- edits outside its claimed job,
- ships without TXT + HTML reports,
- claims runtime success without David testing in BeamNG,
- packages duplicate old FoxNet paths without explaining migration.
