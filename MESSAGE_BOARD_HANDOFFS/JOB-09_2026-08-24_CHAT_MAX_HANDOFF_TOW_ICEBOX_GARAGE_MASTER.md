# READ FIRST — JOB-09 Chat-Max Handoff — Tow + Icebox Garage Architecture Master

Date: 2026-08-24
From: outgoing JOB-09 chat
To: next JOB-09 chat
Primary scope: **JOB-09 — RedFox Tow & Recovery Dispatch**
Secondary temporary lab: **RedFox Icebox** (standalone garage architecture test)
Status: CHAT LIMIT HANDOFF — USE THIS AS CURRENT CONTINUATION POINT

---

# 1. Owner process rules — mandatory

The owner requires source-first/evidence-first work. Do not guess APIs and do not patch first then inspect later.

Required order:

1. inspect the exact supplied archive/source;
2. verify exact APIs, files and behavior;
3. only then edit/build;
4. validate/diff/package;
5. report exact changed/untouched files and runtime uncertainty.

There was a prior order-of-operations incident where v0.5.0.24 work began before direct reconstruction/read of the supplied paid RLS archive. That incident is already logged here:

`PROJECT_MANIFESTS/AUDITS/JOB-09_2026-08-15_INCIDENT_ORDER_OF_OPERATIONS_RLS_2.7.0.1_PREVERIFY_PATCH.md`

Do not repeat it.

Other owner rules:

- no silent changes;
- no auto-moving/migrating existing trucks or trailers;
- test risky vehicle-storage changes one expendable vehicle at a time;
- do not edit paid RLS source files without explicit permission;
- do not require developer-style manual linking/registration steps in the final gameplay flow;
- preserve completed/working behavior unless testing proves it broken;
- when a runtime result contradicts assumptions, record it and redesign rather than layering more UI patches over the wrong architecture.

The owner generally wants testing instructions in chat, not separate checklist downloads.

---

# 2. Exact paid RLS 2.7.0.1 source used

The owner supplied the paid RLS split archive:

- `rls_career_overhaul_2.7.0.1 split.z01`
- `rls_career_overhaul_2.7.0.1 split.z02`
- `rls_career_overhaul_2.7.0.1 split.zip`

The outgoing chat reconstructed/read it read-only before later source work.

Important exact findings:

## RLS Recovery

Shared Recovery skill key:

`careerSkills-recovery`

Native modules:

- `lua/ge/extensions/gameplay/repo.lua`
- `lua/ge/extensions/gameplay/offroadRecovery.lua`

JOB-09 Tow/Recovery jobs should use the same Recovery skill, but native Repo and native Off-Road Recovery own their own native reward/XP logic. Do not duplicate native rewards.

Native Repo XP formula found in source:

`5 + repoBaseXp + round(totalDistanceTraveled / 2000)`

Native Repo has a problematic time payout factor on huge maps:

`timeMultiplier = totalDistanceTraveled / (elapsedSeconds * 10)`

Planned future RedFox-started Repo redesign is a locked/fixed contract using vehicle value + Repo tier + route distance + Recovery skill + RLS economy/difficulty rather than destructive elapsed-time decay. Do not edit RLS `repo.lua`; scope any adapter to RedFox-started Repo work.

Native Off-Road Recovery findings:

- `MAX_OFFERS=3`
- `MAX_ACTIVE_PER_MAP=3`
- APIs include `getState`, `requestState`, `beginAcceptOffer`, `selectRecoveryYard`, `cancelYardSelection`, `previewOffer`, `trackJob`, `abandonJob`, `clearCompletion`, `isContractTarget`, `isContractInventoryId`.

Current native availability requires Recovery level >=5, economy enabled, purchased RLS Recovery Yard, and map recovery sites.

Owner's permanent RedFox rule is different:

**Every RedFox Tow Yard is automatically a Tow + Recovery destination/capability.**

There must not be a separate Recovery Yard checkbox/setup flow. Linking a purchased RLS property is a separate concern.

That RedFox-to-native recovery-yard bridge is still future work.

Only paid-source West Coast currently has off-road recovery sites. Future procedural site generation is desired for other maps, but must use exact BeamNG road/raycast/terrain/clearance APIs after source verification.

## RLS Business Manager

Public APIs verified:

