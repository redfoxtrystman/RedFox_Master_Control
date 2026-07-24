# RedFox Worker Chat Quick Start

This is the first file every RedFox worker chat must read.

David should not have to explain the whole system each time.

Repository:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control
```

---

## 1. Current owner directive — phone-only runtime target

Read this first:

```text
PROJECT_MANIFESTS/OWNER_PHONE_ONLY_ARCHITECTURE_DIRECTIVE_2026-07-23.md
```

Current architecture:

```text
ALL REDFOX / FOXNET RUNTIME PAGES TARGET THE IN-GAME PHONE ONLY.
PC / GARAGE-COMPUTER WEB HOSTING IS DEFERRED.
PC PARITY IS NOT A CURRENT RELEASE REQUIREMENT.
```

Do not spend current work cycles trying to make a feature page work on the Career/garage PC unless David explicitly reopens that requirement.

Earlier phone+PC documents remain historical references. Where they conflict with the phone-only directive, the phone-only directive controls.

Also read:

```text
PROJECT_MANIFESTS/OWNER_WEB_SYSTEM_RECOVERY_RETURN_CHECKLIST_2026-07-17.md
PROJECT_MANIFESTS/OWNER_DETAILED_ORDER_OF_OPERATIONS_2026-07-17.md
PROJECT_MANIFESTS/00_READ_FIRST_ALL_CHATS_CORE_UI_OVERRIDE_BAN_2026-07-22.md
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
```

---

## 2. Complete job names

Valid job IDs remain `JOB-00` through `JOB-12`. Do not rename or renumber them.

Always write the full number and title on first mention and in headings.

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

JOB-01 keeps its official title, but current scope is:

```text
PHONE PLATFORM CORE: ACTIVE
PC PLATFORM CORE: DEFERRED
```

JOB-11 — QA / Logging / Failure Triage remains parked/on-call until an exact candidate or failure is assigned.

---

## 3. Current phone host decision

The final phone host has not yet been frozen.

Two current directions must be compared:

1. the current RLS phone path used by the known phone-working Scrap Yard rollback;
2. the alternate phone mod David downloaded, which appears to work well and may include useful app-store behavior.

Do not copy or adopt the alternate phone until its exact filename, size, SHA-256, source, license, file tree, registration method, UI-to-Lua calls, persistence, startup overrides and removal behavior are recorded.

No feature job may create a competing phone shell.

---

## 4. Current JOB-04 — Scrap Yard / Wrecking Yard rollback

Active rollback candidate:

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
Size: 24,742,835 bytes
SHA-256: e6690693000c176d874f72abf3ffbe60d86815713a7ea65dbd0a1c84ece9fbb0
```

This is an exact copy of v0.1.4, where David confirmed:

```text
Scrap Yard opened
Buy flow opened
A Mustang was purchased
```

Known issues:

- phone page switching may take up to roughly 30 seconds;
- sell flow is unproven;
- the package contains inherited core UI files;
- it is a frozen rollback baseline, not permission for blind global-UI editing.

PC access is not part of its acceptance test.

---

## 5. Backend-first law remains mandatory

Every feature job must prove its backend independently before connecting the final phone page.

Use a development-only:

```text
WEUI
native debug panel
console command
forced-call/test control
or equivalent test harness
```

The test harness and final phone page must call the same backend service/functions.

Phone-only does not permit fake state. Use real BeamNG/RLS Career systems for money, ownership, inventory, garage/storage, purchase and sale behavior.

---

## 6. Who connects and assembles things

```text
JOB-10 — Visual Design / Real Website Polish creates/polishes mobile page presentation.
Each feature job connects its own phone page to its proven backend.
JOB-01 — Phone + PC Platform Core owns the approved phone host, route registry and lifecycle.
JOB-02 — Shared RLS / Career Bridge supplies approved shared Career/RLS data and actions.
JOB-03 — RedFox App Store / Play Store owns phone app catalog/install behavior after the phone host is selected.
JOB-11 — QA / Logging / Failure Triage validates packages, contracts, logs and regressions when activated.
JOB-00 — Coordinator / Integration / Verification approves dependencies and final assembly.
```

JOB-01 does not own feature business logic. JOB-10 does not implement gameplay. JOB-11 does not silently fix another job's code.

---

