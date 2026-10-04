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


## 2026-10-04 — runtime link packaging fix

- Found the reason the user's normal Minecraft launch did not connect/background:
  - the dedicated Minecraft/Subnautica JAR still defaulted the primary SkyCraft mapping to `Local\\FalloutCraft_v2`;
  - Subnautica correctly created `Local\\SkyCraft_Subnautica_v1`;
  - therefore `SkyLink.active()` never became true, so the existing automatic `SDL_HideWindow` handoff never fired.
- Fixed the dedicated branch default mapping to `Local\\SkyCraft_Subnautica_v1`.
- `-Dskycraft.link=...` remains available as an explicit developer override.
- Updated the Subnautica plugin startup log: normal dedicated JAR launch no longer requires a special JVM argument.
- Rebuilt both deliverables successfully.
- Binary verification confirms the compiled JAR contains:
  - `Local\\SkyCraft_Subnautica_v1`,
  - `SDL_HideWindow`,
  - the linked-window hide log string.
- Important remaining distinction:
  - link/background handoff is now fixed;
  - movement takeover remains opt-in until live coordinate/yaw calibration;
  - full Subnautica-side consumption of every SkyCraft render-ring/world-render primitive is a separate integration layer and should not be claimed as live-proven yet.


## 2026-10-04 — render/collision integration pass

User live test proved heartbeat + water linking but exposed that the Subnautica host still was not consuming SkyCraft's visual output and Minecraft still had no Subnautica world collision.

### Fixed

- Added Subnautica-side consumption of SkyCraft's overlay triple buffer.
  - Minecraft HUD, hotbar, hand and GUI screens are uploaded into a Unity `Texture2D` and drawn over the Subnautica frame.
- Added Subnautica-side render-ring consumer.
  - `RenderAtlas` -> Minecraft block/item texture atlas.
  - `RenderAtlasRegion` -> animated atlas updates (water/lava/fire/etc.).
  - `RenderSection` -> Minecraft block section meshes as Unity `Mesh` objects.
  - `RenderTexture` -> Minecraft entity/player textures.
  - `RenderScene` -> Minecraft mobs/entities/particles as Unity meshes with texture batches.
  - `RenderAvatar` -> third-person Minecraft player mesh path.
  - `RenderClearAll` -> tears down stale Minecraft world meshes.
- Unity 3D meshes use normal scene transforms/depth so Subnautica geometry can occlude Minecraft geometry instead of everything being a flat screenshot.
- Added Subnautica -> Minecraft collision-ring producer.
- Added a progressive 3x3x3 region sampler around the player using Unity's real Physics colliders.
- Initial collision quality is intentionally conservative block-resolution:
  - any static Unity collider intersecting a 1m cell fills that Minecraft cell;
  - triggers are ignored;
  - player colliders are ignored;
  - non-kinematic rigidbodies are excluded from static world collision.
- This gives Minecraft immediate collision awareness of Subnautica terrain, reefs, bases/wrecks and collidable flora while preserving the protocol path for later 1/8-block/exact-triangle refinement.
- Added proof logs for each stage:
  - `RENDER PROOF: Minecraft HUD/hand overlay received ...`
  - `RENDER PROOF: Minecraft texture atlas received ...`
  - `RENDER PROOF: first Minecraft section rendered ...`
  - `RENDER PROOF: Minecraft entities/particles mesh received ...`
  - `COLLISION PROOF: initialized ...`
  - `COLLISION PROOF: sent first Unity region ...`
- Added `docs/RENDER_COLLISION_LIVE_TEST.md`.
- Expanded bridge smoke tests to verify:
  - overlay frame acquisition;
  - render-ring consumption/tail advance;
  - collision-ring production/epoch payload.

### Verification

- Current Subnautica/Nautilus/GameLib plugin compilation: GREEN.
- Bridge-core compilation: GREEN.
- Updated protocol smoke build: GREEN.
- Updated protocol smoke execution: GREEN.
- Artifact-producing run `37218570876`: GREEN.

### Next fidelity pass after live proof

- refine Unity collision from full-block occupancy to 1/8-block voxels;
- emit exact MeshCollider triangles for smooth terrain/base geometry;
- match Subnautica lighting/fog/material response for Minecraft meshes;
- add WorldEntities helpers (dropped block/item billboards, arrows/tridents, selection/crack overlays) where RenderScene does not already cover them;
- improve premultiplied-alpha HUD composition if the live Unity blend path shows dark fringes.


