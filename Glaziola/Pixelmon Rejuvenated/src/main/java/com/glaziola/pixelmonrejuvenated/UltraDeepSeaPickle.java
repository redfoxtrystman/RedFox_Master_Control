package com.glaziola.pixelmonrejuvenated;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SeaPickleBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

/** Like Pixelmon 9.4.1, bonemeal spreads Ultra Deep Sea Pickles, never vanilla Sea Pickles. */
public final class UltraDeepSeaPickle extends SeaPickleBlock {
    public UltraDeepSeaPickle(BlockBehaviour.Properties properties) { super(properties); }
    @Override public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state) {
        if (isDead(state) || !level.getBlockState(pos.below()).is(BlockTags.CORAL_BLOCKS)) return;
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                if (dx == 0 && dz == 0 || random.nextInt(6) != 0) continue;
                BlockPos at = pos.offset(dx, 0, dz);
                if (level.getBlockState(at).is(Blocks.WATER) && level.getBlockState(at.below()).is(BlockTags.CORAL_BLOCKS)) {
                    level.setBlock(at, (BlockState)defaultBlockState().setValue(PICKLES, random.nextInt(4) + 1), 3);
                }
            }
        }
        level.setBlock(pos, (BlockState)state.setValue(PICKLES, 4), 2);
    }
}
