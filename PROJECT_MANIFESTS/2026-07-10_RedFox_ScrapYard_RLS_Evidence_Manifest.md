# RedFox Scrap Yard / RLS Evidence Manifest

**Created:** 2026-07-10  
**Project/chat:** RedFox IceFox web pages, Scrap Yard, missions, RLS career bridge  
**Repository:** redfoxtrystman/RedFox_Master_Control

## Purpose

Preserve what the uploaded RedFox/RLS files are for, which ones are testable mods, and which ones are documentation/evidence packs. This exists so future chats can recover the project state without David repeating the whole plan.

## Important distinction

- **Evidence/inspect ZIPs are not mods to test in BeamNG.** They are reports, CSV indexes, file inventories, and code evidence.
- **Testable RedFox baseline:** `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_9_9_PHONE_SCRAP_OPTIMIZED.zip` is the current phone-working RedFox web baseline to preserve and patch.
- **RLS/source archives:** RLS ZIPs are reference/dependency/source material. Do not edit RLS originals unless David explicitly approves it.
- **Current evidence pack created in chat:** `RedFox_RLS_Evidence_v03.zip` / `RedFox_RLS_All_Current_Code_Evidence_ScrapYard_BuySell_INSPECT_v0_3.zip`. This is not a BeamNG mod.

## Current uploaded/test/reference files

### `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_9_9_PHONE_SCRAP_OPTIMIZED.zip`

- Purpose: **TESTABLE REDFOX BASELINE.** Current phone/IceFox web ecosystem baseline. Contains phone launcher/connector and Scrap Yard page. Scrap Yard selling/stripping is read-only in this build.
- SHA256: `9aa91c1328ffb8cfa7ffe176c16929751cc30666f37ccc14f0cba5a246809abc`
- ZIP integrity: PASS
- Evidence lines found: 6,051

### `west_coast_usa.zip`

- Purpose: **REFERENCE DATA.** West Coast map/facility/location data for pickup jobs, scrapyard/industrial locations, port/export areas, parking/spawn/delivery points.
- SHA256: `1d3d42019feec41919565deb28be9e0ac6443f82504c8dab3be7a94e03cc3406`
- ZIP integrity: PASS
- Evidence lines found: 51,587

### `rls_career_overhaul_2.6.6.zip`

- Purpose: **REFERENCE / MAIN RLS OVERHAUL SOURCE.** Main career overhaul code used to find vehicle shopping, auctions, car lots, values, storage, facilities, money, and career hooks. Do not edit originals.
- SHA256: `b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b`
- ZIP integrity: PASS
- Evidence lines found: 48,470

### `rls_RaceTab_Release.zip`

- Purpose: **REFERENCE VEHICLE/PART SOURCE.** RaceTab vehicle parts/JBEAM source; useful for parts evidence and engine/transmission references, not primary Scrap Yard logic.
- SHA256: `d7b83e10624ecb159c92a6b821f0c3b432ea6881e2860d9a5696b83ae344c5e6`
- ZIP integrity: PASS
- Evidence lines found: 8,810

### `rls_career_collection_5.2_beta.zip`

- Purpose: **REFERENCE RLS CAREER COLLECTION.** Source/reference for career systems, missions, economy, storage, auctions, and buy/sell hooks.
- SHA256: `2c856e5f58dde61d1080cc5f07235b37f34f1a632a2a827e426636546dc81f48`
- ZIP integrity: PASS
- Evidence lines found: 19

### `rls_realcargo.zip`

- Purpose: **REFERENCE / POSSIBLE DEPENDENCY.** Cargo/delivery/facility systems useful for abandoned car pickup, towing/removal jobs, destinations, and logistics.
- SHA256: `0ed605228d2818d9b744656c51eaf65ee729f6c1760b6dbd4e00b1f693080474`
- ZIP integrity: PASS
- Evidence lines found: 10,368

### `rls_same_axle_hybrid_system_1.0.zip`

- Purpose: **REFERENCE VEHICLE SYSTEM.** Hybrid/powertrain code; not primary Scrap Yard logic but may inform engine/powertrain handling.
- SHA256: `41a3aa7299b8e77870658d9a421874ba9779de1d75db59df37eed61f14ce2050`
- ZIP integrity: PASS
- Evidence lines found: 810

### `rls_slop_gear_garage_v0.2.zip`

- Purpose: **REFERENCE GARAGE/GEAR SOURCE.** Possible shop/garage related functions.
- SHA256: `6ef61e06c925924c32fc9f1cb1b1d1b16a8ba496f9a4d17039a68f625712427e`
- ZIP integrity: PASS
- Evidence lines found: 1,052

