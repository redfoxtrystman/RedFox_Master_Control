# RedFox Command Screen Handoff — v0.16.7 Layout Profiles / Beam Damage Bridge

Timestamp = 2026-07-06 19:55 America/Los_Angeles
Chat ID = RF-CMD01
Chat Name = Command Screen Chat
Screen status = 🟨 NEEDS TEST

## Current working line

Use the v0.16 rollback line, not the broken v0.18 branch.

Current delivered build:

```text
RedFox_CommandScreen_v0_16_7_LAYOUT_PROFILES_BEAM_DAMAGE_PORTABLE_WITH_ELECTRON_RUNTIME.zip
```

Also delivered:

```text
RedFox_CommandScreen_v0_16_7_LAYOUT_PROFILES_BEAM_DAMAGE_FULL_SOURCE_no_runtime.zip
RedFox_CommandScreen_v0_16_7_LAYOUT_PROFILES_BEAM_DAMAGE_OVERLAY_only_changed_files.zip
RedFox_CommandScreen_Diff_Report_v0_16_6_to_v0_16_7_LAYOUT_PROFILES_BEAM_DAMAGE.zip
```

## Hard process rules David set

- Before editing: inspect baseline and list expected touched / untouched files.
- After editing: verify only approved files changed.
- After ZIP: reopen/check ZIP structure, integrity, dev notes, and no duplicate app folders.
- Every build must include overlay ZIP, full source ZIP, full portable runtime ZIP when requested, and colored side-by-side diff report.
- Never claim runtime success unless David tested it.
- Every version must update `_redfox_dev_notes/` and preserve old history.
- Do not silently revert user changes.
- Do not make unrelated changes while fixing one box/widget.

## Important branch history

### v0.16 rollback baseline

David rolled back from the v0.18 experiment line because repeated patches broke unrelated systems. v0.16 was the better-feeling baseline.

### v0.16.1 rollback rebuild

Re-added planner note archive/search/restore/remove-forever and removed bad `Clear profile` wording by renaming it to `Reset current plan`.

### v0.16.2 widget separation foundation

Added `app/widgets/` folders with manifests/settings/style/script files for stock widgets. This was foundation only. Most render logic still lived in legacy `app/app.js` adapters.

### v0.16.3 widget edit stabilizer

Reduced blur/fog, stabilized edit widget behavior, added live preview, and prevented wheel editor collapse to one fallback spin item.

### v0.16.4 wheel editor fit

Added wheel size, center X/Y, tooltips, clearer wheel slice color labels, live color/logo preview, and reachable/sticky wheel editor action buttons.

### v0.16.5 planner external docs

Added planner CSV/JSON import/export, Builder tab for BeamNG video ideas, compatibility fields, and custom typed values for dropdown menus.

### v0.16.6 edit layout/fonts/wheel background/Beam data prep

Made edit panel smaller/docked, brought edited widget forward, added separate vertical/horizontal layout profiles, added Windows font scanning, added wheel background image support, and prepared Beam data roadmap notes.

### v0.16.7 layout profiles / Beam damage bridge

Added fullscreen wheel controls bottom-left, click-direction toggle, center-logo click-to-spin, safer top boundary, manual layout profile buttons, Add Widget active-count dimming, BeamNG Damage Monitor widget, dummy weather/game-event icons, and an experimental BeamNG bridge scaffold.

## Current Command Screen status

Screen status = 🟨 NEEDS TEST

Working/mostly acceptable from David testing:

- Wheel fullscreen works on rollback line.
- Wheel editor is improving.
- Wheel spinning behavior is good enough to move on.
- Planner is partially good but still needs future overhaul.
- External planner CSV/JSON direction is accepted.
- Widget separation direction is accepted.

Still needs work:

- Edit panel/docked editor must not block seeing the widget being edited.
- Vertical/horizontal layout profiles need user-machine test and likely repair.
- Some widgets can still overlap/jumble when switching screens.
- Need real BeamNG bridge proof before building full BeamNG data dashboard.
- Web panel and screen capture/OBS/Metal compatibility are not solved yet.
- Weather/clock should be compact and use swappable icon assets.

