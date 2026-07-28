# BeamNG Mod QuickScan v0.4.2 — Source Baseline and Verification

**Baseline:** exact v0.4.1 source  
**Patch:** version-only rename, readable controls, full-screen catalog, and reliable image export  
**Runtime label:** `STATIC/SELF-TEST VERIFIED — EXACT INTEGRA REGRESSION PASS — WINDOWS LARGE-LIBRARY RUNTIME NOT YET PROVEN`

## Exact hashes

```text
v0.4.1 source SHA-256
29548be3cbea233f65439103bd4a25ac0b1dc8bb138fff2fd45ef2cd4ac1adc0

v0.4.2 source SHA-256
5a490166433dd98912796ad9a0036c81892a891e73c83bf06c680fb44715bf05

v0.4.2 package SHA-256
2ec328f5acec134d141b66223d17da3507127b423dd0d007ec056e5e9de555e6

Uploaded Integra ZIP SHA-256
a9cdade74adb53a7c60cad58c1865aeb1e3e5e5513dfd6cb42a6cbdf374a9b29
```

## Package file inventory

```text
BASELINE_v0_4_1.json
BeamNG Mod QuickScan.pyw
CAREER_EXPORT_FORMAT.md
DRM_DETECTION_NOTES.md
PATCH_CHANGE_REPORT.md
README.txt
RUN SELF TEST.bat
SIDE_BY_SIDE_COLORED_DIFF.html
START BeamNG Mod QuickScan.bat
TEST_REPORT.txt
VERIFICATION.json
```

## Proven by automated tests

- exact `.zip` discovery and one-ZIP-at-a-time scan foundation preserved;
- complete original filename remains the naming base;
- only version tokens are added or updated;
- no detected version leaves the filename unchanged;
- manual version saved by exact ZIP hash;
- changed manual version invalidates stale cache;
- image export beside ZIP and to QuickScan catalog;
- vehicle preview, map preview, and UI app icon roles;
- preview manifests include source/evidence/role/output paths;
- missing cached preview files rebuild;
- explicit dropdown/read-only-field contrast styles;
- Automatic, Light text, and Dark text modes;
- normal Catalog scrollbars and maximized full-screen Catalog;
- package reopen/CRC, extracted compile, extracted self-test, and extracted GUI smoke.

## Exact Integra proof

The uploaded archive contains a vehicle `info.json` but no declared mod version. No trustworthy version string was found in the filename, metadata, readme, manifest, or source text.

Without a manual version:

```text
BEAM_EVO_Mods_Acura_Integra.zip
BEAM_EVO_Mods_Acura_Integra.png
```

With a saved manual version of `1.2`:

```text
BEAM_EVO_Mods_Acura_Integra_v1.2.zip
BEAM_EVO_Mods_Acura_Integra_v1.2.png
```

The uploaded archive yielded one useful catalog image: `vehicles/AcuraIntegra/default.png`. Engine instruction preview images were filtered out.

## Current custody

The complete v0.4.2 source is inside the verified downloadable package:

```text
BeamNG_Mod_QuickScan_v0_4_2_Version_Contrast_Images.zip
```

Any future chat or Codex session must verify the source SHA-256 above before editing. Do not recreate the source from roadmap text or an older release.

## Not proven

- physical Windows DPI behavior at 100%, 125%, 150%, and 200%;
- every Windows theme/native dropdown edge case;
- large real-library runtime on David's hardware;
- the real version number of the uploaded Integra mod, because it is not declared in the archive.