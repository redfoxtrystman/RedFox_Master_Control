# RedFox System Sentinel / PC Crash Workstream
## GitHub and Order-of-Operations Audit

**Audit date/time:** 2026-07-27 16:34 PDT  
**Audited repository:** `redfoxtrystman/RedFox_Master_Control`  
**Primary coordination lane:** Issue #6 — PC Stability / Crash Monitor — Shared Diagnostic Coordination  
**Audit scope:** Evidence available from issue #6, its 14 comments, the current PC crash/Sentinel chat, accessible handoff material, and repository file/commit searches.

## Important limitation

This is a **minimum verified audit**, not a claim that every historical chat was fully recoverable. Some older chats reached their context limit, and this auditor cannot reconstruct messages that are absent from the available conversation history, handoffs, and GitHub record. Missing or unverifiable history is treated as a traceability problem rather than filled in by guessing.

## Governing requirements

Issue #6 requires every participating chat to record the workstream, date/time, current build version, exact files inspected and changed, fixes, tests performed and not performed, crashes/errors, timestamps, reports, hypothesis, confidence, risks, next action, and what David must test or preserve.

It also states that permanent summaries, schemas, source notes, test matrices, and sanitized diagnostic reports should be committed under `PC_STABILITY/`; a monitor build must not be called working until David tests that exact build; and one diagnostic chat must not overwrite another chat's application or reports without documenting the change.

## Top-line count

The audit found **14 unique compliance incidents**.

- **11 incidents include a missed, late, incomplete, or unverifiable GitHub checkpoint.**
- **12 incidents include an order-of-operations violation.**
- **3 incidents include an unsupported or overstated claim.**
- Categories overlap; do not add 11 + 12 + 3 as though they were separate events.

Issue #6 does contain 14 useful comments. The failure is not that GitHub was never used. The failure is that the record was not maintained consistently **between each version/state transition and before proceeding to the next step**.

## Incident register

### IR-01 — v1.3.2 baseline had no standalone version checkpoint

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** The first major issue update is for v1.4.0 and references `RedFox_System_Sentinel_v1.3.2_READABILITY_DATA_RESTORE.zip` only as a prior comparison artifact. There is no separate issue #6 version entry establishing v1.3.2's exact release state, files, test result, known defects, and acceptance status.

**Why this matters:** The next build started without a complete authoritative baseline. Later regressions in readability, data collection, and startup behavior were therefore harder to attribute.

**Required correction:** Backfill v1.3.2 as `Historical baseline — status unknown/not accepted unless David explicitly confirms`.

---

### IR-02 — v1.4.0 failure and v1.4.1 replacement were combined instead of sequenced

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** Issue comment `5007386268` combines the v1.4.0 startup/parser failure and the v1.4.1 hotfix in one post.

**Why this matters:** The required sequence was: record v1.4.0 failure, freeze it, identify root cause, then create and document v1.4.1. Combining those states creates an after-the-fact record and obscures exactly what changed before the new package existed.

**Required correction:** Mark v1.4.0 `REJECTED — native Windows PowerShell parser failure` and keep its failure record separate from v1.4.1.

---

### IR-03 — v1.4.1 was described as a hotfix without native Windows proof

**Type:** Order-of-operations violation; unsupported/overstated claim  
**Evidence:** The v1.4.1 issue entry calls it a startup hotfix while also admitting that static Linux-side validation could not certify Windows PowerShell 5.1 behavior and that David still had to run the native self-test.

**Why this matters:** A package may be called a candidate or proposed fix, but not a verified hotfix when the failing platform/parser has not executed it.

**Required correction:** Relabel historical v1.4.1 as `UNVERIFIED CANDIDATE`, not a working release.

---

### IR-04 — no acceptance, rejection, or rollback closure for v1.4.1

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** Issue #6 has no separate version closure stating that David tested the exact v1.4.1 package, with native parser output, UI startup, scheduled-task state, checkpoint creation, reboot behavior, and final accepted/rejected status.

**Why this matters:** The workstream moved into evidence collection while the active release status remained ambiguous.

**Required correction:** Close v1.4.1 as `REJECTED/UNTRUSTED` unless exact Windows proof can be produced.

---

### IR-05 — version marker and active worker disagreed

