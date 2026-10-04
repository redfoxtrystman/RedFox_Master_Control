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

- Bridge-core CI is GREEN: run `37211488227` passed build + shared-memory smoke test.
- Build the BepInEx plugin against the user's installed Subnautica assemblies.
- Live coordinate/yaw calibration.
- Native Subnautica movement suppression during Minecraft takeover.
- Real-game proof of swimming/drowning and zombie -> drowned.
- Then replace the temporary open-ocean plane with spatial water-volume sampling and connect collision streaming.


## 2026-10-04 — implementation pass 3

- Bridge-core Windows CI is green.
  - Run: `37211488227`
  - Commit tested: `327b2edd5954ffb5279512186df5aa05959588cf`
  - Core build passed.
  - Protocol smoke executable passed.
- Fixed heartbeat compatibility correctly for .NET Framework 4.7.2:
  - removed unavailable `Environment.TickCount64`,
  - now calls Win32 `GetTickCount64`,
  - this matches the exact clock used by SkyCraft's Java `SkyLink`.
- Verified current Nitrox uses `Player.main.playerController.SetEnabled(...)` while swapping movement controllers.
- Added on-foot authority handoff:
  - Minecraft takeover disables Subnautica's `PlayerController`,
  - only in normal on-foot mode and outside cinematics,
  - disconnect/toggle-off/mode change restores it,
  - plugin destruction restores it as a final fail-safe.
- Takeover remains opt-in until coordinate/yaw calibration is tested in the real game.


## 2026-10-04 — implementation pass 4: cross-game item state

- Added a dedicated second shared-memory mapping for item/state transfer:
  - `Local\\SkyCraft_Subnautica_Items_v1`
  - SkyCraft protocol v11 remains untouched so FalloutCraft stays binary-compatible.
- Added fixed-size bidirectional item rings:
  - Subnautica -> Minecraft,
  - Minecraft -> Subnautica.
- Added stable namespaced item identity plus mutable state:
  - transfer ID,
  - origin game,
  - operation (transfer/update/consume/remove/use),
  - stack count/max stack,
  - energy/current max,
  - durability/current max,
  - item flags,
  - display name,
  - opaque origin-owned JSON state.
- Added bridge-core smoke proof using a Subnautica Seaglide:
  - enters Minecraft at 72.38% charge,
  - returns through the Minecraft -> host ring at 41.06% charge,
  - retains transfer ID 42 and `subnautica:seaglide` identity.
- Windows bridge-core CI passed the stateful item round-trip test.
- Added Java/Fabric `CrossGameItemLink` using the same mapping and record layout.
- SkyCraft now polls the item channel alongside the primary runtime bridge.
- Java/Fabric CI is running for the new item-link code.

### Next item slice

- Bind real Subnautica inventory pickup/removal to the host -> Minecraft item ring.
- Register Minecraft-side proxy items for Subnautica TechTypes.
- First functional item: Seaglide.
  - preserve battery TechType and exact charge,
  - provide underwater propulsion in Minecraft,
  - send charge updates back to Subnautica,
  - prevent duplication with transfer IDs/idempotent consumption.
- Then add battery swap, scanner, oxygen tank and survival consumables.
- Continue spatial water-volume sampling so bases/moonpools/air pockets do not look like open ocean to Minecraft.


## 2026-10-04 — implementation pass 5: functional Seaglide vertical slice

### Completed

- Added a real Minecraft item registration: `skycraft:seaglide`.
- Added legal placeholder presentation using Minecraft's prismarine-shard model; no Subnautica retail asset is committed.
- Added live Subnautica `Inventory.Pickup(Pickupable, bool)` Harmony integration.
- A Seaglide is exported only when:
  - the Subnautica pickup actually succeeded,
  - Minecraft's item-channel heartbeat is live,
  - the item ring accepts the transfer.
