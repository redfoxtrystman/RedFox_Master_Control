# RedFox Skin Studio v0.2.2 — Shared Install, Folder Memory and Red Fox Towing Kit

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_2_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `1f452311ea8c2ff3f16473bdaa9ace5fc68e449448e0ac7dc8ff73e5103d51c5`

## Owner request

David requested that test versions stop requiring a fresh dependency install and stop forgetting selected folders. Folder paths must be chosen through browser dialogs rather than copied and pasted. He also requested a generic company-livery starter based on the supplied tow-truck reference, using the correct name **Red Fox Towing**, with independently movable company text, phone/service text, numbers and names while leaving final logo placement/orientation under user control.

## Implemented in v0.2.2

### One shared installation/runtime

- Added `SETUP_ONCE.bat` / `setup_once.ps1`.
- The first setup opens folder selectors for the application/shared runtime and the persistent workspace.
- Both locations may be placed on a non-C drive.
- One stable launcher follows the currently selected installed version.
- Added `UPDATE_EXISTING_INSTALL.bat` for installing an extracted later version without rebuilding the Python runtime.
- Added in-app **Install Update ZIP** and **Rollback Update** actions.
- Installed versions are retained under `App/Versions` so rollback is possible.

### Cross-version persistence

- Added a small global bootstrap pointer under the Windows local application-settings area.
- Large/user data remains in the selected workspace, not the small pointer location.
- All installed versions share the same projects, settings, vehicle index, UV candidates, Asset Album, Design Vault, backups, exports and cache.
- BeamNG install/user/mod/output and extra-storage folder settings persist across versions.
- Added migration from the older version-local workspace pointer.
- Changing the workspace copies existing data before switching.
- Added remembered last folders for mod ZIPs, UV/skin images, Asset Album imports, Design Vault imports and build outputs.

### Folder selection

- Settings retains Browse buttons for primary folders.
- Guided Wizard now has Browse buttons for BeamNG install, user and active-mod folders.
- Extra mod-storage paths are now managed with **Add Folder** / **Remove Selected**, not a semicolon-separated text field.

### Red Fox Towing kit

- Added a visible **Red Fox Towing Kit** action.
- The kit dialog collects company name, phone/call sign, services line, fleet/unit number, operator/truck name and seafoam/purple/silver colors.
- The kit creates independent editable base, stripe, accent, company, phone, services, number and name layers.
- Added an optional `DROP LOGO HERE` guide; both guide layers use `excludeFromExport=true`.
- The actual logo is intentionally not baked into the kit because left/right orientation remains vehicle/UV-specific.
- Added visible **Duplicate Selected** access. Existing `Ctrl+C`, `Ctrl+V` and `Ctrl+D` layer shortcuts remain available.

## Validation completed

- Python compile-all passed.
- Editor JavaScript syntax validation passed.
- Backend Asset Album, Design Vault and BeamNG ZIP exporter self-test passed.
- Red Fox Towing kit test created 18 independent layers.
- Company and unit-number layers were verified.
- Both logo-guide layers were verified as non-exported.
- HTML/feature structure checks passed.
- Isolated update ZIP staging/current-version/rollback test passed.
- UTF-8 BOM bootstrap compatibility test passed.
- Final ZIP archive integrity test passed.

## Not proven

- Windows one-time setup dialogs and environment creation.
- Windows in-app update/restart behavior.
- PySide6/QWebEngine live GUI interaction because PySide6 is unavailable in the Linux build container.
- Windows drag/drop/clipboard/WebGL preview.
- BeamNG in-game rendering from this exact build.

## Important limit

The Red Fox Towing kit is a generic editable layer collection, not automatic semantic UV placement. Vehicle UV layouts differ, so pieces and the real logo must still be moved to the correct panels and oriented correctly.

No one may relabel this build as working until David tests this exact archive on Windows and in BeamNG.
