package com.glaziola.pixelmonrejuvenated;
import net.minecraft.world.level.block.BushBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
/** Temporary sprout grows into a compact Pixelmon-style berry tree. */
public class RejuvenatedBerrySprout extends BushBlock implements net.minecraft.world.level.block.BonemealableBlock {
 private final String berry;
 public RejuvenatedBerrySprout(String berry,BlockBehaviour.Properties p){super(p);this.berry=berry;}
 @Override public void randomTick(BlockState state,ServerLevel level,BlockPos pos,RandomSource rand){
  if(rand.nextInt(8)==0){BerryTrees.grow(level,pos,berry);}
 }
 @Override public boolean isRandomlyTicking(BlockState state){return true;}
 @Override public boolean isValidBonemealTarget(net.minecraft.world.level.LevelReader level,BlockPos pos,BlockState state){return true;}
 @Override public boolean isBonemealSuccess(net.minecraft.world.level.Level level,RandomSource random,BlockPos pos,BlockState state){return true;}
 @Override public void performBonemeal(ServerLevel level,RandomSource random,BlockPos pos,BlockState state){BerryTrees.grow(level,pos,berry);}

}
