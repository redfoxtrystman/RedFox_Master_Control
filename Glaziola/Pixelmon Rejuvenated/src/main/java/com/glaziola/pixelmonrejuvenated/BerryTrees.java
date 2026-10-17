package com.glaziola.pixelmonrejuvenated;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.Block;
import java.util.function.Supplier;
/** Small survival berry tree: grounded trunk and berry-specific foliage. */
public final class BerryTrees {
 private BerryTrees(){}
 public static boolean grow(ServerLevel level,BlockPos pos,String berry){
  if(!level.getBlockState(pos.above()).isAir() || !level.getBlockState(pos.above(2)).isAir() || !level.getBlockState(pos.above(3)).isAir())return false;
  Block leaf=((Supplier<? extends Block>)BerryBlocks.LEAVES.get(berry)).get();
  Block log=((Supplier<? extends Block>)BerryBlocks.BERRY_LOG).get();
  for(int h=0;h<3;h++)level.setBlock(pos.above(h),log.defaultBlockState(),3);
  for(int dx=-2;dx<=2;dx++)for(int dz=-2;dz<=2;dz++)for(int dy=2;dy<=4;dy++){
   if(Math.abs(dx)+Math.abs(dz)>3|| (dy==4 && Math.abs(dx)+Math.abs(dz)>1))continue;
   BlockPos at=pos.offset(dx,dy,dz);
   if(level.getBlockState(at).isAir())level.setBlock(at,leaf.defaultBlockState().setValue(net.minecraft.world.level.block.LeavesBlock.DISTANCE,Math.min(6,Math.max(Math.abs(dx),Math.abs(dz))+1)),3);
  }
  return true;
 }
}
