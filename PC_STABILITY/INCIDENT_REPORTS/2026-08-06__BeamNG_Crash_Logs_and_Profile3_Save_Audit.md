# BeamNG Crash Logs and Profile 3 Save Audit

**Audit date/time:** 2026-08-06 11:15 PDT  
**Workstream:** PC Stability / BeamNG RLS / Career Save Integrity  
**Files inspected locally, read-only:**

| File | Bytes | SHA-256 |
|---|---:|---|
| `current.zip` | 657,489 | `b3167a36eb35ee3b9907dae04ab88e4d1f550323bd4189357ce4422d5a4aad95` |
| `Profile 3.zip` | 39,329,214 | `ed7e85ce72e3bd2e0ce547a2edc802a47392094e05b1b3f4dba2da4c8e1f7d10` |

No raw logs, save files, screenshots, usernames, or private paths were uploaded to GitHub.

## Executive result

- The uploaded `Profile 3.zip` is **not broadly corrupted**. ZIP CRC/integrity passed, every JSON file parsed, all PNGs verified, the two current autosave slots are structurally complete, and referenced active vehicles have matching vehicle files.
- There is one real **RLS logical-data defect**: `globalEconomy.json` contains duplicate JSON object keys inside `activeEvents` in both autosave2 and autosave3. A normal JSON parser keeps only the last duplicate key, so earlier economy events can be silently overwritten.
- The current BeamNG logs show a severe mod/content error storm, one launcher-reported application hang, one generic exit-code-1 failure, and recent WER entries for BeamNG access violations and transient hangs.
- The current sessions loaded `settings/cloud/saves/bkup/autosave3`, **not `Profile 3`**.
- Launcher cleanup logs also show a nested save path equivalent to `saves/Profile 3/Profile 3/...`, indicating at least one copy of Profile 3 was extracted one folder too deep. This can make BeamNG load the wrong copy or make the expected profile appear missing/outdated even though the uploaded save itself is intact.

## Save archive structural audit

`Profile 3.zip` contains:

- 656 ZIP entries.
- 617 regular files.
- No duplicate archive filenames.
- No zero-byte regular files.
- ZIP integrity/CRC test: PASS.
- 553 JSON files: all 553 parse successfully.
- 59 PNG files: all 59 pass image verification.

### Save slots

| Slot | Regular files | Approx. uncompressed size | Status |
|---|---:|---:|---|
| autosave1 | 9 | 5,721 bytes | Old/incomplete initial slot; do not use as the recovery target |
| autosave2 | 303 | 133,198,205 bytes | Structurally complete |
| autosave3 | 303 | 129,521,612 bytes | Structurally complete and newest |

`autosave3/info.json`:

- creation date: `2026-07-21T22:47:14Z`
- save date: `2026-08-05T22:32:25Z`
- save version: `61`

`autosave2` is only about 16 seconds older than autosave3 and is also structurally valid.

### Vehicle consistency

Both autosave2 and autosave3 contain 53 numbered vehicle JSON records. In autosave3:

- favorite vehicle: 1
- last vehicle: 28
- spawned vehicles: 21, 28, 43

All referenced vehicle IDs have matching vehicle JSON files. No missing active-vehicle reference was found.

### Duplicate-key defect

Both:

- `autosave2/career/rls_career/globalEconomy.json`
- `autosave3/career/rls_career/globalEconomy.json`

contain duplicate keys in `activeEvents`.

Examples:

- `jobMarket.activeEvents` serializes keys in the sequence `1, 2, 1, 2` for four different events.
- `vehicleMarket.activeEvents` serializes keys in the sequence `1, 1, 2`.

JSON object keys are supposed to be unique. Standard parsers retain the final occurrence, so earlier events can disappear on load. This is a likely RLS save-serialization bug. It is not evidence that the entire profile is unreadable, but it is a repair target for the mod.

No manual rewrite was performed because changing active-event identifiers without the RLS loader/source contract could cause a worse mismatch.

## Career/save logs

- `career.log` contains thousands of normal informational entries and repeated successful save records to autosave2/autosave3.
- The save-local `beamng_backalley.log` files contain repeated successful car-theft data saves.
- No explicit `corrupt save`, JSON parse failure, failed career load, or failed autosave message was found in the uploaded profile logs.

