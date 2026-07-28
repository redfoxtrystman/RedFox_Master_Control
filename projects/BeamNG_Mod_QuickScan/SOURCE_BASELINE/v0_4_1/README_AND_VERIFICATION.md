# BeamNG Mod QuickScan v0.4.1 Source Baseline and Verification

**Version:** 0.4.1  
**Patch:** Original Filename + Preview Recovery  
**Baseline:** exact v0.4.0 source extracted from `BeamNG_Mod_QuickScan_v0_4_0_Catalog_Career_DRM.zip`  
**Runtime label:** `STATIC/SELF-TEST VERIFIED — DAVID WINDOWS TEST REQUIRED`

## Exact hashes

```text
v0.4.0 source SHA-256
5df54228831e38bce32439935006d75883a71389bcfc767d73d5090daab358b4

v0.4.1 source SHA-256
29548be3cbea233f65439103bd4a25ac0b1dc8bb138fff2fd45ef2cd4ac1adc0

v0.4.1 package SHA-256
638528e88572bac8a5bb29caf97a81dc5084d8ce8bff837f85c547487ded3446
```

## Custody and change proof

The downloadable package contains:

```text
BASELINE_v0_4_0.json
BeamNG Mod QuickScan.pyw
PATCH_CHANGE_REPORT.md
SIDE_BY_SIDE_COLORED_DIFF.html
TEST_REPORT.txt
VERIFICATION.json
README.txt
START BeamNG Mod QuickScan.bat
RUN SELF TEST.bat
CAREER_EXPORT_FORMAT.md
DRM_DETECTION_NOTES.md
```

## Required behavior preserved

- one ZIP active at a time;
- adjustable checkpoints and unattended continuation;
- Pause / Resume Saved Scan / Cancel;
- metadata recovery;
- DRM indicator reporting;
- career JSON/JSONL/CSV export;
- purple/seafoam themes and Knight Rider sweep;
- backup-first reversible rename;
- source ZIP contents unchanged during preview extraction.

## v0.4.1 regression coverage

- long source/site filename remains intact;
- only a detected version is added or updated;
- no detected version causes no rename;
- old v0.4.0 shortened filenames can be recovered from saved rename history;
- three preview images receive the full proposed ZIP stem;
- missing cached preview files trigger an automatic rebuild;
- rare negative low-load sleep duration is guarded.

## Current source custody

The complete v0.4.1 source is inside:

```text
BeamNG_Mod_QuickScan_v0_4_1_Original_Name_Preview_Fix.zip
```

Future chats must verify the source and package hashes above before editing. Do not rebuild this patch from memory or from v0.4.0 when the v0.4.1 package is available.
