package com.glaziola.pixelmonrejuvenated;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.WallSide;

/** Generates a complete berry tree for both wild worldgen and planted sprouts. */
public final class BerryTrees {
    private BerryTrees() {}

    public static boolean grow(ServerLevel level, BlockPos pos, String berry) {
        return place(level, pos, berry);
    }

    public static boolean place(LevelAccessor level, BlockPos pos, String berry) {
        Supplier<? extends Block> leavesEntry = BerryBlocks.LEAVES.get(berry);
        if (leavesEntry == null || !level.getBlockState(pos.below()).is(BlockTags.DIRT)) return false;
        BlockState original = level.getBlockState(pos);
        if (!original.isAir() && !(original.getBlock() instanceof RejuvenatedBerrySprout)) return false;
        // Do not cut through existing player builds or trees.
        for (int y = 0; y <= 4; y++) {
            for (int x = -2; x <= 2; x++) for (int z = -2; z <= 2; z++) {
                if (y < 2 && (x != 0 || z != 0)) continue;
                if (y >= 2 && !leafAt(x, y, z) && (x != 0 || z != 0)) continue;
                BlockPos test = pos.offset(x, y, z);
                BlockState state = level.getBlockState(test);
                if (!state.isAir() && !(state.getBlock() instanceof RejuvenatedBerrySprout)) return false;
            }
        }
        Block log = ((Supplier<? extends Block>)BerryBlocks.BERRY_LOG).get();
        Block leaf = leavesEntry.get();
        for (int y = 0; y < 3; y++) level.setBlock(pos.above(y), log.defaultBlockState(), 3);
        for (int y = 2; y <= 4; y++) for (int x = -2; x <= 2; x++) for (int z = -2; z <= 2; z++) {
            if (!leafAt(x,y,z) || (x == 0 && z == 0 && y == 2)) continue;
            BlockPos at = pos.offset(x,y,z);
            if (level.getBlockState(at).isAir()) {
                BlockState state = leaf.defaultBlockState()
                    .setValue(LeavesBlock.DISTANCE, Math.min(6, Math.max(Math.abs(x),Math.abs(z)) + 1))
                    .setValue(LeavesBlock.PERSISTENT, false);
                level.setBlock(at, state, 3);
            }
        }
        // Force the directional branch arms after adjacent foliage is placed.
        BlockState trunk = log.defaultBlockState()
            .setValue(WallBlock.UP, true)
            .setValue(WallBlock.NORTH_WALL, WallSide.LOW)
            .setValue(WallBlock.EAST_WALL, WallSide.LOW)
            .setValue(WallBlock.SOUTH_WALL, WallSide.LOW)
            .setValue(WallBlock.WEST_WALL, WallSide.LOW);
        level.setBlock(pos.above(2),trunk, 2);
        return true;
    }

    private static boolean leafAt(int x,int y,int z) {
        if (y == 2 || y == 3) return Math.abs(x) + Math.abs(z) <= 3;
        return y == 4 && Math.abs(x) + Math.abs(z) <= 1;
    }
}
