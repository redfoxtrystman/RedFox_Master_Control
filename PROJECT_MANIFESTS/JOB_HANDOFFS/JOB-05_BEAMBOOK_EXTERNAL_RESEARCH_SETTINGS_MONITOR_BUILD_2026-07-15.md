# JOB-05 — BeamBook external research settings and monitor build

**Original build date:** 2026-07-15  
**Audit correction date:** 2026-07-17  
**Job:** JOB-05 — BeamBook Marketplace  
**Status:** BUILT — RUNTIME UNTESTED  
**Purpose:** Temporary external research package to test configurable BeamBook vehicle generation and observe actual in-game listing results before transferring proven behavior into the canonical RedFox BeamBook implementation.

## Audit correction notice — 2026-07-17

The first version of this record listed several descriptive/internal filenames that did not exactly match the files inside the delivered ZIPs. The delivered binaries were not changed. This record now uses the exact archive paths verified directly from the delivered packages.

Corrections include:

- `READ_ME_FIRST_REDFOX_RESEARCH.txt` and `TEST_CHECKLIST_REDFOX_RESEARCH.txt` are the actual edited-package documentation filenames.
- `lua/ge/extensions/redfoxBeamBookMonitorLoader.lua` is the actual monitor loader path.
- `scripts/redfoxBeamBookMonitor/modScript.lua` is the actual monitor startup-script path.
- `READ_ME_FIRST.txt` is the actual monitor documentation filename.
- The current outer bundle is 29,977 bytes, not the stale 29,938-byte value written inside the original self-contained manifest.

## What was built

Two isolated test packages were created from the user-supplied third-party BeamBook reference:

1. A modified BeamBook research build with a key-opened native WEUI settings window.
2. A separate read-only BeamBook research monitor that observes generated listings and exports diagnostic snapshots.

A combined outer test bundle, user guide, source diff, and build manifest were also delivered through the regular JOB-05 chat.

## Why it was built

The original BeamBook module exposes only `listingCount` through `beamBook/config.json`. Vehicle selection is primarily weighted by each eligible configuration's `Population`, mileage is selected from one broad random range, and the original mod has no dedicated in-game settings window or diagnostic monitor.

The research build is intended to test whether BeamNG/RLS will honor:

- broader vehicle-category selection;
- inclusion of eligible zero-population configurations;
- configurable category and configuration-type weighting;
- condition/quality bands with separate mileage ranges;
- adjustable price, year, negotiation, listing-count, duplicate, and expiration settings;
- live listing regeneration after settings changes;
- read-only observation of the listings actually generated.

This research work does not replace or supersede the preserved standalone RedFox BeamBook v0.1.0 candidate.

## Artifact identity

### Modified BeamBook research build

```text
beamBook_RedFoxResearch_v1_1_0_RUNTIME_UNTESTED.zip
```

- Size: 12,776 bytes
- SHA-256: `c31934535460812bd38a9e1e0ae99058458f16d76c17334282989d1f4ed4705e`
- Files: 8
- ZIP integrity: PASS
- JSON validation: PASS
- Original build validation recorded Lua parse: PASS
- BeamNG/RLS runtime: UNTESTED

Exact archive contents:

```text
READ_ME_FIRST_REDFOX_RESEARCH.txt
TEST_CHECKLIST_REDFOX_RESEARCH.txt
lua/ge/extensions/beamBookLoader.lua
lua/ge/extensions/career/modules/beamBook.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookResearchSettings.json
lua/ge/extensions/redfox/beamBookResearchSettings.lua
mod.json
scripts/beamBook/modScript.lua
```

### Read-only research monitor

```text
RedFox_BeamBook_Research_Monitor_v0_1_0_RUNTIME_UNTESTED.zip
```

- Size: 5,713 bytes
- SHA-256: `1a14a614dec692171cdb3383afaf2ccc912d1008f531c3e8d5dc9ad321adbb8b`
- Files: 6
- ZIP integrity: PASS
- JSON validation: PASS
- Original build validation recorded Lua parse: PASS
- BeamNG/RLS runtime: UNTESTED

Exact archive contents:

```text
READ_ME_FIRST.txt
lua/ge/extensions/core/input/actions/redfoxBeamBookResearchMonitor.json
lua/ge/extensions/redfox/beamBookResearchMonitor.lua
lua/ge/extensions/redfoxBeamBookMonitorLoader.lua
mod.json
scripts/redfoxBeamBookMonitor/modScript.lua
```

### Combined delivery bundle

```text
RedFox_BeamBook_Research_Test_Bundle_v0_1_0_RUNTIME_UNTESTED.zip
```

- Current size: 29,977 bytes
- SHA-256: `f04fe03a0b4c66850ff0d63a6b8b3428e5430bbe0e229e0c043cccf9c869fa19`
- ZIP integrity: PASS
- Files: 5

Exact outer-bundle contents:

```text
beamBook_RedFoxResearch_v1_1_0_RUNTIME_UNTESTED.zip
RedFox_BeamBook_Research_Monitor_v0_1_0_RUNTIME_UNTESTED.zip
BEAMBOOK_RESEARCH_PACKAGE_GUIDE.txt
beamBook_original_vs_RedFoxResearch.diff
BEAMBOOK_RESEARCH_BUILD_MANIFEST.json
```

Supporting-file identities:

```text
BEAMBOOK_RESEARCH_PACKAGE_GUIDE.txt
Size: 3,988 bytes
SHA-256: 8501b1e6e023db04eedcbca27d39836129f3715a6f57f0f9402d48cb34731135

beamBook_original_vs_RedFoxResearch.diff
Size: 38,987 bytes
SHA-256: e5f31bbd5bb10546b550df21681994c4391f705fc8f19f8c58b6f1dda7f52448
```

The outer bundle's embedded manifest intentionally cannot contain its own final archive hash without changing that hash. Its recorded outer-bundle size is stale; the verified external size and hash above are authoritative.

## Modified BeamBook behavior

Main changed file:

```text
lua/ge/extensions/career/modules/beamBook.lua
```

Research additions include:

- persistent expanded configuration;
- balanced-category generation mode;
- optional guaranteed category coverage where eligible entries exist;
- optional inclusion of eligible zero-population configurations;
- minimum population-selection weight;
- duplicate cap per exact configuration;
- category weighting;
- factory/custom/unknown configuration-type weighting;
- excellent/good/average/worn/rough quality bands;
- separate mileage ranges per quality band;
- model-year limits;
- minimum and maximum asking price;
- negotiation enable/disable;
- seller price-multiplier range;
- listing-expiration controls;
- manual save and regeneration actions;
- research metadata attached to generated listings;
- diagnostic counts for eligible pools, generated categories, filtered entries, and parking failures.

Bindable action:

```text
BeamBook Research: Open Settings
```

Settings are stored in:

```text
beamBook/config.json
```

## Monitor behavior

Bindable action:

```text
RedFox: Open BeamBook Research Monitor
```

The monitor is intended to remain read-only. It does not intentionally patch or mutate:

- money;
- purchases;
- ownership;
- inventory;
- garage or storage;
- inspection;
- vehicle spawning;
- Career progression;
- BeamBook listing generation.

It reports:

- BeamBook listing count;
- unique configurations;
- category distribution;
- quality distribution;
- minimum/average/maximum mileage;
- minimum/average/maximum price;
- zero-population configurations selected;
- duplicate configurations;
- parking failures;
- modified-generator diagnostics when available.

Expected exports:

```text
beamBookResearch/latest_snapshot.json
beamBookResearch/listings_YYYYMMDD_HHMMSS.csv
```

## Important limitations

- Runtime behavior is unproven until David tests the exact packages in BeamNG/RLS.
- The modified generator still begins with `util_configListGenerator.getEligibleVehicles()` and cannot select configurations excluded from that eligible list.
- Category detection is metadata/keyword based and must be validated against David's installed vehicle mods.
- Quality bands directly control assigned mileage and valuation. Physical structural wear still depends on Mileage Wear, RLS, or another installed system interpreting mileage.
- Native WEUI visibility and key-action discovery are unproven.
- The third-party derivative still follows the original architecture's global shopping/inspection patch pattern. It is controlled research, not the final RedFox architecture.
- The original third-party `beamBook.zip` must be disabled during this research test to prevent duplicate loaders and competing patches.

## Distribution and repository decision

The modified BeamBook package contains transformed code from a user-supplied third-party mod whose public redistribution permission is not confirmed. Therefore, the derivative ZIP and copied source are not committed to this public repository.

The binaries remain private chat-delivered research artifacts. This repository stores hashes, scope, inventory, validation state, limitations, and test requirements only.

## Scope boundaries

No shared IceFox, phone, PC, browser, registry, bridge, Career/RLS core, App Store, money, ownership, inventory, garage, storage, insurance, or another job's implementation files were changed.

The monitor is a separate JOB-05 research sidecar, not a new project job and not a transfer of JOB-05 ownership.

## Required runtime test after David returns

1. Disable the original third-party `beamBook.zip`.
2. Extract the outer bundle outside BeamNG.
3. Install both inner ZIPs.
4. Start an active Career/RLS save.
5. Bind both research controls.
6. Open settings, choose a mixed configuration, save, and regenerate.
7. Open the normal shopping interface and BeamBook tile.
8. Verify the actual category and quality mix.
9. Open the monitor and export JSON/CSV evidence.
10. Test inspection and one normal purchase on West Coast USA.
11. Repeat essential discovery/listing/inspection checks on at least one non-West-Coast map.
12. Return log lines containing `beamBook` or `BEAMBOOK-MONITOR`, screenshots, exports, exact map, installed RLS/Career versions, enabled-mod list, and the first failing checkpoint.
13. Do not transfer this research logic into the canonical RedFox BeamBook until runtime evidence identifies which settings and metadata classifiers actually work.
