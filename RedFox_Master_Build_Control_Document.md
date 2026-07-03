# RedFox Master Build Control Document

**Document:** RedFox_Master_Build_Control_Document.md  
**Owner Chat:** RedFox Master Build Coordinator  
**Coordinator:** Sol / ChatGPT for Captain David  
**Created:** 2026-07-03  
**Status:** v0.1 starter control document  
**Purpose:** Keep all RedFox BeamNG mod work organized across multiple chats, prevent naming drift, prevent duplicate-ZIP confusion, and build a clean shared loading/bridge system for Freeroam, Career Mode, Garage Hub, GM UI, WE/native ImGui UI, and BeamMP where possible.

---

## 1. Current Mission

Build a clean RedFox-wide coordination system so David's BeamNG RedFox mods can eventually work together in:

```text
Freeroam / Solo
Career Mode
Garage Hub
GM UI
WE/native ImGui UI
BeamMP / Multiplayer where possible later
```

The current phase is **foundation and communication**, not a giant rewrite.

Correct build order:

```text
1. Create and maintain this master build document.
2. Build or inspect a tiny RedFox UI Load Tester mod.
3. Test GM UI vs WE/native ImGui UI load behavior in Freeroam and Career.
4. Build or repair a clean Garage Hub 2.0 around the proven behavior.
5. Build Career Bridge + Load Doctor around the same bridge contract.
6. Convert real mods one at a time only after the test pattern is proven.
```

Do not start by rewriting every real mod.

---

## 2. Hard Rules

```text
1. This master document is the source of truth.
2. Hub controls UI/status/theme/load timing only.
3. Mods own gameplay.
4. Do not rename bridge IDs once created.
5. Do not use editor.setEditorActive(true) for mod settings.
6. Do not auto-open both GM and WE UI at startup.
7. Career Mode needs delayed-load testing.
8. PiP/render modules must wait for RenderViewManager.
9. Vehicle logic must wait for player vehicle.
10. Level logic must wait for level loaded.
11. If one part fails, pause that part, not the whole mod.
12. Do not rewrite all mods until the test module proves the pattern.
13. Avoid giant all-in-one patches.
14. Verify before and after packaging.
15. Do not run duplicate old ZIPs.
16. Every chat works only on its assigned section unless David says otherwise.
17. Every finished output must include what changed, what was preserved, what file was created, what needs testing, bridge info, and risks/unknowns.
```

---

## 3. Current Active Files

| File | Status | Notes |
|---|---:|---|
| `RedFox_Master_Build_Control_Document.md` | Active | Source of truth for cross-chat coordination. |
| `1-RedFox_GarageHub_v0_5_11_AllRedFoxBridges.zip` | Needed | Upload first if this is still the true current Hub baseline. |
| `RedFox_GarageHub_Mod_Bridge_Requirements.md` | Needed | Upload if available. |
| `RedFox_Hub_Bridge_Master_Handoff.md` | Needed | Upload if available. |
| UI Load Tester ZIP | Not built/unknown | Must be created or inspected before mass conversion. |
| Career Bridge + Load Doctor ZIP | Not built/unknown | Must come after load timing pattern is proven. |

---

## 4. Known Good Files

| File | Known Good For | Verification Status | Notes |
|---|---|---:|---|
| TBD | TBD | Not verified in this chat yet | Add only after static inspection and David's in-game test notes. |

---

## 5. Known Bad / Duplicate / Retired Files

| File | Reason | Action |
|---|---|---|
| `41_RedFoxSurfaceStudio_v0_2_9_LayerColors_ModulesHubCompat.zip` | Old Surface Studio v0.2.9 only opened GM/Angular UI and should not be treated as a true native Hub window. | Do not use for current Hub testing. |
| `37_racebuilder_v0_4_16_3_hub_manifest_bridge.zip` | Old/incomplete bridge fields and gameplay functions in Hub manifest. | Do not use for current Hub testing. |
| Duplicate Hub ZIPs | BeamNG may load older code while David thinks he is testing the newest build. | Disable all but one Hub ZIP. |
| Duplicate mod ZIPs | Causes extension/manifest conflicts. | Only one version of each mod enabled during testing. |

Duplicate search terms:

