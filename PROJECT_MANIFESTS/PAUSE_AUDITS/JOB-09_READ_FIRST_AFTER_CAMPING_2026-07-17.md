# JOB-09 — Read First After Camping

**Original pause date:** 2026-07-17  
**Updated:** 2026-07-21  
**Owner:** David / Captain  
**Status:** **PAUSED — NOT A HANDOFF**

Resume the same regular-chat JOB-09 workstation.

Do not create a replacement job, rename JOB-09, or transfer ownership.

---

## Current active test candidate

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_RLSProgressionPersonalClaims.zip
```

```text
Size: 138,580 bytes
SHA-256: a34ed2660e6bf69ad86722c16114f3fe0989422dca4f65cfb3cd5f49a156fd73
Status: BUILT — RUNTIME UNTESTED
```

Actual ZIP location in the active ChatGPT JOB-09 workspace:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_RLSProgressionPersonalClaims.zip
```

The installable ZIP is not stored as a GitHub binary.

Previous candidates remain documented as source baselines/fallbacks and were not declared runtime-broken:

```text
v0.2.6 Police Impound + Emergency Scenes
SHA-256: 82eecc0652d61cc8b6d203d0bf7eb541bdee95532e8c82c2b2ecd59c0a0b2dbd

v0.2.5 Fleet Identity + Hazard Sites
SHA-256: 52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
```

---

## Read these full audits

### 1. Original Tow mod and complete JOB-09 state through v0.2.5

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_TOW_RECOVERY_DISPATCH_PAUSE_AUDIT_2026-07-17.md
```

Contains:

- Job ownership/scope.
- Every build and version decision through v0.2.5.
- Exact files/hashes/status at the original pause.
- What David tested.
- What failed or was rejected.
- Known limitations.
- Current settings and systems.
- GitHub commits and records.
- Return test checklist and resume priorities.

### 2. v0.2.6 police/emergency-scene addendum

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_CAMPING_PAUSE_ADDENDUM_v0.2.6_2026-07-21.md
```

Contains:

- Police-requested impounds.
- Street-racing impounds.
- DUI checkpoint impounds.
- Emergency-scene support.
- Random Events, Traffic Reborn, and Sandbox Tools integration boundaries.

### 3. v0.2.7 RLS progression and personal-claim addendum

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_CAMPING_PAUSE_ADDENDUM_v0.2.7_2026-07-21.md
```

Contains:

- Current v0.2.7 candidate identity and hash.
- Exact RLS Career Overhaul 2.6.8 package reference.
- Money, workload, distance, and target-count scaling.
- Beam XP, Labourer, Repo XP, and Civil Service XP behavior.
- RLS Repo vehicle statistics.
- Tow Yard `Claim as My Personal Vehicle` process.
- Garage-capacity and rollback rules.
- Updated runtime test order.

### 4. RLS cross-map repo carrier and future systems

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_RLS_CROSS_MAP_REPO_AND_FUTURE_SYSTEMS_PAUSE_AUDIT_2026-07-17.md
```

Contains:

- RLS map-switch correction/research.
- Current RLS repo behavior.
- Repo holding and 5/8/10-car bulk transport concept.
- Tractor/trailer/damaged-car persistence test.
- Damage/partConditions findings.
- Coupler/cargo unknowns.
- Static/frozen reconstruction fallback.
- Future player-rigged AI transport.
- Future manual multi-wrecker winch overlay.
- Simple Business Manager boundary.
- Cross-job coordination.

### 5. Third-party Tow/Event compatibility audit

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_THIRD_PARTY_TOW_EVENT_COMPATIBILITY_AUDIT_2026-07-21.md
```

Contains the complete inspection of:

- Random Events 1.9.0.0;
- Traffic Reborn Free 1.4.0.0;
- Sandbox Tools 1.1.0.0;
- public functions found;
- lifecycle/vehicle-ownership limits;
- licensing/redistribution boundary;
- v0.2.6 integration choices.

---

## Current build records

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_POLICE_IMPOUND_EMERGENCY_SCENES_v0.2.6_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.6_POLICE_IMPOUND_EMERGENCY_SCENES_CHANGE_SUMMARY.md

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_RLS_PROGRESSION_PERSONAL_CLAIMS_v0.2.7_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.7_RLS_PROGRESSION_PERSONAL_CLAIMS_CHANGE_SUMMARY.md
```

---

## Existing GitHub issues

```text
Issue #4 — JOB-09 Tow / Recovery / Dispatch
Issue #5 — [JOB-00 ASSIGNMENT REQUEST] Simple Business Manager and future Tow Support controls
```

---

## Immediate return action

Do not begin another large feature first.

Start here:

```text
1. Disable every older JOB-09 ZIP, including v0.2.6.
2. Enable only v0.2.7.
3. Use a disposable RLS Career save.
4. Confirm old yards, fleet records, cataloged history, impounds, and police calls load.
5. Confirm RLS Repo progression is detected.
6. Complete one short Standard Tow and record money, Beam XP, Labourer, Repo XP, and tow-vehicle repo count.
7. Complete a longer Standard Tow and confirm it awards more.
8. Complete Rolled, Semi Rollover, and Accident calls and compare workload rewards.
9. Complete Police and DUI impounds and check Civil Service progression.
10. Complete an abandoned/unpaid outcome and confirm progression despite deferred/no cash.
11. Inspect Tow History progression fields.
12. After a hold expires, use Claim as My Personal Vehicle.
13. Confirm the record leaves the RedFox yard and appears in My Vehicles/private garage.
14. Fill all garage slots and confirm a refused claim preserves the yard record.
15. Save and reload to verify persistence.
16. Return beamng.log around any reward, attribute, inventory, garage, condition, or claim failure.
17. Patch only runtime-proven failures.
```

After the current Tow mod is stable, run the separate RLS persistence test with one tractor, one trailer, and one damaged loaded car before designing the full cross-map repo shipment system.

---

## Permanent warnings

```text
v0.2.2 is REJECTED — DO NOT USE.
Do not claim v0.2.7 working before David tests it.
Do not patch, copy, or redistribute stock BeamNG Career or RLS source.
Do not guess undocumented random-event APIs.
Do not claim live Random Events vehicles without a supported claim/lifecycle API.
Do not delete a Tow Yard record before a successful Career inventory transfer.
Do not assume older Tow Yard records can reconstruct exact deformation.
Do not add a complex business/accounting simulator.
Do not add unfinished AI towing to the current video-test build.
Universal rigging, unified tow controls, backups, and multi-wrecker controls are not in v0.2.7.
Current hold timing still uses JOB-09's existing timer behavior; verified RLS in-game-day hold timing remains separate work.
This camping pause is not a handoff.
```
