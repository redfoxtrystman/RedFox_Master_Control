# RedFox Worker Chat Quick Start

This is the first file every RedFox worker chat must read.

David should not have to explain the whole system each time.

Repository:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control
```

---

## 1. Confirm the exact job

For the FoxNet rebuild, valid job IDs are:

```text
JOB-00 through JOB-12
```

Do not rename, renumber, merge, or silently change the assigned job.

The authoritative job map and complete A-to-R workflow are here:

```text
PROJECT_MANIFESTS/READ_FIRST_REDFOX_END_TO_END_JOB_PIPELINE_2026-07-14.md
PROJECT_MANIFESTS/REDFOX_JOB_PIPELINE_MANIFEST.json
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
```

A replacement regular chat must also update its exact GitHub claim and document what could not be recovered from the inaccessible Work chat.

---

## 2. Current job map

| Job | Role |
|---|---|
| JOB-00 | Coordinator / Integration / Verification |
| JOB-01 | Phone + PC Platform Core |
| JOB-02 | Shared RLS / Career Bridge |
| JOB-03 | RedFox App Store / Play Store |
| JOB-04 | Scrap Yard / Wrecking Yard |
| JOB-05 | BeamBook Marketplace |
| JOB-06 | Import / Export Yard |
| JOB-07 | Classics / Collector Exchange |
| JOB-08 | Insurance / Finance / Garage / Storage Pages |
| JOB-09 | Tow / Recovery / Dispatch |
| JOB-10 | Visual Design / Real Website Polish |
| JOB-11 | QA / Logging / Failure Triage |
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards |

If the chat's assignment does not match one exact row, stop implementation and report the mismatch to JOB-00.

---

## 3. Backend-first law

Every feature job must prove its backend independently before connecting the website.

Use a development-only:

```text
WEUI
native debug panel
console command
forced-call/test control
or equivalent test harness
```

The test harness and final website must call the same backend service/functions.

The test harness must not duplicate the gameplay logic, auto-open beside the production UI, or become a competing production system. For final release it must be retained developer-only, hidden, disabled, moved into a separate test package, or removed—with the disposition recorded.

The website is connected only after the backend can be forced, observed, logged, and tested without fighting the website.

---

## 4. Who connects and assembles things

```text
JOB-10 creates/polishes the approved website presentation.
Each feature JOB connects its own website to its own proven backend.
JOB-01 registers one canonical destination for both phone and PC.
JOB-02 supplies approved shared Career/RLS data and actions.
JOB-11 validates packages, contracts, logs, runtime evidence, and regressions.
JOB-00 approves dependencies and assembles the final combined release.
```

JOB-00 does not rewrite every feature. JOB-10 does not implement gameplay. JOB-01 does not own feature business logic. JOB-11 does not silently fix another job's code.

---

## 5. Before editing

A chat must:

1. confirm its exact JOB number/title and active regular-chat claim;
2. identify the newest source, ZIP, screenshots, logs, and pending test candidate;
3. inspect source before changing it;
4. list working behavior that must be preserved;
5. list exact files it may edit and protected files it must not touch;
6. identify required JOB-01/JOB-02 contract versions;
7. identify its backend test harness and how the website will call the same backend;
8. leave a written GitHub footprint.

No feature chat may select a competing shared FoxNet/RLS baseline. JOB-00 freezes the shared baseline.

---

## 6. Required work order

```text
CLAIM
→ INTAKE
→ INSPECT
→ SEPARATE BACKEND FROM UI
→ BUILD/PRESERVE WEUI TEST HARNESS
→ PROVE BACKEND
→ CONNECT APPROVED WEBSITE
→ REGISTER SAME PHONE/PC DESTINATION
→ STATIC/PACKAGE CHECKS
→ JOB-11 QA
→ DAVID TESTS EXACT ZIP
→ JOB-00 INTEGRATION APPROVAL
→ FINAL ASSEMBLY
```

Do not skip directly from visual mockup to final integration.

---

## 7. Required machine-readable handoff

Every build-producing chat must copy and complete:

```text
PROJECT_MANIFESTS/TEMPLATES/REDFOX_JOB_HANDOFF_TEMPLATE.json
```

The completed candidate must include:

```text
REDFOX_JOB_HANDOFF.json
```

The GitHub validator checks:

```text
QA_LOGGING/validate_redfox_handoffs.py
.github/workflows/redfox-handoff-validation.yml
```

A failed automated check is a stop condition, not permission to ship a mostly complete package.

---

## 8. Required package reports

```text
CHANGE_SCOPE_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.html
VERIFY_*.json
VERIFY_*_FILE_INVENTORY.csv
FILE_TREE_*.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
REDFOX_JOB_HANDOFF.json
```

Static verification is not BeamNG runtime verification.

---

## 9. Allowed status language

```text
DAVID-TESTED WORKING
BUILT — RUNTIME UNTESTED
PARTIAL
BLOCKED
FAILED — STOPPED
MOCKUP / PLACEHOLDER — NOT FUNCTIONAL
```

Do not say working, fixed, done, safe, or final unless the allowed status actually applies.

---

## 10. Written footprint

Each chat must update GitHub directly or return a block for JOB-00 to post:

```text
Timestamp =
Job ID and exact title =
Regular-chat owner =
Message type = CHECK-IN / STATUS / HANDOFF / RESULT / BLOCKED
Status =
Source/candidate inspected =
Files changed =
Files protected =
Backend test harness =
Backend test result =
Website integration status =
JOB-01 platform version =
JOB-02 bridge version =
What David must test =
Known problems =
Next action =
Coordinator action needed = yes/no
```

Reading without leaving a footprint is failed coordination.

---

## 11. Final rules

Do not rewrite working gameplay merely to add a website.

Do not make the website responsible for backend testing.

Do not auto-open both development WEUI and production UI.

Do not copy phone, PC, browser, registry, bridge, or another app's files into a feature mod.

Do not hand-roll fake money, ownership, inventory, garage, storage, insurance, or purchase success.

Do not claim runtime success without David testing the exact ZIP.