- `registerBusiness(businessType, businessObject)`
- `registerBusinessCallback(businessType, callbacks)`
- `isPurchasedBusiness(businessType, businessId)`
- `showPurchaseBusinessPrompt(businessType, businessId)`
- `openBusinessMenu(...)` pattern used by Racing Team

## RLS Bank

Verified APIs:

- `createBusinessAccount`
- `getBusinessAccount`
- `getAccountBalance`
- `getAccountTransactions`

Business account IDs use:

`business_<businessType>_<businessId>`

The native bank supports personal <-> business transfers. Business-originated transfers can be pending for roughly five minutes depending on the native system.

RedFox Tow business IDs already established:

- business type: `redfoxTow`
- business ID: `redfox_tow_company`

## RLS Business Inventory

Verified APIs include:

- `storeVehicle`
- `getBusinessVehicles`
- `getVehicleById`
- `pullOutVehicle`
- `putAwayVehicle`
- `getPulledOutVehicles`
- `updateVehicle`
- `saveBusinessVehicles`

RLS Put Away explicitly captures live part conditions before removing the world vehicle and persisting business inventory.

RLS `BusinessVehiclesTab.vue` displays Business Inventory and provides Pull Out/Put Away, but also exposes Sell by default. RedFox must fail-close business sale unless the correct lifecycle/ownership/accounting path supports it.

## RLS Garage / Racing Team

RLS business garage uses a `businessGarageId` and resolves a `businessGarage` facility with `sitesFile` + `parkingSpotNames`.

RLS Racing Team opens its business computer through `businessManager.openBusinessMenu(...)` and registered `onMenuOpen`. That exact route did **not** solve the stock custom-business close/X issue for RedFox during runtime testing.

The RedFox-owned Vue page introduced in v35 closes using `window.bngVue.gotoGameState("play")`, which is why the project shifted away from depending on the broken stock RLS custom-business close path.

Exact RLS painting has a Racing-Team-specific hard-code in parts of its business flow. Do not blindly reuse it for RedFox without a scoped adapter.

## Normal Career garage findings used by Icebox

Exact normal Career/RLS garage source inspection found:

1. normal Career vehicle UI groups vehicles by `vehicle.location`;
2. normal UI uses `career_modules_garageManager.getGarageCapacityData()` for garage names/capacity;
3. stock `VehicleList.vue` / `VehicleTileRow.vue` provides the interaction the owner wants, including stock thumbnails/cards, selection/popover actions, Retrieve/Replace, Repair, Put in Storage, Favorite, plate, rename and normal list actions;
4. `career_modules_inventory.openMenuFromComputer(computerId)` opens the stock garage/vehicle-list route;
5. `career_modules_inventory.moveVehicleToGarage(inventoryId, garageId)` preserves the same Career inventory identity while changing garage location after normal checks;
6. RLS `garageManager.isGarageSpace(garageId)` and `getGarageCapacityData()` were identified as narrow seams usable for a synthetic garage lab.

---

# 3. JOB-09 version lineage and current baseline

Important recent lineage:

- v20 — mission reliability baseline
- v21 — RLS storage mirror + crash fixes
- v22 — rejected PC/phone lifecycle experiment; never restore the v22 Pull Out/Put Away shortcut
- v23 — safe baseline
- v24 — purchased RLS facility -> Tow Yard; process-tainted due preverification incident, later source-verified
- v25 — shared RLS Recovery XP
- v26 — dispatch queue/native off-road routing cleanup
- v27 — lighter Multi-Car pool + accepted jobs board
- v28 — RLS Tow business foundation
- v29 — business computer/storage pull-put prototype
- v30 — RLS Business Inventory Garage + Finances visible
- v31 — local WEUI sizing/F11 protection
- v32 — UI hold placement + game-day timer attempt
- v33 — business bank + company fleet + real-hour impound
- v34 — RLS Racing-computer path + easy fleet intake
- v35 — RedFox-owned Company Computer / fleet recovery visibility
- v36 — true-business-garage/cross-map transfer attempt; runtime garage UX/actions not accepted