## Current BeamNG crash/hang evidence

### Engine logs

| Log | Session start | Errors | Warnings | Log cap |
|---|---|---:|---:|---|
| `beamng.3.log` | 2026-08-06 10:07:34 | 12,805 | 180 | Reached 15,000-entry cap at ~58 s |
| `beamng.2.log` | 2026-08-06 10:29:33 | 12,265 | 844 | Reached 15,000-entry cap at ~117 s |
| `beamng.1.log` | 2026-08-06 10:44:18 | 11,327 | 1,420 | Reached 15,000-entry cap at ~73 s |
| `beamng.log` | 2026-08-06 11:12:17 | 121 | 176 | No; clean shutdown at ~49 s |

The capped logs are dominated by:

- duplicate JBeam parts;
- duplicate part names across mod/common folders;
- duplicate materials/datablocks;
- missing/failed texture and material resources;
- invalid/missing input action `redfox_career_dev_toggle_launcher`;
- repeated extension unload-mode errors.

This volume is enough to discard the rest of each log, so the final failure sequence may be missing.

### Launcher outcomes

- Launcher history includes `0xCFFFFFFF STATUS_APPLICATION_HANG` after about 1,409 seconds.
- Another launch ended with generic exit code `0x00000001` after about 568 seconds.
- Two other recorded launches exited normally.

### WER snapshot in dxDiag

The dxDiag WER section includes recent BeamNG entries for:

- APPCRASH in `BeamNG.drive.x64.exe` with `c0000005` access violation.
- APPCRASH involving `KERNELBASE.dll` with exception `e0000008`.
- `AppHangTransient` for BeamNG.

The dxDiag block does not provide event timestamps, so these cannot be assigned with certainty to one exact log session.

No fresh `0x8007000e`/out-of-memory marker appears in this uploaded `current.zip`. The current evidence is a mod/content error storm plus hangs/access violations, distinct from the previously documented commit-exhaustion event.

## Save-path/order problem

Two August 6 game sessions explicitly loaded:

`settings/cloud/saves/bkup/autosave3/career/general.json`

They did not load `Profile 3`.

The launcher cleanup log also references a nested structure equivalent to:

`settings/cloud/saves/Profile 3/Profile 3/autosave3/...`

The expected structure is:

`settings/cloud/saves/Profile 3/autosave3/info.json`

The nested path strongly suggests the archive's outer `Profile 3` folder was extracted into an already-existing `Profile 3` folder. This is a placement/copy problem, not proof of file corruption.

## Confidence

- High: uploaded ZIP and core save structure are intact.
- High: autosave2 and autosave3 are both parseable and structurally complete.
- High: the game sessions shown loaded `bkup`, not Profile 3.
- High: a nested `Profile 3/Profile 3` save copy exists or existed during launcher cleanup.
- High: current mod set is producing an extreme error flood and log truncation.
- Moderate: duplicate `globalEconomy.activeEvents` keys are causing lost/overwritten RLS economy events.
- Low: save corruption is the primary cause of the BeamNG access violations; the logs do not establish that.

## Risks

- Continuing to save into the wrong profile (`bkup`) can make new progress diverge from the uploaded Profile 3 backup.
- Moving/deleting folders before a complete copy can destroy the only current version.
- Automatic support-tool cleanup moves files and complicates comparison of mods and saves.
- Editing duplicate economy-event keys without the RLS source contract may damage RLS state.

## Required next action

1. Do not delete or overwrite any save folders.
2. Close BeamNG after the current session.
3. Copy the entire `settings/cloud/saves` directory to a dated backup folder.
4. Verify the folder tree and identify which profile contains the newest `autosave3/info.json` date.
5. Correct the nested `Profile 3/Profile 3` placement only after the full backup exists.
6. Confirm whether David intends to continue from `Profile 3` or from `bkup` before another save is made.
7. Keep autosave2 and autosave3; do not use the incomplete autosave1 as the recovery source.
8. Separately isolate the mod error storm; save structure does not explain 11,000–12,800 errors per launch.
