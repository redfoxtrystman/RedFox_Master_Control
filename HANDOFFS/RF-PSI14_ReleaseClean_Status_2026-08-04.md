# RF-PSI14 — RedFox PSI Controller Release-Clean Status

Date: 2026-08-04
Chat ID: RF-PSI14
Module: PSI Controller / RedFox Tire Control
Status: NEEDS TEST — static/package verification only

## Current release-clean package

```text
14-RedFox_PSIController_v0_2_7_ReleaseClean.zip
```

Built from baseline:

```text
14-RedFox_PSIController_v0_2_6_APlusTirePressureCompat.zip
```

Final ZIP external verification from packaging chat:

```text
Size: 58,967 bytes
SHA-256: ea906f6065291f1d92ca4d8891aa4808f1baaf1c49429b195a36fbac8f10664f
```

## What changed in v0.2.7

This was a release cleanup package, not a gameplay feature patch.

Removed from release ZIP:

```text
REDFOX_DIFF_REPORT_v0_2_0.html
REDFOX_DIFF_REPORT_v0_2_1.html
REDFOX_DIFF_REPORT_v0_2_2.html
REDFOX_DIFF_REPORT_v0_2_3.html
REDFOX_DIFF_REPORT_v0_2_4.html
REDFOX_DIFF_REPORT_v0_2_5.html
REDFOX_DIFF_REPORT_v0_2_6.html
REDFOX_DIFF_SUMMARY_v0_2_0.txt
REDFOX_DIFF_SUMMARY_v0_2_1.txt
REDFOX_DIFF_SUMMARY_v0_2_2.txt
REDFOX_DIFF_SUMMARY_v0_2_3.txt
REDFOX_DIFF_SUMMARY_v0_2_4.txt
REDFOX_DIFF_SUMMARY_v0_2_5.txt
REDFOX_DIFF_SUMMARY_v0_2_6.txt
REDFOX_DIFF_ui_modules_apps_redfoxPSIQuickControls_app.js.txt
REDFOX_DIFF_ui_modules_apps_redfoxPSIQuickControls_app.json.txt
outdated development README text
```

Added/updated for release:

```text
RedFox_PSI_Controller_README.txt
mod_info/info.json
mod_info/icon.png
mod_info/images/README_ADD_3_IMAGES_HERE.txt
mod_info/RELEASE_CONTENTS_AUDIT.md
mod_info/FINAL_ZIP_VERIFICATION.txt
```

Preserved runtime/source/config/UI files from v0.2.6:

```text
lua/ge/extensions/core/input/actions/redfoxPSIController.json
lua/ge/extensions/redfox/modules/redfox_psi_controller/redfox_module.json
lua/ge/extensions/redfoxPSIController.lua
lua/ge/extensions/redfoxPSIControllerNative.lua
lua/ge/extensions/redfoxTireSealant.lua
lua/vehicle/extensions/auto/redfoxPSIController.lua
lua/vehicle/extensions/redfoxpartrepair.lua
scripts/redfoxPSIController/modScript.lua
settings/redfox/psi_controller_settings.json
settings/redfoxPSIController/config.json
ui/modules/apps/redfoxPSIController/app.js
ui/modules/apps/redfoxPSIController/app.json
ui/modules/apps/redfoxPSIQuickControls/app.js
ui/modules/apps/redfoxPSIQuickControls/app.json
```

## Static verification completed

- Input ZIP opened and inventoried.
- Every input file was classified KEEP or REMOVE.
- Clean release tree scanned before zipping.
- Final ZIP reopened and extracted to a clean folder.
- `unzip -t` passed.
- Final package has BeamNG paths at archive root; no accidental enclosing folder.
- JSON validation passed.
- Full GM UI JavaScript syntax passed.
- Compact GM UI JavaScript syntax passed.
- `mod_info/icon.png` exists and opens as a PNG.
- `mod_info/images/` exists with a placeholder for David's three preview images.
- Active runtime/UI source scan found no `setInterval`, `requestAnimationFrame`, `setTimeout(fetchStats)`, old no-pressure spam string, or REDFOX_DIFF artifact names.

## Runtime status

Not proven by the assistant. David still needs to test the exact v0.2.7 ZIP in BeamNG.

## David test checklist

1. Disable every older RedFox PSI Controller ZIP.
2. Install only `14-RedFox_PSIController_v0_2_7_ReleaseClean.zip`.
3. Install/enable the A+ Gladiator tire mod if testing that compatibility path.
4. Confirm BeamNG/mod manager sees `mod_info/icon.png` and package metadata.
5. Add `RedFox Tire Control` GM UI.
6. Add `RedFox PSI Quick Controls` GM UI.
7. Open WE/native PSI settings from the full GM UI.
8. Let all UIs idle for 5-10 minutes and watch for console spam.
9. Click Refresh once and verify all three UI surfaces update together.
10. Set PSI from full GM UI and verify the compact GM and WE UI update.
11. Set PSI from compact GM UI and verify the full GM and WE UI update.
12. Set PSI from WE/native UI and verify both GM UIs update.
13. Test A+ Gladiator tires specifically; if PSI still does not move, next work is a tire-specific adapter/proof, not packaging cleanup.
14. Test self-sealing ON by popping one tire; verify repair completes and hiss/green sealant stops.
15. Test tire-only remove, full wheel/rim remove, selected repair, and pop tire on a normal vehicle.
16. Test Career mode only after Freeroam does not spam or regress.

## Future release rule added

Created:

```text
PROJECT_MANIFESTS/REDFOX_RELEASE_ZIP_CLEANUP_LAW_2026-08-04.md
```

All chats preparing future RedFox release ZIPs should follow that law before delivering a package.

## Message-board block for Coordinator posting

```text
Timestamp = 2026-08-04 07:37 America/Los_Angeles
Chat ID = RF-PSI14
Chat Name = PSI Controller / RedFox Tire Control Chat
Message type = STATUS / HANDOFF
Assigned role = PSI Controller release-clean packaging owner
I read these files = RedFox_Module_Status_Table.csv, current PSI v0.2.6 zip, A+ Gladiator context from David, BeamNG mod_info/icon reference from current web search
I changed these files = RedFox_Module_Status_Table.csv
I created these files = PROJECT_MANIFESTS/REDFOX_RELEASE_ZIP_CLEANUP_LAW_2026-08-04.md, HANDOFFS/RF-PSI14_ReleaseClean_Status_2026-08-04.md
I delivered these files = 14-RedFox_PSIController_v0_2_7_ReleaseClean.zip
What I did = Built release-clean PSI package from v0.2.6. Removed development diff reports and stale readme text, preserved runtime/source/config/UI files, added mod_info/info.json, mod_info/icon.png, mod_info/images placeholder for David's three images, included release audit and final verification records inside mod_info, and created a repo-wide release ZIP cleanup law for future chats.
What the next chat needs to know = v0.2.7 is package cleanup only, not runtime proof. Active code is still the v0.2.6 A+ tire compatibility line. Do not call it working until David tests. Follow PROJECT_MANIFESTS/REDFOX_RELEASE_ZIP_CLEANUP_LAW_2026-08-04.md for all release ZIPs.
What David needs to test/check = Test v0.2.7 alone with older PSI zips disabled; verify icon/metadata appears, all three UIs sync, no idle console spam, A+ Gladiator tires respond if runtime-changeable, and self-sealing repair stops hiss/green sealant.
Coordinator action needed = yes
```
