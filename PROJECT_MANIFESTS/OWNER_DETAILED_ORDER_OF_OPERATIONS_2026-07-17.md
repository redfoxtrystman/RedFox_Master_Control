# OWNER DETAILED ORDER OF OPERATIONS — RedFox/FoxNet BeamNG Web System

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** OWNER-APPROVED WORK ORDER — FOLLOW UNLESS NEW EVIDENCE REQUIRES A CHANGE  
**Purpose:** Give David and every worker chat one readable sequence for continuing the project without losing working features, fighting the websites, or building around an unproven shared platform.

---

## 1. Communication rule — always use the complete job name

From this point forward, project messages, audits, commits, reports, handoffs, and coordinator summaries must use the full job number and title on first mention and in headings.

Correct examples:

```text
JOB-04 — Scrap Yard / Wrecking Yard
JOB-09 — Tow / Recovery / Dispatch
JOB-11 — QA / Logging / Failure Triage
```

Avoid bare references such as `JOB-04`, `chat 9`, or `job eleven` when the complete title can be written. David uses the titles to remember which lane owns which work.

### Complete job map

| Job | Complete title | Main responsibility |
|---|---|---|
| JOB-00 | Coordinator / Integration / Verification | Dependencies, baseline, integration approval, final assembly, audit trail. |
| JOB-01 | Phone + PC Platform Core | IceFox front door, phone/PC hosts, route registry, canonical destinations. |
| JOB-02 | Shared RLS / Career Bridge | Shared Career/RLS data, transactions, ownership, inventory, garage/storage and error contracts. |
| JOB-03 | RedFox App Store / Play Store | App catalog, install/enable/disable/open/update behavior after platform rules are proven. |
| JOB-04 | Scrap Yard / Wrecking Yard | Scrap backend, buying/selling, player-owned yard, dismantling, crusher, parts and scrap business. |
| JOB-05 | BeamBook Marketplace | BeamBook social and marketplace backend and website connection. |
| JOB-06 | Import / Export Yard | Import/export vehicle market and later approved freight/export endpoints. |
| JOB-07 | Classics / Collector Exchange | Classic, rare and collector vehicle market. |
| JOB-08 | Insurance / Finance / Garage / Storage Pages | Vehicle services, insurance, finance, garage and storage adapters/pages. |
| JOB-09 | Tow / Recovery / Dispatch | Tow calls, recovery scenes, yards, fleet/history, impound and tow website connection. |
| JOB-10 | Visual Design / Real Website Polish | Website appearance, responsive layouts, assets and design system. |
| JOB-11 | QA / Logging / Failure Triage | Independent checks, logs, regressions, package validation and failure-layer identification. |
| JOB-12 | SponsorHub / FoxMail / FoxText / Sponsor Rewards | Sponsor progression, mail/text notifications and rewards. |

JOB-11 — QA / Logging / Failure Triage is currently parked/on-call because David has not yet assigned a specific new task. It did not miss the camping sound-off request.

---

## 2. Project law

The project must follow this sequence:

```text
PROVE BACKEND
→ CONNECT WEBSITE
→ REGISTER SAME PHONE/PC DESTINATION
→ TEST INDEPENDENT PACKAGE
→ ASSEMBLE VERIFIED COMPONENTS
```

A visually complete page is not proof that its mod works. A WEUI/debug panel and the final website must call the same backend functions.

Tow work is not forbidden. JOB-09 — Tow / Recovery / Dispatch is productive and enjoyable for David, and it provides useful real gameplay. The control rule is simply:

```text
Test the current exact Tow candidate and fix evidence-based failures before adding another major Tow feature wave.
```

Tow may remain a controlled relaxation/creative lane while the main shared-platform blockers are addressed, but it may not consume every integration cycle.

---

## 3. Website page backlog and staged handoff rule

David remembers that additional pages still need to be added but cannot currently remember every page. This must not force a false “all pages finished” claim or block all progress indefinitely.

### JOB-10 — Visual Design / Real Website Polish may hand off in stages

A staged handoff is valid when it includes:

