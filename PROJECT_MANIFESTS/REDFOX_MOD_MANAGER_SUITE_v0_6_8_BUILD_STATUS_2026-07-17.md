# RedFox Mod Manager Suite v0.6.8 Build Status

**Date:** 2026-07-17  
**Project:** `32-RedFox_Mod_Manager_Suite_`  
**Baseline used:** `32-RedFox_Mod_Manager_Suite_v0_6_6_Simplified_Workspaces(1).zip`  
**Separate preserved build:** `32-RedFox_Mod_Manager_Suite_v0_6_7_Master_Catalog_Foundation.zip` remains untested by David and was not used as the source baseline.  
**Runtime status:** UNTESTED by David at delivery.

## Scope

This build is a catalog/UI repair plus integrated Version & Duplicate Checker. It does not yet implement career metadata writing, online real-world matching, or ZIP patching.

## Implemented

- Fixed Career Shop Builder launcher error by importing `subprocess`.
- Responsive picture catalog grid that reflows to available window width.
- Thumbnail images remain contained inside their cards.
- Missing-source entries hidden by default and sorted last when shown.
- Added `Show missing files` control.
- Clicking an image candidate attempts to preview that exact image.
- Added GIF to preview candidates; existing PNG/JPEG/BMP/WEBP/TGA support retained.
- DDS preview remains dependent on available Pillow decoder support; Extract/View remains fallback.
- Selected catalog entry remains shared across Catalog, Editor, Textures/ZIP Tools, and Career pages.
- Generic `Status` label clarified as `RedFox Review Status`; it is not a BeamNG Career field.
- Added integrated Version & Duplicate Checker.
- Version detection checks metadata first, then likely info/manifest/readme/version files, then ZIP filename.
- Newest internal file date is recorded as fallback evidence only, not claimed as a release version.
- Exact duplicates grouped by ZIP-content fingerprint even when filenames differ.
- Likely version families grouped using internal vehicle/level identity.
- Suggested rename format preserves original base name and adds `_v<version>` before `.zip`.
- No rename occurs without explicit user approval.
- Rename history is saved in the catalog.

## Files changed

- `beamng_mod_manager.py`

## Files preserved unchanged

- `redfox_shop_scanner.py`
- `redfox_vehicle_workshop.py`
- all prior history/readme/verification files

## Checks performed

- Baseline archive extracted and inspected before editing.
- All three Python modules compile after editing.
- Limited GUI startup under Xvfb remained running until the test timeout; no startup traceback was produced.
- Version metadata detection unit test passed.
- Versioned filename unit test passed.
- Final ZIP reopened.
- ZIP integrity test passed.
- All three Python modules compiled again from the reopened final ZIP.
- Required v0.6.8 version/import/version-checker code was confirmed inside the reopened package.

## Not proven

- David's Windows runtime.
- BeamNG integration.
- Career compatibility writer.
- Online research/matching.
- Full support for every DDS/TGA variant.
- Correct behavior on every one of David's thousands of mods.

## Next required user test

1. Launch v0.6.8.
2. Confirm Career Shop Builder no longer reports `subprocess` undefined.
3. Resize Picture Home and confirm tile reflow/image containment.
4. Confirm missing-source items are hidden unless `Show missing files` is enabled.
5. Select a mod and switch between Catalog/Edit/Textures/Career; confirm selection persists.
6. Click image candidates and confirm readable images preview.
7. Open Version & Duplicate Checker and use Suggest Rename before testing a real rename.
