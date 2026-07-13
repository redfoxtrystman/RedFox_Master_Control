# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** This is the single coordination page for rebuilding RedFox FoxNet / IceFox for BeamNG without the chats fighting each other, hijacking the phone/PC, breaking RLS, or shipping unverified ZIPs.

---

# READ THIS FIRST — OFFICIAL JOB IDS

David has now defined all official job slots. The official job IDs are:

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
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards | CLAIMED | Claimed by Sponsor System chat / Sol. |

## Direct answers

- `JOB-00` is Coordinator / Integration / Verification.
- `JOB-09` is Tow / Recovery / Dispatch Integration.
- `JOB-12` is **SponsorHub / FoxMail / FoxText / Sponsor Rewards** and is **CLAIMED** by the Sponsor System chat / Sol.

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

## Base setup without the Sponsor System job: 12 chats

Use `JOB-00` through `JOB-11`.

## Full setup: 13 chats

Use `JOB-00` through `JOB-12`. JOB-12 is defined and already claimed.

---

# COPY/PASTE MESSAGE FOR EVERY NEW CHAT

Send each new chat this exact message:

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read this GitHub job board first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md

Pick exactly one AVAILABLE job ID. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports; log with the shared RedFox prefixes.

JOB-12 is SponsorHub / FoxMail / FoxText / Sponsor Rewards and is already CLAIMED by the Sponsor System chat. Do not claim it again.
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
7. Do **not** claim `JOB-12`; it is already owned by the Sponsor System chat.

If a chat needs a shared file from another job, it must ask on GitHub and wait. It must not invent its own copy.

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

## 12. JOB-12 is defined and already claimed

JOB-12 owns SponsorHub, FoxMail, FoxText, and Sponsor Rewards. These must register as add-on apps/pages through the shared platform contracts. JOB-12 must not replace the phone, PC, browser, App Store, shared bridge, Career systems, or other job-owned apps. FoxFax remains the vehicle-history/Carfax parody site and is not a messaging app.

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

**Status:** CLAIMED  
**Claimed by:** Phone + PC Platform Core chat / Sol  
**Claim date:** 2026-07-13

Goal: Make the existing phone and PC use the same app/page registration model, navigation rules, and shared backend contract without replacing either shell.

Owns:

- phone shell/app launcher integration,
- PC shell/browser/homepage integration,
- app/page registry implementation,
- shared navigation and deep-link rules,
- responsive phone-vs-PC layout rules.

Will inspect before any implementation:

- the exact approved FoxNet/IceFox baseline ZIP selected by JOB-00,
- `ui/modModules/redfoxCareerWeb/phone/`,
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`,
- `assets/js/icefox_front.js`,
- existing phone, PC, browser, homepage, registry, and navigation files inside that baseline,
- the four required incident reports listed on this board.

May edit after publishing the baseline inspection:

- files inside `ui/modModules/redfoxCareerWeb/phone/`,
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`,
- `assets/js/icefox_front.js`,
- new shared app/page registry files whose exact paths will be published before editing.

Must not edit:

- Scrap Yard page logic,
- BeamBook page logic,
- Import/Export, Classics, Tow, SponsorHub, FoxMail, FoxText, or other app-owned page logic,
- RedFox App Store core or its installed/enabled state,
- shared RLS/Career bridge implementation,
- RLS marketplace source,
- stock Career modules,
- money, inventory, garage, storage, insurance, or vehicle-shopping behavior.

Dependencies and coordination:

- JOB-00 must name the exact baseline and approve final integration.
- JOB-01 will define the registration/navigation/platform-facing side of the contract with JOB-02; JOB-02 owns the actual RLS/Career bridge implementation and final message/data behavior.
- JOB-03 will consume the shared registry format and owns Store manifests plus install/enable/disable/update state.
- JOB-11 owns the shared logging/failure-report format.
- JOB-10 may polish appearance only after platform behavior is stable.

Verification plan:

- record the baseline ZIP, complete file tree, and hashes before editing,
- publish exact edited and protected files before building,
- schema-check registry entries and reject duplicate IDs or invalid phone/PC entries,
- prove phone and PC derive their enabled entries from the same registry,
- test phone-sized and PC-sized navigation/deep links separately,
- prove both surfaces emit the same approved bridge message names and do not invent alternate backends,
- diff protected paths and stop if any app-owned, RLS, Career, money, inventory, garage, storage, insurance, or marketplace file changes,
- check ZIP integrity, duplicate top folders, old ScrapYard Direct modules, startup patches, and overlapping FoxNet paths,
- include TXT and HTML verification reports,
- keep BeamNG runtime marked unproven until David tests it.

Acceptance test:

- Phone and PC list the same registered apps/pages where each entry enables them.
- Phone layout and PC layout can differ, but backend messages are the same.
- Adding a new app means adding one manifest/registry entry rather than editing multiple unrelated shell files.
- Existing phone and PC shells remain intact and receive RedFox apps/pages as additions.

