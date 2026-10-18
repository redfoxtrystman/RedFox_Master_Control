package com.glaziola.pixelmonrejuvenated;

import java.util.List;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.ChatFormatting;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;

/** Soul orbs store their progress on each ItemStack, not per player. */
public final class BirdOrbItem extends Item {
    public static final int TARGET = 250;
    private static final String KEY = "pixelmonrejuvenated.bird_orb_defeats";
    public BirdOrbItem(Properties properties) { super(properties.stacksTo(1)); }
    public static int progress(ItemStack stack) {
        if (!(stack.getItem() instanceof BirdOrbItem)) return 0;
        CustomData custom = stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY);
        return Math.max(0, Math.min(TARGET, custom.copyTag().getInt(KEY)));
    }
    public static boolean fullyCharged(ItemStack stack) {
        return stack.getItem() instanceof BirdOrbItem && progress(stack) >= TARGET;
    }
    public static boolean chargeOne(ItemStack stack) {
        if (!(stack.getItem() instanceof BirdOrbItem) || fullyCharged(stack)) return false;
        CompoundTag tag = stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
        tag.putInt(KEY, progress(stack) + 1);
        stack.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));
        return true;
    }
    @Override public boolean isBarVisible(ItemStack stack) { return true; }
    @Override public int getBarWidth(ItemStack stack) { return Math.round(13f * progress(stack) / TARGET); }
    @Override public int getBarColor(ItemStack stack) {
        if (fullyCharged(stack)) return 0x60ed66;
        if (stack.getItem() == BirdOrbs.UNO.get()) return 0x8acaff;
        if (stack.getItem() == BirdOrbs.DOS.get()) return 0xf4e354;
        return 0xff7a49;
    }
    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltips, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltips, flag);
        int count = progress(stack);
        tooltips.add(Component.literal(fullyCharged(stack) ? "Fully charged — shrine feature coming later"
            : "Pokémon defeated in battle: " + count + " / " + TARGET)
            .withStyle(fullyCharged(stack) ? ChatFormatting.GREEN : ChatFormatting.GRAY));
    }
}
