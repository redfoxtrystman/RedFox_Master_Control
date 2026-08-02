# JOB-09 v0.4.7.0 Build Report

## Build

- File: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_7_0_FullTowCompanyWebsitePhotoAlbumWorkingDropdownsRuntimeSlim.zip`
- SHA-256: `44e85a1af3efbad9cf5159d0449a4c51a286ea05930394079dfcf910984cf6e8`
- Size: `3,063,227` bytes
- Archive members: 60
- Base: v0.4.6.0
- Status: **BUILT — STATIC CHECKS PASSED — RUNTIME UNPROVEN**

## Purpose

Replace the partial marketing page with a complete RedFox towing-company website while preserving the existing JOB-09 Company Portal and game bridge. The visual structure was inspired by a professional towing-company site, but all RedFox wording, history, navigation, images, and implementation are original to this mod.

## Public website

- Home
- About / fictional West Coast company history
- Eight service categories
- Fleet and truck-type explanations
- Locations and working location tabs
- Gallery/photo album with category filters and lightbox
- Reviews
- FAQ accordions
- News/blog cards
- Contact and live tow request buttons
- Fake merchandise shop and in-memory demo cart

## Dropdown correction

The Services, Fleet, and Locations dropdowns use explicit click-open state, visible overflow, pointer events, and a very high stacking layer. This is intended to stop BeamNG WebUI from drawing the menu invisibly behind hero photographs.

## Replaceable photos

The archive contains 41 labeled JPG placeholders in:

`ui/modules/apps/redfoxTowPortal/assets/images/site_photos/`

Replacing a placeholder with a screenshot using the same exact filename changes the website image without editing HTML or JavaScript. A full shot list and replacement guide is included in that folder and at archive root.

## Preserved game functions

The existing Company Portal, public tow request actions, dispatch bridge, scene manager, records, custody inventory, Career company assets, fleet, yards, invoices, garage selector, immediate native claim flow, and post-tow results dialog remain attached to the same app.

The internal `redfoxNativeLifecycleVersion` remains `0.4.6.0` intentionally because this build changes the website rather than the native vehicle lifecycle contract.

## Static verification

- ZIP integrity: PASS
- JavaScript syntax: PASS
- JSON parsing: PASS
- HTML parsing: PASS
- Duplicate HTML IDs: PASS
- Referenced photo existence: PASS
- Cache tokens updated to `0470`: PASS
- Dropdown front-layer CSS present: PASS
- Runtime: UNPROVEN
