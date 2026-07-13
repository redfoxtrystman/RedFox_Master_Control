# RedFox FoxNet / IceFox — Owner Start Order and Shared Architecture Directive

**Date:** 2026-07-13  
**Owner:** David / Captain  
**Applies to:** JOB-00 through JOB-12  
**Status:** ACTIVE OWNER DIRECTIVE

This directive tells every RedFox FoxNet rebuild chat what is real now, what the first target is, how the mods must fit together, and what language is allowed when reporting progress.

No chat may leave this path or add features without David's permission.

---

# 1. David-reported current baseline

These are David's observed results. They are not independently verified by static inspection yet.

- The current RLS phone works.
- The current PC works only partially and its available options are not the desired final design.
- The phone already has a working IceFox icon.
- The PC needs an IceFox browser/icon.
- Phone and PC must open the same canonical page destinations.
- The phone is effectively the portable form of the PC: it can be opened anywhere instead of only at an in-game computer location.
- All RedFox pages must be reachable on every map, not only West Coast USA.
- The Scrap Yard currently works on the phone but not correctly on the PC.
- The Scrap Yard appears fully usable only on West Coast USA.
- At the Scrap Yard, David can view/select a car and add insurance.
- Clicking Buy currently spawns the vehicle, but the vehicle is not added to Career/RLS ownership or storage. David must use a developer cheat to add it.
- David suspects West Coast-specific online-shop files or IDs are causing the map restriction. This is a hypothesis, not a proven cause. JOB-01, JOB-02, and JOB-04 must inspect the baseline and logs before stating the cause.

No chat may describe the Scrap Yard purchase path as working while a developer cheat is required to finish ownership/storage.

---

# 2. Required architecture

## 2.1 One platform core / front-door mod

There will be one shared RedFox FoxNet/IceFox platform-core mod. It owns only:

- the existing phone IceFox launch entry,
- the new PC IceFox launch entry,
- the shared app/page registry contract,
- shared navigation and route handling,
- responsive host information for phone versus PC,
- the shared front-end connection to the JOB-02 bridge contract,
- compatibility hooks needed to open existing native in-game/RLS pages.

It must extend the existing RLS/BeamNG phone and PC. It must not replace or hijack either shell.

## 2.2 Phone and PC use the same destinations

Every registered page/app must have one canonical identity and one canonical destination.

- The phone IceFox icon and PC IceFox icon open the same IceFox home/destination system.
- A Scrap Yard link from phone and a Scrap Yard link from PC must resolve to the same Scrap Yard app/page and use the same backend messages.
- Phone and PC may use different responsive presentation, window size, or controls.
- They may not use separate business logic, separate guessed bridges, separate purchase flows, or separate data contracts.
- Existing native in-game/RLS pages should be opened through approved route adapters/deep links, not copied into fake replacement pages.

JOB-01 owns the final registration/navigation contract. JOB-02 owns the final UI-to-Career/RLS data/action contract.

## 2.3 Every app/page is its own development mod

During development, each app/page job must produce an isolated add-on mod with unique paths and IDs.

Examples include:

- Scrap Yard,
- BeamBook,
- Import / Export,
- Classics,
- Insurance / Finance / Garage / Storage,
- Tow / Recovery / Dispatch,
- SponsorHub / FoxMail / FoxText / Sponsor Rewards.

Rules:

- App mods consume the JOB-01 platform contract and JOB-02 bridge contract.
- App mods must not contain copied phone shells, PC shells, shared browser code, shared bridge code, or another app's files.
- The platform core must not contain app-specific business logic.
- A final combined release may be assembled only after each independent mod passes verification and JOB-00 approves integration.
- During testing, do not install multiple packages that contain the same shared FoxNet paths.

## 2.4 App Store is optional for the first working milestone

The App Store is not required to prove the shared platform.

Phase 1 may use the existing phone IceFox icon and a new PC IceFox icon with a registry of installed app manifests.