## 7. Website/page handoff rule

JOB-10 — Visual Design / Real Website Polish may hand off completed mobile pages in stages.

Each page must be marked:

```text
READY FOR FEATURE-OWNER ADAPTATION
NEEDS MINOR VISUAL WORK
PLACEHOLDER / VISUAL ONLY
DEFERRED
OWNER UNASSIGNED
REMEMBERED-LATER BACKLOG
```

Desktop mockups may be preserved as references, but desktop runtime adaptation is deferred and does not block a phone page.

---

## 8. Before editing

A chat must:

1. confirm its complete job number/title and active claim;
2. identify the newest source, ZIP, screenshots, logs and pending candidate;
3. inspect source before changing it;
4. list working behavior that must be preserved;
5. list exact files it may edit and protected files it must not touch;
6. identify the approved phone-host version and JOB-02 bridge version;
7. identify its backend test harness;
8. verify exact filename, archive byte size and SHA-256 from the file itself;
9. check for global UI and phone-layout overrides;
10. leave a written GitHub footprint.

No feature chat may select its own competing RLS or phone baseline.

---

## 9. Required work order

```text
CLAIM
→ INTAKE
→ VERIFY FILE IDENTITY AND LICENSE
→ INSPECT
→ PRESERVE KNOWN WORKING PHONE BEHAVIOR
→ SEPARATE BACKEND FROM UI
→ PROVE BACKEND
→ ADAPT APPROVED MOBILE PAGE
→ REGISTER ON APPROVED PHONE
→ TEST OPEN / CLOSE / BACK
→ TEST REAL DATA OR ACTION
→ TEST SECOND MAP WHERE RELEVANT
→ STATIC / PACKAGE CHECKS
→ JOB-11 — QA / LOGGING / FAILURE TRIAGE
→ DAVID TESTS EXACT ZIP
→ JOB-00 — COORDINATOR / INTEGRATION / VERIFICATION APPROVAL
```

Do not add PC parity steps unless David explicitly restores that requirement.

---

## 10. Core UI override stop condition

Normal feature jobs must not package or edit:

```text
ui/ui-vue/dist/index.js
```

or modify:

```text
lua/ge/extensions/ui/phone/layout.lua
```

without explicit JOB-01 — Phone + PC Platform Core and JOB-00 — Coordinator / Integration / Verification approval, an exact baseline diff, rollback instructions and a high-risk label.

The v0.1.6 Scrap Yard rollback is a grandfathered frozen exception because it is the exact known phone-buying build. It is not a template for new feature ZIPs.

---

## 11. Package and status requirements

Every build-producing chat must include the required handoff and verification records, including:

```text
REDFOX_JOB_HANDOFF.json
CHANGE_SCOPE_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.html
VERIFY_*.json
VERIFY_*_FILE_INVENTORY.csv
FILE_TREE_*.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
```

Allowed status language:

```text
DAVID-TESTED WORKING
BUILT — RUNTIME UNTESTED
PARTIAL
BLOCKED
FAILED — STOPPED
MOCKUP / PLACEHOLDER — NOT FUNCTIONAL
DEFERRED BY OWNER — NOT PART OF CURRENT RELEASE TARGET
```

Static checks are not BeamNG runtime proof.

---

## 12. Support and external lanes

### SUPPORT-01 — Cross-Map 3D Asset Conversion / Prefab / Placement

Issue:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/8
```

Owns model licensing/intake, conversion, materials, collisions, prefabs, cross-map placement and save/reload. JOB-04 retains all Scrap Yard business logic.

### SUPPORT-02 — Career Node Grabber / Developer Mode Compatibility

Issue:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/9
```

### PC Stability / Crash Monitor

Issue:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/6
```

The PC stability investigation remains active because machine reliability affects BeamNG testing. It is separate from the deferred FoxNet PC host.

---

## 13. Final rules

Do not rewrite working gameplay merely to add a phone page.

Do not make the phone page responsible for backend testing.

Do not copy the phone host, route registry, shared bridge or another app into a feature ZIP.

Do not hand-roll fake money, ownership, inventory, garage, storage, insurance or purchase success.

Do not install multiple FoxNet/phone integration ZIPs together during controlled tests.

Do not claim working, fixed, safe, complete or final until David tests the exact ZIP.