```text
GarageHub
ModulesHub
RaceBuilder
EventManager
SurfaceStudio
Knight
TrailSpotter
Spawner
Winch
PSI
Drivetrain
SpyTools
VTOL
```

---

## 6. RedFox Garage Hub 2.0 Plan

The Hub is the control center.

The Hub should do:

```text
Open modules
Close modules
Toggle modules
Open WE/native settings UI
Open GM/tiny overlay UI
Apply theme/font/button/text settings
Remember modules
Restore modules
Check module health
Report broken links
Expose module information to Career Bridge / Load Doctor
```

The Hub must not do gameplay.

Bad:

```text
Hub directly spawns cars.
Hub directly runs winch physics.
Hub directly starts races.
Hub directly controls tire PSI behavior.
Hub directly controls Knight Rider boost.
Hub directly controls TrailSpotter camera logic.
```

Good:

```text
Hub opens Spawner UI.
Hub opens Winch UI.
Hub opens RaceBuilder UI.
Hub opens PSI UI.
Hub opens Knight Rider UI.
Hub checks if module functions exist.
Hub applies theme.
Hub reports what is broken.
```

Fresh Hub 2.0 target features:

```text
Main Hub window
Theme system
Font scale
Button scale
Text color
Button text color
Module registry
Manifest scanner
Manual fallback entries
Module rows
Open / Close / Settings / GM UI buttons
Remember / Restore
Safe Mode
UI Mode column
Dev Doctor panel
Export report
```

Per-module UI mode options:

```text
Core Only
GM Only
WE Only
Both Delayed
Disabled
Safe Mode
```

Dev Doctor buttons:

```text
Check All Modules
Check Selected Module
Ping Open Function
Ping Settings Function
Ping GM UI Function
Check Theme Handshake
Check Status Return
Export Report
```

Module health statuses:

```text
Found
Missing manifest
Extension failed
Function missing
Open failed
Settings failed
GM UI failed
Status OK
Theme OK
Paused unsafe stage
```

---

## 7. RedFox Hub Bridge Contract

Every RedFox mod that should work with the Hub needs one stable GE extension.

Example required extension path:

```text
lua/ge/extensions/redfox_example.lua
```

Hub calls it as:

```lua
extensions.redfox_example
```

Do not change this extension name later unless this master document explicitly approves the change.

### Required Lua Functions

Each module extension should export:

```lua
openWindow()
closeWindow()
toggleWindow()
isWindowOpen()
minimizeWindow()
restoreWindow()
openSettingsWindow()
openGameUI()
applyGlobalTheme(themeTable)
applyGlobalFontScale(scale)
applyGlobalButtonScale(scale)
applyGlobalTextColor(color)
applyGlobalButtonTextColor(color)
setUseLocalOverride(enabled)
getModuleStatus()
```

### Minimal Bridge Skeleton

```lua
local M = {}

local windowOpen = false
local minimized = false
local useLocalOverride = false

function M.openWindow()
  windowOpen = true
  minimized = false
end

function M.closeWindow()
  windowOpen = false
  minimized = false
end

function M.toggleWindow()
  if windowOpen then
    M.closeWindow()
  else
    M.openWindow()
  end
end

function M.isWindowOpen()
  return windowOpen and not minimized
end

function M.minimizeWindow()
  minimized = true
end

function M.restoreWindow()
  windowOpen = true
  minimized = false
end

function M.openSettingsWindow()
  M.openWindow()
  -- switch to settings tab if the UI has tabs
end

function M.openGameUI()
  -- open/toggle GM overlay if this mod has one
end

function M.applyGlobalTheme(themeTable)
  if useLocalOverride then return end
  -- store/apply Hub colors here
end

function M.applyGlobalFontScale(scale)
  if useLocalOverride then return end
end

function M.applyGlobalButtonScale(scale)
  if useLocalOverride then return end
end

function M.applyGlobalTextColor(color)
  if useLocalOverride then return end
end

function M.applyGlobalButtonTextColor(color)
  if useLocalOverride then return end
end

function M.setUseLocalOverride(enabled)
  useLocalOverride = enabled and true or false
end

function M.getModuleStatus()
  return {
    moduleId = "redfox_example",
    visibleName = "RedFox Example",
    windowId = "RedFoxExample",
    open = windowOpen,
    minimized = minimized,
    ready = true,
    useLocalOverride = useLocalOverride
  }
end

function M.onUpdate(dtReal, dtSim, dtRaw)
  if windowOpen and not minimized then
    -- draw native WE/ImGui UI here if applicable
  end
end

return M
```

