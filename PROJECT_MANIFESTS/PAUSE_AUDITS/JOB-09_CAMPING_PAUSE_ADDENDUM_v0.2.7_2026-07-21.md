# JOB-09 — Camping Pause Addendum v0.2.7

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Status:** **PAUSED — NOT A HANDOFF**  
**Build status:** **BUILT — RUNTIME UNTESTED**

This addendum records work completed while David briefly returned from camping. Ownership remains with the same JOB-09 regular-chat workstation.

---

## Current test candidate

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_RLSProgressionPersonalClaims.zip
Size: 138,580 bytes
SHA-256: a34ed2660e6bf69ad86722c16114f3fe0989422dca4f65cfb3cd5f49a156fd73
```

Active workspace path:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_RLSProgressionPersonalClaims.zip
```

Source baseline:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_6_PoliceImpoundEmergencyScenes.zip
SHA-256: 82eecc0652d61cc8b6d203d0bf7eb541bdee95532e8c82c2b2ecd59c0a0b2dbd
```

The installable ZIP is available in the active ChatGPT JOB-09 workspace and is not committed to GitHub as a binary.

---

## Exact RLS reference inspected

David supplied:

```text
1(1).zip
Embedded title: RLS Career Overhaul v2.6.8
Embedded filename: rls_career_overhaul_2.6.8.zip
Size: 43,398,480 bytes
SHA-256: f6aceaf436af2abf36388b69f287e30a6eb59d3dc0d1089da3f4ac0771f1419b
```

It was inspected as an API/source reference only. No RLS source, UI, models, textures, configurations, or other assets were copied or bundled into JOB-09.

Confirmed RLS 2.6.8 interfaces and keys used by v0.2.7:

- Repo skill attribute: `careerSkills-repo`.
- Repo economy section: `repo`.
- RLS payment/reward pipeline.
- `career_modules_difficultyMode.scalePaymentRewardData`.
- `career_modules_inventory.addRepossession`.
- `career_modules_inventory.addVehicle`.
- `career_modules_inventory.hasFreeSlot`.
- `career_modules_inventory.moveVehicleToGarage`.
- `career_modules_inventory.updatePartConditions`.
- `career_modules_inventory.removeVehicleObject`.
- Civil Service skill: `careerSkills-civilService` when installed/available.

---

## Progression changes

Every successfully completed RedFox Tow call now queues progression through the detected Career/RLS systems.

Base progression can include:

- Beam XP.
- Labourer progression.
- Repo XP when `careerSkills-repo` is available.
- Civil Service XP for police, street-racing, and DUI impound work when `careerSkills-civilService` is available.
- Repossession statistics on the inventory tow vehicle used to accept the call.

Reward scaling now considers:

- Response distance.
- Loaded tow distance.
- Job workload/type.
- Number of recovered target vehicles.
- RLS Repo skill level bonus.
- RLS Repo economy multiplier where available.
- Difficulty-mode reward scaling where available.

Longer and more difficult work should therefore pay and progress more than a short basic tow. Exact balance remains runtime-testable and adjustable.

Unpaid and abandoned-hold outcomes can still award gameplay progression even when no immediate cash payment is issued.

---

## Personal vehicle claim from Tow Yard

Eligible Tow Yard records now expose:

```text
Claim as My Personal Vehicle
```

Required conditions:

1. The legal/storage hold must have expired (`eligibleAt`).
2. Career inventory APIs must be active.
3. A free private garage slot must exist.
4. The vehicle must be retrievable/spawnable on the current map.

Successful claim flow:

1. Retrieve/spawn the Tow Yard vehicle if needed.
2. Add it to Career inventory as an owned vehicle.
3. Preserve/capture available part-condition data.
4. Move it to the player's private garage.
5. Mark it as claimed from the RedFox Tow Yard.
6. Remove the live world object after storage.
7. Remove the Tow Yard record only after the Career inventory transfer succeeds.
8. Pay no sale proceeds; this is ownership transfer, not a sale.

Failure/rollback rules:

- No free garage slot: claim is refused and the Tow Yard record remains.
- Inventory/garage transfer failure: the new inventory record is rolled back where possible and the Tow Yard record remains.
- The original yard record is not deleted before successful transfer.

Exported JOB-09 API:

```text
claimYardVehicleToCareerInventory(recordId)
```

Important limitation: older Tow Yard records may not preserve exact physical deformation because the earlier yard system did not serialize every live node/beam deformation state.

---

## UI and history additions

The active call and history can now show:

- Workload units.
- RLS Repo bonus.
- Expected Beam XP.
- Expected Labourer progression.
- Expected Repo XP.
- Expected Civil Service XP where applicable.

Module status now reports whether Repo progression is available, the detected Repo skill level, and the number of currently claimable Tow Yard vehicles.

---

## Static verification completed

- ZIP integrity: PASS.
- Direct-root package layout: PASS.
- Duplicate ZIP entries: none.
- Packaged JSON parsing: PASS.
- Packaged Lua syntax/loadfile checks: PASS.
- Main Lua local-variable compile limit: PASS.
- Protected stock Career/RLS override-path scan: PASS.
- Native executable/library scan: PASS.
- Direct RLS source/asset inclusion scan: PASS.
- Version consistency: PASS.
- Packaged inventory checksum validation: PASS.
- Stubbed personal-claim success test: PASS.
- Stubbed pending progression/payment test: PASS.
- BeamNG/RLS runtime: **UNTESTED**.

---

## First return test

```text
1. Disable every older JOB-09 ZIP, including v0.2.6.
2. Enable only v0.2.7.
3. Use a disposable RLS Career save.
4. Confirm RLS Repo progression is detected.
5. Complete one short Standard Tow and record money/Beam XP/Labourer/Repo XP.
6. Complete a longer Standard Tow and confirm it awards more.
7. Complete Rolled, Semi Rollover, and Accident calls and compare workload rewards.
8. Complete Police and DUI impounds and check Civil Service progression.
9. Complete an abandoned/unpaid outcome and confirm progression despite deferred/no cash.
10. Check the Tow History progression fields.
11. After a Tow Yard hold expires, use Claim as My Personal Vehicle.
12. Confirm the vehicle leaves the Tow Yard and appears in My Vehicles/private garage.
13. Fill every garage slot and confirm a failed claim leaves the Tow Yard record untouched.
14. Save, reload, and confirm progression/history/claimed inventory persist.
```

Return the relevant `beamng.log` section for any payment, attribute, inventory, garage, condition-capture, history, or claim failure.

---

## Permanent warnings

- Do not claim v0.2.7 working until David tests this exact ZIP.
- Do not patch or redistribute RLS source.
- Do not delete a yard record before successful Career inventory transfer.
- Do not assume every older yard record can reconstruct exact deformation.
- Current storage hold timing still follows JOB-09's existing timer behavior; converting it to a verified RLS in-game-day clock remains separate work.
- This is a camping pause, not a handoff.
