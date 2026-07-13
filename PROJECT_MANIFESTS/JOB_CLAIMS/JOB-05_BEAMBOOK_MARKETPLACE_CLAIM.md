# 5 — JOB-05 — BeamBook Marketplace — Claim Record

**Status:** CLAIMED — IMPLEMENTATION BLOCKED PENDING SHARED CONTRACTS  
**Owner/chat title:** 5 — JOB-05 — BeamBook Marketplace  
**Claim date:** 2026-07-13  
**Repository:** `redfoxtrystman/RedFox_Master_Control`

## Hello to the other RedFox chats

Hello JOB-00 through JOB-12. This chat claims exactly one role: **JOB-05 — BeamBook Marketplace**.

JOB-05 will build BeamBook as its own isolated, removable add-on mod after the shared platform, route, Career/RLS bridge, baseline, and testing contracts are published. JOB-05 will not copy or replace shared phone, PC, IceFox/FoxNet, registry, bridge, Career/RLS, money, inventory, ownership, garage, storage, insurance, or another app's files.

GitHub coordination issue:

`https://github.com/redfoxtrystman/RedFox_Master_Control/issues/1`

## Product direction owned by JOB-05

Combine David's existing Facebook-style BeamBook website design with the proven behavior and order of operations from the existing standalone `beamBook.zip`.

The target is a real **BeamBook Marketplace** social/marketplace app, not a generic Private Seller page.

JOB-05 owns only:

- BeamBook Wall/news-feed presentation.
- BeamBook Marketplace storefront.
- BeamBook listing cards.
- Seller/profile/post/comment presentation.
- Saved-listings presentation.
- Groups presentation.
- Messages presentation only where it belongs inside BeamBook; JOB-12 still owns FoxMail and FoxText.
- BeamBook-specific editable post/listing content, including the existing `assets/config/beambook_posts.json` concept if that path is confirmed in the frozen baseline.
- BeamBook-specific assets and documentation.
- Responsive BeamBook layouts for phone and PC while both hosts open the same canonical BeamBook destination.

Vehicle and other transactions must use the approved JOB-02 Career/RLS contract. JOB-05 will not implement fake purchases, fake money, fake ownership, fake storage, fake garage insertion, or direct spawn as purchase success.

## Exact artifacts and paths to inspect before editing

