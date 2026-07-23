# JOB-09 — Read First After Camping

**Original pause date:** 2026-07-17  
**Updated:** 2026-07-22  
**Owner:** David / Captain  
**Status:** **ACTIVE TESTING — NOT A HANDOFF**

Resume the same regular-chat JOB-09 workstation. Do not rename, replace, or transfer JOB-09.

---

## Current active test candidate

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_ActiveCallRecoveryAlertsDamage.zip
Size: 181,835 bytes
SHA-256: 95722351456b6caeb51b448a624bdb33ae4b89e17e45df5fa77a85b6439ea1f2
Status: BUILT — RUNTIME UNTESTED
```

Active workspace path:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_ActiveCallRecoveryAlertsDamage.zip
```

The binary ZIP is not stored on GitHub.

Previous source baseline:

```text
v0.2.8 — Career-Day Clock and Organized Asset Manager
SHA-256: b7ad5424f82f70cec998e1ee01345c8f608b01d60aac6a6f927f06e75019a018
```

---

## Confirmed runtime evidence

David confirmed:

```text
v0.2.8 Western Star Tow Yard record -> personal Career inventory/garage: DAVID-TESTED WORKING
```

David also reported that the reorganized Tow interface was an improvement.

Testing was interrupted by:

- another window crash;
- a power outage during a semi rollover call;
- a headache;
- loss of the active call because v0.2.8 kept it only in runtime memory.

Storage clock, remaining claim paths, progression, responder cleanup, and all other v0.2.8 behavior remain partial until retested.

---

## Why v0.2.9 was created

Runtime findings and owner requirements:

- active Tow calls need crash/power-loss recovery;
- calls need a longer acceptance window;
- incoming dispatch needs an audible and much more visible alert;
- Tow targets should not be deliverable by simply teleporting to and driving them without the tow truck nearby;
- accident and rollover targets need more disabled/damaged/wrecked conditions;
- semi recovery should not add a trailer every time;
- integrated-bed/carrier heavy vehicles should sometimes have a displaced cargo vehicle instead;
- emergency scenes should prefer newer police configurations.

---

## v0.2.9 focus

### Active-call recovery

- Autosaves every 12 seconds by default.
- Rotates between two recovery files plus Career-profile state.
- Manual **Save Active Call Now**.
- **Resume Saved Active Call** and **Discard Saved Active Call** after restart.
- Restores undelivered model/configuration, transform, scene role, condition profile, destination, route, payment plan, and progression preview.
- Regenerates responders from the scene anchor.
- Preserves the last snapshot when a target unexpectedly disappears.

Exact live node/beam deformation is not guaranteed after power loss; the saved damage profile is reapplied.

### Tow/service vehicle validation

- Records the vehicle used to accept the job.
- Stores RLS inventory ID where available.
- Manual service-truck reassignment.
- A target cannot be assigned as its own service truck.
- More than 100 meters separation after target movement starts a 15-second countdown.
- Delivery requires the assigned service truck within 35 meters.

### Incoming dispatch

- Existing users migrate to a five-minute acceptance window.
- Built-in BeamNG mission-information sound.
- Large RedFox incoming-call banner.
- Repeating reminder every 30 seconds by default.
- Acceptance and reminder intervals are adjustable.

### Target condition variety

- Operational impound.
- Operational abandoned.
- Stalled.
- Flat tire.
- Neglected.
- Minor collision.
- Rollover damage.
- Severe collision.
- Heavy wreck.

### Semi/heavy-carrier variety

- Heavy truck only.
- Tractor plus trailer.
- Integrated/rigid carrier plus displaced cargo vehicle.
- Transport tractor plus displaced cargo vehicle.

### Police selection

Compatible modern stock/modded police configurations are scored above older choices. Older vehicles remain fallback-only when no modern option is found.

---

## Read these records

### Complete original state through v0.2.5

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_TOW_RECOVERY_DISPATCH_PAUSE_AUDIT_2026-07-17.md
```

### RLS cross-map repo and future systems

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_RLS_CROSS_MAP_REPO_AND_FUTURE_SYSTEMS_PAUSE_AUDIT_2026-07-17.md
```

### v0.2.6 police/emergency scenes

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_CAMPING_PAUSE_ADDENDUM_v0.2.6_2026-07-21.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_POLICE_IMPOUND_EMERGENCY_SCENES_v0.2.6_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.6_POLICE_IMPOUND_EMERGENCY_SCENES_CHANGE_SUMMARY.md
```

### v0.2.7 RLS progression and personal claims

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_CAMPING_PAUSE_ADDENDUM_v0.2.7_2026-07-21.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_RLS_PROGRESSION_PERSONAL_CLAIMS_v0.2.7_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.7_RLS_PROGRESSION_PERSONAL_CLAIMS_CHANGE_SUMMARY.md
```

### v0.2.8 clock and organized assets

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_CAREER_DAY_ASSET_MANAGER_v0.2.8_2026-07-22.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.8_CAREER_DAY_ASSET_MANAGER_CHANGE_SUMMARY.md
```

### v0.2.9 active-call reliability and target conditions

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_ACTIVE_CALL_RECOVERY_ALERTS_DAMAGE_v0.2.9_2026-07-22.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.9_ACTIVE_CALL_RECOVERY_ALERTS_DAMAGE_CHANGE_SUMMARY.md
```

### Third-party event/tow compatibility

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_THIRD_PARTY_TOW_EVENT_COMPATIBILITY_AUDIT_2026-07-21.md
```

---

## Immediate v0.2.9 test

```text
1. Disable every older JOB-09 ZIP, including v0.2.8.
2. Enable only v0.2.9.
3. Use a disposable RLS Career save and disposable service truck.
4. Accept a call, move a target, save, restart BeamNG, and resume it.
5. Confirm delivered targets do not respawn.
6. Confirm tow-truck separation warning/countdown and delivery proximity.
7. Confirm sound, RedFox banner, repeat reminders, and five-minute acceptance.
8. Run Standard, Rolled, Accident, and Semi calls and inspect damage/disabled profiles.
9. Confirm semi-only, semi/trailer, and carrier/cargo variations.
10. Confirm newer police configurations are preferred when installed.
11. Regression-test v0.2.8 storage clock, organized pages, progression, and personal claim.
12. Return beamng.log around any save, resume, spawn, alert, validation, damage, UI, or persistence failure.
```

---

## Business/company boundary

Still not implemented:

- Tow Yard -> Tow Company Fleet ownership transfer;
- company fleet storage;
- personal <-> company vehicle transfer;
- company bank routing;
- branch relocation/map transfer;
- company sale protection;
- XXX fleet-insurance enrollment;
- full Phone/PC asset-manager UI.

A disposable vehicle must prove rollback-safe company transfer before the valuable abandoned truck is moved.

---

## Permanent warnings

```text
v0.2.2 is REJECTED — DO NOT USE.
Do not claim v0.2.9 working before David tests this exact ZIP.
Do not patch, copy, or redistribute stock BeamNG Career or RLS source.
Do not assume a restored call preserves exact node/beam deformation.
Do not move the valuable abandoned truck into company ownership yet.
Company fleet storage is not in v0.2.9.
This remains the same JOB-09 workstation; it is not a handoff.
```