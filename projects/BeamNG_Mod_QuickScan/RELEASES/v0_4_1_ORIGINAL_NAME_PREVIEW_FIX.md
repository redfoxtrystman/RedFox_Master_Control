# BeamNG Mod QuickScan v0.4.1 — Original Filename + Preview Recovery Fix

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Baseline:** exact v0.4.0 package/source  
**Status:** `STATIC/SELF-TEST VERIFIED — DAVID WINDOWS TEST REQUIRED`

## User-reported failure

v0.4.0 replaced a useful source/site filename with a short internal vehicle title. Example failure:

```text
BEAM_EVO_Mods_Acura_Integra.zip
→
Integra.zip
```

It also failed to reliably recreate extracted previews when cached preview records existed but the actual files were missing.

## v0.4.1 naming law

- Preserve the complete original ZIP filename stem.
- Do not replace it with Brand, Name, vehicle folder, or another short internal title.
- When an internal version is found and no explicit `v` version exists, append only `_v<version>`.
- When an explicit `v` version already exists, update only that version token.
- When no version is detected, keep the original filename unchanged.
- When v0.4.0 already shortened a ZIP, consult `rename_actions` history and recover the saved pre-rename filename.

Expected example:

```text
BEAM_EVO_Mods_Acura_Integra.zip
→
BEAM_EVO_Mods_Acura_Integra_v2.4.zip
```

## Preview fix

- Extract up to three unique preview images.
- Name previews from the full proposed ZIP stem.
- Save them in a readable per-mod preview folder.
- Write `preview_manifest.json` beside the images.
- Automatically rescan a cached ZIP when a recorded preview file is missing.
- Automatically refresh old v0.4.0 catalog records under naming policy version 2.

Expected preview names:

```text
BEAM_EVO_Mods_Acura_Integra_v2.4.png
BEAM_EVO_Mods_Acura_Integra_v2.4_02.png
BEAM_EVO_Mods_Acura_Integra_v2.4_03.png
```

## Additional bug caught by final packaging gate

A rare low-load timing path could call `time.sleep()` with a tiny negative duration. v0.4.1 recalculates the remaining delay and exits the loop when it reaches zero.

## Hashes

```text
v0.4.0 source
5df54228831e38bce32439935006d75883a71389bcfc767d73d5090daab358b4

v0.4.1 source
29548be3cbea233f65439103bd4a25ac0b1dc8bb138fff2fd45ef2cd4ac1adc0

v0.4.1 package
638528e88572bac8a5bb29caf97a81dc5084d8ce8bff837f85c547487ded3446
```

## Verification

```text
PASS  exact v0.4.0 baseline inspected
PASS  Python compilation
PASS  built-in self-test
PASS  full original filename preserved
PASS  detected version appended without shortening
PASS  explicit version token updated in place
PASS  no-version filename preserved unchanged
PASS  three preview extraction
PASS  preview names match full proposed ZIP stem
PASS  deleted cached preview rebuilt automatically
PASS  simulated v0.4.0 short-name failure
PASS  pre-rename filename recovered from rename history
PASS  low-load negative sleep timing fix
PASS  extended regression test
PASS  GUI construction smoke test
PASS  final ZIP reopen/CRC
PASS  packaged source compilation
PASS  packaged self-test
PASS  packaged GUI smoke test
```

## Not proven

- the exact Integra ZIP was not uploaded;
- Windows DPI and mouse interaction;
- large real-library behavior on David's hardware.

The first Windows test must keep automatic bulk rename off and review the Catalog / Rename proposal before applying it.
