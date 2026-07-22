# JOB-09 — Read First After Camping

**Original pause date:** 2026-07-17  
**Updated:** 2026-07-22  
**Owner:** David / Captain  
**Status:** **PAUSED/ACTIVE TESTING — NOT A HANDOFF**

Resume the same regular-chat JOB-09 workstation. Do not rename, replace, or transfer JOB-09.

---

## Current active test candidate

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_8_CareerDayAssetManager.zip
Size: 154,970 bytes
SHA-256: b7ad5424f82f70cec998e1ee01345c8f608b01d60aac6a6f927f06e75019a018
Status: BUILT — RUNTIME UNTESTED
```

Active workspace path:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_8_CareerDayAssetManager.zip
```

The binary ZIP is not stored on GitHub.

Previous source baseline:

```text
v0.2.7 — RLS Progression and Personal Claims
SHA-256: a34ed2660e6bf69ad86722c16114f3fe0989422dca4f65cfb3cd5f49a156fd73
```

---

## Why v0.2.8 was created

David's runtime screenshots showed:

- storage remaining at `0 day(s) / $0`;
- map time/daylight apparently frozen;
- personal claim controls hidden behind a hold that used real calendar days;
- Fleet, Tow Yard, and Tow History producing one extremely long scrolling page;
- values/buttons from adjacent records becoming visually confusing.

Source inspection confirmed that v0.2.7 used `os.time()` and 86,400-second real days for Tow Yard aging.

---

## v0.2.8 focus

### Career-day storage clock

- Follows advancing map time-of-day.
- Uses the map-reported day length when available.
- If time-of-day is frozen, active unpaused Career playtime advances an equivalent day.
- Default fallback is 30 active minutes per Career day.
- Fallback can be adjusted from 5 to 120 minutes.
- Paused time does not advance the fallback clock.
- Existing v0.2.7 yard records migrate without deletion.
- Storage charges accrue per completed Career day.

### Organized asset interface

The main window is split into:

1. Dispatch
2. Fleet
3. Storage / Impound
4. History

Fleet supports location/unit selectors. Storage supports map/category/vehicle selectors. History supports catalog/record selectors.

### Claim visibility

The selected stored record now shows fractional hold progress, remaining Career days, billable storage days, lien, and a clear personal-claim locked/eligible state.

### Vehicle values

The selected record shows its valuation source and can be explicitly reappraised against its exact installed model/configuration. Legacy values are not silently rewritten.

### Future Phone/PC asset manager

Read-only API added:

```text
getAssetManagerData()
```

This prepares Fleet, stored vehicles, history, yards, and clock data for a future Phone/PC company asset page.

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

### Third-party event/tow compatibility

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_THIRD_PARTY_TOW_EVENT_COMPATIBILITY_AUDIT_2026-07-21.md
```

---

## Immediate v0.2.8 test

```text
1. Disable every older JOB-09 ZIP, including v0.2.7.
2. Enable only v0.2.8.
3. Use a disposable RLS Career save.
4. Confirm old yard, fleet, history, and impound records load.
5. Leave time-of-day frozen and confirm Hold Progress advances while driving.
6. Lower fallback to five minutes for a quick billing/expiration test.
7. Confirm one completed Career day adds one storage day and daily storage charge.
8. Confirm three Career days unlock personal claim.
9. Unfreeze time and check that the clock switches to time-of-day-cycle operation.
10. Test Fleet location/unit dropdowns.
11. Test Storage map/category/vehicle dropdowns.
12. Test History catalog/record dropdowns.
13. Reappraise only a disposable stored vehicle.
14. Claim a disposable eligible vehicle with free garage space.
15. Fill garage capacity and confirm a failed claim keeps the Tow Yard record.
16. Save/reload and verify clock, storage, fleet assignment, and history persist.
17. Return beamng.log around any clock, UI, appraisal, claim, payment, or save failure.
```

---

## Business/company boundary

The following are still not implemented and must not be assumed working:

- Tow Yard → Tow Company Fleet ownership transfer;
- personal ↔ company vehicle transfer;
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
Do not claim v0.2.8 working before David tests this exact ZIP.
Do not patch, copy, or redistribute stock BeamNG Career or RLS source.
Do not delete a Tow Yard record before a successful Career inventory transfer.
Do not assume old Tow Yard records preserve exact node/beam deformation.
Do not move the valuable abandoned truck into company ownership yet.
Do not add unfinished AI towing, universal rigging, or company transfer to this clock/UI test.
This remains the same JOB-09 workstation; it is not a handoff.
```