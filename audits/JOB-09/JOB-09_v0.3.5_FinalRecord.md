# JOB-09 v0.3.5 Final Record

Artifact built, packaged, re-extracted, and statically verified from the active sandbox.

- File: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_5_CompleteSceneRosterTargetVariety.zip`
- SHA-256: `d4808a12ff46497dcc5af0ac19d9c0ec3962a8fc669157b2614e845196f6d1e8`
- Size: 241,986 bytes
- ZIP files: 78
- Source inventory rows verified after re-extraction: 77
- Lua parse: PASS
- Mocked top-level execution: PASS
- JSON parsing: PASS
- ZIP CRC: PASS
- Duplicate paths: none
- Protected stock/RLS paths: none
- Packaged strict-roster and target-variety markers: PASS
- Static verification: PASS
- Runtime verification: PENDING DAVID

Primary fixes:

- Saved rollover targets reroll from the same class instead of forcing the captured exact configuration.
- Saved police/support/props are mandatory roster items; partial saved scenes are rejected.
- Failed manual replay preserves the current scene.