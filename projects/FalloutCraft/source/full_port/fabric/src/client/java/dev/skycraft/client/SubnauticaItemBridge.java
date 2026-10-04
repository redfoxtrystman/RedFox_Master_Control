package dev.skycraft.client;

import dev.skycraft.SkyCraft;
import dev.skycraft.link.CrossGameItemLink;
import dev.skycraft.subnautica.SubnauticaItems;
import java.util.UUID;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;

/**
 * Client/runtime glue for Subnautica-origin items.
 *
 * The first proven item is the Seaglide. Its movement constants and energy drain mirror Subnautica:
 * forward 25 m/s, backward/strafe 5 m/s, underwater acceleration 20 * 1.45 m/s^2,
 * and 0.1 energy per second while actively propelling.
 */
public final class SubnauticaItemBridge {
	private static final int SC_W = 26;
	private static final int SC_A = 4;
	private static final int SC_S = 22;
	private static final int SC_D = 7;
	private static final int SC_R = 21;

	private static final double TICKS_PER_SECOND = 20.0;
	private static final double FORWARD_SPEED_PER_TICK = 25.0 / TICKS_PER_SECOND;
	private static final double OTHER_SPEED_PER_TICK = 5.0 / TICKS_PER_SECOND;
	private static final double ACCEL_PER_TICK = (20.0 * 1.45) / (TICKS_PER_SECOND * TICKS_PER_SECOND);
	private static final float ENERGY_PER_SECOND = 0.1F;

	private static boolean returnKeyWasDown;
	private static long lastEnergyDrainTick = Long.MIN_VALUE;

	private SubnauticaItemBridge() {
	}

	public static void tick(Minecraft minecraft) {
		CrossGameItemLink.poll();
		drainIncoming(minecraft);

		LocalPlayer player = minecraft.player;
		if (player == null || minecraft.level == null) {
			returnKeyWasDown = false;
			return;
		}

		ItemStack held = player.getMainHandItem();
		boolean isSeaglide = held.getItem() == SubnauticaItems.SEAGLIDE;
		if (!isSeaglide) {
			returnKeyWasDown = InputBridge.isKeyDown(SC_R);
			return;
		}

		if (SubnauticaItems.pendingReturn(held)) {
			returnKeyWasDown = InputBridge.isKeyDown(SC_R);
			return;
		}

		boolean returnDown = InputBridge.isKeyDown(SC_R);
		if (returnDown && !returnKeyWasDown) {
			returnToSubnautica(minecraft, held);
		}
		returnKeyWasDown = returnDown;

		if (SubnauticaItems.pendingReturn(held)) {
			return;
		}

		float energy = SubnauticaItems.energy(held);
		if (energy <= 0.0F || !player.isInWater()) {
			return;
		}

		double forwardInput = (InputBridge.isKeyDown(SC_W) ? 1.0 : 0.0) - (InputBridge.isKeyDown(SC_S) ? 1.0 : 0.0);
		double strafeInput = (InputBridge.isKeyDown(SC_D) ? 1.0 : 0.0) - (InputBridge.isKeyDown(SC_A) ? 1.0 : 0.0);
		if (forwardInput == 0.0 && strafeInput == 0.0) {
			return;
		}

		Vec3 look = player.getLookAngle();
		Vec3 forward = new Vec3(look.x, 0.0, look.z);
		if (forward.lengthSqr() < 1.0e-8) {
			return;
		}
		forward = forward.normalize();
		Vec3 right = new Vec3(-forward.z, 0.0, forward.x);

		Vec3 wish = forward.scale(forwardInput).add(right.scale(strafeInput));
		if (wish.lengthSqr() < 1.0e-8) {
			return;
		}
		wish = wish.normalize();

		double targetSpeed = forwardInput > 0.0 ? FORWARD_SPEED_PER_TICK : OTHER_SPEED_PER_TICK;
		Vec3 current = player.getDeltaMovement();
		Vec3 currentHorizontal = new Vec3(current.x, 0.0, current.z);
		Vec3 targetHorizontal = wish.scale(targetSpeed);
		Vec3 delta = targetHorizontal.subtract(currentHorizontal);
		double deltaLength = delta.length();
		if (deltaLength > ACCEL_PER_TICK) {
			delta = delta.scale(ACCEL_PER_TICK / deltaLength);
		}

		Vec3 nextHorizontal = currentHorizontal.add(delta);
		player.setDeltaMovement(nextHorizontal.x, current.y, nextHorizontal.z);

		long tick = minecraft.level.getGameTime();
		if (lastEnergyDrainTick == Long.MIN_VALUE) {
			lastEnergyDrainTick = tick;
		}
		if (tick - lastEnergyDrainTick >= 20L) {
			lastEnergyDrainTick = tick;
			float nextEnergy = Math.max(0.0F, energy - ENERGY_PER_SECOND);
			SubnauticaItems.setEnergy(held, nextEnergy);
			syncEnergyToServer(minecraft, SubnauticaItems.transferId(held), nextEnergy);
			sendState(held, CrossGameItemLink.OP_UPDATE);
		}
	}

