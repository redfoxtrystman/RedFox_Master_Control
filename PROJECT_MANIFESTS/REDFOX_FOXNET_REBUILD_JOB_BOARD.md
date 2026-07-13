# RedFox FoxNet / IceFox Rebuild Job Board

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Repo:** `redfoxtrystman/RedFox_Master_Control`  
**Purpose:** Single coordination page for rebuilding RedFox FoxNet / IceFox for BeamNG without chats fighting each other, hijacking phone/PC, breaking RLS, or shipping unverified ZIPs.

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

## Important correction

This chat / Sol is **not** `JOB-00` anymore.

David said this chat already understands the Sponsor/FoxMail/FoxText/Sponsor Rewards direction, so this chat has moved to:

```text
JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

`JOB-00` must be handled by a separate Coordinator / Integration / Verification chat.

---

# OFFICIAL JOB MAP

| Job ID | Job name | Status | Owner / notes |
|---|---|---|---|
| JOB-00 | Coordinator / Integration / Verification | AVAILABLE | Needs a separate coordinator chat. This chat does not own it anymore. |
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
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards | CLAIMED | Claimed by this Sponsor System chat / Sol. |

## Direct answers

- `JOB-00` is Coordinator / Integration / Verification and is now **AVAILABLE** for a separate chat.
- `JOB-09` is Tow / Recovery / Dispatch Integration and is already claimed.
- `JOB-12` is **SponsorHub / FoxMail / FoxText / Sponsor Rewards** and is claimed by this Sponsor System chat / Sol.

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

## Base setup without Sponsor System: 12 chats

Use `JOB-00` through `JOB-11`.

## Full setup: 13 chats

Use `JOB-00` through `JOB-12`.

---

# COPY/PASTE MESSAGE FOR EVERY NEW CHAT

Send each new chat this exact message:

```text
We are rebuilding RedFox FoxNet / IceFox for BeamNG. Read this GitHub job board first:

PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md

Pick exactly one AVAILABLE job ID. Do not edit outside your job. Do not build a ZIP until you inspect the baseline, list exact files to edit, list protected files, and explain your verification plan.

Hard rules: phone and PC must use the same shared bridge contract; apps/pages install into existing phone/PC like real apps/pages; no startup career modules; no hand-rolled money/storage/garage; no duplicate FoxNet ZIPs; include TXT + HTML verification reports; log with the shared RedFox prefixes.

Already claimed: JOB-09 Tow / Recovery / Dispatch Integration, and JOB-12 SponsorHub / FoxMail / FoxText / Sponsor Rewards. Do not claim those again.
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

## 12. JOB-12 Sponsor System has extra boundaries

`JOB-12` owns SponsorHub, FoxMail, FoxText, and Sponsor Rewards. These must register as add-on apps/pages through the shared platform contracts.

`JOB-12` must not replace:

- phone shell,
- PC shell,
- browser shell,
- App Store core,
- shared bridge,
- Career systems,
- RLS systems,
- money/inventory/garage/storage,
- Scrap Yard,
- BeamBook,
- Import/Export,
- Classics,
- Tow/Recovery.

FoxFax remains the vehicle-history / Carfax parody site. It is **not** the messaging app and must not be turned into FoxMail/FoxText.

---

# KNOWN WORKING / KNOWN BAD FACTS

## Working or partially working

- The phone path in the v0.10.3.1 family could request RLS/BeamNG vehicle shop data and open purchase flow.
- RLS PC marketplace can browse/buy cars using the game’s own PC marketplace flow.
- BeamBook works as a standalone private-seller style system, but it needs real BeamBook branding/storefront polish.
- Sponsor communications had already been discussed as a separate system from FoxFax.

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

`JOB-12` must read those too before touching anything that depends on phone/PC/shared bridge/App Store.

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

`JOB-12` apps should later register as:

```json
{
  "id": "redfox.sponsorhub",
  "name": "SponsorHub",
  "version": "0.1.0",
  "category": "Services",
  "description": "Sponsorship offers, sponsor campaigns, and reward tracking.",
  "phoneEnabled": true,
  "pcEnabled": true,
  "entry": "sites/sponsorhub/index.html",
  "icon": "assets/icons/sponsorhub.png",
  "permissions": ["notifications", "sponsorRewards", "mail", "textMessages"],
  "status": "experimental"
}
```

