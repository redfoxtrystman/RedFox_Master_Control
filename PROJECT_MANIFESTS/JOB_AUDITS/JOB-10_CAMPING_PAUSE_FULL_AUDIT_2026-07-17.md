# JOB-10 — Visual Design / Real Website Polish — Camping Pause Full Audit

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Chat role:** JOB-10 regular-chat takeover / Sol  
**Status:** PAUSED while David is camping. This is **not a handoff**. Resume this same JOB-10 chat when David returns.

---

# 1. Sound off

This chat is:

```text
JOB-10 — Visual Design / Real Website Polish
```

JOB-10 is a **cross-mod visual-design job**. It does not own the gameplay/backend systems for every page. It owns the shared visual language and realistic website presentation used across the separate IceFox/FoxNet page add-ons.

JOB-10 owns:

- realistic website appearance;
- visual design system;
- responsive phone and PC layouts;
- typography, spacing, colors, borders, shadows, cards, tables, buttons, forms and navigation;
- page-specific identities so each website looks like a different real company/service;
- visual mockups and offline HTML prototypes;
- loading, empty, unavailable, success, warning and error-state presentation;
- ad-slot presentation;
- approved image placement and visual asset direction;
- visual regression review after a behavior-owning job provides stable files;
- final presentation polish only after behavior contracts are stable.

JOB-10 does **not** own:

- phone or PC browser shell behavior;
- shared route registry;
- shared bridge implementation;
- Career or RLS systems;
- money, ownership, garage, storage, insurance, inventory or purchasing behavior;
- vehicle spawning or persistence;
- Scrap Yard runtime behavior;
- BeamBook marketplace runtime behavior;
- Import/Export runtime behavior;
- Collector Exchange runtime behavior;
- Tow/Recovery runtime behavior;
- SponsorHub, FoxMail, FoxText or Sponsor Rewards runtime behavior;
- external internet/browser capability inside BeamNG;
- final integration approval;
- final QA approval.

This is not a transfer of ownership. Other jobs should continue their own behavior work, but they must not overwrite or independently redesign the JOB-10 visual baseline without coordination.

---

# 2. Project architecture JOB-10 is following

The approved project architecture remains:

1. One shared IceFox/FoxNet front-door platform mod.
2. Each actual website/app remains an isolated, removable add-on mod.
3. Phone and PC open the same canonical page destination.
4. Phone and PC may render differently, but they must use the same backend data/action contract.
5. Pages must work across all maps.
6. No page may require West Coast USA unless a separate optional physical location is deliberately added later.
7. JOB-10 changes presentation only unless another job gives an exact safe-to-edit handoff.
8. No combined release is approved until JOB-00 accepts integration.
9. No runtime result is called working until David tests the exact BeamNG build.

---

# 3. Work-chat migration history

The original JOB-10 Work chat became inaccessible after the separate Work-chat limit was reached. The active job was migrated into this regular chat.

The shared-link transcript, tool history and chat-only attachments could not be fully recovered. That limitation was documented honestly.

Migration/claim commits already recorded:

```text
1713002ab9344c766a3f8d80af821c8407320b8e
JOB-10 regular-chat takeover record

32d364c876a456d6da2adf7f8bffec0b2d1561a1
JOB-10 claim updated for regular-chat migration

e33748ad4f6c0adb57638875c9a7c5a174c811c2
Migration-status tracker updated

ce14c86d2fb72352383ce82e5ec5da13ce27c8c8
Work-chat incident report updated with JOB-10 impact
```

The claim record later had to be restored after an earlier update accidentally shortened its history:

```text
ea804fdecdb99cff2821e2ee059f1621e2862db6
JOB-10 claim history restored and v0.1.0 checkpoint recorded
```

---

# 4. Files and references David supplied to JOB-10

## 4.1 Main website/reference packages

```text
redfox_web_ecosystem_v1_combined_VERIFIED.zip
site_shots.zip
BeamBook_ROUTE_FIX_DROP_IN_v1_3.zip
icefox_browser_frontpage_v0_6_4_EMBEDDED_FOX_SAFE.zip
beamBook.zip
rls_slop_gear_garage_v0.2.zip
backAlley.0.2.2-alpha.zip
```

## 4.2 RLS/Career/reference packages

```text
RedFox_RLS_Evidence_v03_SUMMARY_ONLY.zip
RedFox_RLS_Evidence_v03.zip
rls_career_overhaul_2.6.6.zip
west_coast_usa.zip
```

