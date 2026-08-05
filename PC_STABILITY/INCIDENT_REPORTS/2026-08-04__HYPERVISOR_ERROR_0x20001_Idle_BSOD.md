# 2026-08-04 — HYPERVISOR_ERROR (0x20001) Idle/Light-Load BSOD

**Workstream:** PC Stability / RedFox System Sentinel  
**Local observation time:** approximately 2026-08-04 18:28 PDT  
**Current Sentinel state:** believed disabled/closed  
**Current build context:** Windows 11 build previously reported as 10.0.26200.8875  

## User report

David reports the computer was at idle or near-idle when the blue screen occurred. He does not believe Chrome was open. He is uncertain whether BeamNG.drive was still loaded; the likely visible workload was BeamNG.drive and the ChatGPT desktop app, but this has not yet been confirmed from process/event evidence.

This uncertainty must remain explicit. Do not label the incident BeamNG-caused without the dump and process timeline.

## Visible stop code

Phone photo clearly shows:

```text
Stop code: HYPERVISOR_ERROR (0x20001)
```

Microsoft documents bug check `0x00020001` as a fatal error encountered by the Windows hypervisor. The reserved parameters shown on the blue-screen page do not identify the cause; WinDbg `!analyze -v` is required.

## Evidence metadata

Raw phone image was not committed publicly.

- Local filename: `13481.jpg`
- Size: 143,751 bytes
- Dimensions: 1536 × 710
- SHA-256: `8b20ce66886220b85d6e349aee604f713f76766217d6a9a51a0074e88275ca10`
- Visible status: 100% complete

## Why this is a separate incident class

This is not the same failure as the preceding BeamNG D3D11 `0x8007000e` allocation failure.

- The D3D11 error was a user-mode texture allocation failure with only 6.7 MB commit headroom remaining.
- This event is a kernel/hypervisor bugcheck.
- It may still be triggered by load, a transition from load to idle, VBS/Memory Integrity, CPU power-state handling, firmware, a low-level driver, or hardware instability.
- The prior corrected WHEA platform-memory events and mixed DIMM configuration remain relevant background risks.

## Current hypotheses — confidence ranked

1. **Windows hypervisor/VBS plus Intel CPU idle/power-state interaction — medium confidence pending dump.**  
   The crash reportedly happened at idle/light load, and public reports exist for build 26200-family systems where `HYPERVISOR_ERROR` dumps point to `intelppm!HvRequestIdle`. This is only an analogy; this machine's dump must confirm or reject it.

2. **Firmware/BIOS or CPU/memory-subsystem instability exposed in hypervisor context — medium confidence.**  
   BIOS 1602 is old, and the machine has repeated corrected WHEA platform-memory events plus mixed Corsair/PNY DIMMs.

3. **Low-level driver or VBS/HVCI incompatibility — medium-low confidence.**  
   Memory Integrity/VBS uses the Windows hypervisor, and incompatible kernel drivers can cause system malfunction or blue screens. Exact driver attribution requires the dump.

4. **BeamNG as direct root cause — low confidence.**  
   BeamNG may have been open and could be a trigger, but a user-mode game does not by itself explain a fatal hypervisor error. The near-idle timing weakens a BeamNG-only explanation.

## Immediate preservation steps

1. Do not relaunch BeamNG or Sentinel.
2. Preserve the newest file from `C:\Windows\Minidump` without renaming the original.
3. Also check for `C:\Windows\MEMORY.DMP` if no minidump exists.
4. Record the exact reboot time from Reliability Monitor/Event Viewer.
5. Do not change Hyper-V, VBS, Memory Integrity, BIOS virtualization, power-plan, or pagefile settings before the dump is copied.
6. Do not run cleanup tools.

## Required analysis

Open the newest dump in WinDbg and capture:

```text
.symfix
.reload
!analyze -v
kv
!sysinfo cpuinfo
!sysinfo smbios
```

Preserve:

- Bugcheck parameters
- `MODULE_NAME`
- `IMAGE_NAME`
- `SYMBOL_NAME`
- `FAILURE_BUCKET_ID`
- `STACK_TEXT`
- Hypervisor flags
- Any `intelppm!HvRequestIdle`, `nt!Hvl*`, `securekernel`, VBS/HVCI, or hardware-error references

## Decision points after dump analysis

- If the stack points to `intelppm!HvRequestIdle` or an idle transition: compare BIOS, Windows build, VBS state, chipset/ME drivers, and power-management configuration before hardware stress testing.
- If the dump points to a third-party driver: isolate/update/remove that driver while preserving VBS state for controlled comparison.
- If the dump is corrupt or inconsistent and WHEA memory events continue: prioritize matched-pair RAM isolation and BIOS/board/CPU investigation.
- If the crash repeats with BeamNG and Sentinel closed: BeamNG/Sentinel cannot be the primary cause.

## Current next action

David should upload the newest minidump from `C:\Windows\Minidump`. No configuration changes should be made before that evidence is preserved.