## v35 package

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_5_0_35_REDFOX_COMPANY_COMPUTER_FLEET_RECOVERY.zip`

SHA-256:
`aac17362997cd6c13d5e7ce882850b28712daa4615ad622ea6459bc04d723ac6`

Audit:
`PROJECT_MANIFESTS/AUDITS/JOB-09_2026-08-22_v0.5.0.35_REDFOX_COMPANY_COMPUTER_FLEET_RECOVERY.md`

## v36 package — latest Tow build tested in this chat

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_5_0_36_TRUE_BUSINESS_GARAGE_CROSS_MAP_TRANSFERS.zip`

SHA-256 reported at packaging:
`954776f3a340b6a9d01cff1b9de36100b3f1c8d8550c34a7a19957ee604cea16`

New audit/runtime findings:
`PROJECT_MANIFESTS/AUDITS/JOB-09_2026-08-24_v0.5.0.36_TRUE_BUSINESS_GARAGE_CROSS_MAP_TRANSFERS_RUNTIME_FINDINGS.md`

### v36 owner test conclusion

Do **not** continue iterating Tow garage UI directly from v36 right now. The storage/garage experience is still wrong enough that the owner requested a separate garage lab instead.

---

# 4. What v35 successfully proved

Owner screenshots/runtime testing proved these useful things:

- the RedFox Tow Company Computer opens;
- it can display the real Tow business bank/account;
- business bank showed real money and **towing job money correctly goes into the Tow business bank** — owner explicitly confirmed this is good and must be preserved;
- it can see Fleet Book/Career records for existing company-marked trucks/trailers;
- a trailer that seemed to disappear had not been deleted;
- Tow Yard capacity/custody/company summary cards render;
- RedFox-owned computer avoids relying on the broken stock RLS custom-business X for the normal Tow workflow.

But v35 also proved the main structural failure:

**company-marked vehicles were still normal Career inventory vehicles underneath, so they appeared in personal garages and consumed personal garage capacity.**

That is not acceptable as the final business garage.

---

# 5. v35/v36 runtime garage problems — confirmed

From owner screenshots and direct testing:

## Duplicate yard identity/display

The UI showed both something like:

- `Chinatown Garage`
- `REDFOX TOWING`

for what was effectively the same physical property/location.

The final system must canonicalize the physical facility for display/counting while preserving stable internal yard identities. Do not destructively delete saved IDs just to make the screen look clean.

## Custody count mismatch

Different UI sections reported different numbers of vehicles in custody. The final Company Computer must derive totals/cards from one canonical custody collection so the same data says the same count everywhere.

## Company garage button wrong target

A Tow UI button labelled like:

`OPEN TOW COMPANY GARAGE — VEHICLES / EDIT / PAINT / PARTS`

opened the player's ordinary personal garage list rather than a true Tow-only garage.

## Custom company cards are not stock garage behavior

The RedFox Company Computer vehicle cards were custom presentation and did not behave like the stock Career/RLS garage.

Owner wants the normal game interaction model:

- consistent stock image sizing;
- normal left-click/select behavior;
- normal click/popover/context actions;
- Retrieve/Replace;
- Performance Index;
- Repair;
- Favorite;
- Paint/Customize;
- Parts/Configuration/Tuning;
- plate;
- rename;
- stock sort/filter behavior where practical.

RedFox should add only its extra business/yard actions on top.

## v36 image sizing problem

Custom `<img>` cards produced inconsistent-looking preview scale: some vehicle images appeared huge/full-card and others tiny. This reinforced the decision to reuse the stock garage components/presentation instead of trying to normalize custom cards manually.

## v36 controls not working

Owner reported:

- edit/paint/action buttons do not work correctly;
- vehicle move dropdowns do not work;
- `Search Vehicle` does not work;
- the list looks reasonably good but is still not the actual stock garage UX.

This is why Icebox was created.

---

# 6. RedFox Icebox — standalone garage architecture lab

The owner explicitly asked to stop changing Tow over and over while discovering how the garage should work.

A separate temporary standalone mod was created:

**RedFox Icebox**

Purpose:

- master the normal Career/RLS garage architecture in isolation;
- prove stock garage UI/actions;
- prove independent 10-slot storage behavior;
- prove cross-map storage/retrieval concepts;
- only after it works, port the proven architecture back into Tow.

## Icebox v0.1.0 package

`RedFox_Icebox_v0_1_0_STANDALONE_GARAGE_LAB.zip`

SHA-256:
`c59233e77dfab48dffa7eccbfebf403e01f40c796f7d98cc009606e9789442ec`