1. the current design system;
2. a complete page inventory;
3. each page marked `READY`, `NEEDS MINOR WORK`, `PLACEHOLDER`, `DEFERRED`, or `OWNER UNASSIGNED`;
4. common responsive components and asset rules;
5. a backlog for remembered-later pages;
6. no claim that a page is functional in BeamNG unless its owner has connected and tested it.

Unknown or remembered-later pages can be added after the first handoff because each page must remain a separate registered destination/add-on. Adding one later page must not require rebuilding every finished feature.

### Known page families to preserve in the backlog

Core/assigned page families:

- IceFox home/browser — JOB-01 — Phone + PC Platform Core.
- RedFox App Store / Play Store — JOB-03 — RedFox App Store / Play Store.
- Scrap Yard / Wrecking Yard — JOB-04 — Scrap Yard / Wrecking Yard.
- BeamBook — JOB-05 — BeamBook Marketplace.
- Import / Export Yard — JOB-06 — Import / Export Yard.
- Classics / Collector Exchange — JOB-07 — Classics / Collector Exchange.
- Insurance / Finance / Garage / Storage — JOB-08 — Insurance / Finance / Garage / Storage Pages.
- RedFox Recovery/Towing website — JOB-09 — Tow / Recovery / Dispatch.
- SponsorHub / FoxMail / FoxText / Sponsor Rewards — JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards.

Known visual pages or expansion pages that still need runtime ownership confirmed:

- FoxNet Auctions.
- FoxFax.
- Parts Exchange.
- UndergroundNet Black Market.
- Shadow DMV.
- Chop Shop.
- Most Wanted.
- High Risk Freight.
- Cold Storage.
- Any additional page David remembers later.

Before final integration, JOB-00 — Coordinator / Integration / Verification must assign every functional page to an exact owner or leave it clearly labeled visual-only/deferred.

---

## 4. Detailed order of operations

### Gate 0 — David and test-machine readiness

1. Complete camping/surgery recovery and avoid scheduling important runtime tests when David is not physically or mentally up to them.
2. Preserve the PC monitor/System Sentinel reports generated while the machine is unattended.
3. Record exact PC crash timestamps, USB resets, storage events, Windows events and power/temperature evidence.
4. Review the PC stability reports before using long BeamNG sessions as final verification.
5. Keep all PC diagnostic source and reports separate from BeamNG mod ZIPs.

The PC investigation communicates through GitHub issue:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/6
```

Permanent sanitized records belong under:

```text
PC_STABILITY/
```

### Gate 1 — Preserve exact candidates

6. Gather every current candidate ZIP that exists only in a chat/container or on David's PC.
7. For each exact file, record:
   - filename;
   - byte size of the archive itself;
   - SHA-256 of the archive itself;
   - ZIP integrity;
   - file count;
   - source/baseline;
   - runtime status;
   - location where David has the file.
8. Do not trust a filename alone. Suffixed files such as `(1)` or `(2)` may or may not be identical.
9. Do not treat extracted folder size, download display size, or compressed member total as archive byte size.

### Gate 2 — Resolve shared-baseline identity

10. Locate the exact `rls_career_overhaul_2.6.6` archive intended as the shared reference/build input.
11. Recompute its archive byte size and SHA-256.
12. Resolve the existing contradiction:

```text
SHA-256 recorded by both lanes:
b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b

