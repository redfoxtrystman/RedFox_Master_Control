# Project 43 — RedFox Unicycle Weapons / Player Movement Handoff

Timestamp = 2026-07-07 16:20 America/Los_Angeles  
Chat ID = RF-MOD43  
Chat Name = Project 43 RedFox Unicycle Weapons / Player Movement Chat

## Current priority

Movement is good enough to begin the next foundation step, but keep movement/anti-roll available for tuning. Active priority is now the **native Backpack / Weapon Select foundation** before real inventory/weapons return.

David's target is a BeamNG-native FPS-style player core before full weapon expansion:

- smoother walking
- true walk/sprint speed control
- camera-relative movement
- less rolling/ball behavior after key release
- crouch
- fake prone first, true prone later if possible
- backpack / quickbar / weapon selector
- visible body/gun later
- weapon routing after selection foundation is stable

## Latest delivered build in chat

`43_RedFoxUnicycleWeapons_v2_4_6_backpack_weapon_select_foundation.zip`

This build starts the Backpack / Weapon Select foundation using native ImGui only. It intentionally does **not** add a GM UI app because the old v2.3.3 GM weapon picker was suspected to break BeamNG UI Apps/Grid Selector.

## Last confirmed movement result

David reported v2.4.4 made a big difference and speed control finally changed behavior. David also clarified that **exit did NOT crash the game**. The player still acts somewhat like a ball and keeps rolling after releasing controls, but David said the mod is in a good place and ready to begin backpack/weapon selection.

Status = 🟨 NEEDS TEST / PARTIAL

## Important correction

Do not report v2.4.4 as an exit-crash failure. The correct result is:

```text
Exit car crash = no / did not crash
K panel opens = yes
C crouch = duplicate/conflict shown in bindings, but crouch itself works
Left Alt prone = yes
Movement profiles = all usable, but rolling/coasting remains a tuning issue
```

## v2.4.6 new files

```text
lua/ge/extensions/core/redfoxInventoryWeapons.lua
lua/ge/extensions/core/input/actions/redfoxInventoryWeapons.json
settings/inputmaps/keyboard_redfox_inventory_weapons.json
_redfox_dev_notes/ROADMAP_v2_4_6.md
_redfox_dev_notes/DIFF_REPORT_v2_4_5_to_v2_4_6.md
_redfox_dev_notes/DIFF_REPORT_v2_4_5_to_v2_4_6.patch
```

## v2.4.6 changed files

```text
lua/ge/extensions/core/redfoxGravityWeapon.lua
_redfox_dev_notes/CHANGELOG.md
_redfox_dev_notes/TEST_RESULTS.md
_redfox_dev_notes/TODO_NEXT_BUILD.md
_redfox_dev_notes/CODE_LOCATION_INDEX.md
```

`redfoxGravityWeapon.lua` now exposes:

```text
releaseSilent()
setRequireSelectedWeapon(value)
```

These are used by the inventory foundation so selecting Empty Hands or non-gravity slots can stop inventory-routed Gravity Gun selection.

## v2.4.6 controls to test

```text
B = RedFox Backpack / Weapon Select
1-6 = select first six backpack/weapon slots
[ = previous slot
] = next slot
Backspace = Empty Hands
K = Movement Lab still opens
G = Gravity Tool still opens
```

## Current slots

```text
1 Gravity Gun = working/gated
2 Attach Tool = placeholder
3 PW2 Gun Bridge = placeholder
4 Minigun = parts fallback placeholder
5 Bazooka = parts fallback placeholder
6 Wabbajack Tribute = planned placeholder
7 Empty Hands = safe slot
```

## Important finding

BeamNG supports mod-provided regular input actions in `lua/ge/extensions/core/input/actions/*.json` and vehicle-specific actions in `vehicles/<vehicle>/input_actions*.json`; use unique action names/file names and keep action snippets short. The Backpack uses regular GE Lua actions with unique `redfoxInventory...` names and calls the new GE extension.

BeamNG UI apps are AngularJS app folders with `app.js`, `app.json`, and `app.png`, but v2.4.6 avoids adding any `ui/modules/apps` content until the native state machine passes testing.

## Current likely next fix / current test focus

Test v2.4.6 in BeamNG:

```text
v2.4.6 test:
Backpack opens with B:
Quickbar visible:
1-6 slot select works:
[ and ] cycle works:
Backspace Empty Hands works:
Gravity Gun works when selected:
Gravity is blocked or released when Empty Hands selected:
K Movement Lab still opens:
G Gravity Tool still opens:
UI Apps/Grid Selector still works:
Any Lua errors:
```

If this passes, v2.4.7 should wire selected item state into real primary/alt actions and decide whether to keep native-only or add a tiny optional GM quickbar later.

## File paths to protect

```text
lua/ge/extensions/core/redfoxPlayerMovementLab.lua
lua/vehicle/extensions/redfoxPlayerMovementAssist.lua
lua/ge/extensions/core/input/actions/redfoxPlayerMovementLab.json
settings/inputmaps/keyboard_redfox_player_movement_lab.json
lua/vehicle/controller/playerController.lua
settings/redfox/43_unicycle_player_movement_settings.json
lua/ge/extensions/core/redfoxInventoryWeapons.lua
lua/ge/extensions/core/input/actions/redfoxInventoryWeapons.json
settings/inputmaps/keyboard_redfox_inventory_weapons.json
```

## Do not fully resume weapon expansion yet

Still paused except for placeholder selection/routing foundation:

- real Attach Tool behavior
- Wabbajack tribute effects
- runtime minigun/bazooka firing bridge
- body + weapon slot merge
- AI occupants/dummies

These should wait until Backpack selection is stable.

## Earlier Project 43 notes

Important prior delivered builds:

```text
v2.3.9_exit_crash_compat_visible_gun_guard = removed active old walk.lua and playerController.lua overrides to protect exit stability.
v2.4.0_control_profile_selector = gravity-gun control-feel profiles.
v2.4.1_player_movement_lab = first movement lab, weapons paused.
v2.4.2_panel_key_rebind_hotfix = panel key changed M -> K.
v2.4.3_speed_bridge_prone_hotfix = added prone key and attempted speed bridge.
v2.4.4_guarded_playercontroller_override_test = real speed difference, no exit crash reported, still rolling/ball issue.
v2.4.5_idle_brake_antiball_fps_stop = anti-roll/FPS-stop test build; needs BeamNG testing.
v2.4.6_backpack_weapon_select_foundation = native ImGui backpack/weapon selection foundation; needs BeamNG testing.
```

## Important risk

`lua/vehicle/controller/playerController.lua` is powerful but risky. It can fix speed/stance, but it can also conflict with BeamNG walking/player behavior. Do not restore/override `lua/ge/extensions/gameplay/walk.lua` unless absolutely necessary and explicitly approved.

## Current Hub context David asked to carry forward

Separate Hub issue for RF-HUB01:

```text
Current issue:
Hub loads in Career after rollback, but clicking Scan causes:

lua/ge/extensions/redfox/modulesHub.lua:276
attempt to call global 'msg' (a nil value)

Needed:
Fix scanRedFoxModules so msg() is defined, replaced, or guarded.
Then retest Scan with:
RF-UILOAD01_Discoverable_Dummy_v0_1_2.zip
```
