# PC Stability / RedFox System Sentinel — Master Roadmap

**Roadmap date/time:** 2026-07-27 16:34 PDT  
**Owner:** David / Captain  
**Coordination:** GitHub issue #6  
**Status:** Sentinel development frozen pending audit acceptance and controlled recovery build.

## Purpose

This roadmap consolidates what has been done, what was tried, what succeeded or failed, what evidence exists, and the required order for the next Sentinel version, hardware isolation, and BeamNG/RLS testing.

The investigation has three separate but interacting tracks:

1. Hardware/memory stability.
2. Sentinel/PowerShell/WMI stability.
3. BeamNG/RLS/mod stability and commit pressure.

No single track may be used to erase evidence from the other two.

# 1. Work completed and evidence collected

## 1.1 PC hardware and configuration established

- ASUS PRIME Z490-P motherboard.
- Intel Core i5-10600K, 6 cores / 12 logical processors.
- NVIDIA RTX 3060 12 GB.
- 32 GB DDR4 using four mixed 8 GB DIMMs:
  - two Corsair `CMK16GX4M2B3200C16`
  - two PNY `8GBF1X08QFHH38-135-K`
- BIOS 1602 dated 2021-01-14.
- XMP disabled.
- Memory running at approximately 2133 MT/s / 1.2 V during captured evidence.
- MultiCore Enhancement disabled / Intel limits enforced.
- Samsung 970 EVO Plus NVMe system drive and Inland NVMe secondary drive.
- Two older mechanical drives have bad-block evidence and must not host critical pagefiles or irreplaceable data.

## 1.2 Windows and crash evidence reviewed

Observed bugcheck families include:

- `0xA IRQL_NOT_LESS_OR_EQUAL`
- `0x1E KMODE_EXCEPTION_NOT_HANDLED`
- `0x135 REGISTRY_FILTER_DRIVER_EXCEPTION`
- `0x3B SYSTEM_SERVICE_EXCEPTION`

The newest known kernel crash is `0x3B` with `0xC0000005` access violation.

Repeated corrected WHEA events were collected. Consolidated analysis identified CPER Platform Memory Error sections. This makes an application-only explanation insufficient and places RAM/DIMM compatibility, DIMM/slot failure, the CPU memory controller, motherboard/socket/BIOS, and power stability on the hardware track.

SFC/DISM work was performed and SFC was reported clean, but the exact result still needs to be backfilled into GitHub with preserved command output if available.

## 1.3 Sentinel evidence collected

The read-only Sentinel data review found approximately:

- 84,854 files.
- 11.75 GB total data.
- 4,152 incident folders.
- 307 report ZIPs in the earlier scan; later archives included additional snapshots.
- 3,607 telemetry rows at 95% commit or higher.
- Maximum observed commit near 99%.
- Maximum paging spike around 185,065 pages/sec.
- 19 checkpoint failures in one reviewed period.
- Multiple unexpected stops.
- Failed process attribution: parsed process rows often showed only `System Idle Process` and null CPU.
- Marker/worker version mismatch: v1.4.1 startup marker with active worker reporting v1.3.2.
- Recorder delays measured in minutes during severe pressure.
- Repeated incident/report generation amplified disk and commit pressure.

## 1.4 Live PowerShell/WMI incident captured

During a live incident:

- CPU reached approximately 95–98%.
- WMI Provider Host used about 77.5% CPU.
- Task Manager showed approximately 15 PowerShell processes.
- Ending the PowerShell group reduced CPU to about 19%.
- The PowerShell processes did not immediately return.

`WmiPrvSE.DMP` analysis showed:

- unusually high CPU use over a short WMI process lifetime.
- many WMI threads.
- repeated PowerShell `Get-PnpDeviceProperty` work.
- repeated `Win32_PnPEntity` / device-property requests.
- evidence consistent with overlapping or parallel PnP inventory scans.

Current leading attribution: Sentinel or its startup/worker path was spawning or enabling the PowerShell/WMI polling storm. This is separate from the WHEA hardware-memory events.

## 1.5 BeamNG/RLS evidence collected

- Vanilla BeamNG is substantially more stable than the heavy RLS/mod setup.
- Approximately 158 of 159 mods were enabled in one reviewed configuration.
- Active mod archives were roughly 29 GB.
- BeamNG committed memory reached approximately 19.6–21.1 GB in recorded low-memory events.
- Total system commit reached roughly 69.5–71.0 GB out of a limit around 71.8 GB.
- Physical RAM reached approximately 96–97%.
- Direct3D reported `0x8007000e` / not enough memory.
- .NET and PowerShell also failed allocations during the crash cascade.
- BeamNG logs hit large error counts and log limits.
- Duplicate meshes, JBeam parts, overlapping packages, and older/newer versions were present.
- Console evidence showed repeated `streamUpdate cycle is already active` messages and heavy SmartMinimap pursuit-table/debug output.
- The game can degrade within roughly five minutes until David must terminate and reload it.

