# JOB-09 — Read First After Camping

**Original pause date:** 2026-07-17  
**Updated:** 2026-07-23  
**Owner:** David / Captain  
**Status:** **ACTIVE TESTING — NOT A HANDOFF**

Resume the same regular-chat JOB-09 workstation. Do not rename, replace, or transfer JOB-09.

---

## Current active test candidate

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_10_TowingMultiSkillProgression.zip
Size: 197,466 bytes
SHA-256: b5c4cc4baf0ebea55c8bb6813eb9fdff7b4d78f4a74473fd035cbed797b29c48
Status: BUILT — RUNTIME UNTESTED
```

Active workspace path:

```text
/mnt/data/19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_10_TowingMultiSkillProgression.zip
```

The binary ZIP is not stored on GitHub.

Previous source baseline:

```text
v0.2.9 — Active-Call Recovery, Alerts, and Damage
SHA-256: 95722351456b6caeb51b448a624bdb33ae4b89e17e45df5fa77a85b6439ea1f2
```

---

## Confirmed runtime evidence

David confirmed:

```text
v0.2.8 Western Star Tow Yard record -> personal Career inventory/garage: DAVID-TESTED WORKING
```

David reported that the organized Fleet/Storage/History interface was an improvement.

Other v0.2.8/v0.2.9 systems remain partial or untested because testing was interrupted by a window crash, power outage during a semi rollover call, and headache.

---

## Why v0.2.10 was created

David showed the RLS Career Paths → Skills page and required:

- every Tow job to advance Repo;
- separate RedFox Towing progression;
- towing/transport work to contribute to Logistics/hauling;
- each recovery type to receive appropriate weighting;
- police/emergency work to count toward Civil Service where appropriate;
- all applicable Career progression to be visible and saved.

The exact supplied RLS Career Overhaul 2.6.8 package was inspected before implementation.

Confirmed progression keys:

```text
careerSkills-repo
logistics-delivery
careerSkills-civilService
labourer
beamXP
```

---

## v0.2.10 focus

### Dedicated Towing skill

New additive file:

```text
gameplay/domains/careerSkills/skills/towing/info.json
attributeKey: careerSkills-towing
levels: 50
```

The Towing skill uses the current RLS 2.6.8 50-level threshold curve for matching progression pacing and UI behavior. It does not overwrite or copy an RLS skill file.

### Every Tow call counts

All completed RedFox Tow call types award:

- Towing XP;
- Repo XP;
- Logistics XP;
- Labourer progression;
- Beam XP.

Qualifying police and emergency/public-service calls also award Civil Service XP.

Unpaid and held outcomes still award progression after the recovery work is completed.

### Reward scaling

Rewards scale with:

- response distance;
- loaded/tow distance;
- workload;
- target count;
- recovery type.

Heavy/semi recovery has the strongest Towing and Logistics weighting. Police, DUI, and street-racing impounds have stronger Repo and Civil Service weighting. Accident cleanup receives Towing, Repo, Logistics, and Civil Service credit.

### UI/history

The active-call page previews the full skill breakdown. Completion messages show awarded Towing, Repo, Logistics, and Civil Service XP. Tow History saves and displays the complete progression record.

---

## Current build records

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_TOWING_MULTI_SKILL_PROGRESSION_v0.2.10_2026-07-23.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.10_TOWING_MULTI_SKILL_PROGRESSION_CHANGE_SUMMARY.md
```

Earlier records remain authoritative for their versions:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_ACTIVE_CALL_RECOVERY_ALERTS_DAMAGE_v0.2.9_2026-07-22.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.9_ACTIVE_CALL_RECOVERY_ALERTS_DAMAGE_CHANGE_SUMMARY.md

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_CAREER_DAY_ASSET_MANAGER_v0.2.8_2026-07-22.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.8_CAREER_DAY_ASSET_MANAGER_CHANGE_SUMMARY.md

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_RLS_PROGRESSION_PERSONAL_CLAIMS_v0.2.7_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.7_RLS_PROGRESSION_PERSONAL_CLAIMS_CHANGE_SUMMARY.md

PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_POLICE_IMPOUND_EMERGENCY_SCENES_v0.2.6_2026-07-21.md
PROJECT_SOURCE_PATCHES/JOB-09/v0.2.6_POLICE_IMPOUND_EMERGENCY_SCENES_CHANGE_SUMMARY.md
```

Complete original and cross-map audits:

```text
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_TOW_RECOVERY_DISPATCH_PAUSE_AUDIT_2026-07-17.md
PROJECT_MANIFESTS/PAUSE_AUDITS/JOB-09_RLS_CROSS_MAP_REPO_AND_FUTURE_SYSTEMS_PAUSE_AUDIT_2026-07-17.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_THIRD_PARTY_TOW_EVENT_COMPATIBILITY_AUDIT_2026-07-21.md
```

---

## Immediate v0.2.10 test

```text
1. Disable every older JOB-09 ZIP, including v0.2.9.
2. Enable only v0.2.10 on a disposable RLS Career save.
3. Open Career Paths -> Skills and confirm Towing appears.
4. Record starting Towing, Repo, Logistics, Civil Service, Labourer, and Beam XP.
5. Complete Standard, Abandoned, Rollover, Semi, Accident, Police, Street-Racing, and DUI calls.
6. Confirm every call awards Towing and Repo XP.
7. Confirm every transported/recovered vehicle call awards Logistics XP.
8. Confirm qualifying police/emergency calls award Civil Service XP.
9. Compare short/long, light/heavy, and single/multi-target rewards.
10. Confirm unpaid/held recovery still awards progression.
11. Confirm active-call preview, completion popup, Tow History, and save persistence.
12. Regression-test v0.2.9 active-call save/resume, service-truck validation, alerts, damage, semi variants, and v0.2.8 storage/claim behavior.
13. Return beamng.log around any payment, skill, level-up, UI, or persistence failure.
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
- tow invoice popup/archive;
- full Phone/PC asset manager.

A disposable vehicle must prove rollback-safe company transfer before valuable work trucks are moved.

---

## Permanent warnings

```text
v0.2.2 is REJECTED — DO NOT USE.
Do not claim v0.2.10 working before David tests this exact ZIP.
Do not patch, copy, or redistribute stock BeamNG Career or RLS source.
Do not assume restored active calls preserve exact node/beam deformation.
Company fleet storage and invoices are not in v0.2.10.
This remains the same JOB-09 workstation; it is not a handoff.
```
