package dev.skycraft.client;

import com.mojang.blaze3d.pipeline.RenderTarget;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.renderpearl.api.buffers.GpuBuffer;
import com.mojang.renderpearl.api.buffers.GpuBufferSlice;
import com.mojang.renderpearl.api.commands.CommandEncoder;
import dev.skycraft.SkyCraft;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.VarHandle;
import org.joml.Vector4f;

/**
 * Source-backed colour+depth+overlay exporter adapted from Universal Modder's working
 * examples/minecraft-gta5-passthrough Minecraft 26.3 FrameExporter.
 *
 * Slot data is world RGBA8, world depth float32, then hand/HUD RGBA8.
 */
public final class SubnauticaFrameExporter {
	public static final String NAME = "Local\\SkyCraft_Subnautica_Frame_v1";
	private static final int MAGIC = 0x46435353; // "SSCF" little-endian
	private static final int VERSION = 1;
	private static final int HEADER = 4096;
	private static final int SLOTS = 3;
	private static final int SLOT_DESC = 256;
	private static final int SLOT_DESC_BYTES = 128;
	private static final int MAX_W = 3840;
	private static final int MAX_H = 2160;
	private static final long LAYER_MAX = (long) MAX_W * MAX_H * 4L;
	private static final long STRIDE = LAYER_MAX * 3L;
	private static final int RING = 3;
	private static final long STUCK_NANOS = 1_000_000_000L;
	private static final Vector4f TRANSPARENT = new Vector4f(0.0F, 0.0F, 0.0F, 0.0F);

	private static final ValueLayout.OfInt INT = ValueLayout.JAVA_INT_UNALIGNED;
	private static final ValueLayout.OfLong LONG = ValueLayout.JAVA_LONG_UNALIGNED;
	private static final ValueLayout.OfFloat FLOAT = ValueLayout.JAVA_FLOAT_UNALIGNED;
	private static final ValueLayout.OfDouble DOUBLE = ValueLayout.JAVA_DOUBLE_UNALIGNED;

	private static SubnauticaFrameMemory shm;
	private static boolean failed;
	private static boolean warnedSize;
	private static final Capture[] ring = new Capture[RING];
	private static int ringNext;
	private static int slotNext;
	private static long frameCounter;
	private static long publishCounter;
	private static Capture current;
	private static boolean loggedPublish;

	private SubnauticaFrameExporter() {}

	private static final class Capture {
		GpuBuffer color;
		GpuBuffer depth;
		GpuBuffer overlay;
		int width;
		int height;
		long generation;
		boolean busy;
		long busySince;
		SubnauticaCameraLink.Pose pose;
		float far;
		long frame;
		long captureNanos;

		void allocate(int w, int h) {
			free();
			long n = (long) w * h * 4L;
			int usage = GpuBuffer.USAGE_MAP_READ | GpuBuffer.USAGE_COPY_DST;
			color = RenderSystem.getDevice().createBuffer(() -> "Subnautica passthrough world colour", usage, n);
			depth = RenderSystem.getDevice().createBuffer(() -> "Subnautica passthrough world depth", usage, n);
			overlay = RenderSystem.getDevice().createBuffer(() -> "Subnautica passthrough overlay", usage, n);
			width = w;
			height = h;
		}

		void free() {
			for (GpuBuffer b : new GpuBuffer[]{ color, depth, overlay }) {
				if (b != null) {
					b.close();
				}
			}
			color = depth = overlay = null;
		}
	}

	private static boolean ensureShm() {
		if (shm != null) {
			return true;
		}
		if (failed) {
			return false;
		}

		try {
			shm = SubnauticaFrameMemory.create(NAME, HEADER + STRIDE * SLOTS);
			MemorySegment m = shm.segment;
			m.set(INT, 0, MAGIC);
			m.set(INT, 4, VERSION);
			m.set(INT, 8, HEADER);
			m.set(INT, 12, SLOTS);
			m.set(LONG, 16, STRIDE);
			m.set(INT, 24, MAX_W);
			m.set(INT, 28, MAX_H);
			m.set(INT, 40, -1);
			m.set(INT, 44, (int) ProcessHandle.current().pid());
			SkyCraft.LOG.info(
				"SkyCraft Subnautica frame export: shared memory {} ({} MB)",
				NAME, (HEADER + STRIDE * SLOTS) >> 20
			);
			return true;
		} catch (Throwable t) {
			failed = true;
			SkyCraft.LOG.error("SkyCraft Subnautica frame export disabled: couldn't create shared memory", t);
			return false;
		}
	}

