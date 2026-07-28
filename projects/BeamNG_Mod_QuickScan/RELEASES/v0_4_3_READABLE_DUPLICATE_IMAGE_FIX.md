# BeamNG Mod QuickScan v0.4.3 — Readable Controls, Duplicate Sensitivity, and Image Export

**Date:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Status:** `STATIC/SELF-TEST VERIFIED — REAL DUPLICATE REGRESSION PASS — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Owner-reported failures fixed

- Windows showed white text on white dropdown fields.
- Duplicate detection became too sensitive and marked unrelated trailers as different versions despite zero shared functional files.
- Image destination controls did not automatically write beside-ZIP exports during the scan.
- The Catalog needed a full-screen list and scrollbars.
- Missing versions needed a manual correction action that preserves the complete original filename.

## Readable control law

Native ttk comboboxes were replaced with custom `tk.Menubutton` dropdowns so Windows cannot force its own white field. The app now controls both background and foreground colors.

Text modes:

```text
Automatic
Light text
Dark text
```

Light text is paired with a dark input background. Dark text is paired with a light input background. The folder path field uses the same contrast rule.

## Duplicate sensitivity law

QuickScan no longer treats a shared generic vehicle folder such as `tanker`, `flatbed`, `pickup`, `common`, or `roamer` as proof that two ZIPs are versions of one mod.

A matching declared title is not sufficient by itself. It must be backed by functional-path overlap or a unique explicit mod/repository identity.

Zero shared functional files means the pair cannot be classified as different versions merely because a generic vehicle folder overlaps.

A completed scan replaces old duplicate findings for the selected folder, clearing stale false positives.

## Required duplicate regressions

### Roamer pair

```text
roamerpack_00.zip
roamersadfaw.zip
```

Result:

```text
Exact renamed duplicate
89 internal files
identical complete ZIP SHA-256
```

### Transporter pair

```text
ta_transporter_0.5 tg_m0dsbeamng.zip
car_ta_transporter_v0.5.zip
```

Result:

```text
Same functional mod and version
55 shared functional files
0 changed functional files
3 documentation-only extras
21 matching preview-image hashes
```

## Images

The image destination selector now controls automatic scan-time export:

```text
Beside ZIP + Catalog
Catalog folder only
Beside ZIP only
```

Vehicle previews, map previews, and UI app icons keep their classified roles. `Export Selected Images` can also rebuild/copy a selected mod's existing preview records.

## Catalog and version controls

- Full-screen Catalog window.
- Horizontal and vertical scrolling.
- `Set / Correct Version` action.
- Complete original ZIP filename is preserved.
- Only the missing or incorrect version token is changed.

## Hashes

```text
Source SHA-256
25317a5553fb7f0730e38a1b0380b38c483954dfac084180aa40d41f6d7e8578

Final package SHA-256
f2abfefb47c59eaf0024171048633b3dc83ff7b4f7f22b4a6994f78f7db037f5
```

## Verification

```text
PASS  Python compile
PASS  built-in self-test
PASS  real uploaded Roamer duplicate regression
PASS  real uploaded Transporter duplicate regression
PASS  unrelated zero-shared-functional trailer pair not classified as versions
PASS  custom non-native dropdown construction
PASS  dropdown foreground/background contrast inspection
PASS  read-only path-field contrast inspection
PASS  full-screen Catalog construction
PASS  automatic beside-ZIP image export during scan
PASS  final ZIP reopen and CRC test
PASS  packaged source compile
PASS  packaged self-test
PASS  packaged GUI smoke test
```

## Required Windows test

1. Extract into a new folder.
2. Confirm title says v0.4.3.
3. Set Text to Automatic.
4. Confirm Theme, Text, Checkpoint, Computer Load, and Images menus are readable.
5. Run a completed scan to replace stale false duplicate results.
6. Confirm unrelated trailers with zero shared files are no longer paired.
7. Confirm the Roamer and Transporter pairs remain detected.
8. Set Images to `Beside ZIP + Catalog` and confirm sidecar images are created.
9. Open Full-Screen List and test both scrollbars.
