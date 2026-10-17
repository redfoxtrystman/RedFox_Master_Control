package com.glaziola.pixelmonrejuvenated;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SeagrassBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.DoubleBlockHalf;

/** Ultra Deep Seagrass bonemeals into its own tall variant, as in Pixelmon 9.4.1. */
public final class UltraDeepSeagrass extends SeagrassBlock {
    public UltraDeepSeagrass(BlockBehaviour.Properties properties) { super(properties); }
    @Override public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state) {
        Block above = level.getBlockState(pos.above()).getBlock();
        if (above == Blocks.WATER) {
            BlockState lower = ((Supplier<? extends Block>) UltraSpaceExpansion.ULTRA_DEEP_TALL_SEAGRASS).get().defaultBlockState();
            level.setBlock(pos, lower, 2);
            level.setBlock(pos.above(), (BlockState)lower.setValue(UltraDeepTallSeagrass.HALF, DoubleBlockHalf.UPPER), 2);
        }
    }
}
