# Owner Handoff — Website-to-Runtime Integration Ownership

**Date/time:** 2026-07-14 20:18 PDT / America/Los_Angeles  
**Issued by:** David / Captain through JOB-00 — Coordinator / Integration / Verification  
**Recorded by:** JOB-00 regular-chat takeover / Sol  
**Status:** ACTIVE COORDINATION DIRECTIVE

---

## Current owner-reported progress

David reports:

- the RedFox/FoxNet website presentation is approximately 80 percent complete, with minor visual and content adjustments remaining;
- Tow / Recovery / Dispatch already has functioning tow missions with few known bugs;
- one newer Tow / Recovery / Dispatch candidate still requires David's BeamNG test;
- after each feature's background/gameplay system is stable, the approved website must be connected to that feature mod and exposed through the shared IceFox phone/PC platform.

These are David-reported runtime observations. They are not independent JOB-00 runtime verification.

---

## Packages inspected for this directive

### JOB-10 visual package

```text
RedFox_JOB10_Full_Websites_v0_3_0(1).zip
Bytes: 50,819,666
SHA-256: b0f69fd1fa97d28a80882d784ad4fe37b91590b2375c60851dcf053a27d32970
```

Package status declared by its own reports:

```text
MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG
```

The package contains the shared visual website presentation, HTML/CSS/JavaScript, branding, images, page layouts, and static interaction demonstrations. It intentionally contains no BeamNG/RLS/Career runtime, phone, PC, route, bridge, mission, money, ownership, inventory, garage, storage, or insurance implementation.

### JOB-09 gameplay package

```text
19-RedFox_TowRecoveryDispatch_v0_2_0_CallChooserYard(2).zip
Bytes: 29,438
SHA-256: 217bc62ef0573feb888cf630c4d002fa49996a2fc0aa1cddc06a58e2720cc9ea
```

The package contains the Tow / Recovery / Dispatch gameplay extension, controls action, RedFox module manifest, call chooser, per-map tow-yard support, recovery calls, temporary yard records, Career payments, and testing documents. Its own verification report labels BeamNG runtime as untested in David's current installation. David reports that earlier/live tests are going well, but this exact candidate still requires testing.

---

## Ownership law: who makes websites work with mods

There is no single feature chat that should rewrite and connect every website. Integration is divided by ownership so one chat cannot break unrelated systems.

### 1. JOB-10 — Visual Design / Real Website Polish

JOB-10 owns the approved visual source:

- HTML structure;
- CSS and responsive presentation;
- JavaScript used only for visual interaction;
- logos, cards, images, page layout, and visual design system;
- approved phone-versus-PC presentation rules.

JOB-10 does **not** own gameplay wiring, Career/RLS actions, missions, purchases, storage, ownership, dispatch logic, or the shared platform bridge.

### 2. Each feature/app job wires its own website to its own runtime

The job that owns the feature must adapt the approved JOB-10 page into its isolated add-on mod and connect page actions to that job's real runtime through the published shared contracts.

| Website / feature | Runtime integration owner |
|---|---|
| Scrap Yard / Wrecking Yard | JOB-04 |
| BeamBook | JOB-05 |
| Import / Export Yard | JOB-06 |
| Classics / Collector Exchange | JOB-07 |
| Insurance / Finance / Garage / Storage | JOB-08 |
| Tow / Recovery / Dispatch | JOB-09 |
| SponsorHub / FoxMail / FoxText / Rewards | JOB-12 |

Therefore:

- JOB-05 must connect the approved BeamBook page to BeamBook's real backend behavior.
- JOB-09 must connect the approved Recovery/Towing website page to the Tow / Recovery / Dispatch gameplay extension.
- The same ownership rule applies to every other feature page.

Feature jobs must not redesign the approved page without coordination with JOB-10. JOB-10 must not invent or replace feature runtime logic.

### 3. JOB-01 — Phone + PC Platform Core

JOB-01 owns installing and exposing each completed app/page through:

- the shared IceFox app/page registry;
- canonical page IDs and destinations;
- phone and PC launch entries;
- route/navigation handling;
- responsive host information;
- shared platform events.

JOB-01 makes the integrated feature reachable from both phone and PC. It does not implement BeamBook business behavior or Tow mission logic.

### 4. JOB-02 — Shared RLS / Career Bridge

JOB-02 owns shared UI-to-BeamNG/RLS/Career messages and data/action contracts needed by multiple apps, including approved money, vehicle-shopping, ownership, inventory, garage/storage, and sell flows.

JOB-02 does not take ownership of app-specific Tow mission logic or BeamBook presentation. Feature jobs call the published bridge instead of creating competing shared bridges.

### 5. JOB-11 — QA / Logging / Failure Triage

JOB-11 verifies:

- package ownership boundaries;
- no duplicate platform/bridge files;
- static and integration contracts;
- expected logs;
- phone and PC behavior separately;
- exact BeamNG runtime results supplied by David.

JOB-11 reports failures to the owning job and does not silently fix another job's code.

### 6. JOB-00 — Coordinator / Integration / Verification

JOB-00 owns final coordination and assembly after each job submits a verified isolated package. JOB-00:

- selects the baseline;
- confirms dependency order;
- resolves ownership conflicts;
- approves integration;
- checks for duplicate paths and incompatible versions;
- assembles or approves the final combined release;
- does not personally rewrite every feature's website/runtime connection.

The final combined system is not assembled until the feature job, JOB-01, JOB-02 where applicable, and JOB-11 have completed their handoffs and David has tested required runtime behavior.

---

## Required workflow for every website/runtime pairing

1. David approves the relevant JOB-10 page visually.
2. The feature job identifies the exact page files and the exact runtime functions/messages it owns.
3. The feature job removes visual-only fake behavior where real game data/actions are required.
4. The feature job connects page controls to its own runtime and to JOB-02 only for approved shared Career/RLS operations.
5. JOB-01 registers the completed app/page and canonical destination for both phone and PC.
6. JOB-11 checks package boundaries, contracts, logs, phone, PC, and removal/regression behavior.
7. David tests the exact candidate in BeamNG.
8. JOB-00 approves it for final assembly.

---

## Immediate next pairings

### Tow / Recovery / Dispatch

Primary owner: `JOB-09`.

Inputs JOB-09 needs:

- latest David-tested or pending Tow / Recovery / Dispatch package;
- approved Recovery website files/page from the JOB-10 package;
- JOB-01 app registration and route contract;
- JOB-02 bridge contract only for shared Career/RLS operations that are not already safely owned inside JOB-09;
- David's test result and `beamng.log` for the exact candidate.

JOB-09 should first stabilize the pending gameplay candidate, then wire the Recovery webpage into the existing exported Tow/Recovery functions without replacing the working mission system.

### BeamBook

Primary owner: `JOB-05`.

Inputs JOB-05 needs:

- latest functional BeamBook backend/standalone package;
- approved BeamBook page files and assets from JOB-10;
- JOB-01 registration/route contract;
- JOB-02 bridge contract for real Career/RLS transactions and data;
- JOB-11 QA intake requirements.

JOB-05 should preserve the known working marketplace order of operations while replacing the temporary presentation with the approved BeamBook visual layer.

---

## Truth-status reminder

- JOB-10 websites remain `MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG` until connected by their owning feature jobs.
- The uploaded Tow v0.2.0 candidate remains `BUILT — RUNTIME UNTESTED` for this exact file until David tests it.
- David's earlier successful Tow mission observations must be preserved as user-reported evidence, but they do not automatically prove this exact ZIP.
