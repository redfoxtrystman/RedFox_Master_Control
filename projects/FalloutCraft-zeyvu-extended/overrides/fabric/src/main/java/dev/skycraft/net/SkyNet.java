package dev.skycraft.net;

import dev.skycraft.SkyCraft;
import dev.skycraft.combat.SkyCombat;
import dev.skycraft.world.SkyDig;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.core.BlockPos;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;

/**
 * Multiplayer: every player has their own Skyrim, talking to their own Minecraft client. The host's
 * Skyrim reaches the host's integrated server through shared memory; a guest's Skyrim reaches the
 * host's server through these packets instead.
 */
public final class SkyNet {
	private static final Map<UUID, int[]> SPECIALS = new ConcurrentHashMap<>();

	private SkyNet() {
	}

	/** Guest -> server: the guest's Skyrim hit them (as proto::InputEvent kInHurt). */
	public record Hurt(int kind, float skyrimDamage, int attackerFormId, int flags) implements CustomPacketPayload {
		public static final Type<Hurt> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "hurt"));
		public static final StreamCodec<RegistryFriendlyByteBuf, Hurt> CODEC = StreamCodec.composite(
			ByteBufCodecs.VAR_INT, Hurt::kind,
			ByteBufCodecs.FLOAT, Hurt::skyrimDamage,
			ByteBufCodecs.INT, Hurt::attackerFormId,
			ByteBufCodecs.VAR_INT, Hurt::flags,
			Hurt::new
		);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	/** Guest -> server: the guest's Fallout healed them. Value is Fallout-health percentage share. */
	public record Heal(float falloutHealthShare) implements CustomPacketPayload {
		public static final Type<Heal> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "heal"));
		public static final StreamCodec<RegistryFriendlyByteBuf, Heal> CODEC = StreamCodec.composite(
			ByteBufCodecs.FLOAT, Heal::falloutHealthShare,
			Heal::new
		);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	/** Guest -> server: this guest's own Fallout S.P.E.C.I.A.L. snapshot. */
	public record Special(List<Integer> values) implements CustomPacketPayload {
		public static final Type<Special> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "special"));
		public static final StreamCodec<RegistryFriendlyByteBuf, Special> CODEC = StreamCodec.composite(
			ByteBufCodecs.VAR_INT.apply(ByteBufCodecs.list(7)), Special::values,
			Special::new
		);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	/** Server -> guest: Minecraft activity should award XP in that guest's own Fallout process. */
	public record Activity(int activity, float uses) implements CustomPacketPayload {
		public static final Type<Activity> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "activity"));
		public static final StreamCodec<RegistryFriendlyByteBuf, Activity> CODEC = StreamCodec.composite(
			ByteBufCodecs.VAR_INT, Activity::activity,
			ByteBufCodecs.FLOAT, Activity::uses,
			Activity::new
		);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	/** Server -> guest: the guest died in Minecraft, so their Skyrim player dies too. */
	public record Died(int attackerFormId) implements CustomPacketPayload {
		public static final Type<Died> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "died"));
		public static final StreamCodec<RegistryFriendlyByteBuf, Died> CODEC = StreamCodec.composite(ByteBufCodecs.INT, Died::attackerFormId, Died::new);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	/** Client -> server: the player hit Skyrim's geometry in this cell (SkyDig.open). */
	public record DigOpen(int world, BlockPos pos, int material) implements CustomPacketPayload {
		public static final Type<DigOpen> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "dig_open"));
		public static final StreamCodec<RegistryFriendlyByteBuf, DigOpen> CODEC = StreamCodec.composite(
			ByteBufCodecs.INT, DigOpen::world,
			BlockPos.STREAM_CODEC, DigOpen::pos,
			ByteBufCodecs.VAR_INT, DigOpen::material,
			DigOpen::new
		);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	/** Client -> server: cells around a broken dug block that are inside Skyrim's geometry (SkyDig.reveal). */
	public record DigReveal(int world, List<BlockPos> cells, List<Integer> materials) implements CustomPacketPayload {
		public static final Type<DigReveal> TYPE = new Type<>(Identifier.fromNamespaceAndPath(SkyCraft.MOD_ID, "dig_reveal"));
		public static final StreamCodec<RegistryFriendlyByteBuf, DigReveal> CODEC = StreamCodec.composite(
			ByteBufCodecs.INT, DigReveal::world,
			BlockPos.STREAM_CODEC.apply(ByteBufCodecs.list(64)), DigReveal::cells,
			ByteBufCodecs.VAR_INT.apply(ByteBufCodecs.list(64)), DigReveal::materials,
			DigReveal::new
		);

		@Override
		public Type<? extends CustomPacketPayload> type() {
			return TYPE;
		}
	}

	public static void init() {
		PayloadTypeRegistry.serverboundPlay().register(Hurt.TYPE, Hurt.CODEC);
		PayloadTypeRegistry.serverboundPlay().register(Heal.TYPE, Heal.CODEC);
		PayloadTypeRegistry.serverboundPlay().register(Special.TYPE, Special.CODEC);
		PayloadTypeRegistry.serverboundPlay().register(DigOpen.TYPE, DigOpen.CODEC);
		PayloadTypeRegistry.serverboundPlay().register(DigReveal.TYPE, DigReveal.CODEC);
		ServerPlayNetworking.registerGlobalReceiver(DigOpen.TYPE, (payload, context) -> {
			ServerPlayer player = context.player();
			context.server().execute(() -> SkyDig.open(player, payload.world(), payload.pos(), payload.material()));
		});
		ServerPlayNetworking.registerGlobalReceiver(DigReveal.TYPE, (payload, context) -> {
			ServerPlayer player = context.player();
			int[] materials = payload.materials().stream().mapToInt(Integer::intValue).toArray();
			context.server().execute(() -> SkyDig.reveal(player, payload.world(), payload.cells(), materials));
		});
		PayloadTypeRegistry.clientboundPlay().register(Died.TYPE, Died.CODEC);
		PayloadTypeRegistry.clientboundPlay().register(Activity.TYPE, Activity.CODEC);
		ServerPlayNetworking.registerGlobalReceiver(Hurt.TYPE, (payload, context) -> {
			ServerPlayer player = context.player();
			// A hit's worth of damage, whatever the guest's client claims (friends only, but still).
			float damage = Math.max(0.0F, Math.min(payload.skyrimDamage(), 10000.0F));
			context.server().execute(() -> SkyCombat.hurtPlayer(player, payload.kind(), damage, payload.attackerFormId(), payload.flags()));
		});
		ServerPlayNetworking.registerGlobalReceiver(Heal.TYPE, (payload, context) -> {
			ServerPlayer player = context.player();
			float share = Math.max(0.0F, Math.min(payload.falloutHealthShare(), 100.0F));
			context.server().execute(() -> {
				if (player.isAlive() && share > 0.0F) {
					player.heal(share / SkyCombat.SKYRIM_TO_MC_DAMAGE);
				}
			});
		});
		ServerPlayNetworking.registerGlobalReceiver(Special.TYPE, (payload, context) -> {
			ServerPlayer player = context.player();
			if (payload.values().size() != 7) {
				return;
			}
			int[] values = new int[7];
			for (int k = 0; k < 7; k++) {
				values[k] = Math.max(0, Math.min(payload.values().get(k), 20));
			}
			SPECIALS.put(player.getUUID(), values);
		});
	}

	/** True if this player plays on this machine (their Fallout is on the shared-memory link). */
	public static boolean isHost(ServerPlayer player) {
		var server = player.level().getServer();
		return server != null && server.isSingleplayerOwner(player.nameAndId());
	}

	/** The S.P.E.C.I.A.L. belonging to this Minecraft player, never another player's Fallout stats. */
	public static int[] specialFor(ServerPlayer player) {
		if (isHost(player)) {
			int[] local = dev.skycraft.link.SkyLink.special;
			return local == null ? null : local.clone();
		}
		int[] remote = SPECIALS.get(player.getUUID());
		return remote == null ? null : remote.clone();
	}

	/** Route Fallout-style XP activity to the correct Fallout process. */
	public static void awardActivity(ServerPlayer player, int activity, float uses) {
		if (uses <= 0.0F) {
			return;
		}
		if (isHost(player)) {
			dev.skycraft.link.SkyLink.pushEvent(dev.skycraft.link.Proto.EV_SKILL_USE, activity, uses, 0.0F, 0.0F, 0.0F, 0);
		} else if (ServerPlayNetworking.canSend(player, Activity.TYPE)) {
			ServerPlayNetworking.send(player, new Activity(activity, uses));
		}
	}
}
