package dev.skycraft.client;

import java.lang.foreign.Arena;
import java.lang.foreign.FunctionDescriptor;
import java.lang.foreign.Linker;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.SymbolLookup;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.VarHandle;
import java.nio.charset.StandardCharsets;

/**
 * Read-only Minecraft view of Subnautica's MainCamera.camera state.
 *
 * Layout mirrors SubnauticaCameraProtocol.cs. This is deliberately separate from SkyCraft protocol v11.
 */
public final class SubnauticaCameraLink {
	public static final String NAME = "Local\\SkyCraft_Subnautica_Camera_v1";
	private static final int MAGIC = 0x4D414353;
	private static final int VERSION = 1;
	private static final long BYTES = 4096;
	private static final long TIMEOUT_MS = 2000;

	private static final int FILE_MAP_READ = 0x0004;

	private static final long O_MAGIC = 0x00;
	private static final long O_VERSION = 0x04;
	private static final long O_HEARTBEAT = 0x10;
	private static final long O_SEQ = 0x20;
	private static final long O_HOST_FRAME = 0x28;
	private static final long O_X = 0x30;
	private static final long O_Y = 0x38;
	private static final long O_Z = 0x40;
	private static final long O_YAW = 0x48;
	private static final long O_PITCH = 0x4C;
	private static final long O_ROLL = 0x50;
	private static final long O_FOV = 0x54;
	private static final long O_NEAR = 0x58;
	private static final long O_FAR = 0x5C;
	private static final long O_FLAGS = 0x60;
	private static final long O_VIEW_W = 0x64;
	private static final long O_VIEW_H = 0x68;
	private static final long O_PLAYER_X = 0x70;
	private static final long O_PLAYER_Y = 0x78;
	private static final long O_PLAYER_Z = 0x80;
	private static final long O_BODY_YAW = 0x88;

	private static final int FIRST_PERSON = 1;

	private static final ValueLayout.OfInt INT = ValueLayout.JAVA_INT_UNALIGNED;
	private static final ValueLayout.OfLong LONG = ValueLayout.JAVA_LONG_UNALIGNED;
	private static final ValueLayout.OfFloat FLOAT = ValueLayout.JAVA_FLOAT_UNALIGNED;
	private static final ValueLayout.OfDouble DOUBLE = ValueLayout.JAVA_DOUBLE_UNALIGNED;
	private static final VarHandle LONG_HANDLE = LONG.varHandle();

	private static final MethodHandle OPEN_FILE_MAPPING;
	private static final MethodHandle MAP_VIEW_OF_FILE;
	private static final MethodHandle GET_TICK_COUNT64;

	private static volatile MemorySegment shm;
	private static long lastOpenAttempt;
	private static volatile Pose latest;
	private static Pose frame;

	public record Pose(
		long hostFrame,
		double x, double y, double z,
		float yaw, float pitch, float roll,
		float fov, float nearClip, float farClip,
		boolean firstPerson,
		int viewportWidth, int viewportHeight,
		double playerX, double playerY, double playerZ,
		float bodyYaw
	) {}

	static {
		Linker linker = Linker.nativeLinker();
		SymbolLookup k32 = SymbolLookup.libraryLookup("kernel32", Arena.global());
		OPEN_FILE_MAPPING = linker.downcallHandle(
			k32.find("OpenFileMappingW").orElseThrow(),
			FunctionDescriptor.of(ValueLayout.ADDRESS, INT, INT, ValueLayout.ADDRESS)
		);
		MAP_VIEW_OF_FILE = linker.downcallHandle(
			k32.find("MapViewOfFile").orElseThrow(),
			FunctionDescriptor.of(ValueLayout.ADDRESS, ValueLayout.ADDRESS, INT, INT, INT, LONG)
		);
		GET_TICK_COUNT64 = linker.downcallHandle(
			k32.find("GetTickCount64").orElseThrow(),
			FunctionDescriptor.of(LONG)
		);
	}

	private SubnauticaCameraLink() {}

	public static void poll() {
		if (shm != null) {
			readLatest();
			return;
		}

		long now = System.currentTimeMillis();
		if (now - lastOpenAttempt < 1000) {
			return;
		}
		lastOpenAttempt = now;

		try (Arena arena = Arena.ofConfined()) {
			MemorySegment name = arena.allocateFrom(NAME, StandardCharsets.UTF_16LE);
			MemorySegment handle = (MemorySegment) OPEN_FILE_MAPPING.invokeExact(
				FILE_MAP_READ, 0, name
			);
			if (handle.address() == 0) {
				return;
			}

			MemorySegment view = (MemorySegment) MAP_VIEW_OF_FILE.invokeExact(
				handle, FILE_MAP_READ, 0, 0, 0L
			);
			if (view.address() == 0) {
				return;
			}

			MemorySegment mapped = view.reinterpret(BYTES);
			if (mapped.get(INT, O_MAGIC) != MAGIC || mapped.get(INT, O_VERSION) != VERSION) {
				return;
			}

			shm = mapped;
			readLatest();
		} catch (Throwable ignored) {
		}
	}

	public static void beginFrame() {
		poll();
		frame = live();
	}

	public static Pose frame() {
		return frame;
	}

	public static Pose live() {
		Pose p = latest;
		if (p == null || shm == null) {
			return null;
		}
		long beat = (long) LONG_HANDLE.getAcquire(shm, O_HEARTBEAT);
		long now = tickCount();
		return beat != 0 && now >= beat && now - beat < TIMEOUT_MS ? p : null;
	}

	public static boolean active() {
		return live() != null;
	}

	private static void readLatest() {
		MemorySegment s = shm;
		if (s == null) {
			return;
		}

		try {
			for (int attempt = 0; attempt < 32; attempt++) {
				long seq1 = (long) LONG_HANDLE.getAcquire(s, O_SEQ);
				if ((seq1 & 1L) != 0L) {
					Thread.onSpinWait();
					continue;
				}

				long hostFrame = s.get(LONG, O_HOST_FRAME);
				double x = s.get(DOUBLE, O_X);
				double y = s.get(DOUBLE, O_Y);
				double z = s.get(DOUBLE, O_Z);
				float yaw = s.get(FLOAT, O_YAW);
				float pitch = s.get(FLOAT, O_PITCH);
				float roll = s.get(FLOAT, O_ROLL);
				float fov = s.get(FLOAT, O_FOV);
				float nearClip = s.get(FLOAT, O_NEAR);
				float farClip = s.get(FLOAT, O_FAR);
				int flags = s.get(INT, O_FLAGS);
				int vw = s.get(INT, O_VIEW_W);
				int vh = s.get(INT, O_VIEW_H);
				double px = s.get(DOUBLE, O_PLAYER_X);
				double py = s.get(DOUBLE, O_PLAYER_Y);
				double pz = s.get(DOUBLE, O_PLAYER_Z);
				float bodyYaw = s.get(FLOAT, O_BODY_YAW);

				VarHandle.loadLoadFence();
				long seq2 = (long) LONG_HANDLE.getAcquire(s, O_SEQ);
				if (seq1 == seq2 && (seq2 & 1L) == 0L) {
					latest = new Pose(
						hostFrame, x, y, z, yaw, pitch, roll, fov, nearClip, farClip,
						(flags & FIRST_PERSON) != 0, vw, vh, px, py, pz, bodyYaw
					);
					return;
				}
			}
		} catch (RuntimeException ignored) {
		}
	}

	private static long tickCount() {
		try {
			return (long) GET_TICK_COUNT64.invokeExact();
		} catch (Throwable t) {
			return 0L;
		}
	}
}
