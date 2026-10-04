package dev.skycraft.client.mixin;

import dev.skycraft.client.SkyClient;
import dev.skycraft.client.SubnauticaCameraLink;
import net.minecraft.client.renderer.LevelRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Legacy SkyCraft mesh-host mode suppresses Minecraft's own level render because the host draws
 * exported geometry. The Subnautica compositor path is different: it must render the real
 * Minecraft world so Universal Modder's proven colour+depth exporter can capture it.
 */
@Mixin(LevelRenderer.class)
public abstract class LevelRendererMixin {
	@Inject(
		method = "render(Lcom/mojang/blaze3d/resource/GraphicsResourceAllocator;ZLnet/minecraft/client/renderer/state/level/CameraRenderState;Lcom/mojang/renderpearl/api/buffers/GpuBufferSlice;Lorg/joml/Vector4f;ZZ)V",
		at = @At("HEAD"),
		cancellable = true
	)
	private void skycraft$skipLevel(CallbackInfo ci) {
		if (SkyClient.linked() && !SubnauticaCameraLink.active()) {
			ci.cancel();
		}
	}
}
