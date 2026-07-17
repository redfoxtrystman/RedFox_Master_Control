# JOB-00 — Camping Pause Coordinator Consolidated Review

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification regular chat / Sol  
**Record type:** OWNER-REQUESTED CAMPING PAUSE CHECKPOINT — NOT A HANDOFF  
**Ownership:** JOB-00 claim retained by this regular chat  
**Purpose:** Consolidate the sound-off audits, identify genuine progress and blockers, preserve external operational risks, and define the safest restart order.

---

## 1. JOB-00 sound-off

This chat remains exactly:

```text
JOB-00 — Coordinator / Integration / Verification
```

This pause does not release, transfer, merge, rename, or close JOB-00. No background work is claimed while David is camping. Work resumes in this same chat.

JOB-00 owns coordination, baseline freeze, ownership reconciliation, dependency order, integration gates, collision checks, final assembly approval, release manifests, rollback records, and project-wide audit history. JOB-00 does not rewrite every feature mod.

---

## 2. Pause-audit coverage found in GitHub

| Job | Audit evidence reviewed | Coordinator finding |
|---|---|---|
| JOB-00 | This consolidated review | Pause record now complete. |
| JOB-01 | `f566269756d043677764a1920b140e46c497d543`, `5d17de8b9f320ac55b88aecbc332c66701e90e14` | Full audit and claim-retained notice present. |
| JOB-02 | `f8bf8c7aaad2f1c8e231524c91d94a7da36797a6`, `28afad7e805da5fe5305a0b36420b63016e2ef6d` | Full audit and pause notice present. |
| JOB-03 | `4d38b4f164f8ca0c9579011f82cc95bec2a8483a` | Full App Store pause audit present. |
| JOB-04 | `66cd8873494fcffa35bcae2829ac4a3a922df62e` | Full Scrap Yard pause audit present. |
| JOB-05 | `d100a1b9d4356de7eeaafa30c538889ca46aa65d`, `9de9ff378f2b67e03b3652b2e9d024d15e69af40` | Full BeamBook checkpoint and no-handoff correction present. |
| JOB-06 | `9afaeafda0847b1e22a83187fb3537e8b3827fd7`, `4389093b033e36b5178f1c32fcb3ea1ab325d383` | Full Import/Export audit and sound-off present. |
| JOB-07 | `015cebd602073ecc0367c6221e15cc25df13cf01`, `f9a6a757b0746464717688f0851c09325f0e17d4`, `85291a06aa5c69034c177541234ba2219cd03be7` | Full Classics audit and pause notices present. |
| JOB-08 | `ec24fd022beac04d1cd3e4662143e6612cb8f331`, `8d349ec3dda72bac850326a5e9a41d232414491b` | Full Vehicle Services audit and pause notice present. |
| JOB-09 | `38330844a504ea4a2aad9edacfcddc40f384c945`, `2816825a356eccf957623a1b0257e97ecda84732`, `762b93cc976e2eb86ff94f0e2c58889fb7d2f403` | Extensive Tow audit, read-first index, and future-system notes present. |
| JOB-10 | `0cf771252d05b2938bc901ad0e4e9f0b0f246d14`, `6bd2b81c0fa9392be148ff765c0aec4e77b6a611`, `9de09847c69153c9bf0177c89fb8e4646769e857` | Extensive visual audit, dependency checklist, and no-handoff notice present. |
| JOB-11 | No new July 17 camping-pause audit commit found during this review | Existing QA framework is substantial, but JOB-11 still owes a dedicated owner-requested pause sound-off/audit. |
| JOB-12 | `691bfc5959d20e2cef9adeb58175f7d36f43e98b`, `670f145f775c71415003330f827f3cbd1d768382` | Full current-state record exists; later commit correctly clarifies that it is a pause, not a handoff. |

Audit coverage is strong. The missing dedicated JOB-11 pause audit is a documentation gap, not evidence that its earlier QA work disappeared.

---

