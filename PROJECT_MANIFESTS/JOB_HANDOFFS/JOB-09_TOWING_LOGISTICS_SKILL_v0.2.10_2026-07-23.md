# JOB-09 — Towing, Repo, and Logistics Progression v0.2.10

**Date:** 2026-07-23  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**

## Exact test package

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_10_TowingLogisticsProgression.zip
Size: 206,801 bytes
SHA-256: be3b823101f310e1d41f2a6788db4a0b2ab9555ace386a8b766f5178bef4267e
```

Source baseline:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_ActiveCallRecoveryAlertsDamage.zip
SHA-256: 95722351456b6caeb51b448a624bdb33ae4b89e17e45df5fa77a85b6439ea1f2
```

The binary ZIP remains in the active ChatGPT JOB-09 workspace and is not committed to GitHub.

## Exact RLS 2.6.8 findings

The uploaded `1(1).zip` archive was inspected read-only. Confirmed authoritative progression keys:

```text
Repo: careerSkills-repo
Logistics: logistics-delivery
Civil Service: careerSkills-civilService
Beam XP: beamXP
Labourer: labourer
```

RLS 2.6.8 aliases `vehicleDelivery`, `delivery`, `materials`, and `logistics-vehicleDelivery` into the unified `logistics-delivery` key. JOB-09 awards the unified key only and does not double-award legacy aliases.

No RLS Lua, UI, model, texture, configuration, or other asset was copied or replaced.

## v0.2.10 progression behavior

Every successfully completed RedFox towing job can now award:

- Repo XP;
- RedFox Tow & Recovery XP;
- Logistics XP;
- Beam XP;
- Labourer progression;
- Civil Service XP for police, DUI, and street-racing impounds;
- RLS inventory repossession count on the assigned service truck.

Supported job progression classes:

- Abandoned Recovery;
- Standard Tow;
- Rollover / Light Recovery;
- Heavy / Semi Recovery;
- Accident Scene Cleanup;
- Police Impound;
- Street-Racing Impound;
- DUI Checkpoint Impound.

XP scales by:

- job category;
- response distance;
- loaded tow distance;
- workload units;
- recovered target count.

Heavy/semi recovery and multi-vehicle accident cleanup award more Tow & Recovery and Logistics XP than a short standard tow.

## New RedFox skill

```text
Display name: Tow & Recovery
Attribute key: careerSkills-towing
Levels: 1-50
Order: 71
Definition: gameplay/domains/careerSkills/skills/towing/info.json
```

The skill definition is RedFox-owned and uses its own progression curve and milestone text.

Category XP configuration:

```text
gameplay/redfox_tow_recovery_dispatch/progressionConfig.json
```

## UI/history changes

Active calls and History now display:

- progression class;
- Repo XP;
- Tow & Recovery XP;
- Logistics XP;
- Beam XP / Labourer;
- Civil Service XP where applicable.

## Static verification

- ZIP integrity: PASS.
- Direct-root layout: PASS.
- Duplicate ZIP entries: none.
- Lua loadfile/local-variable limit: PASS.
- Top-level progression smoke test: PASS.
- All eight job types produce Repo XP: PASS.
- All eight job types produce Tow & Recovery XP: PASS.
- All eight job types produce Logistics XP: PASS.
- Distance scaling: PASS.
- Heavy/semi scaling above standard tow: PASS.
- JSON parsing: PASS.
- 50-level monotonic skill thresholds: PASS.
- Protected Career/RLS override-path scan: PASS.
- Native executable/library scan: PASS.
- RLS source/assets bundled: NO.
- BeamNG/RLS runtime: **UNTESTED**.

## Required runtime test

1. Disable every older JOB-09 ZIP, including v0.2.9.
2. Enable only v0.2.10 on a disposable RLS Career save.
3. Open Career Paths > Skills and confirm **Tow & Recovery** appears.
4. Record Repo, Tow & Recovery, Logistics, Civil Service, Beam XP, and Labourer values.
5. Complete one of every RedFox call type.
6. Confirm every completed call increases Repo, Tow & Recovery, Logistics, Beam XP, and Labourer.
7. Confirm police/DUI/street-racing calls also increase Civil Service.
8. Compare short versus long standard tows; longer work should award more XP.
9. Compare standard tow versus semi recovery; semi recovery should award more Tow & Recovery and Logistics XP.
10. Confirm History records the full XP breakdown.
11. Save/reload and confirm progression persists.
12. Return `beamng.log` around any missing-skill, reward, payment, or persistence failure.

## Deliberately not included

- company fleet storage;
- personal/business vehicle transfer;
- company bank routing;
- fleet insurance;
- tow invoice popup/archive;
- World Editor Scene Builder.

These remain separate work. v0.2.10 is a progression-focused candidate.