Base audit:
`PROJECT_MANIFESTS/AUDITS/REDFOX-ICEBOX_2026-08-24_v0.1.0_STANDALONE_GARAGE_LAB.md`

Post-build owner directions:
`PROJECT_MANIFESTS/AUDITS/REDFOX-ICEBOX_2026-08-24_POST_BUILD_OWNER_DIRECTIONS_LOCATION_FREEROAM_MAP_ICONS.md`

## Icebox v0.1.0 files — exactly four

1. `lua/ge/extensions/redfoxIcebox.lua`
2. `scripts/redfox_icebox/modScript.lua`
3. `mod_info/redfox_icebox/info.json`
4. `lua/ge/extensions/redfox/modules/redfox_icebox/redfox_module.json`

JOB-09 files were intentionally untouched by the Icebox build.

## Icebox v0.1.0 design

Synthetic IDs:

- garage: `redfoxIceboxGarage`
- computer: `redfoxIceboxComputer`

Logical capacity: **10 vehicles**.

It was designed as a synthetic Career garage using normal Career inventory and the stock Career/RLS vehicle-list/computer flows rather than a custom RedFox garage screen.

The extension wraps only narrow runtime seams for the synthetic ID and delegates all non-Icebox calls to the original functions.

The intended first test is one expendable vehicle at a time. No automatic migration/batch movement.

### Icebox access

The Icebox setup/control window is a small WEUI/ImGui-style control panel.

The actual vehicle-management screen is intended to be the **normal game/RLS garage UI** after pressing:

`OPEN ICEBOX VEHICLE LIST — STOCK GARAGE UI`

Other lab actions include storing the current owned vehicle, opening the full garage computer for edit/paint/parts, and returning a vehicle to a personal garage.

## Icebox v0.1.0 physical anchor behavior

Current v0.1.0 automatically chooses a usable real garage on the current map as a temporary physical anchor so Retrieve/edit/paint/parts/tuning have real parking spots/zones/computer context.

The logical Icebox ID/capacity remains separate.

However, **the owner does not like silent automatic anchor selection** and asked for manual location choice. This is a next-version requirement and was NOT implemented before this handoff.

---

# 7. Icebox next requirements — NOT yet implemented

These are direct owner directions after v0.1.0 packaging.

## Manual physical location choice

Add obvious controls such as:

- `SET ICEBOX LOCATION`
- `CHANGE ICEBOX LOCATION`

Show valid current-map garages and let the owner explicitly choose the temporary physical anchor.

Always display which location Icebox is using.

Do not silently switch anchors unless the saved choice becomes invalid; if fallback is necessary, tell the player.

Borrowing a real garage as physical anchor must not alter, merge, rename, move or otherwise affect vehicles belonging to that real garage.

## Standalone custom Icebox location

Long-term Icebox should **not require an existing garage**.

After stock garage behavior is proven, add something like:

`MAKE ICEBOX HERE`

This should create/save a custom independent garage location using exact verified BeamNG/RLS facility/parking/computer APIs.

Do not guess facility internals.

## Free Roam access to Career/Icebox vehicles

Owner asked whether Icebox can also be a way to load Career vehicles in Free Roam.

Desired direction: build a safe bridge if exact APIs support it.

This is NOT implemented/verified yet.

First target should be a safe **read-only Free Roam spawn** of a selected Career/Icebox vehicle, preserving model/config/paint/condition/mileage where supported without silently modifying the Career save.

Do not create duplicate authoritative Career inventory records.

Source-first inspect Career profile/save/inventory access from Free Roam context before implementation.

If live Career modules are unsafe outside Career, use an explicit Icebox snapshot/export index rather than blindly writing Career data.

## Main Map + minimap icons

Owner requires future map markers for:

- every RedFox Tow Yard;
- RedFox Icebox.

Markers should show on both the main map and minimap where the current BeamNG/RLS marker APIs support it.

Tow Yard markers should use each saved yard's actual location and name and be visually distinguishable from ordinary garages/businesses.

Icebox marker should show its explicitly selected/custom physical location without renaming the underlying anchor garage.

Source-first inspect current BeamNG/RLS POI/map/minimap registration code before implementing.

---

# 8. Icebox runtime proof still required

At chat handoff, the owner had asked how to access/set up Icebox and then requested location-choice changes. There is no completed runtime proof yet in this chat that all stock UI/actions work.

