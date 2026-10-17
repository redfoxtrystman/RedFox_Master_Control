package com.glaziola.pixelmonrejuvenated;

import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.EntityCollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** The trap becomes non-solid for a player after 300 ticks of sustained contact. */
public final class TimedFallBlock extends Block {
    private static final int COLLAPSE_TICKS = 300;
    private static final int RESET_GAP = 4;
    private static final ConcurrentMap<StandKey, Counter> CONTACTS = new ConcurrentHashMap<>();
    private record StandKey(UUID player, long pos, boolean clientSide) {}
    private record Counter(int began, int lastSeen) {}

    public TimedFallBlock(BlockBehaviour.Properties properties) { super(properties); }

    @Override
    public VoxelShape getCollisionShape(BlockState state, BlockGetter world, BlockPos pos, CollisionContext context) {
        if (context instanceof EntityCollisionContext entityContext
                && entityContext.getEntity() instanceof Player player) {
            int tick = player.tickCount;
            StandKey key = new StandKey(player.getUUID(), pos.asLong(), player.level().isClientSide);
            Counter c = CONTACTS.compute(key, (ignored, existing) -> {
                if (existing == null || tick < existing.began() || tick - existing.lastSeen() > RESET_GAP)
                    return new Counter(tick, tick);
                return new Counter(existing.began(), tick);
            });
            if (CONTACTS.size() > 4096)
                CONTACTS.entrySet().removeIf(e -> e.getValue().lastSeen() < tick - 1200);
            if (tick - c.began() >= COLLAPSE_TICKS)
                return Shapes.empty();
        }
        return super.getCollisionShape(state, world, pos, context);
    }
}