### Native WE / ImGui UI Rule

If a mod says it has a WE UI, it must use native BeamNG ImGui:

```lua
local im = ui_imgui
```

And draw from an update hook:

```lua
function M.onUpdate(dtReal, dtSim, dtRaw)
  if windowOpen and not minimized then
    -- draw ImGui window here
  end
end
```

The gear/settings button must not call:

```lua
editor.setEditorActive(true)
```

That opens the actual BeamNG World Editor. That is wrong.

Correct behavior:

```lua
extensions.load('redfox_example')
extensions.redfox_example.openSettingsWindow()
```

### Required Manifest

Each mod must include:

```text
lua/ge/extensions/redfox/modules/<moduleId>/redfox_module.json
```

Example manifest path:

```text
lua/ge/extensions/redfox/modules/redfox_example/redfox_module.json
```

Manifest example:

```json
{
  "redfoxModule": true,
  "moduleId": "redfox_example",
  "visibleName": "RedFox Example",
  "windowId": "RedFoxExample",
  "version": "0.1.0",
  "category": "Garage Tools",
  "supportsGarageHub": true,
  "supportsStandalone": true,
  "supportsDocking": true,
  "supportsSettings": true,
  "garageHubHidden": false,
  "devOnly": false,
  "openFunction": "extensions.redfox_example.openWindow",
  "closeFunction": "extensions.redfox_example.closeWindow",
  "toggleFunction": "extensions.redfox_example.toggleWindow",
  "isWindowOpenFunction": "extensions.redfox_example.isWindowOpen",
  "minimizeFunction": "extensions.redfox_example.minimizeWindow",
  "restoreFunction": "extensions.redfox_example.restoreWindow",
  "settingsFunction": "extensions.redfox_example.openSettingsWindow",
  "gameUIFunction": "extensions.redfox_example.openGameUI",
  "settingsFile": "settings/redfox/example/settings.json"
}
```

---

## 8. RedFox UI Load Tester Plan

Build this before rewriting the real Hub or converting all real mods.

Name:

```text
RedFox UI Load Tester
```

It should test:

```text
Core only
GM UI only
WE/native UI only
GM first then WE
WE first then GM
Both delayed
Career mode safe load
Freeroam load
Vehicle-required load
RenderViewManager/PiP-required load
```

It should log:

```text
Did extension load?
Did WE window draw?
Did GM app open?
Was Career active?
Was level loaded?
Was player vehicle available?
Did RenderViewManager exist?
What failed?
Was failed part paused?
```

Purpose:

```text
Find out whether Career Mode prefers GM first, WE first, core-only first, or delayed both.
```

---

## 9. Career Bridge + Load Doctor Plan

This should be one combined mod:

```text
RedFox Career Bridge + Load Doctor
```

It has two jobs:

```text
Career Bridge = safely loads RedFox mods at the right time.
Load Doctor = watches, logs, and reports exactly what failed.
```

Best setup:

```text
Garage Hub = source of truth when available.
Career Bridge = safe loader / watchdog / repair helper.
Old mods = supported by manual fallback entries.
```

Career Bridge should use module manifests when possible:

```text
lua/ge/extensions/redfox/modules/<moduleId>/redfox_module.json
```

But it should also allow manual fallback entries for old/weird mods.

### Readiness Order

Career Bridge should check readiness in this order:

```text
1. BeamNG UI ready
2. Career mode detected
3. Level loading started
4. Level loaded
5. Player vehicle exists
6. core_camera ready
7. RenderViewManager ready
8. Garage Hub ready if installed
9. RedFox module manifests found
```

Then load safely:

```text
Load lightweight core first.
Wait.
Load GM UI only if needed.
Wait.
Load WE/native UI only when safe.
Wait.
Load vehicle-dependent systems after player vehicle exists.
Wait.
Load PiP/render modules only after RenderViewManager exists.
Open apps minimized unless user says otherwise.
Never spam missing extension calls.
If something fails, write exact reason to log.
```

