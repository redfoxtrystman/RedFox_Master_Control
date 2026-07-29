# JOB-09 v0.4.2.1 Final Artifact Record

**Version:** 0.4.2.1  
**Purpose:** Emergency correction for all mission-generation failure introduced in v0.4.2.  
**Runtime status:** UNTESTED in BeamNG after correction.

## Exact artifact

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_2_1_AllMissionGenerationEmergencyHotfix.zip
SHA-256: e3c0662d1a2859febd9d500d995c1f4a5784544290210e202a8c5f65f950fc43
Size: 1,607,442 bytes
ZIP entries: 144
Files: 120
```

## Confirmed defect fixed

At `chooseDiverseByClass()`, the v0.4.2 code called the nonexistent global `dispatchClassName`, causing mission generation to abort. v0.4.2.1 calls `vehicleRules.dispatchClassName` instead.

## Static verification

PASS: CRC, Lua syntax, JavaScript syntax, JSON parsing, archive path safety, duplicate-entry scan, native-payload scan, regression assertion, and exact source/re-extraction hash comparison.

## Required user test

The first required test is an accepted **Abandoned Vehicle** request. Runtime success must not be claimed until David confirms the call becomes active and a scene spawns.
