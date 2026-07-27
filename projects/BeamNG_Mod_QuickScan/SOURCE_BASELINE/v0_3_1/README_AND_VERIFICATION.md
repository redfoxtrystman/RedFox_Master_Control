# BeamNG Mod QuickScan v0.3.1 Source Baseline and Verification

**Version:** 0.3.1  
**Patch:** Unattended Scan + Safe Pause  
**Baseline:** v0.3.0  
**Runtime label:** `STATIC/SELF-TEST VERIFIED — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Exact hashes

```text
v0.3.0 source SHA-256
f22e2bd4e4a0dbcffa92e21c288ef892bbf14f498bdf2934172a03ca9cdc9ae9

v0.3.1 source SHA-256
04286362af5d9c95e5dd2120fb637be54592d252cf0a9b7f5f68faf59791a4b3

v0.3.1 package SHA-256
fd9b6bddcc9b34d2bd94b3f444c5c5a807ed53d5cf0d11fd6cc959eeb198d4cc
```

## Source comparison

- v0.3.0: 1,054 lines
- v0.3.1: 1,713 lines
- Approximate added lines: 667
- Approximate deleted lines: 8
- Approximate changed lines: 229

The downloadable package contains the complete `BeamNG Mod QuickScan.pyw` source and a side-by-side colored HTML comparison against v0.3.0.

## Verification results

```text
PASS  v0.3.0 compile
PASS  v0.3.0 self-test
PASS  v0.3.1 compile
PASS  v0.3.1 built-in self-test
PASS  extended pause-during-large-file test
PASS  resume using a new Engine instance
PASS  changed/new ZIP reconciliation
PASS  Tkinter window construction under Xvfb
PASS  final ZIP reopen and CRC test
PASS  packaged source compile
PASS  packaged self-test
```

## Package file inventory

```text
BASELINE_v0_3_0.json
BeamNG Mod QuickScan.pyw
PATCH_CHANGE_REPORT.md
README.txt
RUN SELF TEST.bat
SIDE_BY_SIDE_COLORED_DIFF.html
START BeamNG Mod QuickScan.bat
TEST_REPORT.txt
VERIFICATION.json
```

## Source rules preserved

- exact `.zip` scanning only;
- `.zip.disabled` and similar renamed backups are not treated as active ZIPs;
- generic root `info.json` / `mod_info.json` metadata does not create a destructive conflict by itself;
- ordinary local Lua variables do not create module collisions;
- full disk ZIP and internal-file SHA-256 hashes are retained;
- existing v0.3 data stays under the selected BeamNG drive;
- the existing permanent SQLite library is migrated in place by adding queue tables;
- no ZIP is rewritten by this patch.

## Current source custody

The full source snapshot is in:

```text
BeamNG_Mod_QuickScan_Python_v0_3_1_Unattended_Pause.zip
```

Any chat or Codex session receiving that package must verify the source SHA-256 above before editing it.

Do not substitute a recreated source file or begin from an older scanner unless David explicitly chooses a rollback.

## Next version boundary

v0.3.2 is reserved for the Auto-Pilot resource manager:

- CPU pressure monitoring;
- available-memory monitoring;
- automatic read-delay and chunk-size changes;
- automatic checkpoint reduction;
- critical-pressure pause and recovery;
- clear resource status in the interface.

Do not mix image extraction or catalog renaming into v0.3.2 until the scanner foundation has been tested on Windows.