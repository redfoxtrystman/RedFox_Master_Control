# RedFox Project Incident Report: ChatGPT Work-Chat Lockout and Regular-Chat Migration

**Date/time created:** 2026-07-14 11:11 PDT / America/Los_Angeles  
**Reporting job:** JOB-00 — Coordinator / Integration / Verification  
**Reporting chat:** JOB-00 regular-chat takeover / Sol  
**Requested by:** David / Captain  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Status:** ACTIVE RECOVERY / CONTEXT MIGRATION

---

## 1. Executive summary

David reports that the coordinated RedFox/FoxNet rebuild chats were unintentionally created inside ChatGPT Work chats without him understanding that the full project would be governed by a separate Work-chat usage limit. On 2026-07-14, access to the original project chats became unavailable until Monday, 2026-07-20.

The access interruption stopped active work across multiple coordinated jobs. Continuing the project now requires each job to be transferred manually into a normal ChatGPT chat, the new chat to take over the corresponding GitHub claim, and potentially important files, logs, screenshots, test builds, and context to be reuploaded.

This is not a BeamNG code failure. It is a project-access and continuity incident that creates a material risk of duplicated work, missing context, stale ownership records, inconsistent baselines, and lost testing history.

The lockout date and expected restoration date are recorded from David's direct report. JOB-00 cannot independently inspect account-plan limits or the locked Work-chat interface.

---

## 2. Scope

Potentially affected jobs:

```text
JOB-00 through JOB-12
```

Known migration status at the time this report was created:

- JOB-09 has already been moved into a regular chat according to David.
- JOB-00 is being transferred through this report and its updated claim record.
- The remaining jobs require separate regular-chat takeover, GitHub claim updates, and missing-file/context checks.

Original JOB-00 Work-chat shared link:

```text
https://chatgpt.com/share/6a56797e-c8c0-83e8-9940-172bb992f9ce
```

The share page identifies the conversation as `JOB-00 Coordinator / Integration / Verification`, but the complete conversation was not recoverable through the unauthenticated share-page fetch used during this migration. Recovery therefore relies on available project continuity, David's instructions, and the existing GitHub record. No clean or complete recovery is claimed.

---

## 3. Direct project impact

- Active development and coordination were interrupted.
- Each job now requires a replacement regular chat.
- GitHub claim records may still name the inaccessible Work chat.
- Files uploaded only to the locked chat may need to be uploaded again.
- Chat-only testing results, decisions, and unresolved bugs may be absent from GitHub.
- New chats may repeat work already completed if they cannot recover the former history.
- Different jobs may accidentally select different FoxNet baselines.
- New chats may overstate what they recovered unless recovery limits are documented.
- David must spend additional time recreating context and transferring files.

---

## 4. Required migration procedure for every job

Every replacement regular chat must:

1. State the exact unchanged JOB number and title it is taking over.
2. Read the central job board, architecture directive, claim record, handoffs, incidents, and available release candidates before implementation.
3. Record the old Work-chat share link in its claim or migration handoff.
4. State exactly what was recovered from the shared link, GitHub, current project context, and reuploaded files.
5. State exactly what could not be recovered.
6. List the specific files David must reupload and why each is needed.
7. List files already present on GitHub that do not need reuploading.
8. Identify missing logs, screenshots, runtime results, source packages, and reference packages that would materially help.
9. Update only its own GitHub claim/status and permitted shared audit or handoff files.
10. Preserve previous history instead of deleting or rewriting it.
11. Label all unproven runtime behavior honestly.
12. Add a timestamped trail note for the takeover.

A replacement chat must not claim full recovery simply because it can see the conversation title or partial share-page content.

---

## 5. JOB-00 recovery actions

JOB-00 has performed or initiated the following:

- Confirmed the supplied share link is titled `JOB-00 Coordinator / Integration / Verification`.
- Inspected the live GitHub job board and existing JOB-00 claim.
- Preserved JOB-00's role as coordinator, integrator, and verifier rather than a feature-code owner.
- Created this project-level incident report.
- Created an all-jobs regular-chat migration audit directive.
- Updated the JOB-00 claim to transfer active ownership from the inaccessible Work chat to the replacement regular chat while preserving the prior claim history.

---

## 6. Immediate JOB-00 continuity risks

JOB-00 still cannot honestly freeze the canonical platform baseline until it receives or locates the exact candidate files that contain:

- the known working RLS phone and IceFox entry;
- the partially working PC implementation;
- the latest all-in-one FoxNet/Web Ecosystem candidate;
- any newer JOB-01 platform candidate and its source/build/test handoff;
- installed-mod fingerprints and BeamNG logs from the relevant tests.

Until that evidence is available, baseline selection remains `BLOCKED`.

---

## 7. Accountability statement

David's RedFox development work was disrupted by a platform-access boundary he reports he did not understand when the project was created. Regardless of how the account interface presented that boundary, the project now has a real continuity problem that must be documented rather than minimized.

The replacement chats are responsible for being truthful about incomplete recovery, preserving GitHub history, avoiding duplicate work, and requesting only the specific missing files needed for their assigned job.

---

## 8. Evidence and related records

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-00_COORDINATOR_INTEGRATION_VERIFICATION_CLAIM.md
INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md
INCIDENT_REPORTS/ALL_REDFOX_CHATS_REGULAR_CHAT_MIGRATION_DIRECTIVE_2026-07-14.md
```

Signed,

**Sol — JOB-00 Coordinator / Integration / Verification regular-chat takeover**  
**2026-07-14 11:11 PDT**
