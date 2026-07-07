# RF-RACE01 Active Working Status

Timestamp = 2026-07-06 20:25 America/Los_Angeles
Chat ID = RF-RACE01
Chat Name = Project 37 RaceBuilder Chat
Message type = STATUS / ACTIVE COORDINATION
Screen status = 🟨 NEEDS TEST
Assigned role = RaceBuilder development chat / Project 37 race setup and catalog owner

## Purpose

This is not a handoff. RF-RACE01 is still the active RaceBuilder chat. This file exists so other RedFox worker chats can see what this chat is doing and coordinate without guessing.

## Current RaceBuilder build under test

```text
37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip
```

## Current paired Hub test build

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
```

This was built from David-uploaded:

```text
1-RedFox_GarageHub_v0_5_10_SpawnerBridgeFix.zip
```

## Active objective

Focus on RaceBuilder catalog core before AI spawning or trailer-race gameplay expansion.

The catalog must show saved races, filter them, favorite them, load/edit/replace/save-as-new, and store race metadata/assets per map.

## Current fix made in this chat

David reported RaceBuilder could not be opened/found from Hub. Inspection showed RaceBuilder v0.4.16.7 manifest was already Hub-compliant enough to be discovered, but Hub v0.5.10 had two Hub-side problems:

1. `scanRedFoxModules()` called `msg()` before the local `msg` upvalue was in scope, causing a nil global call.
2. The existing Race/Event top-bar buttons were still mostly placeholder actions and were not wired to RaceBuilder bridge functions.

Created local test artifact:

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
```

Changes:

- Fixed `msg()` scoping by declaring it before scanner/menu helper functions and removing the later shadowing local declaration.
- Added `ensureRaceManagerLoaded()` and `callRaceCommand()`.
- Linked Race/Event menu actions to RedFox Race Manager bridge functions:
  - Open RaceBuilder UI
  - Stage Players
  - Start Race Lights
  - Start Countdown / Race
  - Stop / Reset Race
  - Show Scoreboard
- Preserved Spawner bridge behavior from v0.5.10.
- No RaceBuilder gameplay was moved into Hub.
- No RaceBuilder ZIP was changed in this patch.

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
37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip
```

Test Hub/RaceBuilder link first:

1. Hub opens.
2. Hub Scan Modules does not crash.
3. Race/Event -> Open RaceBuilder UI opens RaceBuilder.
4. Race/Event -> Start Race Lights opens/stages RaceBuilder lights.
5. Race/Event -> Show Scoreboard opens scorecard.

Then test RaceBuilder catalog:

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

## Next RaceBuilder build if v0.4.16.7 passes

```text
37_racebuilder_v0_4_16_8_trailer_figure8_template_rules.zip
```

Planned scope:

- Formal Trailer Figure-8 race template.
- Rules/disqualification panel.
- Trailer required and trailer loss penalty.
- Wrong-way penalty option.
- Contact rules: clean, rubbing allowed, demo-style, custom.
- AI setup fields stored in catalog: count, vehicle class, personality, trailer requirement.
- Asset manifest expansion for props/trailers/lights/sideline markers.

AI spawning remains after catalog/rules pass testing.
