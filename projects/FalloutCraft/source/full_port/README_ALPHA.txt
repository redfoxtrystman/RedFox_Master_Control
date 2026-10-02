FalloutCraft v0.5.0 FULL-PORT ALPHA
==================================

This is the first whole-system Fallout 4 port of the SkyCraft architecture.

Install:
  Data/F4SE/Plugins/FalloutCraft.dll -> Fallout 4
  mods/FalloutCraft-fabric-0.1.0.jar -> the Minecraft 26.3 Fabric instance

IMPORTANT:
- Remove/replace older FalloutCraft.dll and older FalloutCraft Fabric jars.
- Launch Fallout 4 through F4SE exactly as before.
- The old GDI/layered-window overlay is permanently removed.

Systems present in this alpha:
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
