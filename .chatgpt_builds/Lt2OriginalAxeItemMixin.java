package com.glaziolaicefox.lumberlands.mixin;

import com.glaziolaicefox.lumberlands.client.Lt2OriginalAxeRenderer;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Switches source-backed classic LT2 axes from approximated cuboids to genuine triangle meshes. */
@Mixin(ItemRenderer.class)
public abstract class Lt2OriginalAxeItemMixin {
    @Inject(method="render(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemDisplayContext;ZLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;IILnet/minecraft/client/resources/model/BakedModel;)V",
            at=@At("HEAD"),cancellable=true)
    private void lumberlands$renderOriginalAxe(ItemStack stack, ItemDisplayContext context,
                                                boolean leftHand, PoseStack pose, MultiBufferSource buffers,
                                                int light, int overlay, BakedModel model, CallbackInfo ci) {
        if (Lt2OriginalAxeRenderer.render(stack,context,leftHand,pose,buffers,light,overlay,model)) ci.cancel();
    }
}
