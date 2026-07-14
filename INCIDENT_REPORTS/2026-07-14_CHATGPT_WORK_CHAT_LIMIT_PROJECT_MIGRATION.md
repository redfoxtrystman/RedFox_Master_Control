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