# JOB-05 — BeamBook phone direct shop-data cross-mod test v0.3.0

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Jobs involved:** JOB-04 Scrap Yard + JOB-05 BeamBook Marketplace  
**Status:** BUILT — RUNTIME UNTESTED  
**Purpose:** Make the BeamBook website use the same owner-confirmed working phone data path as the Scrap Yard website, without creating a second custom bridge or changing the existing phone/Lua/purchase implementation.

## Exact test package

```text
zzzz_RedFox_FoxNet_JOB04_ScrapYard_JOB05_BeamBook_PHONE_LIVE_v0_3_0_RUNTIME_UNTESTED.zip
```

- Size: 55,352,940 bytes
- SHA-256: `460d332e3efe91642532201823d8993f47c97b6c20d8c8257bb649ad47c9bccc`
- ZIP files: 1,004
- ZIP integrity: PASS
- Duplicate archive entries: 0
- JavaScript parse: PASS
- JSON parse: PASS
- Missing BeamBook assets: 0
- Built-in BeamBook fallback listings: 200
- BeamBook wall posts: 60
- Runtime: UNTESTED

## Base package

The build is a replacement package based on the exact owner-uploaded Scrap Yard ecosystem that David confirmed had working phone website access:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0(1).zip
```

## Implementation decision

The existing phone implementation already routes the BeamBook site and forwards these working messages:

```text
RedFoxRequestCareerData
RedFoxCareerData
RedFoxScrapYardOpenPurchaseMenu
RedFoxScrapYardPurchaseMenuResult
```

The new BeamBook page listens to the same existing `RedFoxCareerData` payload used by the Scrap Yard phone page. It reads `shopData.vehiclesInShop`, normalizes up to 200 live listings, classifies ordinary and unusual vehicle types, and opens the existing stock RLS/BeamNG purchase window with the selected `shopId`.

No second data bridge was introduced.

## Exact changed roots

```text
sites/beambook/
ui/modModules/redfoxCareerWeb/sites/beambook/
info.json
README_OPEN_FIRST_JOB04_JOB05_BEAMBOOK_PHONE_v0_3_0.txt
VERIFY_JOB04_JOB05_BEAMBOOK_PHONE_v0_3_0.json
```

The two BeamBook folders are mirrors because the base FoxNet package contains both root and `ui/modModules` website trees.

## Exact protected systems left unchanged

The following owner-confirmed working files are byte-for-byte unchanged from the uploaded Scrap Yard base:

```text
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
SHA-256: 06f64630b5603a1a700ded4e65c84b1fc7ff19b8ef625215f34aeae33523c48d

lua/ge/extensions/redfoxCareerWeb.lua
SHA-256: 799b2929f873118e6ed739d41886e75e145f60fb6bec3d7b571ffc8007d7a9a3

ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
SHA-256: 75f87a4b9b207aee0d03237d6a0ede9858fb500363d363f738a75bd2a13debbe
```

No unexpected non-BeamBook base files changed.

## BeamBook behavior

The rebuilt BeamBook page provides:

- full social wall and pages;
- 60 wall posts;
- 200 realistic fallback listings available immediately;
- automatic live dealership-data request when the page loads;
- manual `Load live dealership vehicles` retry;
- live listing limit of 200 total across all categories;
- cars, pickups, SUVs, vans, buses, semis/heavy vehicles, trailers, side-by-sides/off-road vehicles, boats/watercraft, aircraft, and specialty vehicles;
- live dealership thumbnails, prices, mileage, seller/dealership and shop IDs when exposed by game data;
- stock purchase/inspection-window request using the exact existing phone handler;
- fallback display when live dealership data does not arrive;
- title/condition disclosures without claiming unsupported game title data.

## Installation rule

Only one FoxNet/Web Ecosystem ZIP may be enabled.

Disable the older JOB-04 Scrap Yard ecosystem ZIP and the separate BeamBook standalone v0.2.0/v0.2.1 ZIPs before installing this replacement package.

The separate `beamBook_RedFoxResearch` generator is optional and remains a separate compatibility test because it globally changes stock shopping data.

## Required runtime test

1. Start Career/RLS.
2. Open the IceFox/FoxNet phone browser.
3. Open BeamBook.
4. Confirm the wall renders.
5. Open Marketplace.
6. Confirm the fallback catalog reports 200 listings before live data arrives.
7. Confirm the page changes to `LIVE DEALERSHIP` listings after `RedFoxCareerData` arrives.
8. Confirm boats, aircraft, trailers, heavy trucks, or other unusual eligible types are classified and displayed where present.
9. Open one live listing.
10. Press `Open stock purchase / inspection`.
11. Confirm the stock RLS/BeamNG purchase window opens for the same listing.
12. Confirm Scrap Yard still opens and behaves exactly as in the base package.
13. Return screenshots and `beamng.log` lines containing `RedFox`, `BeamBook`, `Scrap`, or `vehicleShopping`.

## Honest limits

- Runtime is untested.
- This specifically targets the owner-confirmed working phone path.
- The PC browser path was not repaired or claimed working in this build.
- The built-in 200 listings are visual fallback data; only live dealership listings have a real `shopId` and can open the stock purchase window.
- Purchase completion, money deduction, ownership, storage and garage results remain stock-system responsibilities and must be verified in game.