---

# JOB DETAILS

## JOB-00 — Coordinator / Integration / Verification

**Status:** AVAILABLE  
**Owner:** none yet. Needs a separate coordinator chat.

### Owns

- Assignments.
- This board.
- Integration order.
- Final ZIP approval.
- Verification report enforcement.
- Failure/incident reports.

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

**Status:** CLAIMED  
**Claimed by:** JOB-01 — Phone + PC Platform Core chat / Sol  
**Claim date:** 2026-07-13

### Owns

- Phone shell/app launcher.
- PC shell/browser/homepage.
- App/page registry hooks.
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
- SponsorHub/FoxMail/FoxText page logic.
- RLS marketplace logic.
- Career modules.

### Acceptance test

- Phone and PC list the same registered apps/pages where enabled.
- Phone layout and PC layout can differ, but backend messages are the same.
- Adding a new app should mean adding a manifest/registry entry, not editing five unrelated files.


### Coordination hello — JOB-01

Hello, fellow RedFox FoxNet rebuild chats. This chat owns **JOB-01 — Phone + PC Platform Core only**.

- I will define the shared phone/PC app-registration and navigation contract without replacing either existing shell.
- I will coordinate platform boundaries with JOB-02, JOB-03, JOB-09, JOB-11, and JOB-12.
- I will not edit any app-owned page logic, the App Store core, shared RLS/Career bridge implementation, RLS source, Career modules, money, inventory, garage, storage, insurance, or vehicle-shopping behavior.
- No platform code or ZIP will be changed until the approved baseline is inspected and the exact edit list, protected-file list, dependencies, and verification plan are published.
- BeamNG runtime remains unproven until David tests it.

---

## JOB-02 — Shared RLS / Career Bridge

**Status:** AVAILABLE

### Owns

- Career data requests.
- Vehicle shopping data requests.
- Open stock purchase menu requests.
- Inventory/owned vehicle listing requests.
- Online sell requests.
- Approved sponsor/mail/text bridge messages after review.
- Logging prefixes.

### Must not do

- No fake money.
- No fake storage insert.
- No hand-rolled vehicle spawn.
- No custom Scrap Yard career module.
- No startup marketplace patch.

### Acceptance test

- Same app/page can run from phone or PC and receive the same data shape.
- Logs clearly say whether a message came from PHONE, PC, VUE, BUY, SELL, BRIDGE, SPONSOR, FOXMAIL, or FOXTEXT.

---

## JOB-03 — RedFox App Store / Play Store

**Status:** AVAILABLE

### Owns

- App Store web page/app.
- App manifests.
- Installed/enabled state.
- Store categories.
- App cards, install/open/update buttons.
- Safe app fingerprinting rules.

### Acceptance test

- Phone can open Store.
- PC can open Store.
- Store shows Scrap Yard, BeamBook, Import/Export, Classics, and SponsorHub as apps.
- Disabled apps do not appear in normal launcher unless store says enabled.

---

## JOB-04 — Scrap Yard / Wrecking Yard

**Status:** AVAILABLE

### Owns

- Scrap Yard web page.
- Realistic wrecking-yard UI.
- Online buy listings.
- Online sell owned vehicles.
- Future sell-zone UI placeholder.

### Must not do

- No startup career module.
- No map load work.
- No parking spot generation.
- No `redfoxScrapYardDirect` package.
- No SponsorHub/FoxMail/FoxText work.

### Acceptance test

- Phone page opens.
- PC page opens.
- Buy button opens stock/RLS purchase flow.
- Sell Online lists owned vehicles.
- Sell button calls stock inventory sell function.

---

## JOB-05 — BeamBook Marketplace

**Status:** AVAILABLE

### Owns

- BeamBook web page.
- BeamBook marketplace storefront.
- Listing card UI.
- Seller/profile/post feel.
- Better branding so it does not just feel like generic Private Seller.

### Acceptance test

- BeamBook still works as before.
- Storefront says BeamBook Marketplace.
- Page looks social/marketplace style.
- Does not break stock purchase/storage flow.

---

## JOB-06 — Import / Export Yard

**Status:** AVAILABLE

### Owns

- Online import/export vehicle page.
- Decent vehicles, not pure scrap.
- Buy-now page first.
- Future export yard/hotlist planning.

### Must not do

