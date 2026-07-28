# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.1 Original Filename + Preview Recovery  
**Latest release record:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_1_ORIGINAL_NAME_PREVIEW_FIX.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_1/README_AND_VERIFICATION.md`  
**Career contract:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/CAREER_EXPORT_FORMAT.md`  
**DRM rules:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/DRM_DETECTION_NOTES.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_0_CATALOG_CAREER_DRM.md`
5. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_1_ORIGINAL_NAME_PREVIEW_FIX.md`
6. This file.

## Current truth

- v0.4.0 ran on David's Windows computer and exposed a real catalog naming failure.
- It replaced a useful full source/site name with a short internal vehicle title and did not reliably rebuild missing preview files.
- v0.4.1 was built from the exact v0.4.0 package/source.
- v0.4.1 preserves the complete original filename and only adds or updates the detected version token.
- When v0.4.0 already shortened a ZIP, v0.4.1 checks saved `rename_actions` history and can recover the pre-rename filename.
- Preview images use the same full proposed ZIP stem.
- Missing cached preview files trigger automatic ZIP reprocessing and extraction.
- A rare low-load negative-sleep timing crash found during final package verification was fixed.
- v0.4.1 passed compile, built-in self-test, extended regression tests, GUI smoke tests, package reopen, packaged compile, packaged self-test, and packaged GUI smoke test.
- The exact Integra archive was not uploaded, so David's Windows retest remains required.

## Hashes

```text
v0.4.0 source
5df54228831e38bce32439935006d75883a71389bcfc767d73d5090daab358b4

v0.4.1 source
29548be3cbea233f65439103bd4a25ac0b1dc8bb138fff2fd45ef2cd4ac1adc0

v0.4.1 package
638528e88572bac8a5bb29caf97a81dc5084d8ce8bff837f85c547487ded3446
```

## Controlling naming law

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ADD OR UPDATE ONLY THE DETECTED VERSION.
DO NOT REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
IF NO VERSION IS FOUND, DO NOT RENAME.
```

Example:

```text
BEAM_EVO_Mods_Acura_Integra.zip
→
BEAM_EVO_Mods_Acura_Integra_v2.4.zip
```

Not allowed:

```text
BEAM_EVO_Mods_Acura_Integra.zip
→
Integra.zip
```

## Preview law

- extract up to three unique useful images;
- use the full proposed ZIP stem for every image;
- save a readable `preview_manifest.json`;
- rebuild images when cached paths are missing;
- never modify the image inside the source ZIP.

## First David test

Use the same copied test folder with:

```text
Checkpoint every: 2
Extract catalog previews: enabled
Automatic bulk rename: do not use
```

Confirm:

1. Proposed name retains the complete current/original stem.
2. Only the version is added or updated.
3. A filename with no detected version remains unchanged.
4. Preview images appear in the preview folder and match the proposed ZIP stem.
5. A previously shortened v0.4.0 name is recovered when rename history exists.
6. Apply only one selected rename after reviewing it.
7. Backup and Undo Last Rename still work.

## Current handoff

```text
Project: BeamNG Mod QuickScan / Catalog Manager
Version: v0.4.1 Original Filename + Preview Recovery
Baseline inspected: exact v0.4.0 package/source
Before-edit checks: source hash recorded; v0.4.0 package extracted
After-edit checks: compile, built-in self-test, extended naming/preview/history test, GUI smoke PASS
Packaged ZIP reopened: PASS
Packaged source compile: PASS
Packaged self-test: PASS
Packaged GUI smoke: PASS
Windows runtime by David: REQUIRED
Known limitation: exact Integra archive was not uploaded
Release commit: 6d0d2d615869bc0ed8e2c2c1cd78738223212ec5
Verification commit: 292d0416d287f609e61cfa37e15d70ce45144600
Next safe step: David retests v0.4.1 on the copied Integra folder
```