The West Coast map archive is reference material only. JOB-10 pages must remain all-map.

## 4.3 Text-roadmap files

```text
New Text Document.txt
New Text Document (2).txt
```

Those roadmaps established the core visual philosophy:

- websites must not look like mod menus;
- legal and underground sides need separate identities;
- FoxNet Auctions should resemble Copart/IAA;
- FoxFax should resemble CarFax while remaining original;
- Collector Exchange should resemble a premium collector auction;
- XXX Insurance should retain the black/pink/lace identity;
- Parts Exchange should resemble a real parts retailer/search network;
- Export Yard should feel like ocean freight, ports and containers;
- Tow/Recovery should look like a real towing company;
- UndergroundNet should feel suspicious and professional, not like an edgy placeholder;
- visible player pages should not say game, mod, future feature or parody.

## 4.4 Images supplied

- approved female fox mascot image for FoxFax;
- IceFox front-page visual target/mockup;
- real-site screenshot references;
- BeamNG vehicle/driving images used as prototype visuals;
- BeamBook reference screenshots and assets.

## 4.5 Important use restrictions

- `beamBook.zip` was supplied as a private reference. Do not publicly redistribute copied code/art without reuse permission.
- Real-world screenshots are visual references, not assets to redistribute.
- Real brands, logos and trademark text should not be copied directly.
- Final pages should be recognizable inspired spoofs with original RedFox/FoxNet branding.

---

# 5. What JOB-10 inspected and learned

The combined ecosystem included visual page prototypes for:

```text
FoxNet Auctions
FoxFax
XXX Insurance
Collector Exchange
Parts Exchange
Export Yard
RedFox Recovery
UndergroundNet
```

The BeamBook route package included:

```text
BeamBook index page
BeamBook CSS
BeamBook JavaScript
BeamBook sample data
avatar placeholders
marketplace listings
feed images
IceFox route files
```

The IceFox front-page package included multiple local page families and proved the intended local-browser structure, but JOB-10 did not adopt its protected shared platform JavaScript as owned visual code.

The real-site screenshot archive provided Copart, CarFax, Barrett-Jackson, parts-store and black-market-style visual references.

The RLS files were inspected as behavioral/reference context only. JOB-10 did not alter RLS code.

---

# 6. What was built

## 6.1 Visual Mockup v0.1.0

Package:

```text
RedFox_JOB10_Visual_Mockup_v0_1_0.zip
```

SHA-256:

```text
a44f146833dccbb5c17ee31cc6857cf8f3ffe6d1862dd62623bfab3cf2a3c0a6
```

Initial included pages/features:

- IceFox browser home;
- BeamBook social feed and Marketplace;
- FoxNet Auctions;
- FoxFax;
- XXX Insurance;
- Collector Exchange;
- Parts Exchange;
- Export Yard;
- renameable towing/recovery company;
- underground network;
- rotating ads;
- humorous 404 page;
- responsive desktop/phone appearance.

GitHub records:

```text
159e8b59f05023961d7e2a97485c204809ba9e13
Initial v0.1.0 handoff
```

## 6.2 Visual Mockup v0.2.0

Package:

```text
RedFox_JOB10_Visual_Mockup_v0_2_0.zip
```

SHA-256:

```text
a31d403f2c746848d9061d23e53e065654c7c78b758863069512bc7e383bc2d6
```

Main corrections:

- global light/dark behavior;
- removed visible “career map” wording;
- BeamBook moved closer to the supplied Facebook-style layout;
- BeamBook vehicle popup closing repaired;
- FoxFax garage vehicle selection/report flow added;
- auction registration/membership/payment mock flow added;
- black/pink/lace insurance design restored;
- stronger ocean-freight Export Yard;
- mystery-container purchase/reveal mock flow;
- Tow/Recovery redesigned as a real towing company;
- underground network renamed from BackAlley to UndergroundNet;
- legal Scrap Yard/Wrecking Yard added;
- rotating ads retained.

GitHub record:

```text
b9c99dea07246c21a3dcd647d62748ae0f7b0e12
v0.2.0 feedback revision documented
```

## 6.3 Full offline website delivery v0.2.1

The first direct-preview delivery was broken because the direct HTML folder did not contain the CSS, JavaScript and image asset folders used by the real build. It displayed raw text and controls.

