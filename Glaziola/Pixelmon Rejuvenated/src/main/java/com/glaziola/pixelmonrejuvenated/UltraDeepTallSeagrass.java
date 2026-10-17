package com.glaziola.pixelmonrejuvenated;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.TallSeagrassBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

/** Non-item two-block variant: pick-block returns the collectible single Ultra Deep Seagrass. */
public final class UltraDeepTallSeagrass extends TallSeagrassBlock {
    public UltraDeepTallSeagrass(BlockBehaviour.Properties properties) { super(properties); }
    @Override public ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state) {
        return new ItemStack(((Supplier<? extends Block>)UltraSpaceExpansion.ULTRA_DEEP_SEAGRASS).get().asItem());
    }
}
