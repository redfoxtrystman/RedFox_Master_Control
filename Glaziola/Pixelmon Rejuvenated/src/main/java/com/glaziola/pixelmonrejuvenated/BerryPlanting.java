package com.glaziola.pixelmonrejuvenated;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.tags.BlockTags;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import java.util.function.Supplier;
/** Plant existing Cobblemon berry items on normal dirt/grass while leaving farmland alone. */
public final class BerryPlanting {
 private BerryPlanting(){}
 @SubscribeEvent public static void plant(PlayerInteractEvent.RightClickBlock event){
  Level level=event.getLevel();
  if(level.isClientSide || event.getFace()!=Direction.UP)return;
  if(level.getBlockState(event.getPos()).is(Blocks.FARMLAND))return;
  if(!level.getBlockState(event.getPos()).is(BlockTags.DIRT))return;
  BlockPos place=event.getPos().above();
  if(!level.getBlockState(place).canBeReplaced())return;
  ItemStack item=event.getItemStack();
  ResourceLocation key=BuiltInRegistries.ITEM.getKey(item.getItem());
  if(key==null||!"cobblemon".equals(key.getNamespace())||!key.getPath().endsWith("_berry"))return;
  String berry=key.getPath().substring(0,key.getPath().length()-6);
  var sprout=BerryBlocks.PLANTS.get(berry);
  if(sprout==null)return;
  level.setBlock(place,((Supplier<? extends net.minecraft.world.level.block.Block>)sprout).get().defaultBlockState(),3);
  // Pixelmon-like planting audio: play the sprout block's own place sound
  // server-side, broadcasting to the planter and nearby players.
  net.minecraft.world.level.block.SoundType placementSound=level.getBlockState(place).getSoundType(level,place,event.getEntity());
  level.playSound(null,place,placementSound.getPlaceSound(),net.minecraft.sounds.SoundSource.BLOCKS,
      (placementSound.getVolume()+1f)/2f,placementSound.getPitch()*0.8f);
  Player player=event.getEntity();
  if(!player.getAbilities().instabuild)item.shrink(1);
  event.setCanceled(true);
  event.setCancellationResult(InteractionResult.SUCCESS);
 }
}
