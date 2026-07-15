# JOB-05 — BeamBook external research settings and monitor build

**Date:** 2026-07-15  
**Timestamp:** 2026-07-15 08:47 PDT (America/Los_Angeles)  
**Job:** JOB-05 — BeamBook Marketplace  
**Status:** BUILT — RUNTIME UNTESTED  
**Purpose:** Temporary external research package to test configurable BeamBook vehicle generation and observe actual in-game listing results before transferring proven behavior into the RedFox BeamBook implementation.

## What changed

Two isolated test packages were created from the user-supplied third-party BeamBook reference:

1. A modified BeamBook research build with a key-opened native WEUI settings window.
2. A separate read-only BeamBook research monitor that observes generated listings and exports diagnostic snapshots.

A combined outer test bundle, user guide, source diff, and build manifest were also created for delivery in the replacement regular chat.

## Why it changed

The original BeamBook module exposes only `listingCount` through `beamBook/config.json`. Vehicle selection is primarily weighted by each eligible configuration's `Population`, mileage is selected from a single broad range, and there is no in-game settings window or diagnostic monitor.

This research build tests whether BeamNG/RLS will honor:

- broader vehicle-category selection;
- inclusion of eligible zero-population configurations;
- configurable category and configuration-type weighting;
- condition/quality bands with separate mileage ranges;
- adjustable price, year, negotiation, listing-count, and expiration settings;
- live regeneration after settings changes;
- read-only observation of what was actually generated.

The work is research toward JOB-05's RedFox BeamBook implementation. It does not replace or supersede the preserved standalone RedFox BeamBook v0.1.0 candidate.

## Artifacts created in the regular-chat workspace

### Modified BeamBook research build

```text
beamBook_RedFoxResearch_v1_1_0_RUNTIME_UNTESTED.zip
```

- SHA-256: `c31934535460812bd38a9e1e0ae99058458f16d76c17334282989d1f4ed4705e`
- Files: 8
- ZIP integrity: PASS
- Lua parse: PASS
- JSON parse: PASS
- Runtime: UNTESTED

Primary changed/added paths:

```text
lua/ge/extensions/career/modules/beamBook.lua
lua/ge/extensions/beamBookLoader.lua
lua/ge/extensions/redfox/beamBookResearchSettings.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookResearchSettings.json
scripts/beamBook/modScript.lua
mod.json
README_REDFOX_RESEARCH.txt
CHANGE_SCOPE_JOB-05_BEAMBOOK_RESEARCH.txt
```

### Read-only research monitor

```text
RedFox_BeamBook_Research_Monitor_v0_1_0_RUNTIME_UNTESTED.zip
```

- SHA-256: `1a14a614dec692171cdb3383afaf2ccc912d1008f531c3e8d5dc9ad321adbb8b`
- Files: 6
- ZIP integrity: PASS
- Lua parse: PASS
- JSON parse: PASS
- Runtime: UNTESTED

Primary paths:

```text
lua/ge/extensions/redfox/beamBookResearchMonitor.lua
lua/ge/extensions/redfoxBeamBookResearchMonitorLoader.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookResearchMonitor.json
scripts/redfoxBeamBookResearchMonitor/modScript.lua
mod.json
README_REDFOX_BEAMBOOK_MONITOR.txt
```

### Combined delivery bundle

```text
RedFox_BeamBook_Research_Test_Bundle_v0_1_0_RUNTIME_UNTESTED.zip
```

- SHA-256: `f04fe03a0b4c66850ff0d63a6b8b3428e5430bbe0e229e0c043cccf9c869fa19`
- ZIP integrity: PASS
- Contains both inner ZIPs, installation/test guide, source diff, and build manifest.

## Modified BeamBook controls

Bindable action:

```text
BeamBook Research: Open Settings
```

The WEUI settings window provides:

- listing count;
- balanced category mode;
- guaranteed category coverage where eligible entries exist;
- inclusion of eligible zero-population configurations;
- minimum selection population weight;
- duplicate cap per configuration;
- minimum and maximum model years;
- maximum mileage;
- listing lifetime;
- category weights for cars, pickups, SUVs, vans, buses, heavy vehicles, trailers, special vehicles, and other entries;
- factory, custom, and unknown configuration-type weights;
- excellent, good, average, worn, and rough condition weights and mileage bands;
- negotiation enable/disable and seller price-multiplier range;
- minimum and maximum asking prices;
- save, save-and-regenerate, reload, and restore-default actions.

Settings remain stored in:

```text
beamBook/config.json
```

Generated listings are tagged with research metadata including category, condition, configuration type, and original population value.

## Monitor behavior

Bindable action:

```text
RedFox: Open BeamBook Research Monitor
```

The monitor is read-only. It does not patch shopping, money, ownership, spawning, inspection, garage, storage, or Career/RLS functions.

It reports:

- BeamBook listing count and unique configurations;
- category and quality distributions;
- minimum/average/maximum mileage;
- minimum/average/maximum price;
- zero-population configurations selected;
- missing parking failures;
- modified-generator diagnostics when available.

It can export:

```text
beamBookResearch/latest_snapshot.json
beamBookResearch/listings_YYYYMMDD_HHMMSS.csv
```

## Important limitations

- Runtime behavior is unproven until David tests the exact packages in BeamNG/RLS.
- The modified generator still begins with `util_configListGenerator.getEligibleVehicles()`. It cannot select a vehicle configuration that BeamNG/RLS excludes from that eligible list.
- Category detection is metadata/keyword based and must be validated against David's installed vehicle mods.
- Condition bands currently control assigned mileage and valuation. Physical wear depends on Mileage Wear/RLS or another system interpreting that mileage.
- Native WEUI visibility and key-action discovery are unproven.
- The original BeamBook architecture still performs global shopping/inspection patching. This derivative is for controlled research only and is not the final RedFox architecture.
- The original third-party BeamBook ZIP must be disabled while testing this derivative to avoid duplicate loaders and competing patches.

## Distribution and repository decision

The modified BeamBook package is derived from a user-supplied third-party mod whose public redistribution permission is not confirmed. Therefore, neither derivative ZIP nor copied third-party source was committed to this public repository.

The binaries were delivered only through the current regular chat. This GitHub record preserves hashes, scope, validation state, and test requirements without publicly redistributing the third-party work.

The separate monitor was built specifically for this research task, but it is being kept with the same controlled test delivery until runtime behavior is known.

## Files affected in GitHub

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-05_BEAMBOOK_EXTERNAL_RESEARCH_SETTINGS_MONITOR_BUILD_2026-07-15.md
```

No shared IceFox, phone, PC, registry, bridge, Career/RLS core, App Store, money, ownership, inventory, garage, storage, insurance, or another job's implementation files were changed.

## Work-chat migration note

The original RedFox/FoxNet job chats were unintentionally created as ChatGPT Work chats. David / Captain was not aware that the entire coordinated project was subject to a separate Work-chat usage limit. On July 14, 2026, those chats became inaccessible until July 20, 2026.

Development was interrupted across multiple jobs. Each job has had to be transferred manually into a regular chat, with files, testing history, context, and ownership reconstructed or reuploaded. This creates duplicate-work risk, loss-of-context risk, coordination problems, and unnecessary delay. The incident remains documented for inclusion in a report to OpenAI.

## Required next steps

1. Disable the original third-party `beamBook.zip`.
2. Install both inner research ZIPs from the combined bundle.
3. Start an active Career/RLS session.
4. Bind both settings and monitor actions.
5. Open the settings window, select a mixed preset/configuration, save and regenerate.
6. Open BeamBook and inspect the generated vehicle mix.
7. Open the monitor and export JSON/CSV evidence.
8. Test inspection and one normal purchase on West Coast USA and at least one non-West-Coast map.
9. Return `beamng.log` lines containing `beamBook` or `BEAMBOOK-MONITOR`, exported monitor files, screenshots, exact map, and first failing checkpoint.
10. Do not transfer this logic into the canonical RedFox BeamBook until the runtime results identify which settings and metadata classifications actually work.