## 3. Coordinator assessment — what is genuinely going well

### JOB-09 Tow / Recovery / Dispatch

JOB-09 is the strongest active feature lane. It has an exact v0.2.5 candidate with hash, source tree, static checks, multiple call types, road-scene generation, multi-yard records, Tow Fleet Book, Tow History Book, impound/abandoned records, map-aware hazard classification, and realistic scene paints.

Current candidate:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
SHA-256: 52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
Status: BUILT — RUNTIME UNTESTED
```

David's earlier Tow mission testing is valuable user-reported evidence, but the exact v0.2.5 candidate still requires testing. The productive Tow focus is not a mistake; it created a working-pattern laboratory for backend-first WEUI testing. The risk is feature creep before v0.2.5 is runtime-tested.

### JOB-10 Visual Design

JOB-10 has made substantial visible progress and preserved a detailed design record. The current browser checkpoint is:

```text
RedFox_JOB10_Full_Websites_v0_3_1.zip
SHA-256: 0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
Status: MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG
```

The pages are credible source material for app owners. JOB-10 also documented the earlier broken direct-preview package and the reason a complete asset set or self-contained preview is required. The next visual work should be minor correction and handoff, not another large redesign.

### JOB-05 BeamBook

JOB-05 has a small canonical standalone candidate plus separate research packages. The canonical candidate is statically verified and keeps shared platform/Career ownership boundaries intact:

```text
5-RedFox_BeamBook_Standalone_v0_1_0_RUNTIME_UNTESTED.zip
SHA-256: 1ba7933b39f4897ca22158dc27ca591ad4ec5109b01bd05a1ca7d3072d2361d8
Status: BUILT — RUNTIME UNTESTED
```

The external research derivative and read-only monitor are useful experiments, but they must not replace the canonical RedFox-owned candidate until runtime tests prove which behavior is worth porting.

### JOB-01 Phone + PC Platform Core

JOB-01 has the clearest shared-platform implementation checkpoint:

```text
Draft PR #3
Branch: agent/job01-platform-core-v0-1
Head: 83da4ad165d6347f7b7588a970f9cd1876df1b98
Contract: job01.platform.v1
Status: BUILT — RUNTIME UNTESTED
```

It uses one registry and shared browser source for phone and PC, preserves RLS as the phone/Career authority, and does not absorb feature business logic. That is the correct architecture. It still has unhandled visible controls, sparse diagnostics, a hard-coded weather display, an address-normalization issue, no runtime proof, and no committed generated ZIP.

### JOB-04 Scrap Yard

JOB-04 made the right strategic correction: stop fighting the final website, use a WEUI/backend test panel first, prove stock/RLS calls, then connect both phone and PC to the same proven backend.

Current candidate record:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0.zip
Reported size: 24,404,253 bytes
Status: BUILT — RUNTIME UNTESTED
```

The download link failed for David, so the candidate must be re-uploaded or rebuilt and re-opened before it is trusted.

---

## 4. Shared-spine problem

The project has real progress in feature lanes, but the shared spine is not yet proven:

1. JOB-01 platform PR #3 is open, draft, unmerged, and runtime untested.
2. JOB-02 has no committed final contract, schema, fixtures, Lua adapter, test ZIP, or runtime build.
3. The earlier JOB-02 contract/schema/fixture drafts were reportedly created locally but are missing from GitHub.
4. JOB-03 cannot safely implement install/enable/disable until JOB-01 freezes registry/state behavior.
5. Feature jobs cannot honestly claim complete phone/PC transactions until JOB-01 and JOB-02 are proven.

This is now the project's central bottleneck. More website pages or more Tow features will not solve it.

---

## 5. Critical discrepancy requiring correction

JOB-01 and JOB-02 recorded different byte sizes for the same RLS archive SHA-256:

```text
Filename family: rls_career_overhaul_2.6.6.zip
SHA-256: b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b
JOB-01 recorded size: 43,066,347 bytes
JOB-02 recorded size: 40,035,328 bytes
```

