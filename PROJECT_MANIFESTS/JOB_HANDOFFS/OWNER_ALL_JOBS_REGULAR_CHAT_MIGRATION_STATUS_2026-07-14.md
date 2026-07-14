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
| JOB-02 | Shared RLS / Career Bridge | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:44 PDT. Old link: `https://chatgpt.com/share/6a569142-069c-83e8-b4bf-30a3f6e3179f`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-02_SHARED_RLS_CAREER_BRIDGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`; takeover commit `9631d9f560d0a7dd7ea0f7b8bb1c0230e61acc93`. Recovery: PARTIAL/GITHUB-RECOVERED. Required gaps: two exact baseline ZIPs and three uncommitted contract/schema/fixture drafts. Next action: verify or reconstruct the contract packet and publish `job02.bridge.v1` before any runtime adapter. |
| JOB-03 | RedFox App Store / Play Store | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-04 | Scrap Yard / Wrecking Yard | NOT YET MIGRATED | Needs replacement regular chat, old share link, claim update, recovery report, and exact file request. |
| JOB-05 | BeamBook Marketplace | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:43 PDT. Old link: `https://chatgpt.com/share/6a5690e6-a5fc-83e8-ab78-5ea80ad87da7`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`. Recovery: PARTIAL/GITHUB-RECOVERED. No binary reupload is required before testing the exact v0.1.0 candidate; next action is BeamNG/RLS runtime testing and logs. |
| JOB-06 | Import / Export Yard | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:46 PDT. Old link: `https://chatgpt.com/share/6a569182-d3d0-83e8-9968-86e544c06058`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-06_IMPORT_EXPORT_YARD_REGULAR_CHAT_TAKEOVER_2026-07-14.md`; takeover commit `dd4f9665b5d436a55db18c8a2dc4e9dd3104fc68`. Recovery: PARTIAL/GITHUB-RECOVERED; shared-chat content unavailable. Required now: `Export_Yard_DROP_IN_v1`, `redfox_web_ecosystem_v1_combined_VERIFIED.zip`, the current FoxNet/IceFox full baseline, original Export Yard assets, and any newer JOB-06 build. Next action is an inspection-only baseline comparison and exact edit manifest; implementation remains BLOCKED. |
| JOB-07 | Classics / Collector Exchange | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:49 PDT. Old link: `https://chatgpt.com/share/6a569217-c020-83e8-83de-c947aa36c1ea`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-07_CLASSICS_COLLECTOR_EXCHANGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`; takeover commit `d9c9b5d75dca04e1960c61a2426429723f8f2a13`. Recovery: PARTIAL/GITHUB-RECOVERED. Required input: `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX(1).zip`, size `24,510,848`, SHA-256 `4dac614a4b14d423c069dccc8bdb5e0e511ee208f7414d3e6ed50a86a7903597`. Next action: inspect existing Classics paths/route/assets, publish a JOB-07 baseline inventory, and wait for the final JOB-02 bridge before transaction implementation. |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:51 PDT. Old link: `https://chatgpt.com/share/6a5692c2-5a8c-83e8-99d6-41860c4167ea`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-08_INSURANCE_FINANCE_GARAGE_STORAGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`; takeover commit `cac9fc6fd0ec1490143da65b446fc0c130bdb413`. Recovery: PARTIAL/GITHUB-RECOVERED; shared-chat transcript and attachments unavailable. Required now: the v0.10.3.7 all-in-one FoxNet candidate, the v0.10.3.1 phone-working baseline, RLS Career Overhaul 2.6.6, full RLS evidence archive, designed JOB-08 site package, approved reference mod, missing JOB-02 contract packet, and relevant Garage/Insurance/Finance settings/save JSON. Next action: inspection-only baseline and contract-gap comparison; no JOB-08 runtime build exists. |
| JOB-09 | Tow / Recovery / Dispatch Integration | REGULAR CHAT CREATED — GITHUB TAKEOVER NOT VERIFIED | David reports this job has already been moved. The new JOB-09 chat must update its own claim and recovery record before JOB-00 marks it migrated. |
| JOB-10 | Visual Design / Real Website Polish | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 12:52 PDT. Old link: `https://chatgpt.com/share/6a569314-28cc-83e8-90de-fe8ffedb01e6`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md`; takeover commit `1713002ab9344c766a3f8d80af821c8407320b8e`; claim-transfer commit `32d364c876a456d6da2adf7f8bffec0b2d1561a1`. Recovery: PARTIAL/GITHUB-RECOVERED. Required now: `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX(1).zip` and `beamBook.zip`; conditional: any uncommitted JOB-10 source/mockups and the original dark IceFox UI reference image. Next action: perform an inspection-only baseline comparison and publish the exact editable/protected file manifest and viewport requirements; implementation remains BLOCKED. |
| JOB-11 | QA / Logging / Failure Triage | MIGRATED — GitHub claim and recovery record complete | Regular-chat takeover accepted 2026-07-14 13:02 PDT. Old link: `https://chatgpt.com/share/6a569566-a808-83e8-a996-2ffa49aaf713`. Evidence: `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md`; takeover commit `b29289dd7c804226f41318917989243c0061bec8`; claim-transfer commit `cc081f020faf1c1029ca27d6859d584d90519f55`. Recovery: PARTIAL/GITHUB-RECOVERED; shared transcript and attachments unavailable. No reupload is required to recover prior JOB-11 work because it was documentation only. Missing deliverables: logging specification, master test matrix, failure templates, package checker, and fingerprint checklist. Next action: publish those JOB-11-owned QA artifacts, then run static Gate 1 on an exact candidate supplied by JOB-00 or David. |
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
- **2026-07-14 12:44 PDT — JOB-02:** Marked Shared RLS / Career Bridge migrated after the replacement regular chat accepted the exact unchanged job, documented the inaccessible shared-link result, created the takeover record, identified exact reuploads, and preserved the no-runtime-build status. Takeover commit: `9631d9f560d0a7dd7ea0f7b8bb1c0230e61acc93`.
- **2026-07-14 12:46 PDT — JOB-06:** Marked Import / Export Yard migrated after the replacement regular chat accepted the unchanged job, created a JOB-06 recovery/takeover record, documented the inaccessible shared-chat content, preserved the original claim and incident history, listed exact required reuploads, and left implementation blocked until baseline inspection. Takeover commit: `dd4f9665b5d436a55db18c8a2dc4e9dd3104fc68`.
- **2026-07-14 12:49 PDT — JOB-07:** Marked Classics / Collector Exchange migrated after the replacement regular chat accepted the exact unchanged job, documented that the shared link exposed no retrievable content, preserved the blocked/no-build status, identified the exact IceFox baseline reupload, and recorded the next baseline-inspection action. Takeover commit: `d9c9b5d75dca04e1960c61a2426429723f8f2a13`.
- **2026-07-14 12:51 PDT — JOB-08:** Marked Insurance / Finance / Garage / Storage Pages migrated after the replacement regular chat accepted the exact unchanged job, documented that the shared chat transcript and attachments were not recoverable, preserved the original scope and no-runtime-build state, identified exact baseline, RLS, contract, settings, and save-file gaps, and recorded an inspection-only next action. Takeover commit: `cac9fc6fd0ec1490143da65b446fc0c130bdb413`.
- **2026-07-14 12:52 PDT — JOB-10:** Marked Visual Design / Real Website Polish migrated after the replacement regular chat accepted the exact unchanged job, documented the shared-link fetch failure, preserved the blocked/no-build status, recovered the GitHub-hosted BeamBook visual references and related candidates, identified the two exact required binary reuploads, and recorded the inspection-only next action. Takeover commit: `1713002ab9344c766a3f8d80af821c8407320b8e`; claim-transfer commit: `32d364c876a456d6da2adf7f8bffec0b2d1561a1`.
- **2026-07-14 13:02 PDT — JOB-11:** Marked QA / Logging / Failure Triage migrated after the replacement regular chat accepted the exact unchanged job, documented that the shared link exposed no retrievable transcript or attachments, preserved the documentation-only/no-build state, identified the missing QA deliverables and exact future test inputs, and recorded the next QA-framework action. Takeover commit: `b29289dd7c804226f41318917989243c0061bec8`; claim-transfer commit: `cc081f020faf1c1029ca27d6859d584d90519f55`.
