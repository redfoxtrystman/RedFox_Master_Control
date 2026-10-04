# Vertical Slice 002 — Stateful Subnautica Seaglide inside Minecraft

## Goal

Prove a Subnautica item can cross into Minecraft, remain usable, mutate its native state, and return without becoming an inert copy.

The proof item is the **Seaglide**.

## Transfer contract

A second mapping keeps item traffic independent from SkyCraft protocol v11:

`Local\SkyCraft_Subnautica_Items_v1`

Each item record carries:

- stable transfer ID;
- operation;
- origin game;
- namespaced item ID;
- stack count/max stack;
- energy/max energy;
- durability/max durability;
- item capability flags;
- display name;
- opaque origin-owned state JSON.

The transfer ID is the anti-duplication identity. Both games reject/remove the same transfer ID rather than guessing by item type.

## Subnautica -> Minecraft

1. Minecraft item-channel heartbeat must be live.
2. Player successfully picks up a Seaglide in Subnautica.
3. The Harmony postfix observes the successful `Inventory.Pickup(Pickupable, bool)`.
4. Subnautica serializes the Seaglide and installed battery state.
5. The host->Minecraft ring must accept the transfer before the local item is removed.
6. Minecraft does not consume the ring record until its integrated server and player inventory exist.
7. Minecraft creates one `skycraft:seaglide` carrying the same transfer ID and energy.
8. If Minecraft inventory cannot accept it, Minecraft sends `Remove` compensation and Subnautica reconstructs the outgoing item.

## Minecraft behavior

The Minecraft proxy deliberately uses Subnautica's Seaglide movement/energy rules rather than an arbitrary speed buff.

Current source-of-truth constants used by the bridge:

- forward max speed: **25 m/s**;
- backward max speed: **5 m/s**;
- strafe max speed: **5 m/s**;
- base underwater acceleration: **20 m/s²**;
- Seaglide underwater acceleration multiplier: **1.45**;
- energy drain while active: **0.1 per second**.

Bridge scale for this slice is 1 meter = 1 Minecraft block.

The Seaglide only propels when:

- it is in the main hand;
- Minecraft says the player is in water;
- charge is above zero;
- a horizontal movement key is held.

Vertical motion is intentionally left to Minecraft's real swimming/fluid physics.

## Mutable state

The Minecraft stack stores:

- original transfer ID;
- original namespaced Subnautica ID;
- current energy;
- max energy;
- original state JSON;
- pending-return state.

Every one-second active drain updates the Minecraft stack, the integrated server copy, and sends an `Update` event to Subnautica.

## Minecraft -> Subnautica

For the proof slice, press **R while holding the bridged Seaglide**.

1. Minecraft sends the current item state through the Minecraft->host ring.
2. The local stack is marked pending return so it cannot keep propelling or send a second return.
3. Minecraft removes the exact transfer ID from the authoritative server inventory.
4. Subnautica instantiates the real Seaglide prefab.
5. The real installed battery receives the returned charge.
6. Subnautica picks it into the inventory.
7. If Subnautica inventory is full, the real Seaglide is placed safely in front of the player.
8. If Minecraft fails to remove its local copy, it sends a compensating `Remove`; Subnautica removes/aborts the exact restored transfer.

## Live proof checklist

- [ ] Pick up a charged Seaglide in Subnautica.
- [ ] Subnautica log prints `ITEM BRIDGE PROOF: exported Seaglide...`.
- [ ] One `skycraft:seaglide` appears in Minecraft.
- [ ] No duplicate remains in the Subnautica inventory.
- [ ] Hold it underwater and move forward.
- [ ] Movement is substantially faster forward than backward/strafe.
- [ ] After active use, charge has fallen by 0.1 per second.
- [ ] Press R while holding it.
- [ ] Minecraft stack disappears.
- [ ] Real Seaglide appears back in Subnautica.
- [ ] Returned battery charge equals the Minecraft-side charge.
- [ ] Fill Minecraft inventory and repeat: the transfer is rejected and restored in Subnautica.
- [ ] Fill Subnautica inventory before returning: the Seaglide is dropped safely in front of the player.
- [ ] Disconnect either side: no transfer record is silently consumed before a receiving inventory is ready.

## Visuals

The Minecraft proxy currently uses a vanilla prismarine-shard model as a legal placeholder. No Subnautica game asset is committed to the repository. A later asset-conversion/install step can derive visuals from the user's own game files.

## Not claimed by this slice

This slice does **not** yet claim live-game proof on the user's PC. CI proves both sides compile and the shared-memory item protocol round-trips state. The first local run must prove actual game behavior.

Battery **charge** is preserved now. Alternate installed battery TechType is recorded in the state JSON; exact non-default battery prefab reconstruction is the next item-state extension after this proof.
