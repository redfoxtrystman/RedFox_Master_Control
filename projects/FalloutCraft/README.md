# FalloutCraft recovery repository

This directory preserves the latest owner-supplied FalloutCraft build currently available: **v0.3.4**.

## Important recovery status

The uploaded archive is named `FalloutCraft_v0.3.4_SOURCE_PIPELINE_FIX.zip`, but inspection confirms it is an **installable binary package, not the original editable source tree**. It contains only:

- `Data/F4SE/Plugins/FalloutCraft.dll`
- `mods/FalloutCraft-fabric-0.1.0.jar`

The Fabric JAR identifies itself as FalloutCraft **0.3.4** for Minecraft **26.3**, Fabric Loader **0.19.5+**, Java **25+**, and Fabric API. The JAR also contains its JNI bridge DLL and the mirror-world datapack resources.

The exact v0.3.4 package is preserved under `releases/v0.3.4/` with SHA-256 hashes. Recovery artifacts under `recovery/` include Java bytecode disassembly (`javap`) and extracted text resources so the Fabric half can be reconstructed without guessing.

## Current runtime status

v0.3.4 successfully reaches the Minecraft mirror world, creates the Minecraft player, binds it to Fallout coordinates, starts takeover, and presents the first Minecraft HUD/hand frame. The observed freeze happens after the first Fallout `Actor::SetPosition` takeover path begins and after the first GDI overlay frame is presented. The leading suspect is the v0.3.4 change from the earlier 20 Hz puppet update to per-Fallout-frame `Actor::SetPosition` calls.

## Recovery / development direction

1. Preserve this binary baseline exactly.
2. Reconstruct the Fabric source from the class files and extracted resources.
3. Reconstruct the F4SE native source from the v0.3.4 binary behavior plus the current SkyCraft reference architecture.
4. For v0.3.5, restore a safe ~20 Hz Fallout actor/physics puppet update while retaining per-frame camera/visual interpolation.
5. Port the missing SkyCraft renderer systems, especially real Minecraft third-person avatar export/rendering (`REN_AVATAR`-style pipeline), world-space block/entity rendering, collision streaming, lights, water, combat proxies, and death/ragdoll support.

Do not delete or overwrite the v0.3.4 binary baseline while source recovery is in progress.