The same byte-for-byte SHA-256 cannot have two sizes. Before baseline freeze:

1. locate the exact archive;
2. measure its actual byte size;
3. recompute SHA-256;
4. determine whether one record used extracted size, a suffixed but different archive, or a simple documentation error;
5. correct the current authoritative record while preserving historical notes.

No build should proceed merely by filename until this is resolved.

---

## 6. Current status of the remaining feature lanes

### JOB-03 App Store

Claim and design work exist; no mod exists. This is appropriately blocked/deferred. David has now found approximately three or four additional phone mods, including at least one with a built-in app store. Those files must be inspected before JOB-03 commits to an implementation model.

### JOB-06 Import / Export

Planning and recovery documentation are strong, but there is no accessible source, build, or current version. Historical candidates are missing. It remains blocked on source/baseline intake and shared contracts.

### JOB-07 Classics / Collector Exchange

Claim and architecture are documented, but no source or build exists. It remains blocked on the current IceFox baseline and JOB-02 contract.

### JOB-08 Insurance / Finance / Garage / Storage

The visual prototype and broad product plan are useful. There is no runtime mod. Native insurance IDs/APIs, property/fleet mechanics, and bridge contracts remain unknown. It should begin with read-only live data after the shared contracts exist, not with fake quotes or mutation controls.

### JOB-12 Sponsor System

JOB-12 has learned from several failed approaches. v0.5.0 did not block Career but used the wrong HUD UI interaction and its functions did not work. v0.5.1 used the desired keybind/WebUI direction but blocked Career loading. v0.6.0 is a minimal proof candidate but remains unproven. The correct next step is still the smallest possible open/close/ping/session-state proof, with no money, persistence, phone, PC, mail, text, drift, Hesi, or sponsor economy added until that passes.

### JOB-11 QA

JOB-11 has already produced a real QA framework: logging spec, master test matrix, installed-package fingerprint checklist, static package audit tool, failure templates, handoff validator, and GitHub Action. This is valuable. It still needs a dedicated July 17 pause sound-off and should run its validators against real submitted feature handoffs once those exist.

---

## 7. New phone-mod intake directive

David reports finding approximately three or four other BeamNG phone mods. At least one reportedly contains a built-in app store similar to the desired RedFox Store.

These mods may help, but they are references until inspected. Required ownership:

- JOB-01: inspect phone shell, routing, launch registration, PC compatibility, host lifecycle, and whether the phone can extend RLS without replacing it.
- JOB-03: inspect app-store catalog/state/install/enable/disable/open/update patterns.
- JOB-02: inspect UI-to-Lua communication and Career/RLS permission boundaries.
- JOB-11: inspect packaging, startup behavior, duplicate paths, unsafe overrides, and removal behavior.
- JOB-00: compare results and approve one architecture.

Required checks for each phone mod:

```text
Exact filename, size, SHA-256
License/reuse permission
ZIP root and file tree
Phone shell/framework/app/store classification
Startup extensions and Career overrides
Manifest/app discovery method
Route registration
UI framework: AngularJS/Vue/custom/GMUI/WEUI
Lua bridge calls and message names
Persistence/settings path
Built-in app store behavior
PC-sharing potential
RLS conflicts
Duplicate paths with JOB-01/FoxNet
Removal/uninstall behavior
Known runtime result
```

Do not copy code or replace the current RLS phone merely because another mod has an attractive Store. First extract the mechanism that is safe, licensed, and compatible.

---

## 8. External project conditions that affect FoxNet testing

### PC crash investigation

David is experiencing serious PC crashes. A separate diagnostic/monitoring application has been created to collect evidence and help classify the failure as hardware, software, or a combination. David intends to leave it running for approximately one week to capture failures.

This is not a BeamNG/FoxNet feature, but it directly affects test reliability. JOB-00 will track it as an external environment risk:

