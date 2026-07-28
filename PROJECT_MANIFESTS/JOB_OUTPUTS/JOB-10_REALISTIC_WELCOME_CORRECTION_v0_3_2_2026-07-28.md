# JOB-10 Realistic Welcome Correction v0.3.2

**Date:** 2026-07-28  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Owner:** David / Captain  
**Status:** WEBSITE PROTOTYPE — MOBILE VISUAL BASELINE ONLY — NOT BEAMNG-INTEGRATED

## Phone-only architecture correction

The current controlling owner directive is:

```text
PROJECT_MANIFESTS/OWNER_PHONE_ONLY_ARCHITECTURE_DIRECTIVE_2026-07-23.md
```

Directive commit:

```text
43ee97781b42307f2769011c02c9afa1bfe5c723
```

The active release target is:

```text
REDFOX / FOXNET PAGES RUN ON THE IN-GAME PHONE ONLY
PHONE PLATFORM CORE: ACTIVE
PC PLATFORM CORE: DEFERRED
```

JOB-10 missed this newer directive when v0.3.2 was first documented. The incident is recorded at:

```text
INCIDENT_REPORTS/2026-07-28_JOB-10_PHONE_ONLY_DIRECTIVE_MISSED.md
```

Correction:

- v0.3.2 is preserved as a website visual reference.
- The mobile render is the relevant design baseline.
- The desktop render is reference-only and is not a BeamNG runtime target, release gate or integration requirement.
- All later JOB-10 builds must be designed and tested phone-first.
- No PC-specific page, browser-shell, garage-computer or parity work is part of the current JOB-10 target.

## Corrected package

```text
RedFox_JOB10_Full_Websites_v0_3_2_REALISTIC_WELCOME.zip
```

SHA-256:

```text
fab5913a9d1b580b0ff32d6ea6d53d8f8983fe2b9ddf9110aa79742c7679b5e5
```

## Baseline and failure correction

This build returns to David's supplied and approved visual baseline:

```text
RedFox_JOB10_Full_Websites_v0_3_0(7).zip
```

It replaces the rejected cartoon-style welcome preview:

```text
RedFox_JOB10_IceFox_Welcome_Preview_v0_1_0.zip
```

The cartoon-art failure is documented separately at:

```text
INCIDENT_REPORTS/2026-07-28_JOB-10_WELCOME_PAGE_CARTOON_ART_DIRECTION_FAILURE.md
```

Failure commit:

```text
33fbe593cf9739308d9d5eeb7dd8f9f40d7319f1
```

## What changed

- Rebuilt the IceFox welcome screen from the v0.3.0 full-website baseline.
- Removed flat cartoon vehicle art from all welcome service cards.
- Replaced service-card vehicle art with real BeamNG vehicle renders and game screenshots supplied inside the approved project package.
- Kept the approved FoxFax mascot on the FoxFax card.
- Added a top BeamWire scrolling headline strip.
- Added exactly 100 unique source headlines; the rendered strip duplicates them once only for seamless scrolling.
- Included BeamNG updates, official map names, current community map/mod names, RLS-market flavor, in-game weather/traffic events and humorous local headlines.
- Added the requested East Coast tornado headline.
- Preserved the v0.3.0 welcome structure, browser chrome, quick-access grid, advertisement slot and real featured vehicle listings.
- Renamed the welcome presentation from Scrap Yard to Wrecking Yard.
- Added documented replaceable image folder:

```text
assets/images/welcome/
```

- Added:

```text
WELCOME_IMAGE_REPLACEMENT_GUIDE.txt
assets/config/news_ticker.json
```

## Supplied verified websites preserved

The following uploaded verified website packages were copied unchanged into separate website folders:

```text
sites/foxfax_verified/
sites/recovery_verified/
sites/underground_verified/
sites/xxx_insurance_verified/
```

The welcome cards and top browser navigation link to these independent copied websites.

This means:

- Towing & Recovery uses the supplied Recovery site style/colors.
- XXX Insurance uses the supplied black/pink/lace site unchanged.
- FoxFax uses the supplied CarFax-style site.
- UndergroundNet uses the supplied dark-market site.

## Protected gameplay mods

The working gameplay ZIPs were inspected only and were not changed, merged or repackaged:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_4_SafeFleetTowYardAssignmentNpcDriverReady(1).zip
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1(2).zip
```

JOB-10 remains website-only. The working JOB-09 and JOB-04 systems will later provide or consume approved phone-page routes/data contracts; their code is not combined into this package.

## Verification

```text
JavaScript syntax: PASS
Mobile render 390x844: PASS — ACTIVE DESIGN REFERENCE
Desktop render 1440x1100: PASS — REFERENCE ONLY, NOT RUNTIME TARGET
Welcome service cards: 10
Unique ticker source items: 100
Rendered ticker nodes: 200 for seamless duplicate track
Theme toggle dark to light: PASS
Uncaught browser errors: 0
Real BeamNG welcome vehicle imagery: PASS
Verified FoxFax website present: PASS
Verified Recovery website present: PASS
Verified UndergroundNet website present: PASS
Verified XXX Insurance website present: PASS
Working Tow gameplay mod edited: NO
Working Wrecking Yard gameplay mod edited: NO
Phone integration: NOT TESTED / NOT INCLUDED
PC integration: DEFERRED BY OWNER — NOT PART OF CURRENT RELEASE TARGET
```

Preview files included:

```text
PREVIEW_REALISTIC_WELCOME_MOBILE.png — active visual reference
PREVIEW_REALISTIC_WELCOME_DESKTOP.png — non-runtime design reference only
```

Mandatory scope, verification, JSON, CSV inventory and file-tree reports are included in the ZIP.

## Current state

This is a corrected browser website prototype for David's visual review. It is not a BeamNG release or a combined mod. Its mobile presentation is the current useful reference. All subsequent work must target the approved in-game phone only. Do not integrate or overwrite the working Tow/Wrecking Yard gameplay ZIPs until David approves the mobile welcome screen and the owning jobs provide exact phone connection boundaries.