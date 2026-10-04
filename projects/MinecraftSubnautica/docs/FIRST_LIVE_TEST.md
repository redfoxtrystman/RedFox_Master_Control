# First live test — Vertical Slice 001

This test proves the core architectural claim:

> Subnautica supplies environmental facts. Minecraft executes Minecraft rules.

No Subnautica-side code is allowed to fake swimming, drowning, or zombie conversion.

## Automated setup

From PowerShell:

```powershell
cd projects\MinecraftSubnautica
.\tools\vertical_slice_001.ps1 -Launch
```

If Subnautica is not in a default Steam/Epic/Xbox-PC location:

```powershell
.\tools\vertical_slice_001.ps1 -GameDir "D:\Games\Subnautica" -Launch
```

The script:

1. builds the plugin against the official current Subnautica/Nautilus packages;
2. installs `MinecraftSubnautica.dll` into BepInEx;
3. launches Subnautica when `-Launch` is supplied;
4. launches the existing SkyCraft Minecraft client using `Local\SkyCraft_Subnautica_v1`.

## Expected connection proof

The Subnautica BepInEx log should contain:

```text
BRIDGE PROOF: Minecraft connected (PID ...)
```

The Minecraft client should automatically open/create the SkyCraft mirror world. SkyCraft's first host state automatically forces an initial teleport because its client starts with an unapplied host teleport sequence.

## Water proof

Start in open ocean. For this first slice, the host water sampler deliberately uses the global Subnautica ocean surface and marks interiors/precursor dry areas as dry.

When Minecraft's own player state changes, the Subnautica log prints:

```text
BRIDGE PROOF: Minecraft swimming=True ...
BRIDGE PROOF: Minecraft swimming=False ...
```

Pass criteria:

- submerged in Subnautica -> Minecraft reports swimming when vanilla conditions are met;
- surface -> Minecraft exits swimming;
- Minecraft water movement is produced by SkyCraft's existing entity-fluid hooks;
- Minecraft oxygen/drowning behavior occurs without a C# drowning implementation.

## Zombie -> drowned proof

The SkyCraft mirror disables natural hostile spawning, so use a normal Minecraft command to create the test zombie.

While the player is in open Subnautica ocean, summon a zombie inside the 16x16 host-water window and below the reported water surface.

Example starting point:

```text
/summon minecraft:zombie ~2 ~-2 ~
```

Keep the zombie inside the host-water window and submerged.

**Pass:** Minecraft itself converts the zombie to a drowned.

**Automatic fail:** any Subnautica/C# bridge code directly replaces a zombie with a drowned.

The bridge may report water and entity/environment state. The conversion belongs to Minecraft.

## Takeover calibration

`MinecraftTakeover` defaults to `false`.

Only after connection/water proof:

1. enable takeover in the BepInEx config;
2. verify +X/+Z direction;
3. verify yaw sign/offset;
4. verify 1 Unity meter = 1 Minecraft block;
5. verify disconnect immediately restores Subnautica's native `PlayerController`.

Takeover currently disables the native player controller only when:

- Minecraft heartbeat is live;
- the user enabled takeover;
- the Subnautica player is in normal on-foot mode;
- no cinematic owns the player.

It is automatically restored on bridge disconnect, mode change, toggle-off, or plugin unload.

## Vertical range

This branch expands the SkyCraft mirror dimension to:

- `min_y = -2032`
- `height = 4064`
- valid Y range: `-2032..2031`

That keeps direct 1:1 vertical mapping viable for Subnautica's deep world rather than introducing a floating-origin transform during the first bridge.