### Logging Requirement

Preferred folder name:

```text
RedFox_CareerBridge_LOGS
```

David previously suggested:

```text
D:\Games\Steam\steamapps\common\----new mods folder-----\current\mods\RedFox_CareerBridge_LOGS\
```

If not portable, make it configurable, but always show the current log folder clearly inside the UI.

---

## 10. Module Registry

### RedFox Spawner

```text
moduleId = redfox_spawner
visibleName = RedFox Spawner
windowId = RedFoxSpawner
settingsFile = settings/redfox/spawner/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_spawner/redfox_module.json

openFunction = extensions.redfox_spawner.openWindow
closeFunction = extensions.redfox_spawner.closeWindow
toggleFunction = extensions.redfox_spawner.toggleWindow
isWindowOpenFunction = extensions.redfox_spawner.isWindowOpen
minimizeFunction = extensions.redfox_spawner.minimizeWindow
restoreFunction = extensions.redfox_spawner.restoreWindow
settingsFunction = extensions.redfox_spawner.openSettingsWindow
gameUIFunction = extensions.redfox_spawner.openGameUI
```

### RedFox TrailSpotter Cam

```text
moduleId = redfox_trailspotter_cam
visibleName = RedFox TrailSpotter Cam
windowId = RedFoxTrailSpotterCam
settingsFile = settings/redfox/trailspotter_cam/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_trailspotter_cam/redfox_module.json

openFunction = extensions.scripts_redfox__trailspotter_extension.openWindow
closeFunction = extensions.scripts_redfox__trailspotter_extension.closeWindow
toggleFunction = extensions.scripts_redfox__trailspotter_extension.toggleWindow
isWindowOpenFunction = extensions.scripts_redfox__trailspotter_extension.isWindowOpen
minimizeFunction = extensions.scripts_redfox__trailspotter_extension.minimizeWindow
restoreFunction = extensions.scripts_redfox__trailspotter_extension.restoreWindow
settingsFunction = extensions.scripts_redfox__trailspotter_extension.openSettingsWindow
gameUIFunction = extensions.scripts_redfox__trailspotter_extension.openGameUI
```

Likely requirements:

```text
level loaded = yes
player vehicle = yes
RenderViewManager / PiP = yes
Career delayed load = yes
```

### RaceBuilder

Project/file name:

```text
37_racebuilder
```

Current internal bridge may still be:

```text
redfox_event_manager
```

Use the shipped manifest unless deliberately changing Hub and mod together.

```text
moduleId = redfox_event_manager
visibleName = RaceBuilder
windowId = RedFoxEventManager
settingsFile = settings/redfox/event_manager/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_event_manager/redfox_module.json

openFunction = extensions.redfox_event_manager.openWindow
closeFunction = extensions.redfox_event_manager.closeWindow
toggleFunction = extensions.redfox_event_manager.toggleWindow
isWindowOpenFunction = extensions.redfox_event_manager.isWindowOpen
minimizeFunction = extensions.redfox_event_manager.minimizeWindow
restoreFunction = extensions.redfox_event_manager.restoreWindow
settingsFunction = extensions.redfox_event_manager.openSettingsWindow
gameUIFunction = extensions.redfox_event_manager.openGameUI
```

### Surface Studio

```text
moduleId = redfox_surface_studio
visibleName = RedFox Surface Studio
windowId = RedFoxSurfaceStudio
settingsFile = settings/redfox/surface_studio/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_surface_studio/redfox_module.json

openFunction = extensions.redfox_surface_studio.openWindow
closeFunction = extensions.redfox_surface_studio.closeWindow
toggleFunction = extensions.redfox_surface_studio.toggleWindow
isWindowOpenFunction = extensions.redfox_surface_studio.isWindowOpen
minimizeFunction = extensions.redfox_surface_studio.minimizeWindow
restoreFunction = extensions.redfox_surface_studio.restoreWindow
settingsFunction = extensions.redfox_surface_studio.openSettingsWindow
gameUIFunction = extensions.redfox_surface_studio.openGameUI
```

Important:

