package com.glaziola.pixelmonrejuvenated;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Standard NeoForge deferred worldgen feature registration. */
public final class BerryWorldgen {
    private static final DeferredRegister<Feature<?>> FEATURES =
        DeferredRegister.create(Registries.FEATURE, "pixelmonrejuvenated");
    static {
        FEATURES.register("wild_berry_tree", () -> new WildBerryTreeFeature(NoneFeatureConfiguration.CODEC));
    }
    private BerryWorldgen() {}
    public static void register(IEventBus bus) { FEATURES.register(bus); }
}
