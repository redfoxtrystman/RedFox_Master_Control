package com.glaziola.pixelmonrejuvenated;
import java.util.ArrayList;import java.util.List;import java.util.function.Supplier;
import net.minecraft.world.item.BlockItem;import net.minecraft.world.item.Item;import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.level.block.*;import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;import net.neoforged.neoforge.registries.DeferredBlock;import net.neoforged.neoforge.registries.DeferredItem;import net.neoforged.neoforge.registries.DeferredRegister;
/** Adds missing rock, temple, and timed-falling materials. Pixelmon's custom
 * spawner/timer logic requires a subsequent functional implementation. */
public final class ExtraPixelmonBlocks {
 public static final DeferredRegister.Blocks BLOCKS=DeferredRegister.createBlocks("pixelmonrejuvenated");
 public static final DeferredRegister.Items ITEMS=DeferredRegister.createItems("pixelmonrejuvenated");
 private static final List<DeferredItem<BlockItem>> ALL=new ArrayList<>();
 private static <B extends Block> DeferredBlock<B> add(String id,DeferredBlock<B> b){ALL.add(ITEMS.registerSimpleBlockItem(id,b,new Item.Properties()));return b;}
 private static BlockBehaviour.Properties stone(){return BlockBehaviour.Properties.of().strength(1.5f,6f).requiresCorrectToolForDrops().sound(SoundType.STONE);}
 private static DeferredBlock<Block> cube(String n){return add(n,BLOCKS.registerSimpleBlock(n,stone()));}
 private static DeferredBlock<RotatedPillarBlock> pillar(String n){return add(n,BLOCKS.registerBlock(n,RotatedPillarBlock::new,stone()));}
 public static final DeferredBlock<? extends Block> TEMPLE_PILLAR=pillar("temple_pillar");
 public static final DeferredBlock<? extends Block> TEMPLE_PILLAR_FRACTURED=pillar("temple_pillar_fractured");
 public static final DeferredBlock<? extends Block> CAVE_ROCK=cube("cave_rock");
 public static final DeferredBlock<? extends Block> SPAWNER_CAVE_ROCK=cube("spawner_cave_rock");
 public static final DeferredBlock<? extends Block> TIMED_FALL=add("timed_fall",BLOCKS.registerBlock("timed_fall",TimedFallBlock::new,BlockBehaviour.Properties.of().strength(.5f).sound(SoundType.SAND)));
 public static void populateCreativeTab(CreativeModeTab.Output out){for(DeferredItem<BlockItem> i:ALL)out.accept(((Supplier<? extends BlockItem>)i).get());}
 public static void register(IEventBus bus){BLOCKS.register(bus);ITEMS.register(bus);}
}