```text
Old Surface Studio v0.2.9 only opened GM/Angular UI and should not be treated as a true native Hub window.
Use v0.2.11 NativeHubWindowFix or newer.
```

### RedFox VTOL Drive

```text
moduleId = redfox_vtol_drive
visibleName = RedFox VTOL Drive
windowId = RedFoxVTOLDrive
settingsFile = settings/redfox/vtol_drive_settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_vtol_drive/redfox_module.json

openFunction = extensions.redfox_vtol_drive.openWindow
closeFunction = extensions.redfox_vtol_drive.closeWindow
toggleFunction = extensions.redfox_vtol_drive.toggleWindow
isWindowOpenFunction = extensions.redfox_vtol_drive.isWindowOpen
minimizeFunction = extensions.redfox_vtol_drive.minimizeWindow
restoreFunction = extensions.redfox_vtol_drive.restoreWindow
settingsFunction = extensions.redfox_vtol_drive.openSettingsWindow
gameUIFunction = extensions.redfox_vtol_drive.openGameUI
```

Use the current shipped settings path:

```text
settings/redfox/vtol_drive_settings.json
```

Do not clean it up unless the VTOL mod updates the manifest too.

### Knight Rider

```text
moduleId = redfox_knight_rider
visibleName = Knight Rider
windowId = KnightRiderSettingsWindow
settingsFile = settings/redfox/knight_rider/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_knight_rider/redfox_module.json

openFunction = extensions.redfox_knight_rider.openWindow
closeFunction = extensions.redfox_knight_rider.closeWindow
toggleFunction = extensions.redfox_knight_rider.toggleWindow
isWindowOpenFunction = extensions.redfox_knight_rider.isWindowOpen
minimizeFunction = extensions.redfox_knight_rider.minimizeWindow
restoreFunction = extensions.redfox_knight_rider.restoreWindow
settingsFunction = extensions.redfox_knight_rider.openSettingsWindow
gameUIFunction = extensions.redfox_knight_rider.openGameUI
```

Important:

```text
Gear/settings must call extensions.redfox_knight_rider.openSettingsWindow().
It must not call editor.setEditorActive(true).
The old redfoxTurboBoost extension should remain gameplay/legacy compatibility only.
```

### RedFox Winch Core

```text
moduleId = redfox_winch_core
visibleName = RedFox Winch Core
windowId = RedFoxWinchCore
settingsFile = settings/redfox/winch_core/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_winch_core/redfox_module.json

openFunction = extensions.redfox_winch_core.openWindow
closeFunction = extensions.redfox_winch_core.closeWindow
toggleFunction = extensions.redfox_winch_core.toggleWindow
isWindowOpenFunction = extensions.redfox_winch_core.isWindowOpen
minimizeFunction = extensions.redfox_winch_core.minimizeWindow
restoreFunction = extensions.redfox_winch_core.restoreWindow
settingsFunction = extensions.redfox_winch_core.openSettingsWindow
gameUIFunction = extensions.redfox_winch_core.openGameUI
```

Important:

```text
Hub/Career Bridge should not touch winch physics, cable logic, vehicle attachment, or recovery behavior.
Visual/window bridge only.
```

### RedFox PSI Controller

```text
moduleId = redfox_psi_controller
visibleName = RedFox PSI Controller
windowId = RedFoxPSIController
settingsFile = settings/redfox/psi_controller/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_psi_controller/redfox_module.json

openFunction = extensions.redfox_psi_controller.openWindow
closeFunction = extensions.redfox_psi_controller.closeWindow
toggleFunction = extensions.redfox_psi_controller.toggleWindow
isWindowOpenFunction = extensions.redfox_psi_controller.isWindowOpen
minimizeFunction = extensions.redfox_psi_controller.minimizeWindow
restoreFunction = extensions.redfox_psi_controller.restoreWindow
settingsFunction = extensions.redfox_psi_controller.openSettingsWindow
gameUIFunction = extensions.redfox_psi_controller.openGameUI
```

Important:

```text
Hub/Career Bridge should not own tire/PSI gameplay.
Only load safely, open UI, report status, and apply theme.
```

### RedFox Offroad Drivetrain

