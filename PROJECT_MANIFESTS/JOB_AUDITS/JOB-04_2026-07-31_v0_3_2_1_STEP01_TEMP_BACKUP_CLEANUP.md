# JOB-04 v0.3.2.1 — Step 01 Temp-Backup Cleanup Audit

## Status

- Build: **PACKAGED / STATIC VERIFIED / RUNTIME UNPROVEN**
- Source baseline: v0.3.2 owner-tested PASS
- Source SHA-256: `874f817f61bf7c32498d92f0a29d2c34ff1b5d6a01203a3ec94729d86e03cf76`
- Output SHA-256: `c709444eb71f088a97eb25a04f9d572d81eab5c83609e76f1491c7f9b76bb129`
- Output file: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_1_STEP01_TEMP_BACKUP_UNUSED_PAGES_RECORDS_FROM_v0_3_2.zip`

## Owner-confirmed source behavior

The exact v0.3.2 source was confirmed by David to:

- load Career;
- show the correct owner-edited FoxNet phone icon;
- load the styled welcome page;
- load the styled Wrecking Yard quickly;
- show the approved junk/high-mileage inventory;
- complete purchases.

This exact source is the rollback baseline.

## Step 01 scope

No live welcome-page, browser, icon, route, Lua, purchase, or Wrecking Yard file was edited.

The following were moved from their original active paths into:

`REDFOX_TEMP_BACKUP_DO_NOT_LOAD/STEP_01/`

- nine non-JOB-04 site implementations from both website trees;
- root historical reports/readmes;
- root `docs/` development tree;
- shared module docs/readmes/verification manifests.

Every moved file retains its original path below the backup prefix and is byte-identical to the source.

## Counts

- Source files: **1,017**
- Live files remaining at original runtime paths: **177**
- Files moved into temp backup: **840**
- New backup manifest/readme files: **3**
- Total ZIP entries: **1,020**

The ZIP remains about the same size because backups are intentionally still inside it. The test is whether moving those files out of active BeamNG paths preserves behavior and reduces active WebUI/module clutter.

## Moved site groups

| Site | Files moved from both mirrors |
|---|---:|
| BeamBook page implementation | 56 |
| Collector Exchange | 60 |
| Export Yard | 96 |
| FoxFax | 22 |
| FoxNet Auctions | 112 |
| Parts Exchange | 78 |
| RedFox Recovery | 72 |
| UndergroundNet | 94 |
| XXX Insurance | 68 |

The welcome-page cards/navigation were not edited. Other jobs must later provide their current page files at coordinated routes.

## Protected working content

Kept byte-for-byte:

- root welcome page and all shared assets;
- owner-edited `foxnet-browser.svg`;
- phone layout;
- main Vue UI bundle;
- `redfoxCareerWeb.lua`;
- all JOB-04 Lua;
- both full Wrecking Yard mirrors;
- v0.3.2 page, JavaScript, configuration, catalog, images, native IDs, prices, and purchase path;
- root About/Legal/Underground pages.

## Verification

All checks passed:

- source hash matched frozen baseline;
- output ZIP integrity;
- no duplicate paths;
- no unsafe paths;
- all **177** kept live files byte-identical;
- all **840** moved files byte-identical under backup path;
- no moved file remained at its original active path;
- protected live paths present and byte-identical;
- both 35-file Wrecking Yard mirrors complete and identical;
- owner icon hash preserved: `7a835b81ab12dad2301aae4016c1c79ba8d5dab6818e66179b1bad0404056f08`;
- active JSON parsing passed;
- essential welcome/Wrecking Yard HTML asset references exist;
- 17 active JavaScript files passed `node --check`;
- 7 active Lua files passed non-empty/structural checks;
- fresh extraction contained 1,020 files.

No standalone Lua compiler/parser was available, but no Lua file was edited in this build and all live Lua hashes match the owner-tested source.

## Runtime test gate

Test only this ZIP with all other JOB-04/Core split builds disabled.

Required checks:

1. Career loads.
2. Correct FoxNet icon remains.
3. Welcome page style remains.
4. Wrecking Yard v0.3.2 style remains.
5. Inventory loads fast.
6. One inexpensive purchase still completes.
7. Closing/opening the browser does not introduce new lag.
8. Do not judge the moved non-JOB-04 pages yet; their active implementations are intentionally in the temp backup.

If this passes, Step 02 may permanently remove this backup group into an external records archive or begin the next single cleanup group. If it fails, restore the exact original paths from the embedded manifest.
