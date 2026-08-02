# JOB-09 v0.4.5.1 Build Report

**Job:** JOB-09 — RedFox Tow / Recovery / Dispatch  
**Build:** v0.4.5.1  
**Date:** 2026-08-02 12:17 Pacific  
**Status:** Static validation passed; runtime unproven

## Runtime findings that caused this patch

David confirmed that the old partial Career vehicles could not be repaired and sold them from the disposable test save. The repair experiment is therefore not included in this build.

Testing v0.4.5.0 reached the **Continue Transfer** step but the action did not visibly complete. Inspection found three reliability problems:

1. The Tow Portal host still loaded `portal.html?v=0449`, allowing BeamNG's UI cache to keep serving older JavaScript even though the Lua module was v0.4.5.0.
2. A stale `claimPending` marker could leave a custody record permanently stuck even when no Career inventory vehicle or completed Tow Company record existed.
3. Several legitimate server-side rejection paths displayed an in-game warning but did not return a structured failure to the browser. The browser therefore remained on **Transferring…**.

## Changes

- Cache-busted the app, HTML, CSS, and JavaScript to `0451`.
- Added a dedicated transfer confirmation dialog with lien, capped storage, title fee, and total acquisition cost.
- Routed `claim_yard_vehicle`, `continue_transfer`, `confirm_claim_transfer`, and `claim_yard_vehicle_confirm` to the same idempotent Lua transaction.
- Added duplicate-click recovery: an already-completed custody transfer reports success instead of creating another record or charging again.
- Clears only a proven-stale `claimPending` marker. A marker tied to a real Career inventory ID remains blocked to prevent duplication.
- Every transfer rejection now returns a status and reason to the portal.
- Added an eight-second UI timeout so the Continue button cannot remain frozen indefinitely.
- Added `yardRecordId` to Tow Company Garage portal records so the browser can reconcile the exact source record.
- Added a full-screen **Tow Complete** summary after paid and unpaid tow closures. It shows payment, native BeamXP/labourer XP amounts, vehicle, payer, destination, response distance, tow distance, and quoted charge.
- Retained the native RLS repo-style target generation and purchase-finalization lifecycle from v0.4.5.0.
- After a claimed vehicle is successfully delivered into a linked owned RLS garage and save-verified, JOB-09 opens the native RLS insurance chooser for that exact inventory ID.

## Important behavior boundaries

- Custody → Tow Company Garage creates a virtual company asset. It does not create a player-owned Career vehicle yet, so insurance cannot be selected at this stage.
- Tow Company Garage → linked owned RLS garage creates the native Career vehicle. The insurance chooser opens after this second transaction succeeds.
- The Tow Complete summary is presentation-only. Payment and XP continue through the native RLS payment queue.
- No old-car repair control is included.

## Static validation

- 16 runtime files
- ZIP test passed
- JavaScript syntax passed with Node
- Lua parsed successfully with LuaTeX
- All JSON parsed successfully
- No duplicate HTML IDs
- No stale `0.4.5.0`, `?v=0449`, or `?v=0450` tokens
- No stock BeamNG or RLS Career files are overridden by JOB-09

## Archive

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_5_1_ContinueTransferRecoveryTowSummaryNativeInsuranceRuntimeSlim.zip`  
SHA-256: `1fdd8076bbcd8901c8fe6d50a93b71e6399a416f41e9444b3936a11c7c0ffdd3`

This build must remain marked runtime-unproven until the focused West Coast USA tests pass.