The BeamNG/RLS track is a confirmed user-mode trigger and resource amplifier. It does not explain corrected platform-memory WHEA records.

# 2. Versions and attempts

## 2.1 v1.3.2 — Readability/Data Restore

**Historical status:** baseline referenced, not independently closed in issue #6.  
**Known value:** intended to preserve readability and data collection.  
**Known problem:** later active-worker evidence still reported 1.3.2 while a v1.4.1 startup marker existed.

**Required disposition:** historical baseline only; do not call accepted unless David confirms the exact package and results.

## 2.2 v1.4.0 — Unattended Flight Recorder

**Intended changes:** startup scheduling, restart-on-failure, five-minute checkpointing, six-hour ZIPs, expanded events/process/drive collection, evidence UI, and unattended recording.

**What was tried:** static JSON/XAML/delimiter/feature/ZIP checks.

**Failure:** native Windows PowerShell parser errors and startup failure. Static Linux-side checks did not validate the actual Windows PowerShell 5.1 execution path.

**Required disposition:** `REJECTED — parser/startup failure`.

## 2.3 v1.4.1 — Startup hotfix candidate

**What was claimed:** startup/parser corrections.

**What remains unproven:** exact native Windows PowerShell 5.1 parse, WPF load, task registration, checkpoint creation, reboot recovery, and sustained low-overhead behavior.

**Additional concern:** the installed marker/worker version mismatch means captured evidence cannot be cleanly assigned to v1.4.1.

**Required disposition:** `UNVERIFIED / REJECTED FOR RELEASE USE` until exact proof exists.

## 2.4 No next version assigned yet

Do not reuse v1.4.1. The next build should receive a new number only after this audit is accepted and the pre-edit GitHub checkpoint is posted. A likely number is v1.4.2, but the number is not official until David authorizes the next-version start.

# 3. Immediate freeze and safety state

Until the next version begins:

1. Keep Sentinel closed.
2. Disable Sentinel startup/scheduled tasks that spawn PowerShell or the worker.
3. Do not delete Sentinel reports, dumps, autosaves, or crash timestamps.
4. Do not run Sentinel and BeamNG stress tests together.
5. Do not leave BeamNG/RLS loading unattended.
6. Back up important data from mechanical drives before repair scans or destructive work.
7. Stop a BeamNG test before Windows commit reaches 85–90%.
8. Keep the old failing mechanical drives out of the pagefile plan.

# 4. Mandatory governance for every future Sentinel version

Each version requires seven separate checkpoints.

## Gate A — Pre-edit

Post and commit:

- current version and state.
- exact source/package filename, bytes, and SHA-256.
- exact defects being fixed.
- exact files permitted to change.
- files that must not change.
- UI/readability requirements.
- private-data handling rules.

No editing begins before Gate A exists.

## Gate B — Post-edit source review

Post and commit:

- every changed file.
- changed functions/sections.
- reason for each change.
- risks and rollback method.
- source diff summary.

## Gate C — Native validation

Required before packaging:

- native Windows PowerShell 5.1 parser test.
- WPF/XAML load test.
- JSON/settings parse.
- scheduled-task command validation without enabling auto-start.
- single-instance test.
- child-process count test.
- WMI query-rate test.
- log/checkpoint write test.

Static non-Windows checks may supplement but may not replace this gate.

## Gate D — Package

Post:

- exact ZIP name.
- bytes.
- SHA-256.
- complete file list.
- version state: `CANDIDATE — NOT DAVID TESTED`.

## Gate E — David controlled test

David tests the exact hash in a new folder. Record:

- launch result.
- UI screenshot/readability.
- PowerShell process count.
- WMI CPU.
- total CPU and memory.
- checkpoint creation.
- report creation.
- stop/restart behavior.
- reboot behavior.
- any new errors.

## Gate F — Acceptance or rejection

The GitHub state must explicitly become one of:

- `ACCEPTED`
- `REJECTED`
- `ROLLED BACK`

## Gate G — Next version authorization

Only after Gate F may a new version number be created.

# 5. Next Sentinel recovery build — required engineering scope

The next version is a safety/reliability build, not a feature expansion.

## 5.1 Process and WMI containment

