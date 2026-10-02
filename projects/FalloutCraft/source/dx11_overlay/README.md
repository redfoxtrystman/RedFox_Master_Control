# FalloutCraft DX11 Overlay

Source-based replacement for the temporary GDI/layered-window compositor that froze Fallout 4.

This plugin is intentionally a **sidecar** to the recovered FalloutCraft binary while the lost source is reconstructed. It reads the existing Minecraft HUD/hand frames from `Local\\FalloutCraft_v1` and composites them directly into Fallout 4's D3D11 back buffer from `IDXGISwapChain::Present`.

It never creates a second window and never calls `UpdateLayeredWindow`.

## Existing shared-memory layout used

The recovered v0.3.4 JNI publisher rotates across three pixel slots:

- headers: `0x340 + slot * 0x40`
- frame id: header + `0x10`
- pixels: `0x2020000 + slot * 0x1FA4000`
- maximum frame: 3840 x 2160 RGBA8
- mapping: `Local\\FalloutCraft_v1`

The sidecar selects the newest stable `frameId`, copies that slot, uploads it into a dynamic D3D11 texture, then draws a full-screen triangle with premultiplied-alpha blending.

## Fallout 4 hook

The hook follows the working Fallout 4 pattern used by current F4SE projects:

1. patch the real game's `D3D11CreateDeviceAndSwapChain` CALL site (`REL::ID(224250) + 0x419`);
2. capture the game's real D3D11 device/context;
3. patch the real swap chain VTable entry 8 (`IDXGISwapChain::Present`);
4. draw immediately before the original Present.

## Status

Source-complete first pass. Windows/F4SE runtime testing is required before this replaces the no-GDI test baseline.

The next renderer stages are Minecraft's special invert-blend crosshair, world-space block/entity rendering, and the real F5 Minecraft avatar stream.