**Type:** GitHub/version-control miss; order-of-operations violation  
**Evidence:** The camping-run scan found `startup-v1.4.1-enabled.marker`, while active `worker-state.json` reported `Version=1.3.2`. This mismatch was mentioned in diagnostic evidence but was never resolved with an authoritative rollback, reinstall, or version-state entry.

**Why this matters:** Logs cannot be reliably assigned to a build when the marker, worker, package, and UI do not share one version source.

**Required correction:** The next version must use one immutable version value shared by UI, worker, scheduled tasks, markers, reports, and package metadata.

---

### IR-06 — Sentinel source/build upload could not be verified in the repository

**Type:** GitHub traceability failure  
**Evidence:** Repository file searches for `Sentinel` and `RedFox System Sentinel`, plus commit search for `Sentinel`, returned no result during this audit. Issue comments contain package names, byte counts, and hashes, but no verified source/build commit was found.

**Limitation:** Repository code-search index status was unknown. Therefore this is not proof that no related file exists anywhere; it is proof that the supposed upload cannot be located or verified through the available repository record.

**Required correction:** Commit sanitized source, schemas, version notes, and checksums under a stable `PC_STABILITY/SENTINEL/` structure. Do not commit private logs or dumps.

---

### IR-07 — no permanent audit/roadmap file existed under PC_STABILITY before this audit

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** Issue #6 explicitly says permanent summaries and sanitized diagnostic reports should be committed under `PC_STABILITY/`. The workstream relied primarily on issue comments.

**Required correction:** This audit and the new master roadmap are being committed now.

---

### IR-08 — `current.zip` was not recorded in issue #6

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** `current.zip` was uploaded in the chat, but issue #6 contains no match for that filename and no issue entry confirms its size, SHA-256, inspection status, findings, or whether it was intentionally skipped.

**Required correction:** Before relying on it, inspect it read-only and add filename, bytes, SHA-256, scope, findings, and limitations.

---

### IR-09 — `mods.zip` was not recorded in issue #6

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** `mods.zip` was uploaded in the chat, but issue #6 contains no match for that filename and no issue entry confirms its size, SHA-256, inspection status, findings, or whether it was intentionally skipped.

**Required correction:** Treat it as pending evidence until a read-only inventory and GitHub checkpoint are complete.

---

### IR-10 — Windows integrity-test result was not posted

**Type:** GitHub checkpoint miss  
**Evidence:** The chat history records that DISM/SFC work was performed and SFC was clean, but issue #6 contains no `SFC` or `DISM` result.

**Why this matters:** This result narrows the Windows-corruption hypothesis and should be part of the permanent diagnostic matrix.

**Required correction:** Backfill the exact commands, date, output/result, and limitations if preserved. Do not invent missing output.

---

### IR-11 — readability/theme regression was not logged as a formal release blocker

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** David reported unreadable white-on-white controls and sort-control/theme regressions. Issue #6 contains no matching defect entry.

**Why this matters:** v1.3.2 was specifically a readability/data-restore baseline. Reintroducing unreadable controls is a regression and should block the next release.

**Required correction:** Add UI readability to the mandatory release gate and require screenshots from David's Windows test.

---

### IR-12 — latest BeamNG/Chrome out-of-memory event was initially attributed to Sentinel

**Type:** Order-of-operations violation; unsupported attribution; user correction required  
**Evidence:** David corrected the record: Sentinel was not running during that latest BeamNG + Chrome event. Issue comment `5040504950` later records the correction.

**Why this matters:** Attribution was made before confirming whether the suspected process was active.

**Required correction:** For every incident, first establish an active-process timeline, then separate trigger, amplifier, and independent background faults.

---

### IR-13 — pagefile advice changed without one authoritative configuration checkpoint

**Type:** GitHub checkpoint miss; order-of-operations violation  
**Evidence:** The workstream used several different pagefile arrangements and recommendations. Issue evidence records observed pagefile sizes and disk pressure, but there is no single signed-off configuration entry showing the exact before state, change made, reboot, after state, free space, and committed-memory limit.

**Why this matters:** Pagefile changes materially alter crash behavior and can invalidate comparisons.

**Required correction:** Freeze one healthy-SSD pagefile plan, record exact settings before change, reboot, then record `Win32_PageFileUsage`, free space, and Task Manager commit limit before any BeamNG test.

---

### IR-14 — static validation was treated too strongly despite actual parser failure

