# JOB-04 runtime findings — pricing/UI mismatch and duplicate taxi records

**Owner:** David / Captain  
**Date:** 2026-08-03  
**Tested build:** JOB-04 v0.3.2.4.3  
**Status:** PARTIAL RUNTIME PASS — sale/scrap controls visible, pricing/design not accepted

## Confirmed working

- Owned Career/RLS vehicles load in the Wrecking Yard page.
- Sell Vehicle and Scrap Whole Vehicle controls are visible.
- Native sale confirmation opens.
- Whole-scrap quote confirmation opens.
- The page shows exact Career inventory IDs.

## Pricing defect

The current page exposes two unrelated actions:

1. `Sell Vehicle` calls the normal Career/RLS native sale.
2. `Scrap Whole Vehicle` removes the vehicle and pays a custom Wrecking Yard amount.

The displayed `Estimated native value` is not a reliable final RLS payout because JOB-04 currently prioritizes raw UI fields before `career_modules_valueCalculator.getInventoryVehicleSellValue`. RLS applies its global vehicle-sell market multiplier later. David's runtime notification showed:

```text
Balanced: Sold a vehicle: Ibishu Covet
money: 4330 -> 8661 (x2.0)
```

The whole-scrap quote for the same general value range showed approximately:

```text
Estimated vehicle value: $4,181
Scrap payout: $1,076
```

This matches JOB-04's current base `wholeCarMultiplier = 0.22`, adjusted by region/daily multiplier. That formula is not an accepted final Wrecking Yard economy.

## Owner-required replacement design

The Wrecking Yard must no longer present the normal native marketplace sale as its primary sale option. Required actions:

1. **Sell Complete Vehicle to Yard — instant**
   - complete vehicle and all installed parts go to the yard;
   - payout slightly below the current actual RLS sale reference;
   - instant payment, unlike waiting for a marketplace buyer.

2. **Auto-strip Good Parts + Scrap Remainder**
   - good parts return to the existing RLS parts inventory;
   - parts whose name contains `junk` stay with the chassis and contribute value;
   - one combined labor charge covers removal/handling;
   - cash payout is for chassis/frame plus junk parts after labor.

3. **Scrap Current Remainder / Frame**
   - used after the player manually strips parts in the garage;
   - pays for the remaining chassis/frame and remaining junk parts;
   - optional later action to sell parts in parts inventory whose name contains `junk`.

## Required UI correction

- `Buy From Yard` must be the default page.
- Top-right should show today's scrap rate and a `Sell / Scrap My Vehicles` button.
- That button opens the player's garages/owned vehicles and the three Wrecking Yard actions.
- Receipts must show the actual reference value, discounts/fees, payout, returned parts and destination account.

## Duplicate taxi observation

The Wrecking Yard screenshot shows two Burnside Special taxi records with different Career inventory IDs, mileages and storage locations:

- inventory ID 40 — 228,742 miles — RV There Yet;
- inventory ID 45 — 185,594 miles — Fire Station Shop.

Therefore the Wrecking Yard UI is displaying two distinct Career inventory records, not rendering one card twice. The source of the second taxi is not yet known. Do not delete or merge either record until purchase/auction provenance is traced.

## Classification

- Visibility/UI route: PASS
- Native sale action: mechanically invoked, but wrong product design for Wrecking Yard
- Custom scrap action: mechanically quoted, pricing rejected
- Auto-strip/parts return: NOT IMPLEMENTED
- Duplicate taxi cause: UNRESOLVED
