package com.glaziola.pixelmonrejuvenated;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.CreativeModeTab;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Orb IDs match Pixelmon 9.4.1; Cobblemon provides the three evolution stones. */
public final class BirdOrbs {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("pixelmonrejuvenated");
    public static final DeferredItem<Item> ORB = ITEMS.register("orb", () -> new Item(new Item.Properties().stacksTo(1)));
    public static final DeferredItem<BirdOrbItem> UNO = ITEMS.register("uno_orb", () -> new BirdOrbItem(new Item.Properties()));
    public static final DeferredItem<BirdOrbItem> DOS = ITEMS.register("dos_orb", () -> new BirdOrbItem(new Item.Properties()));
    public static final DeferredItem<BirdOrbItem> TRES = ITEMS.register("tres_orb", () -> new BirdOrbItem(new Item.Properties()));
    public static void register(IEventBus bus) { ITEMS.register(bus); }
    public static void populate(CreativeModeTab.Output output) {
        output.accept(ORB.get());output.accept(UNO.get());output.accept(DOS.get());output.accept(TRES.get());
    }
    private BirdOrbs() {}
}
