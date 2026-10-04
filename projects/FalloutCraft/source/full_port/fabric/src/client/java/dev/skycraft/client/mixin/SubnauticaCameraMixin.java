package dev.skycraft.client.mixin;

import dev.skycraft.client.SubnauticaCameraLink;
import net.minecraft.client.Camera;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.Vec3;
import org.joml.Quaternionf;
import org.joml.Vector3f;
import org.joml.Vector3fc;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Directly adapted from Universal Modder's working Minecraft/GTA CameraMixin for Minecraft 26.3.
 * Subnautica's MainCamera.camera becomes Minecraft's render camera: position, rotation, roll and FOV.
 */
@Mixin(Camera.class)
abstract class SubnauticaCameraMixin {
	private static final float DEG = (float)(Math.PI / 180.0);

	@Shadow @Final private static Vector3fc FORWARDS;
	@Shadow @Final private static Vector3fc UP;
	@Shadow @Final private static Vector3fc LEFT;
	@Shadow @Final private Vector3f forwards;
	@Shadow @Final private Vector3f up;
	@Shadow @Final private Vector3f left;
	@Shadow @Final private Quaternionf rotation;
	@Shadow private float xRot;
	@Shadow private float yRot;
	@Shadow private boolean detached;
	@Shadow private int matrixPropertiesDirty;

	@Shadow
	protected abstract void setPosition(double x, double y, double z);

	@Inject(method = "update", at = @At("HEAD"))
	private void skycraft$subnauticaBeginCameraFrame(DeltaTracker deltaTracker, CallbackInfo ci) {
		SubnauticaCameraLink.beginFrame();
	}

	@Inject(method = "alignWithEntity", at = @At("TAIL"))
	private void skycraft$subnauticaHostCamera(float partialTicks, CallbackInfo ci) {
		SubnauticaCameraLink.Pose p = SubnauticaCameraLink.frame();
		if (p == null) {
			return;
		}

		this.xRot = p.pitch();
		this.yRot = p.yaw();
		this.rotation.rotationYXZ(
			(float)Math.PI - p.yaw() * DEG,
			-p.pitch() * DEG,
			p.roll() * DEG
		);
		FORWARDS.rotate(this.rotation, this.forwards);
		UP.rotate(this.rotation, this.up);
		LEFT.rotate(this.rotation, this.left);
		this.matrixPropertiesDirty |= 3;
		this.setPosition(p.x(), p.y(), p.z());

		Entity player = Minecraft.getInstance().player;
		boolean inside = player != null
			&& player.getEyePosition(partialTicks).distanceToSqr(p.x(), p.y(), p.z()) < 0.8 * 0.8;
		this.detached = !p.firstPerson() && !inside;
	}

	@Inject(method = "calculateFov", at = @At("HEAD"), cancellable = true)
	private void skycraft$subnauticaHostFov(
		float partialTicks,
		CallbackInfoReturnable<Float> cir
	) {
		SubnauticaCameraLink.Pose p = SubnauticaCameraLink.frame();
		if (p != null) {
			cir.setReturnValue(p.fov());
		}
	}
}
