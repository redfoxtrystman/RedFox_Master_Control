# JOB-13 v0.1.8.3 Triple Verification Audit

Date: 2026-08-02
Scope: JOB-13 only. JOB-04 Wrecking Yard and shared FoxNet/browser files were not edited.

## Source

- Base: unreleased JOB-13 v0.1.8.2 stable-state repair tree
- Output: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_3_STABLE_STATE_CAMERA_THUMBNAIL_RETAKE.zip`
- SHA-256: `9c1789d5d8013d783cb2d14f0bc4fb48bd7319afa45d5df66531cb454499015a`
- Files: 19

## Gate 1 — Before editing

PASS

- Recorded SHA-256 and size for every source file.
- Confirmed 19-file JOB-13-only source tree.
- Confirmed existing stable-state fixes, persistent account/watchlist design, varied catalog, unique FoxNet route, image viewer, and direct Career delivery were present before modification.
- No Wrecking Yard source was copied into the build.

## Approved change

Add an owner-controlled thumbnail repair for a purchased auction vehicle:

1. Open the exact purchased lot after Career delivery assigned an inventory ID.
2. Call or spawn that owned vehicle.
3. Position the normal BeamNG in-game camera.
4. Press `Retake image from current camera`.
5. Save the render-view screenshot to the exact Career inventory thumbnail path.
6. Update the purchased lot image with cache busting.

Safety rules:

- Exact settlement inventory ID is required.
- Exact inventory vehicle must still exist.
- Vehicle must be spawned.
- Camera must be between 0.75 and 80 meters from the vehicle.
- Duplicate simultaneous capture is blocked.
- Uses `render_renderViews.takeScreenshot`, so the FoxNet webpage is not burned into the image.
- Does not modify money, ownership, garage assignment, condition, or delivery.

## Gate 2 — After editing

PASS

Changed files: 9

- `lua/ge/extensions/redfoxJob13Auction.lua`
- `mod_info/RedFoxJOB13/RUNTIME_NOTE.txt`
- `mod_info/RedFoxJOB13/info.json`
- `sites/redfox_job13_auctions/index.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job13_auctions/index.html`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.html`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.json`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.css`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.js`

Checks:

- JavaScript syntax: PASS for host and auction page.
- JSON parsing: PASS for all JSON files.
- Mirrored unique route identity: PASS.
- Existing state-merge harness: PASS.
- Stable membership/watchlist/max-bid/image-viewer source checks: PASS.
- New camera action dispatch and UI action wiring: PASS.
- Exact inventory ID, spawn validation, camera APIs, distance guards, thumbnail path, render-view API, and cache-bust checks: PASS.
- Lua delimiter/static balance: PASS.
- No active v0.1.8.2 cache keys remain except historical release-note text.

## Gate 3 — After ZIP creation

PASS

- ZIP integrity: PASS.
- Duplicate ZIP paths: 0.
- Fresh extraction: PASS.
- All 19 extracted file hashes exactly match the after-edit build tree.
- Final JavaScript syntax: PASS.
- Final JSON parse: PASS.
- Final mirrored route identity: PASS.
- SHA-256 confirmed: `9c1789d5d8013d783cb2d14f0bc4fb48bd7319afa45d5df66531cb454499015a`.

## Runtime status

UNPROVEN until David tests the exact ZIP in BeamNG.

The Wrecking Yard ZIP that already passed PC/phone purchasing should remain unchanged and enabled.
