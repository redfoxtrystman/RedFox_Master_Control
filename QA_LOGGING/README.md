# RedFox/FoxNet QA, Logging, and Failure Triage

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 13:08 PDT (America/Los_Angeles)  
**Owner:** JOB-11 — QA / Logging / Failure Triage  
**Status:** INITIAL QA FRAMEWORK PUBLISHED — STATIC TOOL SELF-TESTED — BEAMNG RUNTIME UNPROVEN

## Purpose

This folder contains JOB-11-owned QA standards and tools. It does not contain phone, PC, browser, bridge, Store, Career/RLS, app/page, visual, money, inventory, garage, storage, insurance, ownership, purchase, sell, spawn, save, or another job's implementation.

JOB-11 identifies the earliest provable failing layer and returns evidence to the owning job. JOB-00 alone decides whether a candidate advances to integration.

## Files

```text
QA_LOGGING/README.md
QA_LOGGING/SHARED_LOGGING_SPEC_v1.md
QA_LOGGING/MASTER_TEST_MATRIX_v1.md
QA_LOGGING/INSTALLED_PACKAGE_FINGERPRINT_CHECKLIST_v1.md
QA_LOGGING/PACKAGE_AUDIT_TOOL_README_v1.md
QA_LOGGING/tools/redfox_package_audit.py
QA_LOGGING/templates/FAILURE_REPORT_TEMPLATE.txt
QA_LOGGING/templates/FAILURE_REPORT_TEMPLATE.html
```

## Required status language

```text
PASS — all required static and supplied runtime checks passed
FAIL/STOP — a required check failed; do not ship
BLOCKED — required contract, artifact, dependency, or evidence is missing
RUNTIME UNPROVEN — static checks passed but David has not proven runtime in BeamNG
```

A static PASS is not a BeamNG runtime PASS.

## First use order

1. Obtain the exact candidate ZIP name, size, SHA-256, baseline, dependency hashes, and installed-mod list.
2. Run `tools/redfox_package_audit.py` on all candidate packages that will be installed together.
3. Resolve every `FAIL` and every manual-review blocker before runtime testing.
4. Complete the installed-package fingerprint checklist.
5. Test the exact candidate in BeamNG using the master test matrix.
6. Preserve timestamps, logs, screenshots, and the failure-report template.
7. Return failures to the owning job; do not silently patch another job's code.

## Current known blockers

- JOB-00 has not frozen one canonical integrated baseline for JOB-11.
- JOB-01 v0.2 is a draft source/contracts checkpoint; its generated test ZIP is not committed and runtime is untested.
- JOB-02 has not published production `job02.bridge.v1` and expected log fixtures.
- JOB-03 has not published the final Store manifest/install-state contract.
- Most feature jobs have not submitted complete QA intake packets.
- No clean two-map phone/PC runtime evidence has been supplied for the current platform candidate.

## Change record

**What changed:** Created the JOB-11 QA framework index and published the initial file set.  
**Why:** The previous Work chat promised these shared QA deliverables but only the scope and gates were committed before the Work-chat usage-limit lockout.  
**Files affected:** `QA_LOGGING/README.md` and the JOB-11-owned files listed above.  
**Current status:** Static framework development is active; BeamNG runtime remains unproven.  
**Known problems:** Exact platform candidate, canonical baseline, production bridge/Store contracts, and runtime evidence remain incomplete.  
**Required next step:** Run static Gate 1 against the first exact candidate supplied by JOB-00 or David, then perform the documented BeamNG test matrix without changing another job's implementation.

## Migration note

The original JOB-11 chat became inaccessible on July 14, 2026 because the coordinated project was unintentionally created under a separate ChatGPT Work-chat usage limit, with access shown as unavailable until July 20, 2026. This framework reconstructs missing deliverables from GitHub evidence without claiming recovery of the inaccessible transcript or attachments.
