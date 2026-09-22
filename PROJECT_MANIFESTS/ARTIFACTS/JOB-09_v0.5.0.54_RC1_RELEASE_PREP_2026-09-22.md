# JOB-09 v0.5.0.54-RC1 — RLS Native Recovery / First Release Prep

**Built from default baseline:** v0.5.0.53  
**Status:** STATICALLY VERIFIED / HARNESS VERIFIED / RUNTIME UNTESTED

## Exact artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_5_0_54_RC1_RLS_NATIVE_RECOVERY_RELEASE_PREP.zip`

SHA-256:

`6a7cdb3995f37031ee210bac8dfe00b20fbd11f10b3c24a5f96ac5adebcfe5db`

## Scope

- Restore exact RLS 2.7.1 pickup-site loading.
- Preserve exact RLS 2.7.1 Recovery vehicle-pool and vehicle/spot selection.
- Keep RedFox Tow/Recovery Yards as additional delivery destinations only.
- Add a 20-second watchdog for brand-new accepted Recovery jobs whose target never becomes usable.
- Back off optional extension loading and legacy repo-board polling.
- Cache legacy repo-board path discovery per Career slot.
- Add release-oriented Settings, recommended preset, in-game Help, root README, and runtime test checklist.

## Exact v53 -> RC1 changed files

- `lua/ge/extensions/gameplay/offroadRecovery.lua`
- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `lua/ge/extensions/redfoxRepoBoardTow.lua`
- `lua/ge/extensions/core/input/actions/redfox_tow_recovery_dispatch.json`
- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
- `mod_info/redfox_tow_recovery_dispatch/info.json`
- `scripts/redfox_tow_recovery_dispatch/modScript.lua`

Added:
- `README_RedFox_Tow_Recovery.md`
- `docs/JOB09_v0_5_0_54_RC1_RLS_NATIVE_RECOVERY_RELEASE_PREP.md`
- `docs/JOB09_v0_5_0_54_RC1_RUNTIME_TEST_CHECKLIST.md`

## Verification

- All 7 Lua files syntax-load clean via Lua 5.4.
- All 3 JSON files parse clean.
- `loadRecoverySites()`, `buildVehiclePool()`, and `pickVehicleAndSpot()` match the exact owner-supplied RLS 2.7.1 source.
- Repo cache harness passes.
- Final ZIP integrity check passes with no duplicate paths.
- Exact final ZIP was re-extracted and byte-compared against the verified work tree with zero differences.

## Promotion gate

v0.5.0.53 remains the owner-approved rollback/default until the owner runtime-tests this exact RC and explicitly promotes it.
