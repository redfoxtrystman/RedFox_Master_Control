# BeamNG Mod QuickScan v0.4.0 — Catalog, Career Data, DRM Scan, and Theme

**Date built:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Built by:** Sol / BeamNG Mod QuickScan chat  
**Status:** `STATIC/SELF-TEST VERIFIED — REAL CARAVAN VALIDATION PASS — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Why this release exists

Two chat branches were discussing the same scanner. Their requirements are merged here into one release:

- preserve unattended one-ZIP-at-a-time scanning and safe pause/resume;
- automatically recover common malformed metadata instead of stopping at a vague warning;
- extract useful preview images;
- propose and safely apply version-aware ZIP names;
- create catalog plans and reversible rename records;
- detect DRM/protection indicators without bypassing or removing them;
- export machine-readable vehicle and career metadata for another application;
- add purple/seafoam themes and a Knight Rider-style activity sweep;
- preserve all scan data on the selected BeamNG drive.

## Baseline custody note

The exact v0.3.1 source package was not available in the active runtime, File Library, or repository source tree when this build began. v0.4.0 is therefore a consolidated implementation of the documented v0.3.1 behavior and merged requirements, not a line-for-line patch. This is recorded to prevent a false baseline claim.

## Exact hashes

```text
Source SHA-256
5df54228831e38bce32439935006d75883a71389bcfc767d73d5090daab358b4

Final package SHA-256
46fb770afae8ef622815a9a8c58f91c0925aaa1144959f695d01fe3dfa00a4cd

Uploaded caravan test SHA-256
3075c41ab8321702126a2be4d408ecf70de94995720531b467dd1be70ee65568
```

## Implemented behavior

### Scanner foundation

- exact `.zip` discovery only;
- `.zip.disabled`, `.zip.old`, and other renamed backups ignored;
- one ZIP active at a time;
- Very Low Load, Low Load, Balanced, and Auto-Pilot modes;
- adjustable checkpoint sizes down to one mod;
- automatic unattended continuation;
- per-ZIP SQLite commits;
- Pause, Resume Saved Scan, Cancel, and queue reconciliation;
- disk-backed SQLite temporary work;
- exact ZIP and internal-file SHA-256 hashing;
- exact duplicates, repacked duplicates, version groups, shared-path conflicts, and full override detection;
- generic metadata paths and ordinary local Lua names do not create fake conflicts.

### Automatic metadata recovery

QuickScan tries strict JSON first, then safely retries common BeamNG mod mistakes:

- UTF-8 BOM;
- `//` comments;
- `/* ... */` comments;
- trailing commas.

The original ZIP is not rewritten. The report records whether a file was strict, repaired, or still unreadable. Valid alternate metadata files remain usable when one file is bad.

### DRM/protection indicators

QuickScan reports evidence for:

- encrypted/password-protected ZIP entries;
- executable or native payloads;
- activation/license/HWID/member-verification logic;
- remote endpoints coupled to authentication or license checks;
- anti-tamper/integrity checks;
- strong obfuscation patterns.

Documentation-only words such as `license`, `author`, or `licenseplate` are not enough to create a strong DRM result. The scanner detects and reports protection; it does not bypass or remove it.

### Preview extraction and catalog planning

- chooses up to three useful preview images;
- metadata-linked repository images have highest priority;
- `info` / `mod_info` images are preferred;
- vehicle `default.png`, `.jpg`, or `.jpeg` is a fallback;
- textures, normal maps, roughness maps, and tiny icons are deprioritized;
- images are copied outside the mod ZIP and renamed to match the proposed ZIP name;
- catalog plan, original-name map, metadata repair report, and DRM report are exported.

### ZIP rename safety

- preview-first; no automatic rename during a normal scan;
- backup before rename;
- original path, name, and hash retained;
- load-order prefix warning for numeric or `z`/`zzz` names;
- collision-safe filename generation;
- ZIP contents are not rewritten;
- post-rename hash verification;
- undo record and Undo Last Rename action;
- Copy to Catalog leaves the original in place.

### Career vehicle export

QuickScan writes:

```text
career_exports/career_vehicle_catalog.json
career_exports/career_vehicle_catalog.jsonl
career_exports/career_vehicle_catalog.csv
career_exports/career_vehicle_catalog.schema.json
career_manifests/<zip-hash>.json
```

Each vehicle/configuration record can contain:

- source ZIP path and hash;
- vehicle model folder;
- configuration ID and `.pc` path;
- main vehicle metadata;
- `Value`, `Years`, `Population`, drivetrain, fuel, propulsion, transmission, performance class, configuration type, power, torque, weight, top speed, and paints when present;
- preview source/output paths;
- metadata quality and automatic repairs;
- DRM indicator summary;
- missing recommended fields;
- safe inferred display fields.

QuickScan never invents missing prices, years, performance values, population, drivetrain, or fuel information.

### Theme system

Presets:

- Knight Rider Purple;
- Knight Rider Seafoam;
- Purple / Seafoam Dark;
- Seafoam / Purple Light;
- Classic Dark.

The palette can be flipped. Foreground text is selected for contrast so dark text is used on light backgrounds and light text on dark backgrounds. The activity indicator is a custom back-and-forth Knight Rider sweep.

## Uploaded caravan validation

`caravan2_v1.1.zip` produced:

```text
Status: complete
Blocking malformed-metadata warnings: 0
Detected name: Stretched Travel Trailer
Detected version: 1.1
Detected uploader: Ealan120
Vehicle model: caravan2
Vehicle type: Trailer
Default configuration: Standard
Spawn-ready configurations: 4
JBeam parts with career monetary value: 11
Full-size previews extracted: 3
Proposed ZIP name: Stretched Travel Trailer v1.1.zip
DRM result: No DRM indicators detected
```

The malformed `vehicles/caravan2/info.json` trailing comma was recovered automatically. Missing career price/year/performance fields were left blank and listed rather than invented.

## Verification

```text
PASS  Python compile
PASS  built-in self-test
PASS  unattended scan and checkpoint size 1
PASS  one-ZIP-at-a-time test
PASS  duplicate and full override tests
PASS  tolerant metadata recovery test
PASS  DRM contextual detection test
PASS  preview extraction test
PASS  career JSON/JSONL/CSV/schema export test
PASS  pause and resume test
PASS  real uploaded caravan validation
PASS  rename backup/hash/undo test
PASS  Tkinter construction and theme/sweep smoke test
PASS  final package reopen and CRC test
PASS  packaged source compile
PASS  packaged self-test
PASS  packaged GUI smoke test
```

## Not proven

- real Windows DPI interaction at 100%, 125%, 150%, and 200%;
- real Windows mouse behavior;
- thousands-of-mods runtime on David's hardware;
- every custom DRM system;
- automatic generation of missing career values, which is deliberately not implemented.

## First Windows test

Use a copied folder with a small group of real mods:

```text
Checkpoint every: 2
Computer load: Auto-Pilot or Very Low Load
Extract preview images: enabled
Build career export: enabled
Apply ZIP renames automatically: disabled
```

Review the Catalog and Career Data tabs before applying any rename.