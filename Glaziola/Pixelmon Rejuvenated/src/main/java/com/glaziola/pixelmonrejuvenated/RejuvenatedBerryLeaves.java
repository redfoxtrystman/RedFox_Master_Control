package com.glaziola.pixelmonrejuvenated;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
/** Original Pixelmon berry tree leaves have age=0/1/2; uses Cobblemon's berry item when available. */
public class RejuvenatedBerryLeaves extends LeavesBlock {
 public static final IntegerProperty AGE=BlockStateProperties.AGE_2;
 private final String berry;
 public RejuvenatedBerryLeaves(String berry,BlockBehaviour.Properties p){super(p);this.berry=berry;this.registerDefaultState(this.getStateDefinition().any().setValue(AGE,0).setValue(DISTANCE,7).setValue(PERSISTENT,false).setValue(WATERLOGGED,false));}
 @Override protected void createBlockStateDefinition(StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> b){b.add(DISTANCE,PERSISTENT,AGE,WATERLOGGED);}
 @Override public boolean isRandomlyTicking(BlockState state){return true;}
 @Override public void randomTick(BlockState state,ServerLevel level,BlockPos pos,RandomSource random){
  int age=state.getValue(AGE);
  if(!state.getValue(PERSISTENT)&&age<2&&random.nextInt(10)==0){level.setBlock(pos,state.setValue(AGE,age+1),2);}
  super.randomTick(state,level,pos,random);
 }
 @Override protected InteractionResult useWithoutItem(BlockState state,Level level,BlockPos pos,Player player,BlockHitResult hit){
  if(state.getValue(AGE)!=2)return InteractionResult.PASS;
  Item berryItem=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("cobblemon",berry+"_berry"));
  if(berryItem==null || berryItem==net.minecraft.world.item.Items.AIR)return InteractionResult.PASS;
  if(!level.isClientSide){level.setBlock(pos,state.setValue(AGE,0),2);popResource(level,pos,new ItemStack(berryItem));}
  return InteractionResult.sidedSuccess(level.isClientSide);
 }
}
