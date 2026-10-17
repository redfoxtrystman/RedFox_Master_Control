package com.glaziola.pixelmonrejuvenated;

import com.mojang.serialization.Codec;
import java.util.ArrayList;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;

/** A single wild-tree feature selects uniformly among all registered berry varieties. */
public final class WildBerryTreeFeature extends Feature<NoneFeatureConfiguration> {
    public WildBerryTreeFeature(Codec<NoneFeatureConfiguration> codec) { super(codec); }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        var types = new ArrayList<>(BerryBlocks.LEAVES.keySet());
        if (types.isEmpty()) return false;
        String berry = types.get(context.random().nextInt(types.size()));
        return BerryTrees.place(context.level(), context.origin(), berry);
    }
}
