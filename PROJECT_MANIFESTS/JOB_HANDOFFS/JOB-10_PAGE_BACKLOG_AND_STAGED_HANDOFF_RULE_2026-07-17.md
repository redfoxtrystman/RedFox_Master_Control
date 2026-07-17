# JOB-10 — Visual Design / Real Website Polish — Page Backlog and Staged Handoff Rule

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Visual owner:** JOB-10 — Visual Design / Real Website Polish  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** OWNER DIRECTION — PAGE HANDOFF MAY OCCUR IN STAGES

## Owner note

David remembers that additional pages still need to be added but cannot currently recall every page. The current website work must not be falsely called complete, but the entire integration effort also must not remain blocked until every future page is remembered.

## Staged-handoff rule

JOB-10 — Visual Design / Real Website Polish may hand off the visual system and completed page families in stages.

Every staged handoff must include:

```text
Visual package version
Design-system version
Complete page inventory
Page owner
Page status
Source entry file
Asset folders
Responsive state
Known missing controls
Runtime status
Next visual action
```

Allowed page status values:

```text
READY FOR FEATURE-OWNER ADAPTATION
NEEDS MINOR VISUAL WORK
PLACEHOLDER / VISUAL ONLY
DEFERRED
OWNER UNASSIGNED
REMEMBERED-LATER BACKLOG
```

A stage handoff does not mean every planned RedFox page exists. It means the listed pages and design system are preserved and available for feature owners without blocking remembered-later additions.

## Current known page inventory

### Assigned core pages

| Page family | Runtime owner |
|---|---|
| IceFox browser/home | JOB-01 — Phone + PC Platform Core |
| RedFox App Store / Play Store | JOB-03 — RedFox App Store / Play Store |
| Scrap Yard / Wrecking Yard | JOB-04 — Scrap Yard / Wrecking Yard |
| BeamBook | JOB-05 — BeamBook Marketplace |
| Import / Export Yard | JOB-06 — Import / Export Yard |
| Classics / Collector Exchange | JOB-07 — Classics / Collector Exchange |
| Insurance / Finance / Garage / Storage | JOB-08 — Insurance / Finance / Garage / Storage Pages |
| RedFox Recovery / Tow company website | JOB-09 — Tow / Recovery / Dispatch |
| SponsorHub / FoxMail / FoxText / Sponsor Rewards | JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards |

### Known visual or expansion pages with runtime ownership still needing confirmation

- FoxNet Auctions.
- FoxFax.
- Parts Exchange.
- UndergroundNet Black Market.
- Shadow DMV.
- Chop Shop.
- Most Wanted.
- High Risk Freight.
- Cold Storage.
- Additional UndergroundNet subpages.
- Any page David remembers later.

JOB-00 — Coordinator / Integration / Verification must assign a runtime owner before any unassigned page becomes functional. JOB-10 — Visual Design / Real Website Polish may continue to own its appearance while ownership is unresolved.

## Modularity requirement

Each page added later must be capable of becoming:

- its own isolated add-on; or
- a clearly owned page inside an existing feature add-on;
- one canonical registered destination;
- one responsive page used by phone and PC;
- connected to an approved backend contract;
- independently removable without deleting another page.

Adding a later page must not require replacing the entire IceFox phone, PC, browser, registry or every existing page.

## Before the first visual handoff

JOB-10 — Visual Design / Real Website Polish should:

1. inventory every current page and subpage;
2. mark each page with an allowed status;
3. identify missing pages and remembered-later placeholders;
4. preserve the current design system and common components;
5. identify which pages contain fake browser-only data/actions;
6. separate visual JavaScript from future backend calls;
7. verify all required CSS, JavaScript and assets are included;
8. avoid depending on a huge self-contained browser preview as the production BeamNG entry;
9. give each feature owner only the files it needs;
10. retain a complete visual master package for future page additions.

## Handoff does not equal BeamNG functionality

A visual page handoff means the feature owner can adapt the approved appearance. It does not prove:

- BeamNG page loading;
- phone/PC registration;
- Lua bridge communication;
- Career transactions;
- persistence;
- map independence;
- purchase, sale, mission or reward completion.

Those remain the responsibility of the runtime-owning job, JOB-01 — Phone + PC Platform Core, JOB-02 — Shared RLS / Career Bridge, JOB-11 — QA / Logging / Failure Triage and JOB-00 — Coordinator / Integration / Verification.

## Restart action

When David remembers another page, add it to this backlog with:

```text
Page name =
Legal / underground / shared =
Visual purpose =
Expected runtime behavior =
Proposed owner =
Priority =
Must exist before first integrated milestone = yes/no
Reference images/files =
```

Do not silently fold a new page into an unrelated job.
