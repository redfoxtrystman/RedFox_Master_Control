# BeamNG Mod QuickScan v0.4.7.2 — Storage Hotfix

**Date:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Baseline:** exact v0.4.7.1 package/source  
**Status:** PACKAGED AND VERIFIED; WINDOWS REAL-LIBRARY TEST REQUIRED

## Owner-reported failure

Renaming 160 ZIPs produced approximately 1.6 GB under `RedFoxTools/BeamNG Mod QuickScan/backups/renames` because v0.4.7.1 copied the complete ZIP before every filename-only rename.

A filename-only rename does not modify ZIP contents. Copying every ZIP was unnecessary for normal operation and unacceptable for limited storage.

## Corrected rename law

- Default mode: `Manifest only (recommended)`.
- Store original path, new path, SHA-256, time, warning, database Undo record, and JSONL history.
- Do not create a second ZIP copy for a normal filename-only rename.
- Undo renames the current file back and verifies SHA-256.
- Optional `Full ZIP copy` remains available in Storage.
- Any operation that rewrites files inside a ZIP still requires a complete backup, change report, and explicit confirmation.

## Storage screen

The header now includes **Storage**. It measures:

- old filename-only ZIP backups;
- extracted preview cache;
- generated reports;
- database backups;
- copied catalog ZIPs/images.

Each area can be opened or cleaned separately after confirmation. The screen explains the consequence of each cleanup.

## Existing v0.4.7.1 backup cleanup

The old `backups/renames` copies can be removed after confirming the renamed ZIPs still exist at their current paths. Undo continues to work while the current renamed ZIP is present. Removing the backup removes only the emergency second-copy fallback.

## Hashes

```text
v0.4.7.2 source
4dd5224ee6fdc633e01b18095285fb560036bfa643e2ce9c5dd4086c99815c7f

v0.4.7.2 package
a6def9ddd2a4f39a6708cb614825d923298a309862edb1855ebf2ec866e425e2
```

## Verification

```text
PASS compile
PASS inherited v0.4.4-v0.4.7 tests
PASS v0.4.7.2 storage self-test
PASS packaged ZIP CRC/reopen
PASS packaged compile/self-test
PASS Storage GUI smoke
PASS real filename-only rename with no full backup
PASS hash-verified Undo after manifest-only rename
```

## Preserved features

Folder focus, metadata recovery, automatic images, solid progress colors, duplicate organizer, quarantine, Career wizard, Tow Catalog, Previous Scans, Master Catalog, DRM, pause/resume, reports, and version-only naming remain present.
