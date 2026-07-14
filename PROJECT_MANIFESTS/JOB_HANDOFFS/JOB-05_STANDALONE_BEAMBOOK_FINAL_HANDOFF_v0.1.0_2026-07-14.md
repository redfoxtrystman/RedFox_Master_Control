# JOB-05 final standalone test handoff

**Date:** 2026-07-14  
**Job:** JOB-05 — BeamBook Marketplace  
**Status:** BUILT — RUNTIME UNTESTED  
**Owner:** David / Captain  
**Product spelling:** IceFox

## Exact candidate

```text
5-RedFox_BeamBook_Standalone_v0_1_0_RUNTIME_UNTESTED.zip
```

- Size: **5,098,718 bytes**
- SHA-256: `f33b06ffb10246b596646e2e5a6a580a4bddce00410c3f7231501d2f25152349`
- Packaged files: **28**
- ZIP integrity: **PASS**
- Extracted inventory/hash comparison: **PASS**
- Duplicate archive entries: **0**
- Content posts / unique IDs: **192 / 192**
- Buyable plus purchase-enabled entries: **85**
- Static render status: **PASS**
- BeamNG/RLS runtime: **UNTESTED**

GitHub candidate path:

`PROJECT_RELEASE_CANDIDATES/JOB-05/5-RedFox_BeamBook_Standalone_v0_1_0_RUNTIME_UNTESTED.zip`

## What this candidate provides

- standalone BeamBook UI app;
- bindable `RedFox: Toggle BeamBook` input action;
- WEUI / World Editor-style settings;
- Facebook-like dark/light BeamBook group wall using distinct RF branding;
- randomized 100-post session choice from 192 supplied posts;
- 240 procedural profile identities;
- reactions, contributor/author badges, nested replies and tiled galleries;
- top-left RF Marketplace control;
- cars, trucks, buses, trailers, vans, props and other filters;
- price, distance, search and sorting controls;
- full listing viewer;
- explicit current-map private-seller inspection handoff;
- clear no-purchase state for unmapped props/catalog posts;
- required TXT, HTML, JSON, CSV, tree, logging, scope and provenance reports;
- PC/phone static preview evidence.

## Safety boundary

The ZIP contains none of the shared/protected IceFox paths and does not contain the third-party archive.

It has:

- no startup Career module;
- no `modScript.lua` loader;
- no global `vehicleShopping.getShoppingData` replacement;
- no global `inspectVehicle.startInspection` replacement;
- no custom money;
- no fake ownership, storage, garage or inventory;
- no shared phone/PC/router/registry/bridge files;
- no FoxFax or other job code.

Marketplace vehicle generation runs only after an explicit website or WEUI request. A selected listing is staged only for a direct stock private-seller inspection request.

## Required installation/test order

1. Disable/remove the original third-party `beamBook.zip` for this test.
2. Install only the exact JOB-05 candidate ZIP.
3. Start an active Career/RLS session.
4. Open Esc → UI Apps → Add App.
5. Add **RedFox BeamBook Standalone** once.
6. Open Controls and bind **RedFox: Toggle BeamBook** to an unused key. Suggested: Shift+B if free.
7. Press Settings; if the native WEUI window is not visible, enter World Editor with F11 and press Settings again.
8. Test West Coast USA.
9. Test at least one non-West-Coast map.
10. Verify route/inspection and complete a normal purchase.
11. Confirm real money, ownership, inventory/storage.
12. Return the `[RedFox][BEAMBOOK]` log section.

## Honest runtime limits

Static checks do not prove UI app discovery, input action discovery, key toggling, WEUI behavior, RLS compatibility, current-map parking, stock inspection, purchase completion, ownership or storage.

The UI app may need to be added to a layout once before its key action can toggle it. If that occurs, report it as the exact checkpoint result.

Do not change the status to working/fixed/done until David tests this exact SHA-256 candidate.

## Shared integration

This standalone owner-authorized test does not modify or complete shared IceFox phone/PC integration. JOB-01/JOB-02/JOB-11 contracts remain required before the isolated page becomes the canonical same-destination IceFox app.
