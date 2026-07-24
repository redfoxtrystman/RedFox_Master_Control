# OWNER WEB SYSTEM RECOVERY — PHONE-ONLY RETURN CHECKLIST

**Originally created:** 2026-07-17  
**Updated:** 2026-07-23  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** CURRENT PRACTICAL RESTART LIST  
**Purpose:** This is the exact list for getting the RedFox/FoxNet pages connected and working on the BeamNG in-game phone. PC/garage-computer web hosting is deferred and is not part of this checklist.

Read first:

```text
PROJECT_MANIFESTS/OWNER_PHONE_ONLY_ARCHITECTURE_DIRECTIVE_2026-07-23.md
```

---

## 1. Begin with the known phone-working Scrap Yard rollback

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

Known limitations:

- phone page switching may take around 30 seconds;
- white or grey waiting screens may appear during navigation;
- sell flow remains unproven;
- seller-patience behavior is not the current priority;
- inherited core UI files are present, so this ZIP is a frozen rollback baseline rather than an editing template.

---

## 2. Prepare a clean test installation

Install only:

```text
Current approved RLS Career Overhaul baseline
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
```

Disable or remove:

```text
JOB-04 v0.1.5
JOB-04 v0.1.4 when using the v0.1.6 rollback name
all older JOB-04 test ZIPs
all other zzzz_RedFox_FoxNet... ZIPs
all RedFox_ScrapYard_Direct... ZIPs
all experimental phone integrations
```

Do not test two phone shells or two FoxNet integration ZIPs together.

Back up the Career save before testing any purchase or sale behavior.

---

## 3. Reconfirm the rollback behavior

Test only the phone path:

1. Launch BeamNG.
2. Confirm the title/menu and Career load.
3. Open the in-game phone.
4. Record how long the phone takes to open.
5. Open IceFox/FoxNet/Scrap Yard through the known route.
6. Record how long each page switch takes.
7. Load the Scrap Yard vehicle list.
8. Select one inexpensive test vehicle.
9. Open the real purchase flow.
10. Complete a purchase only on a backed-up/disposable save.
11. Confirm the vehicle appears through real Career/RLS ownership and storage behavior.
12. Save, exit and reload the Career profile.
13. Confirm the purchased vehicle remains correctly owned.
14. Preserve the relevant `beamng.log` lines.

Required report:

```text
Exact ZIP filename =
Archive size =
SHA-256 =
RLS version =
Map =
Career profile =
Phone-open time =
Scrap Yard-open time =
Page-switch time =
Vehicle-list result =
Purchase-menu result =
Purchase result =
Ownership/storage result =
Save/reload result =
Errors/log timestamps =
```

Do not test or repair PC access during this pass.

---

## 4. Preserve the working phone-buy path

Before any development change:

- keep an untouched copy of v0.1.6;
- record its exact hash and file size;
- compare the proposed edit against the rollback;
- change one narrow behavior at a time;
- rebuild under a new version/filename;
- test the phone route before testing the changed feature;
- roll back immediately if the phone icon, route, page or purchase flow disappears.

Do not blindly copy changes from the failed v0.1.5 parity/performance build.

---

## 5. Intake the alternate phone mod

David downloaded another phone mod that appears to work well. It may become the RedFox/FoxNet host.

Before deciding, record:

```text
Exact filename
Archive byte size
SHA-256
Source / creator
Download page
License
Modification permission
Game-mod redistribution permission
Attribution requirements
BeamNG version
RLS version
File tree
Phone framework
Manifest / route registry
Built-in app-store behavior
UI-to-Lua calls
Persistence
Startup extensions and overrides
Stock/RLS files replaced
Core UI files included
Phone layout files included
Duplicate-path risks
Removal behavior
Known runtime result
```

Ownership of the inspection:

- JOB-01 — Phone + PC Platform Core: phone shell, routing, lifecycle, RLS compatibility and removal;
- JOB-03 — RedFox App Store / Play Store: app catalog, install/enable/disable/open/update/remove behavior;
- JOB-02 — Shared RLS / Career Bridge: UI-to-Lua calls and Career permissions;
- JOB-11 — QA / Logging / Failure Triage: package conflicts, startup overrides and clean removal;
- JOB-00 — Coordinator / Integration / Verification: final host decision.

Do not upload or redistribute the alternate phone publicly until its license permits it.

---

## 6. Build one minimal page on the alternate phone

Do not move all RedFox pages at once.

The first proof contains only:

```text
One RedFox title
One status field
One JavaScript button
One UI-to-Lua ping
One Lua-to-UI response
One close/back operation
```

Required result:

1. Career loads normally.
2. The alternate phone opens.
3. The RedFox test page appears.
4. Assets load using package-relative paths.
5. The button reaches Lua.
6. Lua returns a visible response.
7. Close/back works.
8. The mod can be disabled without breaking the phone or Career.
9. The same proof works on a second map where relevant.

If this fails, stop. Do not port Scrap Yard or other pages to that phone yet.

---

## 7. Choose the phone host

Compare the current RLS/v0.1.6 phone path against the alternate phone.

Decision criteria:

```text
Career loads reliably
Phone opens reliably
Page registration is understandable
Pages can be added without duplicating the full phone
UI-to-Lua calls work
RLS purchase/ownership behavior remains authoritative
No avoidable dangerous global UI override
Clean install and removal
No duplicate-path conflicts
Acceptable load and page-switch time
License permits the intended use
Built-in app-store behavior is useful and safe
```

Possible decisions:

```text
A. Keep the current RLS phone and improve it carefully.
B. Use the alternate phone as the RedFox/FoxNet host.
C. Reuse only safe patterns from the alternate phone.
D. Continue intake because neither candidate is safe enough yet.
```

JOB-00 — Coordinator / Integration / Verification records the decision and freezes one phone-host baseline.

---

## 8. Stabilize JOB-01 — Phone + PC Platform Core for phone-only use

JOB-01 retains its official title, but current required deliverables are phone-only:

- one approved phone host;
- one phone route/app registry;
- one canonical ID per RedFox page;
- one approved entry-path format;
- open/close/back behavior;
- clear errors and logs;
- build/version diagnostics;
- clean removal;
- no feature-owned duplicate phone shell;
- no current PC-host requirement.

The old phone+PC parity draft is historical/deferred. Do not merge it as the current target merely because it exists.

---

## 9. Rebuild JOB-02 — Shared RLS / Career Bridge

JOB-02 remains essential even though there is only one UI host.

Commit and prove:

```text
Versioned bridge contract
JSON schema
Fixtures/examples
Capability handshake
Error/result format
Correlation/request IDs
Timeout behavior
```

Start read-only:

```text
Get Career/session status
Get available capabilities
Get vehicle-shopping data
Get owned Career vehicles
Get garage/storage information where supported
```

Then add carefully verified actions:

```text
Open purchase flow
Confirm actual purchase result
Sell one explicitly selected owned vehicle
Other approved feature actions
```

No feature page may invent its own money, ownership, inventory or storage result.

---

## 10. Use JOB-04 — Scrap Yard / Wrecking Yard as the first full phone integration

After the phone host and shared bridge are frozen:

1. Preserve v0.1.6 as rollback evidence.
2. Prove the Scrap Yard backend through its development harness.
3. Keep the working phone buy path intact.
4. Hand the approved mobile Scrap Yard design from JOB-10 — Visual Design / Real Website Polish to JOB-04.
5. Remove mock data.
6. Connect the page to the proven backend/shared bridge.
7. Register it on the approved phone host.
8. Test open/close/back.
9. Test real shopping data.
10. Test purchase and save/reload.
11. Test owned-vehicle listing.
12. Test sale only after purchase stability is proven.
13. Test another map where relevant.
14. Run JOB-11 QA.
15. Have David test the exact ZIP.

First milestone:

```text
ONE PROVEN PHONE HOST
+ ONE VERSIONED SHARED CAREER BRIDGE
+ ONE PROVEN SCRAP YARD BACKEND
+ ONE APPROVED MOBILE SCRAP YARD PAGE
```

---

## 11. Connect remaining pages one at a time

Repeat the same pattern for:

```text
JOB-05 — BeamBook Marketplace
JOB-06 — Import / Export Yard
JOB-07 — Classics / Collector Exchange
JOB-08 — Insurance / Finance / Garage / Storage Pages
JOB-09 — Tow / Recovery / Dispatch
JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

Per page:

```text
Prove backend
→ adapt approved mobile page
→ register on approved phone
→ test open/close/back
→ test real data/action
→ test save/reload where state changes
→ test second map where relevant
→ JOB-11 QA
→ David tests exact ZIP
→ JOB-00 approval
```

Remembered-later pages remain in the JOB-10 backlog and can be added later.

---

## 12. Deferred PC work

The following are deferred by owner and are not current blockers:

- Career/garage PC web host;
- PC browser page registration;
- identical phone and PC destinations;
- phone/PC layout parity;
- PC-specific feature-page adaptation;
- PC integration acceptance tests.

Preserve old PC work as research. Do not delete it or call it impossible. Label it:

```text
DEFERRED BY OWNER — NOT PART OF CURRENT RELEASE TARGET
```

The separate PC Stability / Crash Monitor remains active because hardware/software stability affects BeamNG testing.

---

## 13. Core UI safety

The v0.1.6 rollback contains inherited core UI files and is a narrow grandfathered exception.

Any new change involving:

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
```

requires:

- explicit JOB-01 and JOB-00 approval;
- exact baseline identity;
- exact diff;
- high-risk labeling;
- clean-install instructions;
- rollback/removal instructions;
- immediate stop if title/menu/phone/Career loading regresses.

Normal feature jobs must not independently ship or rewrite those files.

---

## 14. Exact next actions

```text
1. Preserve and install only the v0.1.6 Scrap Yard rollback with the approved RLS baseline.
2. Reconfirm phone opening, Scrap Yard opening and real purchase/save-reload behavior.
3. Upload or provide the alternate phone mod to JOB-01 / JOB-03 for intake.
4. Record its exact identity, license, structure and runtime behavior.
5. Build one minimal RedFox ping page on the alternate phone.
6. Choose and freeze one phone host.
7. Reconstruct JOB-02 shared bridge read-only contract.
8. Stabilize Scrap Yard on the selected phone without touching PC.
9. Connect the approved mobile Scrap Yard page.
10. Repeat the proven phone-only method for the other pages.
```

---

## 15. Stop conditions

Stop and inspect when:

- Career does not finish loading;
- the phone does not open;
- a RedFox page route disappears;
- page assets do not load;
- UI-to-Lua ping does not return;
- more than one phone/FoxNet integration ZIP is installed;
- a page invents gameplay state in browser storage;
- a purchase opens but ownership/storage does not complete;
- save/reload loses or duplicates a purchase;
- a ZIP identity or license is unknown;
- a feature job copies or replaces the entire phone shell;
- a global UI or phone-layout file appears without approval;
- the PC suffers a full-system crash during testing.

No page is called connected, working, fixed or finished until David tests the exact ZIP.
