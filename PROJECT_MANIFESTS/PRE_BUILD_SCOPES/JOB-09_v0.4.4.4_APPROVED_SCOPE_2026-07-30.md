# JOB-09 v0.4.4.4 Approved Pre-Build Scope

**Date/time approved:** 2026-07-30 21:02 PT  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Base artifact:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_3_ExactYardGarageLinkPerformanceRepair.zip`  
**Base SHA-256:** `61f870dbe354cda5ad6ff15b3f1a6a81c2376250108b4a7bc82d17c23fc9201e`

## Authorized repair scope

1. Replace lien claim's mandatory personal-garage path with an atomic same-yard custody-to-company/shop transition.
2. Keep personal Career/RLS garage transfer as a separate explicit action requiring a purchased garage.
3. Separate Random Events normal payment, random payer-default/lien, and non-lienable found-property closure.
4. Apply JOB-09-owned Random Events spawn context and reject unsuitable tunnel placements by default with limited retries.
5. Replace raw `train` substring classification with boundary-aware token matching so `drivetrain` is not Rail/Train.
6. Build the playable ZIP from an explicit runtime allowlist only.
7. Run focused static/mocked regression checks for paid tow, abandoned storage, lien claim/rollback, Random Events outcomes, multiple yards, save/reload duplication protection, and idle update behavior.

## Explicitly deferred

- Saved-job crash-resume reconstruction remains a documented known defect.
- No JOB-04, JOB-13, Browser Core, Random Events, stock BeamNG, Career/RLS, or other job-owned source will be edited.
- No broad redesign, new scene system, new website, or unrelated feature work.

## Required order of operations

1. Publish this pre-build scope.
2. Extract and hash the exact base artifact.
3. Preserve an untouched local baseline.
4. Modify only approved JOB-09-owned runtime files.
5. Record exact changed files and source hashes.
6. Verify syntax, package paths, mocked transactions, and regressions.
7. Package from a strict runtime allowlist.
8. Re-extract and verify every packaged file hash.
9. Publish build audit and exact artifact record.
10. Distribute as **STATIC/MOCK VERIFIED — BEAMNG RUNTIME TEST REQUIRED**.

No source changes existed before this scope record was committed.