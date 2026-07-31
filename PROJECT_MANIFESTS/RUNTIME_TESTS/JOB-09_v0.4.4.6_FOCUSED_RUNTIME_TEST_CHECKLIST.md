# JOB-09 v0.4.4.6 Focused Runtime Test Checklist

## Exact build

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_6_DirectGarageLinkLegacyCompanyRecoveryEquipmentGuardRuntimeSlim.zip`

SHA-256: `f768fab30efdd663ba70f60d02c5b74c552c126afff333577ad6af1e35a166c5`

## Install

1. Back up the Career save and `settings/redfox/`.
2. Disable every older JOB-09 ZIP, including v0.4.4.5.
3. Install only the v0.4.4.6 ZIP.
4. Fully restart BeamNG.
5. Confirm the Tow & Recovery app reports version `0.4.4.6`.

## A — Purchased garage detection and linking

1. Open a selected **normal complete vehicle** in Tow Company Garage.
2. Confirm the record shows available purchased RLS garage choices directly on the page.
3. Select the intended garage.
4. Press **Link Yard & Deliver**.
5. Confirm the exact RedFox yard links to the selected purchased garage.
6. Confirm the vehicle appears exactly once in native Career/RLS inventory at that garage.
7. Save and reload; confirm it still exists once and the virtual company record is gone.

## B — Equipment record

Open `FP Crane Chains 2 rotatable chains` or another attachment record.

Expected result:

- stage reads **Company Equipment / Non-Titled Storage**;
- native garage delivery is blocked;
- the record remains available for sale, auction, scrap or later equipment handling;
- no Career vehicle is created.

This is intentional: loose chains/attachments are not titled vehicles and should not occupy a vehicle garage slot.

## C — Legacy RedFox Unit 8 recovery

1. Open Company Fleet / **Legacy Company Garage Recovery**.
2. Select `RedFox Unit 8 | RF-8`.
3. Confirm the old permanent safety-lock message is gone.
4. Select/link a purchased garage if the exact yard has no link.
5. Press **Restore** or **Link Yard & Restore Vehicle**.
6. Confirm one of these safe outcomes:
   - original Career inventory ID is adopted and moved; or
   - one replacement is created because the old removal was confirmed.
7. Confirm the virtual legacy record disappears only after exact garage placement verifies.
8. Save/reload and verify exactly one owned vehicle remains.

## D — Duplicate protection

Press restore/delivery only once. If interrupted or reloaded, use **Resume Safe Restore**.

Confirm:

- pending Career inventory ID is reused;
- no second vehicle is created;
- no second lien/title charge occurs;
- failed delivery leaves the virtual record intact;
- an identity mismatch shows manual review rather than moving the wrong vehicle.

## E — Existing systems regression

- Run one normal tow call for at least two minutes.
- Confirm whether call-time freeze/stutter remains absent.
- Complete one abandoned/lien intake.
- Confirm emergency vehicles are not selected for abandoned/private-lien work.
- Confirm Scene Manager still uses the guided workflow.

## Return on failure

Provide:

- screenshot of the full selected record and message;
- exact selected yard and garage;
- whether the garage is purchased and has space;
- inventory ID shown before/after;
- whether a virtual record remains;
- `beamng.log` lines containing `RedFox`, `LEGACY_COMPANY`, `garage_delivery`, `Garage Link`, `ERROR`, or `stack traceback`.

## Deferred

Saved-job Resume after a game/computer crash remains deferred.
