# FalloutCraft collision bridge — implementation target

v0.3.8 proved that Minecraft movement works in Fallout when the crashing GDI compositor is removed. The current walk-through-walls behavior is expected because the recovered Fabric build explicitly uses only a temporary support floor; the full Fallout collision stream was never implemented.

## Correct architecture

Do **not** hand physics ownership back to Fallout's player controller. Minecraft remains authoritative.

The port should mirror current SkyCraft:

1. Fallout side reads the current cell's Havok **hknp** world under its read lock.
2. Nearby host collision is harvested in small 8x8x8-Minecraft-block regions with a strict per-frame budget.
3. Host shapes are converted to Minecraft coordinates and sent as exact triangles for the local player's smooth collider and 1/8-block occupancy masks for ordinary Minecraft collision queries and other entities.
4. A worker thread performs expensive voxelization after the Fallout main thread has copied safe shape data.
5. Minecraft consumes the collision ring on its own daemon thread.
6. Minecraft's normal collision code remains unchanged except for Mixins that append Fallout collision shapes; the local player additionally resolves movement against exact host triangles.

## Fallout-specific difference from Skyrim

Fallout 4 uses Havok **hknp** structures rather than Skyrim's older hkp world/island layout. Current CommonLibF4 exposes the pieces needed to begin this port, including `TESObjectCELL::GetbhkWorld()`, `bhkWorld` / `bhkWorldM`, `hknpBSWorld`, its world read lock, `hknpWorld`, `hknpBodyManager`, and `hknpBody`.

The Skyrim Collision.cpp cannot simply be copied byte-for-byte; its hkp island enumeration must be rewritten for Fallout's hknp body manager.

## Minecraft pieces to reconstruct from SkyCraft

- SkyCollision region store / ring consumer
- BlockCollisionsMixin
- SkyCollider exact triangle solver
- EntityCollideMixin
- teleport hold until collision around the arrival point is known

This is the subsystem that will stop the Minecraft player walking through Vault walls, floors, doors, stairs and terrain while preserving Minecraft-style walking, jumping, sprinting and crouching.
