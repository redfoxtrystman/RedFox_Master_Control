# RedFox Skin Studio v0.2.4a — Startup Crash Hotfix

**Date:** 2026-07-27  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_4a_STARTUP_HOTFIX_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `ab8dc8e3552598c01fa57747ab1da2174c4995287b06c1c5e84d3b1589731a15`

## Failure reported by David

The v0.2.4 package failed immediately during startup with:

```text
UnboundLocalError: cannot access local variable 'QTimer' where it is not associated with a value
```

The traceback identified `redfox/main_window.py` in `MainWindow.__init__` while constructing the external-edit reload timer. Qt also printed a warning that the high-DPI rounding policy was being set after `QApplication` creation.

## Root cause

`QTimer` was already imported at module scope, but `MainWindow.__init__` contained a second nested import inside the startup-wizard conditional. In Python, that nested import made `QTimer` a local variable for the entire function, so earlier uses of `QTimer` failed before execution reached the nested import.

The high-DPI warning was caused by calling `setHighDpiScaleFactorRoundingPolicy` after constructing `QApplication`.

## Fixes in v0.2.4a

- Removed the nested `QTimer` import from `MainWindow.__init__`.
- Reused the existing module-level `QTimer` import.
- Moved `QApplication.setHighDpiScaleFactorRoundingPolicy(...)` before `QApplication(sys.argv)`.
- Added self-test regression assertions for both startup-order defects.
- Updated the application version to `0.2.4a`.

No editor, exporter, external-editor, project, shared-workspace or 3D-preview feature was intentionally removed or redesigned in this hotfix.

## Verification completed

- Python `compileall`: PASS.
- Backend self-test: PASS.
- QTimer-shadowing regression assertion: PASS.
- High-DPI initialization-order assertion: PASS.
- Editor JavaScript syntax check: PASS.
- Final ZIP integrity test: PASS.

## Not proven

- Windows GUI startup on David's computer.
- External-editor launch/save/reload round trip.
- Live 3D preview.
- Blender workflow.
- BeamNG runtime export/rendering.

The status must remain **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED** until David launches and tests the exact hotfix package.
