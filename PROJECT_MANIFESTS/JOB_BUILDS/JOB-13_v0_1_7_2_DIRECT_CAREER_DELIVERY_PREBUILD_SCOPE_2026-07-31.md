# JOB-13 v0.1.7.2 — Direct Career Delivery Critical Repair Scope

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Source: RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_1_DROPDOWN_VISIBILITY_HOTFIX.zip

## Runtime blocker

An auction-purchased vehicle could be created and driven, but calling it from a garage computer caused a repeating interaction loop that globally blocked garage computers, the phone, Escape/menu input, and produced severe lag. Garage thumbnails were also blank.

## Confirmed root cause

JOB-13 used the menu-oriented RLS functions `openPurchaseMenu` and `buyFromPurchaseMenu` from outside the normal dealership/computer UI lifecycle. This left global vehicle-shopping/computer UI state vulnerable to remaining half-open.

## Locked repair scope

- Remove JOB-13 use of `openPurchaseMenu` and `buyFromPurchaseMenu`.
- Do not create a temporary dealership/shop listing.
- Use existing Career/RLS primitives directly: Career cash, native vehicle spawn, part-condition initialization, inventory add, garage-capacity validation, garage assignment, insurance hook, delivery access delay, save system, and thumbnail capture.
- Never call `career_career.closeAllMenus()` during auction settlement.
- Preserve all v0.1.7.1 auction UI, bidding, NPC bidding, quick bid, notifications, upcoming lots, varied cached pool, and dropdown hotfix unchanged.
- No edits to JOB-04, JOB-09, BeamBook, Welcome/Home, shared phone layout, shared computer code, or RLS source files.

## Verification gate

1. Lua parses.
2. JavaScript/CSS remain byte-identical to v0.1.7.1.
3. No `openPurchaseMenu`, `buyFromPurchaseMenu`, temporary shop ID, or `closeAllMenus` call remains in JOB-13 settlement.
4. Successful path adds exactly one Career vehicle, charges exactly once, assigns a native garage, initializes metadata/insurance, requests thumbnail capture, and removes the temporary spawned object after capture.
5. Failure before finalization charges nothing and deletes the temporary vehicle.
6. Existing processed-request idempotency remains.
7. ZIP contains only JOB-13 paths and no shared core overrides.

Runtime remains unproven until David tests the exact output ZIP.