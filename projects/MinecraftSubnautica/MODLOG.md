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


## 2026-10-04 — implementation pass 2

- Verified current Nautilus development guidance: .NET Framework 4.7.2, BepInEx 5.4.21, Nautilus dependency.
- Added the real Subnautica BepInEx host plugin scaffold.
- Added open-ocean water export using `Ocean.main.GetOceanLevel()`.
- Added host player/camera state export using `Player.main` and Unity camera state.
- Added opt-in Minecraft-authoritative player transform takeover.
- Verified SkyCraft water hooks are general entity-fluid hooks:
  - `EntityFluidInteractionMixin`,
  - `EntitySwimMixin`,
  - `SkyWater.refresh()` every linked client frame.
- Added host -> Minecraft input-ring production and Subnautica keyboard/mouse forwarding.
- Added Windows bridge-core CI and a shared-memory smoke test covering state, water, input, and Minecraft state.
- Added `SKYCRAFT_LINK` support to the SkyCraft dev run config and a Subnautica launcher using `Local\\SkyCraft_Subnautica_v1`.

### Still required before calling vertical slice 001 complete

- CI must pass.
- Build the BepInEx plugin against the user's installed Subnautica assemblies.
- Live coordinate/yaw calibration.
- Native Subnautica movement suppression during Minecraft takeover.
- Real-game proof of swimming/drowning and zombie -> drowned.
- Then replace the temporary open-ocean plane with spatial water-volume sampling and connect collision streaming.
