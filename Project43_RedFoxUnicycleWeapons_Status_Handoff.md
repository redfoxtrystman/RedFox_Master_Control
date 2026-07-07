# Project 43 — RedFox Unicycle Weapons / Player Movement Handoff

Timestamp = 2026-07-06 19:52 America/Los_Angeles  
Chat ID = RF-MOD43  
Chat Name = Project 43 RedFox Unicycle Weapons / Player Movement Chat

## Current priority

Weapons are paused. The active priority is player movement/control feel.

David's target is a BeamNG-native FPS-style player core before inventory/weapons return:

- smoother walking
- true walk/sprint speed control
- camera-relative movement
- less rolling/ball behavior after key release
- crouch
- fake prone first, true prone later if possible
- visible body/gun later
- inventory and weapons after movement is acceptable

## Latest delivered build in chat

`43_RedFoxUnicycleWeapons_v2_4_5_idle_brake_antiball_fps_stop.zip`

This build adds the anti-roll / FPS-stop test pass on top of the guarded `playerController.lua` branch. It should be tested after v2.4.4 partial pass.

## Last confirmed v2.4.4 user result

David reported v2.4.4 made a big difference and speed control finally changed behavior. David also clarified that **exit did NOT crash the game**. The player still acts like a ball and keeps rolling after releasing controls.

Status = 🟨 NEEDS TEST / PARTIAL

## Important correction

Do not report v2.4.4 as an exit-crash failure. The correct result is:

```text
Exit car crash = no / did not crash
K panel opens = yes
C crouch = duplicate/conflict shown in bindings, but crouch itself works
Left Alt prone = yes
Movement profiles = all usable, but rolling/coasting remains the blocker
```

## Important finding

The earlier v2.4.1–v2.4.3 movement lab was mostly an assist layer. It changed feel but did not fully own the stock walking speed because BeamNG/unicycle walking speed is controlled inside `playerController.lua`.

The scanned BeamNG/user files pointed to these important movement constants/functions:

```text
movementSpeedNormal
movementSpeedSprint
maxAllowedBallAVNormal
maxAllowedBallAVSprint
maxBallTorque
ballPressureCrouch
walkUpDownRaw
walkLeftRightRaw
setSpeedCoef
playerController
```

## Current likely next fix / current test focus

v2.4.5 should test real anti-roll / FPS-stop behavior inside the guarded player controller branch.

Current test build name:

`43_RedFoxUnicycleWeapons_v2_4_5_idle_brake_antiball_fps_stop.zip`

New/target settings:

```text
Idle Brake Strength
Idle Brake Delay
Stop Roll Damping
Counter Torque Brake
Auto Stop Below Speed
Ball Lock Spring
Ball Lock Damping
Ground Stick Assist
Air Control Strength
Camera Relative Strafe Strength
```

Main goal:

```text
When W/A/S/D are released, actively fight leftover movement and ball spin so the player stops like an FPS character instead of coasting like a physics ball.
```

## File paths to protect

```text
lua/ge/extensions/core/redfoxPlayerMovementLab.lua
lua/vehicle/extensions/redfoxPlayerMovementAssist.lua
lua/ge/extensions/core/input/actions/redfoxPlayerMovementLab.json
settings/inputmaps/keyboard_redfox_player_movement_lab.json
lua/vehicle/controller/playerController.lua
settings/redfox/43_unicycle_player_movement_settings.json
```

## Controls as of latest movement builds

```text
K = RedFox Player Movement Lab panel
C = stock Unicycle crouch preferred
Left Alt = fake prone
Left Shift = sprint
W/A/S/D = movement
```

Do not use `M` for the panel because `M` is BeamNG map. Avoid adding a RedFox default C crouch binding if stock `[Unicycle] Crouch` already uses C.

## Movement profiles currently exposed

```text
Stock Safe
Modern Smooth
Fast Arcade
Source Heavy
Experimental Pawn
```

David found the profiles. The guarded `playerController.lua` branch made the first real speed/control difference, but rolling/coasting remains.

## Do not resume weapon expansion yet

Paused features:

- Gravity Gun polish
- Attach Tool
- Wabbajack tribute weapon
- weapon picker UI
- inventory
- body + weapon slot merge
- AI occupants/dummies

These should wait until movement is acceptable.

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
