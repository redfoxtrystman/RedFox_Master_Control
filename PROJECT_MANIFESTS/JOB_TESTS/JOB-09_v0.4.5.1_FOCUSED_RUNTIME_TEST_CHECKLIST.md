# JOB-09 v0.4.5.1 Focused Runtime Test Checklist

## Setup

1. Close BeamNG completely.
2. Disable/remove v0.4.4.9 and v0.4.5.0.
3. Install only `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_1_ContinueTransferRecoveryTowSummaryNativeInsuranceRuntimeSlim.zip`.
4. Use West Coast USA and the disposable test save.
5. Confirm the Tow Portal reports v0.4.5.1.

## A. Existing eligible custody record — Continue Transfer

1. Open Tow Portal → Inventory.
2. Select one vehicle whose legal hold is finished.
3. Press **Claim into Tow Company Garage**.
4. Confirm the new cost dialog shows Tow lien, capped storage, title transfer, and total.
5. Press **Continue Transfer** once.

### Pass

- The button changes to Transferring and resolves within eight seconds.
- The custody record disappears.
- Exactly one matching record appears in Tow Company Garage inventory.
- The Career account is charged exactly once.
- No Career/RLS inventory vehicle is created yet.
- Repeating the action after a delayed refresh reports already completed and does not duplicate or recharge.

### Fail

- The button remains permanently frozen.
- No exact error is shown.
- Duplicate company records appear.
- Money is charged more than once.
- The custody record disappears without a Tow Company record.

## B. Linked RLS garage delivery

1. Link the tow yard to an owned RLS garage with space.
2. On the new Tow Company record, choose Deliver to Linked RLS Garage.
3. Do not change maps or repeat the action while the native lifecycle is running.

### Pass

- Exactly one native Career inventory ID is created.
- Model, configuration, paint, condition, mileage, and plate match the stored record where captured.
- Original parts and changed slots are initialized.
- The vehicle appears in the exact linked garage.
- The Tow Company source record is removed only after save verification.
- The native RLS insurance chooser opens for the new inventory ID.
- Selecting No insurance makes it appear in the Uninsured section, or choosing a policy assigns that policy.
- Save/reload preserves the vehicle.
- A small part can be removed/reinstalled; then test one major part.

## C. Post-tow completion summary

1. Complete one new paid tow.
2. Confirm a full-screen **Tow Complete** summary opens.
3. Verify payment, BeamXP, labourer XP, vehicle, payer, destination, response distance, tow distance, and quoted charge.
4. Press Continue and confirm the reward remains applied.
5. Complete an unpaid/impound closure and verify the summary reports no immediate payment without inventing XP.

## Failure evidence

At the first failure, stop testing and preserve:

- newest `beamng.log` from the user-folder root;
- screenshot of the transfer dialog or exact warning;
- custody record ID, Tow Company shop ID, or Career inventory ID shown;
- whether money changed and by how much.