That failure was corrected by creating a self-contained `START_HERE.html` with CSS, JavaScript and images embedded.

Package:

```text
RedFox_JOB10_Full_Websites_v0_2_1.zip
```

GitHub correction:

```text
066af207c1bef00768e78836a13c9224b48a6276
Broken direct preview documented and full offline website republished
```

This failure must not be repeated. Future test packages should include one verified standalone start file or a complete extracted folder with all linked assets.

## 6.4 Full Websites v0.3.0

Package:

```text
RedFox_JOB10_Full_Websites_v0_3_0.zip
```

SHA-256:

```text
b0f69fd1fa97d28a80882d784ad4fe37b91590b2375c60851dcf053a27d32970
```

Main additions/corrections:

- working auction category filters;
- prototype auction pool initially set to 100 vehicles;
- next-day inventory rotation;
- BeamNG vehicle/driving images in the prototype;
- illustrated BeamBook faces/contacts;
- Wall content swapping;
- corrected Scrap Yard selling choices;
- six visually different UndergroundNet subpages.

GitHub record:

```text
6139e54d266ab6a91dc046e0d6cd6839b6e97f81
v0.3.0 full website mockup documented
```

## 6.5 Current full browser checkpoint: v0.3.1

Current package:

```text
RedFox_JOB10_Full_Websites_v0_3_1.zip
```

SHA-256:

```text
0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
```

Current status:

```text
MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG
```

GitHub record:

```text
e5935c62a8561980c5ba63ad2ce3936eaf7fca8b
v0.3.1 pre-integration browser checkpoint documented
```

David said the project is at a good place and close to being ready to attempt BeamNG integration.

---

# 7. Current v0.3.1 page inventory and visual state

## 7.1 IceFox browser home

Current direction:

- believable browser start page;
- no “career map” wording;
- no hard map dependency;
- optional current-map name/weather may be displayed later if the game supplies it cleanly;
- all website routes should work on every map;
- light/dark themes;
- real website-style cards rather than mod-menu buttons;
- legal and underground entry points remain visually distinct.

Runtime state:

```text
Visual prototype only.
JOB-01 owns final phone/PC/browser-shell behavior and route registration.
```

## 7.2 BeamBook

Current approved direction:

- Facebook-like social layout;
- left navigation, central feed, right contacts/sponsors area;
- white/light Facebook-style primary theme with matching dark option;
- made-up BeamNG-related people with faces;
- funny, serious, sad, strange and “what happened here?” posts;
- real BeamNG vehicle/driving imagery;
- Marketplace integrated into BeamBook presentation;
- vehicle popup closes correctly;
- feed should not change every ten seconds;
- a different selection may load when BeamBook is opened again;
- manual refresh may remain available;
- every vehicle/listing must ultimately use actual in-game vehicle/configuration data and thumbnails.

Runtime owner:

```text
JOB-05 owns BeamBook behavior and marketplace integration.
JOB-10 owns visual design.
```

## 7.3 FoxNet Auctions

Current approved direction:

- Copart/IAA-inspired original auction site;
- categories must work;
- active inventory should be around 100, not exactly 100;
- current prototype rule: roughly 90–110 active vehicles;
- exact total and category mix may change each in-game day;
- vehicles rotate rather than forming a permanent oversized catalog;
- registration must open a membership flow;
- membership fee/payment and bidding access presentation exists;
- categories with zero inventory should show zero/disabled instead of routing to wrong vehicles;
- real in-game thumbnails required at runtime.

Current prototype categories include cars, work trucks, semis, off-road and electric, with unsupported categories able to show zero.

Runtime state:

```text
Visual/prototype interactions only.
Real daily inventory, purchase, bidding, ownership and payment require the owning backend jobs and shared RLS/Career contracts.
```

## 7.4 FoxFax

Current approved direction:

- CarFax-inspired original site;
- approved friendly female fox mascot;
- select a vehicle from owned garages;
- request/open a history report;
- serious, sad, weird and funny history entries;
- may slightly affect value later;
- does not physically change vehicle condition;
- legal vehicles may receive reports;
- stolen Black Market vehicles do not receive FoxFax reports.

Runtime state:

```text
Garage list/report generation are mock data only.
Final owned-vehicle selection and history data require the correct Career/RLS source.
```

## 7.5 XXX Insurance

Current approved direction:

- preserve the supplied black, hot-pink and lace look;
- keep working dropdown/quote presentation from JOB-10 prototype;
- vehicle, fleet, property, business, tow-yard and storage coverages can be represented as their systems become available;
- realistic insurance-site appearance;
- light/dark support without losing the black/pink identity.

Runtime owner:

```text
JOB-08 owns insurance/finance/garage/storage behavior.
JOB-10 owns the final visual presentation.
```

## 7.6 Collector Exchange

Current approved direction:

- Barrett-Jackson-inspired premium original site;
- dark, premium, collector-auction identity;
- rare/high-value vehicles;
- featured docket and premium photography layout;
- real game vehicles/configurations at runtime.

Runtime owner:

```text
JOB-07 owns behavior/data.
JOB-10 owns visuals.
```

## 7.7 Parts Exchange

Current approved direction:

- realistic used/new parts search and retailer presentation;
- acceptable for now; tweak later;
- future stripped-parts inventory;
- AI/customer demand and market pricing later;
- legal parts from legal vehicles can enter normal market;
- stolen serialized parts must remain underground unless approved as unmarked/legal-safe.

Runtime behavior remains unimplemented in JOB-10.

## 7.8 Export Yard / Import-Export Terminal

Current approved direction:

- stronger ocean/port/container identity;
- visible container ship/port imagery;
- international shipping quotes;
- tracking and paperwork presentation;
- sealed abandoned/unclaimed mystery containers;
- container prices roughly $2,000–$25,000;
- possible contents may include parts, crops, vehicles, machinery, aircraft-related cargo, good/bad vehicles or other cargo;
- mystery contents remain a later runtime/economy system;
- light/dark support;
- all-map access through website even if physical port missions are map-specific later.

Runtime owner:

```text
JOB-06 owns Import/Export behavior and missions.
JOB-10 owns visuals.
```

## 7.9 Tow / Recovery company page

Current approved direction:

- must look like a real towing-company website, not a dispatch menu;
- ideally renameable when the player buys/names the business;
- tow-truck, collision and wreck-recovery imagery;
- services include lockouts, local towing, winch-outs, collision recovery, heavy recovery, abandoned vehicles, transport and roadside help;
- future low-cost lockout mission concept;
- support lost, salvaged, wrecked and stranded vehicle scenarios.

Runtime owner:

```text
JOB-09 owns Tow/Recovery/Dispatch behavior when active.
JOB-10 owns page visuals only.
```

## 7.10 Scrap Yard / Wrecking Yard

Current approved direction:

The site is both a Scrap Yard and a Wrecking Yard.

It must support two broad sides:

### Sell/process owned vehicles

1. **Full car sale**
   - sell the whole vehicle;
   - yard keeps the vehicle and all parts;
   - player receives no returned parts;
   - quick/easy option;
   - pays less than dismantling/processing routes.

2. **Hire yard and keep parts**
   - yard pulls usable parts;
   - player pays labor/dismantling cost;
   - parts go to the player’s Parts Shop inventory;
   - player receives less cash because labor is deducted.

3. **Process/strip it yourself**
   - player manually removes parts;
   - parts go to the Parts Shop;
   - only stripped chassis/scrap is sold to yard;
   - no yard dismantling labor charge.

### Buy wrecking-yard vehicles

The yard may list:

- wrecked vehicles;
- salvage-title vehicles;
- parts cars;
- incomplete projects;
- rough-running vehicles;
- cheap rebuilders;
- occasional decent running vehicles at a good price.

These are legal yard vehicles and may have FoxFax/history where data exists.

Future market behavior:

- legal recovered parts enter Parts Shop;
- AI/customers buy parts over random market ticks;
- demand changes by category;
- scarce high-demand parts rise in value;
- inventory should not instantly sell out;
- runtime logic belongs to JOB-04 and other economy owners, not JOB-10.

Runtime owner:

```text
JOB-04 owns Scrap Yard/Wrecking Yard behavior.
JOB-10 owns realistic page visuals.
```

## 7.11 UndergroundNet

The illegal side must not use RedFox legal-company branding.

Each section now has a separate visual identity instead of one repeated page template:

```text
Black Market
Shadow DMV
Chop Shop
Most Wanted
High Risk Freight
Cold Storage
```

### Black Market

- stolen/off-book higher-end vehicles;
- prices much lower than legal-market value;
- no FoxFax button/report;
- no normal public vehicle history;
- expensive Shadow DMV legalization path;
- legalization may cost more than vehicle purchase;
- useful for illegal resale or part-out;
- not processed through normal legal wrecking-yard flow.

