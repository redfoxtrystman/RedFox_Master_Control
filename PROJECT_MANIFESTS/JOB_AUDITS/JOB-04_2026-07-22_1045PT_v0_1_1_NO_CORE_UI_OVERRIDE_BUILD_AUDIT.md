# JOB-04 Scrap Yard / Wrecking Yard — Build Audit

**Timestamp:** 2026-07-22 10:45 Pacific Time  
**Build:** v0.1.1 NO CORE UI OVERRIDE  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** Static package created. Runtime unproven until David tests in BeamNG.

## Output ZIP

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_2026-07-22_1045PT_v0_1_1_NO_CORE_UI_OVERRIDE.zip
```

## Source ZIP

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0(2).zip
```

## Why this build was made

David reported that the v0.1.0 Scrap Yard WebUI test build caused BeamNG to refuse loading the title/background screen and then show a grey screen after load.

Inspection found this high-risk file in the package:

```text
ui/ui-vue/dist/index.js
```

That file is a global BeamNG Vue UI override, not a Scrap Yard-only page file. A broken or stale version can break the main title/menu UI.

## Fix applied

Removed:

```text
ui/ui-vue/dist/index.js
```

Kept intentionally:

```text
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfox_scrapyard_webui_test.lua
ui/modModules/redfoxCareerWeb/
sites/scrap_yard/
sites/scrap_yard_webui_test/
```

Old root-level reports from previous builds were removed so this ZIP only has current timestamped reports.

## Static verification

```text
ZIP integrity: PASS
Entry count: 924
SHA256: feceb334daa5ea3a1d0c954cf510db3b04fea6938db8fef61885d77ac8772067
ui/ui-vue/dist/index.js absent: PASS
No redfoxScrapYardDirect name hits: PASS
No startup ScrapYard Direct career module: PASS
Required Scrap Yard WebUI test files present: PASS
Relevant JavaScript syntax checks: PASS
No __pycache__ / .pyc: PASS
```

## Included current reports

```text
CHANGE_SCOPE_JOB04_2026-07-22_1045PT_v0_1_1_NO_CORE_UI_OVERRIDE.txt
OPEN_THIS_VERIFICATION_REPORT_JOB04_2026-07-22_1045PT_v0_1_1.txt
OPEN_THIS_VERIFICATION_REPORT_JOB04_2026-07-22_1045PT_v0_1_1.html
VERIFY_JOB04_2026-07-22_1045PT_v0_1_1.json
VERIFY_JOB04_2026-07-22_1045PT_v0_1_1_FILE_INVENTORY.csv
FILE_TREE_JOB04_2026-07-22_1045PT_v0_1_1.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
```

## Required test instructions for David

1. Remove or disable every other `zzzz_RedFox_FoxNet_Web_Ecosystem...zip`.
2. Remove or disable every old `RedFox_ScrapYard_Direct...zip`.
3. Install only this ZIP plus RLS.
4. Start BeamNG.
5. First confirm the title/menu/background loads normally.
6. Start Career mode.
7. Try IceFox/RedFox access.
8. Open Scrap Yard.
9. Open Scrap Yard WebUI Test Panel.
10. Click `Check Status` and `Load RLS Shop Data`.
11. Send `beamng.log` if anything fails.

## Important warning

Runtime is still unproven. Removing the core Vue UI override should address the grey title/menu risk, but it may affect how the PC/phone entry point appears. If the game loads normally but the RedFox/IceFox entry point is missing, that is the next thing to patch.
