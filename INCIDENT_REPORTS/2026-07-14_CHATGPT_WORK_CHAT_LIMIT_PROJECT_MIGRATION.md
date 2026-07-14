# Incident Report — ChatGPT Work-Chat Limit Interrupted RedFox/FoxNet Development

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 12:27 PDT (America/Los_Angeles)  
**Related JOB:** JOB-01 — Phone + PC Platform Core; project-wide impact across coordinated JOB-00 through JOB-12 lanes  
**Status:** OPEN — MANUAL CHAT MIGRATION AND CONTEXT RECONSTRUCTION IN PROGRESS

## Incident summary

The RedFox/FoxNet BeamNG Web System project chats were unintentionally created as ChatGPT Work chats. David / Captain was not aware that the entire project would be subject to a separate Work-chat usage limit. On July 14, 2026, the original Work chats became inaccessible and indicated that access would not resume until July 20, 2026.

This access restriction interrupted development across multiple coordinated jobs. Each job now has to be transferred manually into a new regular ChatGPT chat. The transfer process may require files, context, test history, and development ownership to be reconstructed or reuploaded.

## User impact

- Development was interrupted across multiple coordinated jobs.
- The active chats could no longer inspect their own complete conversation history or attachments.
- Each job must be recreated manually in a separate regular chat.
- Files and screenshots that existed only as chat attachments may need to be uploaded again.
- Testing history and unresolved bug context may be incomplete.
- GitHub ownership and job coordination must be revalidated for every transferred chat.
- The situation creates duplicate-work risk, loss-of-context risk, coordination problems, and unnecessary delay.

## Factual criticism and process concern

David was not clearly aware that creating the project in Work chats placed the coordinated project under a separate usage limit that could lock the chats before the work was finished. The resulting interruption materially affected continuity and required a manual recovery process. This incident is being preserved so it can be included in a report to OpenAI.

## Scope of this GitHub change

### What changed

- Added this project incident record.
- Recorded the July 14, 2026 lockout and the July 20, 2026 displayed return date.
- Recorded the required manual transfer and reconstruction work.

### Why it changed

A durable repository audit record is necessary because the original chat system cannot currently be relied upon as the only source of project history.

### Files affected

- `INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md`

No runtime mod source, RLS files, phone/PC files, generated builds, or other job-owned implementation files were changed by this commit.

## Current status

- Project migration: in progress.
- JOB-01 takeover: recorded separately in `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-01_PHONE_PC_PLATFORM_CORE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`.
- Original Work chats: inaccessible at the time of this record.
- Expected access date shown to the user: July 20, 2026.
- Development continuity: partially restored through GitHub records, but chat-only attachments and discussion may still be missing.

## Known problems

- Shared ChatGPT links may not expose all attachments, tool activity, or hidden/locked conversation content to a replacement chat.
- Generated ZIPs were not always committed because they may contain user-supplied third-party mod files.
- Some screenshots and test logs may exist only in the locked chats.
- Multiple jobs can make conflicting assumptions when their original handoffs are unavailable.
- Reconstructing from GitHub can recover committed source and contracts but cannot guarantee recovery of every chat-only decision.

## Required next steps

1. Create one regular replacement chat per job without renumbering or merging jobs.
2. Inspect each job's GitHub claim, handoffs, branches, pull requests, source, and status reports.
3. Record a dated takeover note for each migrated job.
4. Request only the exact missing binary files, screenshots, or logs needed by that job.
5. Preserve all existing commits, audit trails, test evidence, and unresolved issues.
6. Do not declare a build working unless the exact build has been tested and documented.
7. Add further evidence or corrections to this incident record without deleting the original account.

## Audit trail rule

Future updates must append dated notes or make traceable commits. Do not rewrite this incident into a generic outage note, remove the criticism, minimize the impact, or present the manual migration as ordinary planned work.

## JOB-05 migration note — 2026-07-14 12:43 PDT

