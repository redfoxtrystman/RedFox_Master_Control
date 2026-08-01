# JOB-09 v0.4.4.9 Focused Runtime Test Checklist

**Build:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_9_FullNativeLifecycleStoredVehicleRepairRuntimeSlim.zip`  
**Status before testing:** BUILT — STATIC PASS — RUNTIME UNPROVEN  
**Target save:** Captain David's disposable Profile 3 test save  
**First repair target expected:** Career inventory ID **11**, the incomplete blue Dodge Charger Daytona

## Before launching BeamNG

1. Close BeamNG completely.
2. Keep the uploaded `saves.zip` unchanged as the evidence backup.
3. Make one additional copy of the current Profile 3 save folder.
4. Remove or disable JOB-09 v0.4.4.8.
5. Install only JOB-09 v0.4.4.9. Do not run v0.4.4.8 and v0.4.4.9 together.
6. Keep the Charger vehicle mod enabled.
7. Do not use the developer “add current vehicle to garage” action during this test.

## Test A — repair the existing broken Daytona in place

1. Load Profile 3 on West Coast USA.
2. Open the RedFox Tow Web Portal.
3. Open **Inventory**.
4. Confirm the native lifecycle panel reports at least one incomplete stored RedFox vehicle.
5. Press **Audit & Repair Next Stored Vehicle** exactly once.
6. Do not press the button again, change maps, sell the vehicle, remove parts, or close BeamNG while the status says busy.
7. Expected first target: inventory ID **11**.
8. Allow up to two minutes. The process intentionally waits for native part inventory, insurance, thumbnail, garage assignment, physical storage, and two saves.
9. Record the final portal status and any on-screen warning.

### Immediate pass checks

- The process says repair complete for inventory ID 11.
- No new duplicate Daytona appears.
- The existing inventory ID remains 11.
- A thumbnail now exists. It should be generated from the actual spawned blue car, not merely the red default configuration preview.
- The Insurance page shows the Daytona as a registered **uninsured** vehicle instead of ignoring it.
- The vehicle remains assigned to Commercial Garage.
- Opening the parts/configuration screen no longer produces the prior missing-record behavior.

## Test B — save/reload persistence

1. Exit to the main menu normally.
2. Reload Profile 3.
3. Confirm inventory ID 11 is still present once.
4. Confirm its thumbnail remains.
5. Confirm Insurance still counts it as uninsured.
6. Spawn/call the vehicle from the garage.
7. Open the parts screen, but initially remove only a small non-structural part.
8. Save and reload again.
9. Only after that passes, test removing/reinstalling a major part such as the front subframe.

### Persistence pass checks

- No infinite loading screen.
- No Lua error from normal parts changes.
- No duplicate inventory ID or duplicate Daytona.
- No disappearance after reload.
- The vehicle's blue paint and saved damage/removed-part state are preserved as far as the surviving save data permits.

## Test C — repair the next partial RedFox vehicle

After ID 11 passes, run **Audit & Repair Next Stored Vehicle** one more time. The next expected target from the supplied save is inventory ID **33**. Repeat the save/reload checks.

## Test D — fresh lien transfer

1. Complete one new lien-capable abandoned or unpaid tow.
2. At drop-off, confirm JOB-09 displays that it is recording the full vehicle before finalizing the invoice/custody record.
3. Claim the vehicle into the Tow Company Garage.
4. Deliver it to the linked Career/RLS garage.
5. Wait for the full native lifecycle completion message.
6. Verify the new vehicle has:
   - one inventory ID;
   - canonical `partConfigFilename`;
   - original-parts and changed-slots tracking;
   - an uninsured insurance entry;
   - a generated thumbnail;
   - the selected garage assignment;
   - persistence after save/reload.

## Failure handling

- If repair fails, stop and preserve `beamng.log` immediately.
- Do not press repair repeatedly.
- The patch is designed to keep the same inventory record and avoid creating a duplicate after a repair failure.
- The broken vehicle may still be sold afterward on this disposable save, but preserve the log first.
- Damage, paint, mileage, or missing parts that were never captured by older JOB-09 versions cannot be reconstructed perfectly.

## Report back

Provide:

- which test and inventory ID;
- final portal lifecycle message;
- whether Insurance counts it;
- whether the thumbnail is blue/current or a red default preview;
- whether parts editing works;
- whether it survives reload;
- the newest `beamng.log` after any failure.
