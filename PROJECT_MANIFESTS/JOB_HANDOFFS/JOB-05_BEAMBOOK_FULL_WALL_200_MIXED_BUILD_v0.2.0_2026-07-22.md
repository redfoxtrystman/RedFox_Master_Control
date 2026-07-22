# JOB-05 — BeamBook Full Wall + 200 Mixed Marketplace — v0.2.0

**Date:** 2026-07-22  
**Timestamp:** 2026-07-22 09:34 PDT  
**Owner:** David / Captain  
**Active chat:** JOB-05 — BeamBook Marketplace regular-chat takeover / Sol  
**Status:** BUILT — RUNTIME UNTESTED

## Owner request

David returned from the camping pause and asked JOB-05 to rebuild the missing full BeamBook using the original BeamBook behavior as research and the recovered JOB-10 Facebook-style BeamBook wall/pages as the visual source. The requested default was **200 vehicles with mixed types and mixed conditions like a real Facebook Marketplace**.

## Delivered test candidate

```text
RedFox_BeamBook_Full_Wall_200_Mixed_v0_2_0_RUNTIME_UNTESTED.zip
```

- Size: **15,512,650 bytes**
- SHA-256: `93eec881149c63c186205fed3a5e773db6492c45d53b1f9da52cd68955117078`
- Packaged files: **81**
- ZIP integrity: PASS
- Duplicate archive entries: 0
- BeamNG/RLS runtime: UNTESTED

The binary was delivered through the current regular chat. This GitHub record documents identity, scope and test requirements. The large binary was not committed through the text-only GitHub connector.

## Product included

- Standalone BeamNG UI App: `RedFox BeamBook Full Wall`.
- Facebook-style BeamBook wall/feed.
- Friends page.
- Groups page.
- Messages page contained inside BeamBook without replacing JOB-12 FoxMail/FoxText.
- Saved-listings page.
- RedFox Driver profile page.
- Selling/listing-management presentation.
- Marketplace search, category filtering, condition filtering and sorting.
- 60 generated social-wall posts.
- 200 fallback Marketplace vehicle listings that render without Career/RLS data.
- Manual request for up to 200 live eligible Career/RLS configurations.
- Live-listing inspection request through the stock private-seller inspection function.
- Key-opened WEUI generation settings.
- No fake money, ownership, inventory, storage, garage or purchase-success system.

## Exact default 200-vehicle mix

```text
Cars: 70
Pickups: 30
SUVs: 25
Vans: 15
Buses: 8
Heavy / semis: 18
Trailers: 14
Special / modified: 20
TOTAL: 200
```

## Exact default condition mix

```text
Excellent: 20
Good: 55
Average: 65
Worn: 40
Rough: 20
TOTAL: 200
```

Condition bands use separate mileage ranges. The live Career generator applies the same broad mix where matching eligible configurations exist; unavailable category quotas fall back to other eligible configurations so the request can still approach 200 listings.

## Primary implementation paths

```text
lua/ge/extensions/redfox/beamBookStandaloneV2.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookStandaloneV2.json
ui/modules/apps/RedFoxBeamBookV2/app.json
ui/modules/apps/RedFoxBeamBookV2/app.js
ui/modules/apps/RedFoxBeamBookV2/app.html
ui/modules/apps/RedFoxBeamBookV2/app.css
ui/modules/apps/RedFoxBeamBookV2/app.png
ui/modules/apps/RedFoxBeamBookV2/app.svg
ui/modules/apps/RedFoxBeamBookV2/site/index.html
ui/modules/apps/RedFoxBeamBookV2/site/assets/css/beambook.css
ui/modules/apps/RedFoxBeamBookV2/site/assets/js/beambook.js
ui/modules/apps/RedFoxBeamBookV2/site/assets/data/beambook_catalog_200.json
ui/modules/apps/RedFoxBeamBookV2/site/assets/data/beambook_posts.json
```

## Input actions

```text
RedFox: Toggle Full BeamBook
RedFox: BeamBook Generation Settings
```

The UI App must normally be added to the current UI layout once through `Esc -> UI Apps -> Add App` before the toggle action can show or hide that instance.

## Scrap Yard compatibility boundary

This build was explicitly designed not to contaminate JOB-04 testing.

Static comparison against the supplied current JOB-04 archive:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0(1).zip
```

Results:

- Direct archive-path overlap: **0**.
- No `sites/scrap_yard` paths.
- No `redfoxCareerWeb.lua` replacement.
- No shared IceFox/FoxNet phone, PC, browser, route or registry files.
- No startup Career module.
- No `modScript.lua`.
- No replacement or wrapper assignment to `career_modules_vehicleShopping.getShoppingData`.
- No replacement or wrapper assignment to `career_modules_inspectVehicle.startInspection`.
- No money, inventory, ownership, garage or storage implementation.

The only shared runtime service used is an explicit direct call to the stock Career inspection function after David clicks **Inspect in game** on a live BeamBook listing. Static isolation lowers conflict risk, but actual coexistence remains unproven until David tests both exact archives together.

## Static verification

- ZIP CRC/integrity: PASS.
- Duplicate ZIP paths: PASS, 0 duplicates.
- JSON parsing: PASS.
- JavaScript syntax through Node: PASS.
- Lua syntax through `texluac -p`: PASS.
- 200-listing exact count: PASS.
- Category distribution: PASS.
- Condition distribution: PASS.
- 60-post content count: PASS.
- Referenced listing/post image files: PASS.
- HTML element IDs used by JavaScript: PASS.
- JOB-04 archive path overlap: PASS, 0 overlaps.
- Protected/global-patch scan: PASS.

A Chromium headless screenshot attempt could not complete in the container because Chromium did not exit cleanly under the container DBus/headless environment. This is not counted as a render pass. BeamNG runtime/UI rendering remains untested.

## Required clean test order

1. Test the current Scrap Yard package by itself first.
2. Disable original `beamBook.zip` and every `beamBook_RedFoxResearch...zip` derivative.
3. Install only the exact v0.2.0 BeamBook candidate.
4. Start Freeroam or Career/RLS.
5. Add `RedFox BeamBook Full Wall` through UI Apps once.
6. Bind both RedFox BeamBook actions.
7. Verify the wall, friends, groups, messages, profile, saved and selling pages.
8. Verify the fallback Marketplace shows exactly 200 listings.
9. In an active Career/RLS save, press **Load 200 live Career vehicles**.
10. Record the live count and category/condition behavior.
11. Select a live listing and request stock inspection.
12. Complete a normal purchase and verify real money, ownership, inventory/storage and garage results.
13. Test West Coast USA and at least one second map.
14. Only after both standalone tests pass, enable this exact BeamBook ZIP alongside the exact JOB-04 Scrap Yard ZIP and repeat one purchase from each.
15. Return `beamng.log` lines containing `RedFoxBeamBook`, screenshots and the first failing checkpoint.

## Honest limitations

- Runtime remains untested.
- The fallback 200 listings are presentation data and are not purchasable vehicles.
- Only listings returned by the live Career generator can request in-game inspection.
- Live category mix depends on what `util_configListGenerator.getEligibleVehicles()` exposes from David's installed game/mod set.
- Live inspection may fail if the current map has no suitable private-sale parking spot or if RLS changed the expected stock inspection contract.
- Shared IceFox phone/PC integration remains blocked pending the approved JOB-01/JOB-02/JOB-11 contracts.

## Restart state

JOB-05 is active again after the camping pause. The next action is David's exact-candidate runtime test. Fix the first proven failure without reintroducing startup/global shopping patches or crossing into JOB-04/shared-system ownership.