**Job:** JOB-05 — BeamBook Marketplace  
**Change:** Transferred active development ownership from the inaccessible Work chat to a replacement regular chat and created a job-specific recovery record.  
**Why:** The original Work chat was inaccessible because of the separate Work-chat usage limit, so continuity had to be reconstructed from GitHub and limited available project context.  
**Files affected:**

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_ALL_JOBS_REGULAR_CHAT_MIGRATION_STATUS_2026-07-14.md
INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md
```

**Current status:** MIGRATED TO REGULAR CHAT — STANDALONE v0.1.0 BUILT — RUNTIME UNTESTED.  
**Known problems:** The shared link could not be fetched; complete chat-only context is not recovered; the exact candidate has no recorded BeamNG/RLS runtime test; shared IceFox phone/PC integration remains blocked.  
**Required next step:** Test `PROJECT_RELEASE_CANDIDATES/JOB-05/5-RedFox_BeamBook_Standalone_v0_1_0_RUNTIME_UNTESTED.zip` with the original third-party `beamBook.zip` disabled, then preserve the `[RedFox][BEAMBOOK]` logs and screenshots of each discovery/purchase checkpoint.

This note does not minimize the interruption. Manual migration was required because the project was unintentionally subject to the Work-chat usage limit, producing duplicate-work risk, loss-of-context risk, coordination problems, and unnecessary delay.

## JOB-10 migration note — 2026-07-14 12:52 PDT

**Job:** JOB-10 — Visual Design / Real Website Polish  
**Change:** Transferred active development ownership from the inaccessible Work chat to a replacement regular chat, created a JOB-10 recovery record, updated the active JOB-10 claim, and marked the job migrated in the owner tracker.  
**Why:** The original Work chat was inaccessible because of the separate Work-chat usage limit. The supplied share link returned no retrievable transcript or attachments, so continuity had to be reconstructed from GitHub and limited available project context.  
**Files affected:**

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_ALL_JOBS_REGULAR_CHAT_MIGRATION_STATUS_2026-07-14.md
INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md
```

**Current status:** MIGRATED TO REGULAR CHAT — CLAIMED — BLOCKED — NO JOB-10 VISUAL BUILD OR EDITABLE BASELINE RECOVERED.  
**Known problems:** The complete old transcript and attachments are unavailable; the exact current IceFox/FoxNet ecosystem ZIP and third-party `beamBook.zip` are not stored in GitHub; any uncommitted JOB-10 source or mockups may be missing; related JOB-01 and JOB-05 candidates remain runtime untested; stable functional handoffs are incomplete.  
**Required next step:** Reupload the exact current ecosystem ZIP and `beamBook.zip`, perform an inspection-only comparison against the nine committed BeamBook visual references and JOB-01 draft PR `#3`, then publish the exact editable/protected file manifest and viewport requirements before any visual code changes.

This JOB-10 note preserves the criticism and impact. The manual transfer was not routine planned work; it was required because the project was unintentionally placed under a separate Work-chat usage limit, causing development interruption, duplicate-work risk, loss-of-context risk, coordination problems, and unnecessary delay.

## JOB-11 migration note — 2026-07-14 13:02 PDT

**Job:** JOB-11 — QA / Logging / Failure Triage  
**Change:** Transferred active development ownership from the inaccessible Work chat to a replacement regular chat, created a JOB-11 recovery record, updated the active JOB-11 claim, and marked the job migrated in the owner tracker.  
**Why:** The original Work chat was inaccessible because of the separate Work-chat usage limit. The supplied share link returned no retrievable transcript or attachments, so continuity had to be reconstructed from GitHub and limited available project context.  
**Files affected:**

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_ALL_JOBS_REGULAR_CHAT_MIGRATION_STATUS_2026-07-14.md
INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md
```

**Current status:** MIGRATED TO REGULAR CHAT — CLAIMED — QA FRAMEWORK DOCUMENTATION ONLY — NO JOB-11 RUNTIME BUILD.  
**Known problems:** The complete old transcript and attachments are unavailable; no separate logging specification, master test matrix, failure-template set, package checker, fingerprint checklist, JOB-11 branch, runtime build, or BeamNG test bundle exists in GitHub; JOB-01 and JOB-05 candidates remain runtime untested; the JOB-02/JOB-03 contracts and canonical integrated baseline remain incomplete.  
**Required next step:** Publish the missing JOB-11-owned QA artifacts, then run static Gate 1 on the first exact candidate supplied by JOB-00 or David. Runtime must remain unproven until David tests the exact candidate in BeamNG and supplies logs, installed-mod fingerprints, timestamps, and screenshots.

This JOB-11 note preserves the criticism and impact. The manual transfer was not routine planned work; it was required because the project was unintentionally placed under a separate Work-chat usage limit, causing development interruption, duplicate-work risk, loss-of-context risk, coordination problems, and unnecessary delay.
