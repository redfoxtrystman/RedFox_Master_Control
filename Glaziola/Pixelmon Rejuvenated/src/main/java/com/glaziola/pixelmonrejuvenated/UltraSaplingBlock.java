package com.glaziola.pixelmonrejuvenated;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SaplingBlock;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

/** Preserve existing terrain under Ultra saplings during normal bonemeal/random tree growth.
 * Minecraft TreeFeature may replace non-vanilla/untagged modded terrain with vanilla dirt.
 * Do not alter other tree features; only restore soil changed to vanilla dirt by this growth. */
public final class UltraSaplingBlock extends SaplingBlock {
  public UltraSaplingBlock(TreeGrower grower, BlockBehaviour.Properties properties) {
    super(grower, properties);
  }
  @Override
  public void advanceTree(ServerLevel level, BlockPos pos, BlockState state, RandomSource random) {
    final BlockPos[] positions = new BlockPos[25];
    final BlockState[] before = new BlockState[25];
    int i=0;
    for (int dx=-2;dx<=2;dx++) for (int dz=-2;dz<=2;dz++) {
      BlockPos p=pos.offset(dx,-1,dz);
      positions[i]=p;
      before[i]=level.getBlockState(p);
      i++;
    }
    super.advanceTree(level,pos,state,random);
    for (i=0;i<positions.length;i++) {
      // Only revert conversion of previously existing terrain to dirt.
      // If a dirt block was already present, there is nothing to restore.
      if (level.getBlockState(positions[i]).is(Blocks.DIRT) && !before[i].is(Blocks.DIRT)) {
        level.setBlock(positions[i],before[i],3);
      }
    }
  }
}