JOB-03 may be deferred until the core browser, shared routes, and Scrap Yard purchase flow work. Small games such as Snake are future backlog items only and must not be added now without David's permission.

---

# 3. Map-independent behavior

All RedFox page routes must open on every map.

No app may hard-code West Coast-only:

- dealership IDs,
- shop IDs,
- facilities,
- parking spots,
- map paths,
- mission paths,
- inventory locations,
- garage/storage locations,
- purchase success assumptions.

When a page opens, JOB-02 must request the active Career/RLS services and data for the current session/map.

If the underlying game/RLS service is genuinely unavailable on a particular map, the page must report the exact unavailable dependency. It may not silently substitute West Coast data, fake a transaction, or claim that the feature works.

---

# 4. Scrap Yard purchase definition of working

A Scrap Yard purchase is not working merely because a vehicle appears in the world.

The required result is:

1. Phone or PC opens the same Scrap Yard destination.
2. Scrap Yard receives valid current-session vehicle shop data through the approved JOB-02 bridge.
3. David selects a vehicle.
4. The approved stock/RLS purchase UI or purchase action handles the vehicle.
5. Insurance selection is preserved through the real purchase flow.
6. The real Career/RLS transaction succeeds.
7. The vehicle becomes a real owned inventory vehicle.
8. The vehicle enters the correct real garage/storage/ownership system.
9. The vehicle may then spawn or be retrieved through the normal game flow.
10. No developer cheat is required.

The exact BeamNG/RLS function sequence must be discovered from the selected baseline and current RLS code. No chat may invent a hand-rolled ownership or storage insertion path.

---

# 5. Truth and status-reporting rule

David explicitly requires honest feature status.

Allowed status labels:

- **DAVID-TESTED WORKING** — David tested the exact build in BeamNG and confirmed the stated result.
- **BUILT — RUNTIME UNTESTED** — files exist and static checks pass, but BeamNG behavior is not proven.
- **PARTIAL** — some stated behavior works, with every missing/broken part listed.
- **BLOCKED** — dependency or evidence is missing; state exactly what is needed.
- **FAILED — STOPPED** — required verification failed; do not ship.
- **MOCKUP / PLACEHOLDER — NOT FUNCTIONAL** — allowed only when David explicitly approves a mockup or placeholder.

Forbidden reporting:

- “working,” “fixed,” “done,” or “safe” before David tests it,
- “should work” used as a substitute for proof,
- hiding a missing action behind a button,
- shipping placeholder controls as if functional,
- calling a spawned vehicle a completed purchase when ownership/storage failed,
- claiming all-map support after testing only West Coast USA.

Default rule: do not add placeholders. If a proposed feature cannot work yet, report it as BLOCKED or PARTIAL and wait for David's direction.

---

# 6. Exact order of operations

## Phase 0 — Rollcall and baseline freeze

1. JOB-00 must be claimed by one dedicated Coordinator chat.
2. Every active chat must maintain one unique claim record with its exact chat title, not only “this chat / Sol.”
3. JOB-00 selects and records the exact baseline ZIP/files.
4. Only one overlapping FoxNet baseline is used for inspection and testing.
5. JOB-11 publishes the shared verification matrix and report templates.

No feature chat may select a competing baseline.

## Phase 1 — Shared platform and bridge contracts

JOB-01 and JOB-02 work in parallel, coordinated through GitHub.

JOB-01 must publish:

- how the existing phone IceFox icon registers/opens,
- how the PC IceFox icon is added without replacing the PC,
- the canonical app/page manifest schema,
- the canonical route/destination identity rules,
- how the phone and PC open the same destination,
- how existing native in-game pages are registered or deep-linked,
- responsive phone/PC host rules,
- the exact shared files it owns.

JOB-02 must publish:

- the canonical request/response/action messages,
- the data shape for current-session Career/RLS data,
- active-map/current-session vehicle-shopping data behavior,
- the approved stock purchase-entry call,
- purchase result/error reporting,
- real owned-inventory and storage/garage result reporting,
- online sell behavior,
- logging and error shapes,
- the exact shared files it owns.

