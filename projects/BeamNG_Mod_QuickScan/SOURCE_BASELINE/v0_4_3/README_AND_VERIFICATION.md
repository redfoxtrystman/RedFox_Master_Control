# BeamNG Mod QuickScan v0.4.3 Source Baseline and Verification

**Version:** 0.4.3  
**Patch:** Readable Controls + Duplicate Sensitivity + Image Export  
**Runtime label:** `STATIC/SELF-TEST VERIFIED — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Exact hashes

```text
Source SHA-256
25317a5553fb7f0730e38a1b0380b38c483954dfac084180aa40d41f6d7e8578

Package SHA-256
f2abfefb47c59eaf0024171048633b3dc83ff7b4f7f22b4a6994f78f7db037f5
```

## Packaged files

- `BeamNG Mod QuickScan.pyw`
- `START BeamNG Mod QuickScan.bat`
- `RUN SELF TEST.bat`
- `README.txt`
- `PATCH_CHANGE_REPORT.md`
- `SIDE_BY_SIDE_COLORED_DIFF.html`
- `TEST_REPORT.txt`
- `VERIFICATION.json`
- `CAREER_EXPORT_FORMAT.md`
- `DRM_DETECTION_NOTES.md`
- `CARAVAN_TEST_SOURCE_HASH.txt`

## Verification

```text
PASS Python compile
PASS built-in self-test
PASS final ZIP reopen/CRC
PASS packaged source compile
PASS packaged self-test
PASS packaged GUI smoke
PASS custom dropdown contrast
PASS full-screen Catalog
PASS automatic beside-ZIP image export
PASS Roamer exact duplicate regression
PASS Transporter functional duplicate regression
PASS zero-shared-functional false-positive regression
```

## Current limitations

- David must still test physical Windows DPI and real mouse behavior.
- Thousands-of-mods performance remains a Windows runtime test.
- Custom DRM can evade static indicators.
- Missing version data is never invented; the user can use Set / Correct Version.

## Custody rule

Do not rebuild from an older QuickScan package. Verify the source SHA-256 above before editing and preserve the colored diff, test report, and package verification with every later release.
