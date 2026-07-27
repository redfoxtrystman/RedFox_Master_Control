# JOB-04 Full Handoff / Roadmap — Scrap Yard / Wrecking Yard

**Date:** 2026-07-27  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Assistant:** Sol / ChatGPT  
**Current reason for handoff:** Chat space is getting full. This file is the source-of-truth handoff for the next chat.

---

## 0. One-line status

JOB-04 is currently testing **v0.2.4**, which attempts to stop phone welcome-page lag and open the native RLS Joe's Junk seller directly instead of using the slow custom RedFox vehicle-card clone or opening every store.

Current test ZIP:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1.zip
```

Runtime status of v0.2.4: **UNPROVEN until David tests it in BeamNG.**

---

## 1. Absolute rules for the next chat

These rules are not optional.

```text
1. David owns the project decisions.
2. Do only the requested scope.
3. Do not add warnings, banners, extra UI copy, mechanics, timers, regional imports, or dev tools unless David explicitly asks for that exact patch.
4. Do not touch unrelated jobs or pages.
5. JOB-04 owns only Scrap Yard / Wrecking Yard work and immediate phone/web performance work required for this page to function.
6. Runtime behavior is unproven unless David tests it in BeamNG and reports the result.
7. Do not call a build working, fixed, final, proven, or ready unless it was actually tested.
8. If a build breaks something, log it in GitHub and roll back to the last known runtime-working base.
9. If a new patch is needed, inspect first, list exact planned edits, then patch only approved scope.
10. Never use v0.2.0, v0.2.2, or v0.2.3 as a base.
```

---

## 2. Order of Operations / OOO

The next chat must quote and follow this when doing file work:

```text
1. Inspect first, edit nothing.
   List actual file tree, missing files, broken links/routes, current route paths, and exact planned edits.

2. State exactly which files will be edited.
   Also state important files/pages that will NOT be touched.

3. Wait for David’s approval unless he explicitly says build immediately / make edits.

4. Patch only approved files.
   Do not redesign, rename, move, replace images, or alter unrelated assets/pages.

5. Verify real output.
   Check target file existence, exact in-app route paths, direct page open path, local refs, image refs, ZIP integrity, unrelated files unchanged.

6. Include readable TXT and HTML verification reports plus file tree.
   JSON alone is not acceptable.

7. If any check fails or source package cannot be inspected, stop and report failure.
   Do not package it as done.

8. If David points out a missing file/link/path, treat it as the main clue and re-inspect.
   Do not argue.
```

---

## 3. Current active base and current test build

### Last stable rollback base

The safe base is:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_1246PT_v0_2_1_ROLLBACK_TO_v0_1_9_LAST_STOCK_LOADING.zip
```

This is an exact rollback copy of v0.1.9. It should be treated as the last known line before the later failed attempts.

Known SHA256 from earlier verification:

```text
6aca6905fb6a7099d9445276c60378891d01fb266aeac533555e0ddd51306d8f
```

### Current test build

The latest build to test is:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1.zip
```

SHA256 from build verification:

```text
83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
```

v0.2.4 was built from v0.2.1 rollback, not from the bad builds.

v0.2.4 changed:

```text
assets/js/icefox_front.js
sites/scrap_yard/assets/css/scrap.css
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
ui/ui-vue/dist/index.js
```

v0.2.4 purpose:

```text
- Stop the phone welcome page from requesting RLS vehicle/shop data on startup.
- Stop Scrap Yard page from auto-running slow RedFox vehicle-card clone requests.
- Add direct native RLS Joe's Junk open action:
  career_modules_vehicleShopping.openShop('joesJunkDealership', nil, 'buying')
- Avoid opening every store.
- Avoid RedFox custom slow listing clone.
```

v0.2.4 runtime test is still pending.

---

## 4. Immediate next test for David

The next chat should ask David to test v0.2.4 in this exact order:

```text
1. Remove/disable all older JOB-04 / RedFox Scrap Yard test ZIPs from the BeamNG mods folder.
2. Install only:
   zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1.zip
