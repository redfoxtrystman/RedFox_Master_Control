# 25-RedFox_PhantomCloak — Current Handoff / Recovery State

**Updated:** 2026-08-27 22:56 PDT  
**Project:** RedFox Phantom Cloak / future RedFox Spy Tools module  
**Catalog name:** `25-RedFox_PhantomCloak`  
**Repository:** `redfoxtrystman/RedFox_Master_Control`

## Current safest working lineage

The working cloak path is the UI-only mesh visibility path. Do not return to the old license-plate/JBeam/controller approach.

Known progression:
- Early license-plate/JBeam/controller builds broke vehicle loading and are banned as a cloak-control path.
- v0.5.0 proved the UI-only mesh visibility direction.
- v0.5.1 shimmer fade was reported good by David.
- v0.5.11 was later explicitly identified by David as the version he had been using and considered stable enough to preserve.
- v0.5.17 repaired the local ghost visibility and added a saved Local Ghost Visibility slider.
- v0.5.18 added police-stealth suppression logic against RLS police tracking.
- v0.5.19 added manual WE-window behavior, Hub theme integration attempt, and a green night-vision test.
- v0.5.20 added recursive trailer/coupled-cargo cloak support.

**Latest delivered build:** `25-RedFox_PhantomCloak_v0_5_20_TrailerCargoCloakTest.zip`

Runtime status of v0.5.20 is still NOT PROVEN until David tests it.

## Non-negotiable preservation rules

Do not remove or replace any of these without David explicitly asking:
1. Existing whole-vehicle cloak core using BeamNG mesh visibility.
2. Local driver ghost visibility.
3. Local Ghost Visibility % slider and saved value.
4. Cloak on/off sounds.
5. Shimmer/fade timing controls.
6. GM UI cloak activation button.
7. WE settings UI.
8. Settings persistence.
9. Police-stealth work from v0.5.18 unless a targeted repair is needed.
10. Trailer/coupled-object cloak work from v0.5.20 unless a targeted repair is needed.

The current working visual cloak must always remain available as the safe/default style even if experimental styles are added.

## Intended behavior

### Cloak visual behavior
- Vehicle fades/shimmers into cloak.
- Driver can still see a configurable faint ghost of their own vehicle.
- Other players are intended to see full invisibility once multiplayer sync is implemented/proven.
- Police/NPC pursuit logic is intended to lose the player while cloaked.
- Glitch/malfunction mode may temporarily reveal the vehicle if enabled.

### Local ghost visibility
WE setting: `Local Ghost Visibility %`
- 0% = completely invisible to driver
- about 8% = faint default ghost
- 25% = easier to drive
- up to 50% = strongly visible to driver

This is local driver visibility only. It must not become the remote-player visibility level.

### Police stealth
RLS police logic was inspected. Police can keep knowing the player's exact location because RLS caches and rebuilds pursuit targets from live traffic data even when the mesh is invisible.

The v0.5.18 patch added cloak-time pursuit suppression intended to:
- call `gameplay_police.setPursuitMode(0, playerVehicleId)`;
- clear queued pursuit starts;
- keep pursuit score/sight/offense/arrest timers suppressed;
- remove player from police role target caches;
- clear police `targetId` values that still point at the cloaked player.

Runtime success of this police fix was not conclusively confirmed in the latest chat state. Preserve it and test before rewriting.

Relevant RLS files previously inspected:
- `lua/ge/extensions/overrides/gameplay/traffic/roles/police.lua`
- `lua/ge/extensions/overrides/gameplay/police.lua`
- `lua/ge/extensions/overrides/gameplay/traffic/vehicle.lua`
- `lua/ge/extensions/overrides/career/modules/playerDriving.lua`
- `lua/ge/extensions/career/modules/enforcement.lua`

### Trailer and cargo cloak
v0.5.20 added recursive coupled-object cloak support using BeamNG coupler attach/detach relationships and mesh alpha control.

Intended supported objects:
- normal trailers
- fifth-wheel trailers
- converter dollies
- trailer chains
- coupler-attached shipping containers/cargo
- cargo that is part of the trailer vehicle object

Detached objects should be restored visible when uncoupled while cloaked.
Loose nearby props must not be hidden by proximity guessing.

## UI architecture and required behavior

### GM UI
GM UI should remain minimal:
- one Cloak toggle button
- one gear/settings button

Desired styling:
- OFF = dull gray
- ON = green with fluorescent/edge glow

Do not clutter GM UI with development-only controls.

Night Vision, Heat Vision, and Malfunction are dev/WIP features and should stay hidden from GM UI unless David explicitly enables them in WE settings.

### WE UI
WE UI is the full settings/configuration surface.
Requirements:
- vertical scrolling
- controls must not clip
- save/restore settings
- open/close GM UI
- control which GM UI buttons are visible
- GM gear opens WE UI
- WE UI should not force itself open before the title screen
- user should load/open it when desired
- follow RedFox Hub theme colors rather than hardcoded colors

Hub theme integration target came from GarageHub v0.7.1. Phantom Cloak should read the Hub theme API instead of using fixed colors.

## Settings persistence
David explicitly requires settings to persist so values do not reset between sessions.
Do not claim persistence unless verified against the actual settings file after a restart.

