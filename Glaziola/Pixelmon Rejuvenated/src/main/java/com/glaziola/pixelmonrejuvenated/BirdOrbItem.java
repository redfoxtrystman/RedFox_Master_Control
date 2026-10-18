package com.glaziola.pixelmonrejuvenated;

import java.util.List;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.ChatFormatting;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.core.BlockPos;
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
        if (stack.is(BirdOrbs.UNO.get())) return 0x8acaff;
        if (stack.is(BirdOrbs.DOS.get())) return 0xf4e354;
        return 0xff7a49;
    }
    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltips, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltips, flag);
        int count = progress(stack);
        tooltips.add(Component.literal(fullyCharged(stack) ? "Fully charged — right-click to summon legendary bird"
            : "Pokémon defeated in battle: " + count + " / " + TARGET)
            .withStyle(fullyCharged(stack) ? ChatFormatting.GREEN : ChatFormatting.GRAY));
    }
    /** Right-click a solid block: spawn above/along its clicked face. */
    @Override
    public InteractionResult useOn(UseOnContext context) {
        Player player = context.getPlayer();
        if (player == null) return InteractionResult.PASS;
        ItemStack stack = context.getItemInHand();
        if (!fullyCharged(stack)) {
            if (!context.getLevel().isClientSide)
                player.displayClientMessage(Component.literal("Orb charge: " + progress(stack) + "/" + TARGET), true);
            return InteractionResult.PASS;
        }
        if (context.getLevel().isClientSide) return InteractionResult.SUCCESS;
        BlockPos target = context.getClickedPos().relative(context.getClickedFace());
        return trySummon(player, stack, target.getX() + 0.5D, target.getY(), target.getZ() + 0.5D)
                ? InteractionResult.SUCCESS : InteractionResult.FAIL;
    }

    /** Right-click air: raycast toward the target or spawn twelve blocks into empty space. */
    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!fullyCharged(stack)) {
            if (!level.isClientSide)
                player.displayClientMessage(Component.literal("Orb charge: " + progress(stack) + "/" + TARGET), true);
            return InteractionResultHolder.pass(stack);
        }
        if (level.isClientSide) return InteractionResultHolder.success(stack);
        HitResult hit = player.pick(32.0D, 1.0F, false);
        Vec3 spawn;
        if (hit instanceof BlockHitResult block) {
            BlockPos p = block.getBlockPos().relative(block.getDirection());
            spawn = new Vec3(p.getX() + 0.5D, p.getY(), p.getZ() + 0.5D);
        } else {
            spawn = player.getEyePosition().add(player.getLookAngle().scale(12.0D));
        }
        return trySummon(player, stack, spawn.x, spawn.y, spawn.z)
                ? InteractionResultHolder.success(stack) : InteractionResultHolder.fail(stack);
    }

    /** Command runs with server-granted permission from an authenticated charged item use.
     * The Pokémon is wild and catchable, not assigned to the player's party.
     */
    private boolean trySummon(Player player, ItemStack stack, double x, double y, double z) {
        if (!(player instanceof ServerPlayer sp) || !fullyCharged(stack)) return false;
        String species;
        if (stack.is(BirdOrbs.UNO.get())) species = "articuno";
        else if (stack.is(BirdOrbs.DOS.get())) species = "zapdos";
        else if (stack.is(BirdOrbs.TRES.get())) species = "moltres";
        else return false;
        String command = "spawnpokemonat " + x + " " + y + " " + z + " " + species;
        try {
            int result = sp.getServer().getCommands().performPrefixedCommand(
                    sp.createCommandSourceStack().withPermission(4).withSuppressedOutput(), command);
            if (result <= 0) {
                player.displayClientMessage(Component.literal("Failed to summon " + species + "; the orb was not consumed."), true);
                return false;
            }
            stack.shrink(1);
            player.getCooldowns().addCooldown(this, 20);
            player.displayClientMessage(Component.literal("Summoned " + species + "!"), true);
            return true;
        } catch (RuntimeException e) {
            player.displayClientMessage(Component.literal("Summoning failed; orb was not consumed."), true);
            return false;
        }
    }

}
