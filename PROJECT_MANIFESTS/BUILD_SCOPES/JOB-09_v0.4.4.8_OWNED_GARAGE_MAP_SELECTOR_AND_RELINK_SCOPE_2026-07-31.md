# JOB-09 v0.4.4.8 Pre-Build Scope — Owned-Garage Map Selector and Relinking

**Date:** 2026-07-31
**Owner:** David / Captain
**Baseline:** JOB-09 v0.4.4.7
**Status:** OWNER APPROVED — SOURCE WORK MAY BEGIN

## Runtime problem

David selected the wrong purchased RLS garage because the existing chooser exposed confusing facility/street names and then treated the chosen garage as a persistent tow-yard link. The intended tow-shop garage was full, and the UI did not provide an obvious way to change or remove the saved link.

## Approved repair

1. Add a clear **Choose Garage on Map** action from claimed-shop and legacy-company records.
2. Present a full-screen JOB-09 garage-selection map using current RLS garage data rather than modifying the shared RLS Real Estate page.
3. Show only owned or otherwise valid accessible garages for delivery selection.
4. Each map marker/card must show:
   - translated facility/building name;
   - stable garage/facility ID;
   - map/level;
   - used slots, capacity and free slots;
   - current linked state;
   - current/nearby indicator where determinable.
5. Allow selecting a different garage at any time when no garage-delivery transaction is pending.
6. Add **Change Linked Garage**, **Unlink Garage**, and **Use Current/Nearby Owned Garage** actions.
7. A changed link affects future deliveries only and must not silently move vehicles already stored elsewhere.
8. Keep exact pending inventory IDs, duplicate prevention, rollback, source-record identity checks and final placement verification.
9. Add an explicit advanced recovery action to deliver to the selected garage even when reported full. It must be clearly labeled, require a second confirmation, and never run automatically.
10. Do not modify Browser Core, JOB-04, JOB-13, Random Events, stock Career/RLS, shared phone layout or the RLS Real Estate Vue page.

## Source basis

RLS `ui_phone_realEstate.requestGarageListings()` already supplies garage ID, translated name, capacity, vehicle count, ownership, distance and map coordinates. JOB-09 may consume equivalent facility/garage data in its own portal without replacing the shared Real Estate page.

## Deferred

Temporary scene-equipment spawning from the RLS quarry/facility-work pattern is documented separately and will not be mixed into v0.4.4.8.
