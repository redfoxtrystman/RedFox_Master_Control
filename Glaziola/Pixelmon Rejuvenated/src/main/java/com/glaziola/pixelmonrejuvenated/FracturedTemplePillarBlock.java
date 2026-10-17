package com.glaziola.pixelmonrejuvenated;

import net.minecraft.world.level.block.state.BlockBehaviour;

/** Distinguishes fractured temple pillars during registry/cache initialization without registry lookups. */
public final class FracturedTemplePillarBlock extends TemplePillarBlock {
    public FracturedTemplePillarBlock(BlockBehaviour.Properties properties) {
        super(properties);
    }
}
