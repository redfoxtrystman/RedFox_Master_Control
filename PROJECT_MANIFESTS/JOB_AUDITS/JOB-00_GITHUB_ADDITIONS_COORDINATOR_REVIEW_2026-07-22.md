# JOB-00 — GitHub Additions Coordinator Review

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Review range:** Changes after `cc039a75e6790ff0c2a4fc630b8c2a4604e54c30` through current `main`  
**Status:** COORDINATOR REVIEW — NO FINAL RELEASE APPROVED

## 1. Scope reviewed

The repository gained 31 commits after the Web System Recovery return checklist. The file-level changes reviewed fall into these groups:

- JOB-04 — Scrap Yard / Wrecking Yard grey-screen incident reports, v0.1.1 no-core-UI rebuild and v0.1.2 phone/PC access patch audit;
- project-wide core UI override ban;
- JOB-05 — BeamBook Marketplace v0.2.0 and v0.2.1 records;
- JOB-09 — Tow / Recovery / Dispatch v0.2.6 through v0.2.9 records and source-change summaries;
- RedFox Skin Studio corrective rebuild and v0.2.1 hotfix records;
- support-lane and PC stability issue updates;
- read-first/index updates.

Most new repository files are audits, handoffs, incident reports and source-change summaries. The repository still does not contain the installable ZIPs for most current candidates, and it does not contain complete current source trees for every active build. GitHub is currently a strong audit trail, but it is not yet a complete recoverable build archive.

## 2. Critical stop finding — JOB-04 core UI contradiction

The project-wide rule added on 2026-07-22 states that feature jobs must not package:

```text
ui/ui-vue/dist/index.js
```

unless David explicitly approves a high-risk core UI integration task owned by the proper platform/core lane, with an inspected baseline, exact diff, rollback plan and explicit verification disclosure.

However, the current JOB-04 v0.1.2 audit states that this feature package reintroduces:

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
```

in order to add the IceFox phone manifest and route.

This creates a direct coordination contradiction:

```text
PROJECT RULE: feature jobs must not ship the global Vue bundle.
CURRENT JOB-04 v0.1.2: feature ZIP ships the global Vue bundle.
```

Coordinator decision:

```text
JOB-04 v0.1.2 IS HIGH-RISK AND NOT APPROVED AS THE NORMAL NEXT SCRAP-YARD TEST.
```

Do not treat the use of a fresh RLS file as sufficient safety proof. The earlier grey-screen failure demonstrated that a narrow feature ZIP overriding a global UI bundle can break the entire game UI and cost substantial troubleshooting time.

Required resolution:

1. JOB-04 — Scrap Yard / Wrecking Yard keeps only its backend, page and test-panel files.
2. JOB-01 — Phone + PC Platform Core owns phone/PC route and registry integration.
3. Any temporary core-UI compatibility test must be explicitly labeled as a JOB-01/JOB-00 approved high-risk platform test, not a normal JOB-04 feature build.
4. The exact diff against the frozen RLS baseline, rollback instructions and clean-install test must be published before David installs it.
5. A no-global-UI route-registration mechanism should be preferred if one can be proven.

## 3. JOB-04 — Scrap Yard / Wrecking Yard current assessment

Evidence sequence:

- Earlier v0.1.0 included the global Vue bundle and caused the title/background/in-game UI grey-screen failure.
- v0.1.1 removed the global bundle and avoided repeating that exact override, but David reported that PC access did not work and the phone IceFox icon was missing.
- v0.1.2 adds Angular PC states/buttons and reintroduces the global Vue bundle for the phone route. It is statically verified but runtime untested.

Positive progress:

- Incident cause and user time loss were documented honestly.
- The direct/startup Scrap Yard Career module remains banned.
- v0.1.1 and v0.1.2 records preserve explicit test instructions and hashes.
- The PC Angular state/button idea is narrower than patching marketplace logic at startup.

Current status:

```text
BACKEND/WEUI WORK: PARTIAL
PC ACCESS: NEW v0.1.2 PATH — RUNTIME UNTESTED
PHONE ACCESS: DEPENDS ON HIGH-RISK GLOBAL UI OVERRIDE
NORMAL NEXT TEST: BLOCKED UNTIL CORE-UI OWNERSHIP IS RESOLVED
```

## 4. JOB-05 — BeamBook Marketplace current assessment

Current documented candidate:

```text
RedFox_BeamBook_Full_Wall_200_Realistic_v0_2_1_RUNTIME_UNTESTED.zip
Size: 15,521,373 bytes
SHA-256: c1b40de04a1442f950b8fa71d2f20cc9a34d8ba2a02c909e2f1241d4ed2c7993
Status: BUILT — RUNTIME UNTESTED
```

Positive progress:

- The 200-listing fallback catalog is recorded and validated.
- Expensive heavy vehicles can no longer appear inexplicably cheap without a disclosed title/mechanical/damage reason.
- Clean-title floors, market value, discount and repair estimates were added.
- No direct archive-path overlap with the current Scrap Yard candidate was found.
- No startup Career module, global shopping replacement or fake money/ownership/storage system is claimed.

Important limitation:

Title and DMV problems are listing metadata only. They do not currently block registration, charge fees, persist holds or connect to a working DMV system.

Current status:

```text
GOOD ISOLATED CANDIDATE FOR SEPARATE TESTING
NOT PHONE/PC-INTEGRATED
NOT A REAL DMV/TITLE SYSTEM
RUNTIME UNTESTED
```

The official job board is stale because it still lists BeamBook v0.1.0 rather than the current v0.2.1 candidate.

## 5. JOB-09 — Tow / Recovery / Dispatch current assessment

Current documented candidate:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_ActiveCallRecoveryAlertsDamage.zip
Size: 181,835 bytes
SHA-256: 95722351456b6caeb51b448a624bdb33ae4b89e17e45df5fa77a85b6439ea1f2
Status: BUILT — RUNTIME UNTESTED
```

