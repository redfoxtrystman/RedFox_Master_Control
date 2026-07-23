# JOB-05 — BeamBook realistic pricing and title-problem build v0.2.1

**Date:** 2026-07-22  
**Job:** JOB-05 — BeamBook Marketplace  
**Owner:** David / Captain  
**Status:** BUILT — RUNTIME UNTESTED

## Exact test artifact

```text
RedFox_BeamBook_Full_Wall_200_Realistic_v0_2_1_RUNTIME_UNTESTED.zip
```

- Size: 15,521,373 bytes
- SHA-256: `c1b40de04a1442f950b8fa71d2f20cc9a34d8ba2a02c909e2f1241d4ed2c7993`
- Archive entries: 81
- ZIP integrity: PASS
- Duplicate archive paths: 0
- JavaScript syntax: PASS
- Lua syntax through `texluac -p`: PASS
- JSON validation: PASS
- Missing referenced listing images: 0
- Direct archive-path overlap with current JOB-04 Scrap Yard test ZIP: 0
- BeamNG/RLS runtime: UNTESTED

## Owner-reported problem

David noticed that brand-new or expensive vehicles, including tow trucks and semis, could appear with no visible damage or paperwork issue for implausibly low prices such as approximately $1,200.

The requirement is that unusually cheap expensive equipment must have a believable disclosed reason. David also approved title problems because they create future gameplay around DMV replacement-title and registration paperwork.

## What changed

The v0.2.1 generator and the 200-item fallback catalog now use:

- higher baseline values for semis, heavy trucks, buses, tow trucks, wreckers, tankers and similar commercial equipment;
- age, mileage and condition depreciation;
- title-status multipliers;
- known-problem and damage multipliers;
- clean-title value floors;
- a rule that costly heavy equipment below $12,000 must disclose either a severe title problem or a severe mechanical/damage issue;
- estimated clean-market value;
- estimated discount;
- estimated repair cost;
- a visible reason for the discounted price.

## Title statuses added

Every fallback listing and newly generated live listing receives one of:

```text
Clean title
Rebuilt title
Salvage title
Bonded title
Missing title / bill of sale
Lien release required
Abandoned-vehicle paperwork
Parts only / no road title
```

Every title status includes a displayed paperwork action. Examples include replacement-title applications, bonded-title processing, lien releases, salvage/rebuild inspections and abandoned-vehicle ownership processing.

## Known-problem disclosures added

Listings may now disclose:

```text
No known major problems
Cosmetic damage or interior wear
Overdue maintenance
Mechanical fault
Major engine/transmission/hydraulic/electrical repair
Collision or frame damage
Flood/water damage
Fire/heat damage
Incomplete or parts-only vehicle
```

Heavy and tow-equipment listings use commercial-specific language for diesel, air-brake, hydraulic, PTO, boom, winch and electrical faults.

## User-interface changes

Marketplace cards now display:

- category;
- title status;
- problem severity when applicable;
- live-Career status when applicable.

The listing detail page now displays:

- asking price;
- estimated clean-market value;
- estimated discount;
- title status;
- DMV/paperwork action;
- known issues;
- estimated repair cost;
- road-registration warning;
- why the price is discounted.

A title-status Marketplace filter was added.

## Fallback catalog distribution

The catalog remains exactly 200 listings.

Title distribution in this exact build:

```text
Clean title: 114
Rebuilt title: 32
Salvage title: 16
Bonded title: 7
Missing title / bill of sale: 14
Lien release required: 8
Abandoned-vehicle paperwork: 5
Parts only / no road title: 4
```

Problem distribution:

```text
No known major problems: 24
Cosmetic: 42
Maintenance: 51
Mechanical: 47
Major: 23
Frame: 2
Flood: 4
Fire: 3
Parts/incomplete: 4
```

## Bargain-heavy audit

The exact static catalog was scanned for semis, T-Series trucks, tankers, buses, tow trucks, tow rigs, wreckers and other costly equipment below $12,000.

Result: **PASS — 0 unexplained cheap-costly-vehicle violations**.

The cheapest audited costly listing is now an example of the intended behavior:

```text
2008 Gavril T-Series Tanker Sport
Asking price: $1,500
Estimated clean-market value: $51,900
Title: Abandoned-vehicle paperwork
Known problem: Fire or heat damage reported
Estimated repair cost: $36,300
```

A cheap heavy vehicle can still appear, but the reason is no longer hidden.

## Important DMV limitation

Title and DMV requirements are currently BeamBook listing metadata and presentation only.

This build does **not yet**:

- force the player to visit a DMV page;
- charge title or registration fees;
- block vehicle use or registration;
- issue a replacement title;
- persist a registration hold after purchase;
- connect to a completed DMV/registration subsystem.

The metadata fields are intentionally prepared for future integration. Stock BeamNG/RLS remains the transaction authority.

## Scrap Yard boundary

This build contains:

- no Scrap Yard files;
- no startup Career module;
- no `modScript.lua`;
- no global `getShoppingData` replacement;
- no global `startInspection` replacement;
- no custom money, ownership, inventory, garage or storage implementation.

Static archive path overlap with the current JOB-04 Scrap Yard test ZIP is zero. Runtime coexistence remains untested and must not be claimed until David tests both exact builds.

## Required test

1. Disable v0.2.0 and all original/research BeamBook ZIPs.
2. Install only v0.2.1 for the first BeamBook test.
3. Add `RedFox BeamBook Full Wall` through UI Apps.
4. Verify the fallback Marketplace shows 200 listings.
5. Inspect low-price heavy/tow listings and confirm title/problems explain the discount.
6. Verify title filtering.
7. Load live Career listings.
8. Inspect a clean-title good-condition heavy vehicle and confirm it is not priced as junk.
9. Inspect a low-price heavy vehicle and confirm severe title or repair disclosure.
10. Test stock inspection and purchase.
11. Test BeamBook separately from Scrap Yard first, then test the two exact builds together.
12. Return `[RedFoxBeamBook]` log lines and screenshots of both normal-price and bargain-problem listings.
