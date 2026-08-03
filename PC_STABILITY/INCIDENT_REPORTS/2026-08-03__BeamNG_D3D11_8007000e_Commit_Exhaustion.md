# BeamNG D3D11 Error 0x8007000e — Commit Exhaustion Incident

**Incident date/time:** 2026-08-03 08:48 PDT (log session start)  
**Workstream:** PC Stability / BeamNG / RedFox System Sentinel coordination  
**BeamNG version:** 0.38.6.0, build 19963  
**Release/build state:** No Sentinel version change; Sentinel remains disabled pending audit acceptance.

## Files inspected

Private originals remain with David and were not attached publicly.

| File | Bytes | SHA-256 |
|---|---:|---|
| `image.png` | 73,482 | `b621c132bed29566ffe9e5a511b6a0d64491c05bce92aeb65f060e165fa981d1` |
| `current.zip` | 653,738 | `63933c3e5ec232578844a251a1cf859f388c64ac44f58cfb5654b98ac43e547f` |

`current.zip` contains ten files: four BeamNG logs, four launcher logs, `beamng-dxDiag.txt`, and `consoleHistory.json`.

## Direct crash evidence

The current BeamNG log started at `2026-08-03 08:48:44` and crashed while loading West Coast USA approximately 34.6 seconds after startup.

Relevant log sequence:

- D3D11 error `#8007000e`
- `Not enough memory resources are available to complete this operation`
- `GFXD3D11TextureManager::_createTexture - Error creating 2D texture`
- Fatal error number `-2147024882`

BeamNG's memory status at failure:

- Virtual address space: `130999 GB available / 131072 GB total`
- Physical memory: `7.7 GB available / 31.8 GB total`, 75% load
- PageFile/commit resource: `6.7 MB available / 70 GB total`

## Interpretation

This is a system commit-limit exhaustion event, not proof of an RTX 3060 hardware failure.

The important value is not the enormous 131 TB virtual address-space figure. The critical value is only **6.7 MB of pagefile/commit resource remaining out of 70 GB**. Windows could not approve another committed allocation, so D3D11 failed when BeamNG attempted to create a 2D texture.

Physical RAM was only 75% occupied because committed/private memory does not have to be resident in RAM at that moment. A process can exhaust the system commit limit while several gigabytes of physical RAM remain available.

The BeamNG log alone does not identify which process or processes consumed the missing commit. Possible contributors include the current BeamNG mod load, stale BeamNG/helper processes, browser processes, monitoring tools, or another high-commit process. Task Manager or a Windows process snapshot is required to assign responsibility.

## Current mod-load evidence

The current log mounted **222 mod packages** and reorganized **88,999 virtual files** before the crash.

The current session produced 134 errors before failing. Repeated current-session errors include:

- failed manual unload-mode registration for extensions;
- missing RedFox and other input-action IDs;
- missing/unavailable extensions;
- null action parsing failures.

The previous three BeamNG logs in the archive each reached BeamNG's 15,000-entry logging ceiling:

| Log | Session start | Time when logging ceiling was reached | Recorded error entries |
|---|---|---:|---:|
| `beamng.1.log` | 2026-08-03 00:48:59 | 163.8 s | 12,358 |
| `beamng.2.log` | 2026-08-03 00:16:01 | 396.9 s | 11,375 |
| `beamng.3.log` | 2026-08-02 23:41:05 | 180.2 s | 12,469 |

Dominant earlier-session defects include:

- more than twelve thousand repeated Collada resolution errors in one session;
- duplicate meshes with different contents;
- duplicate JBeam parts;
- malformed/undecodable JSON/JBeam files;
- repeated missing actions and extension-registration errors.

This does not prove that one specific mod consumed the entire commit limit, but it establishes that the current 222-package collection is not a clean or controlled test environment.

## Confidence

- **High:** the immediate crash was caused by commit/pagefile resource exhaustion.
- **High:** D3D11 texture creation was the allocation that failed, not necessarily the root consumer.
- **High:** the current mod collection contains extensive conflicts and malformed content and is unsuitable for baseline testing.
- **Medium:** the heavy mod load is the principal trigger for the commit spike.
- **Low:** any claim naming one exact mod or the GPU as the root cause without a process-commit snapshot.

## Known risks

- Reopening the same 222-mod configuration can immediately repeat the failure.
- Allowing commit to reach the limit can crash Chrome, DWM, PowerShell, WMI, or other unrelated Windows processes.
- Increasing the pagefile alone may delay the failure but will not repair a leak, conflict, stale process, or hardware-memory instability.
- Corrected WHEA platform-memory events remain a separate hardware investigation and are not explained by this user-mode allocation failure.

## Required next action

1. Do not relaunch the current mod configuration.
2. Reboot Windows to clear stale committed allocations.
3. Keep Sentinel, browser tabs, overlays, and monitoring utilities closed.
4. Before launching BeamNG, capture Task Manager → Performance → Memory, including `Committed` used/limit.
5. If baseline commit is already abnormally high after reboot, identify the largest commit consumers before touching BeamNG.
6. If baseline commit is normal, use a clean BeamNG user folder with all mods disabled, then test the exact RLS core only in a new career.
7. Reintroduce mods in small controlled groups; do not mount 222 packages at once.
8. Stop any test at 80–85% of the commit limit or when commit rises continuously.

## What David must preserve

- Original `image.png` and `current.zip`.
- Exact screenshot/capture time.
- Any BeamNG crash-report ZIP or DMP created for this incident.
- A post-reboot Task Manager Memory screenshot before applications are opened.
- A process list sorted by Memory/Commit if baseline commit remains high.
