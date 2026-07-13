# JOB-06 — Import / Export Yard — Claim Record

**Status:** CLAIMED

**Owner:** Import / Export Yard chat / Sol

**Claim date:** 2026-07-13

**Repository:** `redfoxtrystman/RedFox_Master_Control`

**Governing directive:** `PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md`

**Directive commit reviewed:** `a05e06829548ddc4e7f5e39ac4a060eb57a0ef70`

**Rollcall/board correction commit reviewed:** `4475437092b7e6012b6174d880210685a1eab928`

## Hello to the other RedFox chats

Hi fellow RedFox rebuild chats. This chat has claimed exactly one job: **JOB-06 — Import / Export Yard**. I own only the Import / Export app/page and its future gameplay plan. I will use the shared platform, Store, and Career/RLS contracts published by their owners; I will not copy, replace, or modify those systems or any other app.

## Phase 1 scope owned by JOB-06

- One isolated, removable Import / Export add-on mod with unique paths and IDs.
- An installable online Import / Export vehicle app/page.
- Decent import/export vehicles rather than pure scrap inventory.
- Buy-now listings only; no auction behavior.
- Import/export branding, page-specific listing presentation, filters, and vehicle-detail UI.
- Buy requests routed only through the approved JOB-02 shared bridge and the existing stock/RLS purchase flow.
- JOB-06 app manifest content after JOB-01 and JOB-03 publish the shared location and schema.
- Future-only planning for an export yard, a ten-vehicle hotlist, sightings/notifications, delivery checks, and export payout flow.

JOB-06 does not own the phone, PC, browser, launcher, App Store, shared bridge, Career/RLS systems, or another app/page.

## Baseline inspection result

The control repository currently contains manifests and incident reports, but no Import / Export website source or baseline ZIP.

The project history names this earlier candidate:

```text
Export_Yard_DROP_IN_v1
```

That candidate is not present in this repository. Its incident report says hover/menu behavior was represented as working from static checks and that assistant-generated SVG/structure replaced David's supplied visual intent. It must be treated as unproven reference material, not as a verified working base.

No implementation or ZIP may begin until the actual baseline is supplied or located and inspected.

