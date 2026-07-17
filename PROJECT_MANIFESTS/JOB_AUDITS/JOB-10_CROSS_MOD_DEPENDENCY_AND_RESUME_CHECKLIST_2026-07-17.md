# JOB-10 Cross-Mod Dependency and Resume Checklist

**Date:** 2026-07-17  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Status:** PAUSED FOR CAMPING — NOT A HANDOFF

This file is the compact operational companion to:

```text
PROJECT_MANIFESTS/JOB_AUDITS/JOB-10_CAMPING_PAUSE_FULL_AUDIT_2026-07-17.md
```

The full audit contains the complete history and page-by-page state. This file tells every job exactly what JOB-10 needs before integration and what David should do first when he returns.

---

# Current baseline

```text
Package: RedFox_JOB10_Full_Websites_v0_3_1.zip
SHA-256: 0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
Status: MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG
```

Current browser pages:

```text
IceFox home
BeamBook
FoxNet Auctions
FoxFax
XXX Insurance
Collector Exchange
Parts Exchange
Export Yard
Tow / Recovery
Scrap Yard / Wrecking Yard
UndergroundNet
404/error page
Rotating ad slots
```

Pages still to add visually:

```text
SponsorHub
FoxMail
FoxText
Sponsor Rewards
Lore & History / Wiki Browser
```

---

# Hard freeze rules during pause

1. Do not transfer JOB-10 ownership.
2. Do not replace the v0.3.1 visual baseline.
3. Do not create a second competing design system.
4. Do not edit JOB-10 pages inside integrated runtime files without a written presentation-only boundary.
5. Do not claim runtime success for any JOB-10 page.
6. Do not turn Lore browser into unrestricted YouTube/general browsing for the first release.
7. Do not copy protected third-party BeamBook code or real-site branding/art.
8. Do not add West Coast-only assumptions.
9. Do not remove rotating ad locations.
10. Do not use stock/fake vehicle photography in final runtime inventory.

---

# Required handoff package from every behavior job

Before JOB-10 edits a runtime page, the owning job must provide:

```text
1. Exact canonical route/page ID
2. Exact current source files
3. Exact files JOB-10 may edit
4. Exact protected files/sections
5. Data schema with sample payload
6. Action/event names
7. Loading/empty/error/success states
8. Phone and PC container dimensions
9. Current runtime status
10. Exact test ZIP and hash if one exists
11. Known failures/limitations
12. Log prefixes and expected events
```

No vague “make it look good” handoff is sufficient once runtime integration starts.

---

# JOB-by-JOB dependency checklist

## JOB-00 — Coordinator / Integration / Verification

Needed from JOB-00:

- approve page integration order;
- confirm which job owns each behavior;
- approve external Lore/RLS domains;
- approve final combined release;
- stop duplicate/competing page rewrites.

JOB-10 deliverable to JOB-00:

- visual file manifest;
- before/after screenshots;
- scope verification;
- current package hash;
- page-by-page runtime status.

## JOB-01 — Phone + PC Platform Core

Needed from JOB-01:

- route registry contract;
- shared browser content container;
- phone and PC target sizes;
- same-destination proof;
- theme host behavior;
- safe Back/Home/Reload/Close behavior;
- minimal external webpage proof for Lore browser;
- presentation-only boundaries.

JOB-10 must not:

- replace phone shell;
- replace PC shell;
- duplicate browser core;
- invent separate PC routes.

## JOB-02 — Shared RLS / Career Bridge

Needed from JOB-02:

- final approved bridge messages;
- data/action schemas for pages that require Career/RLS;
- approval of sponsor/mail/text messages;
- proof no custom fake money/ownership/storage system is being used.

JOB-10 must not:

- alter bridge payloads;
- invent message names;
- call Career/RLS functions directly from presentation without owner approval.

## JOB-04 — Scrap Yard / Wrecking Yard

Needed from JOB-04:

- legal yard inventory;
- owned vehicle list;
- full-car-sale action/result;
- hire-yard/keep-parts action/result;
- self-process/shell-sale action/result;
- labor and parts-return data;
- legal parts inventory output;
- market/demand data when available.

Visual rules to preserve:

- full car sale returns no parts and pays less;
- hire yard returns parts but charges labor;
- self-process keeps parts and sells shell/scrap;
- yard also sells wrecked/salvage/cheap vehicles.

## JOB-05 — BeamBook Marketplace

Needed from JOB-05:

- stable feed schema;
- profile/contact schema;
- Marketplace listing schema;
- real game thumbnail source;
- seller/listing open-close actions;
- refresh/re-entry behavior;
- exact safe page files.

