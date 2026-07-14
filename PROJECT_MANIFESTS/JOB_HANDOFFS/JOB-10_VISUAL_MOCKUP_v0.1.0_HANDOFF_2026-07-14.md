# JOB-10 — Visual Design / Real Website Polish — Visual Mockup v0.1.0 Handoff

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 14:03 PDT (America/Los_Angeles)  
**JOB:** JOB-10 — Visual Design / Real Website Polish  
**Status:** MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG  
**Package:** `RedFox_JOB10_Visual_Mockup_v0_1_0.zip`  
**SHA-256:** `a44f146833dccbb5c17ee31cc6857cf8f3ffe6d1862dd62623bfab3cf2a3c0a6`

## What changed

JOB-10 created a standalone offline HTML/CSS/JavaScript prototype so David can review the visual direction before any game-code integration.

The prototype includes:

- IceFox browser shell, navigation, address/search field and light/dark control;
- responsive desktop and phone layouts;
- BeamBook Facebook-style social feed and Marketplace presentation;
- FoxNet Auctions Copart/IAA-style search, categories, membership and lot detail presentation;
- FoxFax CarFax-style report page using David's approved female fox mascot;
- XXX Insurance luxury black/pink service and quote presentation aligned to RLS coverage classes;
- Collector Exchange premium black/gold collector docket presentation;
- Parts Exchange familiar parts-store/search presentation;
- Export Yard nautical freight, quote and container tracking presentation;
- renameable Recovery/towing-company website presentation;
- separate BackAlley.help illegal-network identity;
- rotating humorous advertisement slots;
- intentional humorous 404 page;
- current-map selector demonstrating map-agnostic presentation.

## Why it changed

David requested a realistic, viewable website mockup before linking pages to BeamNG/RLS code. This isolates visual approval from runtime integration risk and gives all feature jobs one shared visual target.

## Source/reference inputs inspected

```text
redfox_web_ecosystem_v1_combined_VERIFIED.zip
BeamBook_ROUTE_FIX_DROP_IN_v1_3.zip
beamBook.zip
icefox_browser_frontpage_v0_6_4_EMBEDDED_FOX_SAFE.zip
site_shots.zip
rls_career_overhaul_2.6.6.zip
RedFox_RLS_Evidence_v03.zip
RedFox_RLS_Evidence_v03_SUMMARY_ONLY.zip
west_coast_usa.zip
rls_slop_gear_garage_v0.2.zip
backAlley.0.2.2-alpha.zip
David's FoxFax female mascot image
David's IceFox target mockup image
RedFox website roadmap text files
```

The West Coast archive was inspected only as reference evidence. It is not packaged and is not a required location dependency.

## Files in the downloadable package

The package contains:

```text
index.html
assets/css/app.css
assets/js/app.js
approved/reference visual assets
docs/DESIGN_SYSTEM_AND_PAGE_MATRIX.md
docs/previews/*.png
CHANGE_SCOPE_JOB10_v0_1_0.txt
OPEN_THIS_VERIFICATION_REPORT_JOB10_v0_1_0.txt
OPEN_THIS_VERIFICATION_REPORT_JOB10_v0_1_0.html
VERIFY_JOB10_v0_1_0.json
VERIFY_JOB10_v0_1_0_FILE_INVENTORY.csv
FILE_TREE_JOB10_v0_1_0.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
README_OPEN_FIRST.txt
```

## Verification performed

- JavaScript syntax validated with `node --check`.
- Desktop rendering inspected at 1440 × 1000.
- Mobile rendering inspected at 390 × 844.
- Home, BeamBook, Auctions, FoxFax, Insurance, Export Yard and Recovery rendered successfully.
- Every top-level browser destination has page output.
- Unknown destinations route to the intentional 404 page.
- Current-map selector updates map-sensitive text.
- Ads rotate in component slots.
- Recovery business name can be changed in the standalone browser prototype.
- No external CDN or internet connection is required.

## Protected scope confirmed

The package contains no BeamNG/RLS runtime code and does not edit or replace:

- Career modules;
- phone or PC platform source;
- route registry or shared bridge;
- money, inventory, vehicle ownership, garage or storage;
- insurance calculation/authority;
- missions, facilities or delivery systems;
- vehicle-shopping, inspection or purchase logic;
- another job's integrated source.

## Vehicle image rule

The mockup uses existing supplied RedFox/BeamNG-named SVG visual slots. Final runtime pages must obtain images from the actual in-game vehicle/configuration or an approved game-rendered thumbnail pipeline. Unrelated stock vehicle photography is not an approved final source.

## All-map requirement

The visual prototype does not require a West Coast facility. Runtime page text and service locations must derive from the current career map and available facility/mission data. Unsupported facility types should use a truthful unavailable state rather than silently pointing to West Coast USA.

## Required next steps

1. David opens `index.html` and records visual changes page by page.
2. JOB-10 revises the standalone mockup until visual direction is approved.
3. Each feature job provides a stable functional page and exact presentation-only edit boundary.
4. JOB-10 publishes an exact per-page integration manifest.
5. JOB-11 verifies that visual changes do not alter IDs, handlers, routes, bridge messages or backend behavior.
6. David tests the exact integrated candidate in BeamNG before any working/fixed/done claim.

## Known limitations

- This is not connected to BeamNG or RLS.
- Vehicle art is not yet live game thumbnail output.
- Buttons demonstrate intended flows but do not execute Career actions.
- Some site depth is intentionally simplified for the first visual review.
- The downloadable ZIP is delivered in the active regular chat; this repository record preserves its exact identity and scope.