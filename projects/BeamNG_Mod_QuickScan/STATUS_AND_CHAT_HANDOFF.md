# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.2 Version-Only Rename + Contrast + Images  
**Latest release record:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_2_VERSION_CONTRAST_IMAGES.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_2/README_AND_VERIFICATION.md`  
**Career contract:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/CAREER_EXPORT_FORMAT.md`  
**DRM rules:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/DRM_DETECTION_NOTES.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_0_CATALOG_CAREER_DRM.md`
5. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_1_ORIGINAL_NAME_PREVIEW_FIX.md`
6. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_2_VERSION_CONTRAST_IMAGES.md`
7. This file.

## Current truth

- v0.4.0 ran on David's Windows computer and exposed short-name, preview, and contrast failures.
- v0.4.1 restored the controlling original-name law and missing-preview cache recovery.
- David then uploaded the exact `BEAM_EVO_Mods_Acura_Integra.zip` and screenshots from the Catalog UI.
- The uploaded Integra archive contains no declared mod version. QuickScan must not invent one.
- v0.4.2 adds a `Set / Correct Version` action saved by exact ZIP SHA-256.
- Manual version changes invalidate stale cache and rebuild naming/image records.
- The normal Catalog has horizontal and vertical scrollbars.
- `Open Full-Screen List` opens a maximized Catalog view.
- Dropdown/read-only field colors are explicitly styled instead of trusting Windows' white native field.
- Text modes are Automatic, Light text, and Dark text.
- Image exports can go beside the ZIP, to QuickScan's catalog folder, or both.
- Vehicle previews, map previews, and UI app icons are classified separately.
- v0.4.2 passed compile, built-in self-test, exact uploaded Integra regression, GUI contrast/full-screen smoke tests, ZIP reopen/CRC, packaged compile, packaged self-test, and packaged GUI smoke.
- Large-library Windows runtime and physical DPI behavior remain David tests.

## Hashes

```text
v0.4.1 source
29548be3cbea233f65439103bd4a25ac0b1dc8bb138fff2fd45ef2cd4ac1adc0

v0.4.2 source
5a490166433dd98912796ad9a0036c81892a891e73c83bf06c680fb44715bf05

v0.4.2 package
2ec328f5acec134d141b66223d17da3507127b423dd0d007ec056e5e9de555e6

Uploaded Integra ZIP
a9cdade74adb53a7c60cad58c1865aeb1e3e5e5513dfd6cb42a6cbdf374a9b29
```

## Controlling rename law

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD A MISSING VERSION OR UPDATE AN EXISTING VERSION TOKEN.
DO NOT REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
IF NO VERSION IS FOUND, DO NOT RENAME UNTIL THE USER SUPPLIES THE REAL VERSION.
```

Exact uploaded Integra behavior:

```text
No version override:
BEAM_EVO_Mods_Acura_Integra.zip
BEAM_EVO_Mods_Acura_Integra.png

Manual version 1.2:
BEAM_EVO_Mods_Acura_Integra_v1.2.zip
BEAM_EVO_Mods_Acura_Integra_v1.2.png
```

## Preview law

- vehicle: repository/info image, then vehicle default/config preview;
- map: preview/loading/overview/screenshot/cover/thumbnail in the level folder;
- UI app: icon/logo used by the in-game app;
- up to three useful unique images, except normally one UI icon;
- random materials, texture channels, terrain/minimap tiles, engine instructions, and part images are filtered out;
- every record stores role, internal source path, reason, hash, catalog path, and sidecar path;
- ZIP contents are never modified.

## What David should test

1. Extract the new package into its own folder.
2. Confirm the title says `v0.4.2`.
3. Set Image export to `Beside ZIP + Catalog`.
4. Select the Integra row and press `Set / Correct Version`.
5. Enter the real version.
6. Confirm only the version is added to the full original filename.
7. Press `Export Selected Images`.
8. Confirm the image appears beside the ZIP and under QuickScan's preview folder.
9. Open the full-screen Catalog and confirm scrolling.
10. Test Automatic, Light text, and Dark text on the dropdowns.
11. Apply only one selected version rename after reviewing it.

## Current handoff

```text
Project: BeamNG Mod QuickScan / Catalog Manager
Version: v0.4.2 Version-Only Rename + Contrast + Images
Baseline inspected: exact v0.4.1 source
Before-edit checks: baseline hash and compile recorded
After-edit checks: compile, built-in self-test, map/UI/vehicle preview tests, manual-version cache test, exact Integra regression, GUI contrast/full-screen smoke PASS
Packaged ZIP reopened: PASS
Packaged source compile: PASS
Packaged self-test: PASS
Packaged GUI smoke: PASS
Windows runtime by David: REQUIRED
Known limitation: real Integra version is not declared in the archive and must be entered manually
Release commit: 26a69b258c1c4d0e2820734388c500e8e5ea989b
Verification commit: b644900787dcf7f90340206feb19d9cf46772413
Next safe step: David tests v0.4.2 on the copied Integra folder
```