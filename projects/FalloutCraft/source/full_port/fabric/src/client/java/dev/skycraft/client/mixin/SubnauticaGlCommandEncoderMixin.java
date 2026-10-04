package dev.skycraft.client.mixin;

import com.mojang.renderpearl.api.buffers.GpuBuffer;
import com.mojang.renderpearl.api.textures.GpuTexture;
import com.mojang.renderpearl.backend.opengl.GlStateManager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Exact Minecraft 26.3 depth-readback fix from Universal Modder's working passthrough.
 *
 * A depth copy sets the read framebuffer's read buffer to GL_NONE and vanilla does not restore it.
 * Without this, the following colour readback can return "No color buffer"/garbage.
 */
@Mixin(targets = "com.mojang.renderpearl.backend.opengl.GlCommandEncoder")
abstract class SubnauticaGlCommandEncoderMixin {
	private static final int GL_COLOR_ATTACHMENT0 = 0x8CE0;

	@Inject(
		method = "copyTextureToBuffer(Lcom/mojang/renderpearl/api/textures/GpuTexture;Lcom/mojang/renderpearl/api/buffers/GpuBuffer;JLjava/lang/Runnable;IIIII)V",
		at = @At(
			value = "INVOKE",
			target = "Lcom/mojang/renderpearl/backend/opengl/GlStateManager;_glFramebufferTexture2D(IIIII)V"
		)
	)
	private void skycraft$restoreReadBufferAfterSubnauticaDepthCopy(
		GpuTexture source,
		GpuBuffer destination,
		long offset,
		Runnable callback,
		int mipLevel,
		int x,
		int y,
		int width,
		int height,
		CallbackInfo ci
	) {
		if (source.getFormat().hasDepthAspect()) {
			GlStateManager._glReadBuffer(GL_COLOR_ATTACHMENT0);
		}
	}
}
