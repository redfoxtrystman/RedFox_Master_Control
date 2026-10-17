package com.glaziola.pixelmonrejuvenated;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

/** Registers Spirit Pokemon, Ultra Space materials, and classic Pixelmon building decorations. */
@Mod("pixelmonrejuvenated")
public final class PixelmonRejuvenated {
    public PixelmonRejuvenated(IEventBus modBus) {
        UltraSpaceBlocks.register(modBus);
        DecorativeBlocks.register(modBus);
        BerryWoodBlocks.register(modBus);
        ExtraPixelmonBlocks.register(modBus);
        BerryBlocks.register(modBus);
        StoneEquipment.register(modBus);
        GemContent.register(modBus);
        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.register(BerryPlanting.class);
        SpiritOctoberSpawns.initialize();
    }
}