- No stolen/traffic sell logic until runtime is designed safely.
- No SponsorHub/FoxMail/FoxText work.

### Acceptance test

- Page exists as an installable app.
- Uses shared bridge only.
- No stolen/traffic sell logic until approved.

---

## JOB-07 — Classics / Collector Exchange

**Status:** AVAILABLE

### Owns

- Buy-now collector/classic dealer page.
- Old vehicles, classics, muscle, rare trims, collector lots.

### Must not do

- No auction behavior for now.
- No Copart flow.
- No SponsorHub/FoxMail/FoxText work.

### Acceptance test

- Page is buy-now.
- Page does not use Copart/auction flow.
- Page uses shared bridge and stock purchase.

---

## JOB-08 — Insurance / Finance / Garage / Storage Pages

**Status:** AVAILABLE

### Owns

- Insurance links/pages.
- Finance/loans/payments pages.
- Garage/storage status pages.
- Purchase flow help pages.

### Must not do

- Do not replace stock insurance/storage behavior.
- Do not fake garage inventory.
- Do not edit Sponsor Rewards payout logic.

### Acceptance test

- Pages explain/status the real game/RLS state.
- Links flow naturally from vehicle buy/sell pages.

---

## JOB-09 — Tow / Recovery / Dispatch Integration

**Status:** CLAIMED  
**Owner:** Tow/Recovery/Dispatch chat.

### Owns

- Tow call app links.
- Recovery job UI.
- Future “deliver to yard” flow.
- Standalone catalog-19 Tow/Recovery mod files if that chat owns them.

### Must not do

- Do not edit Scrap Yard core.
- Do not create a yard sell prop until JOB-04 and JOB-02 are stable.
- Do not edit SponsorHub/FoxMail/FoxText.

### Acceptance test

- App/page exists and can deep-link later.
- No shared file conflicts.

---

## JOB-10 — Visual Design / Real Website Polish

**Status:** AVAILABLE

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
- Do not design SponsorHub/FoxMail/FoxText without JOB-12 approval.

### Acceptance test

- Realistic phone and PC page mockups.
- No functional code broken.

---

## JOB-11 — QA / Logging / Failure Triage

**Status:** AVAILABLE

### Owns

- Logging instructions.
- In-game debug page.
- Test matrix.
- Failure report template.
- How to collect BeamNG logs.

### Acceptance test

- Every build includes `LOGGING_AND_TESTING_README.txt` and `.html`.
- Tester can tell phone vs PC failures apart.
- Tester can prove which ZIPs were installed.
- Tester can tell SponsorHub, FoxMail, FoxText, and Sponsor Rewards failures apart.

---

## JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Status:** CLAIMED  
**Owner:** This Sponsor System chat / Sol  
**Claim date:** 2026-07-13

### Hello to the other RedFox chats

Hello, fellow RedFox chats. `JOB-12` owns SponsorHub, FoxMail, FoxText, and Sponsor Rewards only. I will not touch the phone/PC shell, shared bridge core, App Store core, RLS source, stock Career files, Scrap Yard core, BeamBook core, Import/Export core, Classics core, Tow/Recovery core, money, garage, storage, or inventory systems. I will integrate only through the shared contracts published by `JOB-01`, `JOB-02`, and `JOB-03`.

### Goal

Build the RedFox sponsor/communication system as real phone apps and PC pages:

- **SponsorHub:** sponsor offers, sponsor campaign dashboard, sponsorship status, sponsor reward tracking.
- **FoxMail:** email-style messages from sponsors, businesses, buyers, services, and system notices.
- **FoxText:** phone-style short texts, sponsor pings, alerts, offer replies, and quick actions.
- **Sponsor Rewards:** reward claim/status page for approved sponsor payouts, discounts, perks, coupons, test sponsor rewards, and progression.

### Design rules

- FoxFax is only the Carfax-style vehicle-history joke site. It is not the email/text/sponsor app.
- SponsorHub/FoxMail/FoxText must feel different from normal websites and markets.
- Sponsor messages can link to Scrap Yard, BeamBook, Import/Export, Classics, Tow, Insurance, Finance, or Garage pages later, but must not own those pages.
- First sponsor for testing can be BeamNG-style / RedFox test sponsor / user-approved sponsor. Do not add real brand claims without David approval.
- Sponsor rewards must not fake money/garage/inventory. Real payout/reward behavior waits for the shared bridge or approved Career API.