Do not claim Icebox architecture proven until the owner tests it.

The core tests are:

1. put ONE expendable personally owned car/trailer into Icebox;
2. confirm source personal garage capacity frees by one;
3. open Icebox stock garage vehicle list;
4. confirm stock image/card sizing;
5. click/select vehicle and verify normal stock action menu;
6. Favorite multiple vehicles eventually;
7. Retrieve;
8. Repair;
9. Rename/plate;
10. Paint;
11. Parts/config/tuning;
12. Put Away;
13. save/reload identity/config/condition preservation;
14. change maps and retrieve the same saved Icebox vehicle at the new/current chosen physical location;
15. return the same vehicle safely to personal garage with no sale/purchase money event.

If the stock UI does not open correctly or controls do not work, fix Icebox only; leave Tow untouched until the pattern is proven.

---

# 9. Final Tow Company garage vision after Icebox is proven

The final Tow Company garage should behave like a normal Career/RLS garage, not a custom imitation.

## All Tow Yards visible

The Company Garage should show all Tow Yards, not only the current-map one.

Possible UI concept:

`ALL TOW YARDS | Yard A | Yard B | Yard C ...`

and filtering/sorting by:

- Favorites;
- name;
- assigned yard;
- mileage;
- value;
- recently added;
- vehicle type/class where useful.

Favorite must support **more than one vehicle** just like the game.

## Vehicle interaction

Use stock garage actions/components where possible.

RedFox-specific additions:

- `Move to Tow Yard`
- `Transfer to Personal Garage`
- `Ship to Tow Yard`
- company ownership/status
- custody/legal disposition actions on custody vehicles

## Personal -> Tow

Final normal flow should be simple:

`Transfer to Tow Company`

If only one yard exists, auto-assign it.

If multiple yards matter, allow choosing the yard.

Behind the scenes automatically perform all business/storage linking. The owner should not need to separately register/link the vehicle to the business.

No money changes hands merely because the owner moved an owned vehicle between personal and owned Tow business storage.

## Tow -> Personal

Provide `Transfer to Personal Garage` and choose a valid personal garage when needed.

Again, no sale/payment by default.

## Tow Yard -> Tow Yard across maps

Owner requires stored vehicles to move between Tow Yards even when the destination is on a different map.

Because the truck is a saved record, the source map should not need to be loaded simply to reassign/ship it.

Initial proof can be immediate saved garage-to-garage assignment.

Long-term workflow should become physical shipping:

1. owner travels to a new map;
2. owner creates a new Tow Yard/shop;
3. from the new shop, owner requests selected trucks/equipment from another Tow Yard/map;
4. transfer enters shipping/transit state;
5. vehicle eventually arrives at a dedicated map shipping/delivery location;
6. owner picks it up and/or sends it into the destination Tow Yard.

This shipping concept should later be reusable by other RedFox businesses where appropriate.

## Company storage capacity

Tow Yard **Company Fleet / Shop Bays** should be the logical business storage capacity.

Literal physical parking spots must not limit the total number of saved business assets. Physical vehicles should hydrate only when needed/nearby.

---

# 10. Tow business/yard architecture that should remain

One RedFox Tow Company / one RLS business account / many Tow Yard branches.

Custom Tow Yards may be arbitrary locations, including places that are not purchased RLS properties.

A purchased RLS property can be linked to a Tow Yard, but that should be optional and separate from Tow/Recovery capability.

Desired simple setup:

`MAKE TOW YARD HERE`

Then automatically:

- Tow Company exists;
- yard is Tow capable;
- yard is Recovery capable;
- computer/garage capability is attached;
- optionally ask whether to link a purchased RLS garage/property.

The first Tow Yard should become primary automatically.

Company display name should eventually be renameable per Career save while internal IDs stay stable:

- type `redfoxTow`
- business ID `redfox_tow_company`

Yard names should also be independently renameable.

---

# 11. Tow business bank/accounting — preserve

v33+ established the real RLS-backed Tow business account.

Owner has now runtime-confirmed:

**Tow job money goes into the Tow business bank. This is working.**

Do not regress it.

Tow payout settlement and Recovery XP settlement were separated so retry paths should not double-pay/deposit.

Ownership-at-sale rule desired across project:

