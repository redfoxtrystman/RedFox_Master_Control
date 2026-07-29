# BeamNG Mod QuickScan v0.4.5 — Source Baseline and Verification

**Baseline source:** exact `BeamNG Mod QuickScan.pyw` from packaged v0.4.4  
**New source SHA-256:** `35d24dda45ae14ed7169f6ebe7862c11403d3f45c6326736cfd0d96eb684fa2b`  
**Final package SHA-256:** `0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939`

## Source custody

The final downloadable package contains the complete UTF-8 source file:

```text
BeamNG_Mod_QuickScan_v0_4_5_Results_Career_History/
└── BeamNG Mod QuickScan.pyw
```

The package also contains:

- `PATCH_CHANGE_REPORT.md`;
- `SIDE_BY_SIDE_COLORED_DIFF.html` comparing v0.4.4 to v0.4.5;
- `OFFICIAL_CAREER_FIELD_NOTES.md`;
- `PREVIOUS_SCANS_AND_STATUS_LIGHTS.md`;
- `CAREER_EXPORT_FORMAT.md`;
- `DUPLICATE_ORGANIZER_GUIDE.md`;
- `VERIFICATION.json`;
- `TEST_REPORT.txt`.

Do not recreate v0.4.5 from prose. Obtain the exact package/source and verify the recorded source hash before editing.

## Baseline checks before editing

```text
PASS  Python compile
PASS  complete v0.4.4 built-in self-test
```

## v0.4.5 source checks

```text
PASS  Python compile
PASS  inherited v0.4.4 scanner/duplicate/image/version self-test
PASS  v0.4.5 extended self-test
PASS  GUI construction under Xvfb
PASS  Maximize Results Area / Restore Full Window
PASS  custom readable previous-scan and sort controls
PASS  persistent scan_runs history
PASS  career override save/load and machine-readable export
PASS  career patch ZIP creation
PASS  native model/config vehicle-group generation
PASS  duplicate delete-to-quarantine
PASS  hash-verified duplicate undo
PASS  desktop.ini error fallback without aborting cleanup
```

## Final package checks

```text
PASS  final ZIP reopen and CRC
PASS  extracted packaged source compile
PASS  packaged inherited self-test
PASS  packaged v0.4.5 extended self-test
PASS  packaged GUI smoke
PASS  packaged maximize/restore
PASS  packaged career patch integration
PASS  packaged duplicate quarantine and undo integration
```

## Required behavior boundaries

### Rename

```text
KEEP THE COMPLETE ORIGINAL ZIP NAME.
ONLY ADD OR UPDATE THE VERSION TOKEN.
DO NOT REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
DO NOT INVENT A VERSION.
```

### Duplicate cleanup

- Keeper stays active.
- Confirmed redundant/older copies may move to duplicate review.
- Delete Selected Duplicate is recoverable quarantine, not permanent deletion.
- Same-version functional variants remain review-only.
- Icon customization failure must not cancel the file operation.

### Career

- Required-to-spawn: model, config, and QuickScan-confirmed `.pc` path.
- Missing economy/performance information remains unknown until approved by the user.
- Career patches are separate ZIPs; the source mod is not silently rewritten.
- Traffic groups use native model/config records.
- Dealership intent remains planning/filter data; do not invent a native per-vehicle dealership field.

## Windows/runtime status

`WINDOWS REAL-LIBRARY TEST REQUIRED`

Static and packaged-copy tests are proven. Physical DPI, Explorer icon refresh, large-library resource behavior, and in-game testing of generated patches are not yet proven.