# JOB-09 — RLS Progression + Personal Claims v0.2.7

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Module:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**  
**Ownership note:** This file is a build record only. It is not a handoff.

## Package

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_RLSProgressionPersonalClaims.zip
Size: 138,580 bytes
SHA-256: a34ed2660e6bf69ad86722c16114f3fe0989422dca4f65cfb3cd5f49a156fd73
```

Baseline:

```text
v0.2.6 Police Impound + Emergency Scenes
SHA-256: 82eecc0652d61cc8b6d203d0bf7eb541bdee95532e8c82c2b2ecd59c0a0b2dbd
```

The installable package remains in the active ChatGPT workspace; GitHub stores documentation and source-change records, not the binary ZIP.

## RLS 2.6.8 integration

David's supplied RLS 2.6.8 package was inspected to identify the exact public Career module names, skill keys, inventory methods, and reward behavior. No RLS code or assets are included in RedFox.

Detected/used systems:

- `careerSkills-repo`
- `careerSkills-civilService` where available
- `career_modules_payment`
- `career_modules_playerAttributes`
- `career_modules_difficultyMode`
- `career_economyAdjuster` section `repo`
- `career_modules_inventory.addRepossession`
- Career inventory ownership/garage APIs

## Reward/progression behavior

Each completed RedFox Tow event calculates a progression package based on:

- event type and workload;
- response and towing distance;
- number of targets;
- RLS Repo skill bonus;
- RLS economy/difficulty systems.

Possible rewards:

- money;
- Beam XP;
- Labourer progression;
- Repo XP;
- Civil Service XP for qualifying enforcement calls;
- repossession-count progression for the inventory tow vehicle used to accept the call.

Longer-distance and multi-target jobs are intended to pay and progress more. Runtime balancing is still required.

## Personal ownership claim

Tow Yard records that have completed their legal/storage hold can be transferred directly into the player's Career inventory using:

```text
Claim as My Personal Vehicle
```

The vehicle is transferred as owned, moved to a free private garage slot, and removed from the Tow Yard only after the inventory transfer succeeds. No sale payment is generated.

Claims are refused when:

- the hold has not expired;
- Career inventory is unavailable;
- no garage slot is free;
- vehicle retrieval or inventory transfer fails.

The Tow Yard record remains after a failed claim.

## Compatibility and fallback

- Vanilla/non-RLS Career still uses only attributes/APIs that are detected.
- Unknown skill attributes are not blindly written.
- Older pending payment records remain readable.
- v0.2.6 police/emergency functionality is preserved.
- No stock Career or RLS override paths are packaged.

## Verification

PASS:

- ZIP integrity and direct-root layout;
- Lua syntax/loading;
- JSON parsing;
- protected-path scan;
- native-binary scan;
- no bundled RLS source/assets;
- version consistency;
- inventory checksum validation;
- stubbed progression/payment processing;
- stubbed Tow Yard-to-Career claim path.

UNTESTED:

- actual BeamNG/RLS reward display;
- exact balance;
- Career inventory condition capture timing;
- garage transfer across all RLS maps/configurations;
- claim behavior for heavily deformed older yard records.

## Required runtime proof

Test v0.2.7 alone on a disposable RLS Career save. Compare a short and long tow, then test heavy/multi-target and police jobs. Verify Repo/Civil Service progression and finally claim an expired Tow Yard record into a private garage. Return `beamng.log` around any error.