- preserve every diagnostic snapshot and autosaved report;
- record exact crash timestamps;
- correlate BeamNG tests with system crashes, USB resets, storage events, power events, driver faults, and hardware telemetry;
- do not label a BeamNG candidate broken solely because the whole PC crashed without identifying the first failing layer;
- do not label a candidate working if the test was cut short by system instability;
- keep PC-monitor source/results separate from BeamNG mod packages.

When David returns, JOB-00 should review the monitor's reports before scheduling long integrated BeamNG tests.

### Career Node Grabber

There is still no working Node Grabber in Career. This is a separate unresolved mod/tool issue and must not be misreported as completed by the FoxNet jobs. Record it as an external Career-tool blocker until its owning chat produces a tested candidate.

---

## 9. Coordinator restart order after camping

### Gate 0 — Personal and machine readiness

1. Review PC-monitor reports and classify major crashes.
2. Preserve logs and do not erase the diagnostic evidence before review.
3. Confirm which testing machine/configuration is stable enough for controlled BeamNG tests.

### Gate 1 — Identity and baseline

4. Resolve the RLS archive size/hash discrepancy.
5. Freeze one exact RLS/FoxNet baseline with filename, size, SHA-256, file tree, and installed-mod rules.
6. Re-upload any binaries that exist only in old chats or local containers.

### Gate 2 — Prove the shared spine

7. Harden and build JOB-01 PR #3 candidate; remove or label dead controls; improve diagnostics.
8. Test JOB-01 phone and PC hosts opening the same `redfox.home` destination.
9. Reconstruct and commit JOB-02 contract/schema/fixtures.
10. Build the smallest read-only JOB-02 capability/data proof before purchase/sell mutations.
11. Prove phone and PC use the same JOB-02 operation contract.

### Gate 3 — Test strongest standalone feature candidates

12. Test exact JOB-09 v0.2.5. Do not add more Tow features until the result is recorded.
13. Re-upload/rebuild and test the JOB-04 Scrap Yard WEUI candidate.
14. Test JOB-05 canonical standalone BeamBook before deciding which research behavior to port.
15. Test JOB-12 minimal v0.6.0 proof only after verifying it is the exact intended package and older sponsor ZIPs are disabled.

### Gate 4 — Phone-mod comparison

16. Intake and hash all newly found phone mods.
17. Compare their phone shell, app store, registration, and bridge methods against JOB-01/JOB-03 requirements.
18. Decide whether to extend RLS, create a RedFox-owned shell, or borrow only a safe pattern.

### Gate 5 — Website integration

19. JOB-10 hands approved page source to each feature owner.
20. Each feature owner converts its page into a BeamNG-hosted entry and connects it to the already-proven backend.
21. JOB-01 registers the same canonical destination for phone and PC.
22. JOB-11 validates package boundaries and runtime evidence.
23. JOB-00 approves final assembly only after independent candidates pass.

---

## 10. Final coordinator opinion

The project is making genuine progress. The strongest breakthroughs are Tow's standalone mission system, JOB-10's visual package, BeamBook's isolated candidate/research tools, the JOB-01 platform branch, and the shift to backend-first WEUI testing.

The main danger is not lack of progress. It is continuing to add features around an unproven platform/bridge core, losing binary candidates outside GitHub, and allowing inconsistent baseline records. The next milestone should not be “more pages.” It should be:

```text
ONE PROVEN PHONE/PC HOST
ONE VERSIONED SHARED CAREER BRIDGE
ONE BACKEND-PROVEN FEATURE CONNECTED TO ONE APPROVED WEBSITE
```

Scrap Yard is the best first cross-system proof because it already exposed the original phone/PC mismatch. Tow should remain the strongest standalone feature and be used as a pattern, not allowed to consume all integration time.

---

## 11. Pause status

```text
PROJECT PAUSED BY OWNER REQUEST
NOT A HANDOFF
JOB CLAIMS RETAINED
NO FINAL RELEASE APPROVED
RUNTIME CLAIMS REMAIN LIMITED TO DAVID'S EXACT TESTS
```
