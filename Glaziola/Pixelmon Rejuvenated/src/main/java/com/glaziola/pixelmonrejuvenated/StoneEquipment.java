package com.glaziola.pixelmonrejuvenated;

import java.util.*;
import java.util.function.*;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.*;

/** Pixelmon 9.4.1 evolution-stone armor and tool port; stones are Cobblemon items. */
public final class StoneEquipment {
    public static final String MODID="pixelmonrejuvenated";
    public static final DeferredRegister.Items ITEMS=DeferredRegister.createItems(MODID);
    public static final DeferredRegister<CreativeModeTab> TABS=DeferredRegister.create(Registries.CREATIVE_MODE_TAB,MODID);
    private static final List<DeferredHolder<Item,? extends Item>> ALL=new ArrayList<>();
    private StoneEquipment(){}

    private static Item stoneIngredient(String name) {
        return BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("cobblemon",name));
    }
    private static Tier tier(String stone, int enchant, float attack){
        return new Tier() {
            @Override public int getUses(){return 1561;}
            @Override public float getSpeed(){return 8.0f;}
            @Override public float getAttackDamageBonus(){return attack;}
            @Override public int getEnchantmentValue(){return enchant;}
            @Override public TagKey<Block> getIncorrectBlocksForDrops(){return BlockTags.INCORRECT_FOR_DIAMOND_TOOL;}
            @Override public Ingredient getRepairIngredient(){return Ingredient.of((ItemLike)stoneIngredient(stone));}
        };
    }
    private static ArmorMaterial material(String stone,int enchant) {
        Map<ArmorItem.Type,Integer> defense=Map.of(ArmorItem.Type.HELMET,3,ArmorItem.Type.CHESTPLATE,7,ArmorItem.Type.LEGGINGS,6,ArmorItem.Type.BOOTS,3);
        String layer=stone.replace("_","");
        return new ArmorMaterial(defense,enchant,SoundEvents.ARMOR_EQUIP_IRON,
            () -> Ingredient.of((ItemLike)stoneIngredient(stone)),
            List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(MODID,layer))),0.0f,0.0f);
    }
    private static void add(String name, Supplier<? extends Item> supplier) {
        ALL.add(ITEMS.register(name,supplier));
    }
    private static void registerSet(String stone, int enchant, float attack){
        final Tier t=tier(stone,enchant,attack);
        final ArmorMaterial m=material(stone,enchant);
        final Holder<ArmorMaterial> h=Holder.direct(m);
        add(stone+"_sword",()->new SwordItem(t,new Item.Properties().durability(t.getUses()).attributes(SwordItem.createAttributes(t, 3, -2.4f))));
        add(stone+"_pickaxe",()->new PickaxeItem(t,new Item.Properties().durability(t.getUses()).attributes(DiggerItem.createAttributes(t, 1.0f, -2.8f))));
        add(stone+"_axe",()->new AxeItem(t,new Item.Properties().durability(t.getUses()).attributes(DiggerItem.createAttributes(t, 5.0f, -3.0f))));
        add(stone+"_shovel",()->new ShovelItem(t,new Item.Properties().durability(t.getUses()).attributes(DiggerItem.createAttributes(t, 1.5f, -3.0f))));
        add(stone+"_hoe",()->new HoeItem(t,new Item.Properties().durability(t.getUses()).attributes(DiggerItem.createAttributes(t, -t.getAttackDamageBonus(), -1.0f))));
        // Initial vanilla-functional hammer tool; custom Pixelmon anvil/3x3 behavior is tracked separately.
        add(stone+"_hammer",()->new PickaxeItem(t,new Item.Properties().durability(t.getUses()).attributes(DiggerItem.createAttributes(t, 1.0f, -2.8f))));
        add(stone+"_helmet",()->new ArmorItem(h,ArmorItem.Type.HELMET,new Item.Properties().durability(ArmorItem.Type.HELMET.getDurability(33))));
        add(stone+"_chestplate",()->new ArmorItem(h,ArmorItem.Type.CHESTPLATE,new Item.Properties().durability(ArmorItem.Type.CHESTPLATE.getDurability(33))));
        add(stone+"_leggings",()->new ArmorItem(h,ArmorItem.Type.LEGGINGS,new Item.Properties().durability(ArmorItem.Type.LEGGINGS.getDurability(33))));
        add(stone+"_boots",()->new ArmorItem(h,ArmorItem.Type.BOOTS,new Item.Properties().durability(ArmorItem.Type.BOOTS.getDurability(33))));
    }
    static {
        registerSet("fire_stone",10,4.0f);
        registerSet("water_stone",10,4.0f);
        registerSet("leaf_stone",14,2.0f);
        registerSet("thunder_stone",22,0.0f);
        registerSet("sun_stone",22,0.0f);
        registerSet("moon_stone",22,0.0f);
        registerSet("dawn_stone",22,0.0f);
        registerSet("dusk_stone",22,0.0f);
        registerSet("ice_stone",22,0.0f);
        registerSet("shiny_stone",22,0.0f);
    }
    public static final DeferredHolder<CreativeModeTab,CreativeModeTab> PIXELMON_ITEMS_TAB =
        TABS.register("pixelmon_items",()->CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.pixelmonrejuvenated.pixelmon_items"))
            .withTabsBefore(CreativeModeTabs.SPAWN_EGGS)
            .icon(()->new ItemStack(((Supplier<? extends Item>)ALL.get(0)).get()))
            .displayItems(new CreativeModeTab.DisplayItemsGenerator() {
                @Override public void accept(CreativeModeTab.ItemDisplayParameters p, CreativeModeTab.Output o) {
                    for(DeferredHolder<Item,? extends Item> item : ALL) o.accept(((Supplier<? extends Item>)item).get());
                    GemContent.populateItems(o);
                }
            }).build());
    public static void register(IEventBus bus) { ITEMS.register(bus);TABS.register(bus); }
}
