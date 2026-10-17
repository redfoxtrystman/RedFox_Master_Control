package com.glaziola.pixelmonrejuvenated;

import net.minecraft.core.Direction;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Original Pixelmon berry-log parity: narrow post and directional side branches.
 *  Berry logs and berry leaves attach to the log; ordinary solid cubes do not.
 */
public final class RejuvenatedBerryLog extends WallBlock {
    public RejuvenatedBerryLog(BlockBehaviour.Properties properties) {
        super(properties);
    }

    @Override
    public boolean connectsTo(BlockState neighbor, boolean faceFull, Direction direction) {
        Block block = neighbor.getBlock();
        return block instanceof RejuvenatedBerryLog || block instanceof RejuvenatedBerryLeaves;
    }

    public static DeferredBlock<Block> register(DeferredRegister.Blocks registry, String name,
                                                BlockBehaviour.Properties properties) {
        return registry.registerBlock(name, p -> (Block)new RejuvenatedBerryLog(p), properties.noOcclusion());
    }
}
