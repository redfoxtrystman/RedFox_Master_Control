# JOB-10 Visual Websites v0.3.1 + JOB-12 Sponsor Coordination

**Date:** 2026-07-14  
**Owner:** David / Captain  
**JOB-10 owner:** Visual Design / Real Website Polish regular-chat takeover / Sol  
**Status:** MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG

## Current approved browser-design checkpoint

David reviewed the standalone JOB-10 browser website package through v0.3.1 and stated that the project is at a good place and close to beginning BeamNG integration.

Current package:

```text
RedFox_JOB10_Full_Websites_v0_3_1.zip
```

SHA-256:

```text
0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
```

This package remains a standalone offline-browser prototype. It does not contain or prove BeamNG, RLS, Career, phone, PC, bridge, money, ownership, inventory, garage, storage, insurance, purchase, mission, sponsor, or messaging runtime integration.

## Current visual direction approved by David

The websites must look like believable real-world company/service websites rather than game or mod menus. The current design direction is approved enough to freeze broad styling and move toward page-specific coordination.

Current page families include:

```text
IceFox browser front page
BeamBook social feed and Marketplace
FoxNet Auctions
FoxFax
XXX Insurance
Collector Exchange
Parts Exchange
Export Yard
Tow / Recovery company site
Scrap Yard / Wrecking Yard
UndergroundNet
```

Key rules already established:

- same canonical destinations on phone and PC;
- responsive presentation only, not separate business logic;
- all pages must be usable on every map;
- no West Coast-only assumptions;
- real in-game vehicle/configuration images at runtime;
- rotating humorous advertisement slots must remain available;
- BeamBook content changes when the user re-enters or manually refreshes, not continuously every few seconds;
- FoxNet Auctions should carry roughly 90–110 active vehicles, with the exact total and category mix varying by in-game day;
- Scrap Yard is also a Wrecking Yard and may sell legal wrecked, salvage-title, parts, rough-running, and occasional good-value vehicles;
- UndergroundNet stolen vehicles do not receive FoxFax reports and require expensive Shadow DMV legalization;
- stolen serialized powertrain/body parts remain on the underground market unless a future approved whitelist identifies unmarked legal-safe parts.

## New visual page requirement: SponsorHub

David requested that JOB-10 add a SponsorHub website/page family after checking the GitHub JOB-12 definition.

JOB-12 owns all sponsor-system behavior, state, persistence, contracts, payments/rewards, FoxMail, and FoxText. JOB-10 owns presentation only.

The SponsorHub visual design should support the following data/states when JOB-12 provides a stable handoff:

```text
Sponsor directory
Sponsor/company profiles
Applications/subscriptions
Pending applications
Sponsor offers
Accept / decline contract presentation
Active contracts
Sponsor status and tier
Sponsor XP
Reputation
Sponsor Points
Assigned sponsor vehicles
Optional sponsor decal/honor status
Reward catalog
Claimable and claimed rewards
Pending-wallet display supplied by JOB-12/JOB-02
Recent FoxMail notices
Recent FoxText alerts
```

The first JOB-12 test concept used the BeamNG GmbH Community Driver Test Program. That can remain a featured first sponsor in the visual prototype, but JOB-10 must not implement automatic approval, persistence, points, deposits, or reward logic.

## Related pages likely intended by David

The project board defines the complete JOB-12 page/app family as:

```text
SponsorHub
FoxMail
FoxText
Sponsor Rewards
```

David remembered the sponsors page but not the other page name. The likely additional visual pages are FoxMail and FoxText, with Sponsor Rewards either integrated into SponsorHub or shown as its own rewards tab/page. Do not treat this as final owner confirmation of which one he meant; preserve all three as the JOB-12 visual backlog until David remembers or chooses.

Suggested visual separation:

- **SponsorHub:** professional sponsorship marketplace and contract dashboard.
- **FoxMail:** full formal inbox for contracts, approvals, payment notices, vehicle assignments, and sponsor correspondence.
- **FoxText:** compact short-message/notification conversation view.
- **Sponsor Rewards:** reward catalog, unlock progress, points cost, claim state, and sponsor-specific perks; may live inside SponsorHub unless David wants a separate page.

## JOB-12 runtime warning and required handoff

The current JOB-12 standalone runtime attempts are not a stable production baseline. GitHub incident record:

```text
INCIDENT_REPORTS/2026-07-14_JOB-12_WEBUI_ORDER_OF_OPERATIONS_FAILURE.md
```

The first test used the wrong HUD UI App launcher. The corrected keybind-opened WebUI opened, but its UI-to-Lua actions and returned state did not work. JOB-10 must not copy or integrate that failed runtime event pattern.

Before JOB-10 connects the visual SponsorHub/FoxMail/FoxText pages to runtime, JOB-12 must provide:

1. stable page/app identity and canonical route IDs;
2. a working UI-to-Lua and Lua-to-UI proof;
3. exact state/data schema for sponsors, offers, contracts, mail, text, points, rewards, and vehicle assignments;
4. exact event/action names approved through JOB-02;
5. loading, empty, unavailable, success, warning, and error states;
6. presentation-only file boundaries JOB-10 may edit;
7. proof that phone and PC use the same backend contract;
8. no phone shell, PC shell, browser core, registry, Career, RLS, money, inventory, garage, or storage duplication.

## Proposed JOB-10 next work

JOB-10 may build standalone browser-only visual pages for SponsorHub, FoxMail, FoxText, and Sponsor Rewards so David can review appearance before integration.

This visual work must remain labeled:

```text
MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG
```

It must not claim sponsor applications, contracts, rewards, points, deposits, persistence, vehicle assignments, mail delivery, or text delivery are working until JOB-12 supplies and David tests a stable runtime handoff.

## Coordination notice to other jobs

- **JOB-12:** provide the stable sponsor/mail/text data and action contract; retain all sponsor-system behavior ownership.
- **JOB-02:** approve any new sponsor/mail/text bridge messages before runtime integration.
- **JOB-01:** provide shared phone/PC registration and responsive container boundaries.
- **JOB-11:** define and run visual/runtime verification after integration.
- **JOB-00:** approve integration order and combined release.
- **JOB-10:** owns only the final visual design, responsive layout, icons, cards, navigation, forms, states, and website polish.

No other job should independently redesign SponsorHub, FoxMail, FoxText, or Sponsor Rewards after this visual coordination note without coordinating with JOB-10 and JOB-12.
