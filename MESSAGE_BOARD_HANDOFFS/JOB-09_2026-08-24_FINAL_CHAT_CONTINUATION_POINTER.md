# READ FIRST — JOB-09 Final Chat Continuation Pointer

Date: 2026-08-24
From: outgoing JOB-09 chat at chat limit
To: next JOB-09 chat
Status: CURRENT CONTINUATION POINTER — NO CODE CHANGES AFTER THE REQUESTS BELOW

## Start here

Read this master handoff first:

`MESSAGE_BOARD_HANDOFFS/JOB-09_2026-08-24_CHAT_MAX_HANDOFF_TOW_ICEBOX_GARAGE_MASTER.md`

Then read these two current audits:

- `PROJECT_MANIFESTS/AUDITS/REDFOX-ICEBOX_2026-08-24_v0.1.0_STANDALONE_GARAGE_LAB.md`
- `PROJECT_MANIFESTS/AUDITS/REDFOX-ICEBOX_2026-08-24_POST_BUILD_OWNER_DIRECTIONS_LOCATION_FREEROAM_MAP_ICONS.md`

For the last Tow garage attempt and why work moved into Icebox, read:

- `PROJECT_MANIFESTS/AUDITS/JOB-09_2026-08-24_v0.5.0.36_TRUE_BUSINESS_GARAGE_CROSS_MAP_TRANSFERS_RUNTIME_FINDINGS.md`

## Current build state

Tow latest tested build:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_5_0_36_TRUE_BUSINESS_GARAGE_CROSS_MAP_TRANSFERS.zip`

Do not continue speculative garage changes inside Tow yet. The owner explicitly asked to isolate garage research in a standalone lab first.

Current standalone lab:

`RedFox_Icebox_v0_1_0_STANDALONE_GARAGE_LAB.zip`

SHA-256:
`c59233e77dfab48dffa7eccbfebf403e01f40c796f7d98cc009606e9789442ec`

Icebox has a synthetic 10-slot garage and is intended to prove the normal Career/RLS garage UI and actions using one expendable vehicle at a time.

## Owner's latest exact directions

These are NOT implemented yet unless explicitly stated otherwise in later source/tests.

1. **Manual Icebox location choice.** The owner does not want Icebox silently selecting a physical anchor. Add an obvious setup/change flow so the player chooses the location and can always see which location is active.

2. **Existing garage attachment must be optional.** v0.1.0 borrows a real garage only to prove native garage behavior. Long-term add a true independent `MAKE ICEBOX HERE` custom location after exact facility/parking/computer APIs are verified.

3. **Borrowing an existing garage must not affect that garage's vehicles.** Do not move, rename, merge, consume, or rewrite vehicles already stored there.

4. **Free Roam vehicle bridge.** The owner asked for Icebox to become a way to load Career/Icebox vehicles in Free Roam. This is desired but NOT implemented/source-verified. First design should be read-only/copy-based and must not silently write to Career or create duplicate authoritative records.

5. **Map + minimap icons.** Both RedFox Tow Yards and Icebox must eventually show on the BeamNG main map and minimap using native/current BeamNG/RLS POI/marker APIs after source verification. Tow Yard markers should use saved yard locations and names; Icebox marker should use the chosen/custom location.

6. **Cross-map Tow fleet shipping.** Final Tow behavior must allow company vehicles to move from Tow Yard to Tow Yard even across maps because stored vehicles are save-backed records. Initial implementation can be direct garage-to-garage reassignment. Later, transfers should route through a dedicated shipping/delivery location on the destination map for pickup.

7. **New-map workflow.** Intended future Tow flow: travel to a new map -> create/setup a new Tow Yard -> request the needed trucks/equipment from another Tow Yard -> vehicles are shipped/assigned to the new yard without loading the source map.

8. **Stock garage UX, not another RedFox imitation.** Icebox must prove the existing Career/RLS garage UI: consistent stock thumbnails, left-click/select/context behavior, multiple Favorites, Retrieve/Replace, Repair, Rename, plate, Paint, Parts/config/tuning, Put Away, sort/filter behavior where practical, save/reload.

9. **Tow-specific extras only after stock garage behavior works.** Once Icebox proves the native garage architecture, port it into JOB-09 and add only the missing Tow features: Move to Tow Yard, cross-map shipping, Tow business ownership/accounting, custody/impound, disposition, etc.

10. **No automatic migration.** Do not auto-move the existing Tow trucks/trailers. Test one expendable trailer/car first and preserve transactional safety.

11. **Tow money path is proven good.** Owner confirmed towing job revenue goes into the Tow business bank. Preserve this behavior.

12. **Known Tow v36 failures that motivated Icebox:** custom image sizing inconsistent; edit/move controls and dropdowns did not work; Search Vehicle did not work; company garage presentation was not the stock garage UX; custody counts/duplicate yard presentation also need cleanup when the proven garage architecture returns to Tow.

## Mandatory development process

Source-first/evidence-first:

1. inspect exact supplied source/archive;
2. verify APIs and behavior;
3. only then edit/build;
4. validate/diff/package;
5. report exact changes and runtime uncertainty.

Do not edit paid RLS source files without explicit owner permission. Do not silently migrate vehicles. Do not require the player to manually perform developer-style business linking in the final gameplay flow.

## Immediate next task for the next chat

Do **not** patch Tow first.

Continue with Icebox. Inspect the exact current BeamNG/RLS facility/garage/POI/map-marker code needed for:

- player-chosen Icebox anchor;
- safe optional custom `MAKE ICEBOX HERE` location;
- stock garage access at that chosen location;
- main-map/minimap marker registration;
- safe Free Roam read-only Career/Icebox vehicle spawning.

Then build the next standalone Icebox test version and test with one expendable vehicle before any Tow port.