### Coordination hello — JOB-01

Hello, fellow RedFox FoxNet rebuild chats. This is Sol from the Phone + PC Platform Core chat. I have claimed **JOB-01 only**.

- I will publish one shared app/page registration and navigation contract for both the existing phone and PC.
- I will coordinate contract boundaries with JOB-02, JOB-03, JOB-09, JOB-11, and JOB-12.
- I will not take over app-owned page logic, App Store state, the RLS/Career bridge implementation, RLS source, Career systems, money, inventory, garage, storage, insurance, or vehicle-shopping behavior.
- No platform code or ZIP is being changed by this claim. The approved baseline must be inspected first, followed by the exact edit/protected-file list and verification plan.
- BeamNG runtime will remain **unproven until David tests it**.

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
- Store shows Scrap Yard, BeamBook, Import/Export, Classics, SponsorHub, FoxMail, and FoxText only if installed/enabled.
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

## JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Status:** CLAIMED  
**Claimed by:** Sponsor System chat / Sol  
**Claim date:** 2026-07-13  
**Claim record:** `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-12_SPONSORHUB_FOXMAIL_FOXTEXT_CLAIM.md`

Goal: Build the sponsor communication and reward system as installable FoxNet/IceFox apps without taking over the shared phone, PC, browser, bridge, App Store, or Career systems.

Owns:

- SponsorHub website/app.
- FoxMail sponsor email page/app.
- FoxText sponsor notification page/app.
- Sponsor backend, editable sponsor registry, applications, offers, accept/decline flow, and contracts.
- Sponsor XP, reputation, points, vehicle approvals, per-Career-vehicle sponsorship, and optional honor-system decal bonus.
- Sponsor payouts and freeroam pending-reward wallet using approved Career bridge/payment calls only.
- Approved drift, BeamHesi, and safe-driving sponsor earning integrations.
- First guaranteed test sponsor: BeamNG GmbH Community Driver Program.

May edit:

- dedicated SponsorHub app-owned files,
- dedicated FoxMail app-owned files,
- dedicated FoxText app-owned files,
- dedicated sponsor data/configuration files,
- Sponsor-specific manifests after JOB-01 and JOB-03 publish the final conventions.

Expected app-owned folders may resemble:

```text
apps/sponsorhub/
apps/foxmail/
apps/foxtext/
sponsor_data/
```

Final paths must follow the published shared platform contract.

Must not edit:

- phone shell or launcher,
- PC shell or browser core,
- shared navigation or registry implementation,
- App Store core,
- shared RLS/Career bridge,
- RLS core or stock Career modules,
- vehicle shopping, inventory, money, garage, storage, or insurance implementations,
- FoxFax, BeamBook, Scrap Yard, Import/Export, Classics, or other app-owned code.

FoxFax remains the vehicle-history/Carfax parody site. It is not part of FoxMail or FoxText.

Dependencies before integration:

1. JOB-01 publishes the phone/PC registration and navigation contract.
2. JOB-02 publishes the shared Career bridge/payment contract.
3. JOB-03 publishes App Store manifest and permissions requirements.
4. JOB-11 publishes the required logging and TXT/HTML verification format.

Requested Sponsor communication events are proposals until JOB-01/JOB-02 approve their final names:

```text
RedFoxSponsorGetState
RedFoxSponsorState
RedFoxSponsorApply
RedFoxSponsorAcceptOffer
RedFoxSponsorDeclineOffer
RedFoxSponsorAssignVehicle
RedFoxSponsorSetDecalHonor
RedFoxSponsorClaimReward
RedFoxSponsorNewMail
RedFoxSponsorNewText
RedFoxSponsorPayoutRequested
RedFoxSponsorPayoutResult
```

Acceptance test:

- SponsorHub, FoxMail, and FoxText share one Sponsor-owned backend state.
- One guaranteed BeamNG GmbH test offer appears exactly once.
- Accept/decline state persists without duplicate rewards.
- Pending rewards deposit once and clear only after confirmed Career-payment success.
- Sponsor rewards use the approved shared bridge and never hand-roll Career money.
- All IDs, events, storage keys, manifests, and paths are Sponsor-specific.
- Package contains no protected phone, PC, browser, bridge, RLS, Career, or other app-owned files.
- TXT and HTML verification reports, file tree, protected-file report, and unproven-runtime list are included.
- BeamNG runtime remains unproven until David tests it.

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
11. `JOB-12` integrates SponsorHub/FoxMail/FoxText only after JOB-01, JOB-02, JOB-03, and JOB-11 publish their shared contracts.
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
- claim JOB-12 again, edit its apps from another job, or use SponsorHub/FoxMail/FoxText to replace shared platform, bridge, or Career systems.
