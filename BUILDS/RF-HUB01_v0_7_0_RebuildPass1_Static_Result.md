# RF-HUB01 — GarageHub v0.7.0 Rebuild Pass 1 Static Result

**Date:** 2026-07-27 PDT  
**Project:** RedFox Garage Hub / WEUI control  
**Baseline:** `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`  
**Artifact:** `1-RedFox_GarageHub_v0_7_0_RebuildPass1.zip`  
**SHA-256:** `804b32d7baa976fbd98f98548ea658872edbc8e9c3f9c8bc333e4bb91fa4d9ef`  
**Status:** STATIC VERIFICATION PASSED; BEAMNG RUNTIME UNTESTED

## Version decision

The hybrid rebuild advances to `v0.7.0` rather than resetting to `v0.1.0` because it remains the same GarageHub app, preserves the same extension/settings/theme-provider lineage, and GitHub already contains `v0.6.x` CleanCore records. `v1.0.0` remains reserved for a stable runtime-proven release.

## Implemented in Pass 1

- Preserved shared WEUI theme/font/readability behavior.
- Preserved `getGlobalUISettings()` for explicit RedFox theme inheritance.
- Removed the visible fixed Spawner/Race/Flood/Infection/VTOL/Tire/Gravity dropdowns.
- New visible top bar: `Hub | Apps/Windows | Theme | Help | [-]`.
- Added mounted regular Control-action JSON scanner.
- Added candidate `Test`, `Add to Hub`, and `Ignore` workflow.
- Nothing from the action scanner is approved automatically.
- Added Apps/Windows Manager containing only mounted RedFox manifests and user-approved actions.
- Added per-app `Minimize with Hub`, `Keep Open`, and `Restore with Hub` settings.
- Added visible selected-group button and `Alt+M` action.
- Retained `Alt+G` for GarageHub.
- Safe minimize skips apps without an explicit proven close/minimize function.
- Restore set contains only apps the Hub successfully closed.
- Active legacy guessed adapter registry is empty; baseline registry is archived.
- Legacy Manual Link and Menu Manager code is retained for rollback/reference but is not exposed or drawn.
- Legacy manual links are excluded from startup.
- Display-name guessing is disabled for connected apps; opening requires an explicit manifest function or approved action.

## Modified package files

- `lua/ge/extensions/redfox/modulesHub.lua`
- `lua/ge/extensions/auto/redfoxModulesHubAuto.lua`
- `lua/ge/extensions/core/input/actions/redfox_modules_hub.json`
- `settings/inputmaps/keyboard_redfox_modules_hub.json`
- `settings/redfox/garage_hub/adapter_registry.json`
- `settings/redfox/garage_hub/action_apps.json`
- `info.json`
- `mod_info/REDFOX_MODULES_HUB/info.json`
- Rebuild documentation/diffs under `_redfox_dev_notes/`

No external mod ZIP was edited or included.

## Static verification completed

- Baseline inspected and archived.
- Side-by-side colored diff generated.
- Text unified diff generated.
- `modulesHub.lua` compiled with `texlua loadfile()`.
- Auto-loader compiled with `texlua loadfile()`.
- All seven JSON files decoded successfully before packaging.
- ZIP reopened with `unzip -t`: no compressed-data errors.
- ZIP extracted to a clean verification directory.
- Extracted Lua files compiled again.
- Extracted JSON files decoded again.
- Required extension, action, settings, baseline, roadmap, verification, and diff files confirmed.
- Old root README clutter moved under `_redfox_dev_notes/LEGACY_READMES/`.

## Not proven until David tests in BeamNG

- Actual Hub load and rendering.
- Actual VFS action-file discovery.
- Quality of scanner candidates across the installed mod collection.
- Third-party action execution.
- Approval/ignore persistence through a game restart.
- External close/minimize behavior.
- Selected group behavior under real docked windows.
- Theme behavior against every third-party WEUI mod.
- Repeated minimize/restore stability.
- BeamNG dock-layout restoration.

## Required first runtime test

1. Disable every older GarageHub/ModulesHub ZIP.
2. Install only `1-RedFox_GarageHub_v0_7_0_RebuildPass1.zip`.
3. Press `Alt+G` and confirm the clean top bar.
4. Verify theme/font/readability controls first.
5. Open `Apps/Windows -> Scan Installed UI Actions`.
6. Screenshot the candidates before approving many entries.
7. Test and approve one likely UI action.
8. Confirm it appears in Apps/Windows.
9. Restart BeamNG and verify approval persists.
10. Mark one app `Keep Open` and test the visible `[-]` button and `Alt+M`.
11. Confirm unsupported apps are reported as skipped rather than falsely closed.
12. Provide screenshot and BeamNG log if any Lua error occurs.

No Pass 2 build may start until the runtime result is committed to GitHub.
