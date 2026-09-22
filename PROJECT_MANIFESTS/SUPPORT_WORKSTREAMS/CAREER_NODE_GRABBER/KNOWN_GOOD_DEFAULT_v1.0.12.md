# Known-Good Default — RedFox RLS Career Full Toolkit v1.0.12

**Status:** DEFAULT / KNOWN-GOOD / ROLLBACK BASELINE  
**Do not replace this baseline with a test build unless David explicitly approves it after runtime testing.**

## Exact baseline package

`RedFox_RLS_Career_Full_Toolkit_v1.0.12_RELEASE_CANDIDATE_TEST.zip`

SHA-256:

`a2accec6e293e1ca41ec8e8a0b7c82688647ea561e53d6d6cb460f3816f6bb23`

## Baseline decision

David confirmed the v1.0.12 build is the current working version and requested that it become the new default before the seated-camera Node Grabber fix is tested.

Future patches must be built from this exact baseline unless David explicitly changes the baseline.

## Known-good behavior at baseline

- RLS 2.7.1 Career loads.
- Node Grabber works in Free Camera.
- Grabber defaults OFF.
- Tiny DEV button/manual dev unlock system is present.
- Money changes work without triggering the unwanted trillion-dollar cheat behavior.
- Broader dev tools are available through the manual activation flow.
- No old RLS `career.lua` override is bundled.

## Known limitation carried into baseline

When seated inside a vehicle, Ctrl can show Node Grabber nodes but a left-click may be consumed by the vehicle camera / RLS camera-change path instead of beginning a grab. Free Camera works correctly.

This limitation is being tested separately in v1.0.13. It does **not** change the default baseline until David verifies it.

## v1.0.13 test delta

The v1.0.13 seated-camera test was generated directly from this v1.0.12 baseline.

Only these files differ:

- `lua/ge/extensions/redfox/grabberUi.lua`
- `mod_info.json`
- `CHANGELOG.txt`

No money, teleport, photo, insurance, XP, garage-add, repair, UI asset, or other toolkit code was changed.

## Backup note

The exact package hash above is the authority for identifying the known-good v1.0.12 ZIP. Keep an untouched copy of that ZIP as the rollback package.
