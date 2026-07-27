# BeamNG Mod QuickScan / Catalog Manager
## Complete Project Record, Requirements, Roadmap, and Codex Handoff

**Created:** 2026-07-26 19:39 PDT / America/Los_Angeles  
**Requested by:** David / Captain  
**Maintained by:** Sol and every RedFox chat or Codex session working on this project  
**Repository:** `redfoxtrystman/RedFox_Master_Control`

---

# 1. Purpose

Build one dependable Python/Tkinter tool that can:

1. Scan one BeamNG mod or thousands of mod ZIPs.
2. Find real duplicate files, different versions, code collisions, overrides, dependencies, missing base mods, and unreadable archives.
3. Avoid fake warnings caused only by generic metadata files or ordinary local Lua variables.
4. Manage its own CPU, RAM, and drive load instead of choking the computer.
5. Run unattended overnight, save every completed ZIP, pause safely, close, and resume later.
6. Extract useful preview images without changing the original ZIP.
7. Rename ZIPs using detected names and versions only after preview, backup, and approval.
8. Sort mods into a clean catalog by type and manufacturer.
9. Export SQLite, JSON, searchable HTML, and color-coded XLSX reports.
10. Preserve enough evidence to repair selected conflicts later.

This project must be built in stages. A roadmap item is not a completed feature until its implementation and tests are recorded in GitHub.

---

# 2. Current Truth

## v0.2.0 Python build

David ran this build on Windows.

Proven:

- The app opened.
- It scanned six active ZIPs.
- It generated JSON and text reports.
- It reported zero broken ZIPs and zero red findings.

Known accuracy failures:

- Root `mod_info.json` files in unrelated mods were treated as path conflicts.
- Ordinary local Lua names such as `seen`, `names`, `parts`, `out`, `candidates`, and `vehicles` were treated as module collisions.

The v0.2 report is useful as proof that the scanner ran, but its fourteen yellow warnings are not trustworthy conflict results.

## v0.3.0 Python baseline

Static/self-test evidence exists for:

- Python compilation.
- Built-in synthetic tests.
- Chunked ZIP and internal-file reading.
- Throttled progress messages.
- SQLite library code.
- Batch cursor and cache reuse.
- Exact/repacked duplicate tests.
- Version comparison where `1.10` is newer than `1.9`.
- Ignoring generic metadata path overlap.
- Not treating local Lua variable names as shared modules.

Not yet proven by David:

- Windows responsiveness with 50–60 real mods.
- Scanning thousands of ZIPs overnight.
- Actual CPU and RAM throttling.
- Pause/resume.
- Recovery after app or Windows restart.
- XLSX and searchable HTML reports.
- Dependency graph.
- Image extraction.
- ZIP renaming and catalog sorting.
- Guided compatibility repair.

Current label:

```text
v0.3.0 DEVELOPMENT BASELINE
STATIC/SELF-TEST VERIFIED
WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN
```

---

# 3. RedFox Ground Rules

Before editing:

1. Open and inspect the current baseline.
2. Record the version and file hashes.
3. List the exact files that will change.
4. Make a complete source backup.
5. Run current tests and save their output.

After editing:

1. Run syntax checks.
2. Run scanner tests.
3. Compare edited files to the baseline.
4. Package the output.
5. Reopen the final ZIP.
6. Verify the promised files and behavior-specific evidence.
7. Create a changed-file list, side-by-side diff, test report, verification report, known-limitations report, and next-step handoff.

Never:

- remove working code without permission;
- replace David's requested design with a different system;
- claim runtime success from syntax or packaging alone;
- call a build working, fixed, ready, complete, final, live, real, or proven without evidence;
- modify or move an original mod without backup and approval.

The main scanner must use normal Python 3 and Tkinter. Do not require .NET, Visual Studio, Java, Node, administrator permission, or pip packages merely to run the scanner.

All large data must be stored on the selected BeamNG drive or another user-selected location, not forced onto C:.

Suggested data structure:

