# JOB-09 v0.4.0 — Linked Tow Website / Company Portal Source Summary

## Runtime baseline

v0.4.0 preserves the v0.3.5 JOB-09 dispatch/recovery extension and adds one mod-owned BeamNG UI app:

`ui/modules/apps/redfoxTowPortal/`

The legacy WEUI remains available as a fallback and for older development controls.

## Public towing website

The public page includes working service links, Request Tow, Company Portal transitions, fleet/recovery/yard sections, local images, and Garage Hub theme response.

`Request In-Game Tow Recovery` sends `request_player_tow` to the Lua bridge. The bridge reads the current player vehicle and Career inventory ID, searches loaded BeamNG/RLS recovery modules for a compatible prompt function, logs the exact namespace/function/attempt, and sends a compatibility hook when no direct API is found. It does not directly move, sell, delete, damage, charge, or reassign the vehicle.

## Company Portal state/action contract

The portal receives one sanitized state built by `getWebPortalState()` and sends explicit JSON actions through `webPortalActionJson()`.

Pages:

- Operations Overview
- Dispatch Center
- Scene Builder
- Records & History
- Tow Yard Inventory
- Company Fleet
- Tow Yard Management
- Invoices
- Settings & Tools

## Scene Builder

The live roster exposes:

- scene object type, model/configuration, saveable/included/selected status;
- world X/Y/Z;
- yaw/heading, pitch, roll, quaternion-derived direction, and plan-view arrow;
- forward/back, left/right, and up/down movement;
- relative and exact rotation;
- include, exclude, delete, and Undo Last Edit;
- cone, warning-sign, barrier, flare, and debris placement;
- strict required-roster save/replay/delete;
- persistent scene event log.

The final static correction passes Euler values to BeamNG as roll, pitch, yaw.

## Global vehicle pools

Persistent category-specific shuffled pools now cover standard towing, abandoned calls, rollovers, saved-scene target rerolls, accident targets, compatible semi/trailer selection, and police support.

- Exact configuration recent window default: 120 calls.
- Same-model recent window default: 24 calls.
- Unseen models/configurations are preferred until the valid class pool is exhausted.
- Multi-target selection reserves configurations within the scene.
- Pool memory is saved with the Career profile.

## Image replacement system

The portal bundles five local JPG screenshot slots plus the UI Apps thumbnail. `IMAGE_REPLACEMENT_GUIDE.md` and `image_manifest.json` define exact paths, names, dimensions, aspect ratios, formats, and use locations so David can replace images without changing code.

## Preserved safety boundary

- Company Fleet home-yard assignment remains metadata only.
- Company garage movement remains locked.
- Custody Claim & Transfer remains locked.
- No stock BeamNG or RLS file is replaced.
- Runtime status remains unproven until David tests the packaged build.
