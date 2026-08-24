# RedFox Icebox — v0.1.0 Standalone Garage Lab

Date: 2026-08-24
Scope: standalone temporary garage architecture test
JOB-09 Tow status: intentionally untouched by this build
Paid RLS reference: exact supplied RLS Career Overhaul 2.7.0.1 split archive, reconstructed/read-only for source inspection before implementation

## Why Icebox exists

Repeated JOB-09 Tow garage experiments proved that imitating a garage UI or tagging ordinary personal Career inventory as company vehicles is the wrong place to continue experimenting. The owner requested a separate temporary mod so garage behavior can be mastered without changing Tow again.

RedFox Icebox is therefore deliberately small:

- one synthetic garage named `RedFox Icebox`;
- capacity 10;
- no bank/business economy;
- no Tow dependency;
- no automatic vehicle migration;
- one owned test vehicle at a time is the intended first test.

## Exact RLS / normal Career findings used

1. The current normal Career vehicle inventory UI already groups vehicles by `vehicle.location` and uses `career_modules_garageManager.getGarageCapacityData()` for garage name/capacity.
2. The stock `VehicleList.vue` / `VehicleTileRow.vue` already provides the interaction the owner wants: stock thumbnails/cards, selection popover, Retrieve/Replace, Repair, Put in Storage, Favorite, license plate, rename, and listing actions where permitted.
3. `career_modules_inventory.openMenuFromComputer(computerId)` opens that stock garage/vehicle-list route and resolves its current garage through `garageManager.computerIdToGarageId()` -> facility lookup.
4. `career_modules_inventory.moveVehicleToGarage(inventoryId, garageId)` preserves the same Career inventory identity and only changes the vehicle's garage location after checking garage capacity/facility existence.
5. RLS `garageManager.isGarageSpace(garageId)` and `getGarageCapacityData()` are sufficient narrow seams for a synthetic 10-slot garage. Icebox does **not** insert itself into RLS `purchasedGarages`, so it does not become a normal property purchase or automatically absorb unrelated vehicle purchases.
6. Moving a vehicle from a normal purchased garage to the Icebox location removes that vehicle from the source garage's stored count, thereby freeing the personal garage slot while the same vehicle remains in Career inventory.
7. The normal Career garage computer provides painting, part inventory/shop, tuning and vehicle inventory through a computer facility. Icebox synthesizes a computer by cloning a real current-map garage computer/physical garage as its temporary anchor.
8. Physical retrieve still needs a real parking area. Icebox therefore has a global logical storage ID but maps physical retrieval to a real garage on the currently loaded map. This is intentionally useful for later cross-map Tow shipping tests.

## v0.1.0 architecture

Stable synthetic IDs:

- garage: `redfoxIceboxGarage`
- computer: `redfoxIceboxComputer`

Logical capacity: 10 vehicles.

The extension wraps only these runtime lookup/capacity seams and restores them on unload:

- `freeroam_facilities.getFacility`
- `freeroam_facilities.getFacilityIfExists`
- `freeroam_facilities.teleportToGarage` only for the synthetic Icebox ID
- `career_modules_garageManager.isGarageSpace`
- `career_modules_garageManager.getGarageCapacityData`

All non-Icebox calls delegate to the prior exact functions.

## Current-map physical anchor

Icebox chooses a real physical garage on the current map so the stock Career retrieve/edit flows have real parking spots, zones and a computer tether.

Selection preference:

1. purchased/current-map garages first;
2. edit-capable computer preferred (vehicle inventory + painting + parts + tuning);
3. stronger normal garage computer capability preferred;
4. proximity breaks ties;
5. if no owned usable garage exists, fall back to another real current-map garage.

The synthetic garage keeps its own logical name/id/capacity but clones the anchor's real parking spots/zones. The synthetic computer clones the best matching real garage computer and exposes vehicle inventory, painting, part inventory/shop and tuning for this garage lab.

## Store test path

`STORE CURRENT PERSONAL VEHICLE IN ICEBOX`