## Frozen future Spy Tools bridge contract
```lua
moduleId = "redfox_spy_tools"
visibleName = "RedFox Spy Tools"
windowId = "RedFoxSpyTools"
settingsFile = "settings/redfox/spy_tools/settings.json"
manifestPath = "lua/ge/extensions/redfox/modules/redfox_spy_tools/redfox_module.json"
openFunction = "extensions.redfox_spy_tools.openWindow"
closeFunction = "extensions.redfox_spy_tools.closeWindow"
toggleFunction = "extensions.redfox_spy_tools.toggleWindow"
isWindowOpenFunction = "extensions.redfox_spy_tools.isWindowOpen"
minimizeFunction = "extensions.redfox_spy_tools.minimizeWindow"
restoreFunction = "extensions.redfox_spy_tools.restoreWindow"
settingsFunction = "extensions.redfox_spy_tools.openSettingsWindow"
gameUIFunction = "extensions.redfox_spy_tools.openGameUI"
```
Do not rename this casually after Hub integration.

## Sound assets already used
- `cloak_on.ogg` ~2.62 sec
- `cloak_off.ogg` ~2.37 sec
- `cloak_malfunction.ogg` ~9.29 sec
No continuous cloak loop is desired.

## Visual styles / shimmer state
Current safe reality: the universal cloak core uses whole-vehicle visibility, so multiple named styles built only from timing/pulses looked too similar in runtime.

Styles previously attempted:
- Smooth Fade
- Pulse Shimmer
- Diamond/Wave
- Predator Heat-Haze
- Bond Adaptive Sweep
- Random Glitch
- Bond Mosaic / Crystal test

David reported the different styles did not meaningfully look different enough.
Do not claim true Bond/Predator distortion unless the build actually contains shader/material/refraction implementation.

Promising future direction:
- individual flexbody/part visibility sequencing
- front-to-back disappearing parts
- back-to-front
- random parts
- center-out / outside-in
- temporary crystal/electrical particles around the transition

The whole-car fade must remain as fallback/default.

## Night vision / heat vision state
### Night vision
Multiple CEF/CSS overlay attempts failed to affect the 3D game view reliably.
Latest approach attempted in v0.5.19: native ImGui full-screen green overlay test.
Desired simple fallback:
- green screen tint
- increased apparent brightness at night
- optional bloom-like effect if BeamNG exposes a safe route
Do not claim night vision works until David sees it in-game.

### Heat vision
Heat vision is not required to finish the cloak mod if it remains impractical.
No working universal thermal renderer has been proven.

## Hover-car fun option backlog
David requested an optional checkbox to hide tires/drivetrain visually so the car appears to hover.
Not yet implemented/proven. Do not fake the checkbox.

## Multiplayer state
Goal:
- cloaked driver sees own local ghost
- remote players see full invisibility
- later seeker/heat role could see a special marker/heat representation

Current state:
- local cloak works
- remote BeamMP invisibility is NOT YET PROVEN
- prior multiplayer-safe intent/settings are not the same as synchronized remote hiding

If BeamMP does not sync mesh visibility automatically, a RedFox network state layer is required: `vehicle X is cloaked` -> broadcast -> each remote client hides that vehicle locally.
Do not claim full multiplayer support until tested with at least two clients.

## BeamNG v0.39 compatibility context
BeamNG v0.39 introduced major UI architecture changes, but legacy Angular HUD apps remain supported through the transition.
Important notes already checked:
- UI Apps renamed HUD Apps.
- major Vue/Lua Router changes occurred.
- old license plate architecture changed heavily.
- Phantom Cloak no longer depends on the dangerous old license-plate/JBeam path.
Do not rewrite Phantom Cloak to Vue preemptively unless the current HUD app actually fails under v0.39.

## Order-of-operations law
Incident report already filed:
`INCIDENT_REPORTS/2026-07-08_PhantomCloak_Order_Of_Operations_Failure.md`

Before every new build:
1. Identify exact baseline ZIP.
2. Reopen baseline and inventory files.
3. Inspect code before edit.
4. Change only requested files/features.
5. Compare edited code after edit.
6. Package ZIP.
7. Reopen final ZIP.
8. Verify promised files/settings/functions are present.
9. Confirm unchanged working sections are preserved.
10. Label status truthfully: static verification vs runtime proven by David.

Never use Working/Fixed/Final/Proven/Ready unless runtime evidence supports it.

## Immediate next tests / recovery instructions
If this chat dies, next chat should start from this file and ask David for the latest available Phantom Cloak ZIP.
Preferred source if available: `25-RedFox_PhantomCloak_v0_5_20_TrailerCargoCloakTest.zip`

Do not reconstruct newer features from memory blindly if only an older ZIP is available.

Runtime tests still needed:
1. Cloak truck and confirm local ghost slider remains correct.
2. Start police chase, cloak, change direction, confirm police no longer track actual position.
3. Attach trailer/cargo, cloak, confirm full coupled train disappears as intended.
4. Detach trailer while cloaked, confirm detached trailer becomes visible again.
5. Check whether v0.5.19/v0.5.20 night-vision green overlay visibly affects screen.
6. Two-client BeamMP test for remote invisibility.

## Naming rule
All future ZIPs must begin `25-RedFox_PhantomCloak_` followed by version and truthful description.
Do not change catalog number 25 unless David explicitly reassigns it.

## Bottom line
The core cloak concept works. Critical preservation points are the UI-only mesh visibility path, local ghost slider, sounds/settings, police-stealth work, and coupled trailer/cargo follow-cloak work. Remaining risky areas are multiplayer remote sync, true per-part cloak styles, and night/heat rendering.