Both contracts must explicitly prohibit map-specific shop assumptions and direct spawn-as-purchase behavior.

## Phase 2 — First functional vertical slice

Before rebuilding every page:

1. Preserve the existing working phone IceFox entry.
2. Add the PC IceFox entry through the existing PC system.
3. Both entries open the same functional IceFox home/destination page.
4. One shared registry entry is proven from both phone and PC.
5. The same page route is tested outside West Coast USA.
6. Logs prove which host opened it and which canonical destination was used.

This must be a functioning minimal platform slice, not a fake button or decorative placeholder.

## Phase 3 — Scrap Yard purchase repair

JOB-04 uses only the published JOB-01 and JOB-02 contracts.

1. Preserve the known useful Scrap Yard selection and insurance behavior.
2. Remove or bypass West Coast-only assumptions only after inspection identifies them.
3. Make phone and PC open the same Scrap Yard destination.
4. Use the approved stock/RLS purchase path.
5. Prove ownership and storage without developer cheats.
6. Test West Coast USA and at least one non-West-Coast map supported by the current RLS/Career session.
7. Report each map separately.
8. Do not start physical sell-zone or towing delivery runtime yet.

## Phase 4 — Independent app/page mods

After the shared route and bridge contracts are stable:

- JOB-05 builds BeamBook as its own add-on.
- JOB-06 builds Import / Export as its own add-on.
- JOB-07 builds Classics as its own add-on.
- JOB-08 builds its approved support portal/pages as its own add-on.
- JOB-09 builds Tow / Recovery / Dispatch as its own add-on.
- JOB-12 builds SponsorHub / FoxMail / FoxText / Sponsor Rewards as its own add-on.

Each app must use the same manifest, route, bridge, logging, and verification contracts.

## Phase 5 — Optional App Store

JOB-03 builds install/enable/disable/open/update behavior only after the platform registry exists. It must feed the JOB-01 registry and must not create a competing launcher.

## Phase 6 — Visual polish

JOB-10 may polish shared visual rules and app presentation after functional contracts and pages are stable. JOB-10 must not alter bridge, purchase, ownership, storage, or navigation behavior.

## Phase 7 — Integration

JOB-00 combines only verified independent mods.

- No duplicate shared paths.
- No copied platform/bridge code inside app mods.
- No runtime claims beyond David's tests.
- Every component remains removable without destroying the others.
- One failure blocks the integrated release.

---

# 7. What each chat must do now

## JOB-00 — Coordinator / Integration / Verification

**Current Git status:** unclaimed.

Must be assigned immediately. It owns the neutral board, baseline selection, contract tracking, integration order, and enforcement. It must not become another feature-code chat.

## JOB-01 — Phone + PC Platform Core

**Current Git evidence:** claimed; the live board previously lost the claim during later overwrites.

Start now:

- inspect the selected phone and PC baseline,
- preserve the working phone IceFox icon,
- identify the correct existing PC registration point,
- draft the single canonical manifest/route contract,
- list exact shared files and protected files,
- do not edit app-owned pages,
- do not promise runtime success before David tests.

## JOB-02 — Shared RLS / Career Bridge

**Current Git status:** claimed.

Start now:

- inspect the exact RLS/Career purchase flow,
- identify why the current Scrap Yard path spawns without ownership/storage,
- inspect active-map shop data and any West Coast-only assumptions,
- publish the bridge contract and error/result shapes,
- do not implement fake ownership, storage, money, or direct-spawn success.

## JOB-03 — RedFox App Store / Play Store

**Current Git status:** unclaimed after the earlier reassignment was corrected back to JOB-04.

This job does not block Phase 1. Claim it later if David still wants the Store. Do not build games now.

## JOB-04 — Scrap Yard / Wrecking Yard

**Current Git status:** claimed.

Start with inspection only:

