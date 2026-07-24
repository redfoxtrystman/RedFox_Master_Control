# OWNER DIRECTIVE — PHONE-ONLY REDFOX / FOXNET ARCHITECTURE

**Date:** 2026-07-23  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** OWNER-APPROVED ARCHITECTURE CHANGE — EFFECTIVE IMMEDIATELY

## 1. Decision

David has ended the current requirement that RedFox/FoxNet pages must operate through both the BeamNG phone and the Career/garage PC.

The approved runtime target is now:

```text
REDFOX / FOXNET PAGES RUN ON THE IN-GAME PHONE ONLY
```

The PC host, PC browser, garage-computer parity, same-destination phone/PC acceptance test and PC-specific website integration are deferred indefinitely. They are not required for current feature completion or release.

This decision is based on repeated runtime roadblocks showing that the phone and PC hosting systems are materially different and that forcing parity is delaying working gameplay.

## 2. What remains unchanged

Phone-only does not mean fake or isolated gameplay state.

All feature pages must still:

- use real BeamNG/RLS Career money, ownership, inventory, garage/storage, purchase and sale behavior;
- use approved shared Lua/backend operations rather than inventing app-specific money or ownership;
- prove backend behavior before connecting the final page;
- avoid startup Career modules and automatic vehicle-shopping patches;
- work on supported maps without one-map assumptions;
- preserve exact archive identity, logs, rollback instructions and honest runtime labels;
- remain removable without damaging Career saves.

## 3. JOB-01 — Phone + PC Platform Core

The job number and complete title do not change.

Current approved scope:

```text
PHONE PLATFORM CORE: ACTIVE
PC PLATFORM CORE: DEFERRED
```

JOB-01 — Phone + PC Platform Core now owns:

- choosing and proving the phone shell/host;
- phone app/page registration;
- phone routing and lifecycle;
- open, close and back behavior;
- phone-safe asset paths;
- version/build diagnostics;
- compatibility with current RLS Career Overhaul;
- clean removal and duplicate-phone-package checks.

JOB-01 must not spend current cycles trying to restore PC parity unless David explicitly reopens that requirement.

The old JOB-01 phone+PC PR/source remains historical research. It is not the active release acceptance target.

## 4. JOB-02 — Shared RLS / Career Bridge

JOB-02 — Shared RLS / Career Bridge remains required.

Its contract is now optimized for one approved phone host, but it must still remain independent of any one website. Feature pages must call shared, versioned operations for real Career/RLS data and actions.

Start read-only, then add carefully verified mutations:

```text
Career/session status
Capabilities
Vehicle-shopping data
Owned vehicle list
Garage/storage state where supported
Open purchase flow
Confirm purchase outcome
Sell one explicitly selected owned vehicle
```

Opening a purchase screen is not purchase success. Spawning a vehicle is not purchase success.

## 5. JOB-03 — RedFox App Store / Play Store

JOB-03 — RedFox App Store / Play Store becomes phone-only.

It should inspect the newly downloaded alternate phone mod for:

- built-in app-store behavior;
- app discovery and registration;
- install/enable/disable/open/update/remove behavior;
- route and manifest format;
- persistence;
- RLS compatibility;
- licensing and redistribution permission;
- startup overrides, duplicate paths and clean removal.

Do not copy or adopt the alternate phone until its exact ZIP, size, SHA-256, file tree, license and runtime behavior are recorded.

## 6. JOB-04 — Scrap Yard / Wrecking Yard rollback baseline

