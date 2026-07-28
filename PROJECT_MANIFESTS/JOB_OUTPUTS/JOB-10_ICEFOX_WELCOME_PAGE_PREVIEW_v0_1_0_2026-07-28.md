# JOB-10 IceFox Welcome Page Preview v0.1.0

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Status:** MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG

## Purpose

This package is a standalone preview of the IceFox welcome/home page only. It does not merge, modify, or replace the working Tow/Recovery or Wrecking Yard mods.

Current working reference packages inspected but not edited:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_4_SafeFleetTowYardAssignmentNpcDriverReady(1).zip
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1(2).zip
RedFox_JOB10_Full_Websites_v0_3_0(6).zip
```

## Preview package

```text
RedFox_JOB10_IceFox_Welcome_Preview_v0_1_0.zip
```

SHA-256:

```text
f2f9db2444ed346c2eace2eb8c4ec683592604d04931fae024b712b2470e47d5
```

## Visual changes

The welcome page now follows the owner-approved IceFox browser reference more closely and gives each quick-access card a distinct real-website identity:

- FoxNet Auctions: blue salvage-auction / Copart-inspired presentation.
- BeamBook: visible Facebook-style post header and social-feed treatment.
- FoxFax Reports: retained mascot/report presentation.
- Collector Exchange: premium black/gold collector-auction presentation.
- XXX Insurance: black and hot-pink lace presentation.
- Parts Exchange: bold auto-parts retailer treatment inspired by major parts stores.
- Export Yard: ocean/port presentation retained.
- Towing & Recovery: 24/7 rollback/recovery treatment.
- Wrecking Yard: renamed from Scrap Yard on the welcome page and treated as salvage/wreck inventory.
- UndergroundNet: crop corrected with a dedicated restricted-network treatment.

## Replaceable images

All welcome-page images are in one folder:

```text
assets/images/welcome/
```

A complete replacement guide is included:

```text
WELCOME_IMAGE_REPLACEMENT_GUIDE.txt
```

The package also contains:

```text
START_HERE_SINGLE_FILE.html
```

This fully self-contained HTML prevents the prior missing-CSS/missing-image preview failure.

## Route boundaries

The preview exposes these presentation routes only:

```text
foxnet
beambook
foxfax
collector
insurance
parts
export
towing
wrecking
underground
```

Each route currently opens a clear website connection-point placeholder. The owning feature job keeps its working code and later supplies the stable destination. JOB-10 will connect the visual route without merging the feature ZIP into the welcome-page package.

## Verification

- JavaScript syntax check passed with Node.
- Desktop browser render completed with no uncaught JavaScript errors.
- Light/dark toggle is included.
- All quick-access cards are clickable.
- Search routes to matching page identities.
- Image files and crop controls are documented.
- Tow and Wrecking Yard mod files were not edited or repackaged.

## Next step

David reviews the welcome-page screenshot/HTML first. After visual approval, JOB-10 can prepare the final presentation-only welcome-page files and coordinate route integration with JOB-01/JOB-00 and the owning site jobs. The separate Tow website preview remains a separate approval step before any Tow website integration.
