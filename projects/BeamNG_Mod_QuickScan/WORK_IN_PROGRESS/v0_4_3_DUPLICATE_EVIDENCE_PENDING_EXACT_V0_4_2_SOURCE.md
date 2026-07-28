# BeamNG Mod QuickScan v0.4.3 — Duplicate Evidence Patch Pending Exact v0.4.2 Source

**Date:** 2026-07-28 PDT  
**Owner:** David / Captain  
**Status:** `DUPLICATE ENGINE TESTED — DO NOT RELEASE FROM v0.4.1 BASELINE — EXACT v0.4.2 SOURCE REQUIRED`

## Why this record exists

David supplied two deliberate duplicate test pairs and requested that QuickScan report the same clear evidence used during manual comparison.

The duplicate engine was implemented and tested against the four uploaded ZIPs. During final source-control review, the active GitHub handoff showed that v0.4.2 already contains newer version-only rename, contrast, full-screen Catalog, text-mode, map/UI image, and sidecar-image export changes.

The active runtime contained only the exact v0.4.1 source. Releasing the duplicate patch built from v0.4.1 would roll back those v0.4.2 features. That package is therefore not approved for delivery.

## Required merge baseline

Upload or recover the exact package/source matching:

```text
v0.4.2 source SHA-256
5a490166433dd98912796ad9a0036c81892a891e73c83bf06c680fb44715bf05

v0.4.2 package SHA-256
2ec328f5acec134d141b66223d17da3507127b423dd0d007ec056e5e9de555e6
```

The duplicate changes must be layered onto that exact source and released as v0.4.3 or later.

## Actual uploaded Roamer regression

```text
Pair:
roamerpack_00.zip
roamersadfaw.zip

Classification:
Exact renamed duplicate

ZIP size:
10,610,859 bytes vs 10,610,859 bytes

ZIP SHA-256:
4bed6322eb3901ab6e635934d1f6120dcd17264f1d6d2acc9bd0135b6efe35ff

Internal files:
89 vs 89

Shared files:
89

Identical shared files:
89

Changed shared files:
0

Changed functional files:
0

Matching preview-image hashes:
17

Result:
CONFIRMED RED DUPLICATE
```

## Actual uploaded Transporter regression

```text
Pair:
ta_transporter_0.5 tg_m0dsbeamng.zip
car_ta_transporter_v0.5.zip

Classification:
Same functional mod and same version

Detected version:
0.5

Vehicle identity:
ta_vehicle_transporter

ZIP files:
84 vs 81

Shared files:
81

Identical shared files:
81

Changed shared files:
0

Functional files:
55 vs 55

Changed functional files:
0

Documentation-only extras:
3

Extra paths:
copyright notice and terms of use.txt
vehicles/copyright notice and terms of use.txt
vehicles/ta_vehicle_transporter/copyright notice and terms of use.txt

Matching preview-image hashes:
21

Result:
CONFIRMED RED FUNCTIONAL DUPLICATE
```

## Duplicate classifications implemented and tested

1. Exact renamed duplicate — complete ZIP SHA-256 matches.
2. Repacked duplicate — ZIP containers differ but complete internal path/hash set matches.
3. Functional duplicate — identity/version match and all functional files match; only docs, metadata, or previews differ.
4. Same-version variant — identity/version match but functional files differ.
5. Different active versions — identity matches and versions differ.

## Evidence shown to the user

Each duplicate result includes:

- both filenames and paths;
- classification;
- confidence;
- ZIP sizes;
- ZIP hashes;
- total internal files;
- shared files;
- identical shared files;
- changed shared files;
- functional file counts;
- changed functional files;
- documentation-only extras;
- matching preview-image count;
- internal identity evidence;
- recommended action.

## Image-assisted duplicate rule

Matching extracted/internal preview hashes are supporting evidence only. Images alone do not prove a duplicate because unrelated mods may reuse icons or placeholder art. When vehicle identity, version, and functional hashes also match, identical previews strengthen the conclusion and are displayed in the report.

## Full-library audit rule

The final safe scan stop must compare the entire active library, including cached mods and mods scanned in earlier checkpoints. Duplicate detection must not be limited to only the newest checkpoint.

## Required reports

```text
reports/duplicate_comparisons.json
reports/duplicate_comparisons.csv
reports/duplicate_comparisons.txt
```

## Permanent regression law

Every later QuickScan self-test must include:

- an exact renamed duplicate trap equivalent to the Roamer pair;
- a functional duplicate with documentation-only extras equivalent to the Transporter pair;
- a check that cached/earlier-checkpoint duplicates are included in the final full-library audit.

## Next safe step

1. Obtain the exact v0.4.2 package/source.
2. Verify its source SHA-256.
3. Apply only the duplicate-evidence changes.
4. Preserve all v0.4.2 version, contrast, full-screen, and image-export features.
5. Run the two uploaded-pair regressions again.
6. Package as v0.4.3.
7. Reopen, compile, self-test, and GUI-smoke-test the packaged copy.
