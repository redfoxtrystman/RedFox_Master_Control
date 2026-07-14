# RedFox/FoxNet Master Static and BeamNG Runtime Test Matrix v1

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 13:08 PDT (America/Los_Angeles)  
**Owner:** JOB-11 — QA / Logging / Failure Triage  
**Status:** PUBLISHED v1 — RUNTIME ROWS REQUIRE DAVID'S EXACT-CANDIDATE TESTS

## Verdict rules

```text
PASS — all required static and supplied runtime checks passed
FAIL/STOP — a required check failed; do not ship
BLOCKED — required contract, artifact, dependency, or evidence is missing
RUNTIME UNPROVEN — static checks passed but David has not proven runtime in BeamNG
```

A candidate cannot skip a failed earlier gate.

## Required test identity

Record before every run:

```text
Test ID:
Date/time/timezone:
Tester:
BeamNG version:
Game mode:
Career save identifier:
Map:
UI resolution:
UI scale/text scale:
Candidate ZIP name/size/SHA-256:
Baseline ZIP name/size/SHA-256:
Dependency ZIP names/sizes/SHA-256:
Enabled-mod fingerprint:
Git commit/branch:
Expected RedFox log prefixes:
```

## Gate 0 — ownership and intake

| ID | Check | Expected result | Failure owner |
|---|---|---|---|
| G0-01 | Exact JOB number/title is claimed | One active owner; no duplicate ownership | JOB-00 coordination |
| G0-02 | Candidate intake packet is complete | No blank fields; N/A fields explained | Candidate-owning job |
| G0-03 | Exact baseline and dependencies are named and hashed | Reproducible inputs | Candidate-owning job / JOB-00 |
| G0-04 | Files added/changed/removed are listed | Complete scope | Candidate-owning job |
| G0-05 | Protected files are named and confirmed untouched | Ownership boundaries preserved | Candidate-owning job |
| G0-06 | Known limitations and runtime-unproven items are explicit | No hidden gaps | Candidate-owning job |

Any failure blocks Gate 1.

## Gate 1 — static/package

| ID | Check | Expected result | Verdict on failure |
|---|---|---|---|
| G1-01 | ZIP opens and CRC test passes | No corrupt entry | FAIL/STOP |
| G1-02 | Exact ZIP SHA-256 matches handoff | Match | FAIL/STOP |
| G1-03 | Paths are safe | No absolute, drive, or `..` traversal paths | FAIL/STOP |
| G1-04 | ZIP contains no duplicate normalized paths | None | FAIL/STOP |
| G1-05 | Package top-level layout matches installation contract | One correct layout or documented exception | FAIL/STOP or BLOCKED |
| G1-06 | Required TXT/HTML/JSON/CSV/file-tree reports exist | All required reports | FAIL/STOP |
| G1-07 | No `__pycache__`, `.pyc`, temporary, or editor files | None | FAIL/STOP |
| G1-08 | No `redfoxScrapYardDirect` startup module or reference | None | FAIL/STOP |
| G1-09 | No unapproved startup `vehicleShopping` patch | None | FAIL/STOP |
| G1-10 | No copied phone/PC/browser/platform core in an app package | None unless package is JOB-01 platform | FAIL/STOP |
| G1-11 | No shared install-path collision across packages | None | FAIL/STOP |
| G1-12 | No duplicate app/site/route/module/window IDs | None | FAIL/STOP |
| G1-13 | HTML/CSS/JS/JSON/Lua touched by the job parses or passes available static checks | Pass | FAIL/STOP |
| G1-14 | File inventory matches ZIP contents and hashes | Match | FAIL/STOP |
| G1-15 | Removal manifest does not delete shared/other-job files | Safe scope | FAIL/STOP |
| G1-16 | Third-party/game assets are not publicly redistributed without permission | Cleared, excluded, or documented hold | BLOCKED |

The JOB-11 package auditor automates part of Gate 1. Manual ownership and contract review remains required.

## Gate 2 — contract/integration

| ID | Check | Expected result | Failure layer/owner |
|---|---|---|---|
| G2-01 | Required JOB-01 platform version matches | Compatible | PLATFORM/REGISTRY — JOB-01 or candidate job |
| G2-02 | Required JOB-02 bridge version matches | Same version on phone and PC | CAREER/RLS BRIDGE — JOB-02 or candidate job |
| G2-03 | JOB-03 manifest schema and permissions match | Valid | STORE — JOB-03 or candidate job |
| G2-04 | App registers without editing platform core | Registered through approved API | PLATFORM/REGISTRY |
| G2-05 | Phone and PC resolve the same canonical destination ID | Same destination/backend contract | PLATFORM/REGISTRY |
| G2-06 | Request/result payloads match published schema | Valid data | DATA/PAYLOAD |
| G2-07 | Request ID is preserved across UI/platform/bridge/result | Correlatable logs | SHARED EVENT API / BRIDGE |
| G2-08 | Unsupported capability returns a stable error | No crash or fake success | Owning contract job |
| G2-09 | Version mismatch fails safely and visibly | Stable error, no mutation | Owning contract job |
| G2-10 | Removing one app leaves platform and other apps intact | No shared-file deletion | Candidate-owning job |

