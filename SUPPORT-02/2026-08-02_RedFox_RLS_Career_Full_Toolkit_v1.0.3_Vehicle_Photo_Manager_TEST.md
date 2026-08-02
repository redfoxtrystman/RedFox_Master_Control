# RedFox RLS Career Full Toolkit v1.0.3 — Vehicle Photo Manager TEST

## Status

Built and statically verified. Runtime untested until David tests this exact ZIP in BeamNG.drive.

## Base

- Base artifact: `RedFox_RLS_Career_Full_Toolkit_v1.0.2_RLS_XP_TABS_TEST.zip`
- Base status reported by David: current solid working version

## Artifact

- Filename: `RedFox_RLS_Career_Full_Toolkit_v1.0.3_Vehicle_Photo_Manager_TEST.zip`
- SHA-256: `6e707186842f013d2301d5cee2d4975c78477903b1c6fad09d203805521544b1`

## Files intentionally changed

- `lua/ge/extensions/redfox/careerDevUnlocker.lua`
- `mod_info.json`
- `README.txt`
- `CHANGELOG.txt`
- Added `VERIFY_v1.0.3.json`

## Existing feature groups preserved

- Career development tools
- Economy controls
- Dynamic RLS XP controls
- Vehicle tools
- Integrated Node Grabber
- Force-add current vehicle to garage
- Garage Hub theme integration

## New proof feature

Added a PHOTOS tab with:

- Resolve current spawned vehicle to exact Career inventory ID
- Capture current BeamNG camera position, rotation, and field of view
- Use `render_renderViews.takeScreenshot`
- Stage capture before applying
- Display staged and active images in World Editor ImGui using `ImTextureHandler` and `Image`
- Apply image to `career/vehicles/<inventoryId>.png`
- Backup previous custom thumbnail
- Restore previous thumbnail
- Restore default configuration thumbnail
- Open photo-storage folder

## Safety limits

- Current spawned Career vehicle only
- No Auction files changed
- No Wrecking Yard files changed
- No automatic application after capture
- Capture failure leaves current thumbnail unchanged
- Apply uses a temporary file before replacing the active thumbnail

## Static verification completed

- Source ZIP integrity checked
- Required photo-manager functions found
- Existing major toolkit functions found after editing
- All JSON files parsed
- Final ZIP reopened
- Required code tokens rechecked inside packaged ZIP

## Runtime test required

1. Back up Career save.
2. Disable older Full Toolkit, standalone Cheat Tools, and standalone Grabber ZIPs.
3. Enable only v1.0.3.
4. Load Career with a low-value owned vehicle.
5. Open PHOTOS and select current vehicle.
6. Position camera with Photo Mode or Shift+C.
7. Capture current camera view.
8. Verify staged preview appears.
9. Apply staged photo.
10. Verify Career Garage displays it.
11. Save and reload Career.
12. Test Restore Previous and Restore Default.
13. Confirm vehicle data and inventory count are unchanged.

## Rollback

Remove v1.0.3 and restore v1.0.2. The photo manager stores staged/backup images under the current Career save's `career/vehicles/redfox_vehicle_photos` folder.