JOB-01 — Phone + PC Platform Core recorded size: 43,066,347 bytes
JOB-02 — Shared RLS / Career Bridge recorded size: 40,035,328 bytes
```

13. Determine whether one figure was extracted size, an incorrect note, or a different file.
14. Publish one authoritative archive identity while preserving the historical correction record.
15. JOB-00 — Coordinator / Integration / Verification freezes the shared test baseline and installed-mod rules.

No shared build may proceed solely from the copied size/hash note until this is corrected.

### Gate 3 — Inspect newly found phone mods

16. Intake all three or four newly found phone mods.
17. Record filename, size, hash, license/reuse permission and exact file tree.
18. Classify each as phone shell, UI framework, app launcher, app store, standalone app, GMUI/WEUI system or unrelated.
19. JOB-01 — Phone + PC Platform Core inspects shell, lifecycle, routes and RLS compatibility.
20. JOB-03 — RedFox App Store / Play Store inspects app catalog and install/enable/disable/open/update behavior.
21. JOB-02 — Shared RLS / Career Bridge inspects UI-to-Lua calls and Career permissions.
22. JOB-11 — QA / Logging / Failure Triage is activated for duplicate paths, startup overrides, removal behavior and unsafe packaging once exact files exist.
23. JOB-00 — Coordinator / Integration / Verification chooses whether to extend RLS, make a RedFox-owned shell, or borrow only a safe pattern.

Do not replace the current phone merely because another mod has an attractive app store.

### Gate 4 — Prove JOB-01 — Phone + PC Platform Core

24. Harden the current draft platform source.
25. Remove, implement or visibly label dead controls.
26. Add build/version diagnostics and stronger route/registry logging.
27. Correct address normalization and misleading hard-coded live-looking data.
28. Build one exact test ZIP from the frozen baseline.
29. Test the phone host and PC host opening the same `redfox.home` destination.
30. Confirm phone and PC use one registry, one canonical app ID and one entry path.
31. Test close/back/return behavior and at least one second map.
32. Do not merge or declare working until David tests the exact ZIP.

### Gate 5 — Build JOB-02 — Shared RLS / Career Bridge

33. Reconstruct and commit the missing contract, schema and fixtures.
34. Publish exact versioned operation names, payloads, errors, timeouts, correlation IDs and compatibility handshake.
35. Start read-only:
   - Career/session capabilities;
   - vehicle-shopping data;
   - owned vehicle list;
   - garage/storage read-only state where supported.
36. Prove identical requests/results from phone and PC.
37. Add purchase/sell mutations only after read-only operations work.
38. Never treat “purchase menu opened” as “vehicle purchased.”
39. Never spawn a vehicle as purchase success.
40. Never invent money, ownership, inventory or storage results.

### Gate 6 — Test JOB-09 — Tow / Recovery / Dispatch

41. Test the exact latest candidate recorded at pause:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
SHA-256: 52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
```

42. Record exact map, call types, yards, fleet/history behavior, logs and failures.
43. Fix only failures proven by the test before adding another major feature set.
44. Preserve WEUI forced-call controls for development.
45. Tow-company skins are a separate creative task under JOB-09 — Tow / Recovery / Dispatch or a dedicated skin workflow. They do not block shared-platform integration.

### Gate 7 — Prove JOB-04 — Scrap Yard / Wrecking Yard

46. Recover, rebuild or re-upload the current WEUI/backend candidate because the previous download failed.
47. Reopen the exact ZIP and verify its identity and contents.
48. Test explicit loading of real vehicle-shopping data.
49. Test opening the real selected purchase menu.
50. Test listing real owned Career vehicles.
51. Test selling only an explicitly selected owned vehicle through the real inventory sell path.
52. Test on a non-West-Coast map.
53. Preserve logs and stop at the first failing layer.
54. Use one backend for WEUI, phone, PC and final website.

### Gate 8 — Prove JOB-05 — BeamBook Marketplace

55. Test the canonical standalone RedFox candidate before importing behavior from research derivatives.
56. Verify UI discovery, key/open behavior, marketplace data, parking/inspection handoff and errors.
57. Keep research settings/monitor packages separate until evidence shows which features belong in the canonical build.
58. Do not call social/mock interactions Career functionality unless real backend state exists.

### Gate 9 — Finish JOB-10 — Visual Design / Real Website Polish page inventory

59. Inventory every current website/page and status.
60. Apply only remaining minor corrections to the current design baseline.
61. Add remembered pages when David identifies them.
62. Hand each approved page source to its exact feature owner.
63. Keep a deferred/backlog directory so missing pages do not block the first end-to-end proof.
64. Do not merge gameplay/backend code into the visual source package.

### Gate 10 — First end-to-end proof

