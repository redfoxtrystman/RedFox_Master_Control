# JOB-09 v0.4.4.5 Focused Runtime Test Checklist

## Install

1. Back up the active Career save and `settings/redfox/`.
2. Disable every older JOB-09 ZIP, including v0.4.4.4.
3. Install only `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_5_GuidedSceneManagerLinkedRLSGarageDeliveryRuntimeSlim.zip`.
4. Fully restart BeamNG.
5. Confirm the Tow & Recovery app reports version `0.4.4.5`.

## A — Existing systems first

- Run one ordinary Standard Car Tow.
- Stay on the active call for at least two minutes.
- Confirm whether the prior repeating call-time freeze/stutter is gone.
- Complete the call and verify payment/history.
- Check for repeated console spam.

## B — Guided Scene Manager

1. Open **Scene Manager** and confirm five understandable steps are visible.
2. Load or accept a call scene.
3. Turn editing on.
4. Select an object.
5. Test **Keep in Saved Scene** and **Do Not Save This Object**.
6. Confirm those choices affect a future reusable template, not acceptance of the live job.
7. Accept the live scene for the current job.
8. Save the adjusted layout as a reusable scene.
9. Replay the saved scene.
10. Open **Advanced Scene Tools** and confirm technical controls stay hidden until requested.
11. Confirm the active tow target cannot be deleted.

## C — Custody to Tow Company Garage

1. Use an eligible abandoned/lien vehicle at a known exact tow yard.
2. Record money before claiming.
3. Select **Claim into Tow Company Garage**.
4. Confirm the lien/title/storage charge happens once.
5. Confirm the custody record disappears only after the company record saves.
6. Confirm the vehicle appears exactly once in that yard's Tow Company Garage.
7. Save/reload and confirm it remains exactly once.

## D — Tow Company Garage to linked RLS garage

1. Link the exact tow yard to a purchased RLS/Career garage with available capacity.
2. Select the claimed company vehicle.
3. Choose **Deliver to Linked RLS Garage**.
4. Confirm exactly one owned Career/RLS inventory vehicle is created.
5. Confirm it is placed in the linked garage.
6. Confirm the virtual Tow Company Garage record disappears only after placement verification.
7. Confirm no second charge occurs.
8. Save/reload and verify one owned vehicle exists with no duplicate company record.

## E — Failure protection

Repeat delivery with one controlled failure: full destination garage, stale/missing garage link, or wrong map/yard.

Confirm:

- no duplicate Career vehicle;
- no money loss;
- vehicle remains safely in Tow Company Garage;
- UI gives a clear reason;
- repeating the action does not create another inventory vehicle.

## Evidence on failure

Return a screenshot, action pressed, exact source yard and linked garage, money before/after, custody/company/Career inventory state, and relevant `beamng.log` lines containing `[RedFox][TOW]`, `garage_delivery`, `shop_transfer`, `claim`, `ERROR`, or `stack traceback`.

## Deferred

Saved-job Resume after a game/computer crash remains deferred and is not expected to be repaired by v0.4.4.5.