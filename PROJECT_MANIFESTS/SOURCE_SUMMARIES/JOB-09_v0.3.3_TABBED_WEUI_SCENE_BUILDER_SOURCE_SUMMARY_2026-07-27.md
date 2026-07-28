# JOB-09 v0.3.3 — Source Summary

## Baseline

v0.3.3 is built from the v0.3.0 source that David reported as working. The v0.3.1 artificial tow-shop garage implementation is deliberately excluded.

## Top-level WEUI sections

1. Dispatch Center
2. Scene Builder
3. Records & History
4. Tow Yard Inventory
5. Company Fleet
6. Tow Yard Management
7. Settings
8. Development Tools

The navigation remains at the top of the main window. Clicking a section changes only the content below.

## Dispatch Center

- random and exact test call requests;
- incoming-call accept/decline;
- target vehicle shown before general call details;
- colored tow-equipment recommendation;
- target route/dropoff information;
- blacklist and whitelist for exact model/configuration;
- saved category recataloging and undo;
- no Scene Builder controls;
- no Temporary Vehicle Spawn Lab.

## Scene Builder

Scene Builder tracks active tow targets, support vehicles, and quick-spawned equipment.

Highlight state:

- green — included and saveable;
- yellow — selected;
- red — excluded;
- gray — detected but insufficient stable metadata for safe replay.

The builder supports:

- accepting the current scene;
- Scene Editor and highlight toggles;
- selecting items from a synchronized list;
- include/exclude controls;
- deleting non-target scene equipment/support;
- undo for inclusion changes and last quick spawn;
- saving adjusted relative transforms as a new template;
- selecting/replaying/deleting saved templates;
- rejecting the active scene and requesting the same call type again.

Saved templates retain `targets[]` and add a schema-v2 `equipment[]` collection. Equipment is respawned as scene support rather than as a tow target.

## Quick scene equipment

The source searches installed eligible vehicle/prop metadata for:

- traffic cones;
- roadside warning signs;
- barricades;
- flares/warning markers;
- debris/roadside hazards.

It does not substitute a random normal road vehicle when no matching prop is found.

## Tow-yard management

- list and select yards on the current map;
- navigate or move the test marker;
- add another yard marker;
- edit and save a custom RedFox yard name;
- preserve the yard's stable internal ID;
- show custody/company capacity and pending-payment summaries.

## Company movement safety lock

The v0.3.0 transfer path that removed the RLS inventory record remains in source only under an explicitly named legacy-unsafe function and is unreachable from normal public/UI transfer calls.

Public transfer and legacy retrieval calls return without changing a vehicle and show a warning. Existing saved Fleet Book/company records remain readable for future migration.

## Garage Hub contract

Preserved functions:

- `openWindow`
- `closeWindow`
- `toggleWindow`
- `isWindowOpen`
- `minimizeWindow`
- `restoreWindow`
- `openSettingsWindow`
- `openGameUI`
- `applyGlobalTheme`
- `applyGlobalFontScale`
- `applyGlobalButtonScale`
- `applyGlobalTextColor`
- `applyGlobalButtonTextColor`
- `setUseLocalOverride`
- `getModuleStatus`

## Deferred

- existing purchased-property computer activation;
- binding RedFox yard identity to the real RLS garage ID;
- free owned-company transfers to that real garage;
- migration from v0.3.1 artificial Tow Yard 1;
- business accounting, upgrades, and insurance;
- guaranteed cone/sign assets when no compatible installed prop configuration exists.
