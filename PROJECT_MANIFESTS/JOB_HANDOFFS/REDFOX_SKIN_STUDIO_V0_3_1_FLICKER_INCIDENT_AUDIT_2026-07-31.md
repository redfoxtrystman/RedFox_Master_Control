# RedFox Skin Studio v0.3.1 Flicker Incident Audit — 2026-07-31

## User-reported incident

David confirmed that RedFox Skin Studio v0.3.0 still showed black/checkerboard repaint artifacts and visible flickering while the mouse or artwork was moved. The earlier fix that only disabled `Accelerated2dCanvasEnabled` did not eliminate the Windows embedded-Chromium rendering problem.

## Baseline handling

- RedFox Skin Studio v0.2.9 remains the locked baseline.
- RedFox Skin Studio v0.3.0 is preserved unchanged as the first Ellexium vehicle/configuration catalog build.
- The corrective work is versioned separately as v0.3.1.

## Corrective changes in v0.3.1

1. Safe software/SwiftShader rendering is now the default launcher mode.
2. Qt software OpenGL is selected before QApplication and QWebEngine are imported.
3. Chromium safe-mode flags disable GPU rasterization, zero-copy, Vulkan, and Canvas OOP rasterization while preserving a software WebGL path.
4. The 2D editor now renders to an off-screen canvas and performs one atomic copy to the visible canvas.
5. Repeated mousemove redraws are coalesced with `requestAnimationFrame`.
6. `ResizeObserver` callbacks no longer reset the canvas bitmap when dimensions did not actually change.
7. Hover transforms, animated transitions, backdrop blur, and the large workspace overlay are disabled in safe mode.
8. `run_hardware_graphics.bat` is included only as an optional diagnostic launcher and is not the first-test path.

## Validation completed

- Python `compileall`: passed.
- JavaScript syntax check with Node: passed.
- RedFox backend self-test: passed.
- Static assertions for software compositor, double buffer, frame coalescing, resize guard, and safe CSS: passed.
- ZIP integrity test: passed.

## Runtime boundary

The Linux build environment cannot reproduce David's exact Windows graphics driver, Qt WebEngine compositor, or BeamNG runtime. Therefore v0.3.1 is **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED** until David tests this exact package.

## Artifact

- File: `RedFox_Skin_Studio_v0_3_1_FLICKER_SAFE_RENDER_HOTFIX_BUILT_RUNTIME_UNTESTED.zip`
- SHA-256: `26fc8275785cb902676aa48487f5b936a02be6a01df707d24b731e11838cd5c1`
- Size: 3,616,798 bytes
