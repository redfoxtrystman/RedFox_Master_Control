# FalloutCraft Extended (zeyvu base)

This branch deliberately stops maintaining the earlier experimental FalloutCraft port as the primary codebase.
It uses **zeyvu/FalloutCraft** as the upstream base and applies RedFox-specific fixes/features as an overlay.

Pinned upstream:
- Repository: https://github.com/zeyvu/FalloutCraft
- Commit: 52030998d63532a1a4d147b394bcc7b07da6f4f4
- Upstream date: 2026-10-02
- Upstream status: v0.1.2-era source with Fallout 4 collision, rendering, combat, scavenging and gathering already implemented.

## RedFox control policy

Minecraft keeps its normal controls:
- **E** = Minecraft inventory
- **Left Ctrl** = sprint
- **Left Shift** = crouch / sneak
- **O** = Minecraft pause/options

Fallout retains:
- **G** = Fallout Activate (doors, NPCs, containers, terminals, workbenches; held interactions stay native Fallout behavior)
- **Tab** = Pip-Boy
- **Esc** = Fallout pause when no Minecraft screen is open
- **~** = Fallout console
- **F9** = Fallout quickload

The C++ override is in `overrides/FO4_ModFiles/fo_input.cpp`.

## Feature roadmap

The current upstream README has a stale Known Limitations block. Current main already contains more than that list implies:
- Fallout-world digging/gathering exists.
- Placed Minecraft blocks have Fallout-side collision, so NPCs/creatures bump into them; route planning around builds is still not implemented.
- Multiplayer code exists (LAN/e4mc join/leave plumbing), though it remains experimental.
- Minecraft-side water support exists, but Fallout-side water-grid publishing still needs a proper Fallout implementation before it is complete.

Actual high-value extension targets:
1. Fallout stimpaks/food healing Minecraft hearts.
2. Give Charisma and Intelligence meaningful Minecraft effects.
3. Minecraft dynamic lights affecting Fallout geometry.
4. Fallout water -> Minecraft water grid publishing.
5. NPC path planning around Minecraft builds, not merely collision.
6. Fallout skill/perk progression from Minecraft actions where a Fallout analogue exists.
7. Uneven/cracked-road collision smoothing.
8. Multiplayer hardening and Fallout-host state synchronization.
