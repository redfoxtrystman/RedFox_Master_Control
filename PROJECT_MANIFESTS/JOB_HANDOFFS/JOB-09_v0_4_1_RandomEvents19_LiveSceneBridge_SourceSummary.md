# JOB-09 v0.4.1 Source Summary

## Version

`0.4.1 — Random Events 1.9 Live Scene Bridge`

## Source design

JOB-09 loads the installed Random Events dependencies through:

- `randomEvents/mapScanner`
- `randomEvents/spawning`
- `randomEvents/events/<selected scene>`

The selected module's `spawn(playerPos, config, scanner)` creates the source scene. JOB-09 inventories the returned instance, classifies targets/support/equipment, creates the paid call, and retains the source module/instance so `despawn(instance)` restores temporary road changes and cleans the entire scene.

JOB-09 does not contain a copied `lua/ge/extensions/randomEvents/` tree and does not override the Random Events manager.

## JOB-09 ownership after adoption

- Paid tow call and reward
- Route and destination
- Target completion
- Records/invoices
- Scene Builder transforms and full roster
- Saved templates and replay
- Catalog/blacklist controls
- User-facing status and failure logging

## Random Events ownership retained

- Source road/parking selection
- Initial scene arrangement
- Damage/effects and props
- Traffic-drivability changes
- Original scene cleanup/restoration

## New persistent data

`settings/redfox/tow_scene_equipment_mappings.json`

This stores exact model/configuration mappings for cones, signs, barriers, debris, police, ambulance, fire, tow support, arrow-board trailers, and future taught roles.

## Key logs

- `[RedFox][TOW][RANDOM_EVENTS_BRIDGE]`
- `[RedFox][TOW][EQUIPMENT_LEARN]`

## Runtime dependency

Random Events 1.9.0.0 must be installed and enabled for live imported scenes. Normal JOB-09 systems remain usable when it is absent.