3. Start BeamNG fresh.
4. Open career.
5. Open the phone/browser/welcome page.
6. Time how long it takes to show the welcome page.
7. Open Scrap Yard.
8. Click the Joe's Junk / Scrap Yard native open button.
9. Confirm whether it opens only Joe's Junk or every store.
10. Confirm whether Joe's Junk stock appears.
11. Try buying one cheap junk vehicle only if stock appears.
12. Report whether money is removed, vehicle spawns, delivery timer appears, and vehicle enters inventory/storage.
13. Save/upload BeamNG.log if there is lag, freeze, no stock, or purchase failure.
```

Expected good result:

```text
- Welcome page opens quickly.
- Scrap Yard page opens quickly.
- Button opens Joe's Junk only.
- RLS-native Joe's Junk stock appears.
- Purchase uses RLS-native delivery/storage/inventory path.
```

Bad result categories:

```text
A. Welcome page still takes 20–30 seconds.
B. Scrap Yard still takes over a minute.
C. Joe's Junk button opens every store.
D. Joe's Junk button opens nothing.
E. Joe's Junk opens but no cars appear.
F. Cars appear but purchase still removes money without inventory/storage.
```

If A or B happens, stop building features and inspect startup/web loading again.
If C happens, v0.2.4 is bad like v0.2.2 and must be logged.
If D or E happens, inspect exact RLS v2.6.8 dealership ID and openShop arguments.
If F happens, fix buy/delivery/storage next.

---

## 5. RLS files and map files currently relevant

David uploaded a newer RLS package:

```text
1(2).zip
```

Inspection result from the prior chat:

```text
This is RLS Career Overhaul v2.6.8 Beta.
```

Important note:

```text
The uploaded RLS ZIP appeared to have content under a "New folder/" prefix.
That is okay for inspection, but if installed exactly like that it may not load correctly in BeamNG.
```

David also uploaded:

```text
west_coast_usa(3).zip
```

Relevant West Coast/RLS finding:

```text
Dealership ID: joesJunkDealership
Name: Joe's Junk
Stock: 10
```

RLS Joe's Junk is the desired native seller for JOB-04. It already represents junk/wrecking-yard stock better than a custom RedFox clone.

---

## 6. What broke and why

### v0.2.0 — BAD

File:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_0929PT_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK_FROM_v0_1_9.zip
```

David's report:

```text
No cars loaded. Refresh did not pull cars. Patch was foobar.
```

Likely cause:

```text
The patch mixed too much: image CSS, Scrap Yard JS load path, phone bridge, PC bridge, and ui/ui-vue/dist/index.js. It removed/changed the stock-load path too aggressively and broke vehicle listing population.
```

Action:

```text
Do not use v0.2.0 as a base.
```

### v0.2.2 — BAD

File:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_1625PT_v0_2_2_USE_STOCK_RLS_SHOWROOMS_FROM_v0_2_1.zip
```

David's report:

```text
Every store in the game popped up.
```

Cause:

```text
It used openShop(nil, nil, 'buying'), which was too broad and opened the entire shopping system, not Joe's Junk / wrecking-yard stock.
```

Action:

```text
Do not use v0.2.2 as a base.
Do not use openShop(nil, nil, 'buying') for the Scrap Yard button.
```

### v0.2.3 — BAD

File:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_2352PT_v0_2_3_RLS_WRECKING_YARD_FILTER_FROM_v0_2_1.zip
```

David's report:

```text
Welcome page took about 20 seconds.
Scrap page took over a minute.
No cars loaded.
```

Cause:

```text
The custom RedFox vehicle-card listing/filter approach remained too slow and unreliable. Even when filtered, it was still cloning/pulling shop data through the slow web bridge instead of opening a native targeted RLS seller.
```

Action:

```text
Do not use v0.2.3 as a base.
Stop building slow RedFox custom vehicle-card clones until native RLS seller path is proven.
```

---

## 7. User's current vehicle-stock design target

David wants a wrecking-yard mix, not every car store.

Desired future stock mix:

```text
80% Joe's Junk / normal wrecking-yard stock
10% random mixed finds
5% possible good vehicles with issues
5% heavies, buses, planes, boats, and oddball/special stock
```

Important: this mix is a future controlled stock design. It should not be attempted until the page can open fast and the native Joe's Junk purchase path works.

---

## 8. Current main problem

The biggest issue is not just Scrap Yard stock. The biggest issue is phone/web performance.

David reported:

```text
Opening the phone webpage takes 20–30 seconds just to reach the welcome page.
```

This is unacceptable because future pages will include:

```text
auction yard
shipping yard
scrap yard
import yard
my vehicles
sell/scrap tools
regional ordering
```

The web system must be lazy-loaded:

