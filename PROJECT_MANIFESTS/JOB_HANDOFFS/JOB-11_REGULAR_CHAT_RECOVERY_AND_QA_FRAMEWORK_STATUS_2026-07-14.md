# JOB-11 — Regular-Chat Recovery and QA Framework Status

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 13:12 PDT (America/Los_Angeles)  
**JOB:** JOB-11 — QA / Logging / Failure Triage  
**Owner:** JOB-11 regular-chat takeover / Sol, under David / Captain  
**Status:** MIGRATED — QA FRAMEWORK PUBLISHED — REAL CANDIDATE STATIC AUDIT PENDING — BEAMNG RUNTIME UNPROVEN

## What changed

- Took over the exact unchanged JOB-11 role in a replacement regular chat.
- Created the job-specific takeover/recovery record.
- Updated the active JOB-11 claim.
- Marked JOB-11 migrated in the owner migration tracker.
- Appended the JOB-11 Work-chat lockout impact to the project incident report.
- Published the initial JOB-11 QA framework:

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

## Why it changed

The original JOB-11 chat became inaccessible on July 14, 2026 because the coordinated project had unintentionally been created under a separate ChatGPT Work-chat usage limit, with access shown as unavailable until July 20, 2026. The shared URL did not expose the prior transcript or attachments. GitHub preserved JOB-11's claim and high-level gates, but the promised reusable QA deliverables had not been committed.

This update restores ownership and reconstructs the missing JOB-11-owned QA framework without claiming that inaccessible chat-only work was recovered.

## Files affected

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-11_QA_LOGGING_FAILURE_TRIAGE_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_ALL_JOBS_REGULAR_CHAT_MIGRATION_STATUS_2026-07-14.md
INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-11_REGULAR_CHAT_RECOVERY_AND_QA_FRAMEWORK_STATUS_2026-07-14.md
QA_LOGGING/README.md
QA_LOGGING/SHARED_LOGGING_SPEC_v1.md
QA_LOGGING/MASTER_TEST_MATRIX_v1.md
QA_LOGGING/INSTALLED_PACKAGE_FINGERPRINT_CHECKLIST_v1.md
QA_LOGGING/PACKAGE_AUDIT_TOOL_README_v1.md
QA_LOGGING/tools/redfox_package_audit.py
QA_LOGGING/templates/FAILURE_REPORT_TEMPLATE.txt
QA_LOGGING/templates/FAILURE_REPORT_TEMPLATE.html
```

No phone, PC, browser, platform, bridge, Store, Career/RLS, feature-app, visual, transaction, save, or another job's implementation was changed.

## Commit trail

```text
b29289dd7c804226f41318917989243c0061bec8  JOB-11 takeover/recovery record
cc081f020faf1c1029ca27d6859d584d90519f55  active claim transfer
845eb20ff147a981d43e6ae0b274323e181a549c  owner migration tracker
61fe0c819912db1e131bf2035c37a9bfbdc8ef65  project incident audit note
8d34303b0e0418606d95bd9eb2aff0de7d66acf7  QA framework index
0ebb5577c09b7d4475e876fb9e53a3ff79871c07  shared logging specification
2e9a61cad82d5fb8b04ddc9da3ecc17196d70897  master test matrix
c460299cc438d08237fcaf81461a4df31e9b5992  installed-package fingerprint checklist
a18bda24709e3d23616dfba0b1bb832839c0d079  package auditor instructions
760fb06c65c633c13929286af00bb183707fab13  TXT failure template
846e9a24325f772f9827061e87242d976bdd6bf9  HTML failure template
7654cba94eac6874e85ca196cd8b0d4a2354fc8c  static package auditor
```

## Verification performed

The package auditor was compiled with Python and tested against two synthetic fixtures:

- clean one-root package with all required report patterns: static PASS, runtime unproven;
- package containing `lua/ge/extensions/career/modules/redfoxScrapYardDirect.lua` and missing reports: FAIL/STOP with the expected findings.

This verifies only the exercised static code paths. No real RedFox/FoxNet candidate has yet been audited by this replacement chat, and no BeamNG runtime result is claimed.

## Current known candidates

- JOB-01 IceFox phone + PC platform core v0.2: open draft PR `#3`; source/contracts and builder available; generated ZIP not committed; static checks reported passing; runtime untested.
- JOB-05 BeamBook standalone v0.1.0: candidate committed; runtime untested.

## Known problems

- Shared Work-chat transcript and attachments remain unavailable.
- JOB-00 has not frozen one canonical integrated baseline for JOB-11.
- The exact JOB-01 v0.2 generated test ZIP is not stored in GitHub.
- Production `job02.bridge.v1` and JOB-03 Store contract are incomplete.
- Most feature jobs have not submitted complete QA intake packets.
- No clean two-map phone/PC runtime evidence exists for the current platform candidate.
- The optional JOB-11 debug/log viewer remains intentionally deferred until platform and Store contracts are stable.

## Required next steps

1. Receive the exact candidate packages and dependency hashes.
2. Run the JOB-11 static package auditor on the full candidate set.
3. Resolve all FAIL and manual-review findings before runtime testing.
4. Complete the installed-package fingerprint checklist.
5. Have David test the exact candidate on West Coast USA and one non-West-Coast map.
6. Preserve logs, timestamps, screenshots, and completed failure/PASS reports.
7. Return failures to the owning job; JOB-11 must not patch another job's implementation.

## Migration impact statement

This manual transfer was not ordinary planned work. It was required because the project was unintentionally subject to the separate Work-chat usage limit, interrupting development and creating duplicate-work risk, loss-of-context risk, coordination problems, missing-attachment risk, and unnecessary delay. This record is preserved for the project audit and a report to OpenAI.
