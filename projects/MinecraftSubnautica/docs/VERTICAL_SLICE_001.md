# Vertical Slice 001 — Subnautica water drives real Minecraft swimming

## Goal

Prove the architecture with the smallest meaningful cross-game loop:

**Subnautica environment -> SkyCraft protocol -> Minecraft vanilla fluid behavior -> Minecraft authoritative player state -> Subnautica host.**

## Existing SkyCraft pieces reused

The Fabric side already has:

- configurable mapping name via `-Dskycraft.link=...`
- protocol magic/version validation
- host and Minecraft heartbeats
- host `SkyState` read
- Minecraft `McState` write
- `WaterGrid` read
- water surface values represented per X/Z column

For the first slice we do not rename the old protocol fields. The byte layout is already proven. Host-neutral naming happens in the new C# wrapper.

## Launch contract

Subnautica side creates:

`Local\SkyCraft_Subnautica_v1`

Minecraft must launch with:

`-Dskycraft.link=Local\\SkyCraft_Subnautica_v1`

Both sides stay on protocol v11 for this slice.

## Subnautica adapter responsibilities

Each host update:

1. pulse the host heartbeat;
2. obtain the current Subnautica player position;
3. convert it to Minecraft block coordinates;
4. write `HostState`;
5. sample water around the player and write the 16x16 water grid;
6. read `MinecraftState`;
7. when takeover is active, puppet the Subnautica player/camera from Minecraft state.

## Coordinate policy

Subnautica/Unity and Minecraft are both Y-up and use meter-scale worlds, so the initial scale is **1 Unity unit = 1 Minecraft block**.

Axis signs and yaw offset are not hard-coded as fact yet. Universal Modder recon must verify them in game with a calibration test before full takeover.

## Water policy

The bridge exports *environment facts*, not Minecraft mechanics.

The Subnautica adapter answers:

- is this X/Z column water-backed?
- where is the water surface?
- later: where are local air pockets, flooded interiors, moonpools, alien-base dry spaces, caves, and special volumes?

Minecraft remains responsible for:

- entering swimming pose;
- water movement;
- oxygen depletion;
- drowning damage;
- enchantments;
- aquatic mob behavior;
- zombie underwater conversion;
- every other vanilla rule driven by fluid state.

## First test

1. Stand in open Subnautica ocean.
2. Start the SkyCraft Minecraft client on the Subnautica mapping.
3. Confirm both heartbeats.
4. Confirm water grid is non-empty.
5. Confirm Minecraft reports `MC_SWIMMING` when submerged.
6. Confirm oxygen/drowning follows Minecraft rules.
7. Spawn/use a Minecraft zombie in the mirror simulation.
8. Keep it submerged using only Subnautica-provided water.
9. Confirm Minecraft itself converts it to drowned.

That final test is the architectural proof: there must be no C# "convert zombie to drowned" code.

## After this passes

- collision streaming from Subnautica colliders/terrain;
- input forwarding;
- camera ownership;
- creature proxies;
- cross-game item schema;
- battery/charge state;
- usable Seaglide in Minecraft water;
- oxygen tanks and fins;
- Minecraft weapons against Subnautica creatures;
- bidirectional containers/inventory;
- vehicles;
- persistence and save coupling.
