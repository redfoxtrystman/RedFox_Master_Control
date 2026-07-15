# JOB-04 Scrap Yard / Wrecking Yard — WebUI Test Panel Build Note

**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** Scrap Yard / Wrecking Yard chat / Sol  
**Date:** 2026-07-15  
**Build artifact created in ChatGPT sandbox:** `zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0.zip`

## Purpose

Create a plain WebUI test panel for Scrap Yard backend testing before wiring the final website.

This follows David's Tow/Recovery approach: prove buttons and backend calls first, then hide the panel behind dev/cheat access or wire the same working calls into the polished site later.

## Baseline used

`zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works(1).zip`

## All-map rule

This build is intended to work on every map. It does not depend on `west_coast_usa` and does not use map-specific coordinates, parking spots, yard markers, or map-load generation.

## What was added

```text
lua/ge/extensions/redfox_scrapyard_webui_test.lua
ui/modModules/redfoxCareerWeb/sites/scrap_yard_webui_test/
sites/scrap_yard_webui_test/
```

The existing Scrap Yard page received a link to the test panel in both mirror paths:

```text
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html
sites/scrap_yard/index.html
```

## Test panel buttons

```text
Check Status
Write Test Log Lines
Load RLS Shop Data
Open Selected Purchase Menu
List Owned Career Vehicles
Sell Selected Owned Vehicle
Copy Short Test Report
```

## Stock functions targeted

```text
career_modules_vehicleShopping.updateVehicleList(true)
career_modules_vehicleShopping.getShoppingData()
career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)
career_modules_inventory.getVehicles()
career_modules_inventory.sellVehicleFromInventory(inventoryId)
career_modules_inventory.sellVehicle(inventoryId)
```

## Hard protections

```text
No redfoxScrapYardDirect
No startup career module
No modScript loader
No map-load parking/shop generation
No fake money
No fake storage insert
No fake garage insert
No fake inventory ownership
No runtime success claim until David tests in BeamNG
```

## Static checks completed

```text
ZIP integrity: PASS
Node syntax checks for touched JS: PASS
No __pycache__: PASS
No redfoxScrapYardDirect path: PASS
No modScript loader: PASS
Reports included: PASS
```

## Runtime status

Runtime is unproven until David tests in BeamNG.
