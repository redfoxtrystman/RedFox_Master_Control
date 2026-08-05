# Minidump Archive Header Audit — 2026-08-04

**Workstream:** PC Stability / RedFox System Sentinel  
**Review time:** 2026-08-04 19:14 PDT  
**Source:** User-uploaded `Minidumps.zip`  
**Raw archive not committed:** contains Windows crash dumps/private machine data.

## Archive metadata

- Filename: `Minidumps.zip`
- Size: 4,852,780 bytes
- SHA-256: `96212be44900617379274356b806f377716a6b3c4524ed03a4b4f5cdd4595e76`
- Contents: 5 Windows kernel minidumps

## Header-confirmed bugchecks

The Windows dump headers were read directly. This does not replace symbol-based WinDbg analysis, but the bugcheck codes and four parameters are part of the dump header and are reliable.

| Dump | Size | SHA-256 | Bugcheck | Parameters |
|---|---:|---|---|---|
| `073126-17156-01.dmp` | 3,987,149 | `1f13ed5931a17b37e4b2f98d55030adf773e7aa3699cfa100479be07598b4752` | `0x3B SYSTEM_SERVICE_EXCEPTION` | `0xC0000005`, `0xFFFFF802A62D8B6A`, `0xFFFFDB8082DAC8F0`, `0x0` |
| `073126-17500-01.dmp` | 4,302,171 | `9cac12e616ecfc2fff1b681cd175ebe96f852c3a5b198a9e2222e3d50ebfb7c5` | `0x3B SYSTEM_SERVICE_EXCEPTION` | `0xC0000005`, `0xFFFFF806D34D0D1A`, `0xFFFF8503B9581CE0`, `0x0` |
| `080426-16484-01.dmp` | 5,543,993 | `1472bc35bef97203ac0a9cd8e14d4f2f808468fa761feee3101f26b931955215` | `0x3B SYSTEM_SERVICE_EXCEPTION` | `0xC0000005`, `0xFFFFF8067DEA7E40`, `0xFFFFBA00B3BAC8F0`, `0x0` |
| `080426-17765-01.dmp` | 4,016,907 | `a9dee98fce7258df867e897035e7e75d764e505bb68c9969f32b42e88ee0aeea` | `0xA IRQL_NOT_LESS_OR_EQUAL` | `0xFFFFF80081275080`, `0x2`, `0x0`, `0xFFFFF8007E5EBBC4` |
| `080426-17515-01.dmp` | 3,906,531 | `a4b5baa1561a57cccf3c1a580df82ab3d03aa959bbfeddc9c9684ec103da76c7` | `0x20001 HYPERVISOR_ERROR` | `0x11`, `0x35CC9E`, `0x1005`, `0xFFFFE70000A05CF0` |

## Key finding

August 4 contains three different kernel crash classes in one day:

- `06:35` — `0x3B` access violation
- `15:10` — `0xA` invalid/high-IRQL memory access
- `18:27` — `0x20001` fatal hypervisor error

The July 31 dumps add two more `0x3B` access-violation crashes.

This varied pattern is more consistent with systemic instability than one stable user-mode application fault. It strengthens the existing need to isolate RAM/memory-controller/motherboard/firmware stability and low-level Windows/driver/hypervisor interactions. It does not by itself identify one failed component.

## Important limits

- No Microsoft symbol server or WinDbg/CDB was available in the review environment.
- No `!analyze -v`, stack trace, module attribution, trap/context decoding, or hypervisor enlightenment decoding was performed.
- The string `intelppm` is present in these kernel dumps, but presence alone is not proof that `intelppm.sys` caused any crash.
- Microsoft documents all four `0x20001` parameters as reserved, so they must not be assigned unsupported meanings.

## Interpretation

1. `0x3B` with `0xC0000005` repeated three times in this archive indicates repeated kernel-mode access violations, but the changing instruction addresses mean no single module can be named from the header alone.
2. `0xA` indicates invalid or pageable memory was referenced at IRQL 2; full stack analysis is required to identify the executing component.
3. `0x20001` confirms the newest blue screen was a fatal Windows hypervisor failure.
4. The new hypervisor crash may involve VBS/Memory Integrity, virtualization, CPU idle/power-state transitions, firmware, or a low-level driver, but this remains a hypothesis until WinDbg stack analysis.
5. Because three crash classes occurred on August 4, continuing BeamNG stress testing before matched-pair RAM isolation and dump analysis risks generating more corruption/noisy evidence.

## Required next actions

1. Preserve `Minidumps.zip` unchanged locally.
2. Run WinDbg on all five dumps with Microsoft symbols.
3. For each dump preserve:
   - `!analyze -v`
   - `MODULE_NAME`
   - `IMAGE_NAME`
   - `FAILURE_BUCKET_ID`
   - `STACK_TEXT`
   - trap/context records
   - hypervisor flags/enlightenment output for `0x20001`
4. Keep Sentinel disabled.
5. Stop extended BeamNG stress testing until one matched two-DIMM kit is tested at JEDEC defaults.
6. Record whether Hyper-V, Virtual Machine Platform, Windows Hypervisor Platform, WSL, Memory Integrity, and Credential Guard are enabled, but do not change several at once before the dump analysis baseline is preserved.

## Confidence

- High: archive metadata, dump list, bugcheck codes, and header parameters.
- High: multiple distinct kernel crash classes occurred.
- Moderate: systemic memory/firmware/low-level instability is more likely than one ordinary application bug.
- Low: exact failing driver or hardware component until symbol-based debugging and hardware isolation are complete.
