package com.glaziola.pixelmonrejuvenated;

import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

/** SoundType mapping based on Pixelmon 9.4.1, with requested Unown/Braille stone override.
 * Minecraft defaults to STONE when Pixelmon did not override the sound. */
public final class UltraSoundParity {
    private UltraSoundParity() {}
    public static BlockBehaviour.Properties apply(String id, BlockBehaviour.Properties p) {
        // Pixelmon Rejuvenated user-requested sound override for ALL 29 Unown and
        // ALL 30 Braille blocks. Stone, not the upstream WOOD assignment.
        if (id.startsWith("unown_block_") || id.startsWith("braille_block_")) {
            return p.sound(SoundType.STONE);
        }

        switch (id) {
            case "window1":
            case "window2":
                return p.sound(SoundType.GLASS);
            case "poke_dirt":
            case "poke_grass":
            case "ultra_elm_leaves":
            case "ultra_elm_sapling":
            case "ultra_forest_fallen_leaves":
            case "ultra_forest_flower":
            case "ultra_ginkgo_leaves":
            case "ultra_ginkgo_sapling":
            case "ultra_jungle_leaves":
            case "ultra_jungle_sapling":
                return p.sound(SoundType.GRASS);
            case "poke_sand":
            case "poke_sand_corner1":
            case "poke_sand_corner2":
            case "poke_sand_corner3":
            case "poke_sand_corner4":
            case "poke_sand_side1":
            case "poke_sand_side2":
            case "poke_sand_side3":
            case "poke_sand_side4":
            case "sandy_grass":
                return p.sound(SoundType.SAND);
            // Keep falling blocks' original granular sounds, not the STONE fallback.
            case "ultra_desert_sand":
            case "ultra_desert_gilded_sand":
                return p.sound(SoundType.SAND);
            case "ultra_deep_gravel":
                return p.sound(SoundType.GRAVEL);
            case "ultra_deep_sea_pickle":
                return p.sound(SoundType.SLIME_BLOCK);
            case "ultra_jungle_vine":
                return p.sound(SoundType.VINE);
            case "ultra_deep_kelp":
            case "ultra_deep_kelp_plant":
            case "ultra_deep_seagrass":
            case "ultra_deep_tall_seagrass":
                return p.sound(SoundType.WET_GRASS);
            case "inside_wall":
            case "inside_wall_moulding":
            case "outside_wall":
            case "poke_center_sign":
            case "poke_mart_sign":
            case "stripped_ultra_elm_log":
            case "stripped_ultra_elm_wood":
            case "stripped_ultra_ginkgo_log":
            case "stripped_ultra_ginkgo_wood":
            case "stripped_ultra_jungle_log":
            case "stripped_ultra_jungle_wood":
            case "ultra_elm_button":
            case "ultra_elm_door":
            case "ultra_elm_fence":
            case "ultra_elm_fence_gate":
            case "ultra_elm_log":
            case "ultra_elm_planks":
            case "ultra_elm_pressure_plate":
            case "ultra_elm_slab":
            case "ultra_elm_trapdoor":
            case "ultra_elm_wood":
            case "ultra_ginkgo_button":
            case "ultra_ginkgo_door":
            case "ultra_ginkgo_fence":
            case "ultra_ginkgo_fence_gate":
            case "ultra_ginkgo_log":
            case "ultra_ginkgo_planks":
            case "ultra_ginkgo_pressure_plate":
            case "ultra_ginkgo_slab":
            case "ultra_ginkgo_trapdoor":
            case "ultra_ginkgo_wood":
            case "ultra_jungle_button":
            case "ultra_jungle_door":
            case "ultra_jungle_fence":
            case "ultra_jungle_fence_gate":
            case "ultra_jungle_log":
            case "ultra_jungle_planks":
            case "ultra_jungle_pressure_plate":
            case "ultra_jungle_slab":
            case "ultra_jungle_trapdoor":
            case "ultra_jungle_wood":
            case "wooden_flooring":
                return p.sound(SoundType.WOOD);
            case "ultra_desert_cactus":
                return p.sound(SoundType.WOOL);
            default: return p.sound(SoundType.STONE);
        }
    }
}
