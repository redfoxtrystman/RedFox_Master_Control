# JOB-09 v0.3.0 — Catalog Overrides, Yard Search, and Test Storage

Date: 2026-07-26

## Identity

- Job: JOB-09 — Tow / Recovery / Dispatch
- Module: `redfox_tow_recovery_dispatch`
- Build: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_0_CatalogOverridesYardSearchTestStorage.zip`
- SHA-256: `124bbf853b7c79c8b750822c6a8d29dc5353c7dc4b0d73d1c12c636af4ef391d`
- Size: 184,358 bytes
- Status: **BUILT — RUNTIME UNTESTED**

The installable ZIP remains outside GitHub. This record documents the exact candidate.

## Reported failures addressed

- Vehicle record could not conveniently be closed after expanding it.
- Crane chains and boom-section props were being treated as towable passenger/rollover targets.
- There was no saved blacklist, whitelist, category correction, or undo system.
- Active-call target and recommended equipment were not prominent.
- Development-spawned boats, aircraft, props, trailers, and other unusual objects could not be stored in the Tow Yard for retrieval testing.
- Company Fleet Garage transfer was difficult to locate in the WE UI.
- Stored abandoned vehicles could not be searched after delivery when roadside searching was forgotten.

## Implemented

### Exact configuration catalog overrides

Each override is stored by exact model/configuration key.

Available saved categories:

- Passenger / Light Vehicle
- Motorcycle / Three-Wheel
- Tow Truck / Recovery Equipment
- Heavy / Vocational Truck
- Semi Tractor
- Trailer / Lowboy / Carrier
- Bus / Coach / Skoolie
- Boat / Watercraft
- Aircraft / Helicopter
- Construction / Industrial
- Rail / Train
- Roadside Hazard / Lost Prop
- Other Non-Road / Unclassified

Active target controls can:

- blacklist the exact configuration from future RedFox calls;
- mark it approved/whitelisted;
- set its exact category;
- undo the active-target override.

Settings include a saved-override browser with undo-blacklist/whitelist, undo-category, and clear-all controls.

Known crane-chain and boom-section prop names are classified as `Roadside Hazard / Lost Prop`. Normal car, rollover, semi, and abandoned selectors reject non-road/roadside-hazard categories.

The former fallback that treated every model literally named `trailer` as a fifth-wheel trailer was removed. Physical fifth-wheel coupling is still deferred.

### Active-call emphasis

The top of the active-call panel now emphasizes:

- `TARGET VEHICLE` in cyan;
- `RECOMMENDED TRUCK / EQUIPMENT` in amber;
- detected vehicle category.

The current WE Dear ImGui path does not guarantee a separate bold font, so strong uppercase/color emphasis is used.

### Stored abandoned search

An abandoned vehicle may be searched once either roadside or after storage. Search state and result transfer into the yard record, preventing double searching.

Color states:

- orange: not searched / search available;
- gray: searched / nothing found;
- green: searched / result found.

Log: `[RedFox][TOW][YARD_SEARCH]`.

### Development vehicle yard storage

The Temporary Vehicle Spawn Lab can store its last spawned test object in a selected Tow Yard under `Development Test Storage`.

This supports test records for boats, aircraft, trailers, props, construction equipment, and other catalog categories. Records can be saved/reloaded, searched, sorted, physically retrieved, returned to virtual storage, or explicitly removed. They cannot generate payment or sale proceeds.

Log: `[RedFox][TOW][DEV_YARD_TEST]`.

### Vehicle-record close control

Expanded yard records now include `CLOSE THIS VEHICLE RECORD` at the bottom.

### Company transfer visibility

The selected Fleet Book unit now exposes a prominent transfer button without requiring the full technical-details panel:

`TRANSFER SELECTED CURRENT TRUCK FROM PERSONAL INVENTORY TO COMPANY GARAGE`

The v0.2.9 verified-transfer sequence remains unchanged.

## Boundary and static checks

- Only JOB-09 runtime code and JOB-09 package documentation were changed.
- No stock Career/RLS, JOB-01, JOB-02, JOB-04, JOB-06, JOB-08, JOB-10, or JOB-11 runtime files were included.
- ZIP integrity: PASS
- JSON parsing: PASS
- Lua syntax/loadfile: PASS
- Lua main-chunk local-variable limit: PASS
- Protected path scan: PASS
- New per-frame console logs: none
- New per-frame save writes: none

Packaged evidence includes verification reports, file inventory, file tree, and the v0.2.9-to-v0.3.0 patch diff.

## Required runtime test

1. Disable older JOB-09 ZIPs and enable only v0.3.0.
2. Confirm Fleet Book, Company Fleet Garage, yard inventory, history, and settings persist.
3. On a wrong active target, open catalog controls, assign the correct category, blacklist it, cancel the existing call, and verify it does not return in later RedFox calls.
4. Use Settings to undo the saved override and verify it becomes eligible again where its category permits.
5. Store an unsearched abandoned vehicle, search it once in the yard, reload, and verify state/result persistence.
6. Spawn a boat or aircraft in the Spawn Lab, store it in the Tow Yard, save/reload, retrieve it, return it, and remove the development test record.
7. Expand a yard record and close it from the bottom button.
8. Transfer one noncritical Career-owned registered tow truck to Company Fleet Garage, save/reload, retrieve it, return it, and verify no duplication or loss.

Stop immediately on duplication, loss from both inventories, inability to return a retrieved company unit, or save corruption.
