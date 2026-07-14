# JOB-05 — Standalone BeamBook Test Plan

**Date:** 2026-07-14  
**Owner:** David / Captain  
**Job:** JOB-05 — BeamBook Marketplace  
**Chat title:** 5 — JOB-05 — BeamBook Marketplace  
**Status:** OWNER-AUTHORIZED STANDALONE TEST IN PROGRESS — RUNTIME UNTESTED

## Owner authorization

David explicitly authorized JOB-05 to build a temporary standalone BeamBook test package before shared IceFox phone/PC integration is available.

The temporary entry will be key-opened and will include a WEUI / World Editor-style native settings surface. This owner authorization is limited to one isolated JOB-05 test mod. It does not authorize edits to shared IceFox, phone, PC, registry, bridge, Career/RLS, App Store, or another job's files.

The product name is **IceFox**, not IceFlux.

## Visual direction

The current BeamBook page inside the uploaded IceFox ecosystem is a placeholder and is not the visual target.

The new page will use the uploaded screenshots as the primary visual reference:

- dark community/group wall cards;
- group name plus author, time, audience, contributor and author badges;
- large single-photo posts;
- tiled multi-photo galleries;
- reactions, comment counts and shares;
- a “Most relevant” comment header;
- nested comment rails and reply chains;
- realistic short comments, disagreements and odd local personalities;
- a full Marketplace listing viewer with large gallery, vehicle facts and seller contact/action area;
- distinct BeamBook/RF branding without copying Facebook's logo.

Screenshot sequence:

1. Marketplace concept post and full listing viewer.
2. Continuation of first comment thread.
3. Continuation of first comment thread.
4. Regular truck post.
5. Truck post comments and nested argument.
6. Multi-photo build gallery.
7. Crash post and tiled gallery.
8. Crash post continuation and comments.
9. Cargo/road incident post.

## Inspected inputs

| Input | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `beamBook.zip` | 9,867 | `2b8ac94018b9ca2c0c04bba597ad4316e177c9a4fd666b408392ad6d5becccc9` | Private-seller behavior reference only |
| `FoxFax_DROP_IN_FULL_PAGE_v1_1_DARK_LIGHT.zip` | 7,474,088 | `19e2bc379971e0583f70d5ceff85926b425cd12f1ded914b375f1e76126d334b` | Responsive dark/light shell reference only; no FoxFax edits |
| `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX(1).zip` | 24,510,848 | `4dac614a4b14d423c069dccc8bdb5e0e511ee208f7414d3e6ed50a86a7903597` | Current IceFox behavioral/route reference; not a modular source base |
| `beambook_buyable_rules_v0_1_1.txt` | 739 | `e7653d119e30119555453c410fba7561dd0675642f313700b011722b4680d704` | Purchase display rules |
| `beambook_content_notes_v0_1_0.txt` | 875 | `86ab01457bbf48ec926f8f6388f1fc460a3229356ff48b527a9d0d403a780e94` | Content rules |
| `beambook_posts_starter_pack_v0_1_0.json` | 155,995 | `0fd05beac1143dcbe012ea9ba23a4723c9e9676724eaf4241f4de2e114990d96` | Historical content reference |
| `beambook_posts_starter_pack_v0_1_1_buyable_flags.json` | 190,243 | `190e4db11285983dbc0ec316edef41f76e4d58037e2f8cd6db1b30f985593b6b` | Active feed source |

All three ZIPs passed archive integrity checks.

## Baseline findings

The supplied third-party BeamBook mod has useful behavior:

- creates private-seller listings from eligible current game vehicles;
- uses current-map parking spots;
- lets the player travel to and inspect a vehicle before purchase;
- persists listing data in the career save;
- delegates final inspection/purchase to the game's private-seller flow.

Unsafe behavior that will not be copied as-is:

- auto-loads a Career module at game/session startup;
- patches `career_modules_vehicleShopping.getShoppingData()` at extension load;
- patches inspection behavior globally;
- contains a West Coast-specific preview image path.

The standalone adapter must lazy-load only when the BeamBook UI is opened. It may request or patch nothing at startup. All-map behavior remains runtime-unproven until David tests West Coast and a non-West-Coast map.

The active v0.1.1 content pack contains:

- 192 unique posts;
- 42 named authors before procedural profile expansion;
- 90 Marketplace-category posts;
- 85 entries with both `buyable == true` and `purchaseEnabled == true`;
- vehicle, prop and joke listing types;
- ten map/location labels.

The site will choose a randomized session subset and progressively load more rather than render all 192 posts at once. A procedural profile pool will provide at least 200 possible names/avatar identities while preserving supplied named characters.