```text
moduleId = redfox_offroad_drivetrain
visibleName = RedFox Offroad Drivetrain
windowId = RedFoxOffroadDrivetrain
settingsFile = settings/redfox/offroad_drivetrain/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_offroad_drivetrain/redfox_module.json

openFunction = extensions.redfox_offroad_drivetrain.openWindow
closeFunction = extensions.redfox_offroad_drivetrain.closeWindow
toggleFunction = extensions.redfox_offroad_drivetrain.toggleWindow
isWindowOpenFunction = extensions.redfox_offroad_drivetrain.isWindowOpen
minimizeFunction = extensions.redfox_offroad_drivetrain.minimizeWindow
restoreFunction = extensions.redfox_offroad_drivetrain.restoreWindow
settingsFunction = extensions.redfox_offroad_drivetrain.openSettingsWindow
gameUIFunction = extensions.redfox_offroad_drivetrain.openGameUI
```

Important:

```text
No gameplay rewrite.
No crawl controller rewrite.
No gearbox changes.
No torque converter changes.
No transfer-case changes.
No Smart Traction changes.
No winch changes.
Hub/Career Bridge only handles UI loading/status/theme.
```

### RedFox Spy Tools

Planned combined spy mod:

```text
moduleId = redfox_spy_tools
visibleName = RedFox Spy Tools
windowId = RedFoxSpyTools
settingsFile = settings/redfox/spy_tools/settings.json
manifestPath = lua/ge/extensions/redfox/modules/redfox_spy_tools/redfox_module.json

openFunction = extensions.redfox_spy_tools.openWindow
closeFunction = extensions.redfox_spy_tools.closeWindow
toggleFunction = extensions.redfox_spy_tools.toggleWindow
isWindowOpenFunction = extensions.redfox_spy_tools.isWindowOpen
minimizeFunction = extensions.redfox_spy_tools.minimizeWindow
restoreFunction = extensions.redfox_spy_tools.restoreWindow
settingsFunction = extensions.redfox_spy_tools.openSettingsWindow
gameUIFunction = extensions.redfox_spy_tools.openGameUI
```

Spy Tools should be one master mod with tabs:

```text
Oil Slick
Phantom Cloak
Smoke Screen
Tire Trap
Future Spy Gadgets
Settings
GM Overlay
```

Do not make separate Hub bridges for every spy gadget unless absolutely needed.

### Third-Party / Adapter Modules Known By Hub

#### Random Gravity

```text
moduleId = random_gravity
visibleName = Random Gravity
toggleFunction = extensions.randomGravityUI.toggleUI
extensionName = randomGravityUI
```

#### Dynamic Gravity

```text
moduleId = dynamic_gravity
visibleName = Dynamic Gravity
toggleFunction = extensions.sinematic_dynamicGravityUI.toggleUI
extensionName = sinematic_dynamicGravityUI
```

#### Flood

```text
moduleId = flood
visibleName = Flood
openFunction = extensions.flood.setShowUI(true)
toggleFunction fallback = extensions.flood.toggleShowUI()
extensionName = flood
```

#### MK Dynamic Weather

```text
moduleId = mk_dynamic_weather
visibleName = MK Dynamic Weather
extensionName = unknown / check current adapter
```

---

## 11. GM UI vs WE UI Test Results

| Test ID | Build Tested | Context | Load Order | GM Result | WE Result | Notes | Pass/Fail |
|---|---|---|---|---|---|---|---|
| GM-001 | TBD | Freeroam | GM only | TBD | N/A | TBD | TBD |
| WE-001 | TBD | Freeroam | WE only | N/A | TBD | TBD | TBD |
| BOTH-001 | TBD | Freeroam | GM first, then WE | TBD | TBD | TBD | TBD |
| BOTH-002 | TBD | Freeroam | WE first, then GM | TBD | TBD | TBD | TBD |
| DELAY-001 | TBD | Freeroam | Core first, both delayed | TBD | TBD | TBD | TBD |
| CAREER-UI-001 | TBD | Career | Core first, both delayed | TBD | TBD | TBD | TBD |

---

## 12. Career Mode Test Results

