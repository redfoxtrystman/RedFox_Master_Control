# JOB-09 Decision — Dual Classification for Spawnable Equipment and Native Garage Storage

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Applies to:** JOB-09 Tow / Recovery / Dispatch  
**Status:** OWNER-APPROVED DESIGN DIRECTION

## Owner clarification

Spawnable objects such as `FP Crane Chains 2 rotatable chains`, walking-character configurations, attachments, props and other equipment may be treated by BeamNG as vehicle inventory objects and stored in native Career/RLS garages. They must not be blocked merely because they are not real-world titled road vehicles.

## Engine-facing classification

JOB-09 must preserve BeamNG's native spawn/inventory behavior:

- exact model/config identity;
- native Career inventory creation when accepted by `career_modules_inventory.addVehicle`;
- native purchased-garage placement;
- exact inventory ID persistence and duplicate prevention.

JOB-09 will not attempt to rewrite stock Career inventory classes or third-party JBeam files merely to force a separate engine object class.

## RedFox gameplay classification

JOB-09 will maintain a separate semantic classification layer:

```text
road_vehicle
trailer
emergency_vehicle
equipment
attachment
prop
walker
heavy_machine
other_spawnable
```

This RedFox classification controls:

- which call types may select the item;
- whether abandoned/private-lien logic is appropriate;
- agency-paid versus private/default outcomes;
- display wording;
- valuation, sale, auction, scrap and equipment-storage behavior;
- scene roles and recovery requirements.

It does not decide whether native Career garage storage is allowed. Native garage eligibility follows actual BeamNG inventory acceptance for the exact model/config.

## Required v0.4.4.7 correction

1. Remove v0.4.4.6's equipment/attachment/walker garage-delivery block.
2. Allow exact spawnable records accepted by native Career inventory.
3. Keep exact transaction IDs, pending inventory IDs, rollback and duplicate protection.
4. Preserve RedFox equipment classification in the company record and transferred inventory metadata where possible.
5. Use equipment-specific UI wording rather than titled-vehicle wording.
6. Keep abandoned/lien selection filtering separate from garage delivery.
7. Do not edit Browser Core, JOB-04, JOB-13, Random Events, stock Career/RLS or third-party equipment/JBeam files.

## Long-term option

A dedicated RedFox Equipment Registry may later track capabilities, attachment type, tow/recovery role, storage requirements and whether an item may be sold, auctioned, scrapped or assigned to a company unit. The physical object may still remain a native BeamNG vehicle object under the engine.
