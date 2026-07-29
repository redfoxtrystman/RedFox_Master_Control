# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-29 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.5 Results Workspace + Previous Scans + Career Wizard  
**Latest release record:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_5_RESULTS_HISTORY_CAREER_WIZARD.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_5/README_AND_VERIFICATION.md`  
**Career field notes:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_5/OFFICIAL_CAREER_FIELD_NOTES.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. v0.4.0 through v0.4.5 release records
5. v0.4.5 verification and career field notes
6. This file

## Current truth

- v0.4.4 is the exact verified baseline used for v0.4.5.
- v0.4.4 baseline compile and full self-test passed before editing.
- v0.4.5 adds a maximizable lower results workspace.
- v0.4.5 preserves folder-by-folder scan runs in a sortable `scan_runs` SQLite table.
- Findings are category-colored and separated visually.
- Catalog rows display processing lights for name/version, duplicate audit, images, and career readiness.
- Edited and renamed history is shown in the Catalog.
- Duplicate Review adds recoverable `Delete Selected Duplicate (Quarantine)`.
- A denied/locked Windows `desktop.ini` no longer cancels duplicate cleanup.
- Career Data is a guided, color-coded readiness editor.
- The Career Wizard separates native BeamNG fields from RedFox planning fields and includes help popups.
- Career patches are separate ZIPs; source mods are not silently rewritten.
- Explicit traffic choices can generate valid `*.vehGroup.json` files using model/config.
- Dealership intent remains planning/filter data because current BeamNG facilities use filters rather than a universal per-vehicle shop id.
- v0.4.5 passed source, packaged-copy, GUI, career-patch, quarantine, and Undo tests.
- Physical Windows DPI, Explorer icon refresh, large-library behavior, and in-game patch testing remain David tests.

## Exact hashes

```text
v0.4.5 source
35d24dda45ae14ed7169f6ebe7862c11403d3f45c6326736cfd0d96eb684fa2b

v0.4.5 final package
0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939
```

## Controlling rename law

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD A MISSING VERSION OR UPDATE AN EXISTING VERSION TOKEN.
DO NOT REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
IF NO VERSION IS FOUND, DO NOT INVENT ONE.
```

## Duplicate evidence and cleanup law

- Exact ZIP hash = exact duplicate.
- Complete internal path/hash match = repacked duplicate.
- Same functional files with only docs/metadata/previews different = functional duplicate.
- Generic folder names and similar titles alone are not identity proof.
- Matching previews are supporting evidence, not sole proof.
- Newest/best/user-selected keeper remains active.
- Confirmed redundant and older copies may move.
- Same-version gameplay variants remain review-only.
- Delete Selected Duplicate uses recoverable quarantine, not permanent erasure.
- All moves use manifests, hashes, and Undo.
- Explorer icon customization failure cannot block a file operation.

## Results workspace

Tabs:

- Findings
- Duplicate Review
- Catalog / Rename
- Career Data
- DRM Details
- Previous Scans

`Maximize Results Area` hides upper scan controls and expands the tabs. `Restore Full Window` returns them.

Previous scans can be sorted by:

- newest / oldest;
- folder;
- red findings;
- duplicate count;
- career-ready count.

## Career readiness law

```text
GREEN  Ready: spawn requirements and important career fields present.
YELLOW May work: spawn-ready but important information missing.
RED    Not ready: model/config/.pc requirement missing.
BLUE   Manually reviewed and complete.
```

Native fields include Value, Years, Population, drivetrain, fuel, propulsion, transmission, performance/config type, body/derby/induction/country, power, torque, weight, top speed, and paints.

RedFox planning fields include traffic intent/group name, dealership/filter intent/facility id, library category, and notes.

## Verification

```text
PASS  exact v0.4.4 baseline compile
PASS  exact v0.4.4 full self-test
PASS  v0.4.5 compile
PASS  inherited scanner/duplicate/image/version self-test
PASS  v0.4.5 extended self-test
PASS  scan-history persistence
PASS  career override and export
PASS  career patch and vehicle-group generation
PASS  duplicate quarantine and hash-verified Undo
PASS  desktop.ini failure fallback
PASS  GUI construction and maximize/restore
PASS  final ZIP reopen/CRC
PASS  packaged compile and both self-tests
PASS  packaged GUI/career/quarantine integration
```

## What David should test

1. Extract v0.4.5 into a completely new folder.
2. Confirm the title says `v0.4.5`.
3. Run a completed copied-folder scan.
4. Test Maximize Results Area and Restore Full Window.
5. Confirm Findings and table rows are visually separated.
6. Confirm Previous Scans lists folder-by-folder runs and sorting works.
7. Inspect Catalog status lights and edited/renamed marks.
8. Use Duplicate Delete on one redundant copy and test Undo.
9. Open the Career Wizard for one known vehicle, save a plan, and build a patch ZIP.
10. Test the patch in BeamNG only after reviewing its generated info and plan files.

## Next version boundary

```text
v0.5.0 — Incoming-folder automatic sorter
- vehicles by make/model/category
- standalone maps vs official-map add-ons
- UI apps
- AI/traffic
- career/gameplay
- version checks
- older versions and duplicate review
- images and processing lights

v0.6.0 — installed/storage Mod Manager and video mod packs
```

## Current handoff

```text
Project: BeamNG Mod QuickScan / Catalog Manager
Version: v0.4.5 Results + History + Career Wizard
Baseline: exact packaged v0.4.4 source
Source hash: 35d24dda45ae14ed7169f6ebe7862c11403d3f45c6326736cfd0d96eb684fa2b
Package hash: 0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939
Packaged ZIP reopened: PASS
Packaged compile/self-tests: PASS
Packaged GUI/career/quarantine integration: PASS
Windows real-library runtime: REQUIRED
Release commit: 71e8eb0fefe4227a52aed8f21673129036a30807
Verification commit: 3fc5b7eef4059729eed3ef54e030f975cb240784
Career notes commit: b3884f6487534486a05587d3f0d9e4a94355dd90
Next safe step: David tests v0.4.5; then v0.5.0 sorter starts from the exact verified source
```