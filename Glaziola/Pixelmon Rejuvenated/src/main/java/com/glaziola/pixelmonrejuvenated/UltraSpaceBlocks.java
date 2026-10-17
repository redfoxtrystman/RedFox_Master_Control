package com.glaziola.pixelmonrejuvenated;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.ItemStack;
import net.minecraft.network.chat.Component;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Ultra Space materials and dedicated creative tab for NeoForge 21.1.x. */
public final class UltraSpaceBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("pixelmonrejuvenated");
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("pixelmonrejuvenated");
    private static final List<DeferredItem<BlockItem>> BLOCK_ITEMS = new ArrayList<>();
    public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS =
        DeferredRegister.create(Registries.CREATIVE_MODE_TAB, "pixelmonrejuvenated");

    private UltraSpaceBlocks() {}

    private static BlockBehaviour.Properties stoneProps() {
        return BlockBehaviour.Properties.of().strength(1.5f, 6f).sound(SoundType.STONE).requiresCorrectToolForDrops();
    }
    private static BlockBehaviour.Properties woodProps() {
        return BlockBehaviour.Properties.of().strength(2f, 3f).sound(SoundType.WOOD).ignitedByLava();
    }
    private static BlockBehaviour.Properties clayProps() {
        return BlockBehaviour.Properties.of().strength(0.6f).sound(SoundType.GRAVEL);
    }
    private static BlockBehaviour.Properties sandProps() {
        return BlockBehaviour.Properties.of().strength(0.5f).sound(SoundType.SAND);
    }
    private static <B extends Block> DeferredBlock<B> add(String id, DeferredBlock<B> holder) {
        BLOCK_ITEMS.add(ITEMS.registerSimpleBlockItem(id, holder, new Item.Properties()));
        return holder;
    }
    private static DeferredBlock<Block> block(String id, BlockBehaviour.Properties props) {
        return add(id, BLOCKS.registerSimpleBlock(id, UltraSoundParity.apply(id, props)));
    }
    private static DeferredBlock<UltraFallingBlock> falling(String id) {
        return add(id, BLOCKS.registerBlock(id, UltraFallingBlock::new, UltraSoundParity.apply(id,sandProps())));
    }
    private static DeferredBlock<SlabBlock> slab(String id, BlockBehaviour.Properties props) {
        return add(id, BLOCKS.registerBlock(id, SlabBlock::new, UltraSoundParity.apply(id,props)));
    }
    private static DeferredBlock<StairBlock> stairs(String id, DeferredBlock<? extends Block> parent) {
        return add(id, BLOCKS.registerBlock(id, props -> new StairBlock(((Supplier<? extends Block>) parent).get().defaultBlockState(), props), UltraSoundParity.apply(id,stoneProps())));
    }
    private static DeferredBlock<WallBlock> wall(String id) {
        return add(id, BLOCKS.registerBlock(id, WallBlock::new, UltraSoundParity.apply(id,stoneProps())));
    }

    public static final DeferredBlock<? extends Block> ULTRA_SPACE_STONE = block("ultra_space_stone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_COBBLESTONE = block("ultra_space_cobblestone", stoneProps());
    public static final DeferredBlock<? extends Block> POLISHED_ULTRA_SPACE_STONE = block("polished_ultra_space_stone", stoneProps());
    public static final DeferredBlock<? extends Block> CHISELED_ULTRA_SPACE_STONE = block("chiseled_ultra_space_stone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_STONE_SLAB = slab("ultra_space_stone_slab", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_STONE_STAIRS = stairs("ultra_space_stone_stairs", ULTRA_SPACE_STONE);
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_STONE_WALL = wall("ultra_space_stone_wall");
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_COBBLESTONE_SLAB = slab("ultra_space_cobblestone_slab", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_COBBLESTONE_STAIRS = stairs("ultra_space_cobblestone_stairs", ULTRA_SPACE_COBBLESTONE);
    public static final DeferredBlock<? extends Block> ULTRA_SPACE_COBBLESTONE_WALL = wall("ultra_space_cobblestone_wall");
    public static final DeferredBlock<? extends Block> POLISHED_ULTRA_SPACE_STONE_SLAB = slab("polished_ultra_space_stone_slab", stoneProps());
    public static final DeferredBlock<? extends Block> POLISHED_ULTRA_SPACE_STONE_STAIRS = stairs("polished_ultra_space_stone_stairs", POLISHED_ULTRA_SPACE_STONE);
    public static final DeferredBlock<? extends Block> POLISHED_ULTRA_SPACE_STONE_WALL = wall("polished_ultra_space_stone_wall");
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SAND = falling("ultra_desert_sand");
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_GILDED_SAND = falling("ultra_desert_gilded_sand");
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SANDSTONE = block("ultra_desert_sandstone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_CHISELED_SANDSTONE = block("ultra_desert_chiseled_sandstone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_CUT_SANDSTONE = block("ultra_desert_cut_sandstone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SMOOTH_SANDSTONE = block("ultra_desert_smooth_sandstone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SANDSTONE_SLAB = slab("ultra_desert_sandstone_slab", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SANDSTONE_STAIRS = stairs("ultra_desert_sandstone_stairs", ULTRA_DESERT_SANDSTONE);
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SANDSTONE_WALL = wall("ultra_desert_sandstone_wall");
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_CUT_SANDSTONE_SLAB = slab("ultra_desert_cut_sandstone_slab", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SMOOTH_SANDSTONE_SLAB = slab("ultra_desert_smooth_sandstone_slab", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DESERT_SMOOTH_SANDSTONE_STAIRS = stairs("ultra_desert_smooth_sandstone_stairs", ULTRA_DESERT_SMOOTH_SANDSTONE);
    public static final DeferredBlock<? extends Block> ULTRA_DEEP_STONE = block("ultra_deep_stone", stoneProps());
    public static final DeferredBlock<? extends Block> ULTRA_DEEP_CLAY = block("ultra_deep_clay", clayProps());
    public static final DeferredBlock<? extends Block> ULTRA_DEEP_GRAVEL = falling("ultra_deep_gravel");
    public static final DeferredBlock<? extends Block> ULTRA_ELM_PLANKS = block("ultra_elm_planks", woodProps());
    public static final DeferredBlock<? extends Block> ULTRA_GINKGO_PLANKS = block("ultra_ginkgo_planks", woodProps());
    public static final DeferredBlock<? extends Block> ULTRA_JUNGLE_PLANKS = block("ultra_jungle_planks", woodProps());

    /** All 124 registered Pixelmon Rejuvenated blocks in one creative inventory tab.
     *  IMPORTANT: Minecraft 1.21.1's DisplayItemsGenerator SAM is named accept(), NOT generate().
     *  An explicit implementation prevents generating the incorrect Alpha 31/32 lambda bridge. */
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> PIXELMON_BLOCKS_TAB =
        CREATIVE_TABS.register("pixelmon_blocks", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.pixelmonrejuvenated.pixelmon_blocks"))
            .withTabsBefore(CreativeModeTabs.SPAWN_EGGS)
            .icon(() -> new ItemStack(((Supplier<? extends Block>) ULTRA_SPACE_STONE).get()))
            .displayItems(new CreativeModeTab.DisplayItemsGenerator() {
                @Override
                public void accept(CreativeModeTab.ItemDisplayParameters parameters, CreativeModeTab.Output output) {
                    for (DeferredItem<BlockItem> item : BLOCK_ITEMS) {
                        output.accept(((Supplier<? extends BlockItem>) item).get());
                    }
                    DecorativeBlocks.populateCreativeTab(output);
                    UltraSpaceExpansion.populateCreativeTab(output);
                    BerryWoodBlocks.populateCreativeTab(output);
                    ExtraPixelmonBlocks.populateCreativeTab(output);
                    BerryBlocks.populateCreativeTab(output);
                    GemContent.populateBlocks(output);
                }
            })
            .build());

    public static void register(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        CREATIVE_TABS.register(modBus);
        UltraSpaceExpansion.register(modBus);
    }
}
