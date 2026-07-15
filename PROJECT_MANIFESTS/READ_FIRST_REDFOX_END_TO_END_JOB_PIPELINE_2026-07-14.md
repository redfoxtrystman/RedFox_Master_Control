# READ FIRST — RedFox/FoxNet End-to-End Job Pipeline

**Date/time:** 2026-07-14 20:31 PDT / America/Los_Angeles  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** ACTIVE OWNER DIRECTIVE  
**Applies to:** JOB-00 through JOB-12

Every replacement regular chat must read this file before editing, packaging, or integrating anything.

## Core rule

Each feature job first proves its backend/gameplay through a development test UI such as WEUI. After the backend is stable, that same job connects the approved JOB-10 website to the proven backend. JOB-01 exposes the completed app through the same phone/PC destination, JOB-02 supplies shared Career/RLS actions, JOB-11 verifies it, and JOB-00 approves and assembles the final release.

## Backend-first WEUI/test-harness law

Each feature job should maintain a development-only WEUI, native debug panel, console command, or equivalent test harness when that makes the backend easier to test.

The test harness must:

1. expose the feature's real backend actions and state without requiring the website;
2. call the same backend service/functions the final website will call;
3. show useful errors, IDs, map/session state, and logs;
4. remain isolated from the production phone/PC website route;
5. never duplicate or replace the real backend logic;
6. never auto-open both the test UI and production UI;
7. be hideable, disabled, developer-only, or removed from the final public package;
8. remain available in a separate developer/test build when useful for future debugging.

A website must not be used to conceal an unproven backend. Backend testing comes first; website integration comes second.

## Mandatory A-to-R workflow

A. **Recover and claim** — Confirm exact JOB number/title, replace the inaccessible Work-chat owner with the regular-chat owner, and record recovery limits.  
B. **Intake** — Identify the newest source, ZIP, screenshots, logs, known-good behavior, pending candidate, and missing files.  
C. **Baseline** — JOB-00 freezes the exact compatible RLS/FoxNet baseline. No feature job selects a competing shared baseline.  
D. **Inspect** — Read source before editing; identify entry points, data flow, protected paths, and current failures.  
E. **Preserve** — Keep all David-tested working behavior unless testing proves it broken.  
F. **Separate backend from UI** — Put gameplay/data/services in reusable backend functions. WEUI and website must call those functions rather than each containing separate logic.  
G. **Build the test harness** — Add or preserve a development WEUI/native test panel capable of forcing backend actions and showing errors.  
H. **Prove backend behavior** — Test the feature without depending on the website. Record exact maps, actions, expected results, actual results, and logs.  
I. **Ownership map** — Publish exact files added/changed/removed and exact protected files left untouched.  
J. **Contracts** — Declare required JOB-01 platform version, JOB-02 bridge version, permissions, events, and dependencies.  
K. **Website integration** — Adapt the approved JOB-10 page to real data/actions. Remove fake visual controls wherever real behavior is required.  
L. **Phone/PC registration** — JOB-01 registers one canonical app/page ID and destination used by both phone and PC.  
M. **Shared Career/RLS wiring** — Use JOB-02 for approved shared money, shopping, ownership, inventory, garage/storage, insurance, and sell operations.  
N. **Static and package checks** — Validate source, ZIP structure, unique IDs, forbidden files, duplicate paths, contracts, and reports.  
O. **QA intake** — Submit the machine-readable handoff JSON and human-readable reports to JOB-11.  
P. **David runtime test** — David tests the exact ZIP and supplies result, map, steps, timestamp, and logs.  
Q. **Failure/integration gate** — JOB-11 identifies the failing layer; only the owning job fixes it. JOB-00 checks compatible versions and approves integration.  
R. **Final assembly/archive** — JOB-00 assembles or approves the combined release and records component hashes, test status, developer-UI disposition, and rollback points.

## Final ownership by job

### JOB-00 — Coordinator / Integration / Verification

Owns baseline freeze, ownership reconciliation, dependency order, integration approval, final assembly, collision checks, release manifest, rollback record, and project-wide audit trail. JOB-00 does not rewrite every feature.

### JOB-01 — Phone + PC Platform Core

Owns the shared IceFox front door, registry, canonical IDs/routes, phone launch entry, PC launch entry, browser/navigation host, responsive host data, deep-link adapters, and same-destination behavior. It does not own feature business logic.

### JOB-02 — Shared RLS / Career Bridge

