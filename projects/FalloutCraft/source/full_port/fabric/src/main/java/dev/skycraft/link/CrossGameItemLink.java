package dev.skycraft.link;

import static java.lang.foreign.ValueLayout.*;

import java.lang.foreign.Arena;
import java.lang.foreign.FunctionDescriptor;
import java.lang.foreign.Linker;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.SymbolLookup;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.VarHandle;
import java.nio.charset.StandardCharsets;

/**
 * Stateful item transport for SkyCraft's Minecraft <-> Subnautica bridge.
 *
 * This lives in a second mapping so the proven SkyCraft/FalloutCraft protocol v11 stays binary-compatible.
 * Low-frequency item handoffs do not belong in the render/collision rings.
 */
public final class CrossGameItemLink {
	public static final int MAGIC = 0x4D495853; // "SXIM"
	public static final int VERSION = 1;
	public static final String MAPPING_NAME = System.getProperty(
		"skycraft.items.link",
		"Local\\SkyCraft_Subnautica_Items_v1"
	);

	public static final int ORIGIN_UNKNOWN = 0;
	public static final int ORIGIN_MINECRAFT = 1;
	public static final int ORIGIN_SUBNAUTICA = 2;

	public static final int OP_TRANSFER = 1;
	public static final int OP_UPDATE = 2;
	public static final int OP_CONSUME = 3;
	public static final int OP_REMOVE = 4;
	public static final int OP_USE = 5;

	public static final int FLAG_HAS_ENERGY = 1;
	public static final int FLAG_HAS_DURABILITY = 1 << 1;
	public static final int FLAG_CONSUMABLE = 1 << 2;
	public static final int FLAG_TOOL = 1 << 3;
	public static final int FLAG_WEAPON = 1 << 4;
	public static final int FLAG_EQUIPMENT = 1 << 5;
	public static final int FLAG_CREATURE = 1 << 6;
	public static final int FLAG_VEHICLE = 1 << 7;

	private static final int FILE_MAP_ALL_ACCESS = 0xF001F;
	private static final long OFF_HEADER = 0x0000;
	private static final long OFF_HOST_TO_MC = 0x1000;
	private static final int RING_ENTRIES = 64;
	private static final int RECORD_BYTES = 1024;
	private static final long OFF_MC_TO_HOST = OFF_HOST_TO_MC + 0x100L + (long) RING_ENTRIES * RECORD_BYTES;
	private static final long MAPPING_BYTES = OFF_MC_TO_HOST + 0x100L + (long) RING_ENTRIES * RECORD_BYTES;

	private static final long H_MAGIC = 0x00;
	private static final long H_VERSION = 0x04;
	private static final long H_MC_PID = 0x0C;
	private static final long H_HOST_HEARTBEAT = 0x10;
	private static final long H_MC_HEARTBEAT = 0x18;

	private static final long R_HEAD = 0x00;
	private static final long R_TAIL = 0x40;
	private static final long R_DATA = 0x100;

	private static final long I_TRANSFER_ID = 0x00;
	private static final long I_OPERATION = 0x08;
	private static final long I_ORIGIN = 0x0C;
	private static final long I_FLAGS = 0x10;
	private static final long I_COUNT = 0x14;
	private static final long I_MAX_STACK = 0x18;
	private static final long I_ENERGY = 0x1C;
	private static final long I_MAX_ENERGY = 0x20;
	private static final long I_DURABILITY = 0x24;
	private static final long I_MAX_DURABILITY = 0x28;
	private static final long I_ID_LENGTH = 0x2C;
	private static final long I_NAME_LENGTH = 0x30;
	private static final long I_STATE_LENGTH = 0x34;
	private static final long I_ID = 0x40;
	private static final int ID_BYTES = 128;
	private static final long I_NAME = I_ID + ID_BYTES;
	private static final int NAME_BYTES = 128;
	private static final long I_STATE = I_NAME + NAME_BYTES;
	private static final int STATE_BYTES = RECORD_BYTES - (int) I_STATE;

	private static final long HEARTBEAT_TIMEOUT_MS = 8000;
	private static final VarHandle LONG = JAVA_LONG.varHandle();
	private static final MethodHandle OPEN_FILE_MAPPING;
	private static final java.lang.foreign.StructLayout CALL_STATE = Linker.Option.captureStateLayout();
	private static final MemorySegment OPEN_STATE = Arena.global().allocate(CALL_STATE);
	private static final MethodHandle MAP_VIEW_OF_FILE;
	private static final MethodHandle GET_TICK_COUNT64;
	private static final MethodHandle GET_CURRENT_PROCESS_ID;

