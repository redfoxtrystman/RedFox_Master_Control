# JOB-09 — Career-Day Clock and Organized Asset Manager v0.2.8

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**

## Exact package

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_8_CareerDayAssetManager.zip
Size: 154,970 bytes
SHA-256: b7ad5424f82f70cec998e1ee01345c8f608b01d60aac6a6f927f06e75019a018
```

Source baseline:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_RLSProgressionPersonalClaims.zip
SHA-256: a34ed2660e6bf69ad86722c16114f3fe0989422dca4f65cfb3cd5f49a156fd73
```

The installable ZIP remains in the active ChatGPT JOB-09 workspace and is not committed as a GitHub binary.

## Runtime finding that caused this build

David's screenshots showed:

- stored vehicles remaining at `0 day(s) / $0`;
- map lighting/time-of-day apparently frozen;
- personal claim controls not visible because the real-calendar hold had not expired;
- Fleet, Tow Yard, and History records expanding into one very long scrolling page;
- adjacent record buttons/text making it difficult to tell which value belonged to which vehicle.

The root clock cause was confirmed in v0.2.7 source: storage used `os.time()` and divided by 86,400 seconds. It therefore represented real calendar days, not Career/game days.

## v0.2.8 changes

### Hybrid Career-day clock

- Adds a saved per-Career clock.
- Follows actual map time-of-day progress when it advances.
- Reads the map-reported day length when available.
- When time-of-day is frozen, active unpaused Career simulation time advances an equivalent Career day.
- Default fallback: 30 active minutes per Career day.
- Fallback can be adjusted from 5 to 120 active minutes.
- Paused time does not advance the fallback clock.
- Legacy v0.2.7 records are migrated without deletion.
- One-time migration preserves already elapsed legacy time, capped by the record's hold length.

### Storage and claim display

The selected stored vehicle now shows:

- fractional hold progress;
- required hold days;
- remaining Career days;
- completed billable storage days;
- storage charge;
- tow charge;
- current lien;
- clear personal-claim locked or eligible state.

Storage billing advances by completed Career days, not real calendar days.

### Organized main interface

The main window now has four separate pages:

1. Dispatch
2. Fleet
3. Storage / Impound
4. History

Only the selected page is expanded.

### Fleet organization

- Filter by assigned map/location.
- Select one vehicle from a dropdown.
- Show only the selected Fleet Book record.
- Assign the selected record to the current map.
- Adds `Delivery / Box Truck` and `Transport Tractor / Carrier` roles.

This remains the identity book. It is not yet the rollback-safe company vehicle inventory.

### Storage / impound organization

- Filter by map.
- Filter by All, Hold, Eligible, or Normal storage.
- Select one stored vehicle from a dropdown.
- Keep all value, lien, retrieval, pricing, and claim controls attached to that selected record.

### History organization

- History catalog dropdown.
- Individual record dropdown.
- Only the selected record's complete details are expanded.

### Valuation clarity

- Prefers `marketValue`, then `configBaseValue`, then legacy configuration `Value` metadata.
- Displays the valuation source on the selected record.
- Adds **Recalculate Selected Vehicle Appraisal** using the exact installed model/configuration when it can be found.
- Legacy stored values are not silently rewritten.

### Future Phone/PC manager preparation

Adds read-only API:

```text
getAssetManagerData()
```

It returns the saved clock, Fleet Book, stored vehicles, history, and yard locations for a future shared Phone/PC company asset page.

## Deliberately not included

- Tow Yard → Tow Company Fleet ownership transfer.
- Personal ↔ business vehicle transfer.
- Company bank routing.
- Business branch relocation.
- Fleet insurance enrollment.
- Company sale protection.
- Full Phone/PC asset-manager page.

Those operations can delete or duplicate valuable vehicles if rushed. They remain blocked until tested with a disposable vehicle and explicit rollback.

## Static verification

- ZIP integrity: PASS.
- Direct-root layout: PASS.
- Duplicate ZIP entries: none.
- Lua `loadfile`: PASS.
- Main-chunk local-variable compile limit: PASS.
- Top-level stub execution: PASS.
- Frozen-time one-day clock test: PASS.
- Legacy real-time record migration test: PASS.
- Packaged JSON parsing: PASS.
- Inventory checksum validation: PASS.
- Protected Career/RLS override-path scan: PASS.
- Native executable/library scan: PASS.
- RLS source/assets bundled: NO.
- BeamNG/RLS runtime: **UNTESTED**.

## Required runtime test

1. Disable every older JOB-09 ZIP, including v0.2.7.
2. Enable only v0.2.8 on a disposable RLS Career save.
3. Confirm old yard, fleet, and history records load.
4. Leave map time frozen and confirm Hold Progress advances while actively driving.
5. Lower fallback to five minutes for a quick day/billing test.
6. Confirm one completed Career day adds one storage day and one storage charge.
7. Confirm three Career days unlock personal claim.
8. Unfreeze time and confirm the clock reports time-of-day-cycle operation without obvious double counting.
9. Verify Fleet location/unit dropdowns.
10. Verify Storage map/category/vehicle dropdowns.
11. Verify History catalog/record dropdowns.
12. Reappraise only a disposable stored record.
13. Test personal claim with and without garage capacity.
14. Save/reload and verify clock, storage, fleet assignment, and history persist.
15. Return `beamng.log` around any clock, UI, appraisal, claim, payment, or persistence error.

## Safety warning

Do not transfer or experiment with the valuable abandoned truck as a company asset yet. v0.2.8 does not include business ownership transfer.