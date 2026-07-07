# RF-RACE01 Active Working Status

Timestamp = 2026-07-07 14:35 America/Los_Angeles
Chat ID = RF-RACE01
Chat Name = Project 37 RaceBuilder Chat
Message type = STATUS / ACTIVE COORDINATION
Screen status = 🟨 NEEDS TEST
Assigned role = RaceBuilder development chat / Project 37 race setup and catalog owner

## Current RaceBuilder build under test

```text
37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip
```

## Current paired Hub test build

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
```

## Base used

David rolled back to:

```text
37_racebuilder_v0_4_16_5_gate_editing_race_library GOOD.zip
```

v0.4.16.5 GOOD keeps gate editing and the basic race library. It does not include the later v0.4.16.6 AI roster/rules or v0.4.16.7 catalog fields.

## What v0.4.16.5.1 adds

- Window open-state BoolPtr fallback fix.
- Player racer count separated from AI racer count.
- AI roster with generated names and editable names.
- AI vehicle class/model/config fields.
- Grid layout settings: 1/2/3/4 lines, staggered, side spacing, back spacing, auto-fit to Start gate width.
- Terrain-height leveling for Start/CP/Finish gate endpoints.
- Build AI Grid button.
- Spawn AI Racers button using the same BeamNG vehicle creation API pattern seen in reference mods.
- Clear Spawned AI button.
- RaceBuilder still owns gameplay. Hub remains a UI shell.

## Not done yet

- AI path driving is not proven yet. This build stages vehicles first.
- Trailer auto attach is not implemented yet.
- Vehicle picker/catalog is not implemented yet.
- Full v0.4.16.7 catalog/index/filter work is not included because this build starts from v0.4.16.5 GOOD.

## Test order

With duplicates disabled, use only:

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip
```

Test:

1. RaceBuilder opens from hotkey or Hub.
2. Set Start / CP / Finish.
3. Press Level All Gates To Ground.
4. Set Player Count = 1.
5. Set AI Count = 3 first.
6. Pick AI Class = Mixed or Truck.
7. Set Grid Lines = 2 and Layout = staggered.
8. Press Build AI Grid.
9. Press Spawn AI Racers.
10. If 3 spawn correctly, then try 8. Try 20 only after smaller counts pass.

## Next build if this passes

```text
37_racebuilder_v0_4_16_5_2_ai_drive_path_test.zip
```

Target: make one spawned AI drive Start -> CP -> Finish before adding trailer attach or large fields.