```text
<Selected Data Location>\
└── RedFoxTools\
    └── BeamNG Mod QuickScan\
        ├── database\
        ├── database_backups\
        ├── reports\
        ├── batch_reports\
        ├── scan_sessions\
        ├── preview_images\
        ├── catalog_plans\
        ├── original_names\
        ├── backups\
        ├── logs\
        ├── errors\
        └── settings\
```

---

# 4. Scan Modes

## Quick Scan

Check filenames, metadata, ZIP hashes, internal paths, internal hashes, obvious duplicates, versions, overrides, and unreadable ZIPs.

## Full Scan

Read source and structured content including Lua, JSON, JBeam, JavaScript, HTML, CSS, materials, input actions, manifests, `modScript.lua`, settings/save keys, UI IDs, extension IDs, dependencies, texture/model references, and override targets.

## Deep Comparison

Compare two selected mods line by line and explain:

- identical, changed, added, and removed files;
- matching virtual paths;
- action/UI/save/settings collisions;
- full-file overrides;
- dependency or addon relationships;
- probable load-order result;
- recommended repair category.

---

# 5. Performance and Auto-Pilot

The scanner processes **one ZIP at a time**. Batch size controls checkpoint/report frequency, not simultaneous ZIP workers.

User-selectable checkpoint batch sizes:

```text
1, 2, 5, 10, 25, 50, 100, or custom
```

Resource modes:

- Very Low Load
- Low Load
- Balanced
- Fast (optional, never default)
- Auto-Pilot

Auto-Pilot watches:

- scanner process RAM;
- available system memory;
- scanner/system CPU pressure;
- drive response when available;
- UI heartbeat;
- time on current ZIP/file;
- queue backlog;
- database/report write time;
- time since last progress.

Under pressure, it may:

- reduce read chunk size;
- increase pauses between chunks or ZIPs;
- run garbage collection;
- delay noncritical image/report work;
- reduce checkpoint size from 25 to 10, 5, 2, or 1;
- save a checkpoint and pause before the next ZIP;
- automatically resume only after an automatic resource pause.

A manual pause must never automatically resume.

The UI must always show a moving heartbeat plus current ZIP, current internal file, ZIP/file counters, completed/remaining ZIPs, batch number, processed MB, elapsed time, time since last completed file, RAM/CPU pressure, drive status, and last database save time.

Status wording must be direct:

```text
Working normally
Reading a large file
Waiting on a slow drive
Saving checkpoint
Paused because memory is low
Possible stalled ZIP
Skipped one unreadable file
```

---

# 6. Overnight, Pause, and Resume

Night Scan automatically continues batch after batch without button presses.

After every completed ZIP:

- commit its result to SQLite;
- save its path, hash, scan mode, parser version, completion time, and status;
- update the remaining queue.

After every checkpoint batch:

- write a timestamped batch report;
- update cumulative master reports;
- rotate a database backup.

## Manual Pause

The Pause button must be cooperative and safe.

When pressed:

1. Show `Pause requested — finishing the current safe step.`
2. Finish the current read chunk.
3. Finish the current internal file when practical.
4. Finish and commit the ZIP if it can be completed safely.
5. Otherwise close it and mark only that ZIP incomplete for rescan.
6. Save all completed work and the remaining queue.
7. Flush logs and database writes.
8. Release file handles and temporary buffers.
9. Show `Paused safely. Completed work has been saved.`

The paused screen must offer:

- Resume Scan
- Close and Resume Later
- Review Queue
- Cancel Remaining Queue

## Filesystem validation on resume

Before resuming, check folders, paths, size, modified time, and hash when needed.

If files changed:

- preserve unchanged completed results;
- requeue changed ZIPs;
- add new ZIPs;
- mark missing/moved ZIPs for review;
- show a clear summary before continuing.

---

# 7. Permanent SQLite Library

Store:

- original/current ZIP filename and path;
- ZIP size, modified time, SHA-256;
- detected name, version, author, manufacturer, type;
- vehicle IDs;
- internal paths and hashes;
- code identifiers;
- dependencies and conflict relationships;
- duplicate/version groups;
- preview-image records;
- proposed catalog destination;
- manual decisions;
- parser version and scan time;
- backup and undo records.

