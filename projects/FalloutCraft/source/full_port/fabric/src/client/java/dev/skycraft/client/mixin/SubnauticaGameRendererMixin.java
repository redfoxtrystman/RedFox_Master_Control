package dev.skycraft.client.mixin;

import com.mojang.blaze3d.pipeline.RenderTarget;
import dev.skycraft.client.SubnauticaCameraLink;
import dev.skycraft.client.SubnauticaFrameExporter;
import net.minecraft.client.renderer.GameRenderer;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyArg;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Direct port of Universal Modder's working Minecraft 26.3 passthrough GameRendererMixin.
 *
 * While the Subnautica camera is live:
 * - Minecraft still renders its world (required for colour+depth export);
 * - host sky is allowed to show through;
 * - world colour+depth is captured immediately before the 3D hand;
 * - hand/HUD/screens are captured separately at render tail.
 */
@Mixin(GameRenderer.class)
abstract class SubnauticaGameRendererMixin {
	@Shadow @Final private RenderTarget mainRenderTarget;

	@ModifyArg(
		method = "renderLevel",
		at = @At(
			value = "INVOKE",
			target = "Lnet/minecraft/client/renderer/LevelRenderer;render(Lcom/mojang/blaze3d/resource/GraphicsResourceAllocator;ZLnet/minecraft/client/renderer/state/level/CameraRenderState;Lcom/mojang/renderpearl/api/buffers/GpuBufferSlice;Lorg/joml/Vector4f;ZZ)V"
		),
		index = 5
	)
	private boolean skycraft$subnauticaNoSky(boolean shouldRenderSky) {
		return shouldRenderSky && !SubnauticaCameraLink.active();
	}

	@Inject(
		method = "renderLevel",
		at = @At(
			value = "INVOKE",
			target = "Lnet/minecraft/client/renderer/GameRenderer;render3dHud(Lnet/minecraft/client/renderer/state/level/CameraRenderState;Lnet/minecraft/client/renderer/state/level/PlayerRenderState;Lnet/minecraft/client/renderer/state/OptionsRenderState;Z)V"
		)
	)
	private void skycraft$captureSubnauticaWorld(CallbackInfo ci) {
		if (SubnauticaCameraLink.active()) {
			SubnauticaFrameExporter.captureWorld(this.mainRenderTarget);
		}
	}

	@Inject(method = "render", at = @At("TAIL"))
	private void skycraft$captureSubnauticaOverlay(CallbackInfo ci) {
		if (SubnauticaCameraLink.active()) {
			SubnauticaFrameExporter.captureOverlay(this.mainRenderTarget);
		}
	}
}
