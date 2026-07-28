# JOB-09 v0.3.5 — Complete Scene Roster and Target Variety Build Audit

Date: 2026-07-27

## Artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_5_CompleteSceneRosterTargetVariety.zip`

- SHA-256: `d4808a12ff46497dcc5af0ac19d9c0ec3962a8fc669157b2614e845196f6d1e8`
- Size: 241,986 bytes
- ZIP integrity / CRC: PASS
- Case-insensitive duplicate ZIP entries: none
- Metadata version: 0.3.5
- Status: **BUILT — STATIC VERIFIED — RUNTIME PENDING DAVID**

## Runtime issue addressed

David received the same saved rollover target configuration four times consecutively. A police support vehicle that had been repositioned and saved also failed to appear on a later saved-scene replay.

## Root causes

1. Saved layouts replayed the exact captured tow-target model/configuration.
2. Saved layouts are weighted heavily in `Prefer Saved`, so one saved rollover template repeatedly forced the same target.
3. Saved support/equipment failures were silently skipped.
4. Manual replay deleted the current scene before the replacement roster was proven complete.
5. Replayed emergency support could be recaptured as generic equipment and lose its support flag.

## Corrections

- Saved tow targets are now same-class layout slots by default.
- Existing recent exact-configuration and model cooldowns apply to saved-scene target rerolls.
- Existing v0.3.3/v0.3.4 templates automatically use the corrected behavior without destructive migration.
- Included police, fire/EMS/support vehicles, cones, signs, barricades, debris, and other saveable props are an exact required roster.
- Any required roster spawn failure rejects the saved scene instead of presenting a partial scene.
- Saved emergency support keeps its identity and light activation through replay and re-save.
- Saved emergency support prevents an additional random police-support roll.
- Manual replay stages the replacement and keeps the current scene unchanged when the new roster cannot be built completely.

## Static checks

- Lua parse with `luatex loadfile`: PASS
- Mocked top-level Lua execution: PASS
- JSON parsing: PASS
- Main extension, mod metadata, and Hub module version consistency: PASS
- Packaged re-extraction and inventory hashes: PASS
- Required saved-roster failure markers: PASS
- Same-class target reroll and recent-selection markers: PASS
- Garage Hub contract and eight top navigation sections: PASS
- Company transfer and legacy retrieval safety locks: PASS
- Protected stock Career/RLS path scan: PASS

## Runtime proof required

1. Replay the existing saved rollover layout several times and confirm the exact target does not repeat four times consecutively under normal eligible-pool conditions.
2. Save a rollover layout containing one police car.
3. Confirm every successful replay contains the police car in its saved relative position.
4. Confirm no second random police car is added.
5. Confirm a missing required support/prop causes replay failure rather than partial success.
6. Confirm failed manual replay leaves the current scene unchanged.

No DAVID-TESTED WORKING claim is made.