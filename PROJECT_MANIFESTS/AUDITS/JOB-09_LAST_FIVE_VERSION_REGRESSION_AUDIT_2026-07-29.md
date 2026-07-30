# JOB-09 last-five-version regression audit — 2026-07-29

## Scope

Full source and ZIP comparison of:

- v0.4.0 — Linked Tow Website / Company Portal
- v0.4.1 — Random Events 1.9 live-scene bridge
- v0.4.2.1 — mission-generation emergency hotfix
- v0.4.3 — per-yard storage, shop transfer, lien claims, sales, auctions and scrap
- v0.4.4 — Random Events 2.1, vehicle/item catalog and external manager

Historical v0.3.x code and the broken v0.4.2 intermediate were also inspected where needed.

## Confirmed history

### v0.4.0 to v0.4.2.1

An unqualified `dispatchClassName(...)` call entered mission generation and caused the v0.4.2 runtime failure. v0.4.2.1 correctly restored `vehicleRules.dispatchClassName(...)`.

### v0.4.3

The yard/business expansion changed custody capacity, company and sales storage, RLS garage linking, safe same-inventory-ID transfers, lien claiming, direct sale, Copart-style auction and scrap systems. Mission-generation behavior from v0.4.2.1 remained intact.

### v0.4.4

The v0.4.3 custody, lien, shop, payment, sale and rollback functions were not rewritten. The regression entered before those functions: the new catalog inference treated both `heavy` and `construction` categories as `heavy_target`. This allowed detached crane pieces and similar equipment to become abandoned-vehicle targets even though the existing lien workflow requires a complete, titleable vehicle or trailer.

This same overly broad classification path explains the spreader-bar target and police-semi civilian-target findings.

## Critical unchanged v0.4.3/v0.4.4 paths

Function-body comparisons confirmed these remained unchanged in the repair scope:

- `shopTools.claimYardRecord`
- `businessTools.yardHasCustodySpace`
- `processDeliveredTarget`
- `updateActiveEvent`
- `finishUnpaidEvent`
- `acceptOffer`
- `createOffer`
- `M.randomEventsBridge.begin`
- `M.activeJobRecovery.save`
- `fleetTools.moveUnitToYard`

## Repair decision

The correct fix is not to rewrite lien or business transactions. It is to separate:

1. general tow-target eligibility;
2. abandoned/lien eligibility;
3. police/emergency/support eligibility;
4. equipment/found-property eligibility;
5. exact manually approved configuration overrides.

Construction items now require exact manual review. Detached equipment remains blocked from abandoned/lien use. A complete mobile crane may be approved explicitly as a heavy target.

## Verification

The resulting v0.4.4.1 source passed 59 static and mocked checks before packaging. The packaged ZIP was re-extracted and independently passed the same 59 checks. The 146 packaged files are an exact hash match to the verified source.

BeamNG, Career/RLS and Random Events runtime behavior remains unproven until David tests the exact ZIP.