- personal-owned vehicle sold personally -> personal proceeds;
- vehicle transferred to Tow ownership then sold -> Tow business proceeds;
- Tow asset transferred back to personal before sale -> personal proceeds;
- Tow direct auction consignment -> Tow proceeds according to Auction contract.

Movement between the owner's personal inventory and owned businesses should not create fake income unless an explicit sale transaction occurs.

---

# 12. Tow Yard custody / impound desired model

Owner wants one Tow Yard custody garage with status/categories rather than multiple fake copied vehicles.

Desired categories/statuses include:

- Abandoned Hold
- Unpaid Customer Tow
- Police Impound
- Recovered/Other
- Disposition Eligible

A vehicle should remain the same authoritative record while its status changes.

Desired cards/details:

- preview;
- year/model/config;
- mileage;
- condition;
- reason;
- yard;
- intake time;
- storage fees;
- remaining hold;
- search status;
- valid actions.

Normal abandoned/impound hold was changed away from frozen Career-day progression toward real elapsed hours because the owner's Career clock was not advancing reliably. Default/testing options were around 3h/6h/12h/24h with a developer disposition override for quick testing.

Automatic abandoned storage should attempt direct Tow Yard custody after successful delivery, falling back only if automatic custody fails.

A separate future physical-yard visualization should keep authoritative saved records and only hydrate a limited number of nearby full vehicles so large lots do not destroy memory/performance.

---

# 13. Tow WEUI / website direction

The current WEUI has grown cluttered. Desired future navigation is cleaner:

- Dispatch — available calls only
- Active Calls — accepted jobs
- Impound / Tow Yard Garage
- Company Fleet Garage
- Tow Yards
- Business / Finances
- Settings
- possibly Records / History

Recovery should not sit awkwardly in the middle of normal dispatch and active/post-tow decisions.

Long-term the owner wants a full RedFox Tow website reachable from:

- WEUI;
- phone;
- PC/business computer;
- full-screen website.

All surfaces should use the same backend/state rather than duplicate business logic.

F11/World Editor previously changed global ImGui scaling and blew up the Tow WEUI. v31/v32 added local sizing/protection controls. Preserve those unless intentionally replacing the WEUI.

---

# 14. Tow job variety desired

Keep existing jobs and add more variety over time:

- standard tow;
- rolled vehicle;
- semi rollover;
- multi-car cleanup;
- abandoned;
- Repo;
- native Off-Road Recovery;
- illegal/private-property parking;
- lockout;
- jump start;
- tire repair/change;
- fuel delivery;
- minor roadside repair;
- winch-out;
- heavy/rotator work;
- Random Events integrations.

Owner wants a new-call popup for useful decision information, e.g. call type + distance + estimated payout + Accept/Decline.

Settings should support On Duty and per-job filters so the player can receive only selected call categories.

Illegal-parking future concept:

- dispatched calls plus opportunistic randomly spawned illegal parks near the player;
- real parking/business/road areas;
- cock-eyed/across spaces/blocking entrances/etc.;
- obvious offending-car marker;
- nearby accept/ignore;
- vehicle condition can vary widely;
- almost all owners eventually reclaim, tiny fraction become unclaimed/disposition;
- `CASH ONLY` can be flavor text but money remains normal game/business money.

---

# 15. Random Events / external integration architecture

Random Events remains a desired JOB-09 integration, but should use a bridge architecture:

**Tow Core -> RedFox Integration Bridge -> provider adapter -> outside mod**

Tow should not directly depend on third-party mod internals.

Bridge should own:

- provider enabled/disabled;
- include in random dispatch;
- manual request availability;
- compatibility state;
- fail-closed behavior when third-party updates break the adapter.

Desired settings:

- Enable Integration
- Include Random Events in Random Dispatch

Manual Random Events request should remain available even if random inclusion is disabled.

This work was intentionally deferred while business/storage foundation is unstable.

---

# 16. Car Lot / JOB-13 handoff already updated

The Auction/Car Lot chat has a full handoff here:

`MESSAGE_BOARD_HANDOFFS/JOB-13_2026-08-23_CAR_LOT_DEALERSHIP_EXPANSION_FROM_JOB-09.md`

It was updated again so the dealer uses its own **business/shop garage** for sale inventory and does not consume personal garage capacity.

Current commit for that update in this chat:
`ae99e01cbba50f240a85b442f23d00cca30d93c6`

