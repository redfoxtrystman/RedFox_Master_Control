# READ FIRST — ALL REDFOX CHATS / JOBS / SUPPORT WORKSTREAMS
# Mandatory Order-of-Operations Enforcement

**Date:** 2026-09-06  
**Owner:** David / Captain  
**Scope:** ALL RedFox BeamNG chats, jobs, support workstreams, compatibility mods, test tools, hotfixes, handoffs, and release candidates  
**Status:** MANDATORY READ-FIRST PROCESS GATE

## Why this directive exists

A new JOB-09 incident on 2026-09-06 repeated a failure pattern already documented in this repository: a patch was rushed before the full evidence-first workflow was completed, the patch broke another working subsystem, and a second corrective package was then rushed to the owner.

Incident:

`INCIDENT_REPORTS/2026-09-06_JOB-09_Order_Of_Operations_Violation_40b_40c.md`

This directive is not JOB-09-only. It is a cross-project reminder that the existing RedFox order of operations applies to every chat that creates or edits an artifact.

## Mandatory workflow before any new artifact is handed to David

1. **Read the current job's GitHub claim, ledger, incident reports, handoffs, and read-first directives.**
2. **Identify the exact owner request and freeze scope.** Do not add unrelated improvements.
3. **Identify the last owner-approved / last known-good baseline.** Record exact filename and SHA-256.
4. **Inspect the exact supplied/current source before editing.** Prior summaries may guide the search but may not substitute for direct source inspection when the exact source is available or required.
5. **Verify the exact behavior/API/schema/ownership boundary being changed.** Do not assume or guess.
6. **Compare the baseline before editing.** Record the files/functions involved and the protected systems that must remain unchanged.
7. **Edit only the requested system.** Preserve working code, job boundaries, save safety, and unrelated features.
8. **Compare/diff after editing.** Verify no unrelated files or interfaces changed.
9. **Run static checks appropriate to the artifact.** At minimum where applicable: Lua syntax, JSON parse, HTML/JS/CSS checks, archive integrity, duplicate-path/root-layout checks.
10. **Package the final artifact.**
11. **Reopen the actual final packaged ZIP/file.** Verify final root/layout, expected contents, changed-file list, and absence of accidental nesting/missing files.
12. **Calculate SHA-256 from the final artifact after final naming/package state.**
13. **Post the GitHub build/version record BEFORE user-facing delivery.** The GitHub record is part of the release gate, not an optional later note.
14. **Present the artifact truthfully as STATICALLY VERIFIED / RUNTIME UNTESTED** until David tests that exact artifact.
15. **Do not call the artifact fixed, working, safe, stable, compatible, restored, or runtime-pass before owner confirmation.**
16. **If runtime fails, STOP.** Inspect logs/source/diff and record the failure before issuing another build.
17. **If the process is violated, file an incident report.** Do not hide or silently correct the violation.

## Required GitHub artifact record

Before delivering a new artifact, the owning chat must record at least:

```text
Job / support lane =
Version =
Date/time =
Owner request =
Approved source/base ZIP =
Source/base SHA-256 =
Exact source files inspected =
Exact files changed =
What changed =
What was deliberately untouched =
Output ZIP/file =
Output SHA-256 =
ZIP/package integrity =
Syntax/JSON/static checks =
Final packaged ZIP reopened = YES / NO
Runtime status = RUNTIME UNTESTED unless David already tested this exact artifact
Known risks =
Rollback artifact =
Next smallest runtime test =
```

## Naming / presentation rule

Do not use success-implying labels as proof.

Until David runtime-tests the exact artifact, prefer neutral names such as:

```text
TEST
CANDIDATE
STATIC_VERIFIED_RUNTIME_UNTESTED
PROOF
EXPERIMENT
```

Avoid using terms such as these as though they are established runtime facts:

```text
FIX
FIXED
SAFE
STABLE
WORKING
RESTORE
COMPATIBILITY
PASS
```

A factual feature label is fine, but wording must not imply runtime confirmation that has not occurred.

## Hard stop after a failed build

When David reports that a build causes any of the following:

- Career/game load failure;
- UI not opening;
- save/ownership/garage corruption;
- another working mod or job no longer functioning;
- crash/freeze;
- repeated periodic lag or UI reload;
- missing vehicles/money/state;
- a protected feature regression;

then the owning chat must NOT immediately issue another ZIP.

Required sequence:

1. mark the candidate failed/unproven;
2. preserve the failed artifact identity;
3. inspect the failed-run evidence/logs if available;
4. diff against last known good;
5. identify root cause or narrow the failure boundary;
6. record the failure on GitHub;
7. only then prepare the next candidate from an approved baseline.

## Cross-job boundary rule

No chat may edit another job's owned files merely because doing so would be faster.

If another job must change:

- stop at the ownership boundary;
- post a GitHub handoff/request;
- let that job own its source change;
- coordinate the compatible test pair before asking David to reload/test.

## Save-safety rule

Career save, ownership, garage, business, inventory, insurance, money, and transaction changes are high-risk.

Before touching them:

- inspect exact current RLS/BeamNG source involved;
- preserve exact native IDs and authoritative ownership domains;
- do not delete/recreate as a shortcut when a same-record transfer is possible;
- do not automatically migrate/merge state from another save/profile;
- do not charge/remove/delete until the native operation is verified;
- preserve rollback/quarantine behavior for partial failures.

## Urgency is not an exception

`ASAP`, `immediately`, or `this is blocking another mod` means the chat should make the change **smaller and better verified**.

Urgency does not authorize skipping source inspection, GitHub records, package reopening, diffing, or truthful runtime labeling.

## Required acknowledgement behavior for active chats

Before the next artifact from an active RedFox chat/job/support lane, that chat should state in its own GitHub ledger/comment that it has read this directive and will follow it.

The acknowledgement should include:

```text
ORDER OF OPERATIONS ACK — JOB/SUPPORT NAME
Read directive = PROJECT_MANIFESTS/00_READ_FIRST_ALL_CHATS_ORDER_OF_OPERATIONS_ENFORCEMENT_2026-09-06.md
Last known good identified = YES / NO
Pre-edit source inspection required = YES
Post-edit diff required = YES
Final package reopen required = YES
GitHub record before delivery required = YES
Runtime truth label required = YES
Failed-build hard stop acknowledged = YES
Cross-job boundary acknowledged = YES
```

## Related durable records

- `INCIDENT_REPORTS/2026-09-06_JOB-09_Order_Of_Operations_Violation_40b_40c.md`
- `2026-07-08__RedFox_Offroad_Drivetrain_Expansion_Order_Of_Operations_Failure.md`
- `PROJECT_MANIFESTS/AUDITS/JOB-09_2026-08-15_INCIDENT_ORDER_OF_OPERATIONS_RLS_2.7.0.1_PREVERIFY_PATCH.md`
- Issue #23 — artifact/version-control order failure
- Issue #29 — JOB-09 provenance/version conflict
- Issue #68 — JOB-09 failed order of operations / boundary violation
- Issue #71 — process proof/filing incident

## Final rule

**The next artifact is not ready for David merely because code was written and a ZIP exists.**

It is ready to be handed to David only after the required source evidence, narrow edit, diff, static checks, final package reopening, GitHub checkpoint, and truthful runtime status are complete.
