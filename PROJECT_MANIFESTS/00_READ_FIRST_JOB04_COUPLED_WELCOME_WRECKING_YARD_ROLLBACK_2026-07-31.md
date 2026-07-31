# OWNER / COORDINATOR DIRECTIVE — JOB-04 COUPLED WELCOME + WRECKING YARD ROLLBACK

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Affected job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** OWNER-APPROVED ROLLBACK — EFFECTIVE IMMEDIATELY

## Decision

The attempted split between the FoxNet welcome/browser package and the JOB-04 Wrecking Yard feature package broke runtime behavior.

The active direction is now:

```text
KEEP THE FOXNET WELCOME/BROWSER SHELL AND WRECKING YARD TOGETHER
IN ONE TRIMMED JOB-04 PACKAGE.
```

This rolls back the package split, but it does **not** roll back the cleanup of unrelated content.

## Required source

Use the last combined JOB-04 source that preserved the working welcome/browser + Wrecking Yard relationship:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1430PT_v0_3_4_NATIVE_PURCHASE_FORCED_GARAGE_DELIVERY_FROM_v0_3_3.zip
SHA-256: e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75
```

The next build must be derived from this combined source or another exact combined source proven equivalent. Do not derive it from the broken separated pair unless the combined runtime relationship is fully restored.

## What stays in the active JOB-04 package

Only the files actually required for:

- FoxNet welcome/browser page needed to reach Wrecking Yard;
- phone tile/icon and required route/layout integration;
- Wrecking Yard webpage, CSS, JavaScript and assets;
- native purchase and forced garage-delivery behavior already owned by JOB-04;
- owned-vehicle selling;
- whole-vehicle scrap;
- strip-and-scrap;
- returned parts and catalytic-converter behavior;
- JOB-04-specific settings, persistence, logs and verification records;
- shared files that are technically inseparable from the currently working JOB-04 runtime path.

## What must remain removed

Do not restore unrelated content removed during the v0.3.5 cleanup:

- JOB-09 Tow / Recovery / Dispatch pages or code;
- JOB-13 Online Auction pages or code;
- JOB-05 BeamBook pages or code;
- Insurance, Import/Export, Collector, Underground, Parts Exchange or other unrelated sites;
- root mirrors, obsolete copies and duplicate historical versions;
- MHTML captures and development-only records in active runtime paths;
- records-only archive content;
- another job's settings, persistence or backend logic.

The archive:

```text
RedFox_JOB-04_v0_3_4_REMOVED_EXTRAS_RECORDS_ONLY_2026-07-30.zip
```

remains records-only and must never be installed.

## Browser Core split status

The following pair is rejected as the active runtime architecture because separating them broke the system:

```text
RedFox_FoxNet_Browser_Core_v0_1_0_COMPAT_TEST_FROM_JOB04_v0_3_4.zip
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1902PT_v0_3_5_SLIM_MODULE_REQUIRES_BROWSER_CORE_FROM_v0_3_4.zip
```

Status:

```text
FAILED RUNTIME ARCHITECTURE — DO NOT CONTINUE AS ACTIVE BASELINE
```

Preserve them only for debugging/history.

## Cross-job architecture after rollback

For now:

- JOB-04 owns one coupled welcome/browser + Wrecking Yard package because that relationship is currently inseparable in the working implementation.
- JOB-09 remains a separate Tow / Recovery / Dispatch mod.
- JOB-13 remains a separate Online Auctions mod.
- JOB-05 remains a separate BeamBook mod.
- Do not copy JOB-09, JOB-13 or JOB-05 code into JOB-04 merely to make their pages visible.
- A future truly generic shared browser may be reconsidered only after a minimal proof does not break JOB-04. It is not the current task.

## Next build rule

The next JOB-04 build must be a **trimmed combined rollback**, not a new architecture experiment.

Required process:

1. Start from the exact combined v0.3.4 source.
2. Keep the welcome/browser and Wrecking Yard integration untouched as much as possible.
3. Remove only files proven unrelated or redundant.
4. Change one narrow group at a time.
5. Produce an exact kept/removed path report.
6. Verify no JOB-09, JOB-13, JOB-05 or other unrelated feature code remains.
7. Test Career load and phone/browser opening before testing Wrecking Yard.
8. Test one inexpensive purchase before selling, scrapping or stripping.
9. Roll back immediately if the welcome page or Wrecking Yard route disappears.

## Acceptance gate

The combined trimmed package is not approved until David confirms the exact ZIP:

- Career loads;
- phone opens;
- FoxNet welcome page opens;
- Wrecking Yard opens;
- listings load acceptably;
- one inexpensive purchase completes through real Career/RLS behavior;
- purchased vehicle reaches the correct garage/inventory;
- unrelated pages are absent;
- JOB-09 and JOB-13 can still be enabled separately without breaking Career.

## Superseded direction

This directive supersedes the immediate active instruction to make Browser Core and JOB-04 separate installable packages.

The long-term modular concept is deferred, not declared impossible. Current priority is restoring and trimming the combined working JOB-04 package without unrelated baggage.