## Standalone test scope

Planned isolated mod paths:

```text
lua/ge/extensions/redfox/beamBookStandalone.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookStandalone.json
ui/modules/apps/RedFoxBeamBook/app.json
ui/modules/apps/RedFoxBeamBook/app.js
ui/modules/apps/RedFoxBeamBook/app.html
ui/modules/apps/RedFoxBeamBook/app.css
ui/modules/apps/RedFoxBeamBook/app.png
ui/modules/apps/RedFoxBeamBook/site/index.html
ui/modules/apps/RedFoxBeamBook/site/assets/css/beambook.css
ui/modules/apps/RedFoxBeamBook/site/assets/js/beambook.js
ui/modules/apps/RedFoxBeamBook/site/assets/data/beambook_posts.json
ui/modules/apps/RedFoxBeamBook/site/assets/icons/*
mod_info/*
JOB-05 verification/report files
```

Exact paths may be narrowed after implementation inspection, but no shared path may be added.

Functional target:

- a standalone BeamBook UI app;
- configurable temporary keyboard action;
- native WEUI / World Editor-style settings window;
- wall, marketplace, saved listings and selling views;
- category filters for cars, trucks, buses, trailers, props and other;
- price, distance and sorting controls;
- full listing viewer modeled on screenshot 1;
- random feed/session selection from the 192-post pack plus at least 200 possible procedural profiles;
- real private-seller vehicle listings when Career/RLS data is available;
- travel/inspect/purchase delegation to the game flow;
- clear nonfunctional state for unmapped props instead of fake purchase completion;
- explicit error state if the current map supplies no usable parking spots.

## Protected paths

The ZIP must not contain or edit:

```text
ui/ui-vue/dist/index.js
ui/modModules/redfoxCareerWeb/
assets/js/icefox_front.js
lua/ge/extensions/redfoxCareerWeb.lua
lua/ge/extensions/ui/phone/
shared phone shell
shared PC shell
shared IceFox registry/router
shared JOB-02 bridge
BeamNG/RLS original Career modules
career_modules_vehicleShopping source
career_modules_inventory source
FoxFax files
Scrap Yard files
Import/Export files
Classics files
SponsorHub/FoxMail/FoxText files
```

No startup Career module, no startup marketplace patch, no custom money, no fake ownership, no fake storage/garage, and no “spawn equals purchase success.”

## GitHub reference-asset policy

David requested that the screenshots and shared JOB-05 inputs remain accessible to all chats.

Planned repository folder:

```text
PROJECT_ASSETS/JOB-05_BEAMBOOK/
  README.md
  SCREENSHOTS/
  CONTENT/
  BASELINE_MANIFESTS/
```

The nine screenshots and the small TXT/JSON packs will be committed there. Large/user-owned baseline ZIPs will be recorded by exact size, hash and inventory; storing large binaries directly will be evaluated against repository health. The third-party `beamBook.zip` archive will not be publicly redistributed unless David confirms redistribution permission; its hash and complete file inventory will be published so every chat can identify the inspected baseline.

GitHub currently warns above 50 MiB, blocks regular repository files above 100 MiB, and browser uploads are limited to 25 MiB per file. This JOB-05 input set is individually below those hard limits, but binary duplication still increases clone size.

## Verification plan

1. Validate every JSON file.
2. Parse HTML and scan local asset references.
3. Syntax-check JavaScript and statically inspect Lua/action JSON.
4. Test responsive layouts at phone and PC viewport sizes.
5. Verify the feed chooses a randomized subset and “load more” works.
6. Verify Marketplace filters and sort combinations.
7. Verify both `buyable` and `purchaseEnabled` are required.
8. Verify unmapped prop and joke entries cannot invoke a purchase.
9. Scan for protected paths, startup loaders, global startup patches, custom money/storage/garage/ownership logic and duplicate shared IceFox files.
10. Verify ZIP integrity, single mod root, no `__pycache__`, and exact file inventory.
11. Include required TXT, HTML, JSON, CSV, tree and logging reports.
12. Label the package **BUILT — RUNTIME UNTESTED** until David tests the exact ZIP in BeamNG.
13. Runtime test West Coast plus one non-West-Coast map, key opening, WEUI settings, listing generation, parking destination, travel, inspection, purchase completion, real ownership and storage.

## Known risk / honest status

Static checks cannot prove that a custom BeamNG key action can surface a UI app on David's exact UI version or that the supplied private-seller flow is compatible with his exact RLS version. If the UI app must be added to a layout once before the key can toggle it, the report will say so. No runtime-success claim will be made before David's test.
