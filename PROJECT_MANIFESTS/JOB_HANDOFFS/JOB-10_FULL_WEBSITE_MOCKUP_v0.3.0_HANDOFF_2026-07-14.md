# JOB-10 — Full Website Mockup v0.3.0 Handoff

**Date:** 2026-07-14 PDT  
**JOB:** JOB-10 — Visual Design / Real Website Polish  
**Status:** MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG  
**Package:** `RedFox_JOB10_Full_Websites_v0_3_0.zip`  
**Package bytes:** `50,819,666`  
**Package SHA-256:** `b0f69fd1fa97d28a80882d784ad4fe37b91590b2375c60851dcf053a27d32970`  
**Primary file:** `START_HERE.html`  
**Primary file bytes:** `35,741,257`  
**Primary file SHA-256:** `d67bdd133a23ae1e46ebf5b9be044a7f14bc41ae5937aaf02c0b6c55413f7857`

## What changed

### FoxNet Auctions

- The active mock auction pool is capped at exactly **100 vehicles**.
- Category buttons now filter independent pools rather than acting as decoration.
- Current visual distribution:
  - Cars: 50
  - Work Trucks: 20
  - Semis: 10
  - Off-Road: 15
  - Electric: 5
  - Motorcycles, Boats, Aircraft and Helicopters: 0 until supported vehicle content is available
- Empty categories remain visible and correctly show zero rather than routing to unrelated vehicle content.
- Added a deterministic **next in-game day** simulation that rotates years, trims, conditions, pricing, mileage, lot numbers and ordering.
- Final BeamNG integration must refresh from real supported vehicle/configuration data once per in-game day; this mockup does not implement game-time hooks.

### Real BeamNG imagery

- Added 21 supplied BeamNG vehicle screenshots to auction, featured-vehicle, listing and social areas.
- Added 12 supplied BeamNG scene/loading screenshots to BeamBook posts.
- Runtime requirement remains that vehicle cards use the actual vehicle/configuration thumbnail supplied by the game rather than unrelated stock photography.

### BeamBook people and Wall rotation

- Added 12 original illustrated face avatars for made-up BeamBook users.
- Added 10 visible contacts with face avatars and online indicators.
- Expanded the Wall to 12 humorous, serious and strange BeamNG-flavored posts.
- Four posts display at a time.
- The Wall can refresh manually and rotates automatically while the feed is open.
- Marketplace and vehicle-detail behavior from the prior mockup remain preserved.

### Scrap Yard corrections

The visual processing choices now match David's definitions:

1. **Full car sale**
   - The yard keeps the entire car and every part.
   - No parts are returned.
   - No dismantling labor is charged.
   - The fast-sale payout is intentionally lower than the full part-out value.

2. **Hire yard to strip it — keep parts**
   - The yard removes the parts.
   - All usable parts are sent to the player's Parts Shop.
   - Dismantling labor is deducted from the chassis credit.
   - The player does not receive the full possible cash value because labor is paid.

3. **Process all manually**
   - The player removes the parts by hand.
   - The removed parts go to the player's Parts Shop.
   - The yard pays only for the stripped chassis and scrap metal.
   - No yard dismantling labor is charged.

Actual inventory transfer, parts-market demand, AI purchases and money mutation remain backend work owned by the appropriate jobs.

### UndergroundNet visual separation

The underground services no longer reuse one repeated page template. Each now has a separate presentation:

- Black Market — anonymous red/black encrypted vehicle listings
- Shadow DMV — paperwork and government-office queue styling
- Chop Shop — industrial dismantling bay with hazard treatment
- Most Wanted — paper/bounty-board vehicle target styling
- High Risk — freight-route and risk-dashboard styling
- Cold Storage — private container/bay storage grid

## Files affected in the delivered standalone package

```text
START_HERE.html
index.html
assets/css/app.css
assets/js/app.js
assets/images/vehicles/real/*
assets/images/beambook/scenes/*
assets/images/beambook/avatars/*
CHANGE_SCOPE_JOB10_v0_3_0.txt
OPEN_THIS_VERIFICATION_REPORT_JOB10_v0_3_0.txt
OPEN_THIS_VERIFICATION_REPORT_JOB10_v0_3_0.html
VERIFY_JOB10_v0_3_0.json
VERIFY_JOB10_v0_3_0_FILE_INVENTORY.csv
FILE_TREE_JOB10_v0_3_0.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
README_OPEN_FIRST.txt
```

No repository runtime mod source was changed or packaged by this handoff.

## Verification performed

- Source JavaScript parse: PASS
- Bundled JavaScript parse: PASS
- ZIP integrity: PASS
- Self-contained CSS/JavaScript/image delivery: PASS
- Full embedded HTML loaded in isolated Chromium: PASS
- Exactly 100 auction lots: PASS
- Category filtering: PASS
- Daily rotation simulation: PASS
- BeamBook four-post Wall: PASS
- Ten face-avatar contacts: PASS
- Manual Wall refresh changes visible posts: PASS
- Three corrected Scrap Yard processing paths: PASS
- Six distinct UndergroundNet page layouts: PASS
- Global dark/light toggle: PASS
- Uncaught JavaScript errors during automated interaction test: NONE

## Protected scope

This package does not edit or implement:

- BeamNG or RLS runtime files;
- Career modules;
- shared bridge contracts;
- money, ownership, inventory, garage, storage or insurance mutation;
- purchasing or selling logic;
- mission logic;
- map-specific facilities;
- phone, PC, launcher or registry code;
- another job's source tree.

## Current status

```text
JOB-10 VISUAL MOCKUP v0.3.0 BUILT — STATIC/INTERACTION VERIFIED — AWAITING DAVID VISUAL REVIEW — NOT INTEGRATED
```

## Required next steps

1. David opens `START_HERE.html` and reviews the revised Auctions, BeamBook, Scrap Yard and UndergroundNet pages.
2. Preserve the rest of the approved visual work unless David identifies a specific change.
3. After visual approval, each backend-owning job supplies a stable page contract and exact presentation-only edit boundary.
4. JOB-10 maps approved visual components onto those stable functional pages without changing backend event names or behavior.
5. JOB-11 verifies integration scope and David tests the exact BeamNG candidate before any runtime-working claim.