Visual rules to preserve:

- Facebook-like layout;
- feed stays stable while open;
- different content may load on re-entry/manual refresh;
- real faces and BeamNG-related posts;
- real in-game vehicles at runtime.

## JOB-06 — Import / Export Yard

Needed from JOB-06:

- shipment/quote/tracking schemas;
- port/mission state;
- container data;
- mystery-container action/result if approved;
- exact safe files.

Visual rules to preserve:

- ocean, ship, container and freight identity;
- all-map website access;
- mystery containers as abandoned/unclaimed freight;
- $2,000–$25,000 concept range remains design guidance, not final economy tuning.

## JOB-07 — Classics / Collector Exchange

Needed from JOB-07:

- premium inventory schema;
- auction/sale actions;
- collector vehicle metadata;
- current safe files.

Visual rules to preserve:

- premium collector-auction identity;
- dark/luxury appearance;
- real rare vehicle imagery/data.

## JOB-08 — Insurance / Finance / Garage / Storage

Needed from JOB-08:

- garage/owned-vehicle schema for FoxFax;
- insurance quote/action schemas;
- property/business/storage state;
- exact safe files.

Visual rules to preserve:

- black/hot-pink/lace insurance identity;
- working dropdown-style quote form;
- FoxFax vehicle selection from actual owned garages.

## JOB-09 — Tow / Recovery / Dispatch

Needed from JOB-09 when active:

- service/job schema;
- company rename state;
- lockout/tow/recovery/transport actions;
- tow-yard/delivery integration;
- exact safe files.

Visual rules to preserve:

- real towing-company website;
- tow truck/wreck/recovery imagery;
- local tow, lockout, winch, collision, heavy recovery, roadside and transport services.

## JOB-11 — QA / Logging / Failure Triage

Needed from JOB-11:

- viewport matrix;
- visual regression checklist;
- route/action smoke tests;
- console/log checks;
- all-map checks;
- external Lore page blocked/offline tests;
- duplicate ZIP detection.

## JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

Needed from JOB-12:

- proven UI-to-Lua call;
- proven Lua-to-UI return;
- sponsor/application/offer/contract schemas;
- XP/reputation/points schemas;
- FoxMail schema;
- FoxText schema;
- rewards schema;
- persistence/payment/assigned-vehicle behavior;
- exact safe visual files.

Do not integrate the failed v0.5.0/v0.5.1 runtime event pattern.

---

# Lore & History browser checklist

Initial visual/content plan:

```text
Vehicle Manufacturers
Vehicle Models
Company History
Years and Generations
Levels and Locations
Trailers and Equipment
Motorsport and Special Configurations
Game Updates
Official RLS guides/pages
Community Lore later
```

First-release domain approach:

```text
Allowlisted official BeamNG sites
Allowlisted official RLS sites after exact URLs are confirmed
Community wiki only after owner approval
```

Required proof before a full page:

1. Load one official page inside BeamNG.
2. Confirm it is not blocked by frame/security rules.
3. Confirm Back/Home/Reload/Close.
4. Confirm return to local RedFox pages.
5. Confirm offline/blocked error page.
6. Confirm phone and PC route parity.
7. Confirm no downloads/pop-ups/general browsing in first release.

Fallback order:

1. Open inside IceFox if allowed.
2. Open externally if embedding is blocked.
3. Show local curated link/index page without scraping full articles.

---

# Exact resume sequence for David

When David returns:

```text
1. Return to the same JOB-10 chat.
2. Re-download/open RedFox_JOB10_Full_Websites_v0_3_1.zip.
3. Verify START_HERE.html still opens correctly.
4. Review the current pages once more.
5. List any final visual changes.
6. Add SponsorHub.
7. Add FoxMail.
8. Add FoxText.
9. Add Sponsor Rewards.
10. Add Lore & History landing page.
11. Freeze the expanded browser prototype.
12. Collect stable handoffs from behavior jobs.
13. Integrate one page at a time.
14. Test PC and phone.
15. Test all maps.
16. Have JOB-11 run regression/log checks.
17. Have JOB-00 approve combined release.
```

---

# Resume success criteria

JOB-10 is ready for controlled integration only when:

- David approves the visual page;
- the behavior owner supplies stable files/contracts;
- JOB-01 supplies the shared route/container;
- JOB-02 approves required messages;
- JOB-10 publishes an exact edit manifest;
- JOB-11 has a test plan;
- JOB-00 approves the integration step.

Final runtime success is not achieved until David tests the exact BeamNG ZIP.