| Test ID | Enabled ZIPs | Career Stage | Result | Error / Log Summary | Action |
|---|---|---|---|---|---|
| CAREER-001 | Hub only | Launch Career | TBD | TBD | TBD |
| CAREER-002 | Hub + UI Load Tester | Launch Career | TBD | TBD | TBD |
| CAREER-003 | Hub + Knight Rider | Launch Career | TBD | TBD | TBD |
| CAREER-004 | Hub + TrailSpotter Cam | Launch Career | TBD | TBD | TBD |

---

## 13. Multiplayer / BeamMP Notes

BeamMP support is a later phase.

Current rule:

```text
Do not claim BeamMP compatibility until tested.
Do not let MP goals force risky single-player or Career rewrites.
UI/status/load bridge work comes first.
Gameplay sync comes later per mod.
```

Initial MP categories:

| Module | MP Risk | Notes |
|---|---:|---|
| Hub | Low/Medium | UI/status only should be safer. |
| Career Bridge | Medium | Mostly local loader; MP context detection later. |
| Winch Core | High | Physics/attachment sync sensitive. |
| Knight Rider | High | Vehicle impulse/boost sync sensitive. |
| TrailSpotter Cam | Low/Medium | Camera local; PiP/render local. |
| Spy Tools | High | Oil, traps, cloak, smoke need MP ownership rules. |

---

## 14. Individual Mod Assignments

| Chat | Assignment | First Job | Must Not Do |
|---|---|---|---|
| Coordinator Chat | Master document, order, naming, bridge contract, status tracking | Keep this document current | Do not randomly rewrite every mod |
| Hub Chat | RedFox Garage Hub 2.0 | Inspect/build scanner and health rows | Do not move gameplay into Hub |
| Career Bridge / Load Doctor Chat | Career-safe loading and logs | Build staged load gate and log reporter | Do not depend only on perfect new mods |
| UI Load Tester Chat | Test GM/WE/Career timing | Build tiny proof mod | Do not skip this step |
| Knight Rider Chat | Knight Rider module | Preserve boost gameplay, fix bridge/UI timing | Do not call World Editor for settings |
| TrailSpotter Cam Chat | TrailSpotter module | Preserve camera logic, delay PiP/render | Do not load RenderViewManager too early |
| RaceBuilder Chat | RaceBuilder module | Preserve shipped internal bridge unless deliberately changed | Do not rename visible/file naming back to Event Manager |
| Surface Studio Chat | Surface Studio module | Use v0.2.11 NativeHubWindowFix or newer | Do not use old v0.2.9 for native Hub testing |
| Winch Core Chat | Winch module | Visual/window bridge only | Do not rewrite cable/physics |
| PSI Controller Chat | PSI module | Visual/window bridge only | Do not own tire gameplay in Hub |
| Offroad Drivetrain Chat | Drivetrain module | Visual/window bridge only | Do not rewrite crawl/gearbox/torque logic |
| Spy Tools Chat | Combined spy module | Keep one master bridge with tabs | Do not split every gadget into separate Hub bridges |
| Testing Chat | Install order, logs, pass/fail | Test one Hub + one mod at a time | Do not enable duplicate ZIPs |

---

## 15. Open Questions

| ID | Question | Owner | Status |
|---|---|---|---|
| Q001 | Is `1-RedFox_GarageHub_v0_5_11_AllRedFoxBridges.zip` the true current Hub baseline? | David / Coordinator | Open |
| Q002 | Which mod is the first Career failure test target: Knight Rider or TrailSpotter Cam? | David / Coordinator | Open |
| Q003 | Does a UI Load Tester already exist, or must it be built fresh? | Coordinator / UI Load Tester Chat | Open |
| Q004 | Where should Career Bridge logs actually write on David's machine? | Career Bridge Chat / David | Open |
| Q005 | Which Hub build last worked in Freeroam with module buttons visible? | David / Testing Chat | Open |

---

## 16. Change Log

| Version | Date | Changed By | Changes |
|---|---|---|---|
| v0.1 | 2026-07-03 | Coordinator Chat | Created starter master control document, bridge rules, chat roles, module registry, blank test tables, and upload plan. |

---

# Communication Bridge System

## How Chats Communicate

Separate chats do not automatically talk to each other. David moves information between them using:

```text
1. This master document.
2. Paste-in chat starter blocks.
3. Mod-specific bridge info blocks.
4. Test result blocks.
5. File upload/checklist order.
```

