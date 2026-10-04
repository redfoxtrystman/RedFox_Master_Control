# Minecraft ↔ Subnautica

This project uses **SkyCraft as the runtime base** and **Universal Modder in its entirety** as the modding/recon/build/verification network.

## Core rule

Neither game is rewritten.

- Minecraft remains authoritative for Minecraft movement, swimming, drowning, mobs, inventory, crafting, item behavior, combat math, status effects, rendering, and game rules.
- Subnautica remains authoritative for the Subnautica world, terrain, water spaces, creatures, vehicles, bases, resources, hazards, and native item state.
- The bridge translates state and events between them.

The first target is not a cosmetic mashup. It is a real cross-game rules bridge.

Examples:

- Subnautica water is reported to Minecraft as water so vanilla Minecraft swimming, oxygen, drowning, Depth Strider, Respiration, mob water behavior, and zombie-to-drowned conversion can occur normally.
- A Subnautica item moved into Minecraft keeps its real identity and mutable state such as charge, durability, upgrades, stack count, and origin.
- Minecraft items moved into Subnautica retain Minecraft metadata and behavior through adapters rather than becoming inert lookalikes.
- Minecraft remains the authority for Minecraft mobs. A zombie submerged in Subnautica water must become a drowned because Minecraft's actual conversion logic says so.

## Base source

This branch is based on:

- `projects/FalloutCraft/source/full_port/`
- Minecraft 26.3 / Fabric / Java 25 SkyCraft code
- SkyCraft shared-memory protocol v11
- existing SkyCraft water-grid support

The existing Minecraft side already accepts a custom mapping name with:

`-Dskycraft.link=Local\\SkyCraft_Subnautica_v1`

That lets the Subnautica host reuse the proven protocol without breaking FalloutCraft.

## Phase 0 vertical slice

1. Subnautica host creates `Local\SkyCraft_Subnautica_v1`.
2. Host writes the existing SkyCraft v11 header and heartbeat.
3. Host writes player/world state.
4. Host exports a 16x16 water-surface grid around the player.
5. Minecraft reads that grid through the existing SkyCraft water path.
6. Minecraft writes its authoritative `McState` back.
7. Subnautica adapter reads `McState` and can puppet the Subnautica player/camera.
8. Verify actual Minecraft swimming and drowning in Subnautica ocean water.
9. Verify a zombie uses vanilla underwater conversion behavior and becomes a drowned.

No fake "Subnautica swimming" implementation is permitted on the Minecraft side.

## Universal Modder

The reviewed Universal Modder revision is pinned in `universal-modder.lock`.

Run:

`tools\bootstrap_universal_modder.ps1`

This clones the **entire** Universal Modder repository at the pinned revision and installs its CLI. The project uses its recon, skills, knowledge base, backup, scan, asset, automation, verification, publishing, and field-note workflow.

Every meaningful development session updates `MODLOG.md`.