## Files and folders JOB-06 will inspect before implementation

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- `PROJECT_MANIFESTS/JOB_CLAIMS/`
- `PROJECT_MANIFESTS/JOB_HANDOFFS/`
- `INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/2026-07-07_RedFox_Web_Ecosystem_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/2026-07-08_FoxNet_IceFox_RLS_Web_Integration_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
- The actual `Export_Yard_DROP_IN_v1` package if recovered.
- David's latest working FoxNet/IceFox baseline ZIP and its complete file inventory.
- Any existing Import/Export, Export Yard, or shipping-yard page source and supplied visual assets.
- JOB-01's published app registration, launch, and phone/PC layout contract.
- JOB-02's published Career/RLS bridge contract and payload schema.
- JOB-03's published app manifest and installed/enabled state schema.
- JOB-11's shared logging and verification format.

## Files JOB-06 may edit after the baseline and contracts are proven

- Only the dedicated JOB-06 Import / Export app directory assigned by the JOB-01/JOB-03 contracts.
- Within that directory only: the JOB-06 app manifest, `index.html`, page-specific JavaScript, page-specific CSS, Import/Export assets, and JOB-06 configuration/data files.
- JOB-06 scope, changelog, file inventory, test, and verification reports.
- This claim record and JOB-06-specific handoff/planning documents.
- The main job board only for JOB-06 status and links requested by David.

The exact runtime paths will be recorded before editing. JOB-06 will not invent a shared directory or write into platform-owned files while JOB-01/JOB-03 contracts are pending.

## Protected files and systems JOB-06 will not edit

- Existing BeamNG/RLS phone and PC shells.
- Browser core, launcher, navigation, theme framework, registry implementation, and cross-app platform files owned by JOB-01.
- Shared UI-to-Lua Career/RLS bridge files and message definitions owned by JOB-02.
- RedFox Store implementation, installed/enabled state implementation, and shared manifest schema owned by JOB-03.
- Scrap Yard, BeamBook, Classics, Insurance/Finance/Garage/Storage, Tow/Recovery, Visual Design, QA UI, SponsorHub, FoxMail, FoxText, Sponsor Rewards, FoxFax, DMV, Dark Web DMV, or other app-owned files.
- Stock BeamNG/RLS Career modules and original RLS files.
- Money, inventory, garage, storage, insurance, vehicle-ownership, purchase, or sell implementations.
- `lua/ge/extensions/career/modules/` and all startup-loaded Career patches.
- Any other job's branch, files, or ZIP.

JOB-06 will not patch `vehicleShopping` at startup, call Career/RLS internals directly from a standalone page, spawn a vehicle as purchase success, hand-roll money/storage/garage/inventory, or package a duplicate phone/PC/FoxNet core.

## Dependencies and coordination

- David provides or identifies the actual current FoxNet/IceFox and Export Yard baseline files and supplied page assets.
- JOB-00 controls integration order and approval for any combined ZIP.
- JOB-01 publishes the app registration location, entry-path rules, phone/PC launcher behavior, and responsive host contract.
- JOB-02 publishes the versioned bridge contract. Phase 1 expects `RedFoxOpenVehiclePurchase` and its result message rather than direct Career/RLS calls.
- JOB-03 publishes the Store manifest schema, permissions, and install/enable/open state contract.
- JOB-11 publishes the shared test/report format.
- JOB-10 may polish shared visuals later without taking over JOB-06 behavior.
- JOB-09 may coordinate a future deliver-to-yard flow only after JOB-00 and JOB-02 approve the runtime design.

JOB-06 will ask on GitHub and wait rather than inventing a substitute for a missing shared contract.

## Contract commit ledger

No implementation contract is in use yet. JOB-06 remains inspection/planning only.

Before editing runtime app files, this claim or its implementation handoff must record the exact commit SHA used for:

- JOB-00 approved baseline selection.
- JOB-01 app manifest, canonical route, registration, and phone/PC host contract.
- JOB-02 Career/RLS bridge contract.
- JOB-03 Store/manifest contract only if JOB-03 is active and required.
- JOB-11 testing, logging, and evidence contract.
- Any JOB-04 or JOB-09 delivery/deep-link handoff used by future phases.

A branch name, file name, or verbal description is not a contract version. The exact Git commit is required.

## Phase 1 verification plan

Before any JOB-06 release, this chat will verify:

1. The exact baseline ZIP name, hash, extracted file tree, active entry path, and current visual assets are recorded before editing.
2. Only the dedicated JOB-06 app files are changed.
3. Every local `href`, `src`, script, stylesheet, image, and font reference resolves from the final packaged paths.
4. The JOB-06 manifest validates against the final JOB-01/JOB-03 schema and declares only approved permissions.
5. Phone and PC open the same canonical registered destination and use the same JOB-02 backend message contract; only responsive presentation may differ.
6. The page and route are tested on West Coast USA and at least one supported non-West-Coast map.
7. No West Coast-only shop, facility, dealer, parking, garage, route, or map ID is hard-coded. If a required RLS/BeamNG service is unavailable on a map, the page reports the exact unavailable dependency instead of substituting data or faking success.
8. Buy buttons are buy-now only and request the existing stock/RLS purchase flow through the shared bridge.
9. No auction logic, direct Career/RLS patch, custom money/inventory/garage/storage path, startup Career module, or fake purchase-success spawn exists.
10. No stolen/traffic sale, physical yard trigger, hotlist payout, sightings runtime, or delivery runtime ships in Phase 1.
11. Page-specific listing filters and details do not rewrite or fabricate authoritative Career/RLS purchase data.
12. No mockup, decorative control, or placeholder is included unless David explicitly approves it and it is labeled `MOCKUP / PLACEHOLDER — NOT FUNCTIONAL`. Otherwise the feature is reported as BLOCKED or PARTIAL.
13. The final ZIP is reopened and checked for integrity, correct BeamNG root depth, exact file inventory, duplicate shared cores, stale files, and forbidden paths.
14. Required TXT, HTML, JSON, CSV, file-tree, scope, logging, and verification reports are present.
15. The exact contract commit SHAs used are recorded in the verification report.
16. Static checks are labeled static. Runtime remains unproven until David tests the exact package in BeamNG. Phrases such as “working,” “fixed,” “done,” and “should work” are not used as proof.

If any required check fails, JOB-06 stops and reports the failure instead of shipping a mostly-passed ZIP.

## Expected Phase 1 output

- One dedicated Import / Export app/page using the shared platform and Store contracts.
- Decent import/export vehicle listings presented as buy-now inventory.
- Page-specific desktop and phone layouts without replacing either host shell.
- A valid JOB-06 app manifest using the approved schema and permissions.
- Calls to the approved shared purchase bridge only.
- Complete required verification and logging reports.
- No integrated ZIP until JOB-00 approves it.

## Future plan only — not approved runtime work

- Physical export yard sell/delivery point.
- Ten-vehicle target hotlist inspired by a movie-style boost list.
- Vehicle sightings and notifications.
- Safe ownership/eligibility/delivery validation.
- Approved export payout through existing Career/RLS systems.

These items remain planning only. No stolen vehicle, ambient traffic, delivery, or payout logic will be implemented until JOB-00, JOB-02, and the relevant gameplay jobs approve a safe design.

## Current action

This claim records JOB-06 ownership and says hello to the other chats. It does not implement the app, change runtime files, or build a ZIP.
