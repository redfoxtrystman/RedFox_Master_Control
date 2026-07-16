# JOB-09 — Cataloged Tow History v0.2.4 Handoff

**Date:** 2026-07-15  
**Owner:** JOB-09 regular-chat workstation  
**Status:** **BUILT — RUNTIME UNTESTED**

## Candidate

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_4_CatalogedHistory.zip`

- Size: 76,643 bytes
- SHA-256: `072c882da5f29ae4bf5be816c6ffbe518dee50d2c64674df084042d0bf0d8405`
- Source baseline: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_3_RoadsideMixedScenes.zip`
- ZIP integrity: PASS
- Lua syntax: PASS via `texlua loadfile`
- JSON parse: PASS
- Protected Career-path scan: PASS
- BeamNG runtime: UNTESTED

## Owner-requested change

David requested that Tow History stop appearing as one long flat list and instead be cataloged by the kind of work performed.

## Catalogs

- All Records
- Abandoned Vehicles
- Accident Scenes
- Rollovers / Recovery
- Standard Tows
- Impound / Unpaid
- Paid / Released
- Cancelled

Call-type catalogs and outcome catalogs intentionally overlap. For example:

- an abandoned vehicle stored on lien appears under **Abandoned Vehicles** and **Impound / Unpaid**;
- a paid accident cleanup appears under **Accident Scenes** and **Paid / Released**.

## Save compatibility

- Existing v0.2.3 and older history records are not deleted or rewritten.
- Existing records are categorized dynamically from their saved event type, payment status, outcome, and yard-record details.
- New records also persist `catalogPrimary`.
- History remains newest-first and retains up to 500 entries per Career profile.
- The UI displays the newest 20 records matching the selected catalog.

## Entry detail improvements

Each displayed record now includes:

- primary catalog and outcome;
- every recorded vehicle name, not only the first vehicle;
- quoted and paid totals;
- payer and map;
- outbound and tow distance;
- destination and scene source.

## Regression boundary

No intentional changes were made to:

- mission generation or completion;
- road/roadside crash-scene placement;
- vehicle selection or damage;
- payments and rewards;
- abandoned or impound disposition;
- tow-yard persistence;
- routing and destination providers;
- random-event scene-provider integration.

## Required first test

1. Disable older JOB-09 ZIPs and enable only v0.2.4.
2. Open the same Career profile shown in David's screenshots.
3. Confirm the abandoned Barstow record appears under **Abandoned Vehicles** and **Impound / Unpaid**.
4. Confirm the three-vehicle Accident Scene Cleanup appears under **Accident Scenes** and **Paid / Released**.
5. Confirm no record is duplicated inside one catalog.
6. Complete one new tow and verify its call category and outcome category.
7. Return screenshots and `beamng.log` if any history button or entry errors.