Owns versioned shared UI-to-Lua contracts for current Career/RLS data and approved shared actions: money, shopping, purchase entry/result, ownership, inventory, garage/storage, insurance, selling, capability/error reporting, and shared logs. It does not own feature-specific Tow missions or page design.

### JOB-03 — RedFox App Store / Play Store

Owns optional install/enable/disable/open/update UI and app-manifest presentation after JOB-01 publishes the registry. It is not required for the first integrated milestone and may not create a competing launcher.

### JOB-04 — Scrap Yard / Wrecking Yard

Owns the Scrap Yard backend, development test harness, website/runtime integration, phone and PC behavior, online buy/sell behavior, map-independence repair, and real ownership/storage completion through JOB-02. Preserve the partially working phone purchase path. Do not use direct spawn as purchase success, fake inventory, or a startup Scrap Yard Career module.

### JOB-05 — BeamBook Marketplace

Owns BeamBook's real marketplace/social backend, development test harness, and approved BeamBook website integration. Preserve known working marketplace order of operations. Use JOB-02 for real Career/RLS transactions. Do not copy the platform core.

### JOB-06 — Import / Export Yard

Owns the Import/Export backend, test harness, website, and real vehicle-market runtime, initially buy-now behavior. Future export/delivery systems require owner approval.

### JOB-07 — Classics / Collector Exchange

Owns the Classics/Collector backend, test harness, website, and real collector/classic dealer runtime. No auction behavior unless David later authorizes it.

### JOB-08 — Insurance / Finance / Garage / Storage Pages

Owns the Vehicle Services backend adapters, test harness, pages, and approved runtime connections. It must not fake balances, loans, insurance, ownership, capacity, garage, or storage state.

### JOB-09 — Tow / Recovery / Dispatch

Owns Tow/Recovery backend/gameplay, WEUI test controls, dispatch/call chooser, tow missions, yard records, payments, multi-map support, and wiring the approved Recovery website to the proven mission system. WEUI may force calls for testing. Stabilize the newest gameplay candidate before website integration. Do not replace working Tow logic to fit a mockup.

### JOB-10 — Visual Design / Real Website Polish

Owns approved website HTML structure, CSS, responsive presentation, visual-only JavaScript, logos, images, cards, layouts, and design-system assets. JOB-10 hands approved page files to each feature owner. It does not implement gameplay or shared bridge behavior.

### JOB-11 — QA / Logging / Failure Triage

Owns automated/static handoff validation, ZIP/collision/forbidden-path checks, contract checks, test matrices, log expectations, failure evidence, regression/removal tests, and truth-status verdicts. It verifies the backend independently from the website, then verifies website-to-backend integration.

### JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

Owns those four apps' backend behavior, development test harnesses where useful, pages, and integration. It uses JOB-01 for registration and JOB-02 for approved shared messages/actions. It must not replace FoxFax or edit unrelated market/Tow systems.

## Minimum acceptance requirements for every feature mod

Every candidate must:

1. have one exact JOB owner, version, app/site ID, and canonical destination;
2. be an isolated add-on with unique paths and no copied platform/bridge core;
3. separate backend logic from WEUI/website presentation;
4. include a usable development test path for forcing and observing backend behavior where practical;
5. declare exact JOB-01/JOB-02 API versions, permissions, events, and dependencies;
6. use the same destination and backend contract from phone and PC;
7. avoid West Coast-only assumptions unless explicitly location-specific;
8. preserve proven working behavior and document intentional removals;
9. use real game/RLS/Career actions; placeholders cannot masquerade as functional controls;
10. include changed/protected files, ZIP size, SHA-256, logs, test instructions, limitations, and removal instructions;
11. state whether the development WEUI is retained, hidden, disabled, separately packaged, or removed for release;
12. pass static validation and JOB-11 intake before integration;
13. remain `BUILT — RUNTIME UNTESTED` until David tests the exact ZIP;
14. be rejected when required checks fail;
15. be independently removable without deleting or overwriting another job's files.

## Required package reports

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

## Current priority order

1. Finish regular-chat ownership migration.
2. JOB-00 freezes the shared baseline.
3. JOB-01/JOB-02 publish stable contracts.
4. Every feature job proves its backend through WEUI/test controls.
5. JOB-10 finishes and hands off approved pages.
6. Each feature job connects its own page to its proven backend.
7. JOB-01 registers it for the same phone/PC destination.
8. JOB-11 validates and David tests.
9. JOB-00 assembles the final release.
