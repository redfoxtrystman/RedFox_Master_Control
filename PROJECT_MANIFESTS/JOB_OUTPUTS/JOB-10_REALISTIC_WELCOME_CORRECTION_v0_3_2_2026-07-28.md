# JOB-10 Realistic Welcome Correction v0.3.2

**Date:** 2026-07-28  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Owner:** David / Captain  
**Status:** WEBSITE PROTOTYPE — NOT BEAMNG-INTEGRATED

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

The failure is documented separately at:

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

JOB-10 remains website-only. The working JOB-09 and JOB-04 systems will later provide or consume approved page routes/data contracts; their code is not combined into this package.

## Verification

```text
JavaScript syntax: PASS
Desktop render 1440x1100: PASS
Mobile render 390x844: PASS
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
BeamNG runtime integration: NOT TESTED / NOT INCLUDED
```

Preview files included:

```text
PREVIEW_REALISTIC_WELCOME_DESKTOP.png
PREVIEW_REALISTIC_WELCOME_MOBILE.png
```

Mandatory scope, verification, JSON, CSV inventory and file-tree reports are included in the ZIP.

## Current state

This is the corrected full browser website package for David's visual review. It is not a BeamNG release or a combined mod. Do not integrate or overwrite the working Tow/Wrecking Yard gameplay ZIPs until David approves this welcome screen and the owning jobs provide exact connection boundaries.
