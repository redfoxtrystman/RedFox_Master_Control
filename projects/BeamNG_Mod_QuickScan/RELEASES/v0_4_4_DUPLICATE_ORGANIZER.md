# BeamNG Mod QuickScan v0.4.4 — Duplicate Organizer

**Date:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Baseline:** exact packaged v0.4.3 source  
**Status:** `STATIC/SELF-TEST VERIFIED — REAL ROAMER/TRANSPORTER MOVE+UNDO PASS — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Owner request implemented

- Create a duplicate review folder inside the selected scan folder.
- Create one separate review folder per duplicate group.
- Give those folders a red-dot Windows Explorer icon using `RedDot.ico` and `desktop.ini`.
- Keep the recommended newest/best copy active.
- Move confirmed duplicates and lower versions into the group folder.
- Add `_DUPLICATE` immediately before `.zip` on moved ZIPs.
- Apply the same `_DUPLICATE` suffix rule to matching images.
- Explain which file is newer, better, and recommended to keep.
- Export a side-by-side colored comparison.
- Highlight exact changed lines for readable text/code files.
- Keep gameplay variants review-only rather than moving them automatically.
- Write an undo manifest and restore moved files safely.

## Duplicate movement law

```text
KEEP ACTIVE:
- recommended newest version;
- or best-supported equal-version copy.

MOVE:
- exact duplicates;
- repacked duplicates;
- functional duplicates where gameplay files are identical;
- lower versions with strong identity evidence.

DO NOT AUTO-MOVE:
- same-version variants with changed functional/gameplay files.
```

## Output location

```text
<selected scan folder>/_QuickScan_Duplicate_Review/
```

Each group folder contains:

- moved duplicate ZIPs;
- matching moved/copied preview images;
- `KEEPER_RECOMMENDATION.txt`;
- `DUPLICATE_GROUP_MANIFEST.json`;
- `SIDE_BY_SIDE_COMPARISON.html`;
- `RedDot.ico`;
- `desktop.ini`.

The duplicate review root is excluded from future scans.

## Side-by-side reports

```text
RedFoxTools/BeamNG Mod QuickScan/duplicate_review/SIDE_BY_SIDE_DUPLICATE_REVIEW.html
RedFoxTools/BeamNG Mod QuickScan/reports/duplicate_side_by_side.html
```

Color meanings:

- green: recommended keeper or path only in keeper-side archive;
- red: duplicate or path only in duplicate-side archive;
- amber: same path with changed contents;
- exact line additions/deletions/changes for readable text and code;
- binary/large files show size and SHA-256 evidence.

## Keeper recommendation

QuickScan first prefers the highest detected version. For equal or unknown versions it compares:

- functional-file completeness;
- metadata quality;
- extracted useful previews;
- filename/source clarity;
- archive completeness.

The user can select another copy and press **Use Selected as Keeper** before moving.

## Real uploaded regression results

### Roamer pair

```text
roamerpack_00.zip: KEEP
roamersadfaw.zip: MOVE_DUPLICATE
Result: exact renamed duplicate
Undo: PASS
```

### Transporter pair

```text
ta_transporter_0.5 tg_m0dsbeamng.zip: KEEP
car_ta_transporter_v0.5.zip: MOVE_DUPLICATE
Result: same functional mod/version; documentation-only extras
Undo: PASS
```

Matching preview images were transferred with `_DUPLICATE` names and were deduplicated by image SHA-256.

## Hashes

```text
v0.4.3 baseline source
25317a5553fb7f0730e38a1b0380b38c483954dfac084180aa40d41f6d7e8578

v0.4.4 source
2e1fd616e8dec86fc12bf96a656d8fd1e28a1aa23401f6930d28212f76944698

v0.4.4 final package
b00112834f2870a127a2eceb4f84ace7a2844f704e17e0c4bab38b6dc3db2636
```

## Verification

```text
PASS Python compile
PASS built-in self-test
PASS exact uploaded Roamer pair scan/group/move/undo
PASS exact uploaded Transporter pair scan/group/move/undo
PASS keeper recommendation
PASS manual keeper override support
PASS _DUPLICATE ZIP naming
PASS _DUPLICATE image naming
PASS image-hash deduplication
PASS red-dot icon marker creation
PASS review-folder scan exclusion
PASS side-by-side HTML
PASS text/code line highlighting
PASS packaged ZIP reopen/CRC
PASS packaged source compile
PASS packaged self-test
PASS packaged GUI smoke
PASS packaged real-pair regression
```

## Not proven

- physical Explorer icon-cache refresh on David's Windows computer;
- thousands-of-mods cleanup on David's hardware;
- every unusual file-permission situation;
- physical Windows DPI behavior.
