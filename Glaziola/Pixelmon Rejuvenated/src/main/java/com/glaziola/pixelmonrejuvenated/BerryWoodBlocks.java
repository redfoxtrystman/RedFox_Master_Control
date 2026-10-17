package com.glaziola.pixelmonrejuvenated;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockSetType;
import net.minecraft.world.level.block.state.properties.WoodType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
/** Six Pixelmon berry wood palettes using native 1.21.1 block mechanics. */
public final class BerryWoodBlocks {
  public static final DeferredRegister.Blocks BLOCKS=DeferredRegister.createBlocks("pixelmonrejuvenated");
  public static final DeferredRegister.Items ITEMS=DeferredRegister.createItems("pixelmonrejuvenated");
  private static final List<DeferredItem<BlockItem>> ALL=new ArrayList<>();
  private BerryWoodBlocks(){}
  private static BlockBehaviour.Properties wood(){return BlockBehaviour.Properties.of().strength(2f,3f).sound(SoundType.WOOD).ignitedByLava();}
  private static <B extends Block> DeferredBlock<B> add(String n,DeferredBlock<B> b){ALL.add(ITEMS.registerSimpleBlockItem(n,b,new Item.Properties()));return b;}
  private static DeferredBlock<Block> planks(String n){return add(n,BLOCKS.registerSimpleBlock(n,wood()));}
  private static DeferredBlock<StairBlock> stairs(String n,DeferredBlock<? extends Block> base){return add(n,BLOCKS.registerBlock(n,p->new StairBlock(((Supplier<? extends Block>)base).get().defaultBlockState(),p),wood()));}
  private static DeferredBlock<SlabBlock> slab(String n){return add(n,BLOCKS.registerBlock(n,SlabBlock::new,wood()));}
  private static DeferredBlock<FenceBlock> fence(String n){return add(n,BLOCKS.registerBlock(n,FenceBlock::new,wood()));}
  private static DeferredBlock<FenceGateBlock> fenceGate(String n){return add(n,BLOCKS.registerBlock(n,p->new FenceGateBlock(WoodType.OAK,p),wood()));}
  private static DeferredBlock<ButtonBlock> button(String n){return add(n,BLOCKS.registerBlock(n,p->new ButtonBlock(BlockSetType.OAK,30,p),wood()));}
  private static DeferredBlock<PressurePlateBlock> pressure(String n){return add(n,BLOCKS.registerBlock(n,p->new PressurePlateBlock(BlockSetType.OAK,p),wood()));}
  private static DeferredBlock<DoorBlock> door(String n){return add(n,BLOCKS.registerBlock(n,p->new DoorBlock(BlockSetType.OAK,p),wood().noOcclusion()));}
  private static DeferredBlock<TrapDoorBlock> trapdoor(String n){return add(n,BLOCKS.registerBlock(n,p->new TrapDoorBlock(BlockSetType.OAK,p),wood().noOcclusion()));}
  public static final DeferredBlock<? extends Block> RED_PLANKS=planks("red_berry_wood_planks");
  public static final DeferredBlock<? extends Block> RED_STAIRS=stairs("red_berry_wood_stairs",RED_PLANKS);
  public static final DeferredBlock<? extends Block> RED_SLAB=slab("red_berry_wood_slab");
  public static final DeferredBlock<? extends Block> RED_FENCE=fence("red_berry_wood_fence");
  public static final DeferredBlock<? extends Block> RED_FENCE_GATE=fenceGate("red_berry_wood_fence_gate");
  public static final DeferredBlock<? extends Block> RED_BUTTON=button("red_berry_wood_button");
  public static final DeferredBlock<? extends Block> RED_PRESSURE_PLATE=pressure("red_berry_wood_pressure_plate");
  public static final DeferredBlock<? extends Block> RED_DOOR=door("red_berry_wood_door");
  public static final DeferredBlock<? extends Block> RED_TRAPDOOR=trapdoor("red_berry_wood_trapdoor");
  public static final DeferredBlock<? extends Block> BLUE_PLANKS=planks("blue_berry_wood_planks");
  public static final DeferredBlock<? extends Block> BLUE_STAIRS=stairs("blue_berry_wood_stairs",BLUE_PLANKS);
  public static final DeferredBlock<? extends Block> BLUE_SLAB=slab("blue_berry_wood_slab");
  public static final DeferredBlock<? extends Block> BLUE_FENCE=fence("blue_berry_wood_fence");
  public static final DeferredBlock<? extends Block> BLUE_FENCE_GATE=fenceGate("blue_berry_wood_fence_gate");
  public static final DeferredBlock<? extends Block> BLUE_BUTTON=button("blue_berry_wood_button");
  public static final DeferredBlock<? extends Block> BLUE_PRESSURE_PLATE=pressure("blue_berry_wood_pressure_plate");
  public static final DeferredBlock<? extends Block> BLUE_DOOR=door("blue_berry_wood_door");
  public static final DeferredBlock<? extends Block> BLUE_TRAPDOOR=trapdoor("blue_berry_wood_trapdoor");
  public static final DeferredBlock<? extends Block> GREEN_PLANKS=planks("green_berry_wood_planks");
  public static final DeferredBlock<? extends Block> GREEN_STAIRS=stairs("green_berry_wood_stairs",GREEN_PLANKS);
  public static final DeferredBlock<? extends Block> GREEN_SLAB=slab("green_berry_wood_slab");
  public static final DeferredBlock<? extends Block> GREEN_FENCE=fence("green_berry_wood_fence");
  public static final DeferredBlock<? extends Block> GREEN_FENCE_GATE=fenceGate("green_berry_wood_fence_gate");
  public static final DeferredBlock<? extends Block> GREEN_BUTTON=button("green_berry_wood_button");
  public static final DeferredBlock<? extends Block> GREEN_PRESSURE_PLATE=pressure("green_berry_wood_pressure_plate");
  public static final DeferredBlock<? extends Block> GREEN_DOOR=door("green_berry_wood_door");
  public static final DeferredBlock<? extends Block> GREEN_TRAPDOOR=trapdoor("green_berry_wood_trapdoor");
  public static final DeferredBlock<? extends Block> YELLOW_PLANKS=planks("yellow_berry_wood_planks");
  public static final DeferredBlock<? extends Block> YELLOW_STAIRS=stairs("yellow_berry_wood_stairs",YELLOW_PLANKS);
  public static final DeferredBlock<? extends Block> YELLOW_SLAB=slab("yellow_berry_wood_slab");
  public static final DeferredBlock<? extends Block> YELLOW_FENCE=fence("yellow_berry_wood_fence");
  public static final DeferredBlock<? extends Block> YELLOW_FENCE_GATE=fenceGate("yellow_berry_wood_fence_gate");
  public static final DeferredBlock<? extends Block> YELLOW_BUTTON=button("yellow_berry_wood_button");
  public static final DeferredBlock<? extends Block> YELLOW_PRESSURE_PLATE=pressure("yellow_berry_wood_pressure_plate");
  public static final DeferredBlock<? extends Block> YELLOW_DOOR=door("yellow_berry_wood_door");
  public static final DeferredBlock<? extends Block> YELLOW_TRAPDOOR=trapdoor("yellow_berry_wood_trapdoor");
  public static final DeferredBlock<? extends Block> PINK_PLANKS=planks("pink_berry_wood_planks");
  public static final DeferredBlock<? extends Block> PINK_STAIRS=stairs("pink_berry_wood_stairs",PINK_PLANKS);
  public static final DeferredBlock<? extends Block> PINK_SLAB=slab("pink_berry_wood_slab");
  public static final DeferredBlock<? extends Block> PINK_FENCE=fence("pink_berry_wood_fence");
  public static final DeferredBlock<? extends Block> PINK_FENCE_GATE=fenceGate("pink_berry_wood_fence_gate");
  public static final DeferredBlock<? extends Block> PINK_BUTTON=button("pink_berry_wood_button");
  public static final DeferredBlock<? extends Block> PINK_PRESSURE_PLATE=pressure("pink_berry_wood_pressure_plate");
  public static final DeferredBlock<? extends Block> PINK_DOOR=door("pink_berry_wood_door");
  public static final DeferredBlock<? extends Block> PINK_TRAPDOOR=trapdoor("pink_berry_wood_trapdoor");
  public static final DeferredBlock<? extends Block> PURPLE_PLANKS=planks("purple_berry_wood_planks");
  public static final DeferredBlock<? extends Block> PURPLE_STAIRS=stairs("purple_berry_wood_stairs",PURPLE_PLANKS);
  public static final DeferredBlock<? extends Block> PURPLE_SLAB=slab("purple_berry_wood_slab");
  public static final DeferredBlock<? extends Block> PURPLE_FENCE=fence("purple_berry_wood_fence");
  public static final DeferredBlock<? extends Block> PURPLE_FENCE_GATE=fenceGate("purple_berry_wood_fence_gate");
  public static final DeferredBlock<? extends Block> PURPLE_BUTTON=button("purple_berry_wood_button");
  public static final DeferredBlock<? extends Block> PURPLE_PRESSURE_PLATE=pressure("purple_berry_wood_pressure_plate");
  public static final DeferredBlock<? extends Block> PURPLE_DOOR=door("purple_berry_wood_door");
  public static final DeferredBlock<? extends Block> PURPLE_TRAPDOOR=trapdoor("purple_berry_wood_trapdoor");
  public static void populateCreativeTab(CreativeModeTab.Output out){for(DeferredItem<BlockItem> i:ALL)out.accept(((Supplier<? extends BlockItem>)i).get());}
  public static void register(IEventBus bus){BLOCKS.register(bus);ITEMS.register(bus);}
}
