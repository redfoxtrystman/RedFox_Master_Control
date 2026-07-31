# JOB-09 v0.4.4.7 Focused Runtime Test Checklist

## Install

1. Back up the active Career save and `settings/redfox/`.
2. Disable v0.4.4.6 and every older JOB-09 ZIP.
3. Install only:
   `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_7_SpawnableItemGarageDeliveryPropFilesUntouchedRuntimeSlim.zip`
4. Fully restart BeamNG.
5. Confirm the Tow & Recovery app reports version `0.4.4.7`.

## Test A — FP Crane Chains exact record

1. Open the Tow Company Garage or Legacy Company Garage Recovery page containing `FP Crane Chains 2 rotatable chains`.
2. Choose the purchased RLS garage for the exact assigned tow yard.
3. Press **Link Yard & Deliver** or **Link Yard & Restore Item**.
4. Confirm JOB-09 attempts the native Career transaction instead of blocking the record as equipment.
5. Confirm the exact model/config remains:
   - model: `fp_crane_chains`
   - config: `rotatable_chains`
6. Confirm the item appears exactly once in the selected RLS garage.
7. Save and reload.
8. Confirm it remains exactly once.

## Test B — Duplicate and rollback protection

Repeat with one controlled failure such as a full destination garage or stale link.

Confirm:

- the virtual Tow Company Garage/legacy record remains;
- no second inventory item is created;
- no money is charged again;
- repeating the action resumes the same pending inventory ID when one exists;
- the UI reports the failure rather than deleting the record.

## Test C — Ordinary vehicle regression

1. Deliver one normal claimed road vehicle to a linked RLS garage.
2. Confirm it still creates exactly one owned inventory record.
3. Confirm virtual storage is removed only after placement verifies.
4. Save/reload and confirm no duplicate.

## Test D — Prop files untouched

No prop, equipment, vehicle, JBeam or controller file is included in v0.4.4.7. Confirm the crane chains and any walking-character/prop mods still spawn and behave exactly as they did before this JOB-09 update.

## Evidence on failure

Return:

- screenshot of the selected record and message;
- exact model/config shown;
- selected garage;
- whether an inventory ID was created;
- whether the virtual record remains;
- relevant `beamng.log` lines containing `[RedFox][TOW]`, `garage_delivery`, `legacy`, `ERROR`, or `stack traceback`.

## Deferred

Saved-job Resume after a game/computer crash remains deferred.
