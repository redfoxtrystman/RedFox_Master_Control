# INCIDENT REPORT — JOB-09 Order-of-Operations Violation During v0.5.0.40b / v0.5.0.40c

**Date:** 2026-09-06  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Owner:** David / Captain  
**Severity:** HIGH — process violation with runtime/user-test impact  
**Status:** OPEN — corrective controls required

## Executive summary

During emergency work intended to restore the normal commercial Career garage and Tow UI behavior, the assistant violated the established RedFox order of operations that was already documented on GitHub and had previously been reinforced by multiple incident reports.

The failure was not caused by an unknown rule. The required workflow already existed and explicitly required source-first inspection, baseline comparison, narrow edits, post-edit comparison, packaged-ZIP reopening/verification, truthful static-vs-runtime labeling, and GitHub checkpointing before user-facing delivery.

Instead, the assistant rushed v0.5.0.40b and then v0.5.0.40c to the owner while the surrounding Tow/RLS/garage state was still not sufficiently verified. v0.5.0.40b replaced a full Tow/RLS business compatibility module with an undersized shim, which removed interfaces expected by the rest of JOB-09 and caused the Tow UI to stop opening. v0.5.0.40c was then produced as an immediate corrective package before the full approved evidence-first recovery sequence had been re-run from the last known-good baseline.

This incident records that the assistant failed to follow the owner's established process and required the owner to stop development and explicitly demand a GitHub order-of-operations review.

## Established order of operations that was already in force

The relevant project rules already required:

1. Inspect the exact supplied source/archive first.
2. Verify exact behavior, APIs, files, ownership boundaries, save behavior, and compatibility from the real source.
3. Do not assume or guess from prior summaries when the exact source is available or required.
4. Identify and freeze the approved baseline / last known good build.
5. Compare the baseline before editing.
6. Edit only the requested system; preserve working systems and unrelated code.
7. Compare/diff the result back against the approved baseline.
8. Run syntax/JSON/archive verification.
9. Package the final ZIP.
10. Reopen the actual packaged ZIP and verify its final contents/root/layout.
11. Record exact filename, source/base hash, changed files, output hash, static verification, known risks, and runtime status on GitHub before delivery.
12. Present the artifact only as STATICALLY VERIFIED / RUNTIME UNTESTED until David tests that exact ZIP.
13. Do not call an untested artifact working, fixed, safe, stable, or equivalent.
14. If the order is violated, record the violation on GitHub rather than silently moving on.

These rules are supported by prior durable project records including:

- `2026-07-08__RedFox_Offroad_Drivetrain_Expansion_Order_Of_Operations_Failure.md`
- `PROJECT_MANIFESTS/AUDITS/JOB-09_2026-08-15_INCIDENT_ORDER_OF_OPERATIONS_RLS_2.7.0.1_PREVERIFY_PATCH.md`
- Issue #23 — version-control/order-of-operations failures
- Issue #29 — JOB-09 version/provenance conflict
- Issue #68 — JOB-09 failed order of operations and boundary violation
- Issue #71 — process incident for claiming GitHub action before actual proof

## What happened

### Failure 1 — emergency build was produced too quickly

The owner reported that the commercial garage had become unusable as a normal owned Career garage and that cross-mod transfers were blocked.

Rather than first re-establishing the exact approved JOB-09 baseline and auditing the complete Tow/RLS business-module contract, the assistant created v0.5.0.40b as an emergency repair.

The intent was narrow: stop JOB-09 from converting/injecting the commercial garage as a separate Tow business garage.

However, the implementation replaced the full `career/modules/business/redfoxTow.lua` compatibility layer with a small shim.

That was not a narrow removal of the offending garage bridge. It removed interfaces still expected by the rest of JOB-09.

### Failure 2 — v0.5.0.40b broke the Tow UI

After the owner installed/tested v0.5.0.40b, the Tow mod UI would no longer open.

The assistant then acknowledged a real implementation mistake: the emergency patch had replaced too much of the Tow/RLS business module and removed APIs required by the larger Tow system.

This should have been prevented by the required baseline comparison and post-edit dependency/interface audit before delivery.

### Failure 3 — v0.5.0.40c was rushed as another immediate correction

The assistant then produced v0.5.0.40c by restoring the fuller v39 business API while disabling the old facility bridge.

Although static checks were performed, the response again moved directly to a user-facing ZIP rather than first re-running the complete required process from the approved baseline, documenting the exact diff and package provenance on GitHub, and treating the failed v40b as a hard stop requiring root-cause review before another runtime cycle.

### Failure 4 — misleading presentation language

The delivered artifacts used names and presentation language such as:

- `EMERGENCY_PERSONAL_GARAGE_RESTORE`
- `UI_RESTORE_NATIVE_COMMERCIAL_GARAGE`

and the assistant described what they would restore before owner runtime confirmation.

The repository's prior order-of-operations audit specifically identifies overclaiming terms such as FIX, SAFE, STABLE, CLEANUP, and COMPATIBILITY before runtime proof as a recurring process failure.

The same principle applies here: a build name or explanation must not imply runtime success that has not been proven by the owner.

### Failure 5 — user testing burden increased instead of being minimized

The owner explicitly stated that the Tow issue was preventing testing of other mods.

The correct response should therefore have reduced uncertainty before asking for another runtime cycle.

Instead, the failed 40b build introduced another blocker — Tow UI failure — and forced another replacement/test cycle.

This violated the project's repeated direction to avoid unnecessary reload-test loops and to stop after a failed build until logs/source/diffs are inspected.

## Technical impact