### Stolen-part rules

Remain underground:

- engines;
- transmissions;
- axle/rear-end assemblies;
- VIN-stamped body sections;
- serialized major components.

Potentially legal-safe only after an approved runtime whitelist confirms they are unmarked:

- some wheels;
- seats;
- suspension components;
- generic hardware;
- unmarked internal gear components;
- other clearly non-serialized items.

JOB-10 does not decide serialization in code. The behavior owner must use a real whitelist/data rule.

### Shadow DMV

- paperwork/title/registration legalization service;
- functional process page, not a vehicle gallery;
- very expensive for valuable stolen vehicles.

### Chop Shop

- underground vehicle stripping and illegal-part marketplace;
- stolen serialized parts remain underground;
- separate from legal Parts Exchange and legal Scrap Yard.

### Most Wanted

Targets may include:

- rare exotics;
- high-end collector cars;
- prototypes;
- competition cars;
- expensive machinery;
- aircraft;
- high-end semis;
- semi/trailer combinations;
- sealed trailers with valuable goods;
- collector transporters.

Future gameplay concept:

- target vehicles may appear while driving;
- player notices/locates them;
- steals/retrieves them;
- delivers them to illegal export/receiving location;
- behavior not implemented by JOB-10.

### High Risk Freight

- questionable cargo/imports;
- visually separate risky-freight identity.

### Cold Storage

- illegal container/vehicle storage;
- separate from home garage, legal tow yard and legal storage.

Runtime state:

```text
Visual prototype only.
Illegal ownership, theft, heat, paperwork, part routing, rewards and storage require dedicated backend design.
```

## 7.12 Ads

- rotating ad locations must remain on appropriate pages;
- future funny ad packs will cycle through them;
- ad system should support cross-site businesses and sponsor content;
- JOB-10 owns ad-slot presentation, not the final ad-scheduling/backend system.

## 7.13 404/error pages

- intentional humorous 404 page exists in the browser prototype;
- dead/non-game links can route there until a real destination is added;
- external Lore/browser pages also need blocked/offline/error presentation later.

---

# 8. Things that were tried and failed or needed correction

## 8.1 Broken direct preview

Failure:

- direct HTML link opened without styles/scripts/images;
- page appeared as raw text and controls;
- user correctly rejected it.

Cause:

- linked folder contained only HTML/reports;
- real assets lived in a different build directory.

Correction:

- self-contained `START_HERE.html` created;
- future deliveries must verify the exact user-facing link, not only ZIP contents.

## 8.2 Early BeamBook styling drift

Failure:

- initial JOB-10 BeamBook moved too far from the Facebook-style version David supplied;
- background and structure were not close enough.

Correction:

- restored Facebook-like left navigation, central feed, right contact/sponsor rail;
- preserved BeamBook branding and original content;
- added real faces and BeamNG-themed posts;
- fixed popup closing;
- stopped rapid automatic post changes.

## 8.3 Overly exact auction inventory

Earlier mock rule:

```text
Exactly 100 active vehicles
```

Corrected rule:

```text
Roughly 90–110 active vehicles, changing by in-game day
```

## 8.4 Underground pages looked too similar

Failure:

- sections initially reused one visual template.

Correction:

- Black Market, Shadow DMV, Chop Shop, Most Wanted, High Risk Freight and Cold Storage now have separate visual identities.

## 8.5 Wrong Scrap Yard wording/logic

Failure:

- early labels implied incorrect parts-return/payment behavior.

Correction:

- full car sale = no parts returned and lower money;
- hire yard/keep parts = labor cost deducted and parts returned to Parts Shop;
- process yourself = player strips parts and sells shell/scrap only.

## 8.6 Map/career wording

Failure:

- early copy mentioned “career map” unnecessarily.

Correction:

- visible pages no longer say career map;
- optional map name/weather may be added only as normal website location/weather information;
- no page should imply it only works on a specific map.

---

# 9. New pages added to the backlog

David requested additional website/page families:

```text
SponsorHub
FoxMail
FoxText
Sponsor Rewards
Lore & History / Wiki Browser
```

## 9.1 SponsorHub

JOB-12 behavior/data; JOB-10 visuals.

Visual requirements should support:

- sponsor directory;
- sponsor/company profiles;
- applications/subscriptions;
- pending applications;
- sponsor offers;
- accept/decline contract presentation;
- active contracts;
- sponsor status/tier;
- Sponsor XP;
- reputation;
- Sponsor Points;
- assigned sponsor vehicles;
- decal/honor requirements;
- reward summary;
- recent FoxMail/FoxText notices.

## 9.2 FoxMail

Formal full-message system for:

- sponsor applications;
- contract offers;
- approvals/declines;
- payment/reward notices;
- vehicle assignments;
- sponsor correspondence;
- system notices.

JOB-10 must make it look like a believable email client/site, while JOB-12 owns delivery, state and persistence.

## 9.3 FoxText

Short-message/notification interface for:

- sponsor alerts;
- quick offer updates;
- reminders;
- dispatch-like short messages when appropriate;
- compact phone-friendly conversations.

JOB-12 owns behavior. JOB-10 owns presentation.

## 9.4 Sponsor Rewards

Could be a separate page or a SponsorHub section, depending on David’s later choice.

Visual requirements:

- reward catalog;
- sponsor-specific rewards;
- points price;
- unlock progress;
- locked/available/claimed states;
- claim confirmation;
- assigned vehicle/decal perks.

## 9.5 Lore & History / Wiki Browser

Goal:

- local IceFox-designed landing page;
- live authoritative BeamNG/RLS pages as source of truth;
- no scraping or copied full articles;
- categories for manufacturers, models, company history, years/generations, levels/locations, trailers/equipment, motorsport/special configurations, updates and community lore;
- official and community sources clearly labeled;
- search, bookmarks, recent pages and featured entries;
- Back, Forward, Home, Reload, Stop, Close and Open Externally controls;
- offline/blocked-page handling.

Initial safe-domain direction:

```text
documentation.beamng.com
beamng.com
www.beamng.com
approved official RLS domains once identified
```

Unrestricted general web browsing and YouTube are deferred as future experiments.

Reason:

- external pages may refuse iframe embedding;
- embedded-browser video, cookies, pop-ups, downloads and performance increase risk;
- first release should prove approved BeamNG/RLS sites only.

External internet browsing inside BeamNG is plausible but unproven. JOB-01/JOB-11 must test one minimal external page before broader implementation.

---

# 10. Sponsor-system warning found in GitHub

JOB-12 owns SponsorHub/FoxMail/FoxText/Sponsor Rewards behavior.

Previous JOB-12 test attempts had an order-of-operations failure:

1. First package used a HUD UI App instead of the requested keybind-opened standalone WebUI.
2. Corrected WebUI opened, but Apply, offers, FoxMail, FoxText and state updates did not work.
3. Static syntax/ZIP checks did not prove UI-to-Lua and Lua-to-UI runtime flow.

Incident record:

```text
INCIDENT_REPORTS/2026-07-14_JOB-12_WEBUI_ORDER_OF_OPERATIONS_FAILURE.md
```

JOB-10 must not copy the failed runtime event pattern.

Before sponsor visual pages connect to runtime, JOB-12 must prove:

- one UI button reaches Lua;
- Lua sends state back to UI;
- one offer is generated;
- FoxMail count updates;
- FoxText count updates;
- state persists;
- exact data/action contracts are documented.

---

