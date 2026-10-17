package com.glaziola.pixelmonrejuvenated;

import com.mojang.serialization.MapCodec;
import net.minecraft.world.level.block.FallingBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;

/** Standard vanilla falling-block physics with NeoForge/Minecraft 1.21.1 codec. */
public final class UltraFallingBlock extends FallingBlock {
    public static final MapCodec<UltraFallingBlock> CODEC = simpleCodec(UltraFallingBlock::new);

    public UltraFallingBlock(BlockBehaviour.Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends FallingBlock> codec() {
        return CODEC;
    }
}