## 2026-10-04 — live test: simulation alive, visual producer stalled

User's live screenshot showed normal Subnautica rendering with no Minecraft HUD/hand/world visuals. Minecraft audio simultaneously produced splash/drowning sounds, proving:
- shared-memory heartbeat/state was live;
- Subnautica water was reaching Minecraft simulation;
- Minecraft client tick/audio simulation was alive;
- the failure was isolated to the visual-export path.

### Root-cause candidate found and fixed

The linked SkyCraft client called `SDL_HideWindow()` as soon as the host connected. On Minecraft 26.x/SDL this can leave simulation/audio ticking while the GPU presentation/render path stops or is short-circuited. That prevents both:
- `FrameExporter` from getting new HUD/hand framebuffer readbacks;
- the render-frame timing path that drives the world visual exporter reliably.

The dedicated Minecraft/Subnautica client now does **not** hide or minimize its SDL window.

Instead it:
- explicitly keeps the SDL window shown/render-active;
- moves it to `(-32000,-32000)`;
- sets opacity to 1%;
- continues pretending focused/not-iconified through the existing mixins;
- reapplies the off-screen parking after host viewport resizing.

This keeps Minecraft effectively invisible to the player while preserving an active GPU render target for Subnautica.

### Added visual proof/diagnostics

Minecraft now logs the first successful framebuffer publication:

`SkyCraft render proof: published first HUD/hand overlay frame ...`

Subnautica now logs producer/consumer health every 5 seconds until visuals arrive:

`VISUAL BRIDGE STATUS: overlayFrames=..., overlayState=..., renderHead=..., renderTail=..., overlaySeen=..., sectionSeen=...`

This separates:
- no Minecraft visual production (`overlayFrames=0`, no render head);
- Minecraft producing but Subnautica not consuming (head advances, tail stalls);
- ring consumption working but Unity display failing (seen flags true but nothing visible).

### Verification

GREEN:
- Minecraft 26.3 / Java 25 / Fabric build with render-active background window.
- Artifact-producing SkyCraft run `37219974228`.
- Current Subnautica/Nautilus/GameLib build with visual diagnostics.
- Bridge-core build.
- Overlay/render/collision protocol smoke tests.
- Artifact-producing Subnautica run `37220071192`.

Binary verification of the new JAR:
- contains `SDL_SetWindowOpacity`;
- contains `SDL_SetWindowPosition`;
- contains `render window parked off-screen at 1% opacity; GPU frame export remains active`;
- no `SDL_HideWindow` string in the compiled `SkyClient.class`.

Matched local test bundle:
- JAR SHA-256: `09c9cb8ca825a9a948bb2864a224d0b698b15d0f0b121c1e7045b852f2089210`
- Subnautica package SHA-256: `a532fff3e39175b8016eac6f881fd9d3e0cee79e3d0f196a03b3934f0b189ad8`
- Subnautica DLL SHA-256: `5cfeafe5aa31766843e0f60eb511da71bbf23208af091dd8679e79ea4ba5dd50`


## 2026-10-04 — source-backed visual pipeline reset

The previous Subnautica visual pass mixed an experimental Unity OnGUI/Unity-mesh consumer with SkyCraft's
native-host mesh protocol. User correctly rejected further guess-driven fixes because the repository already
contains working reference implementations.

### Source of truth used

Universal Modder commit:
- `8607693be42ce02442251f05e0495f58c2b77e5d`

Directly inspected/ported:
- `skills/mashup-mods/SKILL.md`
- `skills/reverse-engineering/SKILL.md`
- `examples/minecraft-gta5-passthrough/mc/.../FrameExporter.java`
- `GameRendererMixin.java`
- `GlCommandEncoderMixin.java`
- `CameraMixin.java`
- `gta/src/compositor.cpp`
- `gta/shaders/MCPassthrough.fx`
- `gta/fetch_deps.sh` and `install.sh`

SkyCraft/FalloutCraft native host reference:
- `f4se/src/Overlay.cpp`
- `f4se/src/WorldRender.cpp`
- `f4se/src/Launcher.cpp`
- `protocol/falloutcraft_protocol.h`

### What the source audit established

- SkyCraft/FalloutCraft can hide Minecraft because Fallout has a native D3D11 renderer that consumes
  Minecraft data in Fallout's render pipeline.
