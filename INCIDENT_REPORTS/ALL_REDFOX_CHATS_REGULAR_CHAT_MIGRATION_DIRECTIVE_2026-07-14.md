# RedFox All-Chats Regular-Chat Migration Audit Directive

**Date/time created:** 2026-07-14 11:11 PDT / America/Los_Angeles  
**Issued by:** JOB-00 — Coordinator / Integration / Verification regular-chat takeover / Sol  
**Requested by:** David / Captain  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Status:** ACTIVE OWNER DIRECTIVE

---

## 1. Why this directive exists

David reports that the RedFox/FoxNet rebuild jobs were created inside ChatGPT Work chats without him understanding that the project would be governed by a separate Work-chat usage limit. On 2026-07-14, the original chats became inaccessible until Monday, 2026-07-20.

Every job must now be transferred into a normal ChatGPT chat so development can continue. This migration creates a risk of missing files, missing context, duplicate work, stale GitHub claims, inconsistent baselines, and false claims of recovery.

Read the project incident first:

```text
INCIDENT_REPORTS/2026-07-14_ChatGPT_Work_Chat_Project_Lockout_And_Regular_Chat_Migration.md
```

---

## 2. Applies to

```text
JOB-00 through JOB-12
```

Each replacement chat keeps the same exact job number and job title. No job may be renamed, renumbered, merged, or silently reassigned during migration.

---

## 3. Required takeover record

Before implementation, each replacement regular chat must update its existing claim file or create a migration handoff containing:

```text
Exact JOB number and title:
New regular-chat owner title:
Takeover date/time and timezone:
Old Work-chat owner title:
Old Work-chat shared link:
What was recovered from the shared link:
What was recovered from GitHub:
What was recovered from project context or reuploaded files:
What could not be recovered:
Files David must reupload:
Files already available on GitHub:
Missing logs/screenshots/runtime results:
Current build/status:
Known bugs/blockers:
Protected files that will not be edited:
Next concrete action:
```

The old claim and history must be preserved as historical context. Do not delete it merely because the original chat is inaccessible.

---

## 4. Truth rules for migration

A replacement chat must not claim that it read a complete shared chat when it only recovered the title, partial page content, snippets, GitHub notes, or project-memory summaries.

Allowed recovery descriptions include:

```text
FULLY RECOVERED FROM SOURCE
PARTIALLY RECOVERED
RECOVERED FROM GITHUB ONLY
RECOVERED FROM PROJECT CONTEXT, NOT FULL CHAT
BLOCKED — SOURCE OR FILE MISSING
```

Every missing item must be listed. Silence is not proof that nothing is missing.

---

## 5. File reupload rules

Do not ask David to upload everything.

Each job must provide a precise list divided into:

1. **Required now** — cannot continue the next concrete task without it.
2. **Useful but not blocking** — would improve accuracy or restore context.
3. **Already on GitHub** — do not ask David to reupload it.
4. **Mentioned but missing** — known from prior discussion but not found in GitHub or current chat.
5. **Runtime evidence needed** — logs, screenshots, installed-mod list, test steps, map, game version, and exact ZIP identity.

Each requested file must include the reason it is needed.

---

## 6. GitHub ownership rules

Each replacement chat may update only:

- its own job claim and job-specific migration handoff;
- its own status inside the central board when permitted;
- shared migration/incident records when relevant;
- files already permitted by its job scope.

It must not edit another job's implementation or claim.

Every migration GitHub change must include:

- date/time;
- exact JOB number;
- what changed;
- why it changed;
- files affected;
- current status;
- known missing information;
- next action.

---

## 7. Required first response to David

Every new regular chat must report:

```text
Job taken over:
Old Work-chat link:
Recovery status:
Recovered from shared link:
Recovered from GitHub:
Newest known build/status:
Known unresolved bugs:
Required reuploads:
Useful optional reuploads:
Files already on GitHub:
Missing information:
GitHub files changed:
Commit SHA(s):
Next action:
```

If GitHub access or a write action fails, the chat must state the exact failure. It must not claim the takeover is complete.

---

## 8. Coordination requirement

JOB-00 must track which jobs have completed migration and which still point to inaccessible Work chats.

A job is not considered migrated merely because a new regular chat exists. Migration is complete only when:

1. the new chat accepts the exact job;
2. its GitHub claim records the takeover;
3. its recovery limits are documented;
4. required reuploads are identified;
5. current status and next action are recorded.

---

## 9. Relationship to the existing audit directive

This directive supplements, but does not replace:

```text
INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md
```

The original audit still governs false verification, overclaiming, broken-build history, ignored coordination, and order-of-operations failures. This new directive governs continuity and evidence during the Work-chat-to-regular-chat migration.

---

Signed,

**Sol — JOB-00 Coordinator / Integration / Verification regular-chat takeover**  
**2026-07-14 11:11 PDT**