Missing final contracts produce `BLOCKED`, not guessed PASS/FAIL assignment.

## Gate 3 — BeamNG runtime

Run the exact candidate with only one FoxNet/Web Ecosystem platform package enabled unless the approved architecture explicitly requires separate non-overlapping app packages.

### Startup and base regression

| ID | Test | Expected result |
|---|---|---|
| G3-01 | Launch BeamNG and load Career save | No new crash, freeze, or startup loop |
| G3-02 | Review logs from launch through map load | Required init checkpoints; no FATAL/uncaught RedFox error |
| G3-03 | Existing RLS phone opens | Existing phone authority preserved |
| G3-04 | Existing non-RedFox RLS apps still open | No platform regression |
| G3-05 | Existing PC/computer functions still open | Existing PC authority preserved |

### Phone and PC same-destination slice

| ID | Test | Expected result |
|---|---|---|
| G3-06 | Open IceFox from phone | Correct phone layout and canonical destination |
| G3-07 | Open IceFox from PC | Correct PC layout and same canonical destination ID |
| G3-08 | Compare route/data identifiers in logs | Same platform/bridge contract; layout may differ |
| G3-09 | Navigate back/forward/reopen | No dead route, duplicate window, or stale state |
| G3-10 | Close and reopen phone/PC | Clean lifecycle; no leaked duplicate registration |

### Map portability

| ID | Test | Expected result |
|---|---|---|
| G3-11 | Repeat phone/PC slice on West Coast USA | Pass |
| G3-12 | Repeat on one non-West-Coast map | Same registered destinations; no map-hardcoded failure |

### Negative and failure behavior

| ID | Test | Expected result |
|---|---|---|
| G3-13 | Open app with optional dependency disabled | Clear dependency error; no crash |
| G3-14 | Send invalid/unsupported action where test fixture allows | Stable validation error; no mutation |
| G3-15 | Trigger bridge timeout fixture where available | One timeout result; no infinite retry |
| G3-16 | Disable app and attempt open | Disabled state respected |
| G3-17 | Remove app and reopen platform | Platform and other apps remain intact |

### Feature-job transaction tests

Transaction-capable jobs must add job-specific rows covering validation, cancel, insufficient funds/capacity, authority call, success confirmation, save persistence, and rollback. Spawning a vehicle is not proof of purchase, ownership, storage, or garage insertion.

## Gate 4 — regression, update, and removal

| ID | Test | Expected result |
|---|---|---|
| G4-01 | Install over clean baseline | Correct registration and no collision |
| G4-02 | Update from prior candidate | State migration documented and safe |
| G4-03 | Disable and re-enable | State and registration recover correctly |
| G4-04 | Remove one feature app | Shared platform and other apps preserved |
| G4-05 | Remove RedFox platform add-on | RLS phone/PC and Career remain intact |
| G4-06 | Reinstall | No stale duplicate IDs or settings corruption |
| G4-07 | Repeat critical phone/PC/map tests | No regression |

## Required evidence per runtime row

- test ID and timestamp;
- expected and actual result;
- screenshot or recording when visible;
- relevant unfiltered log range;
- filtered RedFox/request-ID range;
- PASS, FAIL/STOP, BLOCKED, or RUNTIME UNPROVEN;
- first provable failing layer and owning job when failed.

## Current known project status

- JOB-01 v0.2 draft PR reports static checks passing; generated ZIP runtime untested and not committed.
- JOB-05 standalone v0.1.0 candidate is committed; runtime untested.
- No current candidate has a complete Gate 0 through Gate 4 JOB-11 record.

## Change record

**What changed:** Published the first complete shared Gate 0–4 test matrix covering ownership, package integrity, contracts, phone/PC same-destination behavior, two-map portability, negative cases, update/removal, and evidence requirements.  
**Why:** The prior Work chat defined high-level gates but did not commit the promised reusable master matrix before becoming inaccessible under the Work-chat usage limit.  
**Files affected:** `QA_LOGGING/MASTER_TEST_MATRIX_v1.md`.  
**Current status:** Static and runtime procedures are defined; no BeamNG runtime PASS has been issued.  
**Known problems:** Canonical baseline, exact test binaries, production bridge/Store contracts, and app-specific rows are incomplete.  
**Required next step:** Apply Gate 0 and Gate 1 to the first exact candidate, then have David execute Gate 3 on West Coast and a non-West-Coast map with logs and screenshots.

## Migration note

This matrix was reconstructed in the replacement regular chat after the original JOB-11 Work chat became inaccessible on July 14, 2026 until the displayed July 20, 2026 return date. It preserves the known rules without claiming recovery of chat-only test drafts.
