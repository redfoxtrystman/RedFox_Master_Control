# JOB-04 Incident Amendment — Scrap Yard WebUI Test ZIP caused title/grey-screen time loss

**Date:** 2026-07-22  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Chat:** Scrap Yard / Wrecking Yard chat / Sol  
**Related incident:** `INCIDENT_REPORTS/JOB-04_2026-07-22_SCRAPYARD_WEBUI_TEST_PANEL_GREY_SCREEN_CORE_UI_OVERRIDE.md`

---

## User impact

David reported that the grey-screen/title-background failure took roughly **12 hours** to track down.

This was not acceptable. The failure wasted significant user time because the test ZIP included a global BeamNG core UI override that should have been flagged as high-risk before it was shipped.

---

## Confirmed bad package

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0.zip
```

This package must not be used as a valid test baseline.

---

## Primary suspected cause

The package included:

```text
ui/ui-vue/dist/index.js
```

That is a global BeamNG Vue UI override, not a Scrap Yard-only file.

A Scrap Yard WebUI/backend test package must not replace BeamNG's main Vue UI bundle unless there is a specific, inspected, approved reason and a rollback plan.

---

## Process failure

The assistant packaged a high-risk global UI override into what was supposed to be a JOB-04 Scrap Yard test panel.

That violated the project rule:

```text
Inspect first, edit second, and do not ship broad/global changes for a narrow feature test.
```

Static ZIP checks and syntax checks were not enough. They did not prove that the global UI override was safe.

---

## New hard rule for JOB-04

Until David explicitly approves otherwise, JOB-04 Scrap Yard test builds must not include:

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
```

unless the build purpose is specifically phone/platform integration and the file is inspected against the exact current baseline.

For Scrap Yard backend testing, keep the build narrow:

```text
lua/ge/extensions/redfox_scrapyard_webui_test.lua
sites/scrap_yard_webui_test/
ui/modModules/redfoxCareerWeb/sites/scrap_yard_webui_test/
sites/scrap_yard/
ui/modModules/redfoxCareerWeb/sites/scrap_yard/
```

No BeamNG core UI override.

---

## Required recovery build

Next valid JOB-04 build should be:

```text
JOB-04 v0.1.1 emergency no-core-UI build
```

Required removals:

```text
ui/ui-vue/dist/index.js
```

Recommended caution:

```text
Do not modify lua/ge/extensions/ui/phone/layout.lua in the emergency recovery build.
```

Required reports:

```text
CHANGE_SCOPE_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.txt
OPEN_THIS_VERIFICATION_REPORT_*.html
VERIFY_*.json
VERIFY_*_FILE_INVENTORY.csv
FILE_TREE_*.txt
LOGGING_AND_TESTING_README.txt
LOGGING_AND_TESTING_README.html
```

Required verification wording:

```text
Runtime unproven until David tests in BeamNG.
```

---

## Do not repeat

Do not package a global UI override into a narrow Scrap Yard test panel again.

Do not make David discover that kind of issue by trial and error.
