# JOB-09 — Temporary Vehicle Spawn Lab v0.2.8

**Module:** `redfox_tow_recovery_dispatch`  
**Visible name:** RedFox Tow & Recovery Dispatch  
**Build:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_8_TemporaryVehicleSpawnLab.zip`  
**SHA-256:** `cf690a13f7b2a4783f767387f082966dbd4cef977c9f31eb5d80643a3efae244`  
**Status:** BUILT — RUNTIME UNTESTED

## Scope

This build adds one isolated temporary WE UI testing tool. It does not change normal dispatch, payouts, Fleet Book behavior, tow-yard records, or Career inventory.

The new Temporary Vehicle Spawn Lab appears below the normal call chooser when there is no offer or active call. It scans the installed eligible-configuration catalog and reports counts for:

- Passenger / light vehicles
- Motorcycles / three-wheelers
- Tow trucks / recovery equipment
- Heavy / vocational trucks
- Semi tractors
- Trailers / lowboys / carriers
- Buses / coaches / skoolies
- Boats / watercraft
- Aircraft / helicopters
- Construction / industrial equipment
- Rail / trains
- Other non-road / unclassified vehicles

Each button spawns one random detected configuration near the player and emits one `[RedFox][TOW][DEV_SPAWN]` log line. The pool is cached for the session; no catalog scan or spawn logging is performed per frame.

Temporary test vehicles:

- do not create calls;
- do not pay;
- do not enter RedFox tow-yard storage;
- do not enter Career inventory;
- can be removed individually or all at once;
- are cleaned up when the extension unloads.

## Static verification

- ZIP integrity: PASS
- JSON parsing: PASS
- Lua syntax: PASS
- Lua main-chunk local-variable limit: PASS
- Protected Career/shared UI path scan: PASS
- No per-frame console logging added: PASS
- No per-frame JSON writes added: PASS

## Required runtime test

1. Disable older JOB-09 ZIPs and enable only v0.2.8.
2. Open the Temporary Vehicle Spawn Lab with no active dispatch.
3. Screenshot the category counts.
4. Spawn one vehicle from each nonzero category.
5. Record categories with zero candidates, wrong classifications, or spawn failures.
6. Test Remove Last and Remove All.
7. Confirm normal calls and saved Fleet Book/tow-yard data still work.

## Next priority: company/tow-garage storage

Registered work trucks must eventually become **company/tow-garage vehicles**, not personal Career-storage vehicles. This is not implemented in v0.2.8.

The next integration assessment must use the exact installed RLS/overhaul garage and inventory contract and preserve:

- vehicle model and exact configuration;
- paint;
- approximate condition;
- Fleet Book identity and call sign;
- assigned map and tow yard;
- company ownership state;
- attached trailer/cargo where support exists.

No cosmetic or fake personal-garage entry should be used as a substitute for real company storage.