- preserve known useful phone behavior,
- document the exact West Coast versus other-map difference,
- document the spawn-without-storage failure,
- wait for JOB-01/JOB-02 contracts before changing shared integration,
- do not create the physical yard sell zone yet,
- do not create a startup Career module.

## JOB-05 — BeamBook Marketplace

**Current Git status:** no completed Git claim found.

The BeamBook chat must post its exact claim before work. After claiming, it may inspect its own baseline and preserve the known working marketplace order of operations, but it must wait for shared contracts before integration.

## JOB-06 — Import / Export Yard

**Current Git status:** claimed.

Inspect and plan its isolated app only. Do not implement shared routes, bridge code, stolen-vehicle runtime, or yard delivery runtime.

## JOB-07 — Classics / Collector Exchange

**Current Git status:** claimed.

Inspect and plan its isolated buy-now app only. No auction flow and no shared code edits.

## JOB-08 — Insurance / Finance / Garage / Storage Pages

**Current Git status:** claimed.

Inspect real RLS/Career service/status APIs. Do not fake insurance, finance, ownership, garage, or storage. Preserve the option to separate the four sections later.

## JOB-09 — Tow / Recovery / Dispatch Integration

**Current Git status:** claimed.

Wait for JOB-01/JOB-02 route and bridge contracts plus JOB-04/JOB-06 delivery handoffs. Do not edit Scrap Yard or Import/Export core and do not build yard-delivery runtime yet.

## JOB-10 — Visual Design / Real Website Polish

**Current Git status:** claimed.

Prepare non-destructive visual guidance only. Do not alter navigation, bridge, purchase, ownership, storage, or app business logic.

## JOB-11 — QA / Logging / Failure Triage

**Current Git status:** claimed.

Start immediately:

- publish the phone/PC/same-destination test,
- publish the all-map route matrix,
- publish the Scrap Yard ownership/storage test,
- define evidence required for DAVID-TESTED WORKING,
- enforce protected-file and duplicate-path scans.

## JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Current Git status:** claimed.

Inspect and plan isolated Sponsor-owned apps only. Wait for JOB-01/JOB-02/JOB-03/JOB-11 contracts before integration. No fake payouts or Career money.

---

# 8. GitHub handoff requirements

Every contract-producing chat must publish a versioned handoff file and commit SHA.

Every consuming chat must:

1. link the exact producer commit,
2. state which contract version it consumed,
3. list any requested change,
4. wait for the owning job to approve shared-contract changes,
5. never silently copy or fork the shared contract.

Required first handoffs:

- JOB-01 → all app chats: manifest, route, PC/phone launch, shared file ownership.
- JOB-02 → all data/action apps: request/response/actions, active-map behavior, purchase/storage results.
- JOB-11 → all chats: test matrix, report format, evidence/status labels.
- JOB-04 → JOB-09/JOB-06 later: approved yard-delivery/deep-link interface.
- JOB-03 → app chats later: Store manifest/install state contract.

---

# 9. Permission and scope rule

No chat may:

- add features David did not request,
- “improve” another job's design or behavior,
- change job numbering,
- rename a job,
- create a competing platform, bridge, registry, launcher, or storage system,
- replace native RLS/BeamNG systems with guessed implementations,
- leave the assigned path without David's explicit permission.

If a chat thinks a change is necessary, it must post:

- the exact problem,
- the exact proposed change,
- affected jobs/files,
- risks,
- why the current contract cannot handle it,

and wait for David's approval.

---

# 10. First milestone David should expect

The first milestone is not the full FoxNet ecosystem.

It is:

1. existing phone IceFox icon still works,
2. a real IceFox entry exists on the PC,
3. both open the same functional IceFox destination,
4. the route opens on West Coast USA and a non-West-Coast map,
5. one shared registry/route contract is published,
6. one shared Career/RLS bridge contract is published,
7. logs prove host, destination, current map/session, success, and errors,
8. no app-specific feature has hijacked the platform,
9. every unproven item is labeled honestly.

The next milestone is Scrap Yard purchase completion with real Career/RLS ownership and storage and no developer cheat.
