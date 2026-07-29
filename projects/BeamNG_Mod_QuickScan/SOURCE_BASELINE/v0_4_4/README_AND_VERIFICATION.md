# BeamNG Mod QuickScan v0.4.4 — Source and Verification

**Version:** 0.4.4  
**Source file:** `BeamNG Mod QuickScan.pyw` inside the delivered package  
**Source SHA-256:** `2e1fd616e8dec86fc12bf96a656d8fd1e28a1aa23401f6930d28212f76944698`  
**Package SHA-256:** `b00112834f2870a127a2eceb4f84ace7a2844f704e17e0c4bab38b6dc3db2636`

## Baseline custody

The exact v0.4.3 packaged source was used.

```text
v0.4.3 source SHA-256
25317a5553fb7f0730e38a1b0380b38c483954dfac084180aa40d41f6d7e8578
```

No rewrite or older reconstruction was substituted.

## Source changes

- duplicate connected-component grouping;
- keeper recommendation and manual override;
- duplicate/older-version actions;
- red-dot review folder generation;
- `_DUPLICATE` ZIP and image suffixing;
- per-operation manifests;
- undo support;
- side-by-side path and line diff HTML;
- duplicate review UI tab;
- exclusion of the review folder from discovery/audit;
- duplicate preview-image hash deduplication.

## Package contents

- `BeamNG Mod QuickScan.pyw`
- `START BeamNG Mod QuickScan.bat`
- `RUN SELF TEST.bat`
- `README.txt`
- `DUPLICATE_ORGANIZER_GUIDE.md`
- `CAREER_EXPORT_FORMAT.md`
- `DRM_DETECTION_NOTES.md`
- `PATCH_CHANGE_REPORT.md`
- `SIDE_BY_SIDE_COLORED_DIFF.html`
- `TEST_REPORT.txt`
- `VERIFICATION.json`

## Verification gates

```text
PASS baseline source hash recorded
PASS source compile
PASS built-in self-test
PASS synthetic duplicate organizer test
PASS real uploaded Roamer pair
PASS real uploaded Transporter pair
PASS move operations and SHA-256 verification
PASS unique image transfers
PASS undo restoration
PASS duplicate review folder excluded from scanning
PASS red-dot icon and desktop.ini created
PASS side-by-side comparison HTML
PASS changed text/code line diff generation
PASS package reopen and ZIP CRC
PASS extracted packaged source compile
PASS extracted packaged self-test
PASS extracted packaged GUI smoke
PASS extracted packaged real-pair scan/move/undo
```

## Real pair keeper results

```text
KEEP  ta_transporter_0.5 tg_m0dsbeamng.zip
MOVE  car_ta_transporter_v0.5_DUPLICATE.zip

KEEP  roamerpack_00.zip
MOVE  roamersadfaw_DUPLICATE.zip
```

The move was then undone successfully and all original ZIPs were restored.

## Unproven

- physical Windows Explorer icon refresh behavior;
- very large collection cleanup on David's computer;
- Windows permission edge cases;
- physical DPI interaction.

## Safe continuation rule

Later work must start from the source inside the exact v0.4.4 package and verify the source hash before editing. Preserve the duplicate movement law, version-only naming law, readable custom controls, image exports, career exports, and DRM reporting unless David explicitly changes them.
