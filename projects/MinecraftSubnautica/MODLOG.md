# MODLOG — Minecraft ↔ Subnautica

## 2026-10-04 — project start

### Locked decisions

- SkyCraft is the runtime base.
- Universal Modder is used in its entirety, not copied piecemeal.
- Minecraft 26.3 / Fabric / Java 25 stays the Minecraft authority for the current SkyCraft line.
- The bridge must preserve real game rules instead of reimplementing them in the other game.
- Subnautica water must feed Minecraft's real fluid/environment queries.
- Zombie -> drowned is a required behavioral proof, not a scripted special case.
- Cross-game items must preserve state and be usable, not merely represented by icons/models.
- The existing SkyCraft protocol v11 is reused for the first vertical slice.
- The Subnautica mapping is isolated as `Local\SkyCraft_Subnautica_v1`.
- FalloutCraft recovery/baseline files are not overwritten.

### Work completed

- Created branch `minecraft-subnautica-universal-bridge` from `falloutcraft-full-skycraft-port`.
- Verified SkyCraft already has:
  - configurable shared-memory mapping names,
  - host heartbeat + Minecraft heartbeat,
  - host state -> Minecraft,
  - Minecraft authoritative state -> host,
  - a 16x16 water-surface grid,
  - collision/input/event/render rings.
- Pinned Universal Modder commit `8607693be42ce02442251f05e0495f58c2b77e5d`.
- Added a standalone C# host-side shared-memory core compatible with SkyCraft protocol v11.

### Next engineering slice

- Bind the C# host core to Subnautica/BepInEx/Nautilus.
- Source the actual Subnautica player transform and viewport.
- Probe ocean/water volumes and air pockets.
- Feed input to Minecraft.
- Puppet Subnautica player/camera from Minecraft `McState`.
- Run the first in-game water test.
