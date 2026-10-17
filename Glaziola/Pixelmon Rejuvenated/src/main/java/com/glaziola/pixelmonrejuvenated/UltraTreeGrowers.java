package com.glaziola.pixelmonrejuvenated;

import java.util.Optional;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;

/** Pixelmon 9.4.1 tree grower option layout, with Rejuvenated-native feature IDs.
 * The full Pixelmon custom trunk placers are not in the base game; the
 * bundled configured features adapt those structures with vanilla placers. */
public final class UltraTreeGrowers {
    private UltraTreeGrowers() {}

    private static ResourceKey<ConfiguredFeature<?, ?>> key(String path) {
        return ResourceKey.create(Registries.CONFIGURED_FEATURE,
            ResourceLocation.fromNamespaceAndPath("pixelmonrejuvenated", "trees/" + path));
    }

    // Pixelmon: elm/jungle normal feature slots, Ginkgo large-tree/2x2 slot.
    public static final TreeGrower ULTRA_ELM =
        new TreeGrower("ultra_elm", Optional.of(key("ultra_elm")), Optional.empty(), Optional.empty());
    public static final TreeGrower ULTRA_GINKGO =
        new TreeGrower("ultra_ginkgo", Optional.empty(), Optional.of(key("ginkgo")), Optional.empty());
    public static final TreeGrower ULTRA_JUNGLE =
        new TreeGrower("ultra_jungle", Optional.of(key("ultra_jungle")), Optional.empty(), Optional.empty());
}