- Enforce one recorder instance with a named mutex or equivalent lock.
- Enforce one dashboard instance.
- Prevent overlapping scheduled-task launches.
- Do not spawn one PowerShell process per device or polling cycle.
- Use one cached PnP inventory pass at startup.
- Refresh device inventory slowly or event-driven.
- Hard concurrency limit of 1 for WMI/PnP work.
- Add exponential backoff after WMI errors, delays, or quota events.
- Add a hard timeout for every external query.
- Track and display child-process count.
- Stop collecting rather than multiplying workers when the system is under pressure.

## 5.2 Bounded monitoring

- Replace unbounded incident creation with state transitions and cooldowns.
- One incident per condition until recovery or a defined escalation interval.
- Cap incident attachments by size and age.
- Rotate logs.
- Configurable retention and storage budget.
- Never fill the selected drive.
- Pause noncritical collection under high commit, paging, disk queue, or CPU.
- A diagnostic monitor must reduce its workload when the machine is unstable.

## 5.3 Reliable checkpoints

- Atomic write: write temporary file, flush, then rename.
- Never leave a zero-filled primary checkpoint.
- Keep last-known-good checkpoint.
- Validate JSON before replacing the prior checkpoint.
- Recover from interrupted writes and file locks.
- Include version, process ID, start time, and schema version.

## 5.4 Accurate process attribution

- Fix the collector that recorded only `System Idle Process`.
- Collect top CPU, private bytes, commit, working set, I/O, handles, threads, parent process, and command path where safe.
- Record sampling timestamp and collection duration.
- Detect stale samples and clearly mark them stale.
- Do not present delayed data as current data.

## 5.5 Version integrity

Use one version constant/source shared by:

- UI title.
- worker state.
- startup marker.
- scheduled-task arguments.
- autosaves.
- report manifests.
- ZIP metadata.
- checksums and release notes.

The app must refuse to start when incompatible mixed-version files are detected.

## 5.6 UI/readability release gate

- Restore readable foreground/background contrast.
- Fix white-on-white controls.
- Fix sort controls and selected-row visibility.
- Preserve the v1.3.2 readability intent.
- Require Windows screenshots before acceptance.
- No theme redesign during the safety build unless required to repair readability.

## 5.7 Safe startup model

- Auto-start disabled by default in the candidate.
- Manual recorder start first.
- Scheduled-task installation is a separate explicit action.
- Provide a one-click emergency stop/disable command.
- Provide a safe mode that opens the UI without starting collectors.
- Startup task must not relaunch repeatedly after rapid failures.

# 6. Controlled test plan for the next Sentinel version

Run these in order and stop at the first failure.

## Test 1 — Parser and UI only

- No scheduled tasks.
- No collectors.
- Native PowerShell 5.1 parse.
- Open UI.
- Verify readability and version.
- Close cleanly.

## Test 2 — Recorder idle, 15 minutes

- Manual start.
- No BeamNG.
- No browser workload.
- Confirm only expected PowerShell processes.
- WMI Provider Host should settle near normal idle behavior.
- No repeated PnP scans.
- No incident storm.

## Test 3 — Recorder idle, 60 minutes

- Confirm stable CPU, memory, handles, thread count, WMI usage, log growth, and checkpoint rotation.
- Confirm no overlapping worker.

## Test 4 — Controlled stop/restart

- Stop from UI/script.
- Verify clean state.
- Restart once.
- Verify one worker.

## Test 5 — One reboot

- Only after prior tests pass.
- Enable one scheduled task.
- Reboot once.
- Confirm one instance and correct version.

## Test 6 — Light workload

- Browser/video only.
- No BeamNG.
- Confirm monitor overhead remains low.

## Test 7 — Failure injection

- Simulate unavailable WMI query, locked checkpoint, low disk-space threshold, and collector timeout.
- Confirm backoff and bounded reporting.

BeamNG testing starts only after Sentinel passes all seven tests or remains disabled.

# 7. Hardware/memory isolation roadmap

This track remains necessary even after Sentinel is fixed.

## Step H1 — Back up data

Back up important files from the mechanical drives before scans or repairs.

## Step H2 — Test matched Corsair pair only

- Power off fully.
- Remove both PNY DIMMs.
- Install the Corsair pair in the motherboard-recommended two-DIMM slots.
- Keep XMP off and use JEDEC defaults.
- Confirm BIOS memory size and speed.

## Step H3 — Bootable memory test

- Run at least four complete passes.
- Any error is a failure.
- Record exact test version, configuration, pass count, and error addresses.

## Step H4 — Test matched PNY pair only

Repeat in the same recommended slots.

## Step H5 — Isolate stick versus slot

If a pair fails, test one stick at a time and repeat in another slot.

## Step H6 — BIOS review

After data backup and stable power, check for a newer stable BIOS for the exact PRIME Z490-P board. Record current settings and follow ASUS procedures. Reapply safe defaults after update.

