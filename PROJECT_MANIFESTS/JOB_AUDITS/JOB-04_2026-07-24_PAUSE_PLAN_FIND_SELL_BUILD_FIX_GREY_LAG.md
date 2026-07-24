# JOB-04 Pause Plan — Find Sell-Capable Build, Fix Grey Screen and Lag

**Date:** 2026-07-24
**Job:** JOB-04 — Scrap Yard / Wrecking Yard
**Status:** Paused until David returns from doctor appointment
**This is not a handoff.**

## Current user report

David checked back through many versions and still found grey-screen behavior across many of them.

Important correction from David:

- Some builds were marked or remembered as working, but may already have had the grey screen before it was noticed.
- Tomorrow, after the doctor appointment, the plan is to work with one of the grey-screen builds if needed.
- The priority is to find a build that can actually sell cars, then fix lag and grey-screen behavior from there.

## Current truth / do not overclaim

No current build should be called final, working, fixed, or safe without fresh testing in BeamNG.

Known partial facts from recent tests:

- One recent line opened Scrap Yard and allowed David to buy a Mustang.
- Seller patience did not change during haggling, which may mean the listing is not using the full expected RLS negotiation/session behavior or may be an RLS/base-game behavior issue.
- v0.1.5 PC/phone parity build broke phone and PC access and must not be used as a base.
- v0.10.3.1 phone-only candidate contains the bad `ui/ui-vue/dist/index.js` family and is rejected as a safe baseline despite its filename saying phone works.
- Multiple older builds appear to have grey-screen risk.

## Next work plan

1. Stop building new guesses tonight.
2. Use inspect-only mode first tomorrow.
3. Inventory every likely candidate ZIP and record:
   - file name
   - whether it has `ui/ui-vue/dist/index.js`
   - hash of that file if present
   - phone access files present/missing
   - Scrap Yard page files present/missing
   - sell-related strings/functions present/missing
   - buy-related strings/functions present/missing
   - startup career modules present/missing
   - banned `redfoxScrapYardDirect` present/missing
4. Find the best candidate that can actually sell cars, or at least contains the sell path closest to RLS stock inventory sell functions.
5. Do not touch PC access. Phone-only direction remains active unless David changes it.
6. Fix grey screen by removing or replacing only the bad main game UI override after confirming what depends on it.
7. Fix lag by changing page behavior after the phone path is confirmed:
   - no heavy auto refresh on page open
   - page draws immediately
   - RLS/shop data loads only on click
   - session cache after successful load
   - visible loading state instead of blank white/grey
   - timing logs
8. Package only after checks pass and include readable TXT/HTML verification reports.

## Hard constraints

Do not use these as active runtime approaches:

- startup Scrap Yard career modules
- `redfoxScrapYardDirect`
- map-load parking/shop generators
- custom money removal
- custom inventory insertion/removal
- custom purchase/sell replacement logic

Use stock/RLS paths where possible:

- `career_modules_vehicleShopping.updateVehicleList(true)`
- `career_modules_vehicleShopping.getShoppingData()`
- `career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)`
- `career_modules_inventory.sellVehicleFromInventory(inventoryId)`
- fallback `career_modules_inventory.sellVehicle(inventoryId)`

## Immediate next checkpoint

When David returns after the doctor appointment, begin with candidate ZIP inspection and a build matrix. Do not create a new ZIP until the most promising sell-capable baseline is identified and David confirms the patch direction.
