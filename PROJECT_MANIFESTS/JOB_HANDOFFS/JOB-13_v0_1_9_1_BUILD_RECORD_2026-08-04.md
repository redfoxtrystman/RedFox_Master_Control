# JOB-13 v0.1.9.1 Build Record

**Date:** 2026-08-04
**Branch:** `job13-online-auctions`

## Artifact

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_1_RECOVERY_FILTERS_CALMER_NPCS_MULTI_CONSIGNMENTS.zip`

SHA-256:

`178648f5b3b4588ba76350e53e9954c0aab979b4db5b9ef73149b17aac170ff7`

Base:

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_0_BANK_RESERVE_SELLING_CRASH_RECOVERY.zip`

Base SHA-256:

`58debecc1e7c2eb2257dcbb9d70e7c7265090063276159ebfa6129c10fbfefa0`

## Runtime reason for build

v0.1.9.0 did not restore auction state after reload. Additional user-confirmed defects were native CEF dropdown failure, excessive NPC competition, unclear seller market values, one-car consignment limit, and missing Wrecking Yard acquisition metadata.

## Changes

- Per-Career-save auction/account/ledger files under `career/rls_career/redfox_job13`.
- One-time migration from v0.1.9.0 global files.
- Structural recovery validation instead of strict catalog-pool rejection.
- Snapshot serial readback verification after each write.
- Career activation, save-slot, deactivation, save commit, and unload hooks.
- 30-second dirty active snapshot policy retained; no full write per NPC bid.
- Native category/sort selects replaced with custom CEF menus.
- Calmer NPC count, timing, response chance, and value limits.
- Current RLS market value and suggested seller prices displayed.
- Fixed consignment limit removed; overflow uses later future auctions.
- Read-only exact-inventory-ID lookup of JOB-04 Wrecking Yard purchases.
- No JOB-04, JOB-09, or shared FoxNet file changed.

## Triple verification

Gate 1 passed: exact base SHA, 19 files, no duplicate/unsafe paths.

Gate 2 passed: 12 JOB-13 files changed, JSON parsed, JavaScript syntax passed, Lua syntax compiled, mirrored HTML identical, recovery/filter/NPC/consignment invariants checked.

Gate 3 passed: fresh extraction matched all source hashes, ZIP CRC passed, duplicate paths 0, unsafe paths 0.

## Runtime status

**UNPROVEN.** Test recovery first: place one bid and maximum, wait 35 seconds, close normally, restart the same Career save, and verify the exact auction/bid/history/timer restore. Stop if recovery fails.