- Universal Modder's working generic passthrough does not rebuild the guest world as host-native Unity meshes.
  It exports Minecraft world RGBA + depth before the hand, clears colour, then exports hand/HUD/screens
  separately and composites those three buffers against the host's real depth.
- Universal Modder explicitly keeps Minecraft's render window open for the passthrough proof because minimized
  rendering slows/stalls.
- Minecraft 26.3 depth readback requires restoring GL_COLOR_ATTACHMENT0 after a depth copy; the working example
  contains an explicit GlCommandEncoder mixin for that issue.
- Therefore the active Subnautica visual path must follow the proven framebuffer/depth compositor architecture,
  not the earlier Unity OnGUI/section-mesh experiment.

### Implemented replacement

Subnautica/BepInEx:
- added `Local\\SkyCraft_Subnautica_Camera_v1`;
- publishes canonical `MainCamera.camera` pose, roll, vertical FOV, near/far clip, viewport, player pose;
- disabled the experimental `MinecraftRenderBridge`/OnGUI visual consumer in the active plugin;
- SkyCraft state/water/collision/input/items remain active.

Minecraft/Fabric 26.3:
- added source-backed camera reader;
- ported Universal Modder CameraMixin;
- ported world RGBA + float depth + HUD/hand triple-buffer exporter;
- ported GameRenderer capture points;
- ported the exact GlCommandEncoder depth-readback fix;
- restored real Minecraft level rendering in Subnautica compositor mode;
- legacy SkyCraft WorldExporter/old overlay capture are bypassed in compositor mode;
- removed hide/off-screen-opacity behavior for the source-backed proof path.

Native Subnautica compositor:
- added standalone ReShade `.addon64`;
- pinned compile target to ReShade **6.8.0**, exactly matching Universal Modder;
- ported the working world/depth/HUD upload and camera-reprojection logic;
- ported/adapted `MCPassthrough.fx` as `MinecraftSubnautica.fx`;
- uses standard ReShade D3D11 `dxgi.dll` route;
- safe PowerShell installer opens the official ReShade 6.8.0 Add-on installer when the runtime is absent and
  does not silently replace an existing ReShade.ini.

### Verification

GREEN:
- current Subnautica GameLib/Nautilus BepInEx build with MainCamera channel;
- current Minecraft 26.3 / Java 25 / Fabric build with exact passthrough mixins/exporter;
- standalone `MinecraftSubnautica.addon64` MSVC build against pinned ReShade 6.8.0 headers;
- compositor artifact packaging;
- existing state/water/input/item/collision smoke tests.

Source-backed test bundle:
- `MinecraftSubnautica-SOURCE-BACKED-PASSTHROUGH.zip`
- bundle SHA-256: `8f181fac067d811dc57ae8408fc70362fa803b532b2f15fab1bbe23c66b6c7f7`
- JAR SHA-256: `c80ee7ad0828592d38fb9c5566d1d4088a4ab8e50c7620799212f6c3f930681c`
- BepInEx DLL SHA-256: `0c67140adef6fc1a1116265e9d3a52359425ce48d95004c1f23183fe4688faab`
- ReShade add-on SHA-256: `12c905df876e17a228f26a9b47766de80e3bc5f69ebf61e65657329f57780c2e`


### 2026-10-04 11:39 — Java 25 FFM startup crash fixed

Crash report:
- `java.lang.ExceptionInInitializerError`
- cause: `java.lang.IllegalArgumentException: Unsupported layout: 1%i4`
- origin: `dev.skycraft.client.SubnauticaCameraLink.<clinit>`

Root cause:
- the packed shared-memory layouts `JAVA_INT_UNALIGNED` / `JAVA_LONG_UNALIGNED` were
  accidentally reused in Win32 Foreign Function & Memory downcall descriptors;
- Java 25 accepts the unaligned layouts for packed memory access, but rejects them as native ABI
  function parameter/return layouts.

Fix:
- keep unaligned layouts for shared-memory fields;
- use canonical aligned `JAVA_INT` / `JAVA_LONG` exclusively in
  `OpenFileMappingW`, `MapViewOfFile`, and `GetTickCount64` descriptors.

Commit: `9805000ec6ce6a6c635f1c31a34232bf3deb5808`

Verification:
- Minecraft Subnautica SkyCraft 26.3 CI build passed after the fix.