Each chat must read this document first and work only on its assigned section.

## Universal Paste Block For Every RedFox Chat

```text
You are working under the RedFox Master Build Control Document.

Before changing code, read the latest master document.

Only work on your assigned section.

Do not rename moduleId, windowId, extension names, manifest paths, or bridge function names unless the master document explicitly says to.

Do not move gameplay logic into the Hub.

Do not auto-open GM UI or WE UI at startup unless the master document says that module is allowed to do so.

Every output must include:
1. What changed
2. What was preserved
3. What file was created
4. What needs testing
5. Any bridge info the Hub needs
6. Any risk or unknown

If you package a ZIP:
1. Inspect the source ZIP/current baseline first.
2. Preserve working gameplay.
3. Package the edited ZIP.
4. Reopen the output ZIP.
5. Verify file structure, Lua extension names, module IDs, window IDs, manifest paths, bridge functions, settings paths, GM UI folders, input files if relevant, and required exported functions.
6. Include a verification report.
```

## Mod Chat Return Block

Each mod chat should send this back to the Coordinator:

```text
moduleId =
visibleName =
windowId =
settingsFile =
manifestPath =

openFunction =
closeFunction =
toggleFunction =
isWindowOpenFunction =
minimizeFunction =
restoreFunction =
settingsFunction =
gameUIFunction =

extensionName =
does it use GM UI app? yes/no
GM app folder/name =
does it use WE/native UI? yes/no
does it use PiP/render views? yes/no
does it need player vehicle before loading? yes/no
does it need level loaded before loading? yes/no
does it need Career-safe delayed load? yes/no

What changed =
What was preserved =
What file was created =
What needs testing =
Risks / unknowns =
```

## Testing Chat Result Block

```text
Test date =
BeamNG version =
Game mode = Freeroam / Career / BeamMP
Enabled ZIPs =
Disabled duplicate ZIPs =
Map/level =
Vehicle =
What was expected =
What happened =
UI visible? yes/no
GM UI visible? yes/no
WE/native UI visible? yes/no
Errors/log lines =
Screenshot included? yes/no
Pass/fail =
Next action requested =
```

---

# First Upload Checklist

Start small. Do not upload every mod at once.

## Upload Set 1: Foundation

```text
1. 1-RedFox_GarageHub_v0_5_11_AllRedFoxBridges.zip
2. RedFox_GarageHub_Mod_Bridge_Requirements.md
3. RedFox_Hub_Bridge_Master_Handoff.md
```

If `1-RedFox_GarageHub_v0_5_11_AllRedFoxBridges.zip` is not the latest real baseline, upload the true latest Hub ZIP instead and clearly say it replaces v0.5.11 as the current baseline.

## Upload Set 2: First test mods

Upload only one or two:

```text
1. Knight Rider
2. TrailSpotter Cam
```

Then later, if needed:

```text
3. RaceBuilder
4. Surface Studio v0.2.11 NativeHubWindowFix or newer
```

## Upload Set 3: Evidence from BeamNG

```text
1. beamng.log from Freeroam test
2. beamng.log from Career Mode fail
3. Screenshot of enabled mods folder
4. Screenshot of UI problem
5. Console error screenshot if available
```

---

# David's Moving Between Chats Checklist

```text
1. Open the latest RedFox_Master_Build_Control_Document.md.
2. Paste the Universal Paste Block into the target chat.
3. Tell that chat its role: Hub, Career Bridge, UI Load Tester, Individual Mod, or Testing.
4. Upload only the files that chat needs.
5. Tell the chat not to rename bridge IDs.
6. Require the Mod Chat Return Block or Testing Chat Result Block.
7. Bring the result back to Coordinator Chat.
8. Coordinator updates the master document.
9. Do not install new ZIPs until verification report is included.
10. Keep only one version of each ZIP enabled in BeamNG.
```

---

# Current Next Step

Upload the foundation files first:

```text
1-RedFox_GarageHub_v0_5_11_AllRedFoxBridges.zip
RedFox_GarageHub_Mod_Bridge_Requirements.md
RedFox_Hub_Bridge_Master_Handoff.md
```

Then stop and let Coordinator inspect before adding more mods.
