FalloutCraft v0.5.4 FULL-PORT ALPHA
==================================

This is the guarded follow-up to the first whole-system Fallout 4 port of the SkyCraft architecture.

Install:
  Data/F4SE/Plugins/FalloutCraft.dll -> Fallout 4
  mods/FalloutCraft-fabric-0.1.0.jar -> the Minecraft 26.3 Fabric instance

IMPORTANT:
- Remove/replace older FalloutCraft.dll and older FalloutCraft Fabric jars.
- Launch Fallout 4 through F4SE exactly as before.
- The old GDI/layered-window overlay is permanently removed.

0.5.4 input/look/cursor pass:
- Restores SkyCraft's proven single look authority: Fallout consumes raw mouse deltas, applies Minecraft's sensitivity curve once, then publishes stable yaw/pitch back to Minecraft. This removes the v0.5.3 double-integration snap/jitter loop.
- Routes Fallout 4 input through a native BSInputEventUser inserted first in MenuControls, marking Minecraft-owned events handled so Fallout does not also open menus or move its own player.
- Restores host-driven Minecraft yaw/pitch every frame so WASD movement direction, ray picking and the Fallout camera all use the same look state.
- Adds the missing virtual Minecraft cursor to the Fallout D3D11 compositor for inventory/crafting/chest screens.
- Adds a hard timeout to the arrival hold so a missing early Fallout collision region cannot freeze Minecraft movement forever.
- Rejects behind-camera and extreme projected block vertices to stop near-plane triangles from exploding across the screen while the temporary post-scene block renderer is still in use.

0.5.3 camera/collision pass:
- Corrects Fallout 4's padded row-major camera basis (row0=right, row1=forward, row2=up). The previous Skyrim-style column basis is what rotated/tilted the world.
- Adds a Fallout PlayerCamera::Update post-hook at vfunc 0x03 so Minecraft's camera is applied after Fallout's own camera smoothing/collision pass instead of being overwritten later in the frame.
- Sends raw relative mouse deltas to Minecraft; removes the first-frame fake 960x540 camera kick.
- Replaces the failing CommonLibF4 bhkPickData result wrappers with Fallout 1.11.x verified Address Library raycast entry points and collision-filter offset.
- Anchors the emergency collision floor at the arrival height so it cannot fall downward with the player.

0.5.2 crash fix:
- Corrected the Fallout player update hook: Actor::Update is vfunc 0xCF. The previous full-port alpha incorrectly hooked TESObjectREFR::ApplyMovementDelta at 0xAD with the wrong function signature, which could corrupt movement calls and run bridge work on the wrong engine path.
- Fallout collision sampling now waits until Minecraft has a real player in the mirror world instead of firing as soon as the heartbeat appears.
- The entire bhkPickData constructor/setup/Pick/result/destructor sequence is guarded, and the hknp world is read-locked during queries.

0.5.1 crash fix:\r\n- Guards Fallout hknp Pick() calls with SEH, sets the required LOS query filter, and drastically lowers the per-frame ray budget.\r\n- If a live Fallout physics pick faults, collision rays disable for the session and a small support plane keeps the rest of the bridge testable instead of crashing Fallout.\r\n\r\nSystems present in this alpha:
- Minecraft-authoritative movement and camera state
- Fallout->Minecraft keyboard/mouse bridge
- Fallout collision stream -> Minecraft collision queries
- exact-triangle + voxel collision protocol
- Minecraft HUD/hand composited through Fallout's D3D11 Present
- Minecraft block/section render stream
- Minecraft entity/particle/item scene stream
- real Minecraft F5 avatar stream (skin/armor/held items/pose)
- texture atlas + animated atlas updates
- block placing/breaking/export protocol
- block light/hazard stream
- NPC-solid stream
- water/combat/digging/ragdoll protocols retained from the full SkyCraft port
- shared-memory heartbeat, teleport handoff and frame pacing architecture

Known first-alpha compromises:
- Fallout 4 uses hknp rather than Skyrim's hkp physics. The first Fallout-native collision
  producer samples Fallout's real cell physics with bhkPickData rays and publishes conservative
  full-block collision plus cube triangles. It is intentionally rough before the full hknp body
  harvester is validated.
- World-space Minecraft geometry is initially drawn in Fallout's final D3D11 frame. It does not
  yet use Fallout's scene depth, so some occlusion/post-processing will be wrong.
- Fallout-native combat/NPC pathing/light-spawn glue is in compatibility mode while the complete
  imported SkyCraft implementations remain in source for Fallout-specific API adaptation.

This is deliberately a full-system alpha: test the whole thing first, then fix behavior/runtime
bugs against actual Fallout 4 rather than continuing the old half-finished binary bridge.
