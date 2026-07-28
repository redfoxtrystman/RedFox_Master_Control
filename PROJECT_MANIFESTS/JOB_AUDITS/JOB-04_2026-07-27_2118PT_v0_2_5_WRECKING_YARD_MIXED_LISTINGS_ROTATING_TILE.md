# JOB-04 — v0.2.5 RedFox Wrecking Yard Mixed Listings / Rotating Tile

**Date/time:** 2026-07-27 2118 PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Assistant:** Sol / ChatGPT  
**Runtime status:** UNPROVEN until David tests this exact ZIP in BeamNG

## Source

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1(1).zip
SHA-256: 83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
```

Known source runtime result:

```text
- IceFox welcome/browser opened without the previous lag.
- v0.2.4 opened Joe's Junk as a visible native storefront.
- David corrected the architecture: Joe's Junk must be a hidden stock source, while RedFox Wrecking Yard remains the visible page.
```

## Output

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-27_2118PT_v0_2_5_MIXED_RLS_LISTINGS_ROTATING_TILE_FROM_v0_2_4.zip
SHA-256: 291776b0d5affaa21c9376cdc8275e2757154457ee8cf07b5d2e4626e7774922
Size: 25,230,817 bytes
ZIP entries: 951
```

## Owner request implemented

```text
- Keep the no-lag welcome page.
- Rename the visible site/link to Wrecking Yard.
- Do not open Joe's Junk storefront.
- Render real RLS/career vehicle listings inside the RedFox Wrecking Yard page.
- Keep Joe's Junk as the primary hidden source.
- Include other real career sources when present, especially Slop Gear.
- Make inventory-source percentages adjustable.
- Keep tow trucks, work trucks, heavies, trailers and oddballs eligible.
- Rotate the welcome-page Wrecking Yard image each browser load without a vehicleShopping request.
- Enforce a 10-second total listing-load ceiling with no retry storm.
- Keep selling/scrapping deferred to the next patch.
```

## Adjustable default mix

File:

```text
sites/scrap_yard/assets/config/wrecking_yard_mix.json
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json
```

Defaults:

```text
80% Joe's Junk / normal yard salvage
10% other real sources, including Slop Gear/private/auction/used when present
5% potentially good vehicles with issues
5% work/heavy/trailer/special/oddball vehicles
12 visible listings per load
10,000 ms total load ceiling
```

The percentages and listing count can be changed in the JSON without rewriting the selection code.

## Source-mod findings used

```text
rls_slop_gear_garage_v0.2(1).zip
- dealership id confirmed: slopGearDealership
- its project/work/oddball configs remain eligible when RLS exposes them in vehiclesInShop

backAlley.0.2.2-alpha(1).zip
- manual spawn/inventory purchase logic was not copied

barnfindgenerator(2).zip
- no damage mutation code copied; reserved for later condition/damage work

rls_RaceTab_Release.zip
- no RaceTab files copied; installed special configs may appear only if the career market exposes them
```

## Changed files

```text
info.json
assets/js/icefox_front.js
sites/scrap_yard/index.html
sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/assets/css/scrap.css
sites/scrap_yard/assets/config/wrecking_yard_mix.json
ui/ui-vue/dist/index.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json
```

Readable verification reports were added under:

```text
docs/job04_v025_wrecking_yard_mixed_listings/
ui/modModules/redfoxCareerWeb/docs/job04_v025_wrecking_yard_mixed_listings/
```

## Functional changes

### Welcome page

```text
- Visible tile renamed from Scrap Yard to Wrecking Yard.
- Tile image is selected locally on every home-page render.
- Before real stock has ever loaded, it rotates among bundled lightweight junk/work-vehicle SVGs.
- After Wrecking Yard stock loads, real preview paths are cached and used for later welcome-page rotations.
- Welcome-page rendering makes no shop-data request.
```

### Wrecking Yard page

