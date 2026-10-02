# FalloutCraft full SkyCraft port

This directory is the one-pass source port of SkyCraft's entire native host half into an F4SE/CommonLibF4 target.

All upstream systems are present in source form: shared-memory link, launcher, input ownership, Minecraft HUD compositor, world rendering, Minecraft block lights, host collision export, digging/destruction, combat, NPC block collision/path avoidance, camera/F5/death handling and crash diagnostics.

This is intentionally the **full system first** branch. Host-specific compile/runtime incompatibilities are fixed against Fallout 4 after the complete architecture is present instead of maintaining the old reduced binary bridge.

The Minecraft half lives in `../fabric`; the common protocol lives in `../protocol`.

SkyCraft's MIT license is retained in the Fabric tree and the upstream source attribution is preserved in project documentation.
