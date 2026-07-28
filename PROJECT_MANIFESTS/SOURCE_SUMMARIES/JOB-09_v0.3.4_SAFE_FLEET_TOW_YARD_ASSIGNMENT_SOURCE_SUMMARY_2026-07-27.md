# JOB-09 v0.3.4 — Safe Fleet Tow-Yard Assignment Source Summary

Date: 2026-07-27

Runtime source:

`lua/ge/extensions/redfoxTowRecoveryDispatch.lua`

## Baseline

v0.3.4 is a focused patch over v0.3.3. v0.3.3 itself uses David-confirmed working v0.3.0 dispatch behavior and excludes the failed v0.3.1 artificial garage bridge.

## Fleet assignment implementation

New runtime state:

- `fleetAssignmentLevel`
- `fleetAssignmentYardId`

New Fleet Book functions:

- `assignmentYardsForCurrentMap()`
- `selectedAssignmentYard(unit)`
- `cycleAssignmentYard(direction, unit)`
- `assignUnitToSelectedYard(unit)`
- `clearUnitYardAssignment(unit)`

The assignment writes only:

- `unit.assignedLevel`
- `unit.assignedYardId`
- `unit.assignedYardName`
- `unit.businessAssignmentAt`
- `unit.status = assigned_to_tow_yard`

It then saves the RedFox state and records a single diagnostic line:

```text
[RedFox][TOW][FLEET_YARD_ASSIGNMENT]
```

## WEUI correction

Inside Company Fleet -> selected unit details, v0.3.4 now displays:

- assigned tow yard;
- assigned driver;
- current assignment target;
- previous/next yard controls when multiple yards exist;
- assign selected truck button;
- remove assignment button;
- explicit notice that the action does not move or delete the RLS vehicle.

## Future NPC-driver compatibility

New Fleet Book units initialize:

- `assignedDriverId = nil`
- `assignedDriverName = nil`
- `driverAssignmentStatus = unassigned`

Existing units are migrated in memory/save state to an unassigned driver status when the field is absent.

These fields are reserved for future employee/NPC drivers. No NPC spawning, pathing, job selection, payroll, shifts, convoy logic, or autonomous recovery behavior is included in v0.3.4.

## Unchanged safety locks

- `transferCurrentToCompanyGarage()` remains blocked and non-mutating.
- legacy Company Garage retrieval remains blocked.
- no artificial `redfox_towshop_*` garage is registered.
- no stock Career or RLS file is included or replaced.

## Preserved systems

- top-tab WEUI;
- Dispatch Center;
- Scene Builder;
- vehicle catalog blacklist, whitelist, and reclassification;
- records/history;
- custody yard inventory;
- custom tow-yard naming;
- Development Tools;
- Garage Hub open/close/theme/font/button contract.