```text
- Automatically makes one explicit RedFoxRequestCareerData request after the Wrecking Yard page opens.
- Requests current getShoppingData without opening a dealership.
- If current stock is empty, performs at most one forced stock generation within the same 10-second total deadline.
- Does not poll and does not run timed retry chains.
- Selects an adjustable mixed list from real vehiclesInShop data.
- Joe's Junk remains hidden behind the Wrecking Yard intake label.
- Slop Gear is recognized by slopGearDealership when installed/exposed.
- Tow, wrecker, rollback, flatbed, D-Series, T-Series, truck, semi, trailer and other work/special keywords remain eligible.
- Vehicle images use real RLS preview paths first and lightweight bundled fallbacks on image failure.
```

### Purchase

```text
- Each Buy/Open Native Purchase button sends the exact shopId.
- The existing native path remains:
  career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)
- No manual money subtraction was added.
- No manual vehicle spawn was added.
- No manual inventory/storage insertion was added.
```

### Phone bridge

`ui/ui-vue/dist/index.js` received one limited existing-bridge change:

```text
- rfSendCareerData now accepts the explicit request flags.
- getShoppingData is called only when includeShopData=true.
- updateVehicleList(true) is called only when forceShopRefresh=true.
- No automatic welcome-page shopping call was restored.
```

This shared bridge edit is limited but remains a core-UI integration risk and must be validated by a full BeamNG restart.

## Static verification

```text
Mirrored Scrap Yard JS identical: PASS
Mirrored Scrap Yard CSS identical: PASS
Mirrored Scrap Yard HTML identical: PASS
Mirrored mix config identical: PASS
No active Open Joe's Junk button/page action: PASS
Visible Wrecking Yard naming present: PASS
Welcome home page contains no shop request: PASS
Rotating tile cache/fallback logic present: PASS
One explicit page-open listing request present: PASS
10-second total deadline present: PASS
Adjustable 80/10/5/5 config present: PASS
Slop Gear dealership ID support present: PASS
Tow/wrecker/rollback/flatbed keywords present: PASS
Native purchase message path present: PASS
Explicit phone shop-data bridge present: PASS
No setInterval/polling in Wrecking Yard JS: PASS
No manual money/spawn/inventory insertion code: PASS
All changed JavaScript syntax checks: PASS
Changed HTML local references: PASS
ZIP integrity/testzip: PASS
```

JavaScript syntax checked:

```text
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/ui-vue/dist/index.js
```

## Protected / not implemented

```text
RLS Lua originals unchanged
money logic unchanged
inventory/storage logic unchanged
vehicle delivery logic unchanged
selling/scrapping not implemented
parts stripping not implemented
Barn Find damage mutation not implemented
Back Alley purchase code not copied
RaceTab content not copied
other websites unchanged
```

## Required runtime test

Install only the current RLS setup and this exact JOB-04 ZIP. Disable older JOB-04/FoxNet versions.

```text
1. Fully restart BeamNG. Do not rely only on Ctrl+L because ui/ui-vue/dist/index.js changed.
2. Open Career and IceFox.
3. Confirm the welcome page remains fast.
4. Confirm the tile says Wrecking Yard and displays a vehicle image.
5. Return/reload the IceFox home page and confirm the tile image can change.
6. Open Wrecking Yard and time it from click to usable vehicle buttons.
7. PASS target: listings usable within 10 seconds.
8. Confirm Joe's Junk storefront never opens.
9. Confirm real vehicle cards appear inside RedFox Wrecking Yard.
10. Look specifically for tow/work trucks and Slop Gear entries when available.
11. Open one vehicle's native purchase screen.
12. Buy one inexpensive vehicle and verify money, delivery, ownership, inventory and storage are handled by RLS.
```

## Pass/fail gate

```text
PASS:
- no welcome lag
- mixed real listings inside RedFox Wrecking Yard
- <=10-second load
- no Joe's Junk storefront
- native purchase menu and correct RLS completion

FAIL:
- grey/title UI failure
- welcome page starts loading shops
- Joe's Junk storefront opens
- no real cards
- load exceeds 10 seconds
- duplicate vehicle/manual spawn/storage failure
```

No v0.2.6 may be created until this exact v0.2.5 runtime result is logged in issue #30.