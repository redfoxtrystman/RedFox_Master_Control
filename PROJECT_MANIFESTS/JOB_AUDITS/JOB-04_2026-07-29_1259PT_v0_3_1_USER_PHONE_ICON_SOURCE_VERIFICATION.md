# JOB-04 — v0.3.1 User Phone Icon Source Verification

**Date/time:** 2026-07-29 12:59 PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain

## Purpose

Verify the owner-updated v0.3.1 ZIP before adopting it as the new source of truth. The owner stated that only the phone/browser icon was changed and requested confirmation that no Wrecking Yard site files were altered.

## Compared archives

### Original delivered v0.3.1

- File: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_0848PT_v0_3_1_MULTI_SOURCE_CLEAN_UI_FROM_v0_3_0.zip`
- SHA-256: `1d75d10ab9c814197f5264d5a9df6042d0269e218d06c323717a724b6c7f4be4`
- Size: `25,465,240 bytes`
- Entries: `1,461`

### Owner-updated source

- File: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_v0_3_1_REDFOX_BROWSER_ICON_ONLY- new phone icon.zip`
- SHA-256: `eafbe5618f6e97a14e872d071528f9fd8f450586dc9f7ff28ba55063bda1f4b2`
- Size: `25,511,793 bytes`
- Entries: `1,461`

## Full archive comparison

- Added paths: `0`
- Removed paths: `0`
- Changed paths: `1`
- Unchanged paths: `1,460`
- Duplicate internal paths: `0`
- Unsafe paths: `0`
- ZIP integrity: `PASS`

## Only changed file

`ui/entrypoints/main/tiles/foxnet-browser.svg`

- Original file SHA-256: `60eed2821d511912ae727234b3761ac396a37fa8aaac1c89703c6fda35c36cc9`
- Updated file SHA-256: `7a835b81ab12dad2301aae4016c1c79ba8d5dab6818e66179b1bad0404056f08`
- Original size: `618 bytes`
- Updated size: `51,389 bytes`
- SVG XML parse: `PASS`
- SVG viewBox: `0 0 128 128`
- Script elements: `0`
- External URL/file references: `0`

## Wrecking Yard site verification

All Wrecking Yard site files are byte-for-byte identical to the original delivered v0.3.1 archive, including:

- Root `sites/scrap_yard/**`
- Mirrored `ui/modModules/redfoxCareerWeb/sites/scrap_yard/**`
- All Wrecking Yard HTML files
- All Wrecking Yard JavaScript files
- All Wrecking Yard CSS files
- All Wrecking Yard JSON/configuration files
- All Wrecking Yard images and fallback assets
- `info.json`
- Shared UI bundle checked in the comparison

A total of 80 directly relevant Wrecking Yard/core paths were explicitly re-hashed and all matched exactly.

## Decision

The owner-updated ZIP is accepted as the new v0.3.1 source of truth for future JOB-04 work.

No Wrecking Yard site behavior, pricing logic, source selection, cycling, purchase bridge, HTML, JavaScript, CSS, or configuration was changed. Only the RedFox browser/phone tile icon changed.

## New source-of-truth archive

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_v0_3_1_REDFOX_BROWSER_ICON_ONLY- new phone icon.zip`

SHA-256: `eafbe5618f6e97a14e872d071528f9fd8f450586dc9f7ff28ba55063bda1f4b2`
