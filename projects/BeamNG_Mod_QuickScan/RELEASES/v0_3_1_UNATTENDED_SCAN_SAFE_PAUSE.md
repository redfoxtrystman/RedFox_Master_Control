# BeamNG Mod QuickScan v0.3.1 — Unattended Scan + Safe Pause

**Date built:** 2026-07-26 PDT  
**Owner:** David / Captain  
**Built by:** Sol / BeamNG Mod QuickScan chat  
**Baseline:** v0.3.0 Python/Tkinter source  
**Status:** Static/self-test verified; Windows large-library runtime not yet proven

## Baseline proof

- v0.3.0 source SHA-256: `f22e2bd4e4a0dbcffa92e21c288ef892bbf14f498bdf2934172a03ca9cdc9ae9`
- v0.3.0 source lines: 1,054
- Baseline Python compile: PASS
- Baseline built-in self-test: PASS

## v0.3.1 proof

- v0.3.1 source SHA-256: `04286362af5d9c95e5dd2120fb637be54592d252cf0a9b7f5f68faf59791a4b3`
- v0.3.1 source lines: 1,713
- Final ZIP: `BeamNG_Mod_QuickScan_Python_v0_3_1_Unattended_Pause.zip`
- Final ZIP SHA-256: `fd9b6bddcc9b34d2bd94b3f444c5c5a807ed53d5cf0d11fd6cc959eeb198d4cc`
- Final ZIP bytes: 76,946
- Final ZIP reopen/test: PASS
- Packaged Python compile: PASS
- Packaged self-test: PASS
- Required packaged files missing: 0

## What this patch changes

1. Removes the v0.3.0 preparation pass that opened every ZIP before the real scan.
2. Replaces manual `SCAN NEXT BATCH` behavior with one unattended scan queue.
3. Adds adjustable checkpoint sizes: 1, 2, 5, 10, 25, 50, 100, All, or a typed number.
4. Keeps only one ZIP active at a time.
5. Adds separate **Pause Scan** and **Cancel Scan** controls.
6. Saves every completed ZIP immediately to SQLite.
7. Saves scan jobs and queue items in new `scan_jobs` and `scan_queue` tables.
8. Resumes a paused or interrupted scan in a new application session.
9. Reconciles changed, new, missing, and interrupted ZIPs before resuming.
10. Adds Very Low Load, Low Load, and Balanced profiles.
11. Uses disk-backed SQLite temporary comparison work instead of forcing temporary work into RAM.
12. Uses a 2 MB retained source sample in Very Low Load, 4 MB in Low Load, and 8 MB in Balanced. Full file hashes are still completed.
13. Writes checkpoint reports automatically and continues scanning.
14. Updates `MASTER_CURRENT` at checkpoints without rebuilding the entire cumulative report every time.
15. Refreshes the full cumulative findings report when the scan pauses, is cancelled, or finishes.
16. Adds safe close behavior: closing during a scan requests Pause and closes after the checkpoint is written.
17. Preserves v0.3.0 duplicate/version/conflict analysis and false-positive corrections.

## Test evidence

### Built-in self-test

- PASS — unattended continuation through all test ZIPs
- PASS — checkpoint sizes 1 and 2
- PASS — cache reuse
- PASS — exact duplicate detection
- PASS — repacked duplicate detection
- PASS — numeric version comparison: 1.10 newer than 1.9
- PASS — generic `mod_info.json` false positive remains removed
- PASS — local Lua `seen` / `names` false positive remains removed
- PASS — broken ZIP does not stop the queue
- PASS — pause after a committed ZIP
- PASS — resume in a new Engine instance
- PASS — changed completed ZIP is requeued
- PASS — new ZIP added while paused is added to the queue
- PASS — Cancel remains separate from Pause
- PASS — rotating database backup exists
- PASS — master report exists

### Extended test

- PASS — pause during a large internal Lua file
- PASS — half-scanned ZIP returned to pending
- PASS — no partial ZIP result trusted
- PASS — resume rescanned interrupted ZIP from the beginning
- PASS — final latest report status is `complete`
- PASS — full cumulative report written at a safe stop

### GUI smoke test

- PASS — Tkinter application window constructed under an Xvfb virtual display
- PASS — Start/Resume button exists
- PASS — Pause button exists

## Not proven

The following still require David's real Windows test:

- Windows DPI and resizing behavior
- Real mouse/button behavior
- 50–60 real-mod scan stability
- thousands-of-mods scan stability
- actual CPU and RAM load on David's computer
- pause timing on real slow drives
- database/report behavior with David's existing large library

## Not in this patch

- Auto-Pilot CPU/RAM monitoring and automatic throttling — planned v0.3.2
- preview-image extraction
- version-aware ZIP renaming
- duplicate naming
- catalog sorting/moving
- dependency graph
- guided compatibility repair

## Package contents

- `BeamNG Mod QuickScan.pyw`
- `START BeamNG Mod QuickScan.bat`
- `RUN SELF TEST.bat`
- `README.txt`
- `BASELINE_v0_3_0.json`
- `PATCH_CHANGE_REPORT.md`
- `SIDE_BY_SIDE_COLORED_DIFF.html`
- `TEST_REPORT.txt`
- `VERIFICATION.json`

## Next safe step

David should test v0.3.1 on a small copied folder first:

```text
Checkpoint every: 2
Computer load: Very Low Load
```

The first Windows test should confirm:

1. the window opens at a usable size;
2. the scan begins without the old full preparation pass;
3. checkpoint 1 is written after two mods;
4. the scan continues without another button press;
5. Pause saves and changes the button to Resume;
6. closing and reopening resumes the saved queue;
7. CPU/RAM behavior is acceptable.

Do not call v0.3.1 Windows-runtime proven until David reports those results.