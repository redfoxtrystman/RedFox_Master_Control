# BeamNG Mod QuickScan v0.4.2 — Version-Only Rename, Contrast, Full-Screen Catalog, and Image Export

**Date:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Baseline:** exact v0.4.1 package/source  
**Status:** `STATIC/SELF-TEST VERIFIED — EXACT INTEGRA REGRESSION PASS — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Owner-reported failures corrected

David's Windows screenshots proved:

1. a mod without a detected version showed an unchanged proposed name without explaining why;
2. the main goal is version correction, not replacing the useful original filename;
3. Windows dropdown/read-only fields could show white text on a white field;
4. the Catalog list was squeezed into a short bottom strip;
5. image exports were not clear or reliable enough to use;
6. maps need map preview/loading images and UI apps normally need their in-game icon.

## Controlling rename law

```text
KEEP THE COMPLETE ORIGINAL ZIP FILENAME.
ONLY ADD A MISSING VERSION OR UPDATE AN EXISTING VERSION TOKEN.
NEVER REPLACE THE ORIGINAL NAME WITH A SHORT INTERNAL TITLE.
IF NO VERSION CAN BE FOUND, DO NOT INVENT ONE.
```

For the uploaded Integra archive, no version exists in the filename, `vehicles/AcuraIntegra/info.json`, readme, manifest, metadata, or source text. v0.4.2 therefore shows:

```text
Version: Not found — Set Version
Current:  BEAM_EVO_Mods_Acura_Integra.zip
Proposed: BEAM_EVO_Mods_Acura_Integra.zip
```

The new **Set / Correct Version** action stores a manual version against the exact ZIP SHA-256. Entering `1.2` produces:

```text
BEAM_EVO_Mods_Acura_Integra.zip
→
BEAM_EVO_Mods_Acura_Integra_v1.2.zip
```

Only the version is changed. Saved overrides invalidate stale cached naming and preview records.

## Contrast and text controls

- explicit themed backgrounds for dropdown and read-only fields;
- contrasting text and arrow colors;
- dropdown-list background/foreground styling;
- `Automatic`, `Light text`, and `Dark text` choices;
- forced text choices also select an opposite input background so fields remain readable;
- theme, load mode, checkpoint, path field, and image-destination controls use the corrected styles.

## Full-screen Catalog

The Catalog tab now contains **Open Full-Screen List**.

- opens a maximized catalog window;
- vertical and horizontal scrollbars;
- wider Current, Proposed, Version Action, and DRM columns;
- Escape or Close Full Screen exits;
- double-clicking a row returns to the matching row in the main Catalog tab.

The normal Catalog table also has horizontal and vertical scrollbars.

## Image export

New actions:

- **Export Selected Images**
- **Rebuild All Images**

Destination choices:

- `Beside ZIP + Catalog`
- `Catalog folder only`
- `Beside ZIP only`

Image roles:

- `vehicle_preview`
- `map_preview`
- `ui_app_icon`
- `mod_preview`
- `mod_icon`
- `fallback_preview`

Selection rules:

- vehicles prefer repository/info images and `vehicles/<model>/default.*`;
- maps prefer level preview, loading, overview, screenshot, cover, map, or thumbnail images;
- UI apps prefer the icon/logo under the in-game app folder;
- random textures, material channels, terrain/minimap tiles, engine instructions, and part images are filtered out;
- UI apps normally export one icon; other mods may export up to three useful unique images;
- `preview_manifest.json` records role, source path, selection reason, hash, catalog path, and sidecar path;
- ZIP contents are never modified.

## Exact uploaded Integra validation

Uploaded ZIP SHA-256:

```text
a9cdade74adb53a7c60cad58c1865aeb1e3e5e5513dfd6cb42a6cbdf374a9b29
```

Result before manual version:

```text
Detected version: none
Proposed ZIP: BEAM_EVO_Mods_Acura_Integra.zip
Useful images: 1
Image role: vehicle_preview
Sidecar export: BEAM_EVO_Mods_Acura_Integra.png
```

Result after manual version `1.2`:

```text
Proposed ZIP: BEAM_EVO_Mods_Acura_Integra_v1.2.zip
Sidecar export: BEAM_EVO_Mods_Acura_Integra_v1.2.png
```

## Hashes

```text
v0.4.1 source
29548be3cbea233f65439103bd4a25ac0b1dc8bb138fff2fd45ef2cd4ac1adc0

v0.4.2 source
5a490166433dd98912796ad9a0036c81892a891e73c83bf06c680fb44715bf05

v0.4.2 final package
2ec328f5acec134d141b66223d17da3507127b423dd0d007ec056e5e9de555e6
```

## Verification

```text
PASS  baseline compile
PASS  v0.4.2 compile
PASS  built-in self-test
PASS  complete-original-name preservation
PASS  version-only add/update naming
PASS  manual version override saved by ZIP hash
PASS  manual override invalidates stale cache
PASS  map preview detection
PASS  UI app icon detection
PASS  vehicle default preview selection
PASS  sidecar and catalog exports
PASS  contrast style smoke test
PASS  text mode smoke test
PASS  full-screen catalog smoke test
PASS  exact uploaded Integra scan
PASS  exact uploaded Integra no-version behavior
PASS  exact uploaded Integra manual-version behavior
PASS  package reopen/CRC
PASS  packaged compile
PASS  packaged self-test
PASS  packaged GUI smoke test
```

## Required Windows test

1. Confirm the title says `v0.4.2`.
2. Set Image export to `Beside ZIP + Catalog`.
3. Select the Integra row.
4. Press **Set / Correct Version** and enter the real version.
5. Confirm only the version was added.
6. Press **Export Selected Images**.
7. Confirm the image appears beside the ZIP and in QuickScan's preview catalog.
8. Open the full-screen Catalog.
9. Check dropdown readability using Automatic, Light text, and Dark text.
10. Apply only the selected version rename after confirming the proposal.