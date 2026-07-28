# BeamNG Mod QuickScan — Status and Chat Handoff

**Last updated:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Current version:** v0.4.3 Readable Controls + Duplicate Sensitivity + Image Export  
**Latest release record:** `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_3_READABLE_DUPLICATE_IMAGE_FIX.md`  
**Latest verification:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_3/README_AND_VERIFICATION.md`  
**Career contract:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/CAREER_EXPORT_FORMAT.md`  
**DRM rules:** `projects/BeamNG_Mod_QuickScan/SOURCE_BASELINE/v0_4_0/DRM_DETECTION_NOTES.md`

## Read before editing

1. `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
2. `INCIDENT_REPORTS/2026-07-26_BeamNG_Mod_QuickScan_Order_Of_Operations_Failure.md`
3. `projects/BeamNG_Mod_QuickScan/MASTER_PROJECT_RECORD_2026-07-26.md`
4. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_0_CATALOG_CAREER_DRM.md`
5. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_1_ORIGINAL_NAME_PREVIEW_FIX.md`
6. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_2_VERSION_CONTRAST_IMAGES.md`
7. `projects/BeamNG_Mod_QuickScan/RELEASES/v0_4_3_READABLE_DUPLICATE_IMAGE_FIX.md`
8. This file.

## Current truth

- v0.4.0 ran on David's Windows computer and exposed short-name, preview, and contrast failures.
- v0.4.1 restored the complete-original-name rule and missing-preview cache recovery.
- v0.4.2 documented version-only rename, full-screen Catalog, text modes, and image destinations.
- A duplicate-evidence test build then exposed two new failures:
  - Windows still rendered white text on white native dropdown fields;
  - duplicate detection became too sensitive and marked unrelated trailer ZIPs as versions despite zero shared functional files.
- v0.4.3 replaces native comboboxes with custom colored Menubutton dropdowns.
- v0.4.3 adds Automatic, Light text, and Dark text controls with guaranteed contrasting input backgrounds.
- v0.4.3 tightens duplicate identity rules and replaces stale duplicate findings after a completed scan.
- v0.4.3 makes the image destination selector control automatic scan-time sidecar export.
- v0.4.3 includes full-screen Catalog, version correction, selected image export, duplicate evidence reports, career export, and DRM indicators.
- v0.4.3 passed compile, self-test, real uploaded Roamer/Transporter regressions, false-positive regression, ZIP reopen/CRC, packaged compile, packaged self-test, and packaged GUI smoke.
- Physical Windows DPI and thousands-of-mods performance remain David tests.

## Hashes

```text
v0.4.3 source
25317a5553fb7f0730e38a1b0380b38c483954dfac084180aa40d41f6d7e8578

v0.4.3 package
f2abfefb47c59eaf0024171048633b3dc83ff7b4f7f22b4a6994f78f7db037f5
```

## Controlling rename law

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD A MISSING VERSION OR UPDATE AN EXISTING VERSION TOKEN.
DO NOT REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
IF NO VERSION IS FOUND, DO NOT INVENT ONE.
```

## Duplicate evidence law

- Exact same ZIP SHA-256: confirmed exact duplicate.
- Same complete internal path/hash set: confirmed repacked duplicate.
- Same functional files and identity/version, with only docs/metadata/previews different: functional duplicate.
- A shared generic vehicle folder alone is not identity evidence.
- A similar title alone is not enough without functional overlap or a unique explicit ID.
- Zero shared functional files cannot become a version-duplicate finding merely because both touch `tanker`, `flatbed`, `pickup`, `common`, `roamer`, or similar folders.
- Matching preview hashes are supporting evidence, not the sole proof.

Required real results:

```text
Roamer pair:
89 files, identical ZIP hash, exact renamed duplicate.

Transporter pair:
55 shared functional files, 0 changed functional files,
3 documentation-only extras, 21 matching preview hashes.
```

## Preview/image law

- vehicle: repository/info image, then vehicle default/config preview;
- map: preview/loading/overview/screenshot/cover/thumbnail in the level folder;
- UI app: icon/logo used by the in-game app;
- up to three useful unique images, normally one UI icon;
- random materials, texture channels, terrain/minimap tiles, engine instructions, and part images are filtered out;
- scan-time destination choices:
  - Beside ZIP + Catalog
  - Catalog folder only
  - Beside ZIP only
- every record stores role, source path, reason, hash, catalog path, and sidecar path;
- ZIP contents are never modified.

## What David should test

1. Extract v0.4.3 into a new folder.
2. Confirm the title says `v0.4.3`.
3. Set Text to `Automatic`.
4. Confirm Theme, Text, Checkpoint, Computer Load, and Images controls are readable.
5. Run a **completed** scan so old false duplicate records are replaced.
6. Confirm unrelated trailers with zero shared functional files are no longer paired.
7. Confirm the Roamer and Transporter pairs remain detected.
8. Set Images to `Beside ZIP + Catalog` and confirm images are written automatically.
9. Open Full-Screen List and test both scrollbars.
10. Use Set / Correct Version only when a real version is known.

## Current handoff

```text
Project: BeamNG Mod QuickScan / Catalog Manager
Version: v0.4.3 Readable Controls + Duplicate Sensitivity + Image Export
Baseline inspected: v0.4.2.1 sensitivity source and v0.4.2 documented feature boundary
Before-edit checks: source compile, existing self-test, reports.zip false-positive audit
After-edit checks: compile, self-test, real Roamer/Transporter regression, unrelated-trailer regression, custom dropdown GUI smoke, full-screen Catalog smoke, automatic sidecar image test PASS
Packaged ZIP reopened: PASS
Packaged source compile: PASS
Packaged self-test: PASS
Packaged GUI smoke: PASS
Windows runtime by David: REQUIRED
Known limitation: physical DPI and thousands-of-mods performance not yet proven
Release commit: 2106768e094502a4d82cfb6cc51283a96e185d94
Verification commit: 05bb44fd3e2bb200a360c4fd465a5b52ccb3f553
Next safe step: David runs one completed v0.4.3 scan and reports Windows UI/resource results
```
