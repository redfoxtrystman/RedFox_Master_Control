# RedFox Worker Chat Quick Start

This is the first file every RedFox worker chat must read.

David should not have to explain the whole system each time.

Repository:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control
```

---

## 1. Read the owner-level documents first

For the FoxNet rebuild, read these before implementation:

```text
PROJECT_MANIFESTS/OWNER_DETAILED_ORDER_OF_OPERATIONS_2026-07-17.md
PROJECT_MANIFESTS/READ_FIRST_REDFOX_END_TO_END_JOB_PIPELINE_2026-07-14.md
PROJECT_MANIFESTS/REDFOX_JOB_PIPELINE_MANIFEST.json
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
```

The owner order document is the current detailed sequence. Follow it unless new test evidence or David changes the priority. Any change must be written to GitHub with the reason and restart point.

Archive identity warning:

```text
PROJECT_MANIFESTS/OWNER_ARCHIVE_IDENTITY_SIZE_HASH_CORRECTION_REQUIRED_2026-07-17.md
```

The shared RLS archive currently has contradictory byte-size records attached to the same SHA-256. Do not copy either size as authoritative until the exact archive is measured and hashed again.

A replacement regular chat must update its exact GitHub claim and document what could not be recovered from the inaccessible Work chat.

---

## 2. Confirm and write the complete job name

Valid job IDs are `JOB-00` through `JOB-12`.

Do not rename, renumber, merge, or silently change the assigned job.

Always write the full number and title on first mention and in headings. Do not use only a bare number when the complete title is known.

| Job | Complete title |
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

If the assignment does not match one exact row, stop implementation and report the mismatch to JOB-00 — Coordinator / Integration / Verification.

JOB-11 — QA / Logging / Failure Triage is currently parked/on-call until David assigns an exact candidate, failure investigation or QA task. It did not miss the camping sound-off request.

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

The test harness must not duplicate gameplay logic, auto-open beside the production UI, or become a competing production system. For final release it must be retained developer-only, hidden, disabled, moved into a separate test package, or removed—with the disposition recorded.

The website is connected only after the backend can be forced, observed, logged and tested without fighting the website.

---

## 4. Who connects and assembles things

```text
JOB-10 — Visual Design / Real Website Polish creates/polishes approved website presentation.
Each feature job connects its own website to its own proven backend.
JOB-01 — Phone + PC Platform Core registers one canonical destination for phone and PC.
JOB-02 — Shared RLS / Career Bridge supplies approved shared Career/RLS data and actions.
JOB-11 — QA / Logging / Failure Triage validates packages, contracts, logs and regressions when activated.
JOB-00 — Coordinator / Integration / Verification approves dependencies and assembles the final combined release.
```

JOB-00 — Coordinator / Integration / Verification does not rewrite every feature. JOB-10 — Visual Design / Real Website Polish does not implement gameplay. JOB-01 — Phone + PC Platform Core does not own feature business logic. JOB-11 — QA / Logging / Failure Triage does not silently fix another job's code.

---

## 5. Website staged-handoff rule

David remembers that additional pages still need to be added but cannot currently recall every page.

Read:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-10_PAGE_BACKLOG_AND_STAGED_HANDOFF_RULE_2026-07-17.md
```

JOB-10 — Visual Design / Real Website Polish may hand off completed pages and the design system in stages. Each page must be inventoried and marked:

```text
READY FOR FEATURE-OWNER ADAPTATION
NEEDS MINOR VISUAL WORK
PLACEHOLDER / VISUAL ONLY
DEFERRED
OWNER UNASSIGNED
REMEMBERED-LATER BACKLOG
```

Remembered-later pages can be added as separate registered destinations. They must not require rebuilding every finished app or replacing the phone/PC platform.

---

## 6. Before editing

A chat must:

