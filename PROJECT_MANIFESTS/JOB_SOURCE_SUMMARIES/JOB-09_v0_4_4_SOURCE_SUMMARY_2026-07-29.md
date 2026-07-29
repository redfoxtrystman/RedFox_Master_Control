# JOB-09 v0.4.4 Source Summary

Main extension: `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`

## Added

- Persistent exact model/config catalog at `settings/redfox/tow_vehicle_spawnable_catalog.json`.
- One-at-a-time WEUI classification for targets, support vehicles, equipment, props, hazards, decoration, and disabled items.
- Live Scene Builder item classification with immediate persistence.
- Filtering that keeps police-marked configurations and recovery props out of normal civilian target pools.
- External JSON manager at `_redfox_external_tools/RedFox_Tow_Data_Manager.html`.
- Saved-scene enable/disable support.
- Random Events 2.1 interface detection and warm-up support.
- Timber Spill and RV Trouble imports.

## Preserved

All v0.4.3 storage, garage transfer, lien, sale, auction, scrap, dispatch, traffic-control, portal, records, fleet, yard, and active-job-recovery systems remain.

## Boundaries

Random Events remains a separate installed mod. JOB-09 does not copy or replace its files. JOB-09 does not replace stock Career/RLS core files.
