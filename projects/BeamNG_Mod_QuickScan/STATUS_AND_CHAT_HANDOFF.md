# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Primary chat:** BeamNG Mod QuickScan / Catalog Manager  
**Repository:** redfoxtrystman/RedFox_Master_Control  
**Master record:** `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`  
**Incident record:** `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`  
**Latest release record:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_0_CATALOG_CAREER_DRM.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/README_AND_VERIFICATION.md`  
**Career contract:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/CAREER_EXPORT_FORMAT.md`  
**DRM rules:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/DRM_DETECTION_NOTES.md`

## Read before doing work

Every chat or Codex session must read:

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md`
3. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
4. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
5. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_0_CATALOG_CAREER_DRM.md`
6. This status file.

## Split-chat reconciliation

Two chats were discussing the same application. Their requirements are merged into v0.4.0. Do not revive a separate scanner branch without recording why.

Merged requirements include:

- one-ZIP-at-a-time unattended scanning;
- adjustable checkpoints and low-load operation;
- Pause, Resume Saved Scan, Cancel, and queue reconciliation;
- automatic handling of common malformed BeamNG metadata;
- DRM/protection indicator reporting;
- preview extraction;
- version-aware ZIP rename planning;
- backup-first reversible renaming;
- catalog copying and original-name records;
- career vehicle JSON/JSONL/CSV/schema exports for another application;
- purple/seafoam theme presets;
- Knight Rider-style activity sweep;
- automatic readable foreground contrast;
- scanner data stored on the selected BeamNG drive.

## Current truth

- v0.2.0 opened and scanned on David's Windows computer but contained known false positives.
- v0.3.0 passed Python compilation and a synthetic self-test.
- v0.3.1 delivered documented unattended queue and pause/resume behavior and passed static/synthetic tests.
- The exact v0.3.1 source package was not available in the active runtime, File Library, or GitHub source tree when v0.4.0 began.
- v0.4.0 is a consolidated implementation of documented v0.3.1 behavior and merged requirements. It is **not** presented as a line-for-line v0.3.1 patch.
- v0.4.0 passed compile, self-tests, real uploaded caravan validation, rename backup/undo tests, GUI construction smoke tests, package reopen, packaged compile, packaged self-test, and packaged GUI smoke test.
- v0.4.0 has not yet been tested by David on Windows with a large real mod collection.

## Current development baseline

```text
BeamNG Mod QuickScan.pyw v0.4.0
```

Hashes:

```text
v0.4.0 source
5df54228831e38bce32439935006d75883a71389bcfc767d73d5090daab358b4

v0.4.0 final package
46fb770afae8ef622815a9a8c58f91c0925aaa1144959f695d01fe3dfa00a4cd