# 11. GitHub coordination documents already created

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-10_VISUAL_WEBSITES_v0_3_1_AND_JOB-12_SPONSOR_COORDINATION_2026-07-14.md
Commit: bad92c9ad156a20629300fd6798947c447623489

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-10_SPONSOR_MAIL_TEXT_REWARDS_AND_LORE_WEB_PAGE_PLAN_2026-07-14.md
Commit: 7d55a443ab3b276bd5e46fefc34a6bac95c74ec0

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-10_LORE_BROWSER_RLS_SITE_ALLOWLIST_ADDENDUM_2026-07-14.md
Commit: 9f22c07b8038a859ca1b22e22228f937d51fcf27
```

These older files are coordination records despite being stored in the existing handoff folder. This camping document is explicitly a pause audit, not a handoff.

---

# 12. Current state of JOB-10’s mod/work

Current latest JOB-10 package:

```text
RedFox_JOB10_Full_Websites_v0_3_1.zip
```

Current hash:

```text
0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
```

Current state:

```text
Standalone browser prototype.
Broad visual direction approved/liked by David.
Close to integration planning.
Not installed as a BeamNG app/page mod.
Not connected to RLS/Career.
Not connected to phone/PC shared platform.
Not runtime-tested in BeamNG.
No final integrated ZIP exists.
```

What is visually present now:

- main IceFox page;
- BeamBook feed/Marketplace;
- FoxNet Auctions;
- FoxFax;
- XXX Insurance;
- Collector Exchange;
- Parts Exchange;
- Export Yard;
- Tow/Recovery;
- Scrap Yard/Wrecking Yard;
- UndergroundNet subpages;
- rotating ads;
- light/dark modes;
- humorous 404/error presentation.

What is not yet present in v0.3.1:

- SponsorHub page;
- FoxMail page;
- FoxText page;
- Sponsor Rewards page/section;
- Lore & History browser page;
- real BeamNG runtime routes;
- live vehicle/configuration thumbnail feed;
- live owned-garage feed;
- real auction-day inventory feed;
- real transactions or ownership changes;
- real insurance quotes/contracts;
- real sponsor/mail/text state;
- real external internet page loading inside BeamNG.

---

# 13. Cross-mod dependencies

Because JOB-10 is cross-mod visual work, integration depends on other jobs.

## JOB-00 — Coordinator / Integration / Verification

Must provide:

- integration approval;
- final source/domain approval;
- combined-release order;
- resolution of cross-job ownership conflicts.

## JOB-01 — Phone + PC Platform Core

Must provide:

- canonical route registration;
- shared browser container boundaries;
- phone/PC responsive host dimensions;
- external-page capability for Lore browser;
- Back/Home/Reload/Close/return-to-game behavior;
- safe presentation-only files JOB-10 may edit.

## JOB-02 — Shared RLS / Career Bridge

Must provide/approve:

- final shared page data/action contracts;
- sponsor/mail/text messages if required;
- no invented duplicate bridge names;
- correct use of game/RLS systems.

## JOB-04 — Scrap Yard / Wrecking Yard

Must provide:

- stable legal yard vehicle inventory data;
- owned-vehicle sell/process actions;
- parts-return/labor/process results;
- Parts Shop inventory handoff;
- demand/market data if built;
- exact presentation-only boundary.

## JOB-05 — BeamBook Marketplace

Must provide:

- stable feed/Marketplace data schema;
- seller/profile/post/listing data;
- live real in-game vehicle thumbnail/configuration source;
- safe modal/open/close/action contracts;
- exact presentation-only boundary.

## JOB-06 — Import / Export Yard

Must provide:

- shipment/container/quote/tracking data;
- mystery-container purchase/reveal contract if approved;
- mission and delivery state;
- exact presentation-only boundary.

## JOB-07 — Classics / Collector Exchange

Must provide:

- rare/collector inventory schema;
- auction/sale actions;
- premium vehicle data;
- exact presentation-only boundary.

## JOB-08 — Insurance / Finance / Garage / Storage

Must provide:

- owned vehicles/garages for FoxFax selection;
- insurance quote/coverage/action schema;
- property/business/storage state;
- exact presentation-only boundary.

## JOB-09 — Tow / Recovery / Dispatch

Must provide when active:

- service/job data;
- company rename state if supported;
- tow/recovery/lockout/transport actions;
- yard/delivery integration points;
- exact presentation-only boundary.

## JOB-11 — QA / Logging / Failure Triage

Must verify:

- desktop/phone rendering;
- light/dark modes;
- broken links/assets;
- modal behavior;
- route regression;
- all-map operation;
- external page failures;
- browser console and BeamNG logs;
- no protected behavior changed.

## JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

Must provide:

- proven UI-to-Lua and Lua-to-UI runtime path;
- sponsor/application/offer/contract schemas;
- XP/reputation/points/reward schemas;
- FoxMail/FoxText schemas;
- persistence/payment/vehicle-assignment behavior;
- exact presentation-only boundary.

---

# 14. Protected files and behavior JOB-10 must not take over

Do not edit/replace without exact owner handoff:

```text
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
lua/ge/extensions/career/
shared phone shell
shared PC shell
shared browser shell
shared registry
shared bridge
RLS core
Career core
vehicle shopping/inventory/garage/storage logic
purchase/sell/ownership logic
insurance logic
sponsor/mail/text state logic
another job’s functional JavaScript mixed with actions
```

If an HTML or JavaScript file mixes presentation and behavior, JOB-10 must coordinate an exact section/file boundary before editing.

---

# 15. Required next steps when David returns

## Phase A — confirm/freeze current visual checkpoint

1. Reopen `RedFox_JOB10_Full_Websites_v0_3_1.zip`.
2. Confirm the ZIP downloads and extracts correctly.
3. Open `START_HERE.html` in Chrome/Edge/Firefox.
4. Confirm David still approves the broad visual direction.
5. Record any final page-specific visual changes.
6. Freeze v0.3.1 as the comparison baseline.

## Phase B — add the five missing page families

Build browser-only visual prototypes for:

```text
SponsorHub
FoxMail
FoxText
Sponsor Rewards
Lore & History / Wiki Browser
```

Requirements:

- same global IceFox design system;
- each page has its own believable identity;
- responsive PC/phone layouts;
- light/dark support where appropriate;
- no fake claims of BeamNG functionality;
- rotating ad support where appropriate;
- proper empty/loading/error states.

## Phase C — obtain behavior handoffs

Ask each behavior-owning job for:

- exact route ID;
- exact data schema;
- exact action/event names;
- state list;
- error list;
- safe files/sections JOB-10 may edit;
- protected files;
- test build/result.

## Phase D — integration order

Integrate one page at a time rather than rebuilding the entire ecosystem at once.

Recommended order:

1. IceFox platform route/container proof.
2. BeamBook visual integration.
3. Scrap Yard/Wrecking Yard visual integration.
4. Import/Export visual integration.
5. Collector Exchange visual integration.
6. Insurance/FoxFax/garage selection integration.
7. Tow/Recovery visual integration.
8. SponsorHub/FoxMail/FoxText/Rewards after JOB-12 runtime is proven.
9. Lore browser minimal one-site test.
10. Full visual consistency pass.
11. JOB-11 regression testing.
12. JOB-00 combined-release approval.

## Phase E — real images/data

Replace prototype images/data with:

- actual BeamNG vehicle/configuration thumbnails;
- actual owned-garage list;
- actual auction/scrap/collector/black-market inventory;
- actual user/business name where supported;
- actual map name/weather only if cleanly supplied;
- actual sponsor and message records.

No unrelated stock car images should remain in final runtime pages.

---

# 16. Testing requirements after integration begins

Every integrated page must be tested for:

- PC layout;
- phone layout;
- window resizing;
- scroll/overflow/clipping;
- light/dark modes;
- broken images/assets;
- Back/Home/Reload/Close;
- modal open/close;
- empty/loading/error states;
- keyboard/mouse focus;
- all maps;
- duplicate FoxNet ZIP conflicts;
- correct runtime data;
- correct game actions;
- no fake transaction success;
- no lost ownership/garage/storage state;
- no startup Career modules;
- no map-load page generation;
- no protected file duplication;
- BeamNG log/console errors.

Runtime status must remain:

```text
BUILT — RUNTIME UNTESTED
```

until David tests the exact package.

---

# 17. Pause rules while David is camping

This is a pause, not a handoff.

While David is away:

- JOB-10 ownership does not transfer;
- v0.3.1 remains the current visual baseline;
- no other chat should overwrite the JOB-10 design system;
- behavior jobs may continue their own isolated work;
- behavior jobs should document stable contracts/files for later JOB-10 polish;
- no combined integration should be called complete;
- no one should claim SponsorHub/Lore pages are working in BeamNG;
- no unrestricted browser/YouTube experiment should be added to the first release;
- no new broad redesign should start without David’s approval.

Resume point:

```text
Return to this same JOB-10 chat.
Reopen the v0.3.1 package.
Review/add SponsorHub, FoxMail, FoxText, Sponsor Rewards and Lore browser.
Then begin controlled per-page BeamNG integration after owner handoffs.
```

---

# 18. Current summary

```text
Job: JOB-10 — Visual Design / Real Website Polish
Type: Cross-mod visual-design work
Current package: RedFox_JOB10_Full_Websites_v0_3_1.zip
SHA-256: 0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
Current state: Standalone browser prototype
David feedback: Broad design liked; project at a good place
BeamNG integration: Not started/proven
New visual pages remaining: SponsorHub, FoxMail, FoxText, Sponsor Rewards, Lore & History
External web: BeamNG/RLS allowlist planned; not proven in BeamNG
Pause status: Paused for camping; not a handoff
Resume location: Same JOB-10 chat
```
