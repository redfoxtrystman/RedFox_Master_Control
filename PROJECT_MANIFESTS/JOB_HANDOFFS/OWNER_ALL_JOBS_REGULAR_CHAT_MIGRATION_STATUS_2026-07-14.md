# Owner Migration Tracker — Work Chats to Regular Chats

**Created:** 2026-07-14 11:11 PDT / America/Los_Angeles  
**Owner:** David / Captain  
**Maintained by:** JOB-00 — Coordinator / Integration / Verification regular-chat takeover / Sol  
**Status:** ACTIVE

---

## Purpose

Track the transfer of each RedFox/FoxNet job from the inaccessible ChatGPT Work project into a replacement regular chat. A job is marked `MIGRATED` only when the new chat has accepted the exact job, updated or created its GitHub claim/migration record, documented recovery limits, and identified required reuploads.

Related records:

```text
INCIDENT_REPORTS/2026-07-14_ChatGPT_Work_Chat_Project_Lockout_And_Regular_Chat_Migration.md
INCIDENT_REPORTS/ALL_REDFOX_CHATS_REGULAR_CHAT_MIGRATION_DIRECTIVE_2026-07-14.md
```

---

## Status labels

```text
MIGRATED — GitHub claim and recovery record complete
REGULAR CHAT CREATED — GITHUB TAKEOVER NOT VERIFIED
NOT YET MIGRATED
BLOCKED — OLD LINK OR JOB ID MISSING
```

---

## Current migration status

| Job | Title | Migration status | Evidence / next requirement |
|---|---|---|---|
| JOB-00 | Coordinator / Integration / Verification | MIGRATED — GitHub claim and recovery record complete | Active replacement regular chat owns the claim. Original Work-chat link recorded. |
| JOB-01 | Phone + PC Platform Core | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-02 | Shared RLS / Career Bridge | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-03 | RedFox App Store / Play Store | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-04 | Scrap Yard / Wrecking Yard | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-05 | BeamBook Marketplace | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:43 PDT. Old link: `https://chatgpt.com/share/6a5690e6-a5fc-83e8-ab78-5ea80ad87da7`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`. Recovery: PARTIAL/GITHUB-RECOVERED. No binary reupload is required before testing the exact v0.1.0 candidate; next action is BeamNG/RLS runtime testing and logs. |
| JOB-06 | Import / Export Yard | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-07 | Classics / Collector Exchange | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-09 | Tow / Recovery / Dispatch Integration | REGULAR CHAT CREATED — GITHUB TAKEOVER NOT VERIFIED | David reports this job has already been moved. The new JOB-09 chat must update its own claim and recovery record before JOB-00 marks it migrated. |
| JOB-10 | Visual Design / Real Website Polish | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-11 | QA / Logging / Failure Triage | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |

---

## JOB-00 takeover evidence

Original Work-chat link:

```text
https://chatgpt.com/share/6a56797e-c8c0-83e8-9940-172bb992f9ce
```

Active claim:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-00_COORDINATOR_INTEGRATION_VERIFICATION_CLAIM.md
```

Recovery state:

```text
PARTIALLY RECOVERED
```

Complete shared-chat content was not recoverable through the unauthenticated share-page fetch. GitHub records and available project continuity were used. No full recovery is claimed.

---

## Update rule

When a job completes migration, update only that row with:

- new regular-chat title;
- takeover timestamp;
- old Work-chat shared link;
- claim or handoff path;
- commit SHA;
- recovery label;
- required missing files;
- next concrete action.

Do not mark a job migrated solely because a replacement chat was opened.

---

## Audit trail

- **2026-07-14 11:11 PDT — JOB-00:** Created the tracker after completing the JOB-00 regular-chat GitHub takeover.
- **2026-07-14 11:11 PDT — JOB-09:** Recorded David's report that a replacement regular chat exists; GitHub takeover remains unverified and is not marked complete.
- **2026-07-14 12:43 PDT — JOB-05:** Marked BeamBook Marketplace migrated after the regular chat accepted the exact job, created a recovery/takeover record, preserved standalone v0.1.0 as runtime untested, documented shared-link limitations, and identified the exact next runtime evidence.