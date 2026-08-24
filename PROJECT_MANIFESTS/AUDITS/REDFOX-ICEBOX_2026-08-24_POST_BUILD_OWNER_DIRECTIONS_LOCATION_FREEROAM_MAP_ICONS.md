# RedFox Icebox — Post-Build Owner Directions: Location Choice, Free Roam Bridge, Map Icons

Date: 2026-08-24
Related build: `RedFox_Icebox_v0_1_0_STANDALONE_GARAGE_LAB.zip`
Related base audit: `PROJECT_MANIFESTS/AUDITS/REDFOX-ICEBOX_2026-08-24_v0.1.0_STANDALONE_GARAGE_LAB.md`
Status: OWNER DIRECTIONS / NOT YET IMPLEMENTED

## Critical status

The owner asked these questions/requirements **after** Icebox v0.1.0 was packaged.

No Icebox code was changed in response to these directions before this handoff. Treat everything below as the next design/test requirements, not as functionality already present in v0.1.0.

## 1. Owner must choose the Icebox physical location

The owner does not want Icebox silently choosing a garage/location for them.

Current v0.1.0 behavior:

- Icebox has a synthetic logical garage ID with capacity 10.
- It automatically chooses a real current-map garage as a temporary physical anchor so stock Career/RLS retrieve/edit/paint/parts/tuning flows have real parking/zones/computer facilities.
- The control window reports the selected anchor, but the owner cannot choose/change it in v0.1.0.

Next required behavior:

- add an obvious `SET ICEBOX LOCATION` / `CHANGE ICEBOX LOCATION` flow;
- show all valid existing garages/facilities on the current map;
- let the owner explicitly choose the anchor;
- persist that choice for the map/save as appropriate;
- always display the selected physical location clearly in the Icebox control UI;
- never silently switch anchors unless the saved anchor is invalid/missing, and if fallback is necessary, tell the player.

The physical anchor must not merge Icebox inventory with the real garage's inventory.

Borrowing an existing garage's parking spots/zones/computer must **not**:

- move vehicles already stored in that garage;
- rename that garage;
- consume or rewrite that garage's stored vehicle ownership;
- make Icebox vehicles count as the physical garage's normal stored vehicles if the synthetic logical storage architecture can prevent it.

## 2. Existing garage attachment should be optional, not permanent architecture

The owner asked whether Icebox has to attach to an existing garage.

Long-term answer/design direction: **no**.

An existing garage anchor was chosen for v0.1.0 only as the fastest safe way to prove the stock Career/RLS garage UI/actions.

After the stock garage behavior is proven, build a standalone custom-location mode such as:

`MAKE ICEBOX HERE`

That custom location should persist enough information to behave as an independent garage/shop, including at minimum as supported by exact BeamNG/RLS APIs:

- level/map ID;
- world position;
- orientation;
- one or more retrieve/parking positions;
- computer/interaction location;
- map marker location;
- logical garage identity/capacity.

Do not invent facility internals. Source-first inspect exact BeamNG 0.39/RLS 2.7.0.1 facility/garage/computer/parking APIs before implementing a custom facility.

## 3. Free Roam access to Career vehicles

Owner request/question:

> Can Icebox be used as a way to load Career vehicles in Free Roam as well?

Desired capability: **yes if it can be done safely after exact source verification**, but this is NOT built in v0.1.0 and must not be claimed as working yet.

The goal is for Icebox to become a controlled bridge where the player can select a vehicle saved in a Career profile/Icebox and hydrate/spawn that vehicle while in Free Roam.

Safety requirements:

- do not silently modify a Career save while the player is in Free Roam;
- default Free Roam spawning should be read-only/copy-based unless a separately designed explicit write-back workflow is approved;
- preserve the saved vehicle's model/config/paint/part-condition/mileage data where the exact APIs support it;
- avoid creating duplicate authoritative Career inventory records;
- clearly identify which Career save/profile and which vehicle is being read;
- if exact Career save/inventory modules are not safely available in Free Roam context, build an explicit exported Icebox snapshot/index rather than poking live Career modules blindly;
- source-first verify save path/profile APIs and vehicle hydration methods before implementation.

Potential future modes to evaluate after source audit:

1. **Read-only Free Roam Spawn** — spawn a copy of a selected Icebox/Career vehicle; changes in Free Roam do not write back.
2. **Explicit Export/Import** — export exact vehicle snapshot to Icebox's own data and spawn that in Free Roam.
3. **Explicit Write Back** — only if later approved, provide a deliberate action to save Free Roam changes back to the Career/Icebox vehicle with backup/transaction protection.

For the initial feature, favor read-only spawning to protect Career data.

## 4. Main Map + minimap icons

Owner wants both **Tow Yards** and the **Icebox** to show on:

- the main map;
- the minimap.

This is a required future UI/navigation feature.

### Tow Yard markers

Every configured RedFox Tow Yard should have a map marker using its saved yard location.

Desired behavior:

- visible on main map;
- visible on minimap where BeamNG/RLS marker APIs support it;
- persistent for purchased/configured Tow Yards across reloads;
- yard name displayed on hover/selection where supported;
- distinguish Tow Yard from ordinary garages/businesses;
- all yards can be seen, not just the active/current yard, subject to the game's normal map-level filtering (other-map yards obviously cannot occupy coordinates on the current level's map).

### Icebox marker

The Icebox should show a distinct marker at its chosen physical/custom location.

If Icebox is still using a real-garage anchor during testing, the marker should identify **RedFox Icebox**, not misleadingly rename the underlying real garage.

If/when `MAKE ICEBOX HERE` exists, the marker should use the custom saved location.

### Implementation rule

Do not guess marker APIs. Inspect current BeamNG/RLS map/POI/minimap registration code and use the same supported mechanism as native facilities/missions where possible.

## 5. Tow shipping direction reinforced

The garage lab is being built because the final Tow garage must support business vehicles across maps.

Owner's intended future workflow:

1. Travel to a new map.
2. Set up a new Tow shop/yard on that map.
3. Open the new yard.
4. Request/ship selected company trucks/equipment from another Tow Yard, even if that source yard is on another map.
5. Initially prove this with direct saved garage-to-garage reassignment.
6. Later route the transfer through a dedicated shipping/delivery location where the vehicle can be picked up.

Because stored vehicles are save records rather than permanently living world objects, cross-map movement should not require loading the source map merely to change the stored destination.

## 6. Why Icebox remains separate from Tow for now

Do not port another speculative garage implementation into JOB-09.

First prove in Icebox:

- stock garage vehicle list presentation;
- correct image sizing through native stock components;
- normal left-click/right-click/select/popover behavior;
- Favorite (multiple vehicles);
- Retrieve/Replace;
- Repair;
- Rename/plate;
- Paint;
- Parts/config/tuning;
- Put Away;
- save/reload;
- location selection;
- cross-map retrieval/assignment.

Only after that architecture works should JOB-09 consume it and add Tow-specific actions such as Move to Tow Yard, shipping, business ownership, custody and accounting.

## 7. Do not change Tow while proving Icebox

The owner explicitly chose Icebox to stop repeatedly changing the Tow mod while garage architecture is still being discovered.

Any future Icebox test build should remain standalone and should not modify JOB-09 files unless the owner specifically asks to port proven behavior back into Tow.
