# RF-RACE01 Project 37 RaceBuilder Handoff

Timestamp = 2026-07-06 19:52 America/Los_Angeles
Chat ID = RF-RACE01
Chat Name = Project 37 RaceBuilder Chat
Message type = HANDOFF / STATUS
Screen status = 🟨 NEEDS TEST
Assigned role = RaceBuilder development chat / Project 37 race setup and catalog owner

## Files read

- RedFox_Worker_Chat_Quick_Start.md
- RedFox_Chat_Message_Board.md
- RedFox_Module_Status_Table.csv
- RedFox_Test_Results_Table.csv
- RedFox_GarageHub_Mod_Bridge_Requirements.md supplied by David in chat
- Project 37 Exit Roadmap / handoff supplied by David in chat

## Local builds created in chat

- 37_racebuilder_v0_4_16_4_hub_bridge_requirements_compliance.zip
- 37_racebuilder_v0_4_16_5_gate_editing_race_library.zip
- 37_racebuilder_v0_4_16_6_ai_roster_route_rules.zip
- 37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip
- 1-RedFox_GarageHub_v0_5_8_1_ModuleScannerMsgHotfix_OVERLAY.zip
- Project37_RaceBuilder_Catalog_Taxonomy_AI_Research_2026_07_01.xlsx
- Project37_AI_Route_Racer_Code_Source_Map_2026_07_01.zip

## RaceBuilder status

Current latest RaceBuilder test build is:

```text
37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip
```

This build was made from the recovered v0.4.16 line. Do not restart from scratch. Do not resume the failed 37A/37B/37C split. Do not bring back the old broken GM catalog as the main path.

## What changed across recent RaceBuilder builds

### v0.4.16.4

- Updated RaceBuilder toward the RedFox Garage Hub bridge contract.
- Hub should control UI shell only.
- RaceBuilder keeps gameplay, race logic, scoring, rules, and saves.
- Manifest path remains `lua/ge/extensions/redfox/modules/redfox_race_manager/redfox_module.json`.
- Added/confirmed shell bridge functions such as open, close, toggle, status, settings, game UI, and theme hooks.

David later found duplicate mods were the cause of a major Hub/RaceBuilder break. After removing duplicates, v0.4.16.4 with GarageHub v0.5.8 looked good. Treat as a user-reported sanity pass, not a full stable pass.

### v0.4.16.5

- Added post-placement gate editing.
- Select Start / CP / Finish after placement.
- Adjust width, rotation, and move selected gate to vehicle position.
- Added race library foundation: favorites, load, replace, save as new, delete safety.
- Added first Race Line / AI route node storage and debug line display.

### v0.4.16.6

- Added AI roster and race rule data foundation.
- Added racer count, generated names, personality/style fields, contact-rule data, and AI grid plan.
- Added route recorder and route node editing controls.
- Real AI vehicle spawning was not implemented yet.

### v0.4.16.7

- Added catalog core index: `settings/redfox/motorsports/race_catalog_index.json`.
- Added catalog metadata fields: race type, subtype, vehicle class, venue/map, preview path, trailer-required.
- Added filters: search, current map, favorites, race type, vehicle class, venue, preview-only, asset-only.
- Added large race/event suggestion list.
- Added Trailer Figure-8 preset foundation.
- Added rules foundation and asset manifest placeholder.
- `getRaceLibrary()` returns fuller catalog entries.
- No Hub files were edited.
- No AI spawning was added.

## Current Hub blocker found while testing v0.4.16.7

David got this Hub scanner error:

```text
lua/ge/extensions/redfox/modulesHub.lua:483: attempt to call global 'msg' (a nil value)
```

The screenshot showed Hub scan found module manifests, including:

```text
lua/ge/extensions/redfox/modules/redfox_race_manager/redfox_module.json
```

Interpretation:

- This is a Hub-side scanner failure, not a RaceBuilder catalog crash.
- RaceBuilder manifest is discoverable.
- Hub scanner calls `msg(...)` without defining or guarding it.
- RF-HUB01 should fix `scanRedFoxModules` by defining local `msg()`, replacing the call with safe logging, or guarding the call.

Temporary overlay created in this chat:

```text
1-RedFox_GarageHub_v0_5_8_1_ModuleScannerMsgHotfix_OVERLAY.zip
```

This overlay is not the final Hub rebuild.

## What David needs to test next

Use only intended ZIPs and no duplicates:

```text
1-RedFox_GarageHub_v0_5_8_RememberDockedModules.zip
37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip
optional overlay only if Hub scan still crashes: 1-RedFox_GarageHub_v0_5_8_1_ModuleScannerMsgHotfix_OVERLAY.zip
```

Test:

1. Hub opens.
2. RaceBuilder opens.
3. Set Start / CP / Finish still works.
4. Lights and scoreboard still work.
5. Create Trailer Figure-8 metadata/preset.
6. Save race.
7. Rebuild/refresh catalog.
8. Confirm saved race appears.
9. Search/filter by Trailer / Figure-8 / current map / favorite.
10. Favorite it.
11. Load it.
12. Edit one gate.
13. Replace saved race.
14. Save as new copy.

## Next objective after v0.4.16.7 passes

Build:

```text
37_racebuilder_v0_4_16_8_trailer_figure8_template_rules.zip
```

Target:

- Formal Trailer Figure-8 template.
- Rule panel with disqualification options.
- Trailer required / trailer loss penalty.
- Wrong-way penalty setting.
- Contact rules: clean, rubbing allowed, demo-style, custom.
- AI setup fields tied to catalog: count, vehicle class, personality, trailer requirement.
- Asset manifest expansion for props/trailers/lights/sideline markers.

## Critical rules

- Every RaceBuilder version must update `_redfox_dev_notes` and add a new version-specific roadmap.
- Keep prior roadmaps/history intact.
- Do not rename moduleId/windowId/extension names unless approved.
- Do not move gameplay into the Hub.
- Do not fake runtime verification.
