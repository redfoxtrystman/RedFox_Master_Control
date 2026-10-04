# Render + collision live proof

This pass closes the two large gaps found after the first successful heartbeat/water link.

## What should happen after link

Minecraft still runs the Minecraft simulation, but its normal window is hidden after the Subnautica heartbeat is live.

Subnautica now consumes Minecraft's existing SkyCraft render output:

- overlay triple buffer -> Minecraft hand, HUD and GUI screens;
- block atlas + section meshes -> Minecraft blocks in the Subnautica 3D world;
- entity textures + scene meshes -> Minecraft mobs/entities/particles;
- avatar mesh -> third-person Minecraft player body when Minecraft publishes it.

Subnautica also streams nearby Unity collision back to Minecraft using the existing SkyCraft collision ring. The first live pass is intentionally coarse: any static Unity collider intersecting a Minecraft-sized cell fills that one block's 8x8x8 occupancy. This makes terrain, reefs, wrecks, bases and collidable flora solid to Minecraft immediately. Exact triangles/sub-block voxelization can refine it later without a protocol change.

## Required BepInEx log proofs

After both games link:

```text
BRIDGE PROOF: Minecraft connected (PID ...)
COLLISION PROOF: initialized Subnautica -> Minecraft collision stream.
COLLISION PROOF: sent first Unity region (...), N solid Minecraft-space blocks.
RENDER PROOF: Minecraft HUD/hand overlay received ...
RENDER PROOF: Minecraft texture atlas received ...
```

After Minecraft has a block section to draw:

```text
RENDER PROOF: first Minecraft section rendered at (...), N triangles.
```

When Minecraft publishes entities/particles:

```text
RENDER PROOF: Minecraft entities/particles mesh received, N triangles in N batches.
```

## Visual proof

1. Start Subnautica and load a save in open ocean.
2. Start Minecraft 26.3 with the dedicated MinecraftSubnautica SkyCraft JAR.
3. Minecraft links and hides its window.
4. The Minecraft HUD/hotbar/hand appears over the Subnautica picture.
5. Subnautica itself continues drawing its ocean, terrain, flora, bases and creatures.
6. Minecraft receives nearby Subnautica static collision, so its player no longer falls/walks through reefs, terrain, bases or other collidable surroundings.
7. Place Minecraft blocks in the mirror simulation. They should appear as real textured Unity meshes at the corresponding Subnautica-space position and depth-test against the Subnautica scene.
8. Minecraft mobs/entities/particles should appear when their RenderScene batches are published.

## Current collision quality

The first live collision pass is block-resolution for safety and performance:

- one Unity-intersected 1m cell -> one full Minecraft collision block;
- triggers are ignored;
- the Subnautica player's own colliders are ignored;
- non-kinematic rigidbodies (creatures, loose items, moving objects) are not treated as static terrain.

This is intentionally conservative. The next quality pass is 1/8-block occupancy plus exact MeshCollider triangles for smooth terrain and curved base geometry.

## If one layer fails

The proof logs identify the layer:

- connected + water only, no `RENDER PROOF` overlay -> overlay producer/consumer path;
- overlay works, no atlas -> Minecraft world exporter path;
- atlas works, no section -> no Minecraft section has been emitted/changed yet;
- section proof but invisible mesh -> Unity material/camera/depth layer;
- collision initialized but first region reports 0 solids while standing at terrain -> Unity collider sampling/layer issue.
