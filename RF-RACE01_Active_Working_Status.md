# RF-RACE01 Active Working Status

Timestamp = 2026-07-07 13:18 America/Los_Angeles
Chat ID = RF-RACE01
Chat Name = Project 37 RaceBuilder Chat
Message type = STATUS / ACTIVE COORDINATION
Screen status = 🟨 NEEDS TEST
Assigned role = RaceBuilder development chat / Project 37 race setup and catalog owner

## Purpose

This is not a handoff. RF-RACE01 is still the active RaceBuilder chat. This file exists so other RedFox worker chats can see what this chat is doing and coordinate without guessing.

## Current RaceBuilder build under test

```text
37_racebuilder_v0_4_16_7_1_window_open_fix.zip
```

## Current paired Hub test build

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
```

## Last known good RaceBuilder baseline David reported

```text
37_racebuilder_v0_4_16_round_start_lights.zip best working solid ver.zip
```

v0.4.16.4 also had a later user-reported sanity pass after duplicate mods were removed, but the protected fully known-good baseline remains v0.4.16 round start lights.

## Current fix made in this chat

David reported RaceBuilder shows in keys but refuses to open.

Static inspection found a RaceBuilder-side open-window bug in v0.4.16.7:

- `setFromBoolPtr()` only handled Lua tables.
- BeamNG ImGui BoolPtr may be table-like userdata/cdata.
- When the window opened, `im.Begin(...)` ran and then `showUI = setFromBoolPtr(open)` could immediately set `showUI` false if the pointer was not `type(table)`.
- Same risk existed for Score Card and Race Lights.

Created local test artifact:

```text
37_racebuilder_v0_4_16_7_1_window_open_fix.zip
```

Changes:

- Updated `setFromBoolPtr(ptr, fallback)` to safely read `ptr[0]` using `pcall` and preserve the previous open state if pointer read fails.
- Updated main UI, Score Card, and Race Lights to pass fallback open states.
- Preserved v0.4.16.7 catalog foundation, Hub manifest, gate editing, AI roster/route/rules data.
- No Hub files edited in this RaceBuilder patch.

## What other chats need to know

- Do not restart Project 37 from scratch.
- Do not resume the failed 37A/37B/37C split.
- Do not move race gameplay into GarageHub.
- Do not rename RaceBuilder `moduleId`, `windowId`, extension name, manifest path, settings path, or bridge function names without approval.
- Every RaceBuilder version must update `_redfox_dev_notes` and include a new version-specific roadmap while preserving old roadmaps.

## What David should test next

With duplicates disabled, use:

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
37_racebuilder_v0_4_16_7_1_window_open_fix.zip
```

First test only the open issue:

1. Start Freeroam.
2. Press the RaceBuilder hotkey or use Hub Race/Event -> Open RaceBuilder UI.
3. Confirm the RaceBuilder window stays open.
4. Confirm Race Lights and Score Card can stay open.

Only if that passes, test catalog:

1. Set Start / CP / Finish still works.
2. Lights and scoreboard still work.
3. Create Trailer Figure-8 metadata/preset.
4. Save race.
5. Refresh/rebuild catalog.
6. Confirm race appears.
7. Search/filter/favorite it.
8. Load it.
9. Edit one gate.
10. Replace saved race.
11. Save as new copy.

## Next RaceBuilder build if v0.4.16.7.1 passes

```text
37_racebuilder_v0_4_16_8_trailer_figure8_template_rules.zip
```

AI spawning remains after catalog/rules pass testing.
