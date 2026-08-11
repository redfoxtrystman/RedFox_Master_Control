# RedFox RLS Career Full Toolkit v1.0.8 — Photo Filter Fix

Date: 2026-08-10
Support lane: SUPPORT-02 — Career Node Grabber / Developer Mode Compatibility
Build: `RedFox_RLS_Career_Full_Toolkit_v1.0.8_Working_Photo_Filters_TEST.zip`
Base: v1.0.7 Photo Filters + Thumbnail Lock Test
Runtime status: UNTESTED

## User-reported failure in v1.0.7
The filter dropdown changed, but captured images did not visibly change. Screenshot evidence showed the selected preset (for example Cool) while the staged/current thumbnail remained visually unchanged.

## Root cause
v1.0.7 wrote to an obsolete/wrong PostFX preset namespace and did not call BeamNG's current PostFX apply function. The filter data therefore did not reach the live renderer used by the screenshot utility.

## v1.0.8 changes
- Uses `client/postFx`.
- Uses `$PostFXManager::Settings::HDR1::ColorCorrectionRamp2`.
- Uses `$PostFXManager::Settings::HDR1::enabledHSL`.
- Uses `$PostFXManager::Settings::HDR1::factorHSL`.
- Calls `settingsApplyFromPreset()` after selecting a RedFox filter.
- Saves the current live PostFX state before a temporary filter using `settingsApplyAll()` + `savePresetFile()`.
- Restores the previous PostFX state after capture with `loadPresetFile()` + `settingsApplyFromPreset()`.
- Adds Live Preview and Restore Game Look controls so the user can verify a filter visibly before capturing.
- Adds Black & White and Color Boost.
- Strengthens Vintage, High Contrast, Warm, and Cool presets.
- Retains exact-inventory-ID thumbnail locking from v1.0.7.
- Existing Insurance, XP, Dev Tools, Node Grabber, Teleport, Economy, and Garage code retained.

## Filters
- Current Game / Photo Mode
- Black & White
- Vintage
- High Contrast
- Warm
- Color Boost
- Cool

## Test sequence
1. Select Black & White.
2. Click `LIVE PREVIEW SELECTED FILTER`.
3. Confirm the live world visibly becomes monochrome.
4. Capture the current camera view.
5. Confirm staged image is monochrome.
6. Repeat using Color Boost and confirm visibly increased color saturation.
7. Test Vintage, High Contrast, Warm, and Cool.
8. Confirm original game/PostFX look returns after each capture.

If live preview does not visibly change the world, stop testing the saved image and report the Dev Manager status line.

## Artifact
SHA-256: `b8ebbca605d101597160428614f41235e9d7f0e2a278aa1273470127c846ce8b`

## Protected scope
No stock BeamNG or RLS files are replaced by this patch. The changes are within the RedFox toolkit package and its packaged RedFox PostFX ramp assets.
