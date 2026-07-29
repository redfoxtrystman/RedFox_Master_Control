# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.4 Duplicate Organizer + Side-by-Side Comparison  
**Latest release record:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_4_DUPLICATE_ORGANIZER.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_4/README_AND_VERIFICATION.md`  
**Career contract:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/CAREER_EXPORT_FORMAT.md`  
**DRM rules:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/DRM_DETECTION_NOTES.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.4 release records
5. This file

## Current truth

- v0.4.3 corrected unreadable native dropdowns, duplicate over-sensitivity, and automatic image destinations.
- David required duplicates and older versions to be physically separated into review folders.
- v0.4.4 adds a review-first, reversible duplicate organizer.
- A completed scan groups connected duplicate findings and recommends a keeper.
- Exact, repacked, functional duplicates, and lower versions can be moved.
- Same-version variants with changed functional files remain review-only and are never auto-moved.
- Every duplicate group receives its own folder under `_QuickScan_Duplicate_Review`.
- Moved ZIPs and images end with `_DUPLICATE` before the extension.
- The review folder is excluded from future scans.
- Windows folder marker files use a red-dot `.ico` and `desktop.ini`.
- Side-by-side HTML identifies the keeper, newer/older versions, unique paths, changed paths, and exact changed text/code lines.
- A manifest is written around each operation; Undo restores moved ZIPs/images.
- v0.4.4 passed compile, built-in self-test, packaged tests, and exact uploaded Roamer/Transporter scan/move/undo regression tests.
- Physical Explorer icon display and large-library Windows cleanup remain David tests.

## Hashes

```text
v0.4.3 baseline source
25317a5553fb7f0730e38a1b0380b38c483954dfac084180aa40d41f6d7e8578

v0.4.4 source
2e1fd616e8dec86fc12bf96a656d8fd1e28a1aa23401f6930d28212f76944698

v0.4.4 package
b00112834f2870a127a2eceb4f84ace7a2844f704e17e0c4bab38b6dc3db2636
```

## Controlling rename law

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD A MISSING VERSION OR UPDATE AN EXISTING VERSION TOKEN.
DO NOT REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
IF NO VERSION IS FOUND, DO NOT INVENT ONE.
```

## Duplicate evidence law

- Exact same ZIP SHA-256: exact duplicate.
- Same complete internal path/hash set: repacked duplicate.
- Same functional files with only docs/metadata/previews different: functional duplicate.
- Lower versions require strong identity evidence and overlapping functional content.
- Generic vehicle folders or similar titles alone are not enough.
- Matching preview hashes support a finding but are not sole proof.

## Duplicate movement law

```text
KEEP:
- newest detected version;
- otherwise the best-supported equal/unknown-version copy;
- user-selected keeper override when set.

MOVE:
- exact duplicates;
- repacked duplicates;
- confirmed functional duplicates;
- lower versions.

REVIEW ONLY:
- same-version variants with changed gameplay files.
```

## Duplicate output

```text
<selected folder>/_QuickScan_Duplicate_Review/
```

Every group folder contains moved copies, images, keeper recommendation, manifest, side-by-side comparison, `RedDot.ico`, and `desktop.ini`.

Reports:

```text
RedFoxTools/BeamNG Mod QuickScan/duplicate_review/SIDE_BY_SIDE_DUPLICATE_REVIEW.html
RedFoxTools/BeamNG Mod QuickScan/reports/duplicate_side_by_side.html
```

## Required real results

```text
Roamer:
KEEP roamerpack_00.zip
MOVE roamersadfaw_DUPLICATE.zip
Exact renamed duplicate

Transporter:
KEEP ta_transporter_0.5 tg_m0dsbeamng.zip
MOVE car_ta_transporter_v0.5_DUPLICATE.zip
Same functional mod/version; documentation-only extras
```

## Preserved features

- custom readable purple/seafoam controls and text modes;
- full-screen Catalog and scrollbars;
- version-only naming;
- vehicle/map/UI preview/icon extraction;
- beside-ZIP and catalog image exports;
- career JSON/JSONL/CSV/schema exports;
- DRM indicator detection only;
- unattended one-ZIP-at-a-time scan;
- checkpoints, Pause, Resume, Cancel, queue reconciliation.

## What David should test

1. Extract v0.4.4 into a new folder and confirm the title.
2. Run a complete scan on a copied small batch.
3. Open Duplicate Review.
4. Inspect the recommended keeper and side-by-side report.
5. Change the keeper when desired.
6. Move one selected group first.
7. Confirm the active keeper stayed in place.
8. Confirm moved ZIPs/images have `_DUPLICATE` names.
9. Confirm each group folder displays the red-dot icon after reopening Explorer.
10. Test Undo Last Duplicate Cleanup.
11. Only then test Move All Confirmed Duplicates.

## Current handoff

```text
Project: BeamNG Mod QuickScan / Catalog Manager
Version: v0.4.4 Duplicate Organizer
Baseline: exact packaged v0.4.3 source
Before-edit: baseline hash, compile, self-test, real duplicate evidence checked
After-edit: compile, self-test, GUI smoke, synthetic organizer, real Roamer/Transporter move+undo PASS
Packaged ZIP reopened: PASS
Packaged source compile: PASS
Packaged self-test: PASS
Packaged GUI smoke: PASS
Packaged real-pair regression: PASS
Windows runtime by David: REQUIRED
Known limitations: Explorer icon cache, Windows permissions, thousands-of-mods cleanup unproven
Release commit: 3c2732fb6fd1f7dd5d607712884a4b2406b54d0c
Verification commit: 3c5482dbd22da20ea3142e23fe3417f28041913d
Next safe step: David tests one selected duplicate group and Undo on a copied folder
```
