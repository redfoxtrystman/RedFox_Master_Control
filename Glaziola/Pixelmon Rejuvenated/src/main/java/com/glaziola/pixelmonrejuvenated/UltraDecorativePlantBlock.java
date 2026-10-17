package com.glaziola.pixelmonrejuvenated;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.BushBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Low-profile Ultra Forest Flower: small targeted outline, not a full-block selection box. */
public class UltraDecorativePlantBlock extends BushBlock {
    private static final VoxelShape FLOWER_SHAPE = Block.box(2, 0, 2, 14, 4, 14);
    public UltraDecorativePlantBlock(BlockBehaviour.Properties properties) { super(properties); }
    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return FLOWER_SHAPE;
    }
}
