package com.glaziola.pixelmonrejuvenated;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SimpleWaterloggedBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.material.FluidState;
import net.minecraft.world.level.material.Fluids;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.minecraft.util.StringRepresentable;

/** Connected Pixelmon-style Temple Pillar with per-face connection state and geometry. */
public class TemplePillarBlock extends RotatedPillarBlock implements SimpleWaterloggedBlock {
    public enum Connection implements StringRepresentable {
        AIR("air"), PILLAR("pillar"), SOLID("solid");
        private final String name;
        Connection(String value) { this.name = value; }
        @Override public String getSerializedName() { return name; }
    }

    public static final EnumProperty<Connection> NORTH = EnumProperty.create("north", Connection.class);
    public static final EnumProperty<Connection> EAST = EnumProperty.create("east", Connection.class);
    public static final EnumProperty<Connection> SOUTH = EnumProperty.create("south", Connection.class);
    public static final EnumProperty<Connection> WEST = EnumProperty.create("west", Connection.class);
    public static final EnumProperty<Connection> UP = EnumProperty.create("up", Connection.class);
    public static final EnumProperty<Connection> DOWN = EnumProperty.create("down", Connection.class);
    public static final BooleanProperty WATERLOGGED = BlockStateProperties.WATERLOGGED;

    private boolean fractured() { return this instanceof FracturedTemplePillarBlock; }

    public TemplePillarBlock(BlockBehaviour.Properties properties) {
        super(properties);
        registerDefaultState(defaultBlockState()
            .setValue(AXIS, Direction.Axis.Y)
            .setValue(NORTH, Connection.AIR).setValue(EAST, Connection.AIR)
            .setValue(SOUTH, Connection.AIR).setValue(WEST, Connection.AIR)
            .setValue(UP, Connection.AIR).setValue(DOWN, Connection.AIR)
            .setValue(WATERLOGGED, false));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        super.createBlockStateDefinition(builder);
        builder.add(NORTH, EAST, SOUTH, WEST, UP, DOWN, WATERLOGGED);
    }

    private static EnumProperty<Connection> property(Direction direction) {
        return switch (direction) {
            case UP -> UP;
            case DOWN -> DOWN;
            case NORTH -> NORTH;
            case SOUTH -> SOUTH;
            case EAST -> EAST;
            case WEST -> WEST;
        };
    }

    private static Direction forward(Direction.Axis axis) {
        return switch (axis) {
            case X -> Direction.EAST;
            case Y -> Direction.UP;
            case Z -> Direction.SOUTH;
        };
    }

    private static Connection connected(LevelAccessor level, BlockPos neighborPos, Direction direction, BlockState other) {
        if (other.getBlock() instanceof TemplePillarBlock && other.getValue(AXIS) == direction.getAxis()) {
            return Connection.PILLAR;
        }
        if (other.isFaceSturdy(level, neighborPos, direction.getOpposite())) return Connection.SOLID;
        return Connection.AIR;
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        Direction.Axis axis = context.getClickedFace().getAxis();
        BlockPos pos = context.getClickedPos();
        LevelAccessor level = context.getLevel();
        Direction f = forward(axis);
        Direction b = f.getOpposite();
        return defaultBlockState().setValue(AXIS, axis)
            .setValue(property(f), connected(level, pos.relative(f), f, level.getBlockState(pos.relative(f))))
            .setValue(property(b), connected(level, pos.relative(b), b, level.getBlockState(pos.relative(b))))
            .setValue(WATERLOGGED, level.getFluidState(pos).getType() == Fluids.WATER);
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction facing, BlockState other,
            LevelAccessor level, BlockPos pos, BlockPos otherPos) {
        if (state.getValue(WATERLOGGED)) level.scheduleTick(pos, Fluids.WATER, Fluids.WATER.getTickDelay(level));
        if (facing.getAxis() == state.getValue(AXIS))
            return state.setValue(property(facing), connected(level, otherPos, facing, other));
        return super.updateShape(state, facing, other, level, pos, otherPos);
    }

    @Override
    public FluidState getFluidState(BlockState state) {
        return state.getValue(WATERLOGGED) ? Fluids.WATER.getSource(false) : super.getFluidState(state);
    }

    private VoxelShape pillarShape(BlockState state) {
        Direction.Axis axis = state.getValue(AXIS);
        Direction f = forward(axis);
        Connection positive = state.getValue(property(f));
        Connection negative = state.getValue(property(f.getOpposite()));
        VoxelShape shaft = switch (axis) {
            case X -> Block.box(0, 2, 2, 16, 14, 14);
            case Y -> Block.box(2, 0, 2, 14, 16, 14);
            case Z -> Block.box(2, 2, 0, 14, 14, 16);
        };
        if (fractured() && (positive == Connection.AIR || negative == Connection.AIR)) {
            shaft = Shapes.empty();
            if (positive == Connection.AIR) shaft = Shapes.or(shaft, switch (axis) {
                case X -> Block.box(0, 2, 2, 9, 14, 14);
                case Y -> Block.box(2, 0, 2, 14, 9, 14);
                case Z -> Block.box(2, 2, 0, 14, 14, 9);
            });
            if (negative == Connection.AIR) shaft = Shapes.or(shaft, switch (axis) {
                case X -> Block.box(7, 2, 2, 16, 14, 14);
                case Y -> Block.box(2, 7, 2, 14, 16, 14);
                case Z -> Block.box(2, 2, 7, 14, 14, 16);
            });
        }
        if (positive != Connection.PILLAR && (!fractured() || positive == Connection.SOLID)) {
            shaft = Shapes.or(shaft, switch (axis) {
                case X -> Block.box(13, 0, 0, 16, 16, 16);
                case Y -> Block.box(0, 13, 0, 16, 16, 16);
                case Z -> Block.box(0, 0, 13, 16, 16, 16);
            });
        }
        if (negative != Connection.PILLAR && (!fractured() || negative == Connection.SOLID)) {
            shaft = Shapes.or(shaft, switch (axis) {
                case X -> Block.box(0, 0, 0, 3, 16, 16);
                case Y -> Block.box(0, 0, 0, 16, 3, 16);
                case Z -> Block.box(0, 0, 0, 16, 16, 3);
            });
        }
        return shaft;
    }

    @Override
    public VoxelShape getShape(BlockState state, BlockGetter world, BlockPos pos, CollisionContext context) {
        return pillarShape(state);
    }

    @Override
    public VoxelShape getCollisionShape(BlockState state, BlockGetter world, BlockPos pos, CollisionContext context) {
        return pillarShape(state);
    }
}