Car Lot direction includes:

- starts at 10 stock slots, upgrades to 100;
- dealer/business inventory separate from personal garage;
- Tow -> Dealer, Auction -> Dealer, Personal -> Dealer;
- slow retail sales;
- customer financing;
- delinquent financing can generate Repo work for JOB-09;
- one vehicle lifecycle, no duplicate clone;
- future physical 100-car lot uses proximity/lightweight representation rather than 100 fully simulated vehicles.

Existing direct Tow -> Auction consignment handoff remains:

`MESSAGE_BOARD_HANDOFFS/JOB-13_2026-08-15_REQUIRED_EXTERNAL_CONSIGNMENT_API_FOR_JOB-09.md`

Protocol:
`redfox.externalConsignment.v1`

Suggested future Tow -> Dealer transfer protocol:
`redfox.externalDealerTransfer.v1`

Do not finalize function names until JOB-13 source review.

---

# 17. Wrecking Yard / JOB-04 handoff already exists

Tow Yard/business/location framework was previously handed to JOB-04 here:

`MESSAGE_BOARD_HANDOFFS/JOB-04_2026-08-16_FROM_JOB-09_TOW_YARD_BUSINESS_LOCATION_FRAMEWORK_PORT.md`

Keep JOB-04 and JOB-09 separate; share stable contracts/patterns, not mutable save tables.

---

# 18. Current outstanding map/navigation request

Owner's latest navigation requirement:

**Tow Yard icons and Icebox icon must show on the minimap and main map.**

This is documented but not implemented in Icebox/Tow during this chat after the request.

Before coding, inspect exact current BeamNG/RLS POI/map/minimap marker registration and use native-supported APIs.

Other-map yards should remain visible in company lists, but map markers only make sense on the level whose coordinates they belong to.

---

# 19. Current outstanding Free Roam request

Owner asked whether Icebox can be used to load Career vehicles in Free Roam.

This is a desired future capability but was not source-verified/implemented before chat handoff.

Preferred first design is safe/read-only:

- choose Career profile/save explicitly;
- choose Icebox/Career vehicle;
- hydrate/spawn a copy in Free Roam using exact model/config/paint/part-condition/mileage snapshot where supported;
- no silent write-back to Career;
- no duplicate authoritative Career record;
- explicit later write-back only if separately designed/approved with backup/transaction protections.

Source-first verify Career save/inventory APIs in Free Roam context before making claims.

---

# 20. Immediate next action for the new chat

Do **not** immediately build JOB-09 v37.

The owner intentionally created Icebox to stop burning Tow versions on garage experiments.

The next chat should:

1. read this handoff;
2. read the v35, v36 and Icebox audits referenced above;
3. wait for / review the owner's Icebox runtime screenshots and results;
4. if Icebox v0.1.0 needs fixes, modify **Icebox only**;
5. next likely Icebox changes are manual location selection and then custom location support, but still source-first;
6. prove the stock garage UI/actions and one-vehicle round trip before broadening;
7. only after Icebox architecture is proven should the owner be asked whether to port it back into JOB-09;
8. when eventually porting, preserve working Tow bank/recovery/business logic and add Tow-specific yard/shipping actions on top of the stock garage pattern.

If the owner immediately asks for a new Tow build anyway, confirm scope and use the exact latest Tow archive/source before editing.

---

# 21. New GitHub documentation commits created at chat close

v36 runtime/build findings:
`e15eca60f1d7ad43c563a607e29ed1a59aff2424`

Icebox post-build location/Free Roam/map-icon requirements:
`07bb04794900983f60afd52d9105a1903b6a6537`

This master handoff commit will be the commit that created this file.

---

# 22. Short continuation summary

**Tow money/business bank works. Garage architecture does not yet meet the owner's expectations. Stop changing Tow garage code. Use RedFox Icebox to prove the stock Career/RLS garage architecture first. Icebox v0.1.0 exists with 10 slots but still auto-selects a physical anchor; the owner wants manual anchor choice, eventual custom `MAKE ICEBOX HERE`, safe Career-vehicle spawning in Free Roam, and Tow Yard/Icebox markers on minimap + main map. After Icebox works, port the proven normal-garage behavior into Tow and add cross-map Tow Yard shipping/transfer on top. No automatic fleet migration.**