The active rollback candidate is:

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
Size: 24,742,835 bytes
SHA-256: e6690693000c176d874f72abf3ffbe60d86815713a7ea65dbd0a1c84ece9fbb0
```

It is an exact byte-for-byte copy of the v0.1.4 build where David confirmed:

```text
Scrap Yard opened
Buy flow opened
A Mustang was purchased
```

Known limits:

- phone page switching may take approximately 30 seconds and may show white/grey waiting screens;
- sell flow is not yet proven;
- seller patience behavior is not a current blocker;
- the package contains inherited core UI files and must be treated as a frozen rollback baseline, not a template for blind editing.

Current acceptance target:

```text
PHONE SCRAP YARD BUYING WORKS RELIABLY
```

PC access is not required.

Next JOB-04 work must preserve the working phone buy path. Change one narrow file or behavior at a time, test it, and roll back immediately when the phone route or purchase flow regresses.

## 7. All feature jobs

The following pages are now phone-only runtime targets:

- JOB-04 — Scrap Yard / Wrecking Yard;
- JOB-05 — BeamBook Marketplace;
- JOB-06 — Import / Export Yard;
- JOB-07 — Classics / Collector Exchange;
- JOB-08 — Insurance / Finance / Garage / Storage Pages;
- JOB-09 — Tow / Recovery / Dispatch;
- JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards;
- all approved future FoxNet pages.

For every page:

```text
PROVE BACKEND
→ ADAPT APPROVED MOBILE PAGE
→ REGISTER ON APPROVED PHONE
→ TEST OPEN/CLOSE/BACK
→ TEST REAL DATA/ACTION
→ TEST SECOND MAP WHERE RELEVANT
→ JOB-11 QA
→ DAVID TESTS EXACT ZIP
→ JOB-00 APPROVAL
```

No feature job may create its own competing phone shell.

## 8. JOB-10 — Visual Design / Real Website Polish

JOB-10 — Visual Design / Real Website Polish should prioritize mobile/phone layouts.

Desktop mockups may be preserved as design references, but desktop/PC runtime adaptation is deferred. A page is not blocked merely because it lacks a working PC version.

Remembered-later pages remain valid backlog items and can be added later as separate phone destinations.

## 9. Alternate phone mod intake

David has downloaded another phone mod that appears to work well. It may become the new RedFox/FoxNet host, but no decision is final until intake is complete.

Required intake record:

```text
Exact filename
Archive byte size
SHA-256
Source and creator
License / redistribution permission
BeamNG and RLS versions tested
File tree
Phone framework
App/route registry
Built-in app-store behavior
UI-to-Lua calls
Persistence
Startup extensions/overrides
Stock/RLS files replaced
Duplicate-path risks
Removal behavior
Known runtime result
```

Comparison candidates:

1. current RLS phone path used by the v0.1.6 Scrap Yard rollback;
2. the newly downloaded alternate phone;
3. any other phone mod David supplies.

Selection criteria:

- stable Career loading;
- reliable app opening;
- simple page registration;
- no dangerous global override when avoidable;
- clean removal;
- ability to host all RedFox pages;
- compatibility with real RLS Career actions;
- acceptable license/reuse terms.

Do not move all pages to the alternate phone until one minimal RedFox page and one real backend call work there.

## 10. PC-related records

Existing PC architecture work is preserved as historical/deferred research. It is not deleted.

Do not report the PC system as failed forever or impossible. Report it as:

```text
DEFERRED BY OWNER — NOT PART OF CURRENT RELEASE TARGET
```

The separate PC Stability / Crash Monitor investigation remains active because computer stability affects BeamNG testing even though FoxNet pages are phone-only.

## 11. Core UI safety

The project-wide core UI override warning remains in force.

The v0.1.6 rollback contains inherited core UI files because it is the exact known phone-buying baseline. This is a narrow grandfathered rollback exception, not general approval for feature jobs to package or rewrite global UI bundles.

Any future change involving:

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
```

must be explicitly disclosed, diffed against the exact baseline and tested as a high-risk phone-platform change under JOB-01 — Phone + PC Platform Core and JOB-00 — Coordinator / Integration / Verification.

## 12. Immediate work order

```text
1. Preserve v0.1.6 unchanged as the known phone-buying rollback.
2. Record and inspect the newly downloaded alternate phone mod.
3. Test v0.1.6 phone buy flow again with only RLS and the rollback ZIP installed.
4. Capture phone load time, page-switch time, purchase result and logs.
5. Do not test or repair PC access.
6. Choose the phone host only after the alternate-phone inspection and minimal proof.
7. Stabilize one phone host and one shared bridge contract.
8. Connect Scrap Yard first.
9. Repeat the phone-only pattern for the remaining pages.
```

## 13. Superseded requirements

This directive supersedes all earlier requirements that currently demand:

- one identical phone and PC destination;
- a working Career/garage PC host before feature completion;
- PC and phone parity as a release gate;
- PC-specific page adaptation before phone release.

Earlier documents remain useful history, but where they conflict with this directive, this directive controls.
