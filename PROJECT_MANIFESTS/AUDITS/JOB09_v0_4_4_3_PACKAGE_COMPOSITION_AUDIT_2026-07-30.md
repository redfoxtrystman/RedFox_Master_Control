# JOB-09 v0.4.4.3 Package Composition and Cross-Job Collision Audit

Date: 2026-07-30

Audited artifact:
`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_3_ExactYardGarageLinkPerformanceRepair.zip`

SHA-256:
`61f870dbe354cda5ad6ff15b3f1a6a81c2376250108b4a7bc82d17c23fc9201e`

## Exact package totals

- ZIP entries: 164
- ZIP size: 1,762,242 bytes
- Uncompressed size: 4,690,822 bytes
- Exact duplicate-content groups: 0

## Runtime versus non-runtime content

- Historical reports, diffs, inventories and documentation: 141 files / 3,286,133 bytes
- External catalog manager: 2 files / 15,788 bytes
- JOB-09 Lua/module/input runtime: 5 files / 503,520 bytes
- Unique RedFox Tow Portal runtime and images: 16 files / 885,381 bytes

Approximately 86% of the file count and 70% of the uncompressed bytes are development/audit material rather than playable runtime content.

## Dangerous shared/core files checked

The audited JOB-09 ZIP does not contain:

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfoxCareerWeb.lua
ui/modModules/redfoxCareerWeb/**
ui/ui-vue/dist/**
lua/ge/extensions/ui/phone/**
```

It also does not contain copies of the JOB-13 auction website, JOB-04 Wrecking Yard website, BeamBook, FoxFax, Parts Exchange, Export Yard, insurance sites, Random Events runtime/source, or stock Career/RLS files.

## Unique runtime paths present

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/core/input/actions/redfox_tow_recovery_dispatch.json
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
scripts/redfox_tow_recovery_dispatch/modScript.lua
mod_info/redfox_tow_recovery_dispatch/info.json
ui/modules/apps/redfoxTowPortal/**
```

These are JOB-09-specific filenames and IDs.

## Confirmed packaging problems

The playable ZIP carries historical reports, diffs, old verification files, file inventories, development notes and the external HTML catalog manager. These are safe but should remain in GitHub/source storage instead of being mounted by BeamNG.

The in-progress v0.4.4.4 work folder also contains:

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua.v0443.baseline
```

This is a development backup and must not ship.

## Functional overlap versus file collision

JOB-09 currently has internal auction and scrap fallback functions inside its unique Lua and Tow Portal files. This is functional overlap with JOB-13 and JOB-04, but not a path collision. Long-term, JOB-09 should own custody/lien/shop inventory and export requests; JOB-13 should own the auction engine/site; JOB-04 should own wrecking/scrap/parts processing.

## Required packaging change

Future JOB-09 builds must use an explicit runtime allowlist rather than zipping the entire work folder. Development reports and external tools should be delivered separately.

## Verdict

```text
Dangerous shared/core override: NOT FOUND
Unrelated websites bundled: NOT FOUND
Exact duplicate-content files: NOT FOUND
Development/report bloat: CONFIRMED
External tool incorrectly bundled with game mod: CONFIRMED
In-progress baseline source backup at packaging risk: CONFIRMED
Exact three-way compatibility with current JOB-04/JOB-13 binaries: NOT YET PROVEN
```
