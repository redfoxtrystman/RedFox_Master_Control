# SkyCraft -> FalloutCraft gap audit (recovery baseline)

The target is the same core experience as SkyCraft, with Fallout 4 as the host world: Minecraft owns Minecraft gameplay/physics/inventory while Fallout supplies the world, NPCs, quests, saves, and host rendering.

## Confirmed present in v0.3.4 binary baseline

- shared-memory Fallout <-> Minecraft link
- automatic mirror-world startup / takeover handshake
- Minecraft player creation and host-position binding
- input takeover plumbing
- Minecraft HUD/hand frame capture
- temporary GDI screen-space overlay
- expanded mirror-world vertical range resources
- temporary support-floor fallback

## Missing or not yet proven complete

- real streamed Fallout collision field feeding Minecraft physics
- world-space Minecraft block/fluid/entity/particle renderer inside Fallout's depth buffer
- Minecraft texture-atlas transfer and animated atlas updates
- third-person Minecraft player avatar export and Fallout-side rendering (skin, armor, pose, held items)
- F5 rear/front camera parity and zoom collision
- Minecraft player death body / host ragdoll integration
- Minecraft light emitters affecting Fallout world lighting
- Fallout water -> Minecraft swimming/fluid-state integration
- Fallout NPC proxy entities for Minecraft combat
- Fallout NPC collision/path avoidance around Minecraft blocks
- Minecraft block entities / moving blocks
- digging/destruction of Fallout geometry
- robust interior/worldspace identity mapping
- host-scripted interaction takeover/return flow

## Third-person target

SkyCraft's current implementation exports the real Minecraft player through Minecraft's entity renderer whenever the camera is detached (F5), including the current skin, armor layers and pose, then the host renders that geometry in-world. FalloutCraft should port the same architecture instead of approximating the player with a custom mesh.