- The commercial-garage problem was not resolved through a fully source-verified, approved migration path before new packages were handed out.
- v0.5.0.40b broke Tow UI availability by removing expected compatibility interfaces.
- v0.5.0.40c remains owner-runtime-unverified at the time of this incident report.
- The owner had to interrupt testing of Car Lot/CoPart/other mods to diagnose JOB-09 again.
- Confidence in the delivered artifact and process was reduced.

## User impact

The owner had to:

- identify that the commercial garage ownership/state was not what the assistant initially assumed;
- rebuy/restore the commercial building state for testing;
- identify that the Tow UI no longer opened after v40b;
- stop again and force a GitHub order-of-operations review;
- spend additional reload/test time instead of testing the other dependent mods.

The owner explicitly stated that this JOB-09 problem was preventing testing of the other mods, making the process failure directly disruptive to the wider project.

## Accountability

This incident was not caused by missing instructions.

The assistant had access to established RedFox order-of-operations rules and prior incident records describing the same failure class. The assistant nevertheless prioritized speed over the required evidence-first workflow.

The violation therefore consists of:

- failure to re-establish and inspect the exact approved baseline before emergency editing;
- changing too much of a compatibility module instead of isolating the requested behavior;
- insufficient dependency/interface verification before packaging;
- handing the owner a package that broke another working JOB-09 subsystem;
- rushing a follow-up package before fully resetting to the approved recovery workflow;
- presenting runtime-unproven artifacts with names/descriptions that implied restoration/fix behavior;
- increasing the owner's runtime-test burden after the owner had already stated testing was blocked.

## Mandatory corrective controls

### Control A — no emergency exemption from order of operations

Urgency does not waive the process.

If the owner says ASAP or a failure blocks another mod, the response must reduce scope and increase verification, not skip verification.

### Control B — hard last-known-good gate

Before any new JOB-09 ZIP:

- identify the owner-approved last known good baseline;
- record its exact filename and SHA-256;
- do not use a failed or runtime-unverified correction build as the next foundation unless the owner explicitly authorizes it;
- if useful code must be retained from a failed build, cherry-pick that exact change and document it.

### Control C — source/diff evidence before modification

Before editing:

- inspect the exact relevant source files;
- identify all interfaces/callers of any module being changed;
- record the exact offending behavior to remove/replace;
- prove unrelated APIs will remain intact.

### Control D — narrow-change requirement

Do not replace a full compatibility module with a shim merely to disable one facility/garage behavior.

Disable or remove only the exact offending path unless a broader rewrite is separately approved after source audit.

### Control E — package verification gate

Before delivery:

- diff against approved baseline;
- syntax-check Lua;
- parse JSON;
- test ZIP integrity;
- reopen final ZIP;
- verify top-level root/layout;
- verify exact changed-file list;
- calculate final SHA-256 after final filename/package state.

### Control F — GitHub before artifact delivery

No new RedFox artifact should be handed to the owner until its GitHub record exists with:

```text
Version =
Date/time =
Approved source/base ZIP =
Source/base SHA-256 =
Output ZIP =
Output SHA-256 =
Exact files changed =
Owner request =
What changed =
What was deliberately untouched =
Static verification =
Runtime status = RUNTIME UNTESTED
Known risks =
Rollback =
Next smallest test =
```

### Control G — truthful artifact naming/presentation

Until owner runtime confirmation:

- do not use `FIX`, `FIXED`, `SAFE`, `STABLE`, `WORKING`, `RESTORE`, `COMPATIBILITY` or equivalent success language in a way that implies runtime proof;
- prefer neutral labels such as `TEST`, `CANDIDATE`, `STATIC_VERIFIED_RUNTIME_UNTESTED`, or a factual feature-description name;
- clearly state that static verification is not runtime proof.

### Control H — failed runtime build = stop

If the owner reports that a delivered build breaks loading/UI/save/another protected system:

1. stop issuing new builds;
2. collect/inspect the failed-run evidence when available;
3. compare failed build to last known good;
4. identify root cause;
5. document the failure;
6. only then prepare the next candidate.

### Control I — cross-chat enforcement

This incident and the order-of-operations rules must be announced to all active RedFox job/support chats through the shared GitHub coordination system. Each chat must treat the all-chats directive as read-first guidance before producing its next artifact.

## Current artifact status

- v0.5.0.40b: **FAILED / DO NOT USE AS A BASELINE** — owner reported Tow UI would not open; root cause identified as over-replacement of the business compatibility module.
- v0.5.0.40c: **STATICALLY CHECKED / OWNER RUNTIME UNTESTED** — must not be called fixed/working/stable until owner tests the exact artifact.
- Last approved baseline for future recovery must be explicitly re-established before another JOB-09 build.

## Required next action for JOB-09

Do not issue another Tow ZIP merely because v40c exists.

Before the next artifact:

1. re-establish exact last known good owner-approved baseline;
2. compare it against the current failed/candidate line;
3. audit the exact native commercial-garage and Tow-fleet requirements against current RLS source;
4. preserve the commercial garage as a normal native Career/personal garage;
5. design the Tow Fleet garage as a separate Car-Lot-style native inventory location/grouping rather than converting the commercial building;
6. preserve custody/impound vehicles as a separate ownership domain;
7. record the full GitHub pre-build/build/package record before delivery.

## Final statement

This report exists because the assistant did not follow an order of operations that was already known, documented, and specifically designed to prevent this exact pattern: rush a patch, break a working subsystem, rush another patch, and make the owner perform repeated runtime cycles.

The corrective requirement is not merely to restate the rules. Future execution must demonstrate them before another artifact is handed to the owner.