	private static void drainIncoming(Minecraft minecraft) {
		if (!CrossGameItemLink.active()) {
			return;
		}

		for (int i = 0; i < 32; i++) {
			CrossGameItemLink.Item item = CrossGameItemLink.tryReceiveFromHost();
			if (item == null) {
				break;
			}

			if (item.operation == CrossGameItemLink.OP_TRANSFER && "subnautica:Seaglide".equalsIgnoreCase(item.itemId)) {
				addSeaglide(minecraft, item);
			} else if (item.operation == CrossGameItemLink.OP_REMOVE) {
				removeByTransferId(minecraft, item.transferId, false);
			}
		}
	}

	private static void addSeaglide(Minecraft minecraft, CrossGameItemLink.Item item) {
		MinecraftServer server = minecraft.getSingleplayerServer();
		LocalPlayer local = minecraft.player;
		if (server == null || local == null) {
			return;
		}

		UUID uuid = local.getUUID();
		ItemStack stack = SubnauticaItems.createSeaglide(
			item.transferId,
			item.itemId,
			item.energy,
			item.maxEnergy,
			item.stateJson
		);

		server.execute(() -> {
			ServerPlayer player = server.getPlayerList().getPlayer(uuid);
			if (player == null) {
				compensateHost(item, CrossGameItemLink.OP_REMOVE);
				return;
			}

			if (findByTransferId(player, item.transferId) >= 0) {
				SkyCraft.LOG.warn("SkyCraft: ignored duplicate Subnautica transfer {}", item.transferId);
				return;
			}

			boolean added = player.getInventory().add(stack);
			if (!added) {
				compensateHost(item, CrossGameItemLink.OP_REMOVE);
				SkyCraft.LOG.warn("SkyCraft: Minecraft inventory full; cancelled Subnautica transfer {}", item.transferId);
				return;
			}

			SkyCraft.LOG.info(
				"SkyCraft proof: received Subnautica Seaglide transfer {} at {}/{} energy",
				item.transferId, item.energy, item.maxEnergy
			);
		});
	}

	private static void returnToSubnautica(Minecraft minecraft, ItemStack held) {
		MinecraftServer server = minecraft.getSingleplayerServer();
		if (server == null || minecraft.player == null || !CrossGameItemLink.active()) {
			return;
		}

		long transferId = SubnauticaItems.transferId(held);
		if (transferId == 0L) {
			return;
		}

		CrossGameItemLink.Item item = fromStack(held, CrossGameItemLink.OP_TRANSFER);
		if (!CrossGameItemLink.trySendToHost(item)) {
			SkyCraft.LOG.warn("SkyCraft: couldn't return Seaglide {}; item channel is full", transferId);
			return;
		}

		SubnauticaItems.setPendingReturn(held, true);
		UUID uuid = minecraft.player.getUUID();
		server.execute(() -> {
			ServerPlayer player = server.getPlayerList().getPlayer(uuid);
			if (player == null || !removeFromInventory(player, transferId)) {
				// The host may already have restored the item. Cancel that exact transfer.
				compensateHost(item, CrossGameItemLink.OP_REMOVE);
				SkyCraft.LOG.error("SkyCraft: failed to remove returned Seaglide {}; sent compensation", transferId);
				return;
			}
			SkyCraft.LOG.info("SkyCraft proof: returned Subnautica Seaglide transfer {}", transferId);
		});
	}

