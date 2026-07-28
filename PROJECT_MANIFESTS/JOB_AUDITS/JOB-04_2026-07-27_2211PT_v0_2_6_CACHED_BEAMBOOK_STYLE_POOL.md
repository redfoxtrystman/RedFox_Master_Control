# JOB-04 — RedFox Wrecking Yard v0.2.6

## Status

- Build: **v0.2.6 — Cached BeamBook-style 100-car pool**
- Runtime: **UNPROVEN**
- Static verification: **PASS (32/32 checks)**
- ZIP integrity: **PASS**
- ZIP entries: **959**
- ZIP size: **25,215,057 bytes**
- ZIP SHA-256: `cb4b1b1424fa5c4fea2d44b4bb413ca03beb6e7a2b2ef0162e71609005d8b87a`

## Source and reference

- Base ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-27_2118PT_v0_2_5_MIXED_RLS_LISTINGS_ROTATING_TILE_FROM_v0_2_4.zip`
- Base SHA-256: `291776b0d5affaa21c9376cdc8275e2757154457ee8cf07b5d2e4626e7774922`
- BeamBook reference ZIP: `beamBook(2).zip`
- BeamBook reference SHA-256: `2b8ac94018b9ca2c0c04bba597ad4316e177c9a4fd666b408392ad6d5becccc9`

## v0.2.5 closure

v0.2.5 is **superseded without a full gameplay test**. Its full runtime test became redundant because the direct live-dealership listing source was intentionally replaced. The useful pieces of v0.2.5 were retained:

- no-lag welcome page
- RedFox Wrecking Yard name and page design
- rotating welcome-page vehicle image
- adjustable 80/10/5/5 mix
- 10-second page load ceiling
- native purchase handoff by exact `shopId`

## What changed in v0.2.6

1. Added a JOB-04-owned Lua inventory provider modeled on BeamBook's efficient use of `util_configListGenerator`.
2. The provider does **not** generate vehicles at career or browser startup.
3. The first explicit Wrecking Yard page request generates a cached pool of 100 real BeamNG-eligible vehicle configurations.
4. The pool can be configured from 10 to 200 vehicles in the BeamNG user folder at `redfoxWreckingYard/config.json`.
5. Generated entries are inserted into `career_modules_vehicleShopping.getVehiclesInShop()` with native `shopId` records so the existing purchase menu can handle them.
6. Cached entries are saved to `career/redfoxWreckingYardInventory.json` and reused.
7. Existing Joe's Junk, Slop Gear, BeamBook/private, auction, barn/back-alley-style listings are included when already available in the native shop list.
8. Provider-generated salvage fills the Wrecking Yard even if those other mods have not generated stock yet.
9. The Wrecking Yard page now displays 24 listings from the available pool while retaining lazy image loading.
10. Tow, wrecker, rollback, flatbed, truck, semi, trailer, bus, van, aircraft, boat, and other special candidates remain protected by a dedicated category and priority weighting.
11. Mileage display now prefers explicit miles and converts BeamNG's `Mileage` meters to miles.
12. The automatic empty-list force-refresh retry from v0.2.5 was removed.
13. One explicit Refresh Yard Inventory action still regenerates one pool.

## Changed payload files

- Added `OPEN_ME_FIRST_JOB-04_Wrecking-Yard_2026-07-27_2211PT_v0_2_6_CACHED_POOL.txt`
- Modified `info.json`
- Added `lua/ge/extensions/career/modules/redfoxWreckingYardInventory.lua`
- Added `lua/ge/extensions/redfoxWreckingYardInventoryLoader.lua`
- Added `scripts/redfoxWreckingYardInventory/modScript.lua`
- Modified `sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- Modified `sites/scrap_yard/assets/css/scrap.css`
- Modified `sites/scrap_yard/assets/js/scrap.js`
- Modified `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- Modified `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css`
- Modified `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js`

Embedded verification TXT/HTML/JSON/CSV files were also added after payload comparison.

## Protected files confirmed untouched

- `ui/ui-vue/dist/index.js`
- `ui/ui-vue/dist/index.css`
- `assets/js/icefox_front.js`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
- `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js`
- RLS original Lua
- BeamBook original Lua
- `lua/ge/extensions/redfox/career/scrapyardBridge.lua`
- selling, scrapping, stripping, money, storage, and delivery logic

## Static verification

Passed:

- all changed JavaScript syntax
- all Lua files parsed successfully through Lua 5.4 syntax loading
- mirrored Wrecking Yard JS/config pairs identical
- adjustable percentages total 100
- page display count 24
- 10,000 ms load ceiling retained
- automatic empty-list retry disabled
- provider default 100 and max 200 confirmed
- no generation in `onCareerActivated`
- explicit page-only provider entrypoint confirmed
- native shop-list synchronization confirmed
- career-save cache confirmed
- BeamBook source compatibility confirmed
- tow priority keywords confirmed
- direct Lua request and fallback bridge confirmed
- native purchase handoff confirmed
- changed files do not open Joe's Junk storefront
- selling logic untouched
- BeamBook code not bundled or replaced
- touched page local references resolved

## Required runtime test

1. Disable older JOB-04/FoxNet test ZIPs.
2. Keep BeamBook installed if desired; it remains independent for the BeamBook/Facebook marketplace.
3. Install exact v0.2.6 and fully restart BeamNG.
4. Open IceFox and confirm the welcome page remains fast.
5. Open RedFox Wrecking Yard and time the first load.
6. Listings must become usable within 10 seconds.
7. Joe's Junk storefront must not appear.
8. Status should report a cached provider pool and available listing count.
9. Confirm tow/work/special vehicles can appear.
10. Open one inexpensive vehicle's native purchase screen.
11. Buy it and verify money, delivery, ownership, inventory, and storage.
12. Leave and reopen the Wrecking Yard; cached listings should return faster without regeneration.
13. Use Refresh Yard Inventory once and confirm one intentional regeneration.

## Next step after pass

Implement whole-vehicle **Sell / Scrap** using native inventory ownership and value APIs. Do not begin stripping/parts storage until buying, delivery, and cached listing reuse pass runtime testing.