**Type:** Order-of-operations violation; unsupported/overstated verification  
**Evidence:** The v1.4.0 entry says static checks passed, but Windows later found PowerShell parser errors, missing string termination, and missing braces. Linux-side delimiter/XAML checks did not validate the actual Windows PowerShell 5.1 execution path.

**Why this matters:** The wrong verification layer was allowed to act as a release gate.

**Required correction:** Native Windows PowerShell 5.1 parse and WPF-load testing must occur before packaging and before any version is called fixed.

## Things the chats did correctly

This audit is not a claim that all work failed. The following were correctly recorded or corrected:

- Issue #6 was created as a shared coordination lane and contains 14 substantive comments.
- Large private logs and dumps were generally kept off public GitHub; filenames, sizes, hashes, and findings were posted instead.
- v1.4.0 was initially labeled a candidate rather than a David-tested release.
- The camping-run scan documented 84,854 files, 11.75 GB, 4,152 incident folders, 307 report ZIPs, commit pressure, pagefile pressure, storage warnings, failed process attribution, and the version mismatch.
- The correction that Sentinel was not running during the later BeamNG/Chrome OOM event was posted.
- The live WMI/PowerShell storm, BeamNG console flood, WMI dump findings, consolidated crash evidence, and Sentinel suspicion were posted.
- Ending the PowerShell group reduced CPU from roughly 95–98% to 19%, which strongly tied the live CPU storm to PowerShell-driven WMI work.

## Product defects that must be treated separately from chat-compliance failures

These are confirmed or strongly evidenced Sentinel defects and are not counted again as GitHub/order incidents:

1. Multiple or overlapping PowerShell processes performing repeated `Get-PnpDeviceProperty` / WMI device scans.
2. WMI Provider Host CPU and private-memory runaway.
3. No reliable single-instance guard.
4. Process attribution returning only `System Idle Process` with null CPU.
5. Thousands of repeated incident captures for one sustained condition.
6. Report/incident growth to 84,854 files and 11.75 GB.
7. Checkpoint failures, file-lock errors, missing paths, and a zero-filled/corrupt checkpoint.
8. Recorder delays of minutes under pressure.
9. Crash artifact naming collisions/`unknown` overwrites.
10. Version-marker/worker mismatch.
11. UI readability/theme regressions.
12. Monitoring activity amplifying disk, commit, and CPU pressure during an already unstable event.

## Root-cause status at audit time

The investigation must remain split into three tracks:

1. **Hardware/memory subsystem:** repeated corrected WHEA platform-memory events, mixed Corsair/PNY DIMMs, varied bugchecks, and access-violation patterns. This is the leading explanation for kernel-level instability but does not identify one bad stick without isolation testing.
2. **Sentinel/WMI overload:** PowerShell fan-out and repeated PnP/WMI queries can independently drive CPU to 100%, overload WMI Provider Host, and worsen freezes.
3. **BeamNG/RLS/mod workload:** vanilla is more stable; the RLS/mod set causes commit exhaustion, console/log storms, duplicate/override conflicts, and five-minute performance collapse. This is a user-mode trigger/amplifier, not a sufficient explanation for WHEA memory errors.

## Governance rule effective immediately

No new Sentinel version may begin until the previous state is posted and committed.

For every version, in this order:

1. **Pre-edit checkpoint:** current version, exact source/package hash, active defects, requested changes, and files to touch.
2. **Edit/build work.**
3. **Post-edit checkpoint:** exact changed files and line/function summary.
4. **Native test checkpoint:** what actually ran on Windows and what did not.
5. **Package checkpoint:** exact ZIP name, bytes, SHA-256, included files, and release state.
6. **David test checkpoint:** exact build tested, screenshots/logs, pass/fail, regressions.
7. **Close state:** `ACCEPTED`, `REJECTED`, or `ROLLED BACK`.
8. Only then may the next version number be assigned.

Allowed release states:

- `DRAFT`
- `CANDIDATE — NOT WINDOWS TESTED`
- `CANDIDATE — WINDOWS SELF-TEST PASSED`
- `DAVID TESTING`
- `ACCEPTED`
- `REJECTED`
- `ROLLED BACK`

The words `working`, `fixed`, `final`, or `release` must not be used before David tests that exact artifact and the GitHub close-state entry is posted.

## Audit disposition

**Status:** FAILED — corrective records required before the next version.  
**Next action:** Commit the master roadmap, post both audit and roadmap to issue #6, freeze Sentinel auto-start, and do not assign the next version until David approves this audit baseline.
