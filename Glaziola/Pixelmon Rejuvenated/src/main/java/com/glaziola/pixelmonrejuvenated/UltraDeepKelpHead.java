package com.glaziola.pixelmonrejuvenated;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.KelpBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import java.util.function.Supplier;
/** One collectible Ultra Deep Kelp item, matching Pixelmon's head -> custom stem conversion. */
public final class UltraDeepKelpHead extends KelpBlock {
    public UltraDeepKelpHead(BlockBehaviour.Properties properties) { super(properties); }
    @Override protected Block getBodyBlock() {
        return ((Supplier<? extends Block>)UltraSpaceExpansion.ULTRA_DEEP_KELP_PLANT).get();
    }
}