```text
PHONE OPEN
→ load only tiny welcome shell
→ no cars
→ no RLS shop calls
→ no inventory calls
→ no auction/scrap/import data
→ no page preload
→ no heavy images
→ welcome appears almost instantly

CLICK SCRAP YARD
→ load only Scrap Yard page
→ then open/request native Joe's Junk seller

CLICK AUCTION YARD
→ load only Auction Yard page/data

CLICK SHIPPING YARD
→ load only Shipping Yard page/data

CLICK MY VEHICLES
→ load inventory only when that tab/page is opened
```

If the welcome page is slow, stop all feature work and fix startup first.

---

## 9. Purchase bug that must be fixed after stock opens

David reported an important buy bug from earlier working/partial builds:

```text
When buying, vehicle spawns next to player.
Money is removed.
Delivery countdown does not happen.
Vehicle does not enter inventory/storage.
David has to use dev tools to add vehicle to storage.
```

This means the current RedFox buy path was not using the complete RLS purchase completion/delivery/storage path.

Correct direction:

```text
Use RLS-native purchase flow.
Do not manually subtract money.
Do not manually spawn the vehicle.
Do not manually add to storage.
Do not hand-roll delivery.
Let RLS handle money, delivery timer, storage, ownership, inventory.
```

This should be fixed only after a native Joe's Junk stock page successfully opens.

---

## 10. Selling/scrap roadmap

After v0.2.4 test passes and buy/delivery/storage is fixed, the next gameplay feature is sell/scrap.

Desired My Vehicles design:

```text
Scrap Yard page tabs:
- Yard Stock
- My Vehicles
- Sell / Scrap
```

My Vehicles should rely on the stock game/RLS inventory list, not a homemade giant dropdown.

Required My Vehicles features:

```text
- search by vehicle name/config
- filter by map/region
- filter by garage/storage location
- handle hundreds of vehicles without freezing
- click owned vehicle
- choose sell whole vehicle / sell for scrap / later strip parts
```

Safe selling path to use:

```text
career_modules_inventory.sellVehicleFromInventory(inventoryId)
```

Fallback only if needed:

```text
career_modules_inventory.sellVehicle(inventoryId)
```

Do not hand-roll money or inventory removal.

---

## 11. Deferred features — do not mix into current patch

The following are real future ideas but must not be mixed into the immediate Joe's Junk/performance fix:

```text
refresh limits
countdown timers
regional import
shipping yard pickup
auction yard
cargo selling
trailer splitting
combo vehicle splitting
dev remove-all-parts tool
sell parts inventory
full website-wide redesign
all other sales pages
modded vehicle bypass/special orders
map-by-map stock weighting
heavies/buses/planes/boats 5% special table
```

These come later.

---

## 12. Refresh limits plan — later only

David wants refresh limits eventually, but not now because regional import/shipping-yard testing will need unlimited refresh.

Future plan:

```text
DEV / TEST MODE
- Unlimited Refresh Yard Stock
- No cooldown
- No penalty

GAMEPLAY MODE
- Yard stock refresh has cooldown
- Local yards have limited stock
- Regional import may take time/money
- Better stock can depend on reputation, distance, seller patience, or delivery cost
```

Do not implement this until buy/sell/scrap/import are stable.

---

## 13. Regional import / shipping yard future plan

Future idea from David:

```text
Choose a region/map from website.
Browse vehicles normally found there.
Order/import vehicle.
Vehicle ships to an import/shipping pickup point.
Player goes there, picks it up, and tows it back.
```

Suggested pickup logic:

```text
If map has a real import/shipping yard, use it.
If not, use the travel arrival/spawn location.
Italy → airport / arrival spawn / import lot if present
West Coast USA → ferry terminal / port
East Coast USA → town yard / dock / arrival spawn
Utah → desert roadside yard / arrival spawn
Johnson Valley → off-road yard / arrival spawn
```

Requires map inspection later.

---

## 14. Warning-banner incident and correction

There was a prior instruction failure where warning/cargo/combo text was added or pushed despite David saying not to.

Current rule:

```text
Do not add warning/caution/combo/cargo/split banners or labels unless David explicitly asks for them again.
```

The warning removal patch was:

```text
v0.1.9 — REMOVE_UNAPPROVED_WARNINGS_ONLY
```

This must stay respected.

---

## 15. JOB-10 visual website style context

David uploaded:

```text
RedFox_JOB10_Full_Websites_v0_3_0(4).zip
```

He said this is closer to what he wanted the pages/websites to look like.

Important boundary:

```text
JOB-04 should not convert all websites.
JOB-04 can use style ideas for Scrap Yard only if David asks.
All-site website conversion belongs to the correct web/page owner job, not JOB-04.
```

Current priority is performance and native RLS stock, not visual redesign.

---

## 16. GitHub audit trail from this phase

Relevant audits/incident files created or updated during this JOB-04 phase include:

```text
PROJECT_MANIFESTS/INCIDENT_REPORTS/JOB-04_2026-07-24_INSTRUCTION_OVERRIDE_WARNINGS_AND_STATUS_REPORT.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-24_2141PT_v0_1_9_REMOVE_UNAPPROVED_WARNINGS_ONLY.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-25_0929PT_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-25_1246PT_v0_2_1_ROLLBACK_v0_2_0_FIRST_BAD.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-25_1625PT_v0_2_2_USE_STOCK_RLS_SHOWROOMS.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-25_v0_2_2_BAD_OPENED_ALL_STORES.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-25_2352PT_v0_2_3_RLS_WRECKING_YARD_FILTER.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-26_v0_2_3_BAD_SLOW_NO_STOCK_AND_NEXT_RLS_NATIVE_SELLER_PLAN.md
PROJECT_MANIFESTS/JOB_AUDITS/JOB-04_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD.md
```

This handoff file is:

```text
PROJECT_MANIFESTS/HANDOFFS/JOB-04_2026-07-27_FULL_HANDOFF_ROADMAP_AND_NEXT_TESTS.md
```

---

## 17. Do not confuse with the mod conflict scanner

A separate file was also attached about a BeamNG Mod Conflict Scanner. That is not JOB-04 Scrap Yard/Wrecking Yard. Do not mix scanner requirements into this patch or handoff work.

---

## 18. Exact next-chat opening instruction

David can paste this into the next chat:

```text
You are taking over JOB-04 — Scrap Yard / Wrecking Yard for the RedFox/FoxNet BeamNG Web System project.

Read the GitHub handoff:
PROJECT_MANIFESTS/HANDOFFS/JOB-04_2026-07-27_FULL_HANDOFF_ROADMAP_AND_NEXT_TESTS.md

Current test build is:
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1.zip

Runtime is unproven. First, help me test v0.2.4. Do not build another patch until the test result is known.

Test goals:
1. Does phone welcome page load fast now?
2. Does Scrap Yard open fast?
3. Does the button open only Joe's Junk, not every store?
4. Does Joe's Junk stock show?
5. Does buying use proper RLS delivery/storage/inventory instead of only spawning and taking money?

Do not use v0.2.0, v0.2.2, or v0.2.3 as a base.
Use v0.2.1 rollback / v0.1.9 as the safe base if a new patch is required.
Follow the OOO/order of operations exactly.
```

---

## 19. Final roadmap summary

```text
PHASE 1 — Test v0.2.4
- Verify welcome page speed.
- Verify Scrap Yard speed.
- Verify Joe's Junk only.
- Verify stock appears.
- Verify buy/delivery/storage behavior.

PHASE 2 — If welcome is still slow
- Stop feature work.
- Inspect phone startup.
- Remove any remaining startup preloads/RLS calls/heavy images.
- Keep welcome page pure UI.

PHASE 3 — If Joe's Junk does not open correctly
- Inspect RLS v2.6.8 openShop/dealership API.
- Confirm exact dealership ID and current map support.
- Patch only the native targeted seller open action.

PHASE 4 — If buy still only spawns/removes money
- Inspect RLS purchase completion path.
- Fix Scrap Yard to use complete RLS buy/delivery/storage flow.
- Do not hand-roll money, spawn, storage, or inventory.

PHASE 5 — My Vehicles / Sell Scrap
- Add My Vehicles tab using stock RLS/career inventory data.
- Search/filter by vehicle, map/region, garage/storage.
- Use stock inventory sell function for whole-vehicle sale.

PHASE 6 — Scrap/parts workflow
- Quote scrap value.
- Sell/scrap owned vehicles.
- Later add dev strip-all-parts test.

PHASE 7 — Regional import and shipping yard
- Inspect maps.
- Add regional stock pools.
- Add pickup destinations.
- Add import/shipping cost and delays.

PHASE 8 — Refresh limits and stock weighting
- Add dev/gameplay modes.
- Add cooldown/stock limits.
- Add desired stock mix:
  80% Joe's Junk
  10% random
  5% possible good with issues
  5% heavies/buses/planes/boats/oddballs
```