### `rls_vehicle_editor_modland326748.zip`

- Purpose: **REFERENCE TOOL SOURCE.** Vehicle info/editor utility, may help read/understand vehicle data.
- SHA256: `12bdf5eaee6fe3121da728c8fc8bdcfa61da393c731179990b074e5629610c15`
- ZIP integrity: PASS
- Evidence lines found: 896

### `RedFox_RLS_Career_Dev_Unlocker_v0_1_0.zip`

- Purpose: **REDFOX DEV TOOL / POSSIBLE TEST MOD.** Unlock/helper utility for RLS career development.
- SHA256: `7da978c62673963f01ecb24cfb0e1a84d8520ce240bd4af31dc757ee7bc95166`
- ZIP integrity: PASS
- Evidence lines found: 82

### `backAlley.0.2.2-alpha.zip`

- Purpose: **REFERENCE / POSSIBLE GAMEPLAY SOURCE.** Car theft/back alley job code useful for underground jobs, illegal storage, pickup/repo-like mission patterns.
- SHA256: `a9b0d80c32570413bab64b51b529a1cfc3675a19891133c41d37ba89bc2f99e9`
- ZIP integrity: PASS
- Evidence lines found: 3,192

## Evidence pack contents

`RedFox_RLS_Evidence_v03.zip` contains:

- `OPEN_THIS_FIRST_SUMMARY.txt`
- `OPEN_THIS_ALL_CURRENT_RLS_CODE_EVIDENCE_REPORT.html`
- `OPEN_THIS_ALL_CURRENT_RLS_CODE_EVIDENCE_REPORT.md`
- `RLS_CODE_EVIDENCE_HELPFUL_LINES_FULL.csv`
- `WEST_COAST_LOCATION_FACILITY_EVIDENCE.csv`
- `RLS_FILE_INVENTORY_HASHED_ALL_ENTRIES.csv`
- `archive_summaries.json`
- `scan_errors.json`
- `GITHUB_MANIFEST_RedFox_ScrapYard_RLS_Evidence.md`

## Counts from v0.3 evidence scan

- Archives scanned: 11
- Evidence lines: 131,337
- West Coast location/facility lines: 44,937
- Hashed inventory entries: 2,439
- Scan errors: 0

## Evidence line counts by system

- `buy_sell_market_auction`: 16,073
- `insurance_damage_condition`: 8,684
- `missions_jobs_repo_pickup`: 18,307
- `parts_partout_engine_transmission`: 12,538
- `scrap_sell_vehicle_money`: 5,800
- `storage_garage_property`: 11,597
- `ui_phone_bridge`: 14,504
- `west_coast_locations_facilities`: 89,007

## Highest-value source files

- `west_coast_usa.zip` → `main/MissionGroup/DecalRoads/items.level.json` — 4,763 useful lines
- `west_coast_usa.zip` → `city.sites.json` — 2,703 useful lines
- `rls_realcargo.zip` → `levels/italy/facilities/delivery/local.facilities.json` — 2,237 useful lines
- `west_coast_usa.zip` → `main/MissionGroup/StaticObjects/items.level.json` — 1,946 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/career/modules/business/racingTeam.lua` — 1,546 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/career/modules/usedCarAuction.lua` — 1,270 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/overrides/career/modules/vehicleShopping.lua` — 1,109 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/overrides/career/modules/inventory.lua` — 1,002 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/overrides/career/modules/insurance/insurance.lua` — 835 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/career/modules/garageManager.lua` — 739 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/overrides/career/modules/marketplace.lua` — 495 useful lines
- `rls_career_overhaul_2.6.6.zip` → `lua/ge/extensions/gameplay/repo.lua` — 516 useful lines
- `backAlley.0.2.2-alpha.zip` → `lua/ge/extensions/carTheft/main.lua` — 557 useful lines
- `backAlley.0.2.2-alpha.zip` → `lua/ge/extensions/carTheft/jobManager.lua` — 467 useful lines

## Required next build law

Before building the working Scrap Yard:

1. Use `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_9_9_PHONE_SCRAP_OPTIMIZED.zip` as the baseline unless David gives a newer phone-working baseline.
2. Inspect before editing.
3. Preserve the phone/IceFox launcher.
4. List exact files to edit and exact files not to touch.
5. Patch only Scrap Yard and a RedFox bridge module.
6. Do not edit RLS originals.
7. First action to make real: quote + sell whole car for scrap with confirmation.
8. After editing, compare changes against baseline.
9. Reopen final ZIP and verify exact files inside.
10. Label runtime as unproven until David tests in BeamNG.
