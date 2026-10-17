package com.glaziola.pixelmonrejuvenated;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.Holder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.*;

/** The Ruby, Sapphire and Crystal material sets from the user-supplied Pixelmon 9.4.1.
 *  No duplicate Cobblemon gems, crystal cores or evolution stones are registered. */
public final class GemContent {
    private static final String MODID="pixelmonrejuvenated";
    public static final DeferredRegister.Blocks BLOCKS=DeferredRegister.createBlocks(MODID);
    public static final DeferredRegister.Items ITEMS=DeferredRegister.createItems(MODID);
    private static final List<DeferredHolder<Item, ? extends Item>> COLLECTABLE_ITEMS=new ArrayList<>();
    private static final List<DeferredItem<BlockItem>> BLOCK_ITEMS=new ArrayList<>();
    private GemContent() {}

    private static void addItem(String id, Supplier<? extends Item> item) { COLLECTABLE_ITEMS.add(ITEMS.register(id,item)); }
    private static void addBlock(String id, boolean ore) {
        BlockBehaviour.Properties p=BlockBehaviour.Properties.of()
            .strength(ore?3.0f:5.0f, ore?3.0f:6.0f)
            .sound(SoundType.STONE).requiresCorrectToolForDrops();
        DeferredBlock<Block> block=BLOCKS.registerSimpleBlock(id,p);
        BLOCK_ITEMS.add(ITEMS.registerSimpleBlockItem(id,block,new Item.Properties()));
    }
    private static Tier tier(String name) {
        return new Tier() {
            @Override public int getUses(){return 300;}
            @Override public float getSpeed(){return 8.0f;}
            @Override public float getAttackDamageBonus(){return 2.0f;}
            @Override public int getEnchantmentValue(){return 10;}
            @Override public TagKey<Block> getIncorrectBlocksForDrops(){return BlockTags.INCORRECT_FOR_DIAMOND_TOOL;}
            @Override public Ingredient getRepairIngredient(){
                return Ingredient.of((ItemLike)((Supplier<? extends Item>)GEM_ITEMS.get(name)).get());
            }
        };
    }
    private static final java.util.Map<String,DeferredHolder<Item,? extends Item>> GEM_ITEMS=new java.util.LinkedHashMap<>();
    private static void addGem(String gem) {
        DeferredHolder<Item, ? extends Item> ref=ITEMS.register(gem,()->new Item(new Item.Properties()));
        COLLECTABLE_ITEMS.add(ref);
        GEM_ITEMS.put(gem,ref);
    }
    private static void addGear(String gem) {
        Tier t=tier(gem);
        addItem(gem+"_sword",()->new SwordItem(t,new Item.Properties()));
        addItem(gem+"_pickaxe",()->new PickaxeItem(t,new Item.Properties()));
        addItem(gem+"_axe",()->new AxeItem(t,new Item.Properties()));
        addItem(gem+"_shovel",()->new ShovelItem(t,new Item.Properties()));
        addItem(gem+"_hoe",()->new HoeItem(t,new Item.Properties()));
        // Classic Pixelmon hammer special behavior requires its own later implementation.
        addItem(gem+"_hammer",()->new PickaxeItem(t,new Item.Properties()));
        if (!gem.equals("crystal")) {
            Map<ArmorItem.Type,Integer> protection=Map.of(
                ArmorItem.Type.HELMET,3,ArmorItem.Type.CHESTPLATE,7,
                ArmorItem.Type.LEGGINGS,6,ArmorItem.Type.BOOTS,3);
            ArmorMaterial material=new ArmorMaterial(protection,10,SoundEvents.ARMOR_EQUIP_IRON,
                ()->Ingredient.of((ItemLike)((Supplier<? extends Item>)GEM_ITEMS.get(gem)).get()),
                List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(MODID,gem))),0f,0f);
            Holder<ArmorMaterial> holder=Holder.direct(material);
            addItem(gem+"_helmet",()->new ArmorItem(holder,ArmorItem.Type.HELMET,
                new Item.Properties().durability(ArmorItem.Type.HELMET.getDurability(33))));
            addItem(gem+"_chestplate",()->new ArmorItem(holder,ArmorItem.Type.CHESTPLATE,
                new Item.Properties().durability(ArmorItem.Type.CHESTPLATE.getDurability(33))));
            addItem(gem+"_leggings",()->new ArmorItem(holder,ArmorItem.Type.LEGGINGS,
                new Item.Properties().durability(ArmorItem.Type.LEGGINGS.getDurability(33))));
            addItem(gem+"_boots",()->new ArmorItem(holder,ArmorItem.Type.BOOTS,
                new Item.Properties().durability(ArmorItem.Type.BOOTS.getDurability(33))));
        }
    }
    static {
        for(String gem:List.of("ruby","sapphire","crystal")) {
            addGem(gem);
            addBlock(gem+"_ore",true);
            addBlock("deepslate_"+gem+"_ore",true);
            addBlock(gem+"_block",false);
            addGear(gem);
        }
    }
    public static void populateBlocks(CreativeModeTab.Output out) {
        for(DeferredItem<BlockItem> h:BLOCK_ITEMS) out.accept(((Supplier<? extends BlockItem>)h).get());
    }
    public static void populateItems(CreativeModeTab.Output out) {
        for(DeferredHolder<Item,? extends Item> h:COLLECTABLE_ITEMS) out.accept(((Supplier<? extends Item>)h).get());
    }
    public static void register(IEventBus bus) { BLOCKS.register(bus); ITEMS.register(bus); }
}
