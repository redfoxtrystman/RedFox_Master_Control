package com.glaziola.pixelmonrejuvenated;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Ordinary-model Pixelmon decorations. Deliberately excludes custom-shaped furniture and machines. */
public final class DecorativeBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("pixelmonrejuvenated");
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("pixelmonrejuvenated");
    private static final List<DeferredItem<BlockItem>> BLOCK_ITEMS = new ArrayList<>();
    private static final Map<String, DeferredBlock<? extends Block>> BLOCK_HANDLES = new LinkedHashMap<>();

    private DecorativeBlocks() {}
    private static BlockBehaviour.Properties decorProps(String id) {
        if (id.equals("bridge_block") || id.equals("window1") || id.equals("window2"))
            return UltraSoundParity.apply(id, BlockBehaviour.Properties.of().strength(0.8f, 2.0f).sound(SoundType.STONE).noOcclusion());
        if (id.startsWith("poke_sand") || id.equals("poke_dirt") || id.equals("poke_grass") || id.equals("sandy_grass"))
            return UltraSoundParity.apply(id, BlockBehaviour.Properties.of().strength(0.5f, 0.5f).sound(SoundType.SAND));
        if (id.equals("wooden_flooring") || id.startsWith("shingles"))
            return UltraSoundParity.apply(id, BlockBehaviour.Properties.of().strength(2.0f, 3.0f).sound(SoundType.WOOD));
        return UltraSoundParity.apply(id, BlockBehaviour.Properties.of().strength(1.5f, 6.0f).sound(SoundType.STONE).requiresCorrectToolForDrops());
    }
    private static <B extends Block> DeferredBlock<B> add(String id, DeferredBlock<B> block) {
        BLOCK_HANDLES.put(id, block);
        BLOCK_ITEMS.add(ITEMS.registerSimpleBlockItem(id, block, new Item.Properties()));
        return block;
    }
    private static DeferredBlock<Block> cube(String id) {
        return add(id, BLOCKS.registerSimpleBlock(id, decorProps(id)));
    }
    private static DeferredBlock<SlabBlock> slab(String id) {
        return add(id, BLOCKS.registerBlock(id, SlabBlock::new, decorProps(id)));
    }
    private static DeferredBlock<StairBlock> stairs(String id, String parentId) {
        DeferredBlock<? extends Block> parent = BLOCK_HANDLES.get(parentId);
        if (parent == null) throw new IllegalStateException("Missing parent block: " + parentId);
        return add(id, BLOCKS.registerBlock(id, props ->
            new StairBlock(((Supplier<? extends Block>) parent).get().defaultBlockState(), props), decorProps(id)));
    }

    // Only Pixelmon 9.4.1 cube/cube_column models; no indexed/legacy Unown or Braille placeholders.
    private static final String[] CUBES = {
            "unown_block_a",
            "unown_block_b",
            "unown_block_c",
            "unown_block_d",
            "unown_block_e",
            "unown_block_f",
            "unown_block_g",
            "unown_block_h",
            "unown_block_i",
            "unown_block_j",
            "unown_block_k",
            "unown_block_l",
            "unown_block_m",
            "unown_block_n",
            "unown_block_o",
            "unown_block_p",
            "unown_block_q",
            "unown_block_r",
            "unown_block_s",
            "unown_block_t",
            "unown_block_u",
            "unown_block_v",
            "unown_block_w",
            "unown_block_x",
            "unown_block_y",
            "unown_block_z",
            "unown_block_blank",
            "unown_block_exclaim",
            "unown_block_question",
            "braille_block_a",
            "braille_block_b",
            "braille_block_c",
            "braille_block_d",
            "braille_block_e",
            "braille_block_f",
            "braille_block_g",
            "braille_block_h",
            "braille_block_i",
            "braille_block_j",
            "braille_block_k",
            "braille_block_l",
            "braille_block_m",
            "braille_block_n",
            "braille_block_o",
            "braille_block_p",
            "braille_block_q",
            "braille_block_r",
            "braille_block_s",
            "braille_block_t",
            "braille_block_u",
            "braille_block_v",
            "braille_block_w",
            "braille_block_x",
            "braille_block_y",
            "braille_block_z",
            "braille_block_blank",
            "braille_block_comma",
            "braille_block_stop",
            "braille_block_underscore",
            "bridge_block",
            "dusty_ruins_wall",
            "fancy_pillar",
            "inside_wall",
            "inside_wall_moulding",
            "outside_wall",
            "ruins_wall",
            "shingles",
            "shingles_corner1",
            "shingles_corner2",
            "wooden_flooring",
            "window1",
            "window2",
            "temple_block",
            "temple_brick",
            "poke_center_sign",
            "poke_mart_sign",
            "poke_dirt",
            "poke_grass",
            "poke_sand",
            "sandy_grass",
            "rock",
            "poke_sand_corner1",
            "poke_sand_corner2",
            "poke_sand_corner3",
            "poke_sand_corner4",
            "poke_sand_side1",
            "poke_sand_side2",
            "poke_sand_side3",
            "poke_sand_side4"
    };
    static {
        for (String id : CUBES) cube(id);
        slab("temple_slab");
        stairs("temple_stairs", "temple_block");
        slab("temple_brick_slab");
        stairs("temple_brick_stairs", "temple_brick");
    }

    /** Add each decorative item once to the single shared Pixelmon Blocks tab. */
    public static void populateCreativeTab(CreativeModeTab.Output output) {
        for (DeferredItem<BlockItem> entry : BLOCK_ITEMS) {
            output.accept(((Supplier<? extends BlockItem>) entry).get());
        }
    }

    public static void register(IEventBus bus) {
        BLOCKS.register(bus);
        ITEMS.register(bus);
    }
}