Positive progress since v0.2.5:

- police impound and emergency-scene expansion;
- RLS progression and personal-claim work;
- Career-day clock and asset manager;
- active-call autosave/recovery after crashes or power loss;
- tow/service-truck validation;
- longer and more visible dispatch alerts;
- target-condition variety;
- improved semi/heavy-carrier scene composition;
- newer police-configuration preference;
- protected Career/RLS override scan remains clear.

Confirmed runtime evidence retained from v0.2.8:

```text
Western Star Tow Yard record -> personal Career inventory/garage: DAVID-TESTED WORKING
```

Everything else in v0.2.9 remains runtime untested.

Coordinator concern:

The Tow lane has advanced through four version waves while the shared web platform and bridge remain unproven. The additions are thoughtful, but v0.2.9 is now large enough that another feature wave before testing would create avoidable regression risk.

Coordinator direction:

```text
FREEZE NEW MAJOR TOW FEATURES.
TEST EXACT v0.2.9.
FIX ONLY EVIDENCE-BASED FAILURES.
```

The official job board is stale because it still says JOB-09 — Tow / Recovery / Dispatch is AVAILABLE even though issue #4, the claim file and current v0.2.9 work establish an active owner.

## 6. SUPPORT-01 — Cross-Map 3D Asset Conversion / Prefab / Placement

Current status:

```text
CLAIMED — INTAKE AND ARCHITECTURE VERIFICATION
NO RUNTIME BUILD TESTED
```

The lane correctly keeps model conversion, materials, collision, prefab creation and map-independent placement separate from JOB-04 business logic.

Current blocker:

- no candidate model archive/license record has been supplied to the support chat;
- Blender/export tool versions and David's BeamNG version still need recording;
- no prefab placement ZIP exists yet.

Next action:

Intake the models David found, but do not publish or redistribute them until the exact license permits game-mod conversion and redistribution. Start with one simple model and a two-map placement proof.

## 7. SUPPORT-02 — Career Node Grabber / Developer Mode Compatibility

Current candidate:

```text
RedFox_Career_Dev_Tools_v2_0_3_RMOD_NODE_SWITCH_UNPROVEN_TEST.zip
SHA-256: 611856ae05d4d916a850f27d8aab53a9297e09566e41755904faa33de8c299d6
Status: RUNTIME UNTESTED
```

Positive progress:

- abandoned full-file replacement of Career logic;
- abandoned broad cheats-mode replacement and repeating patch loop;
- targets only the `careerNodeGrabberActions` input-block group;
- has explicit ON/OFF controls and test steps;
- standalone custom grabber failure is documented rather than hidden.

Risk:

The build still wraps the global `core_input_actionFilter.addAction` function at runtime. The exact-group guard narrows the effect, but wrapper stacking, load order and OFF-state restoration need testing.

Required test:

