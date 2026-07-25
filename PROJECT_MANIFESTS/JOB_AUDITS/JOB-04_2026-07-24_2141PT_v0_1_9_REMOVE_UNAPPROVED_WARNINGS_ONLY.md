# JOB-04 Audit — v0.1.9 Remove Unapproved Warning Text Only

**Date/time:** 2026-07-24 2141PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Package:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-24_2141PT_v0_1_9_REMOVE_UNAPPROVED_WARNINGS_ONLY_FROM_v0_1_8.zip`  
**Base:** `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-24_1910PT_v0_1_8_VISUAL_SWAP_SCRAP_PAGE_ONLY_FROM_JOB10_ON_v0_1_7.zip`

## Purpose

This patch exists only to correct the instruction violation where visible warning/cargo/split/combo text was added to the Scrap Yard page after David had rejected warning text.

## Files edited

Only these Scrap Yard page files were edited:

```text
sites/scrap_yard/index.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html
sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
```

## Visible text removed

Removed from the Scrap Yard page:

```text
Listings may include attached trailers or cargo; splitting is not supported yet.
Combo listing warning: some listings may include attached trailers or cargo...
Split-combo/trailer/cargo handling comes later in garage tools.
Combo Listings
Trailer/cargo splitting is not supported yet.
trailer splitting, cargo buyers
```

## Files intentionally not touched

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
Scrap Yard buy path
Scrap Yard sell path
PC access
lag/card rendering logic
timer system
regional ordering
scrapping/strip tools
```

## Static verification

```text
ZIP integrity: PASS
Output entry count: 927
No forbidden warning/cargo/split phrases in both Scrap Yard index.html copies: PASS
No combo-warning CSS selector left in both Scrap Yard CSS copies: PASS
ui/ui-vue/dist/index.js unchanged from v0.1.8 visual base: PASS
ui/ui-vue/dist/index.css unchanged from v0.1.8 visual base: PASS
JavaScript syntax checks: PASS
No redfoxScrapYardDirect startup module: PASS
```

## SHA256

```text
6aca6905fb6a7099d9445276c60378891d01fb266aeac533555e0ddd51306d8f
```

## Runtime status

Unproven until David tests this exact ZIP in BeamNG.

## Required rule reinforced

Do not add warning banners, warning cards, warning labels, or rejected explanatory UI text unless David explicitly asks for it. If David says remove something, remove it completely from visible build files.