	private static volatile MemorySegment shm;
	private static long lastOpenAttempt;

	static {
		Linker linker = Linker.nativeLinker();
		SymbolLookup k32 = SymbolLookup.libraryLookup("kernel32", Arena.global());
		OPEN_FILE_MAPPING = linker.downcallHandle(
			k32.find("OpenFileMappingW").orElseThrow(),
			FunctionDescriptor.of(ADDRESS, JAVA_INT, JAVA_INT, ADDRESS),
			Linker.Option.captureCallState("GetLastError")
		);
		MAP_VIEW_OF_FILE = linker.downcallHandle(
			k32.find("MapViewOfFile").orElseThrow(),
			FunctionDescriptor.of(ADDRESS, ADDRESS, JAVA_INT, JAVA_INT, JAVA_INT, JAVA_LONG)
		);
		GET_TICK_COUNT64 = linker.downcallHandle(
			k32.find("GetTickCount64").orElseThrow(),
			FunctionDescriptor.of(JAVA_LONG)
		);
		GET_CURRENT_PROCESS_ID = linker.downcallHandle(
			k32.find("GetCurrentProcessId").orElseThrow(),
			FunctionDescriptor.of(JAVA_INT)
		);
	}

	private CrossGameItemLink() {
	}

	public static final class Item {
		public long transferId;
		public int operation = OP_TRANSFER;
		public int origin = ORIGIN_UNKNOWN;
		public int flags;
		public int count = 1;
		public int maxStack = 1;
		public float energy;
		public float maxEnergy;
		public float durability;
		public float maxDurability;
		public String itemId = "";
		public String displayName = "";
		public String stateJson = "";
	}

	public static void poll() {
		MemorySegment s = shm;
		if (s != null) {
			s.set(JAVA_LONG, OFF_HEADER + H_MC_HEARTBEAT, tickCount());
			return;
		}

		long now = System.currentTimeMillis();
		if (now - lastOpenAttempt < 1000) {
			return;
		}
		lastOpenAttempt = now;

		try (Arena arena = Arena.ofConfined()) {
			MemorySegment name = arena.allocateFrom(MAPPING_NAME, StandardCharsets.UTF_16LE);
			MemorySegment handle = (MemorySegment) OPEN_FILE_MAPPING.invokeExact(
				OPEN_STATE, FILE_MAP_ALL_ACCESS, 0, name
			);
			if (handle.address() == 0) {
				return;
			}

			MemorySegment view = (MemorySegment) MAP_VIEW_OF_FILE.invokeExact(
				handle, FILE_MAP_ALL_ACCESS, 0, 0, 0L
			);
			if (view.address() == 0) {
				return;
			}

			MemorySegment mapped = view.reinterpret(MAPPING_BYTES);
			if (mapped.get(JAVA_INT, OFF_HEADER + H_MAGIC) != MAGIC
				|| mapped.get(JAVA_INT, OFF_HEADER + H_VERSION) != VERSION) {
				return;
			}

			mapped.set(JAVA_INT, OFF_HEADER + H_MC_PID, (int) GET_CURRENT_PROCESS_ID.invokeExact());
			mapped.set(JAVA_LONG, OFF_HEADER + H_MC_HEARTBEAT, tickCount());
			shm = mapped;
		} catch (Throwable ignored) {
			// Main SkyLink logs the primary bridge status. Item transport may come up later.
		}
	}

	public static boolean active() {
		MemorySegment s = shm;
		if (s == null) {
			return false;
		}
		long beat = (long) LONG.getAcquire(s, OFF_HEADER + H_HOST_HEARTBEAT);
		return beat != 0 && tickCount() - beat < HEARTBEAT_TIMEOUT_MS;
	}

	public static Item tryReceiveFromHost() {
		MemorySegment s = shm;
		if (s == null) {
			return null;
		}

		long head = (long) LONG.getAcquire(s, OFF_HOST_TO_MC + R_HEAD);
		long tail = s.get(JAVA_LONG, OFF_HOST_TO_MC + R_TAIL);
		if (tail >= head) {
			return null;
		}

		long record = OFF_HOST_TO_MC + R_DATA
			+ (tail & (RING_ENTRIES - 1L)) * RECORD_BYTES;

		Item item = readRecord(s, record);
		VarHandle.loadLoadFence();
		LONG.setRelease(s, OFF_HOST_TO_MC + R_TAIL, tail + 1);
		return item;
	}