Use a backed-up disposable Career save, enable only v2.0.3, avoid all money controls and verify actual node attachment—not just node rendering.

## 8. PC Stability / Crash Monitor current assessment

Issue #6 contains meaningful evidence rather than a single-cause guess:

- repeated WHEA corrected hardware events;
- grouped USB/device loss and reconnect events;
- bad-block events on two disk numbers;
- memory/page-file exhaustion during BeamNG/PiP use;
- a blue-screen minidump;
- a v1.4.0 unattended monitoring candidate with autosave/checkpoint plans.

The TrailSpotter PiP/mirror mod is a confirmed heavy-load trigger, but it does not explain the WHEA and grouped USB evidence by itself.

Current direction remains correct:

1. protect data on drives reporting bad blocks;
2. preserve all monitoring evidence;
3. verify the exact Sentinel build on Windows;
4. isolate mechanical drives and other hardware carefully;
5. do not use interrupted or unstable sessions as final BeamNG mod proof.

## 9. RedFox Skin Studio

Current documented candidate:

```text
RedFox_Skin_Studio_v0_2_1_BUILT_RUNTIME_UNTESTED.zip
Corrected SHA-256: 7402125eeaca928cd587bcaf0d75d39df00b58b879d58e07d679af84b672cf48
Status: BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED
```

The corrective record is detailed and honestly preserves David's v0.2.0 failures. The v0.2.1 record adds vehicle/source indexing, existing-skin discovery, asset album, reusable design vault, named history and UV-guide export exclusion.

This is a separate RedFox tool, not one of JOB-00 through JOB-12 and not part of the FoxNet runtime integration path. It must not be allowed to block the web-system recovery work.

The corrected hash commit is important: older notes showing `7c0549...` are not authoritative for the final v0.2.1 artifact. The current authoritative recorded hash is `740212...`.

## 10. Shared platform status remains unresolved

Despite substantial feature activity, the central web spine has not materially advanced in the reviewed commits:

- JOB-01 — Phone + PC Platform Core PR #3 remains open, draft, unmerged and runtime untested.
- PR #3 is currently reported non-mergeable against the newer `main` history and needs review/rebase before use.
- JOB-02 — Shared RLS / Career Bridge still lacks a committed final contract/schema/fixtures/runtime proof.
- Issue #7, the RLS 2.6.6 archive size/hash discrepancy, remains open with no resolution comment.
- No current feature may honestly claim full shared phone/PC integration.

This remains the main project bottleneck.

## 11. Repository/index inconsistencies requiring correction

1. `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md` still marks JOB-09 — Tow / Recovery / Dispatch as AVAILABLE.
2. The same board still reports JOB-05 — BeamBook Marketplace v0.1.0 instead of v0.2.1.
3. `RedFox_Worker_Chat_Quick_Start.md` does not yet link the new project-wide core UI override ban.
4. The Quick Start does not list SUPPORT-01, SUPPORT-02 or the Web System Recovery return checklist.
5. The core UI ban and the JOB-04 v0.1.2 audit conflict directly.
6. Current candidate ZIPs and complete source are often outside GitHub; hashes alone are not a recoverable backup.

## 12. Coordinator priority after this review

```text
1. DO NOT NORMAL-TEST JOB-04 v0.1.2 until the global UI override is reclassified/removed.
2. Preserve the grey-screen incident rule as a hard stop condition.
3. Test JOB-09 — Tow / Recovery / Dispatch v0.2.9 before any more Tow feature work.
4. Test JOB-05 — BeamBook Marketplace v0.2.1 separately.
5. Resolve issue #7 and freeze the exact RLS baseline.
6. Rebase/review JOB-01 — Phone + PC Platform Core PR #3 against current main.
7. Reconstruct JOB-02 — Shared RLS / Career Bridge contract and read-only proof.
8. Return JOB-04 to backend-first WEUI work without feature-owned global UI files.
9. Intake SUPPORT-01 models/licenses.
10. Test SUPPORT-02 v2.0.3 only on a backed-up disposable save.
11. Preserve and review the PC stability evidence before long integration testing.
12. Keep RedFox Skin Studio as a separate tool lane.
```

## 13. Release decision

```text
NO FINAL RELEASE APPROVED
NO SHARED FOXNET BASELINE FROZEN
NO PHONE/PC WEB INTEGRATION PROVEN
NO JOB-04 GLOBAL UI OVERRIDE APPROVED
```
