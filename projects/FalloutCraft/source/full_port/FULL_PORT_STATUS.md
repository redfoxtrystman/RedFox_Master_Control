# FalloutCraft full SkyCraft port — handoff/status

Branch: `falloutcraft-full-skycraft-port`

## Completed in this one-pass import

- Imported the complete SkyCraft Fabric source tree into `source/full_port/fabric`.
- Imported the complete SkyCraft shared-memory protocol and renamed the host mapping to `Local\\FalloutCraft_v2`.
- Imported every SkyCraft native subsystem into `source/full_port/f4se`: movement/takeover, camera/F5/death path, input ownership, HUD compositor, world renderer, block/entity/avatar render stream, collision, digging/destruction, water, lights, combat, NPC block collision/path avoidance, launcher, link, diagnostics/crash logging.
- Imported SkyCraft tools and design documentation.
- Added Fallout 4/F4SE/CommonLibF4 build scaffolding and CI.
- Preserved the upstream MIT license.
- Fabric/Minecraft 26.3 full-port build currently passes in CI.

## Important current boundary

The native host half is **not yet runtime-testable**. The whole architecture is present, but the first F4SE compile exposes the expected Skyrim-vs-Fallout engine API differences. This is no longer missing-feature work; it is host adaptation work.

The latest native compile reaches the actual C++ build and fails on Fallout-specific equivalents in several systems, especially:

- `Collision.cpp/.h`: SkyCraft's older Havok hkp shape/world APIs must be converted to Fallout 4's hknp world/body APIs.
- `WorldRender.cpp`: Skyrim render-target enums/runtime camera wrappers do not exist in CommonLibF4. Fallout exposes `NiCamera::worldToCam/viewFrustum/port` directly and `BSGraphics::GetRendererData()` with numeric render/depth target arrays.
- `BlockLights.cpp`: Skyrim light creation/runtime structures must be replaced with Fallout 4 light APIs.
- `Combat.cpp`: actor-value, hit-data, hostility/essential/dead checks and form helpers need CommonLibF4 equivalents.
- additional Game/Input/Dig/NPC/pathing hooks will be compiled and adapted after these first blockers are cleared.

## Build policy

Do not fall back to the old partial GDI architecture. The stable findings remain authoritative:

- GDI/layered-window compositor caused the Fallout freeze and stays removed.
- Minecraft owns movement/physics and final look state.
- Fallout supplies collision/world/NPC/scene data.
- HUD renders through Fallout's D3D11 frame.
- world-space Minecraft rendering uses the render ring and Fallout depth.
- third-person uses Minecraft's real avatar exporter/model stream.

The next pass should continue from this branch and fix CommonLibF4/Fallout 4 API substitutions until the native DLL compiles, then package both halves together for the first full-system runtime test.