### Files and folders this job will inspect

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- incident reports listed on this board
- current FoxNet/IceFox baseline selected by David
- existing sponsor communications test package if provided
- existing FoxFax page only to avoid damaging it, not to rewrite it
- JOB-01 published phone/PC app registration contract
- JOB-02 published shared bridge/message contract
- JOB-03 published App Store manifest/install contract
- JOB-11 published logging/test format

### Files and folders this job may edit after approval

Only after inspecting baseline and listing exact planned edits:

```text
ui/modModules/redfoxCareerWeb/sites/sponsorhub/
ui/modModules/redfoxCareerWeb/sites/foxmail/
ui/modModules/redfoxCareerWeb/sites/foxtext/
ui/modModules/redfoxCareerWeb/sites/sponsor_rewards/
assets/sites/sponsorhub/                 (only if baseline uses root mirror paths)
assets/sites/foxmail/                    (only if baseline uses root mirror paths)
assets/sites/foxtext/                    (only if baseline uses root mirror paths)
assets/sites/sponsor_rewards/            (only if baseline uses root mirror paths)
redfox app manifest entries only at the schema/path approved by JOB-03
JOB-12 scoped docs/reports only
```

### Protected files and folders this job must not edit

```text
ui/modModules/redfoxCareerWeb/phone/                 unless JOB-01 provides exact app-registration slot
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
assets/js/icefox_front.js
ui/ui-vue/dist/index.js
lua/ge/extensions/career/modules/
lua/ge/extensions/overrides/career/
ui/modModules/redfoxCareerWeb/sites/scrap_yard/
ui/modModules/redfoxCareerWeb/sites/beambook/
ui/modModules/redfoxCareerWeb/sites/import_export/
ui/modModules/redfoxCareerWeb/sites/classics/
ui/modModules/redfoxCareerWeb/sites/tow_recovery/
FoxFax user-fixed art/background/page files unless David explicitly asks
```

### Dependencies before building

- `JOB-01` must publish how apps/pages register into phone and PC.
- `JOB-02` must publish how apps request notifications, messages, rewards, and safe Career actions.
- `JOB-03` must publish the app manifest/store schema.
- `JOB-11` must publish the logging/test format.
- No integrated FoxNet ZIP should be built until `JOB-00` approves integration.

### Required app IDs

```text
redfox.sponsorhub
redfox.foxmail
redfox.foxtext
redfox.sponsor_rewards
```

### Required log prefixes

```text
[RedFox][SPONSOR]
[RedFox][FOXMAIL]
[RedFox][FOXTEXT]
```

### Initial app behavior target

Phase 1 should be page/app UI and data-safe placeholders only:

- SponsorHub opens on phone and PC.
- FoxMail opens on phone and PC.
- FoxText opens on phone and PC.
- Sponsor Rewards opens on phone and PC.
- Apps show test sponsor messages/offers without touching money or inventory.
- Apps can deep-link later through approved shared navigation only.
- No fake payout, fake money, fake inventory, fake vehicle ownership, or fake garage changes.

Phase 2 after shared bridge approval:

- Sponsor message notifications.
- Sponsor offer acceptance.
- Sponsor campaign progress.
- Reward claim status.
- Safe hooks to approved Career/RLS APIs only.

### Verification plan

- Inspect baseline before editing.
- List exact edited files before building.
- Validate all HTML/CSS/JS/JSON touched by JOB-12.
- Verify no protected files changed.
- Verify no RLS/Career files changed.
- Verify no phone/PC shell hijack.
- Verify no money/inventory/garage/storage changes.
- Reopen final ZIP and verify paths/reports.
- Include TXT and HTML verification reports.
- Mark runtime unproven until David tests in BeamNG.

### Acceptance test

- SponsorHub, FoxMail, FoxText, and Sponsor Rewards exist as installable/openable app/page targets through the shared Store/registry.
- They do not replace phone, PC, App Store, or shared bridge code.
- They do not touch money, inventory, garage, storage, or vehicle ownership.
- FoxFax remains untouched unless David separately approves a FoxFax task.
- Logs clearly separate SponsorHub, FoxMail, and FoxText behavior.

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
- changes SponsorHub/FoxMail/FoxText from another job without `JOB-12` coordination.