Rules:

- transaction per completed ZIP;
- rotating backups;
- startup validation and recovery;
- unchanged-ZIP cache reuse;
- import useful old scan data without importing known false-positive warnings;
- remember manual decisions such as safe together, intentional, ignored, base mod, addon, duplicate, and not duplicate.

---

# 8. Conflict and Dependency Analysis

Never claim conflict solely because two mods contain generic metadata files.

Classify shared paths as:

- identical duplicate;
- different duplicate;
- full override conflict;
- intentional addon;
- compatibility bridge;
- unknown/manual review.

Extract real shared identifiers, not local variable names:

- `extensions.load` / `extensions.unload`;
- `M.dependencies`;
- extension/global namespaces;
- exported module functions;
- input action IDs;
- action-filter groups;
- UI app/window IDs;
- settings/save keys;
- career module names;
- event hooks;
- override targets;
- JBeam part IDs and relevant slot types.

Every finding must explain why it was flagged and show confidence:

```text
Confirmed, Very High, High, Medium, Low, or Unknown
```

Dependency relationships:

- requires;
- optional integration;
- loads;
- overrides;
- patches;
- duplicates;
- conflicts;
- newer/older version;
- standalone alternative.

Do not rely on one giant graph. Tables and filters are required; graphs are optional for selected groups.

---

# 9. Duplicate and Version Rules

Version detection priority:

1. internal metadata;
2. `info.json`;
3. `mod_info.json`;
4. manifests;
5. version strings in source;
6. filename;
7. content similarity.

Examples:

```text
Ford Truck v3.0.zip
Ford Truck v3.1.zip
```

These are different versions, not duplicates.

Confirmed duplicate naming:

```text
Ford Truck v3.0.zip
Ford Truck v3.0 Duplicate.zip
Ford Truck v3.0 Duplicate 2.zip
```

Same claimed version but different code must be treated as variants/manual review, not automatically as confirmed duplicates.

---

# 10. Preview Images and Catalog Organizer

Scanning remains read-only.

Image selection order:

1. images in an `info` folder;
2. images in a `mod_info` folder;
3. images referenced by metadata;
4. `default.png`;
5. `default.jpg`;
6. `default.jpeg`;
7. other likely vehicle previews.

Do not extract entire texture libraries, normal maps, roughness maps, or tiny UI icons unless no better preview exists.

Copy selected images outside the ZIP and name them after the proposed ZIP:

```text
Ford Truck v3.1.png
Ford Truck v3.1_02.png
Ford Truck v3.1_03.png
```

Suggested catalog:

```text
Catalog\
├── Car\
├── Truck\Ford\
├── SUV\
├── Van\
├── Bus\
├── Semi\
├── Trailer\
├── Parts\
├── Maps\
├── UI Apps\
├── Career\
├── Gameplay\
└── Unknown - Needs Review\
```

Organizer modes:

- Preview only (default)
- Copy to catalog
- Move to catalog
- Rename only
- Extract images only
- Copy and rename
- Move, rename, and extract

Before any rename or move:

1. preserve original filename/path/hash in SQLite and `original_names.json`;
2. make a full backup;
3. show every planned change;
4. warn when numeric or `z`/`zz`/`zzz` prefixes may change load order;
5. require confirmation;
6. use collision-safe filenames;
7. verify the destination ZIP opens;
8. write an undo manifest;
9. never delete the only original automatically.

Renaming is not a permanent fix for two different files occupying the same BeamNG virtual path.

---

# 11. Reports

Required outputs:

- SQLite database
- JSON
- searchable HTML
- color-coded XLSX
- dependency graph data
- optional SVG/PNG graph for selected groups

XLSX sheets:

1. Mod Inventory
2. Conflicts
3. Shared Paths
4. Code Identifiers
5. Dependencies
6. Duplicate Versions
7. Recommended Loadout
8. Catalog Plan
9. Errors and Unreadable Files

Colors:

- dark red: confirmed destructive conflict;
- red: very likely conflict;
- orange: possible conflict;
- yellow: shared system needing review;
- blue: dependency/integration;
- green: compatible or identical duplicate;
- gray: unknown.

---

# 12. Guided Repair

Never rewrite mods automatically.

Possible repair suggestions:

- merge both code changes;
- replace a full override with a hook;
- rename global/action/UI/settings/save identifiers;
- create a compatibility bridge;
- remove copied base files from an addon;
- declare a dependency;
- archive an obsolete version.

Any selected repair requires original backup, exact change preview, side-by-side diff, confirmation, new ZIP, reopened package verification, and a change report.

---

# 13. Build Stages

## Stage 0 — Stabilize current Python scanner

False-positive regression tests, chunked reads, honest progress, cancellation, baseline/diff verification, and a real 50–60 mod Windows test.

## Stage 1 — Inventory and permanent library

SQLite, per-ZIP commits, unattended queue, adjustable checkpoints, pause/resume, filesystem validation, backups, Quick Scan, combined reports, and old-data import.

## Stage 2 — Auto-Pilot

RAM/CPU/drive monitoring, safe throttling, automatic resource pauses, watchdog, keep-awake, and clear live status.

## Stage 3 — Full conflict reports

Real identifier extraction, path index, confidence, pairwise explanations, deep comparison, XLSX/HTML/JSON, and recommended actions.

## Stage 4 — Images and catalog

Preview extraction, version-aware names, duplicate names, manufacturer/type sorting, preview-only plan, backups, undo, copy/move options.

## Stage 5 — Dependencies and load order

Base/addon/bridge detection, missing dependencies, load-order evidence, and filtered graph data.

## Stage 6 — Guided compatibility repair

Manual repair selection, backups, diffs, rebuilt ZIP verification, and no unapproved edits.

---

# 14. Required Tests

At minimum test:

- exact and repacked duplicates;
- v1.9 versus v1.10;
- same version/different code;
- generic metadata in several mods;
- same local Lua variable names;
- real duplicate input/UI IDs;
- same override path/different code;
- base/addon and missing dependency;
- broken/encrypted ZIP;
- huge file and thousands of tiny files;
- interruption, pause, close/reopen resume, database recovery;
- files added/moved/deleted/changed while paused;
- low-memory and slow-drive behavior;
- info/default preview extraction;
- avoiding texture libraries;
- rename collisions, load-order warnings, undo, and `original_names.json` recovery.

---

# 15. Codex and Chat Working Instructions

Every session must:

1. Read this record, the current status file, and relevant incident reports.
2. Inspect the current source before changing it.
3. Work on one stage only.
4. List exact changed files.
5. Run tests and fix failures.
6. Package and reopen the output.
7. Commit source, roadmap/status updates, test evidence, diff, and verification.
8. State what is proven and what remains unproven.

Required handoff:

```text
Project:
Version:
Baseline inspected:
Files changed:
Before-edit checks:
After-edit checks:
Packaged ZIP reopened:
Static tests:
Windows runtime tests by David:
Proven:
Not proven:
Known problems:
GitHub commit:
Next safe step:
```

Use direct language. Write like a real modding tool, not corporate or AI filler.

---

# 16. Permanent Artifact Package

A downloadable consolidated package was created on 2026-07-26 containing:

- this project record;
- roadmap/Codex handoff;
- status/handoff;
- QuickScan incident report;
- expanded requirements;
- v0.2 test reports;
- v0.3 source baseline and verification;
- small Python build archives;
- SHA-256 file manifest.

Package filename:

```text
BeamNG_Mod_QuickScan_COMPLETE_PROJECT_RECORD_2026-07-26.zip
```

Final local package SHA-256:

```text
cb9d32365e7dc57ec5ef3bd9600db7515aea4c136131b2dd8fe7f322ac9c3aea
```

---

# Final Controlling Statement

The goal is not a scanner that looks smart. The goal is a scanner that safely gets through the collection, preserves its work, explains real problems, avoids fake warnings, and never risks original mods without clear approval.

That is the project.