- requires the player to be sitting in an owned Career vehicle;
- refuses auction-listed vehicles;
- refuses when Icebox is full;
- captures the live part-condition snapshot first;
- moves the same Career inventory ID to `redfoxIceboxGarage`;
- stores the previous personal garage identity as return metadata;
- removes only the live world object after the condition snapshot;
- saves Career;
- no purchase/sale money changes hands.

There is no automatic migration and no batch movement into Icebox.

## Stock UI test path

`OPEN ICEBOX VEHICLE LIST — STOCK GARAGE UI`

Calls the normal RLS/Career `career_modules_inventory.openMenuFromComputer("redfoxIceboxComputer")` path.

The test is specifically intended to verify that the Icebox appears as a normal stock garage group with the stock vehicle thumbnail/card behavior and normal click/popover actions rather than another custom RedFox card imitation.

Expected stock actions depend on normal Career permissions/state but include Retrieve/Replace, Repair, Put in Storage, Favorite, plate, rename and related normal vehicle inventory actions.

## Full garage computer test path

`OPEN FULL ICEBOX GARAGE COMPUTER — EDIT / PAINT / PARTS`

For this test, retrieve the Icebox vehicle first and remain at the physical anchor garage. Icebox then opens the normal Career computer using the synthetic computer that shares the anchor's real doors/physical zone.

This is intended to prove the normal edit/paint/parts/tuning workflow before any architecture is ported back into Tow.

## Cross-map test concept

The logical Icebox garage ID is save-based, not map-based.

A stored vehicle therefore remains assigned to `redfoxIceboxGarage` across map changes. On a newly loaded map Icebox resolves a new real physical anchor. The owner can then open the stock Icebox list and attempt to retrieve that same saved vehicle on the new map.

If this works reliably, the same principle can later become one independent synthetic garage per Tow Yard and support Tow Yard -> Tow Yard / map -> map transfer while physical pull-out happens at the destination yard.

## Return path

`RETURN TO PERSONAL GARAGE`

- requires the Icebox vehicle to be put away/not spawned;
- prefers its previous personal garage when that garage exists on the current map and has room;
- otherwise uses a current-map purchased garage with free space;
- moves the same Career inventory ID;
- no sale/purchase money changes hands;
- if no safe destination exists, the Icebox vehicle remains untouched.

A cleanup action can return all Icebox vehicles one at a time, stopping safely if a destination cannot be found.

## Files — exactly 4

1. `lua/ge/extensions/redfoxIcebox.lua`
2. `scripts/redfox_icebox/modScript.lua`
3. `mod_info/redfox_icebox/info.json`
4. `lua/ge/extensions/redfox/modules/redfox_icebox/redfox_module.json`

## Validation

- both Lua files pass Lua 5.4 syntax-only parsing via `luaL_loadbufferx`;
- both JSON files parse successfully;
- finished ZIP passes `unzip -t` with no compressed-data errors;
- extracted finished ZIP contains exactly the same four files and every file hash matches the source tree;
- JOB-09 files were not changed.

## Package

`RedFox_Icebox_v0_1_0_STANDALONE_GARAGE_LAB.zip`

SHA-256: `c59233e77dfab48dffa7eccbfebf403e01f40c796f7d98cc009606e9789442ec`

## Runtime proof still required

This build is source-verified and packaged, but BeamNG runtime still needs to prove:

1. source personal garage slot frees when one vehicle moves to Icebox;
2. stock garage list renders Icebox correctly;
3. stock vehicle click/popover actions work;
4. Retrieve physically spawns at the current-map anchor without a delivery charge;
5. normal garage computer can paint/parts/tune the retrieved Icebox vehicle;
6. Put Away/save/reload preserves identity/config/condition;
7. map change + retrieve hydrates the same Icebox vehicle at the new map's anchor;
8. return to personal garage restores the same vehicle safely.

Do not port this architecture into JOB-09 until those runtime tests pass.