	/**
	 * GameRenderer.renderLevel, immediately before render3dHud (hand):
	 * capture the complete Minecraft world colour+depth, then clear colour so everything after it
	 * becomes the separate hand/HUD/screen layer.
	 */
	public static void captureWorld(RenderTarget target) {
		current = null;
		SubnauticaCameraLink.Pose pose = SubnauticaCameraLink.frame();
		if (pose == null || !ensureShm()) {
			return;
		}

		int w = target.width;
		int h = target.height;
		if ((long) w * h * 4L > LAYER_MAX) {
			if (!warnedSize) {
				warnedSize = true;
				SkyCraft.LOG.warn(
					"SkyCraft Subnautica frame export: {}x{} exceeds {}x{}",
					w, h, MAX_W, MAX_H
				);
			}
			return;
		}

		Capture c = ring[ringNext];
		if (c == null) {
			c = ring[ringNext] = new Capture();
		}

		long now = System.nanoTime();
		if (c.busy && now - c.busySince < STUCK_NANOS) {
			return;
		}
		if (c.width != w || c.height != h || c.color == null) {
			c.allocate(w, h);
		}

		c.generation++;
		c.busy = true;
		c.busySince = now;
		c.pose = pose;
		c.far = pose.farClip();
		c.frame = ++frameCounter;
		c.captureNanos = now;

		CommandEncoder encoder = RenderSystem.getDevice().createCommandEncoder();
		encoder.copyTextureToBuffer(target.getColorTexture(), c.color, 0L, () -> {}, 0);
		encoder.copyTextureToBuffer(target.getDepthTexture(), c.depth, 0L, () -> {}, 0);
		encoder.clearColorTexture(target.getColorTexture(), TRANSPARENT);
		current = c;
	}

	/** End of GameRenderer.render: the hand/HUD/GUI layer is complete. */
	public static void captureOverlay(RenderTarget target) {
		Capture c = current;
		current = null;
		if (c == null) {
			return;
		}
		if (target.width != c.width || target.height != c.height) {
			c.busy = false;
			return;
		}

		long generation = c.generation;
		RenderSystem.getDevice().createCommandEncoder().copyTextureToBuffer(
			target.getColorTexture(),
			c.overlay,
			0L,
			() -> {
				if (c.generation == generation && c.busy) {
					publish(c);
				}
			},
			0
		);
		ringNext = (ringNext + 1) % RING;
	}

	private static void publish(Capture c) {
		try {
			MemorySegment m = shm.segment;
			int slot = slotNext;
			slotNext = (slotNext + 1) % SLOTS;
			long desc = SLOT_DESC + (long) SLOT_DESC_BYTES * slot;
			long seq = m.get(LONG, desc);
			if ((seq & 1L) != 0L) {
				seq++;
			}

			m.set(LONG, desc, seq + 1L);
			VarHandle.fullFence();

			long base = HEADER + STRIDE * slot;
			long n = (long) c.width * c.height * 4L;
			copy(c.color, m, base, n);
			copy(c.depth, m, base + n, n);
			copy(c.overlay, m, base + 2L * n, n);

			SubnauticaCameraLink.Pose p = c.pose;
			m.set(LONG, desc + 8, c.frame);
			m.set(LONG, desc + 16, p.hostFrame());
			m.set(INT, desc + 24, c.width);
			m.set(INT, desc + 28, c.height);
			m.set(FLOAT, desc + 32, Math.max(0.001F, p.nearClip()));
			m.set(FLOAT, desc + 36, Math.max(p.nearClip() + 1.0F, c.far));
			m.set(FLOAT, desc + 40, p.fov());
			m.set(INT, desc + 44,
				(RenderSystem.getDevice().getDeviceInfo().isZZeroToOne() ? 1 : 0) | 2 | 4);
			m.set(DOUBLE, desc + 48, p.x());
			m.set(DOUBLE, desc + 56, p.y());
			m.set(DOUBLE, desc + 64, p.z());
			m.set(FLOAT, desc + 72, p.yaw());
			m.set(FLOAT, desc + 76, p.pitch());
			m.set(FLOAT, desc + 80, p.roll());
			m.set(INT, desc + 84, p.firstPerson() ? 1 : 0);
			m.set(LONG, desc + 88, c.captureNanos);
			m.set(LONG, desc + 96, System.nanoTime());

			VarHandle.fullFence();
			m.set(LONG, desc, seq + 2L);
			m.set(INT, 40, slot);
			VarHandle.fullFence();
			m.set(LONG, 32, ++publishCounter);

			if (!loggedPublish) {
				loggedPublish = true;
				SkyCraft.LOG.info(
					"SkyCraft render proof: published Subnautica passthrough world+depth+HUD frame {} ({}x{})",
					c.frame, c.width, c.height
				);
			}
		} catch (RuntimeException e) {
			SkyCraft.LOG.warn("SkyCraft Subnautica frame export failed", e);
		} finally {
			c.busy = false;
		}
	}

	private static void copy(GpuBuffer buffer, MemorySegment dst, long offset, long n) {
		try (GpuBufferSlice.MappedView view = buffer.map(true, false)) {
			MemorySegment.copy(MemorySegment.ofBuffer(view.data()), 0L, dst, offset, n);
		}
	}
}
