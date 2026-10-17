package com.glaziola.pixelmonrejuvenated;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockSetType;
import net.minecraft.world.level.block.state.properties.WoodType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Pixelmon Ultra Space block families that use vanilla Minecraft geometry and behaviors.
 * Saplings use vanilla SaplingBlock + TreeGrower, as in Pixelmon 9.4.1.
 * The underwater kelp stem grows using vanilla kelp behavior, not a custom Ultra Space growth hook. */
public final class UltraSpaceExpansion {
  public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("pixelmonrejuvenated");
  public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("pixelmonrejuvenated");
  private static final List<DeferredItem<BlockItem>> ALL_ITEMS = new ArrayList<>();
  private UltraSpaceExpansion() {}
  private static BlockBehaviour.Properties wood() { return BlockBehaviour.Properties.of().strength(2f,3f).sound(SoundType.WOOD).ignitedByLava(); }
  private static BlockBehaviour.Properties stone() { return BlockBehaviour.Properties.of().strength(1.5f,6f).sound(SoundType.STONE).requiresCorrectToolForDrops(); }
  private static BlockBehaviour.Properties leaf() { return BlockBehaviour.Properties.of().strength(0.2f).sound(SoundType.WOOD).noOcclusion(); }
  private static BlockBehaviour.Properties plant() { return BlockBehaviour.Properties.of().strength(0f).sound(SoundType.WOOD).noCollission().noOcclusion(); }
  private static <B extends Block> DeferredBlock<B> add(String id,DeferredBlock<B> block) {
    ALL_ITEMS.add(ITEMS.registerSimpleBlockItem(id,block,new Item.Properties()));return block;
  }
  private static DeferredBlock<Block> full(String id,BlockBehaviour.Properties p) { return add(id,BLOCKS.registerSimpleBlock(id,UltraSoundParity.apply(id,p))); }
  private static DeferredBlock<RotatedPillarBlock> pillar(String id) { return add(id,BLOCKS.registerBlock(id,RotatedPillarBlock::new,UltraSoundParity.apply(id,wood()))); }
  private static DeferredBlock<LeavesBlock> leaves(String id) { return add(id,BLOCKS.registerBlock(id,LeavesBlock::new,UltraSoundParity.apply(id,leaf()))); }
  private static DeferredBlock<UltraDecorativePlantBlock> bush(String id) {return add(id,BLOCKS.registerBlock(id,UltraDecorativePlantBlock::new,UltraSoundParity.apply(id,plant()))); }
  private static DeferredBlock<SaplingBlock> sapling(String id, net.minecraft.world.level.block.grower.TreeGrower grower) {
    return add(id, BLOCKS.registerBlock(id, p -> new UltraSaplingBlock(grower, p),
      UltraSoundParity.apply(id, plant().randomTicks().instabreak())));
  }
  private static DeferredBlock<SlabBlock> slab(String id) {return add(id,BLOCKS.registerBlock(id,SlabBlock::new,UltraSoundParity.apply(id,wood()))); }
  private static DeferredBlock<StairBlock> stairs(String id,DeferredBlock<? extends Block> parent) {
    return add(id,BLOCKS.registerBlock(id,p -> new StairBlock(((Supplier<? extends Block>)parent).get().defaultBlockState(),p),UltraSoundParity.apply(id,wood())));
  }
  private static DeferredBlock<FenceBlock> fence(String id) {return add(id,BLOCKS.registerBlock(id,FenceBlock::new,UltraSoundParity.apply(id,wood()))); }
  private static DeferredBlock<FenceGateBlock> gate(String id) {return add(id,BLOCKS.registerBlock(id,p -> new FenceGateBlock(WoodType.OAK,p),UltraSoundParity.apply(id,wood()))); }
  private static DeferredBlock<ButtonBlock> button(String id,boolean wood) {
    return add(id,BLOCKS.registerBlock(id,p -> new ButtonBlock(wood?BlockSetType.OAK:BlockSetType.STONE,wood?30:20,p),UltraSoundParity.apply(id,wood?wood():stone())));
  }
  private static DeferredBlock<PressurePlateBlock> plate(String id,boolean wood) {
    return add(id,BLOCKS.registerBlock(id,p -> new PressurePlateBlock(wood?BlockSetType.OAK:BlockSetType.STONE,p),UltraSoundParity.apply(id,wood?wood():stone())));
  }
  private static DeferredBlock<DoorBlock> door(String id) {return add(id,BLOCKS.registerBlock(id,p -> new DoorBlock(BlockSetType.OAK,p),UltraSoundParity.apply(id,wood().noOcclusion()))); }
  private static DeferredBlock<TrapDoorBlock> trapdoor(String id) {return add(id,BLOCKS.registerBlock(id,p -> new TrapDoorBlock(BlockSetType.OAK,p),UltraSoundParity.apply(id,wood().noOcclusion()))); }
  private static DeferredBlock<CactusBlock> cactus(String id) {return add(id,BLOCKS.registerBlock(id,CactusBlock::new,UltraSoundParity.apply(id,plant().randomTicks()))); }
  private static DeferredBlock<VineBlock> vine(String id) {return add(id,BLOCKS.registerBlock(id,VineBlock::new,UltraSoundParity.apply(id,plant()))); }
  private static DeferredBlock<UltraDeepKelpHead> kelp(String id) {return add(id,BLOCKS.registerBlock(id,UltraDeepKelpHead::new,UltraSoundParity.apply(id,plant().randomTicks().lightLevel(state -> 5)))); }
  private static DeferredBlock<UltraDeepKelpBody> kelpPlant(String id) {return BLOCKS.registerBlock(id,UltraDeepKelpBody::new,UltraSoundParity.apply(id,plant().lightLevel(state -> 5))); }
  private static DeferredBlock<UltraDeepSeagrass> seagrass(String id) {return add(id,BLOCKS.registerBlock(id,UltraDeepSeagrass::new,UltraSoundParity.apply(id,plant()))); }
  private static DeferredBlock<UltraDeepTallSeagrass> tallSeagrass(String id) {return BLOCKS.registerBlock(id,UltraDeepTallSeagrass::new,UltraSoundParity.apply(id,plant())); }
  private static DeferredBlock<UltraDeepSeaPickle> pickle(String id) {return add(id,BLOCKS.registerBlock(id,UltraDeepSeaPickle::new,UltraSoundParity.apply(id,plant()))); }
  private static DeferredBlock<CarpetBlock> fallenLeaves(String id) {return add(id,BLOCKS.registerBlock(id,CarpetBlock::new,UltraSoundParity.apply(id,plant()))); }

