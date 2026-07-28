# BeamNG Mod QuickScan v0.4.0 — Source Custody and Verification

**Version:** 0.4.0  
**Release:** Catalog, Career Data, DRM Scan, and Theme  
**Runtime label:** `STATIC/SELF-TEST VERIFIED — REAL CARAVAN VALIDATION PASS — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Source custody

The exact v0.3.1 source ZIP referenced by the earlier chat was not available in the active runtime, File Library search, or shared GitHub source tree. GitHub contained v0.3.1 verification records and hashes, but not the source file itself.

This build therefore does **not** claim a line-for-line patch against v0.3.1. It is a consolidated implementation based on:

- documented v0.3.1 unattended queue, checkpoints, one-ZIP-at-a-time scanning, low-load profiles, pause, resume, and reports;
- the master QuickScan roadmap;
- expanded scanner requirements;
- the pasted split-chat requirements;
- the uploaded `caravan2_v1.1.zip` test case.

## Exact hashes

```text
v0.4.0 source SHA-256
5df54228831e38bce32439935006d75883a71389bcfc767d73d5090daab358b4

v0.4.0 final package SHA-256
46fb770afae8ef622815a9a8c58f91c0925aaa1144959f695d01fe3dfa00a4cd

caravan2_v1.1.zip test source SHA-256
3075c41ab8321702126a2be4d408ecf70de94995720531b467dd1be70ee65568
```

## Verification results

```text
PASS  Python compile
PASS  built-in self-test
PASS  full unattended scan
PASS  checkpoint size 1
PASS  one ZIP active at a time
PASS  exact duplicate detection
PASS  confirmed same-path career.lua override detection
PASS  contextual DRM indicator detection
PASS  .zip.disabled ignored
PASS  tolerant trailing-comma metadata recovery
PASS  preview extraction
PASS  career JSON/JSONL/CSV/schema export
PASS  catalog plan/original-name/DRM/metadata reports
PASS  pause after a safe commit
PASS  resume saved queue
PASS  real uploaded caravan validation
PASS  Tkinter construction under Xvfb
PASS  Knight Rider sweep construction
PASS  theme palette flip construction
PASS  backup-before-rename
PASS  ZIP hash unchanged after rename
PASS  rename database record
PASS  undo restored original filename and hash
PASS  final package reopen and CRC test
PASS  packaged source compile
PASS  packaged self-test
PASS  packaged GUI smoke test
```

## Real caravan validation

```text
Source ZIP: caravan2_v1.1.zip
Scan status: complete
ZIPs completed: 1 of 1
Blocking malformed metadata warnings: 0
Detected name: Stretched Travel Trailer
Detected version: 1.1
Detected author/uploader: Ealan120
Detected vehicle model: caravan2
Detected vehicle type: Trailer
Detected default configuration: Standard
Spawn-ready configurations exported: 4
JBeam parts with career monetary value: 11
Full-size preview images extracted: 3
Proposed ZIP name: Stretched Travel Trailer v1.1.zip
DRM result: No DRM indicators detected
```

Missing price, year, performance, drivetrain, fuel, and population values were left blank and listed. They were not invented.

## Not proven

- real Windows 100%, 125%, 150%, and 200% DPI interaction;
- real Windows mouse behavior;
- thousands-of-mods runtime on David's hardware;
- every possible custom DRM system;
- automatic generation of missing career prices or performance values.

## Source availability

The complete source is included in the delivered package:

```text
BeamNG_Mod_QuickScan_v0_4_0_Catalog_Career_DRM.zip
```

Any future chat or Codex session must verify the source hash above before editing it. Do not substitute a reconstructed older scanner without recording the baseline change.