## BeamNG bridge status

Important: the bridge is not confirmed live.

Current status:

```text
Bridge idea = yes
Bridge scaffold files = yes
Confirmed live BeamNG data = no
Production bridge = no
```

v0.16.7 added:

```text
app/widgets/redfox_beamng_damage/
app/data/beamng/beamng_damage_widget_catalog.json
beamng_bridge_mod/RedFox_CommandScreen_Bridge/
```

BeamNG Damage Monitor currently has areas for:

- vehicle damage
- engine data
- wheels / tires
- bridge status
- editable category/group/source labels

This does not mean all BeamNG UI apps are available in Command Screen. It is the first test widget only.

## Correct next step

Build and prove the bridge before expanding the BeamNG catalog too far.

Recommended next build:

```text
v0.16.8 BeamNG Bridge Proof / App Registry
```

Scope:

1. Build a real Command Screen bridge receiver/debug log.
2. Build a BeamNG-side sender that sends one simple proof packet.
3. Add Bridge Debug Log widget.
4. Add BeamNG UI App Catalog placeholders with honest status labels.
5. Auto-scan known BeamNG UI app/mod folders if possible.
6. Mark each found app as Working / Bridge Required / Detected Only / Placeholder / Unsupported / Needs Adapter.
7. Prove easiest live data first: speed/RPM/gear/throttle/brake.
8. Keep Damage Monitor, but do not fake damage data.

## BeamNG UI app catalog plan

Eventually Command Screen should show:

```text
BeamNG
├── Damage
│   ├── Vehicle Damage Monitor
│   ├── Body Damage Map
│   ├── Part Health List
│   └── Crash Severity Log
├── Engine
│   ├── RPM / Gear / Speed
│   ├── Oil / Coolant Temp
│   ├── Turbo / Boost
│   └── Engine Warnings
├── Tires / Wheels
│   ├── Tire Pressure
│   ├── Tire Temp
│   ├── Wheel Damage
│   └── Grip / Slip
├── Race / Mission
│   ├── Checkpoints
│   ├── Lap Time
│   ├── Split Times
│   └── Scoreboard
├── Weather / World
│   ├── Time of Day
│   ├── Rain / Fog / Wind
│   ├── Flood / Tornado / Blackout / Infection
│   └── Dynamic Weather State
├── Vehicle / Catalog
│   ├── Current Vehicle
│   ├── Vehicle Picker
│   ├── Spawn / Replace
│   └── Paint / Config
└── Controls / Input
    ├── Pedals
    ├── Steering
    ├── Controller Viewer
    └── Keybind Status
```

Auto-discovery should list BeamNG UI apps/mod UI apps, but not pretend they work externally unless they have a RedFox adapter or emit usable bridge data.

## Hub issue context David asked to carry forward

Current Hub issue:

```text
Hub loads in Career after rollback, but clicking Scan causes:

lua/ge/extensions/redfox/modulesHub.lua:276
attempt to call global 'msg' (a nil value)
```

Needed:

```text
Fix scanRedFoxModules so msg() is defined, replaced, or guarded.
Then retest Scan with:
RF-UILOAD01_Discoverable_Dummy_v0_1_2.zip
```

## Files other chats should read

Start with:

```text
RedFox_Worker_Chat_Quick_Start.md
RedFox_Chat_Message_Board.md
RedFox_CommandScreen_Handoff_v0_16_7.md
RedFox_Module_Status_Table.csv
RedFox_Research_Findings_Log.csv
```

## Notes for next chat

- Do not continue the old v0.18 line unless specifically asked.
- Do not claim Bridge works until BeamNG sends data and Command Screen displays it.
- Do not try to auto-run every BeamNG UI app inside Electron. First build a data bridge + registry + adapter model.
- Keep widgets separated and self-contained.
- Wheel and Recording Planner may stay linked, but through explicit bridge/events, not shared files.