  public static final DeferredBlock<? extends Block> ULTRA_ELM_LOG = pillar("ultra_elm_log");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_WOOD = pillar("ultra_elm_wood");
  public static final DeferredBlock<? extends Block> STRIPPED_ULTRA_ELM_LOG = pillar("stripped_ultra_elm_log");
  public static final DeferredBlock<? extends Block> STRIPPED_ULTRA_ELM_WOOD = pillar("stripped_ultra_elm_wood");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_LEAVES = leaves("ultra_elm_leaves");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_SAPLING = sapling("ultra_elm_sapling", UltraTreeGrowers.ULTRA_ELM);
  public static final DeferredBlock<? extends Block> ULTRA_ELM_SLAB = slab("ultra_elm_slab");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_STAIRS = stairs("ultra_elm_stairs", UltraSpaceBlocks.ULTRA_ELM_PLANKS);
  public static final DeferredBlock<? extends Block> ULTRA_ELM_FENCE = fence("ultra_elm_fence");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_FENCE_GATE = gate("ultra_elm_fence_gate");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_BUTTON = button("ultra_elm_button", true);
  public static final DeferredBlock<? extends Block> ULTRA_ELM_PRESSURE_PLATE = plate("ultra_elm_pressure_plate", true);
  public static final DeferredBlock<? extends Block> ULTRA_ELM_DOOR = door("ultra_elm_door");
  public static final DeferredBlock<? extends Block> ULTRA_ELM_TRAPDOOR = trapdoor("ultra_elm_trapdoor");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_LOG = pillar("ultra_ginkgo_log");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_WOOD = pillar("ultra_ginkgo_wood");
  public static final DeferredBlock<? extends Block> STRIPPED_ULTRA_GINKGO_LOG = pillar("stripped_ultra_ginkgo_log");
  public static final DeferredBlock<? extends Block> STRIPPED_ULTRA_GINKGO_WOOD = pillar("stripped_ultra_ginkgo_wood");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_LEAVES = leaves("ultra_ginkgo_leaves");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_SAPLING = sapling("ultra_ginkgo_sapling", UltraTreeGrowers.ULTRA_GINKGO);
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_SLAB = slab("ultra_ginkgo_slab");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_STAIRS = stairs("ultra_ginkgo_stairs", UltraSpaceBlocks.ULTRA_GINKGO_PLANKS);
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_FENCE = fence("ultra_ginkgo_fence");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_FENCE_GATE = gate("ultra_ginkgo_fence_gate");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_BUTTON = button("ultra_ginkgo_button", true);
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_PRESSURE_PLATE = plate("ultra_ginkgo_pressure_plate", true);
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_DOOR = door("ultra_ginkgo_door");
  public static final DeferredBlock<? extends Block> ULTRA_GINKGO_TRAPDOOR = trapdoor("ultra_ginkgo_trapdoor");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_LOG = pillar("ultra_jungle_log");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_WOOD = pillar("ultra_jungle_wood");
  public static final DeferredBlock<? extends Block> STRIPPED_ULTRA_JUNGLE_LOG = pillar("stripped_ultra_jungle_log");
  public static final DeferredBlock<? extends Block> STRIPPED_ULTRA_JUNGLE_WOOD = pillar("stripped_ultra_jungle_wood");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_LEAVES = leaves("ultra_jungle_leaves");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_SAPLING = sapling("ultra_jungle_sapling", UltraTreeGrowers.ULTRA_JUNGLE);
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_SLAB = slab("ultra_jungle_slab");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_STAIRS = stairs("ultra_jungle_stairs", UltraSpaceBlocks.ULTRA_JUNGLE_PLANKS);
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_FENCE = fence("ultra_jungle_fence");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_FENCE_GATE = gate("ultra_jungle_fence_gate");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_BUTTON = button("ultra_jungle_button", true);
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_PRESSURE_PLATE = plate("ultra_jungle_pressure_plate", true);
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_DOOR = door("ultra_jungle_door");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_TRAPDOOR = trapdoor("ultra_jungle_trapdoor");
  public static final DeferredBlock<? extends Block> ULTRA_SPACE_STONE_BUTTON = button("ultra_space_stone_button", false);
  public static final DeferredBlock<? extends Block> ULTRA_SPACE_COBBLESTONE_BUTTON = button("ultra_space_cobblestone_button", false);
  public static final DeferredBlock<? extends Block> ULTRA_SPACE_STONE_PRESSURE_PLATE = plate("ultra_space_stone_pressure_plate", false);
  public static final DeferredBlock<? extends Block> ULTRA_SPACE_COBBLESTONE_PRESSURE_PLATE = plate("ultra_space_cobblestone_pressure_plate", false);
  public static final DeferredBlock<? extends Block> ULTRA_DESERT_CACTUS = cactus("ultra_desert_cactus");
  public static final DeferredBlock<? extends Block> ULTRA_FOREST_FALLEN_LEAVES = fallenLeaves("ultra_forest_fallen_leaves");
  public static final DeferredBlock<? extends Block> ULTRA_FOREST_FLOWER = bush("ultra_forest_flower");
  public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_VINE = vine("ultra_jungle_vine");
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_CRYSTAL = full("ultra_deep_crystal",stone());
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_CRYING_CRYSTAL = full("ultra_deep_crying_crystal",stone().noOcclusion());
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_KELP = kelp("ultra_deep_kelp");
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_KELP_PLANT = kelpPlant("ultra_deep_kelp_plant");
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_SEAGRASS = seagrass("ultra_deep_seagrass");
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_TALL_SEAGRASS = tallSeagrass("ultra_deep_tall_seagrass");
  public static final DeferredBlock<? extends Block> ULTRA_DEEP_SEA_PICKLE = pickle("ultra_deep_sea_pickle");

  public static void populateCreativeTab(CreativeModeTab.Output output) {
    for (DeferredItem<BlockItem> i: ALL_ITEMS) output.accept(((Supplier<? extends BlockItem>)i).get());
  }
  public static void register(IEventBus bus) {BLOCKS.register(bus);ITEMS.register(bus);}
}