- The Subnautica copy is removed only after the ring accepts it.
- Minecraft leaves incoming records queued until both the local player and integrated-server inventory exist.
- Full Minecraft inventory now rejects the exact transfer ID and causes Subnautica to reconstruct the outgoing Seaglide.
- Added transfer-ID compensation/removal on both sides to close duplicate/loss paths after partial transfer failures.
- Current Subnautica GameLibs expose `EnergyMixin.charge` as read-only; charge restoration correctly writes the installed `IBattery.charge`.
- Minecraft stack data preserves:
  - transfer ID,
  - Subnautica item ID,
  - current/max energy,
  - opaque origin state JSON,
  - return-pending state.
- Minecraft-side Seaglide propulsion now follows the Subnautica rules inspected for this slice:
  - forward max: 25 m/s,
  - backward max: 5 m/s,
  - strafe max: 5 m/s,
  - base underwater acceleration: 20 m/s²,
  - Seaglide acceleration multiplier: 1.45,
  - active energy use: 0.1 per second.
- Vertical movement remains Minecraft's own swimming/fluid behavior.
- Active energy drain updates:
  - client stack,
  - integrated-server stack,
  - Subnautica state channel.
- Proof return control: press R while holding the bridged Seaglide.
  - state is sent back,
  - Minecraft marks the stack pending return,
  - exact transfer ID is removed server-side,
  - Subnautica creates the real Seaglide and restores battery charge,
  - full Subnautica inventory drops the real item safely in front of the player.
- Added `docs/VERTICAL_SLICE_002_SEAGLIDE.md` with explicit pass/fail tests.

### Automated verification

GREEN:
- Minecraft Subnautica Bridge workflow:
  - current Subnautica/Nautilus/GameLib plugin compilation,
  - bridge-core compilation,
  - shared-memory state/water/input/item smoke test.
- Minecraft Subnautica SkyCraft workflow:
  - Minecraft 26.3 / Java 25 / Fabric full build,
  - functional Seaglide proxy code,
  - item registration/resources,
  - item-channel readiness guard.

Key green runs from this pass:
- `37215483260` — Subnautica rejected-transfer recovery.
- `37215495814` — Minecraft keeps incoming item queued until inventory is ready.
- `37215345933` — SkyCraft build including registered item/resources.
- `37214059279` — stateful Seaglide shared-memory round trip (72.38 -> 41.06).

### What is proven vs. what is not

Proven by CI/code:
- both current codebases compile;
- shared-memory state and item layouts agree;
- Seaglide mutable charge survives a protocol round trip;
- real Subnautica inventory APIs compile;
- real Minecraft 26.3 item/runtime APIs compile;
- water continues to enter Minecraft through real fluid queries.

Still requires the user's local games for runtime proof:
- actual visual composite inside Subnautica;
- live Subnautica ocean -> Minecraft swimming/drowning;
- live zombie -> drowned conversion;
- axis/yaw calibration under takeover;
- live Seaglide pickup -> Minecraft -> propulsion -> charge drain -> Subnautica return.

### Next after live proof

Do not widen item coverage before Vertical Slice 001/002 are observed in the real games. After proof:
- restore exact alternate battery TechType, not only exact charge;
- battery swapping in Minecraft;
- scanner;
- oxygen tanks/fins;
- survival consumables;
- spatial water volumes/air pockets;
- Subnautica collision streaming;
- creature proxies and cross-game combat;
- bidirectional general inventory/container support.


### Pass 5 closure

- Full-inventory world-drop returns are now retained in the transfer-ID map, so a late Minecraft compensation can remove the dropped Subnautica copy too.
- Final Subnautica code verification run `37215659497`: all steps GREEN:
  - bridge core build,
  - current Subnautica plugin build,
  - protocol smoke build,
  - protocol smoke execution.
- Final SkyCraft item behavior/readiness build `37215495814`: GREEN.
- `tools/vertical_slice_001.ps1` now prints both the water/zombie proof and the Seaglide round-trip proof in one launch workflow.
