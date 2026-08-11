# RedFox RLS Career Full Toolkit v1.0.7 — Photo Filters + Thumbnail Lock TEST

**Date:** 2026-08-10  
**Base:** v1.0.6 Insurance Repair Test  
**Runtime status:** UNTESTED  
**Artifact:** `RedFox_RLS_Career_Full_Toolkit_v1.0.7_Photo_Filters_Thumbnail_Lock_TEST.zip`  
**SHA-256:** `afa695d7e1ae3d9a5e57d19b7527d8a2cdada067552c9a90da852e6d54b99c6e`

## User-reported problems addressed

1. Vehicle Photo Manager captures were heavily overexposed compared with the live game camera.
2. RLS/BeamNG regenerates vehicle thumbnails after vehicle edits, overwriting the user's chosen custom image.
3. User requested simple photo filter choices in the Dev Toolkit.

## Changes

- Replaced the Photo Manager's custom `render_renderViews.takeScreenshot` capture path with `extensions.util_screenshotCreator.takeThumbnailScreenshot`, matching the screenshot utility used by the current RLS inventory thumbnail system.
- Preserved the user-positioned current camera position, rotation, and FOV.
- Added capture filter choices:
  - Current Game / Photo Mode
  - Neutral
  - Warm
  - Cool
  - Vintage
  - High Contrast
- Added RedFox 256x1 PNG color-correction ramps under `art/postfx/redfox/`.
- Added persistent thumbnail locking keyed to the exact Career inventory ID.
- Locked masters are stored under `settings/redfox/vehicle_photo_locks/<profile>/` rather than inside rotating Career autosaves.
- Added `onVehicleSaveFinished(currentSavePath)` handling. When RLS regenerates a thumbnail, RedFox first copies the generated file to `inventory_<ID>_last_generated.png`, then reapplies the locked master to `career/vehicles/<ID>.png`.
- Added controls for:
  - Apply + Lock Thumbnail
  - Lock Current Thumbnail
  - Update Locked Image
  - Restore Locked Image Now
  - Unlock Thumbnail
- Preserved the existing v1.0.6 Insurance Repair, XP, Economy, Vehicle, Node Grabber, Teleport, Garage, and Photo preview/apply systems.

## Static verification

- Source v1.0.6 archive integrity: PASS
- Old custom render-view capture removed from Photo Manager capture function: PASS
- Native thumbnail screenshot path present: PASS
- Filter assets packaged: PASS
- Thumbnail lock and post-save restore hook present: PASS
- Generated-thumbnail backup logic present: PASS
- Existing Insurance/Teleport/XP/Node Grabber code tokens retained: PASS
- Final ZIP integrity: PASS

## Required runtime test

1. Enable only v1.0.7 and keep v1.0.6 available for rollback.
2. Use `Current Game / Photo Mode` and capture a known vehicle.
3. Verify staged capture is no longer overexposed.
4. Apply + Lock the thumbnail.
5. Change a vehicle part/tuning option so RLS saves/regenerates its thumbnail.
6. Confirm RedFox restores the locked master after the vehicle save.
7. Save/reload Career and confirm the lock persists.
8. Test RedFox filter presets last.

## Known risk

Custom RedFox filter presets temporarily set BeamNG's Color Correction Ramp for the capture and then restore the BeamNG default ramp. Users with a custom active Photo Mode filter should use `Current Game / Photo Mode` if they want to preserve the current game's filter state.
