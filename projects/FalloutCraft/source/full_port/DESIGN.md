# FalloutCraft — Design Doc

> Play Fallout 4 as the main game while *being* a Minecraft player: real Minecraft movement physics, inventory, items, block placing, and combat, inside the real Fallout 4 world, able to fight and talk to Fallout 4 NPCs.

Status: draft v0.1 · 2026-09-29

---

## 1. Core principle

**Neither game is rewritten.** Minecraft runs its own, unmodified game logic: movement, collision resolution, combat math, inventory, crafting, block logic, rendering of items and hands. Fallout 4 runs its own world: terrain, buildings, NPCs, AI, quests, dialogue, saves.

The two mods only **translate** between them:

- Fallout 4 tells Minecraft *what the world is shaped like* and *where the NPCs are*.
- Minecraft tells Fallout 4 *where the player is*, *what the player hit*, and *what to draw on top*.

If we ever find ourselves re-implementing a Minecraft mechanic in C++ or a Fallout 4 mechanic in Java, the design has gone wrong.

## 2. Target environment

| Thing | Value | Notes |
|---|---|---|
| Fallout 4 | **Anniversary Edition runtime** (developed on 1.7.104) | F4SE64 + Address Library |
| Mod manager | MO2 or Vortex | The plugin installs like any F4SE plugin |
| Minecraft | **26.3 + Fabric** (fabric-api 0.161.0+26.3) | 26.x ships unobfuscated, so Mixins target Mojang names directly |
| Java | 25 | Minecraft 26.x needs it |
| C++ toolchain | Visual Studio 2026, CMake, Git | |

Development happens against a **clean Fabric 26.3 dev environment** (Loom `runClient`), not a modpack. Sodium and friends replace the renderer, so compat with them comes later (§12).

## 3. Components

```
┌──────────────────── Fallout 4.exe ────────────────────┐        ┌──────────────── javaw.exe (Minecraft 26.3) ────────────────┐
│  falloutcraft.dll  (F4SE plugin, CommonLibSSE-NG)       │        │  falloutcraft (Fabric mod)                                     │
│                                                     │        │                                                            │
│  WorldExporter   ─ Fallout 4 collision near player ────┼──────▶ │  CollisionField  → injected into MC collision queries      │
│  ActorMirror     ─ nearby NPCs (pos, box, state) ───┼──────▶ │  ActorProxy entities (invisible, hittable)                │
│  InputBridge     ─ raw keyboard/mouse ──────────────┼──────▶ │  input handlers (as if MC window had focus)                │
│  HitBridge       ─ "NPC hit player for X" ──────────┼──────▶ │  player.hurt(falloutcraft:skyrim_* damage source)              │
│                                                     │        │                                                            │
│  PlayerPuppet    ◀─ player pos / look / pose ───────┼─────── │  real MC LocalPlayer physics                               │
│  CameraDriver    ◀─ view + projection matrix ───────┼─────── │  GameRenderer camera                                       │
│  DamageApplier   ◀─ "you hit NPC 0x1A2B3 for X" ────┼─────── │  ActorProxy.hurt() hook                                    │
│  Compositor      ◀─ color+depth textures (GPU) ─────┼─────── │  offscreen render: world layer / hand layer / GUI layer    │
└─────────────────────────────────────────────────────┘        └────────────────────────────────────────────────────────────┘
                         shared memory (Local\FalloutCraft_v1) + named events + shared GPU textures
```

Plus one small shared piece: **`protocol/`**, the message schema used by both sides (§10).

## 4. Coordinate mapping

Fallout 4 is Z-up and Minecraft is Y-up. Scale is **1 block = 70 Fallout 4 units** (≈1 m). This works out neatly because the MC player is 1.8 blocks tall and the Fallout 4 player is about 128 units.

```
mc.x =  sky.x / 70
mc.y =  sky.z / 70
mc.z = -sky.y / 70          (Fallout 4 +Y is north; MC -Z is north)
mc.yaw   = f(sky.rotZ)      (exact sign/offset pinned down in Phase 0 with a test)
mc.pitch = f(sky.rotX)
```

