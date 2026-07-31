# JOB-04 v0.3.5 Three-Mod Compatibility and Package Split Audit

**Date:** 2026-07-30 19:02 PT  
**JOB-04 ledger:** issue #30  
**JOB-09 coordination:** issue #4  
**JOB-13 coordination:** issue #40

## Exact inputs

- JOB-04 v0.3.4 SHA-256: `e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75`
- JOB-09 v0.4.4.3 SHA-256: `61f870dbe354cda5ad6ff15b3f1a6a81c2376250108b4a7bc82d17c23fc9201e`
- JOB-13 v0.1.2 SHA-256: `1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071`

## Important correction

The exact uploaded JOB-04, JOB-09 and JOB-13 archives have **zero identical internal active file paths in common**. The current Career-load failure is therefore not proven to be a direct same-path overwrite between these exact builds. The earlier collision assumption was too broad and is corrected here.

Confirmed JOB-04 packaging problems remain:

- JOB-04 bundled the shared Browser/Core inside a feature ZIP.
- JOB-04 bundled obsolete Auction and Recovery/Tow website copies under its browser-site namespace.
- JOB-04 bundled many unrelated websites, root mirrors, old versions, reports, MHTML captures and development records.
- JOB-04 independently shipped the shared `ui/ui-vue/dist/index.js`, `index.css`, phone layout and browser bridge.
- Shared/core paths need one authoritative owner even though the exact current JOB-09 and JOB-13 standalone builds use different paths.

## Architecture decision

Use one shared **RedFox FoxNet Browser Core** for the phone/PC browser shell, shared UI bundle, phone layout, tile and common bridge. Keep JOB-04, JOB-09 and JOB-13 as isolated feature modules. After compatibility is proven, they may remain modular or be assembled into one final release from the ownership manifest.

## Built outputs

### Browser Core v0.1.0 compatibility test

`RedFox_FoxNet_Browser_Core_v0_1_0_COMPAT_TEST_FROM_JOB04_v0_3_4.zip`

- SHA-256: `d731f364328b1f17761117793331be85c0f6e1f7577bfcdff1eb609f57fa8fc3`
- 51 files
- 1,240,469 ZIP bytes
- 5,902,462 uncompressed bytes
- Contains shared browser/core files only; no feature website directory.
- Missing feature routes render a local not-installed page instead of trying to load removed site files.

### JOB-04 v0.3.5 slim feature module

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1902PT_v0_3_5_SLIM_MODULE_REQUIRES_BROWSER_CORE_FROM_v0_3_4.zip`

- SHA-256: `358f663e2fd2ce35f8b720c1d07f5db57393135247efc6fd6cb40215e1238bd5`
- 34 files
- 75,748 ZIP bytes
- 281,128 uncompressed bytes
- Preserves approved junk inventory, native purchase adapter, sell/scrap/strip/parts/cat logic.
- Contains no Auction, Tow/Recovery, Parts, Insurance, Export, Collector, Underground or BeamBook website.
- Contains no shared main UI bundle or phone layout.

### Records-only archive

`RedFox_JOB-04_v0_3_4_REMOVED_EXTRAS_RECORDS_ONLY_2026-07-30.zip`

- SHA-256: `57225e44a0bb1006e6e13081257e59841c19341df7c367f09a513f5aa70759f1`
- 974 files
- 24,406,994 ZIP bytes
- All files nested under `RECORDS_ONLY_DO_NOT_INSTALL/`.
- Must not be installed as a BeamNG mod.

## Reduction

- Active file count: 1,047 → 85 (91.9% reduction)
- Active compressed size: 25,581,535 → 1,316,217 bytes (94.9% reduction)
- Active uncompressed size: 48,403,159 → 6,183,590 bytes (87.2% reduction)

## Active path ownership after split

Ignoring each archive's required root `info.json` metadata:

- Browser Core ↔ JOB-04 slim: 0 overlaps
- Browser Core ↔ JOB-09: 0 overlaps
- Browser Core ↔ JOB-13: 0 overlaps
- JOB-04 slim ↔ JOB-09: 0 overlaps
- JOB-04 slim ↔ JOB-13: 0 overlaps
- JOB-09 ↔ JOB-13: 0 overlaps

## Static verification

- ZIP integrity: PASS for all four active test packages
- Duplicate internal paths: 0
- Unsafe traversal paths: 0
- JavaScript syntax: 11 files checked, 0 failures
- JSON parse: 28 files checked, 0 failures
- Lua lexical/bracket structure: 14 files checked, 0 failures
- Merged Browser Core + JOB-04 HTML references: 0 missing
- JOB-09 unchanged at exact input hash
- JOB-13 unchanged at exact input hash

Lua checking is structural, not a complete BeamNG runtime/compiler test.

## Runtime gate

Install Browser Core v0.1.0 + JOB-04 v0.3.5, keep exact unchanged JOB-09 v0.4.4.3 and JOB-13 v0.1.2, and fully restart BeamNG. Test Career load before opening apps. If the all-four combination fails, test Core+JOB04, then add JOB09, then JOB13 separately and capture the first failing game log. No further broad package change is authorized without that runtime evidence.