65. Use JOB-04 — Scrap Yard / Wrecking Yard as the first full proof because it exposed the original phone-versus-PC mismatch.
66. Connect the approved Scrap Yard page to the already-proven Scrap Yard backend.
67. Register one canonical destination through JOB-01 — Phone + PC Platform Core.
68. Use JOB-02 — Shared RLS / Career Bridge for real data/actions.
69. Test phone and PC against the same backend contract.
70. Test at least two maps.
71. JOB-11 — QA / Logging / Failure Triage independently checks the package, logs, duplicate paths and regression behavior.
72. JOB-00 — Coordinator / Integration / Verification approves or rejects the integration.

The first integrated milestone is:

```text
ONE PROVEN PHONE/PC HOST
+ ONE VERSIONED SHARED CAREER BRIDGE
+ ONE BACKEND-PROVEN FEATURE
+ ONE APPROVED WEBSITE
```

### Gate 11 — Expand the feature set

73. Repeat the same pattern for:
   - JOB-05 — BeamBook Marketplace;
   - JOB-06 — Import / Export Yard;
   - JOB-07 — Classics / Collector Exchange;
   - JOB-08 — Insurance / Finance / Garage / Storage Pages;
   - JOB-09 — Tow / Recovery / Dispatch;
   - JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards.
74. Activate JOB-03 — RedFox App Store / Play Store after the platform registry/state model is stable.
75. Assign or defer the currently unowned page families.
76. Do not let one app copy the platform or bridge into its own ZIP.

### Gate 12 — Physical player-owned Scrap/Wrecking Yard

77. Acquire or create one or more properly licensed yard/building models.
78. Inspect the house-building/placement mod David identifies.
79. Decide whether to adapt a safe licensed placement mechanism or create a RedFox-owned placement system.
80. Begin with a visual-only physical yard shell:
   - office/shop building;
   - fence/gates;
   - stacks of cars;
   - crusher/processing area;
   - storage areas;
   - signs and props.
81. Let the player select a reasonably flat location on any map.
82. Save yard map, position, rotation and model set.
83. Keep the model/placement layer separate from business logic.
84. The first physical yard does not need to run the economy; it may initially be realistic scenery plus marked interaction zones.
85. Add yard ownership, capacity, upgrades and business actions only after placement/save behavior is stable.

### Gate 13 — Scrap/Wrecking Yard business expansion

86. Add player purchase/build cost and yard record.
87. Add legal vehicle intake and whole-vehicle resale.
88. Add controlled dismantling and salvage-part/material records.
89. Give the in-game car crusher a real economic purpose with transaction safety.
90. Add processed scrap and crushed-bale outputs.
91. Add same-map and later cross-map freight manifests.
92. Add optional illegal disposal and underground parts only after legal progression works.
93. Keep legal/illegal records, payouts, heat and reputation clearly separated.
94. Prevent duplicate disposal, save/reload duplication and arbitrary vehicle deletion-for-money.

### Gate 14 — Final QA and assembly

95. Every candidate submits required reports and `REDFOX_JOB_HANDOFF.json`.
96. JOB-11 — QA / Logging / Failure Triage runs static/package/runtime evidence checks.
97. David tests each exact ZIP.
98. JOB-00 — Coordinator / Integration / Verification confirms compatible versions and no overlapping protected files.
99. Assemble the combined release from verified components—not from a fresh giant rewrite.
100. Record hashes, versions, WEUI disposition, known limitations and rollback points.

---

## 5. When the order may change

The order may be changed only when:

- a test reveals a prerequisite was wrong;
- a newly found mod provides a safer, licensed mechanism;
- the PC stability investigation makes runtime testing unreliable;
- David explicitly changes priority;
- a health/recovery need makes pausing the correct choice;
- a feature has a small isolated test that does not risk the shared baseline.

Any change must be written to GitHub with the reason and new restart point.

---

## 6. Coordinator direction to David

David does not need to stop doing Tow work that is calming and enjoyable. The practical discipline is:

```text
Tow test/fix cycle
→ one shared-spine task
→ one Scrap Yard task
→ optional Tow/creative task
```

The coordinator should direct priorities without turning the project into punishment. The goal is steady progress, preserved working code and fewer repeated failures—not removing the part David enjoys.
