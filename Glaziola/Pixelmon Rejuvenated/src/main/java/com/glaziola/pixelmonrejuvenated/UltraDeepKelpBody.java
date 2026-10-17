package com.glaziola.pixelmonrejuvenated;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.KelpBlock;
import net.minecraft.world.level.block.GrowingPlantHeadBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import java.util.function.Supplier;
/** Non-item internal kelp stem; growing or stacking never converts to vanilla Minecraft kelp. */
public final class UltraDeepKelpBody extends KelpBlock {
    public UltraDeepKelpBody(BlockBehaviour.Properties properties) { super(properties); }
    @Override protected GrowingPlantHeadBlock getHeadBlock() {
        return (GrowingPlantHeadBlock)((Supplier<? extends Block>)UltraSpaceExpansion.ULTRA_DEEP_KELP).get();
    }
    @Override protected Block getBodyBlock() {
        return ((Supplier<? extends Block>)UltraSpaceExpansion.ULTRA_DEEP_KELP_PLANT).get();
    }
}
