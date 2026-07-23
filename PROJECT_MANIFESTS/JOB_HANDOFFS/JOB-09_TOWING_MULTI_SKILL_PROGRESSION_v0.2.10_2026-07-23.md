# JOB-09 — Towing and Multi-Skill Progression v0.2.10

**Date:** 2026-07-23  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**

## Exact package

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_10_TowingMultiSkillProgression.zip
Size: 197,466 bytes
SHA-256: b5c4cc4baf0ebea55c8bb6813eb9fdff7b4d78f4a74473fd035cbed797b29c48
```

Source baseline:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_ActiveCallRecoveryAlertsDamage.zip
SHA-256: 95722351456b6caeb51b448a624bdb33ae4b89e17e45df5fa77a85b6439ea1f2
```

The installable ZIP remains in the active ChatGPT JOB-09 workspace and is not committed to GitHub as a binary.

## Exact RLS reference inspected

David supplied `1(1).zip`, embedded **RLS Career Overhaul 2.6.8**.

Confirmed progression keys:

- `careerSkills-repo`
- `logistics-delivery`
- `careerSkills-civilService`
- `labourer`
- `beamXP`

RLS discovers additive Career skill definitions from:

```text
/gameplay/domains/careerSkills/skills/*/info.json
```

No RLS Lua, UI, model, texture, or original skill file is copied or overwritten.

## Dedicated Towing skill

v0.2.10 adds:

```text
/gameplay/domains/careerSkills/skills/towing/info.json
attributeKey: careerSkills-towing
levels: 50
```

The level thresholds follow the installed RLS 2.6.8 50-level Career-skill curve for consistent UI pacing. This is a new RedFox-owned additive skill and contains no RLS unlock flags.

## Progression behavior

Every successfully completed RedFox Tow call now queues:

- Towing XP;
- Repo XP;
- Logistics XP for transported/recovered vehicles;
- Labourer progression;
- Beam XP;
- Civil Service XP when the call is police/emergency/public-service work.

Unpaid and held outcomes still award progression when the physical recovery work is completed.

Rewards scale with:

- response distance;
- loaded/tow distance;
- workload units;
- target count;
- call/recovery type.

## Call weighting

| Call | Towing | Repo | Logistics | Civil Service |
|---|---:|---:|---:|---:|
| Standard tow | 1.00x | 0.90x | 0.75x | — |
| Abandoned recovery | 1.05x | 1.35x | 0.80x | — |
| Rollover recovery | 1.35x | 1.05x | 0.90x | 0.25x |
| Semi/heavy recovery | 1.90x | 1.25x | 1.80x | 0.30x |
| Accident cleanup | 1.65x | 1.05x | 1.20x | 0.60x |
| Police impound | 1.00x | 1.45x | 0.70x | 1.00x |
| Street-racing impound | 1.35x | 1.65x | 0.85x | 1.20x |
| DUI checkpoint | 1.05x | 1.50x | 0.70x | 1.10x |

Logistics emphasizes loaded distance and heavy/multi-vehicle transport. Semi/heavy recovery receives the largest hauling weight.

## UI and history

The active call now previews:

- Career skill category;
- Towing XP;
- Repo XP;
- Logistics XP;
- Civil Service XP where applicable;
- Beam XP and Labourer progression.

The completion popup reports awarded skill values. Tow History stores and displays the same breakdown.

## Static verification

- ZIP integrity: PASS.
- Direct-root layout: PASS.
- Duplicate ZIP entries: none.
- Lua loadfile/local-variable limit: PASS.
- Top-level stub execution: PASS.
- JSON parsing: PASS.
- Towing skill schema and 50 levels: PASS.
- All eight call types present in reward matrix: PASS.
- Every call type produces positive Towing, Repo, and Logistics XP in static reward tests: PASS.
- Heavy recovery weighted above standard tow for Towing and Logistics: PASS.
- Protected Career/RLS override-path scan: PASS.
- Native executable/library scan: PASS.
- RLS source/assets bundled: NO.
- Packaged inventory checksum validation: PASS.
- BeamNG/RLS runtime: **UNTESTED**.

## Required runtime test

1. Disable every older JOB-09 ZIP, including v0.2.9.
2. Enable only v0.2.10 on a disposable RLS Career save.
3. Open Career Paths → Skills and confirm **Towing** appears.
4. Complete every Tow call type and verify expected skill categories increase.
5. Compare short versus long and light versus heavy jobs.
6. Confirm unpaid/held work still awards progression.
7. Confirm active-call preview, completion popup, Tow History, and save persistence.
8. Regression-test v0.2.9 active-call recovery, validation, alerts, target damage, and v0.2.8 storage/claim systems.

## Deliberately not included

- Company fleet storage.
- Tow Yard → business inventory transfer.
- Personal ↔ business transfer.
- Company bank routing/insurance/branches/sale protection.
- Invoice popup/archive.

Those remain separate because vehicle-ownership transfer requires rollback-safe testing with a disposable vehicle.