	public static synchronized boolean trySendToHost(Item item) {
		MemorySegment s = shm;
		if (s == null || item == null || item.itemId == null || item.itemId.isBlank()) {
			return false;
		}

		long head = s.get(JAVA_LONG, OFF_MC_TO_HOST + R_HEAD);
		long tail = (long) LONG.getAcquire(s, OFF_MC_TO_HOST + R_TAIL);
		if (head - tail >= RING_ENTRIES) {
			return false;
		}

		long record = OFF_MC_TO_HOST + R_DATA
			+ (head & (RING_ENTRIES - 1L)) * RECORD_BYTES;

		writeRecord(s, record, item);
		VarHandle.storeStoreFence();
		LONG.setRelease(s, OFF_MC_TO_HOST + R_HEAD, head + 1);
		return true;
	}

	private static Item readRecord(MemorySegment s, long b) {
		Item item = new Item();
		item.transferId = s.get(JAVA_LONG, b + I_TRANSFER_ID);
		item.operation = s.get(JAVA_INT, b + I_OPERATION);
		item.origin = s.get(JAVA_INT, b + I_ORIGIN);
		item.flags = s.get(JAVA_INT, b + I_FLAGS);
		item.count = s.get(JAVA_INT, b + I_COUNT);
		item.maxStack = s.get(JAVA_INT, b + I_MAX_STACK);
		item.energy = s.get(JAVA_FLOAT, b + I_ENERGY);
		item.maxEnergy = s.get(JAVA_FLOAT, b + I_MAX_ENERGY);
		item.durability = s.get(JAVA_FLOAT, b + I_DURABILITY);
		item.maxDurability = s.get(JAVA_FLOAT, b + I_MAX_DURABILITY);
		item.itemId = readUtf8(s, b + I_ID, ID_BYTES, s.get(JAVA_INT, b + I_ID_LENGTH));
		item.displayName = readUtf8(s, b + I_NAME, NAME_BYTES, s.get(JAVA_INT, b + I_NAME_LENGTH));
		item.stateJson = readUtf8(s, b + I_STATE, STATE_BYTES, s.get(JAVA_INT, b + I_STATE_LENGTH));
		return item;
	}

	private static void writeRecord(MemorySegment s, long b, Item item) {
		s.set(JAVA_LONG, b + I_TRANSFER_ID, item.transferId);
		s.set(JAVA_INT, b + I_OPERATION, item.operation);
		s.set(JAVA_INT, b + I_ORIGIN, item.origin);
		s.set(JAVA_INT, b + I_FLAGS, item.flags);
		s.set(JAVA_INT, b + I_COUNT, item.count);
		s.set(JAVA_INT, b + I_MAX_STACK, item.maxStack);
		s.set(JAVA_FLOAT, b + I_ENERGY, item.energy);
		s.set(JAVA_FLOAT, b + I_MAX_ENERGY, item.maxEnergy);
		s.set(JAVA_FLOAT, b + I_DURABILITY, item.durability);
		s.set(JAVA_FLOAT, b + I_MAX_DURABILITY, item.maxDurability);
		writeUtf8(s, b + I_ID, ID_BYTES, b + I_ID_LENGTH, item.itemId);
		writeUtf8(s, b + I_NAME, NAME_BYTES, b + I_NAME_LENGTH, item.displayName);
		writeUtf8(s, b + I_STATE, STATE_BYTES, b + I_STATE_LENGTH, item.stateJson);
	}

	private static String readUtf8(MemorySegment s, long off, int capacity, int length) {
		if (length < 0 || length > capacity) {
			return "";
		}
		byte[] bytes = new byte[length];
		for (int i = 0; i < length; i++) {
			bytes[i] = s.get(JAVA_BYTE, off + i);
		}
		return new String(bytes, StandardCharsets.UTF_8);
	}

	private static void writeUtf8(MemorySegment s, long off, int capacity, long lengthOff, String value) {
		byte[] bytes = (value == null ? "" : value).getBytes(StandardCharsets.UTF_8);
		if (bytes.length > capacity) {
			throw new IllegalArgumentException("Cross-game item field exceeds protocol capacity");
		}
		for (int i = 0; i < capacity; i++) {
			s.set(JAVA_BYTE, off + i, (byte) 0);
		}
		for (int i = 0; i < bytes.length; i++) {
			s.set(JAVA_BYTE, off + i, bytes[i]);
		}
		s.set(JAVA_INT, lengthOff, bytes.length);
	}

	private static long tickCount() {
		try {
			return (long) GET_TICK_COUNT64.invokeExact();
		} catch (Throwable t) {
			throw new RuntimeException(t);
		}
	}
}
