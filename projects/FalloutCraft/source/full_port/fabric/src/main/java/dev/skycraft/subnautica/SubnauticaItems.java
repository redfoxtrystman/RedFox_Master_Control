package dev.skycraft.subnautica;

import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;

/** Minecraft-side proxy items whose authoritative mutable state originates in Subnautica. */
public final class SubnauticaItems {
	public static final String TRANSFER_ID = "skycraft_subnautica_transfer_id";
	public static final String ORIGIN_ID = "skycraft_subnautica_origin_id";
	public static final String ENERGY = "skycraft_subnautica_energy";
	public static final String MAX_ENERGY = "skycraft_subnautica_max_energy";
	public static final String STATE_JSON = "skycraft_subnautica_state_json";
	public static final String PENDING_RETURN = "skycraft_subnautica_pending_return";

	public static final Item SEAGLIDE = register("seaglide");

	private SubnauticaItems() {
	}

	public static void init() {
		// Class initialization performs registration.
	}

	private static Item register(String name) {
		Identifier id = Identifier.fromNamespaceAndPath("skycraft", name);
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
		Item item = new Item(new Item.Properties().setId(key).stacksTo(1));
		return Registry.register(BuiltInRegistries.ITEM, id, item);
	}

	public static ItemStack createSeaglide(long transferId, String originId, float energy, float maxEnergy, String stateJson) {
		ItemStack stack = new ItemStack(SEAGLIDE);
		CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> {
			tag.putLong(TRANSFER_ID, transferId);
			tag.putString(ORIGIN_ID, originId == null ? "subnautica:Seaglide" : originId);
			tag.putFloat(ENERGY, energy);
			tag.putFloat(MAX_ENERGY, maxEnergy);
			tag.putString(STATE_JSON, stateJson == null ? "" : stateJson);
			tag.putBoolean(PENDING_RETURN, false);
		});
		return stack;
	}

	public static long transferId(ItemStack stack) {
		if (stack.isEmpty() || stack.getItem() != SEAGLIDE) {
			return 0L;
		}
		CompoundTag tag = data(stack);
		return tag.getLong(TRANSFER_ID).orElse(0L);
	}

	public static String originId(ItemStack stack) {
		CompoundTag tag = data(stack);
		return tag.getString(ORIGIN_ID).orElse("subnautica:Seaglide");
	}

	public static float energy(ItemStack stack) {
		CompoundTag tag = data(stack);
		return tag.getFloat(ENERGY).orElse(0.0F);
	}

	public static float maxEnergy(ItemStack stack) {
		CompoundTag tag = data(stack);
		return tag.getFloat(MAX_ENERGY).orElse(0.0F);
	}

	public static String stateJson(ItemStack stack) {
		CompoundTag tag = data(stack);
		return tag.getString(STATE_JSON).orElse("");
	}

	public static boolean pendingReturn(ItemStack stack) {
		CompoundTag tag = data(stack);
		return tag.getBoolean(PENDING_RETURN).orElse(false);
	}

	public static void setEnergy(ItemStack stack, float energy) {
		CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putFloat(ENERGY, Math.max(0.0F, energy)));
	}

	public static void setPendingReturn(ItemStack stack, boolean pending) {
		CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putBoolean(PENDING_RETURN, pending));
	}

	private static CompoundTag data(ItemStack stack) {
		return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
	}
}