caravan2_v1.1.zip validation source
3075c41ab8321702126a2be4d408ecf70de94995720531b467dd1be70ee65568
```

Label:

```text
STATIC/SELF-TEST VERIFIED
REAL UPLOADED CARAVAN VALIDATION PASS
WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN
```

## v0.4.0 delivered behavior

### Scanner and resource behavior

- exact `.zip` scanning only;
- one ZIP active at a time;
- Very Low Load, Low Load, Balanced, and Auto-Pilot modes;
- adjustable checkpoint size down to one;
- unattended continuation;
- per-ZIP SQLite commits;
- Pause, Resume Saved Scan, Cancel;
- changed, new, missing, and interrupted ZIP reconciliation;
- disk-backed SQLite temporary work;
- full ZIP and internal-file hashes;
- exact/repacked/version duplicate checks;
- shared-path and full override checks;
- generic metadata and local Lua variable false positives remain suppressed.

### Automatic metadata recovery

- strict JSON first;
- UTF-8 BOM recovery;
- line-comment recovery;
- block-comment recovery;
- trailing-comma recovery;
- repairs are recorded;
- the original ZIP is not rewritten;
- only unrecoverable metadata remains a warning.

### DRM indicator detection

- encrypted/password-protected entries;
- executable/native payloads;
- activation, license, HWID, member verification, remote authentication, anti-tamper, and strong obfuscation context;
- documentation-only wording is excluded from strong conclusions;
- detection only, no bypass or removal.

### Catalog and previews

- up to three useful preview images copied outside the ZIP;
- metadata-linked repository images preferred;
- `info` / `mod_info` image preference;
- vehicle default image fallback;
- version-aware proposed ZIP names;
- load-order prefix warning;
- collision-safe names;
- backup-first rename;
- hash verification after rename;
- original-name map;
- undo last rename;
- copy to catalog without removing the original.

### Career vehicle export

```text
career_exports/career_vehicle_catalog.json
career_exports/career_vehicle_catalog.jsonl
career_exports/career_vehicle_catalog.csv
career_exports/career_vehicle_catalog.schema.json
career_manifests/<zip-hash>.json
```

Exports source ZIP identity, model, configuration, `.pc` path, main vehicle data, career configuration metadata, preview records, metadata quality, DRM indicators, missing fields, safe inferences, and `spawn_ready` state.

QuickScan does not invent missing prices, years, performance values, population, drivetrain, or fuel information.

### Theme

- Knight Rider Purple;
- Knight Rider Seafoam;
- Purple / Seafoam Dark;
- Seafoam / Purple Light;
- Classic Dark;
- flip palette;
- dark text on light backgrounds;
- light text on dark backgrounds;
- custom back-and-forth sweep widget.

## Real uploaded caravan result

```text
Mod: caravan2_v1.1.zip
Detected name: Stretched Travel Trailer
Detected version: 1.1
Detected uploader: Ealan120
Vehicle model: caravan2
Vehicle type: Trailer
Default configuration: Standard
Spawn-ready configurations: 4
Career-valued JBeam parts: 11
Full-size previews extracted: 3
Proposed name: Stretched Travel Trailer v1.1.zip
DRM: No DRM indicators detected
Blocking malformed metadata warning: none
```

The trailing comma in `vehicles/caravan2/info.json` was recovered automatically. Missing career fields were exported as missing instead of being invented.

## Verification completed

```text
PASS  Python compile
PASS  built-in self-test
PASS  one-ZIP-at-a-time unattended scan
PASS  checkpoint size 1
PASS  duplicate/full override tests
PASS  tolerant metadata recovery
PASS  contextual DRM test
PASS  preview extraction
PASS  career export files
PASS  pause/resume
PASS  real caravan validation
PASS  rename backup/hash/undo
PASS  GUI/theme/sweep construction smoke test
PASS  final ZIP reopen and CRC
PASS  packaged compile
PASS  packaged self-test
PASS  packaged GUI smoke test
```

## Not proven

- real Windows DPI at 100%, 125%, 150%, and 200%;
- real Windows mouse interaction;
- thousands-of-mods performance on David's computer;
- every possible custom DRM system;
- automatic creation of missing career values.

## What David should test first

Use a copied folder containing a small group of real mods.

```text
Checkpoint every: 2
Computer load: Auto-Pilot or Very Low Load
Extract preview images: enabled
Build career export: enabled
Automatic rename: disabled
```

Confirm:

1. app opens and remains readable;
2. Knight Rider sweep moves;
3. scan continues automatically;
4. Pause and Resume work;
5. previews appear in Catalog;
6. Career Data shows vehicle/config records;
7. DRM status has evidence and confidence;
8. metadata repairs are explained;
9. proposed ZIP names are correct;
10. Apply Selected Rename creates a backup and Undo restores the original;
11. CPU and RAM remain usable.

## Next safe step

Do not make another broad rewrite.

First record David's Windows v0.4.0 results. Patch only verified failures or clearly bounded additions. Keep normal scanning read-only. Any rename or catalog modification must remain previewed, backup-first, verified, and reversible.

## Current handoff

```text
Project: BeamNG Mod QuickScan / Catalog Manager
Version: v0.4.0 Catalog + Career Data + DRM + Theme
Baseline inspected: documented v0.3.1 records; exact v0.3.1 source unavailable and recorded
Files changed: consolidated Python source; launchers; career contract; DRM notes; reports; verification
Before-edit checks: v0.3.1 GitHub records and merged requirements inspected
After-edit checks: compile, self-test, real caravan validation, rename/undo test, GUI smoke PASS
Packaged ZIP reopened: PASS
Packaged source compile: PASS
Packaged self-test: PASS
Packaged GUI smoke: PASS
Windows runtime tests by David: NOT YET RUN FOR v0.4.0
Proven: static source, synthetic engine tests, real caravan parsing/export, package integrity
Not proven: David's large Windows collection, DPI, real resource behavior at scale
Known limitations: custom DRM can evade static indicators; missing career values are not invented
Release record commit: 0ff379d34194b1daa8f7294b74527d9c77d48b08
Verification record commit: 6215048533e6d077f54309fd169e13303fcc8708
Career contract commit: 54e6918f49031d71a9be55f9b84125ed710128a5
DRM notes commit: 48726cac9d2592d85610ad4f5f6db34437aecba6
Next safe step: David tests v0.4.0 on a copied real mod folder
```