- **Vertical range:** Fallout 4 terrain spans more than 384 blocks (the Throat of the World is well above MC's default build height). The mirror world therefore uses a **custom `dimension_type`** with an expanded range (up to min_y −2032 / height 4064).
- **Worldspaces:** each Fallout 4 worldspace (Tamriel, Solstheim, etc.) maps to its own MC dimension.
- **Interiors:** interior cells live in one `falloutcraft:interiors` dimension. Each interior cell gets its own 1024×1024 region slot, allocated by FormID.
- Changing cell or worldspace in Fallout 4 (load doors) moves the MC player to the matching dimension or slot.

## 5. The mirror world (Minecraft side)

The MC mod runs a normal singleplayer world ("mirror world") with these properties:

- **Void generator:** there are no MC blocks at all except the ones the player places.
- `doMobSpawning false`, `doWeatherCycle false`, `doDaylightCycle false`. Time and weather are driven from Fallout 4.
- The integrated server runs normally. Physics runs on the client as usual in MC. Because collision injection is common code, the server's movement validation sees the same world and won't rubber-band the player.

### 5.1 CollisionField: how Fallout 4's shape reaches MC physics

MC's movement code (`Entity.collide` and friends) asks the level for collision shapes (`VoxelShape`s, which are unions of AABBs) along the movement path. A Mixin appends **extra shapes from the CollisionField** to that query. MC's own collision resolution, step-up, gravity, sprint-jumping, sneaking-at-edges and so on then run completely unchanged against those shapes.

- The field is a sparse store of AABBs, bucketed per 16³ section, at **1/8-block resolution** (8.75 units).
- These shapes are **not blocks**. They don't occupy the block grid, so player blocks can be placed next to or on top of Fallout 4 geometry freely.
- **Slopes** become 1/8-block micro-steps. Each one is well under MC's 0.6 step height, so walking up a hill is effectively smooth. The Fallout 4 camera may apply *visual-only* Y smoothing; physics is untouched.
- **Steep surfaces:** to stop the player strolling up cliffs, the exporter raises any cell whose surface normal is steeper than a threshold (~50°, matching Fallout 4's walkable slope) into a full wall column. MC's step-up rule then refuses it naturally. This is a data decision, not a physics change.

**Where the data comes from (Fallout 4 side, WorldExporter):**

| Stage | Method | Covers | Cost |
|---|---|---|---|
| A: MVP | Havok ray casts on a grid around the player (≈48-block radius, refined near the player, amortized over frames), multi-hit per column for overhangs | Terrain, most statics | Cheap; misses thin geometry |
| C: final | Walk the loaded `bhkWorld`, read the actual shapes (heightfields, compressed meshes, boxes/capsules), voxelize on a worker thread | Everything, including mod-added content and opened doors | Complex (Havok shape decoding) but exact |

Data streams as deltas per section. MC keeps a ring around the player and evicts far sections.

### 5.2 Water

Later: a Mixin on fluid-state queries reports `water` inside Fallout 4 water volumes. MC's swimming physics then applies unchanged.

## 6. The player

**Minecraft is authoritative for player position and physics.**

1. Each MC render frame, the mod sends `PlayerState`:
   - the interpolated position and look (MC's partial-tick render position, not the raw 20 TPS tick position)
   - pose (standing, sneaking, swimming, flying) and on-ground
   - the full **view matrix, including view bob**, plus the projection/FOV
2. The Fallout 4 plugin (**PlayerPuppet**):
   - disables the player's own movement (character controller input), and
   - moves the `PlayerCharacter` reference and its Havok capsule to that position every frame.

   The Fallout 4 player ref stays in the world as a **puppet**. That keeps NPC AI targeting, detection and stealth, trigger volumes, quest location checks, and projectiles hitting the player working.
3. **CameraDriver** forces Fallout 4 first person and overwrites the camera with MC's view and projection. MC's FOV is vertical and Fallout 4's is effectively horizontal, so it converts between them. The Fallout 4 player body and arms are hidden.

## 7. Input

- The Fallout 4 window has OS focus. **InputBridge** reads raw input through Fallout 4's input device manager, **swallows it from Fallout 4's controls**, and forwards it to MC's `KeyboardHandler` / `MouseHandler` through Mixin entry points.
- The MC window is hidden but told it is focused, so it doesn't pause or release the mouse.
- **Routing modes:**
  - **Gameplay:** input goes to MC. Fallout 4 receives only a small allow-list: Esc for the Fallout 4 journal/system menu, and the Fallout 4 "Activate" route described below.
  - **MC screen open** (inventory, crafting, chest): input goes to MC and the MC cursor is shown in the overlay.
  - **Fallout 4 menu open** (dialogue, barter, lockpicking, map, loading screen): input goes to Fallout 4 and the MC client is frozen.
- **"Use" arbitration:** when you press MC's use key, both sides pick a target:
  - MC's ray pick (blocks and actor proxies)
  - Fallout 4's crosshair pick (doors, containers, NPCs to talk to, items)

  The **nearest target wins**. A Fallout 4 target becomes a Fallout 4 `Activate`. That is how you open doors, loot, and start dialogue.

## 8. Combat

### 8.1 Fallout 4 NPCs inside Minecraft: ActorProxy

For every Fallout 4 actor within ~64 blocks, the MC server spawns a `falloutcraft:actor_proxy` entity:

- **Invisible**, because Fallout 4 draws the real NPC.
- Its **hitbox** comes from the actor's bound or race dimensions and updates each tick; position and rotation are interpolated.
- It carries the actor's FormID, a mirrored health fraction, and hostility, essential and dead flags.
- Proxies are real `LivingEntity`s. Your sword swing, attack cooldown, crits, sweeping edge, Sharpness, Fire Aspect, knockback, arrows, tridents and splash potions all work on them **with vanilla MC code**.

### 8.2 You hit an NPC

1. Vanilla MC computes the final damage on the proxy (`hurt` / actuallyHurt path).
2. The mod intercepts the result, keeps the proxy alive (it isn't the real NPC), and sends `HitActor {formId, damage, knockback, isCrit, sourceItem, fireTicks}`.
3. **DamageApplier** in Fallout 4 applies it through the game's own hit pipeline, so the NPC reacts properly: hit reaction and stagger, blood, sounds, aggro, and **crime/assault** if they're a citizen. The exact function will be found with RE (Ghidra is available).
   - Fallback: `DamageActorValue(Health)`, then an assault alarm, then a stagger animation event.
   - Knockback becomes a Havok impulse.
4. **Damage scaling is an open decision (§13).** A diamond sword does 7, while a Fallout 4 bandit has 50–300 HP.

### 8.3 An NPC hits you

1. Fallout 4's hit on the player puppet (melee, arrow, spell) is caught in a hook and **cancelled on the Fallout 4 side**.
2. The plugin sends `PlayerHurt {amount, type, sourceFormId, direction}`.
3. MC applies `player.hurt()` with custom damage types (`falloutcraft:skyrim_melee`, `skyrim_arrow`, `skyrim_magic`). Armor, Protection, shields and blocking, totems, i-frames and knockback are all vanilla MC.
4. **MC health is authoritative.** Fallout 4's player health is mirrored as a fraction so NPC behaviour (fleeing, finishers) still reads sensibly.
   - MC death means the Fallout 4 player is killed, and Fallout 4's normal death/reload flow runs.
   - Fall damage is MC's own.

## 9. Rendering

Fallout 4 renders the world. MC renders **only its own stuff** offscreen at Fallout 4's resolution, using the camera Fallout 4 is about to use, in three layers:

| Layer | Contents | Composited |
|---|---|---|
| **World** | Placed blocks, block entities (chests), dropped items, arrows, particles. Sky, clouds and fog are off; transparent clear | Mid-frame, **depth-tested against Fallout 4's depth buffer**, so Fallout 4 walls correctly hide your blocks and vice versa |
| **Hand** | First-person arm and held item, including MC's swing, equip and eat animations | After Fallout 4's scene, before the HUD |
| **GUI** | Hotbar, hearts, hunger, XP, crosshair, and every open MC screen | On top of everything |

- **Transport:** the color and depth textures are shared on the GPU. How depends on which renderer MC 26.3 actually uses, which needs checking:
  - **OpenGL:** `WGL_NV_DX_interop2` onto D3D11 shared textures.
  - **Vulkan:** `VK_KHR_external_memory_win32` importing D3D11 shared NT handles, plus a shared fence.
  - **Fallback:** PBO readback and upload, which costs about one frame of latency.
- **Frame lockstep:** MC's own frame cap and vsync are disabled.
  1. Fallout 4 signals "begin frame N" with the camera.
  2. Both games render in parallel.
  3. Fallout 4 waits, with a timeout, on MC's "frame N ready" fence before compositing.
  4. If MC misses the deadline, Fallout 4 reuses frame N−1.
- **Lighting:** MC `dayTime` is driven from Fallout 4's `GameHour`, and MC weather follows Fallout 4's (rain/snow → rain). That keeps block shading roughly in line with the scene.
- **Fallout 4 depth format and hook points** (after the scene, before post-processing and Scaleform) get pinned down with RenderDoc in Phase 2. ENB compatibility is a stretch goal.

## 10. Protocol / IPC

- **Shared memory** `Local\FalloutCraft_v1` holds:
  - a **header**: magic, protocol version, both PIDs, heartbeats
  - **latest-value slots** under a seqlock, for per-frame data: `PlayerState`, `CameraState`, `FrameSync`
  - **two SPSC ring buffers** (Fallout 4→MC and MC→Fallout 4) for events
- **Named events** handle wakeups; heartbeats detect crashes. If either side dies, the other drops to a safe state: Fallout 4 restores normal control, MC pauses.
- **Schema:** it lives once in `protocol/messages.*`. It generates or is mirrored into a C++ header and a Java class, and a layout test runs in CI on both sides. Everything is little-endian with fixed-size structs, so there's no serialization library in the hot path.

Initial message catalog:

| Dir | Message | Rate |
|---|---|---|
| S→M | `Hello / Heartbeat` | 1 Hz |
| S→M | `WorldContext {worldspace/cell, GameHour, weather}` | On change |
| S→M | `CollisionSection {sectionPos, aabbs[]}` / `CollisionEvict` | Streamed |
| S→M | `ActorUpsert {formId, pos, rot, box, hpFrac, flags}` / `ActorRemove` | 20 Hz |
| S→M | `Input {keys, mouse dx/dy, wheel, buttons}` | Per frame |
| S→M | `PlayerHurt {...}` | Event |
| S→M | `BeginFrame {frameId, viewport}` | Per frame |
| S→M | `SaveRequest / LoadRequest {saveId}` | Event |
| M→S | `PlayerState {pos, look, pose, onGround, viewMtx, projMtx}` | Per frame |
| M→S | `HitActor {...}` / `UseTarget {...}` | Event |
| M→S | `BlockChange {pos, stateId}` (for Fallout 4-side NPC collision) | Event |
| M→S | `FrameReady {frameId}` | Per frame |
| M→S | `MenuState {mcScreenOpen}` | On change |

## 11. Other systems

- **NPCs vs placed blocks:** MC blocks are real in MC, but Fallout 4 NPCs need to collide with your builds too. The plugin keeps Fallout 4-side collision in sync using `BlockChange`:
  - MVP: invisible collision-only box statics.
  - Final: one merged Havok shape per chunk.
- **Save/load:** F4SE serialization stores a `saveId` in each Fallout 4 save. On save, MC flushes the mirror world and snapshots its (tiny, sparse) region and player data under that id. On load, it restores that snapshot, so loading an old Fallout 4 save also rewinds your builds and inventory consistently.
- **Launching:** the MC client must go through a real launcher for account auth.
  - v1: start the FalloutCraft MC profile first. It waits in standby and Fallout 4 connects on game load.
  - Later: Fallout 4 triggers the launcher automatically.
  - During development, Loom `runClient` is enough.

## 12. Phased plan

Each phase ends in something you can actually play.

| # | Phase | "Done" when |
|---|---|---|
| 0 | **Link** | Both mods handshake over shared memory. The coordinate mapping is unit-tested. Walking in MC (on a temporary flat floor at Fallout 4 ground height) moves the Fallout 4 player |
| 1 | **Walk Fallout 4 in MC physics** | CollisionField stage A, CameraDriver, InputBridge. You can sprint-jump around Whiterun with real MC movement, and slopes and cliffs behave |
| 2 | **Overlay** | Hand and GUI layers composited (CPU path first, then GPU interop). The real MC hotbar and inventory screen work in Fallout 4 |
| 3 | **Combat** | ActorProxy, HitActor, PlayerHurt, health mirroring, death. You can fight a bandit camp with an MC sword and shield |
| 4 | **Blocks** | Place and break blocks on Fallout 4 surfaces, world layer depth-composited, NPCs collide with builds |
| 5 | **Full world** | CollisionField stage C (buildings, interiors, multi-level), water, activation arbitration, load doors across dimensions |
| 6 | **Persistence & polish** | Save snapshots, time/weather sync, Fallout 4 loot → MC items bridge, third person, auto-launch, Sodium compat |

## 13. Decisions (2026-09-29)

1. **Damage scaling:** Claude's call. MC→Fallout 4 damage is multiplied by `5 + 0.25 × NPC level` (a diamond sword crit of ~10 hits a level-10 bandit for ~75). Fallout 4→MC damage is divided by 5, so a 20-damage Fallout 4 hit becomes 4 MC damage (2 hearts). Both are config values.
2. **Fallout 4 HUD:** keep the **compass** and the **Esc (journal/system) menu**. Hide everything else.
3. **Shouts, magic, Fallout 4 inventory, skill leveling:** off or ignored for now.
4. **Loot bridge:** out of scope for now.
5. **Mining Fallout 4 ore veins** for MC ores: parked.

## 14. Risks

| Risk | Mitigation |
|---|---|
| Havok shape extraction (stage C) is hard | Stage A ray-cast field is good enough to ship Phases 1–4 |
| Hit-pipeline function in Fallout 4 needs RE | Ghidra plus CommonLib; the `DamageActorValue` fallback always works |
| GPU interop across GL/Vulkan and D3D11 | CPU fallback path built first |
| Frame lockstep adds latency or stutter | Timeout plus reuse of the previous frame; measure early in Phase 2 |
| Mixin targets shift between MC versions | Pin to 26.3; keep all Mixins in one package with a target list |
| Two games' RAM and GPU cost | MC renders almost nothing (void world, no terrain); cap JVM heap at ~3 GB |

## 15. Repo layout (proposed)

```
falloutcraft/
  docs/DESIGN.md
  protocol/            message schema + generator + layout tests
  skse/                F4SE plugin (CMake, vcpkg, CommonLibSSE-NG, C++23)
  fabric/              Fabric mod (Gradle, Loom, MC 26.3)
  tools/               dev scripts (deploy to MO2, launch both)
```