1. confirm its exact full job number/title and active regular-chat claim;
2. identify the newest source, ZIP, screenshots, logs and pending test candidate;
3. inspect source before changing it;
4. list working behavior that must be preserved;
5. list exact files it may edit and protected files it must not touch;
6. identify required JOB-01 — Phone + PC Platform Core and JOB-02 — Shared RLS / Career Bridge contract versions;
7. identify its backend test harness and how the website will call the same backend;
8. verify exact archive filename, byte size and SHA-256 from the file itself;
9. leave a written GitHub footprint.

No feature chat may select a competing shared FoxNet/RLS baseline. JOB-00 — Coordinator / Integration / Verification freezes the shared baseline.

---

## 7. Required work order

```text
CLAIM
→ INTAKE
→ VERIFY FILE IDENTITY
→ INSPECT
→ SEPARATE BACKEND FROM UI
→ BUILD/PRESERVE WEUI TEST HARNESS
→ PROVE BACKEND
→ CONNECT APPROVED WEBSITE
→ REGISTER SAME PHONE/PC DESTINATION
→ STATIC/PACKAGE CHECKS
→ JOB-11 — QA / LOGGING / FAILURE TRIAGE
→ DAVID TESTS EXACT ZIP
→ JOB-00 — COORDINATOR / INTEGRATION / VERIFICATION APPROVAL
→ FINAL ASSEMBLY
```

Do not skip directly from visual mockup to final integration.

---

## 8. Required machine-readable handoff

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

## 9. Required package reports

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

## 10. Allowed status language

```text
DAVID-TESTED WORKING
BUILT — RUNTIME UNTESTED
PARTIAL
BLOCKED
FAILED — STOPPED
MOCKUP / PLACEHOLDER — NOT FUNCTIONAL
```

Do not say working, fixed, done, safe or final unless the allowed status actually applies.

---

## 11. Written footprint

Each chat must update GitHub directly or return a block for JOB-00 — Coordinator / Integration / Verification to post:

```text
Timestamp =
Full job ID and title =
Regular-chat owner =
Message type = CHECK-IN / STATUS / HANDOFF / RESULT / BLOCKED
Status =
Source/candidate inspected =
Exact archive size and SHA-256 =
Files changed =
Files protected =
Backend test harness =
Backend test result =
Website integration status =
JOB-01 — Phone + PC Platform Core version =
JOB-02 — Shared RLS / Career Bridge version =
What David must test =
Known problems =
Next action =
Coordinator action needed = yes/no
```

Reading without leaving a footprint is failed coordination.

---

## 12. PC stability/crash-monitor chats

The PC crash investigation is external to the BeamNG job map but affects test reliability.

Every PC diagnostic chat must post to:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/6
```

Permanent sanitized records belong under:

```text
PC_STABILITY/
```

Read:

```text
PC_STABILITY/README.md
```

Do not mix PC diagnostic applications, raw dumps or private machine data into BeamNG feature packages.

---

## 13. JOB-04 — Scrap Yard / Wrecking Yard expansion records

The immediate priority remains proving the current backend.

Long-term player-owned yard direction:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_PLAYER_OWNED_SCRAP_WRECKING_YARD_EXPANSION_DIRECTIVE_2026-07-17.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_PLAYER_OWNED_YARD_IMPLEMENTATION_APPENDIX_2026-07-17.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_PHYSICAL_YARD_MODEL_AND_BUILD_PLACEMENT_PLAN_2026-07-17.md
```

The physical yard may begin as scenery placed on a flat location on any map. Model placement and save/load must be proven before connecting the business economy.

---

## 14. Final rules

Do not rewrite working gameplay merely to add a website.

Do not make the website responsible for backend testing.

Do not auto-open both development WEUI and production UI.

Do not copy phone, PC, browser, registry, bridge or another app's files into a feature mod.

Do not hand-roll fake money, ownership, inventory, garage, storage, insurance or purchase success.

Do not pair a SHA-256 with an extracted-size or rounded display-size measurement.

Do not claim runtime success without David testing the exact ZIP.
