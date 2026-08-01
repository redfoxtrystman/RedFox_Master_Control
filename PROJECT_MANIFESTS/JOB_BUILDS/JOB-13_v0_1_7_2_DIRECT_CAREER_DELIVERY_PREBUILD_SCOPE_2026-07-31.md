# JOB-13 v0.1.7.2 — Phone-Only Direct Career Delivery Critical Repair Scope

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Source: RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_1_DROPDOWN_VISIBILITY_HOTFIX.zip

## Runtime blocker

An auction-purchased vehicle could be created and driven, but retrieving it after delivery caused a repeating global interaction loop that blocked the phone, Escape/menu input, garage interfaces, and produced severe lag. Garage thumbnails were also blank.

## Product boundary

JOB-13 is phone-only. The auction website, bidding, winning, payment status, delivery status, notifications, and retry actions must all be available through the phone. This repair must not add or require a computer-facing JOB-13 interface.

Career garage and vehicle systems may still be used internally for storage and delivery because they are the game's authoritative systems, but JOB-13 will not depend on a computer menu or computer lifecycle.

## Confirmed root cause

JOB-13 used the menu-oriented RLS functions `openPurchaseMenu` and `buyFromPurchaseMenu` outside their normal UI lifecycle. That could leave global vehicle-shopping/input state half-open even though the auction itself was opened from the phone.

## Locked repair scope

- Remove JOB-13 use of `openPurchaseMenu` and `buyFromPurchaseMenu`.
- Do not create a temporary dealership/shop listing.
- Do not open, close, or depend on a computer menu.
- Use existing Career/RLS primitives directly: Career cash, native vehicle spawn, part-condition initialization, inventory add, garage-capacity validation, garage assignment, insurance hook, delivery access delay, save system, and thumbnail capture.
- Never call `career_career.closeAllMenus()` during auction settlement.
- Preserve all v0.1.7.1 phone auction UI, bidding, NPC bidding, quick bid, notifications, upcoming lots, varied cached pool, and dropdown hotfix unchanged.
- No edits to JOB-04, JOB-09, BeamBook, Welcome/Home, shared phone layout, shared computer code, or RLS source files.

## Verification gate

1. Lua parses.
2. JavaScript/CSS remain byte-identical to v0.1.7.1.
3. No `openPurchaseMenu`, `buyFromPurchaseMenu`, temporary shop ID, `closeAllMenus`, or JOB-13 computer UI dependency remains.
4. Successful path adds exactly one Career vehicle, charges exactly once, assigns a native garage, initializes metadata/insurance, requests thumbnail capture, and removes the temporary spawned object after capture.
5. Failure before finalization charges nothing and deletes the temporary vehicle.
6. Existing processed-request idempotency remains.
7. The phone remains usable before and after purchase, retrieval, entering, and exiting the delivered vehicle.
8. ZIP contains only JOB-13 paths and no shared core overrides.

Runtime remains unproven until David tests the exact output ZIP.