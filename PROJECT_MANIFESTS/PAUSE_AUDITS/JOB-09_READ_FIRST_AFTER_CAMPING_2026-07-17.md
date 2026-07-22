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
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_6_PoliceImpoundEmergencyScenes.zip
```

```text
Size: 118,799 bytes
SHA-256: 82eecc0652d61cc8b6d203d0bf7eb541bdee95532e8c82c2b2ecd59c0a0b2dbd
Status: BUILT — RUNTIME UNTESTED
```

Actual ZIP location in the active ChatGPT JOB-09 workspace:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_6_PoliceImpoundEmergencyScenes.zip
```

The installable ZIP is not stored as a GitHub binary.

v0.2.5 remains the known source baseline/fallback and was not declared broken:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
SHA-256: 52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
```

---

## Read these full audits

### 1. Original current Tow mod and complete JOB-09 state

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

### 2. v0.2.6 camping-pause addendum

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_CAMPING_PAUSE_ADDENDUM_v0.2.6_2026-07-21.md
```

Contains:

- New current candidate identity/hash.
- Police-requested, street-racing, and DUI impound additions.
- Emergency-scene support additions.
- Optional-mod integration decisions.
- Updated runtime test order.
- Explicit list of systems still not implemented.

### 3. RLS cross-map repo carrier and future systems

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

### 4. Third-party Tow/Event compatibility audit

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

## v0.2.6 build records

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_POLICE_IMPOUND_EMERGENCY_SCENES_v0.2.6_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.6_POLICE_IMPOUND_EMERGENCY_SCENES_CHANGE_SUMMARY.md
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
1. Disable every older JOB-09 ZIP, including v0.2.5.
2. Enable only v0.2.6.
3. Use a disposable Career save for the first responder-scene test.
4. Confirm old yards, fleet records, cataloged history, and impounds load.
5. Test Police-Requested Vehicle Impound.
6. Test Street-Racing Vehicle Impound.
7. Test DUI Checkpoint Impound.
8. Test one Accident and one Semi Rollover with emergency support enabled.
9. Confirm police/EMS/cones clean up after completion and cancellation.
10. Check Optional Mod Connections with the supplied mods installed.
11. Return complete SITE_SCAN/EVENT_LIBRARY lines and beamng.log around errors.
12. Patch only runtime-proven failures.
```

After the current Tow mod is stable, run the separate RLS persistence test with one tractor, one trailer, and one damaged loaded car before designing the full cross-map repo shipment system.

---

## Permanent warnings

```text
v0.2.2 is REJECTED — DO NOT USE.
Do not claim v0.2.6 working before David tests it.
Do not patch stock BeamNG Career or RLS source directly.
Do not guess undocumented random-event APIs.
Do not claim live Random Events vehicles without a supported claim/lifecycle API.
Do not copy or bundle third-party source/assets without permission and compatible licensing.
Do not add a complex business/accounting simulator.
Do not add unfinished AI towing to the current video-test build.
Universal rigging, unified tow controls, backups, and multi-wrecker controls are not in v0.2.6.
This camping pause is not a handoff.
```
