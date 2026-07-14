# JOB-05 standalone BeamBook — build checkpoint

**Date:** 2026-07-14  
**Status:** BUILT SOURCE CHECKPOINT — RUNTIME UNTESTED  
**Job:** JOB-05 — BeamBook Marketplace  
**IceFox integration:** Not included; shared integration remains blocked pending contracts.

## Implemented isolated source

```text
lua/ge/extensions/redfox/beamBookStandalone.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookStandalone.json
ui/modules/apps/RedFoxBeamBook/app.json
ui/modules/apps/RedFoxBeamBook/app.js
ui/modules/apps/RedFoxBeamBook/app.html
ui/modules/apps/RedFoxBeamBook/app.css
ui/modules/apps/RedFoxBeamBook/app.svg
ui/modules/apps/RedFoxBeamBook/app.png
ui/modules/apps/RedFoxBeamBook/site/index.html
ui/modules/apps/RedFoxBeamBook/site/assets/css/beambook.css
ui/modules/apps/RedFoxBeamBook/site/assets/js/beambook.js
ui/modules/apps/RedFoxBeamBook/site/assets/data/beambook_posts.json
```

No shared IceFox, phone, PC, router, registry, bridge, RLS core, FoxFax, or other job file is included.

## Website checkpoint

Implemented:

- dark/light Facebook-style community wall using distinct BeamBook/RF branding;
- group cover, author/time/audience metadata and contributor badges;
- reactions, comment counts, shares and “Most relevant”;
- nested comment rails, mentions and author labels;
- large single-image and tiled-gallery post layouts;
- 192-post source pack;
- randomized 100-post session pool with 16 initially rendered and 10-at-a-time load-more;
- 240 procedural profile identities;
- right-side contacts/group chats/sponsored blocks;
- top-left RF storefront/Marketplace control;
- Marketplace categories for cars, trucks, buses, trailers, vans, props and other;
- search, price, distance and sorting filters;
- 90 catalog entries derived from the supplied content pack;
- full photo/details/seller listing viewer;
- explicit non-purchase state for props/catalog posts without a game item mapping;
- responsive phone and PC layouts.

## Standalone runtime adapter checkpoint

Implemented:

- unique `redfox_beamBookStandalone` extension;
- unique bindable `RedFox: Toggle BeamBook` input action;
- UI app container that loads the website;
- native WEUI / World Editor-style settings window;
- current-map parking-spot selection;
- eligible-vehicle generation only when the site explicitly requests Marketplace data;
- direct selected-listing handoff to stock `career_modules_inspectVehicle.startInspection`;
- optional quick-travel inspection;
- explicit error if Career/RLS, generator, inspection service, eligible vehicles or current-map parking are unavailable;
- `[RedFox][BEAMBOOK]` logging.

Not implemented:

- no startup Career module;
- no `modScript.lua` startup loader;
- no global `getShoppingData` replacement;
- no global `startInspection` replacement;
- no custom money;
- no fake ownership, storage or garage;
- no spawn-as-purchase-success;
- no shared IceFox phone/PC registration.

## Static/render evidence

Headless Chromium render matrix:

| View | Viewport | JS/page errors | Horizontal overflow | Evidence |
|---|---:|---:|---:|---|
| Wall | 1440×1000 | 0 | 0 px | 16 rendered posts; 192 source posts; 240 profiles |
| Marketplace | 1440×1000 | 0 | 0 px | 90 filterable catalog listings |
| Listing viewer | 1440×1000 | 0 | 0 px | full modal/gallery/details rendered |
| Wall | 390×844 | 0 | 0 px | phone layout rendered |
| Marketplace | 390×844 | 0 | 0 px | phone storefront rendered |

Additional checks:

- JavaScript syntax: PASS
- JSON parse: PASS
- Lua 5.1 grammar parse: PASS
- supplied content pack: 192 unique post IDs
- source status: BUILT — RUNTIME UNTESTED

Static renders prove layout only. They do not prove BeamNG app discovery, input action discovery, WEUI behavior, current-map spawning/inspection, purchase completion, real ownership or storage.

## Runtime test dependency

David must test the exact final ZIP in an active Career/RLS session. The original third-party `beamBook.zip` should be disabled for this test because it auto-loads and globally patches Career shopping.

The UI app may need to be added to a UI layout once before the key action can toggle it. That is explicitly runtime-unproven.
