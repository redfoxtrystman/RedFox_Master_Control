# JOB-04 v0.3.2.3 — Website-Preserving Cleanup Audit

**Date:** 2026-07-31 PT  
**Owner:** David / Captain  
**Workstream owner:** Sol  
**Scope:** FoxNet/IceFox Welcome Hub + JOB-04 Wrecking Yard  
**Packaging:** One installable ZIP

## Runtime-passed source

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_2_STEP02_PURCHASE_REPAIR_FORCED_GARAGE_FROM_v0_3_2_1.zip
SHA-256: 55668d13385ad996ce0f1b160a9fbb8484e7757489f593ca3f08266a0de33481
Files: 1,026
```

Confirmed before this build: correct phone icon, Welcome Hub, styled/fast Wrecking Yard, native purchase, money, Career ownership, inventory and garage assignment all passed. The purchased tanker trailer briefly appeared in the world before native storage completed; no permanent duplicate was confirmed.

## Owner instruction

Keep every current website page and asset active. Remove only unrelated reports, verification records, development notes and redundant temporary backup copies. Continue using one combined Welcome Hub + Wrecking Yard ZIP. Other jobs will later coordinate their completed page files and routes with this package owner.

## Exact build result

### Installable ZIP

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-31_v0_3_2_3_STEP03_KEEP_ALL_WEBSITES_REMOVE_RECORDS_FROM_v0_3_2_2.zip
SHA-256: 8b238d50b3254b336c9665cd712082cae5e81cd16fab67e79dc6e8614f39ca48
Files: 829
ZIP bytes: 16,949,392
```

### Records-only archive

```text
RedFox_JOB-04_v0_3_2_3_REMOVED_RECORDS_ONLY_2026-07-31.zip
SHA-256: 3bc383a3bdf1ed3b01dd0064f727539d0533c097e6e2a183ca6d76e2fc9b8124
Files: 200
ZIP bytes: 8,673,603
```

The records archive is nested entirely under `RECORDS_ONLY_DO_NOT_INSTALL/` and must not be installed as a BeamNG mod.

## Website restoration

This build restored 658 website files byte-for-byte from the Step 01 temporary backup to their original active paths:

```text
sites/**
ui/modModules/redfoxCareerWeb/sites/**
```

All ten website directories are active in both trees:

- `beambook`
- `collector_exchange`
- `export_yard`
- `foxfax`
- `foxnet_auctions`
- `parts_exchange`
- `redfox_recovery`
- `scrap_yard`
- `undergroundnet`
- `xxx_insurance`

Every file under `sites/**` has a byte-identical mirror under `ui/modModules/redfoxCareerWeb/sites/**`.

## Removed from the installable ZIP

Only non-runtime records and documentation were removed:

- 190 non-website files from the temporary backup area;
- historical verification reports and JSON results;
- old change-scope and file-tree ledgers;
- old `OPEN_ME_FIRST` and development readmes;
- old documentation under the browser module;
- five Step 02 original-file backups after the purchase repair passed runtime;
- seven documentation-only text files with no page or route references.

All removed files are preserved byte-for-byte in the records-only archive.

## Protected runtime files

The phone icon, Welcome Hub, phone pages, browser shell, both Wrecking Yard mirrors, purchase adapter, bridge, Lua, Vue bundle, phone layout, inventory, pricing, mileage and negotiation files remain byte-identical to v0.3.2.2. The only active content changed was `info.json`, updated to identify v0.3.2.3.

## Verification

```text
Checks: 1,638 / 1,638 PASS
ZIP integrity: PASS
Fresh extraction file-set parity: PASS
Fresh extraction byte parity: PASS
Duplicate internal paths: 0
Unsafe/traversal paths: 0
Temporary backup paths in installable ZIP: 0
Restored website files: 658 / 658 exact
Website directories: 10 / 10 in both trees
Website mirror parity: PASS
Active JSON files parsed: 61 / 61
Active JavaScript syntax: 37 / 37 PASS
HTML/CSS local references checked: 4,568
Missing mod-owned local references: 0
Route targets active: PASS
Lua structural bracket check: PASS
Protected runtime hashes: PASS
Records preservation: PASS
```

Absolute `/ui/...` references inside `ui/ui-vue/dist/index.css` were recognized as BeamNG base-game resources rather than missing mod-owned files.

## Runtime test gate

Disable v0.3.2.2 and every other JOB-04/Browser Core test ZIP. Install only v0.3.2.3.

Test Career load, correct icon, unchanged Welcome Hub, every website card/page, styled/fast Wrecking Yard, inventory/prices, one inexpensive native purchase, garage storage and performance.

No feature backend from JOB-09, JOB-13, BeamBook or another job was edited. Their current bundled pages remain available until those job owners provide completed files and integration requirements.