	private static void syncEnergyToServer(Minecraft minecraft, long transferId, float energy) {
		MinecraftServer server = minecraft.getSingleplayerServer();
		if (server == null || minecraft.player == null || transferId == 0L) {
			return;
		}
		UUID uuid = minecraft.player.getUUID();
		server.execute(() -> {
			ServerPlayer player = server.getPlayerList().getPlayer(uuid);
			if (player == null) {
				return;
			}
			int slot = findByTransferId(player, transferId);
			if (slot >= 0) {
				SubnauticaItems.setEnergy(player.getInventory().getItem(slot), energy);
			}
		});
	}

	private static void removeByTransferId(Minecraft minecraft, long transferId, boolean compensateOnFailure) {
		MinecraftServer server = minecraft.getSingleplayerServer();
		if (server == null || minecraft.player == null || transferId == 0L) {
			return;
		}
		UUID uuid = minecraft.player.getUUID();
		server.execute(() -> {
			ServerPlayer player = server.getPlayerList().getPlayer(uuid);
			if (player != null) {
				removeFromInventory(player, transferId);
			}
		});
	}

	private static boolean removeFromInventory(ServerPlayer player, long transferId) {
		int slot = findByTransferId(player, transferId);
		if (slot < 0) {
			return false;
		}
		player.getInventory().setItem(slot, ItemStack.EMPTY);
		return true;
	}

	private static int findByTransferId(ServerPlayer player, long transferId) {
		for (int i = 0; i < player.getInventory().getContainerSize(); i++) {
			ItemStack stack = player.getInventory().getItem(i);
			if (stack.getItem() == SubnauticaItems.SEAGLIDE && SubnauticaItems.transferId(stack) == transferId) {
				return i;
			}
		}
		return -1;
	}

	private static void sendState(ItemStack stack, int operation) {
		if (!CrossGameItemLink.active()) {
			return;
		}
		CrossGameItemLink.trySendToHost(fromStack(stack, operation));
	}

	private static CrossGameItemLink.Item fromStack(ItemStack stack, int operation) {
		CrossGameItemLink.Item item = new CrossGameItemLink.Item();
		item.transferId = SubnauticaItems.transferId(stack);
		item.operation = operation;
		item.origin = CrossGameItemLink.ORIGIN_SUBNAUTICA;
		item.flags = CrossGameItemLink.FLAG_TOOL | CrossGameItemLink.FLAG_HAS_ENERGY;
		item.count = 1;
		item.maxStack = 1;
		item.energy = SubnauticaItems.energy(stack);
		item.maxEnergy = SubnauticaItems.maxEnergy(stack);
		item.itemId = SubnauticaItems.originId(stack);
		item.displayName = "Seaglide";
		item.stateJson = SubnauticaItems.stateJson(stack);
		return item;
	}

	private static void compensateHost(CrossGameItemLink.Item source, int operation) {
		CrossGameItemLink.Item compensation = new CrossGameItemLink.Item();
		compensation.transferId = source.transferId;
		compensation.operation = operation;
		compensation.origin = source.origin;
		compensation.flags = source.flags;
		compensation.count = source.count;
		compensation.maxStack = source.maxStack;
		compensation.energy = source.energy;
		compensation.maxEnergy = source.maxEnergy;
		compensation.durability = source.durability;
		compensation.maxDurability = source.maxDurability;
		compensation.itemId = source.itemId;
		compensation.displayName = source.displayName;
		compensation.stateJson = source.stateJson;
		CrossGameItemLink.trySendToHost(compensation);
	}
}
