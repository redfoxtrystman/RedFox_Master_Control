package com.glaziolaicefox.lumberlands.client;

import com.glaziolaicefox.lumberlands.axe.Lt2AxeItem;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.InputStream;
import java.util.Map;
import java.util.Set;

/** Original 2017 LT2 ROBLOX axe triangle mesh, rendered directly from its decoded vertices.
 * Only axes verified to use the original shared mesh asset 145815658 are intercepted.
 * The axes added after the user's RBXL date deliberately keep their other model shapes. */
public final class Lt2OriginalAxeRenderer {
    private static final Set<String> SOURCE_BACKED = Set.of(
        "basic_hatchet", "plain_axe", "steel_axe", "hardened_axe", "silver_axe",
        "rukiryaxe", "end_times_axe", "alpha_axe", "beta_axe",
        "fire_axe", "candy_cane_axe", "chicken_axe", "gold_axe");
    private static final ResourceLocation BASE_TEXTURE =
        ResourceLocation.fromNamespaceAndPath("lumberlands", "textures/item/lt2_original_axe.png");
    private static final Map<String, ResourceLocation> TEXTURES = Map.of(
        "hardened_axe", ResourceLocation.fromNamespaceAndPath("lumberlands", "textures/item/lt2_original_hardened.png"),
        "beta_axe", ResourceLocation.fromNamespaceAndPath("lumberlands", "textures/item/lt2_original_beta.png"),
        "fire_axe", ResourceLocation.fromNamespaceAndPath("lumberlands", "textures/item/lt2_original_fire.png"));
    private static volatile float[] triangles;
    private static volatile boolean loadAttempted;

    public static boolean render(ItemStack item, ItemDisplayContext displayContext, boolean leftHand,
                                 PoseStack pose, MultiBufferSource buffers, int packedLight,
                                 int packedOverlay, BakedModel bakedModel) {
        if (!(item.getItem() instanceof Lt2AxeItem axe)) return false;
        String id = axe.definition().id();
        if (!SOURCE_BACKED.contains(id)) return false;
        float[] vertices = mesh();
        if (vertices == null) return false; // preserve vanilla fallback if assets are missing
        pose.pushPose();
        // Use the same display transforms the normal 3-D item model would receive.
        bakedModel.getTransforms().getTransform(displayContext).apply(leftHand, pose);
        pose.translate(0.5F,0.5F,0.5F);

        // Original Roblox mesh is centered on its own handle origin and measures roughly
        // 0.6 by 9.1 by 3.2 studs. It is normalized into one full Minecraft item height,
        // without replacing the actual vertex shapes or original per-vertex UVs.
        float size = 0.105F;
        if ("candy_cane_axe".equals(id) || "fire_axe".equals(id)) size=0.092F;
        pose.scale(size,size,size);
        VertexConsumer consumer = buffers.getBuffer(
            RenderType.entityCutoutNoCull(TEXTURES.getOrDefault(id, BASE_TEXTURE)));
        PoseStack.Pose p = pose.last();
        for (int i=0; i<vertices.length; i+=24) {
            for (int n=0; n<3; n++) vertex(consumer, p, vertices, i+n*8, packedLight, packedOverlay);
            // Modern Minecraft's entity cutout pipeline is quads, not triangles.
            // Duplicate the third vertex to preserve the original triangle precisely.
            vertex(consumer, p, vertices, i+16, packedLight, packedOverlay);
        }
        pose.popPose();
        return true;
    }

    private static void vertex(VertexConsumer out, PoseStack.Pose pose, float[] v, int i,
                               int packedLight, int packedOverlay) {
        out.addVertex(pose, v[i],v[i+1],v[i+2])
            .setColor(255,255,255,255)
            .setUv(v[i+6],v[i+7])
            .setOverlay(packedOverlay)
            .setLight(packedLight)
            .setNormal(pose,v[i+3],v[i+4],v[i+5]);
    }

    private static synchronized float[] mesh() {
        if (loadAttempted) return triangles;
        loadAttempted=true;
        try (InputStream input=Lt2OriginalAxeRenderer.class.getResourceAsStream(
                    "/assets/lumberlands/meshes/lt2_original_axe.bin")) {
            if (input == null) return null;
            DataInputStream in = new DataInputStream(new BufferedInputStream(input));
            int count = in.readInt();
            if (count != 6504) return null;
            float[] data=new float[count*8];
            for (int i=0;i<data.length;i++) data[i]=in.readFloat();
            triangles=data;
        } catch (Exception ignored) {
            triangles=null;
        }
        return triangles;
    }
    private Lt2OriginalAxeRenderer(){}
}