- The exact baseline selected and frozen by JOB-00.
- David's exact current `beamBook.zip` standalone marketplace mod.
- David's exact current Facebook-style BeamBook website/FoxNet baseline archive.
- Every frozen-baseline path containing `beamBook`, `beambook`, `BeamBook`, or `privateSeller`.
- Existing BeamBook manifest, entry HTML, JavaScript, CSS, JSON/content, icon/assets, and BeamBook-specific Lua files, if present.
- `assets/config/beambook_posts.json`, if present in the selected baseline.
- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`.
- `PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md`.
- `INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md`.
- Published JOB-01 manifest/route/phone-PC host contract and exact commit.
- Published JOB-02 Career/RLS bridge contract and exact commit.
- Published JOB-11 verification/report contract and exact commit.

No feature code will be edited until these inputs identify the exact BeamBook-owned paths.

## Files JOB-05 may edit after dependencies are published

Only:

- BeamBook-owned files inside the isolated add-on path assigned by the JOB-01 contract.
- The BeamBook app manifest using the canonical schema and ID assigned by JOB-01.
- BeamBook entry HTML.
- BeamBook app JavaScript.
- BeamBook app CSS.
- BeamBook-specific JSON/content files.
- BeamBook-specific icons/images/assets.
- JOB-05-specific change-scope, verification, inventory, tree, logging, changelog, and handoff reports.

JOB-05 will publish the exact filenames and archive paths after baseline inspection. It will not invent a competing folder, manifest schema, route, event, or bridge just to begin early.

## Protected files and systems JOB-05 must not edit or package

- Existing BeamNG/RLS phone shell or phone launcher.
- Existing BeamNG/RLS PC shell or PC launcher.
- Shared IceFox/FoxNet platform core.
- Shared browser, registry, navigation, destination, theme, or responsive-host core.
- JOB-02 shared Career/RLS bridge implementation.
- JOB-03 App Store implementation.
- BeamNG or RLS original Career modules.
- `career_modules_vehicleShopping` or `career_modules_inventory` source.
- Money, ownership, inventory, insurance, garage, or storage implementations.
- Startup Career modules or startup `vehicleShopping` patches.
- Scrap Yard, Import/Export, Classics, Insurance/Finance/Garage/Storage, Tow/Recovery/Dispatch, SponsorHub, FoxMail, FoxText, Sponsor Rewards, FoxFax, or Visual Design-owned files.
- Coordinator-owned baseline/integration files except this JOB-05 claim and requested JOB-05 handoffs.

The isolated BeamBook add-on must not contain duplicated shared platform or bridge files.

## Working behavior to preserve during inspection

The standalone BeamBook baseline is known to use marketplace order-of-operations patterns involving:

- `util_configListGenerator.getEligibleVehicles()`
- `util_configListGenerator.getRandomVehicleInfos()`
- `career_modules_vehicleShopping.getVehiclesInShop()`
- `career_modules_vehicleShopping.getShoppingData()`

These names are inspection targets, not permission for JOB-05 to patch Career/RLS internals. Any needed action must be exposed by the versioned JOB-02 contract.

## Dependencies and required contract commits

- **JOB-00:** claim acknowledgement, one frozen baseline, integration approval.
- **JOB-01:** canonical manifest, route, same-destination, phone/PC host, shared-file ownership contract.
- **JOB-02:** current-session/all-map vehicle data, purchase, ownership/storage result, error, and logging contract.
- **JOB-11:** required evidence matrix, status labels, report templates, duplicate/protected-path scans.
- **JOB-10:** visual polish may be coordinated later without changing BeamBook behavior.
- **JOB-03:** App Store integration is optional/deferred and does not block the initial isolated BeamBook add-on once JOB-01's registry contract exists.

JOB-05 will link the exact producer commit and contract version it consumes. It will not silently copy or fork a shared contract.

## Verification plan

1. Record exact baseline filenames and SHA-256 hashes.
2. Inventory every BeamBook-related file before edits.
3. Record last known useful and first bad BeamBook packages where evidence exists.
4. Diff only BeamBook-owned files.
5. Validate the manifest and all BeamBook JSON/HTML/JS/CSS.
6. Verify phone and PC resolve to one canonical BeamBook destination.
7. Verify the route has no West Coast-only map, shop, facility, garage, or storage assumptions.
8. Verify every Career/RLS data/action request uses the exact JOB-02 contract version.
9. Scan for copied platform/bridge files, startup patches, fake transaction logic, duplicate IDs, duplicate archive roots, overlapping shared FoxNet paths, and `__pycache__`.
10. Render and inspect phone and PC BeamBook layouts.
11. Include all JOB-11-required TXT, HTML, JSON, CSV, file-tree, scope, logging, changelog, and verification reports.
12. Use `[RedFox][BEAMBOOK]` plus the shared phone/PC/bridge prefixes defined by the contracts.
13. Label static output **BUILT — RUNTIME UNTESTED** until David tests the exact build in BeamNG.
14. Test West Coast USA and at least one non-West-Coast map through David's runtime test plan before any all-map claim.

## Expected outputs

After dependencies are ready:

- One isolated BeamBook add-on mod.
- Facebook-style BeamBook Wall and Marketplace presentation.
- Preserved proven marketplace behavior through the approved shared contracts.
- One canonical phone/PC destination with responsive layouts.
- Editable BeamBook-specific content.
- Exact file inventory and protected-file proof.
- Required verification and logging reports.
- A versioned JOB-05 handoff for JOB-00 integration.
- No integrated FoxNet ZIP until JOB-00 approves it.

## Current action

This claim completes the Git rollcall for JOB-05. It does not select a baseline, edit feature code, or build a ZIP.
