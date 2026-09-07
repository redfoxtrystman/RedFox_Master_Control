# ALL CHATS HANDOFF — Mandatory RedFox Order of Operations

**Date:** 2026-09-06  
**From:** JOB-09 / owner-directed process correction  
**To:** ALL active RedFox chats, jobs, support workstreams, compatibility projects, and artifact-producing conversations

## Read first

`PROJECT_MANIFESTS/00_READ_FIRST_ALL_CHATS_ORDER_OF_OPERATIONS_ENFORCEMENT_2026-09-06.md`

New incident:

`INCIDENT_REPORTS/2026-09-06_JOB-09_Order_Of_Operations_Violation_40b_40c.md`

## Required action before your next artifact

Every active chat must re-check its current baseline, source, diff, packaging, GitHub checkpoint, and runtime-label process before handing David another file.

Minimum acknowledgement:

```text
ORDER OF OPERATIONS ACK — JOB/SUPPORT NAME
Read directive = YES
Last known good identified = YES / NO
Source inspected before edit = REQUIRED
Post-edit diff = REQUIRED
Final packaged ZIP reopened = REQUIRED
GitHub artifact record before delivery = REQUIRED
Runtime label stays UNTESTED until David confirms = REQUIRED
Failed build causes hard stop before next ZIP = REQUIRED
Cross-job boundaries = REQUIRED
```

## Why this is being broadcast

JOB-09 repeated a known failure pattern on v0.5.0.40b/v0.5.0.40c: emergency patching moved faster than the established evidence-first workflow, the first patch broke the Tow UI, and a follow-up package was rushed before fully resetting to the required recovery process.

The owner explicitly requires this incident and correction to be visible to the other project chats so the same failure is not repeated elsewhere.

## Hard rule

No artifact should be delivered merely because a ZIP exists. Delivery requires source evidence, narrow scope, baseline comparison, post-edit diff, static/package verification, final package reopening, GitHub record, and truthful runtime status.