## Step H7 — Escalation

- One pair passes, one fails: replace failing pair.
- Both pairs pass separately, four sticks fail: four-DIMM compatibility/IMC load issue; use one matched kit.
- Same slot fails with multiple known-good sticks: suspect slot, motherboard trace, socket contact/pins, or CPU memory controller.
- WHEA memory events continue with known-good RAM at defaults: prioritize board, CPU/socket, BIOS, and power diagnostics.

# 8. Pagefile and disk-pressure roadmap

Before the next BeamNG test:

1. Record current free space on C: and D:.
2. Preserve at least 15–20% free space where practical.
3. Use a system-managed pagefile on a healthy NVMe SSD.
4. Do not place the pagefile on the old drives with bad-block history.
5. Reboot after the change.
6. Record:
   - `Win32_PageFileUsage`
   - pagefile drive and allocated size
   - C:/D: free space
   - Task Manager committed used/limit
7. Do not change pagefile settings again during the same comparison run.

A larger pagefile can delay allocation failure but cannot repair a memory leak, mod conflict, or defective RAM.

# 9. BeamNG/RLS/mod roadmap

## Step B1 — Preserve current state

- Back up the current BeamNG user folder and career save.
- Preserve mod inventory and logs.
- Do not delete the original setup while diagnosing.

## Step B2 — Clean user folder

- Clear cache using BeamNG support tools.
- Disable all mods.
- Start vanilla BeamNG and confirm baseline.

## Step B3 — RLS-only test

- Enable only the exact current RLS Career Overhaul core and strictly required dependency/map.
- Remove duplicate/older RLS ZIPs.
- Create a new test career as required by the RLS release instructions.
- Disable SmartMinimap, custom radio/RDRADIO, Traffic Reborn, TrailSpotter/PiP, RedFox tow/recovery utilities, parked cars, police, and extra traffic for the first run.
- Use DX11 initially.
- No Chrome, overlays, recording, or hardware-monitor polling during the test.

## Step B4 — Monitor commit

- Watch Task Manager `Committed` used/limit.
- Stop when commit reaches 80–85% or climbs continuously.
- Never leave a loading screen unattended.
- Record one-, three-, five-, and ten-minute values.

## Step B5 — Binary reintroduction

- Add one required expansion.
- Test.
- Add mods in groups of five to ten.
- Test each group.
- When failure returns, split that group and repeat.

## Step B6 — Console/log storm isolation

First suspects based on visible evidence:

1. SmartMinimap debug/pursuit output.
2. RDRADIO/custom radio.
3. Traffic Reborn.
4. RedFox Tow & Recovery UI/apps.
5. duplicate CDC wheel/trailer/vehicle packages.

Keep the console closed during performance testing and inspect `beamng.log` afterward.

# 10. BeamNG Mod Conflict Scanner roadmap

This is a separate application project and must not be mixed into the Sentinel safety build.

## Scanner Stage 1

- ZIP inventory.
- metadata.
- internal paths.
- SHA-256 hashes.
- identical/different duplicate paths.
- duplicate versions.
- Excel export.
- SQLite cache.

## Scanner Stage 2

- Lua/JSON/JBeam/JS identifier extraction.
- extension names.
- dependencies.
- action IDs.
- settings/save keys.
- global namespaces.
- direct two-mod comparison.

## Scanner Stage 3

- dependency graph.
- confidence scoring.
- HTML report.
- load-order analysis.
- recommended loadout.

## Scanner Stage 4

- guided compatibility-repair workflow.
- backup originals.
- show exact planned edits.
- require confirmation.
- never rewrite mods automatically without explicit approval.

# 11. Required GitHub structure going forward

Recommended paths:

```text
PC_STABILITY/
  INCIDENT_REPORTS/
  ROADMAPS/
  SENTINEL/
    BASELINES/
    SOURCE/
    VERSION_REPORTS/
    TEST_RESULTS/
    SCHEMAS/
  HARDWARE_TESTS/
  BEAMNG_TESTS/
```

For each version, commit:

- pre-edit report.
- source changes or sanitized source package.
- test matrix.
- release/package manifest.
- final accepted/rejected state.

Issue #6 remains the notification and coordination lane; permanent records belong in files under `PC_STABILITY/`.

# 12. Current next action

1. Audit file committed.
2. This master roadmap committed.
3. Post both commit SHAs and the audit counts to issue #6.
4. Keep Sentinel disabled.
5. David reviews and accepts/corrects the audit baseline.
6. Only then open the pre-edit checkpoint for the next Sentinel version.

**Roadmap state:** READY FOR DAVID REVIEW — no new build authorized yet.
