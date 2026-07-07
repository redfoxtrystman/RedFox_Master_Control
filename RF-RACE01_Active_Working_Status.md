# RF-RACE01 Active Working Status

Timestamp = 2026-07-06 19:58 America/Los_Angeles
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

## Current paired Hub

```text
1-RedFox_GarageHub_v0_5_8_RememberDockedModules.zip
```

Optional temporary overlay if Hub scan crashes:

```text
1-RedFox_GarageHub_v0_5_8_1_ModuleScannerMsgHotfix_OVERLAY.zip
```

## Active objective

Focus on RaceBuilder catalog core before AI spawning or trailer-race gameplay expansion.

The catalog must show saved races, filter them, favorite them, load/edit/replace/save-as-new, and store race metadata/assets per map.

## Current Hub blocker

David reported a Hub scanner Fatal Lua Error during scan:

```text
lua/ge/extensions/redfox/modulesHub.lua:483: attempt to call global 'msg' (a nil value)
```

This is Hub-side. The screenshot showed the scan found:

```text
lua/ge/extensions/redfox/modules/redfox_race_manager/redfox_module.json
```

So RaceBuilder is discoverable before the Hub scanner crashes. RF-HUB01 should fix `scanRedFoxModules` by defining/guarding/replacing `msg()`.

## What other chats need to know

- Do not restart Project 37 from scratch.
- Do not resume the failed 37A/37B/37C split.
- Do not move race gameplay into GarageHub.
- Do not rename RaceBuilder `moduleId`, `windowId`, extension name, manifest path, settings path, or bridge function names without approval.
- Every RaceBuilder version must update `_redfox_dev_notes` and include a new version-specific roadmap while preserving old roadmaps.

## What David should test next

With duplicates disabled:

1. Hub opens.
2. RaceBuilder opens.
3. Set Start / CP / Finish still works.
4. Lights and scoreboard still work.
5. Create Trailer Figure-8 metadata/preset.
6. Save race.
7. Refresh/rebuild catalog.
8. Confirm race appears.
9. Search/filter/favorite it.
10. Load it.
11. Edit one gate.
12. Replace saved race.
13. Save as new copy.

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
