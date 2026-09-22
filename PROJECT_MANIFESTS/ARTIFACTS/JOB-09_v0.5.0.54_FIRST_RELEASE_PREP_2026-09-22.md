# JOB-09 v0.5.0.54 — FIRST RELEASE PREP RELEASE CANDIDATE — 2026-09-22

Baseline: exact owner-promoted v0.5.0.53 default artifact.

## Artifact
- Filename: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_5_0_54_FIRST_RELEASE_PREP_RLS_NATIVE_RECOVERY_HELP_SETTINGS.zip`
- SHA-256: `650e98a8ba48631f73eead95b1970a72232b27f8b6834751cdb71cc32f55d7b3`
- Status: **STATICALLY VERIFIED / RUNTIME UNTESTED**
- Do not promote over v53 until owner runtime gates pass.

## RLS source reference
Exact RLS Career Overhaul 2.7.1 native `lua/ge/extensions/gameplay/offroadRecovery.lua`:
- SHA-256: `28c23c59925d911e9e494b2d90ff3ee21549a81add53d0e1a83f7d06464b8540`

v54 restores the native RLS site/vehicle path and adds only RedFox destination/safety compatibility around it.

## Main changes
- RLS 2.7.1 owns Recovery pickup sites and eligible vehicle selection again.
- Native RLS Recovery Yards remain native; RedFox Tow Yards are append-only extra Recovery delivery choices.
- Immediate failed target spawn does not leave a ghost job.
- Fresh accepted targets have a 30-second second-stage setup watchdog; saved/restored jobs are excluded.
- Shared Job Board preferred for Car Lot repos, legacy board retained as fallback.
- Legacy repo poll default reduced from every second to 10 seconds; board events can trigger immediate sync.
- Optional extension load attempts use retry backoff.
- Settings schema 21 and First-Release Basics UI added.
- In-game Help / Instructions page and detailed release guide added.
- Recovery Equipment remains separate.

## Exact v53 -> v54 scope
Only 7 paths changed/new:
1. `README_REDFOX_TOW_RECOVERY.txt`
2. `docs/JOB09_v0_5_0_54_FIRST_RELEASE_PREP.md`
3. `docs/REDFOX_TOW_RECOVERY_FIRST_RELEASE_GUIDE.md`
4. `lua/ge/extensions/gameplay/offroadRecovery.lua`
5. `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
6. `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
7. `mod_info/redfox_tow_recovery_dispatch/info.json`

22 v53 files remain byte-identical.

## Verification
- 7 Lua files syntax-load clean through liblua5.4.
- 3 JSON files strict-parse clean.
- 2 JS files pass `node --check`.
- Initial verification caught the Lua 200-local limit; release helper was moved off a top-level local slot and the final source compiles cleanly.
- Final ZIP `unzip -t` clean.
- No duplicate ZIP paths.
- Direct BeamNG root preserved.
- Exact final ZIP re-extracted: 29 files, zero missing, zero extra, zero byte differences against verified work tree.

## Runtime gates before promotion
1. RLS Recovery offer uses real RLS site + eligible vehicle.
2. Accepted target visibly spawns.
3. Failed spawn/setup leaves no ghost job.
4. Native RLS Recovery Yard completes RLS Recovery.
5. RedFox Tow Yard completes RLS Recovery.
6. Ordinary RedFox Tow job can complete at imported native RLS Recovery Yard.
7. Help/Settings work and persist.
8. Shared Job Board surfaces eligible Car Lot repo.
9. No one-second repo/load spam.
