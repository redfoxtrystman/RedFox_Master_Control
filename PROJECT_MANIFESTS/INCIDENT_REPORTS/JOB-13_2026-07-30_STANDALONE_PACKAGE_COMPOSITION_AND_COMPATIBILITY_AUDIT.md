# JOB-13 Standalone Package Composition and Compatibility Audit

**Date/time:** 2026-07-30 19:06 PT  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Artifact audited:** `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip`  
**SHA-256:** `1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071`  
**Runtime result prompting audit:** Three-mod test reported long phone-auction load/freeze behavior; JOB-04 independently found that its own v0.3.4 archive bundled shared/core UI files and complete copies of unrelated websites.

## Executive result

JOB-13 v0.1.2 is not oversized like the rejected JOB-04 v0.3.4 archive and does not contain the shared/core replacements identified in that archive.

Measured JOB-13 package:

- ZIP size: approximately 422 KB
- 41 files plus 14 directory entries
- Uncompressed file data: 503,822 bytes
- Duplicate ZIP paths: none
- Byte-identical duplicate-file groups: none
- 21 vehicle images, all referenced by the JOB-13 candidate pool

The archive does **not** contain:

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfoxCareerWeb.lua
ui/modModules/redfoxCareerWeb/**
ui/modModules/redfoxCareerWeb/sites/redfox_recovery/**
ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/**
BeamBook, FoxFax, Parts Exchange, Export Yard, insurance, or other websites
```

Therefore JOB-13 v0.1.2 is not independently replacing BeamNG/RLS's main UI bundle, phone layout, shared RedFox browser host, or another job's site.

## JOB-13-owned runtime paths

```text
ui/modules/apps/redfoxJob13Auctions_v012/**
lua/ge/extensions/redfoxJob13Auction.lua
lua/ge/extensions/redfoxJob13AuctionSettings.lua
scripts/redfox_job13_online_auctions/modScript.lua
mod_info/RedFoxJOB13/**
```

These paths are namespaced to JOB-13 and should remain.

## Problems found inside JOB-13

### 1. Constant state-file writes

`redfoxJob13Auction.onUpdate()` ticks every 0.5 seconds. `tickLots()` calls `saveState(false)` every tick, and `saveState(false)` writes the complete JSON state whenever two seconds have elapsed—even when no lot, bid, timer status, shipping state, or account data changed.

This is unnecessary continuous disk activity and violates the intended dirty-state persistence pattern. It is not expected to cause a two-to-three-minute catalog load by itself, but it can contribute to stutter, disk churn, and poor multi-mod behavior.

Required correction:

- Introduce a dirty-state flag.
- Mark dirty only when persistent data changes.
- Save only dirty data on a bounded interval or immediately for critical transactions.
- Do not save merely because a timer was checked.

### 2. WEUI settings extension loaded continuously

`modScript.lua` loads both the backend and the WEUI settings extension at startup. The settings extension registers `onUpdate()` for every frame, although `drawWindow()` exits immediately while closed.

This is a small overhead, not the reported multi-minute freeze. It should still be improved:

- Load only `redfoxJob13Auction` at startup.
- Lazy-load `redfoxJob13AuctionSettings` when the user opens Settings.
- Unload or leave dormant according to the shared WEUI pattern after closing.

### 3. Generic documentation paths inside the runtime ZIP

The runtime archive contains:

```text
FILE_MANIFEST_SHA256.csv
README_OPEN_FIRST.txt
docs/BUILD_AUDIT_2026-07-29.md
docs/TEST_PLAN.md
docs/WEUI_SETTINGS_REFERENCE.md
docs/v012_behavior_harness.lua
docs/V0_1_2_BIDDING_SCREEN_CORRECTION.md
docs/JOB13_INTEGRATION_MANIFEST.md
```

These total only about 11.7 KB and are not a meaningful load-time cause, but generic root and `docs/` virtual paths can collide with equivalent files in other mods. The Lua behavior harness also does not belong in a release/runtime ZIP.

Required correction:

- Remove audit, test, harness, and manifest files from the runtime package.
- Preserve them in GitHub and in a separate development/handoff archive.
- If an in-mod README is retained, namespace it under a JOB-13-specific path.

### 4. Full-state browser polling

The inner auction page requests complete web state every five seconds. The UI host may also supply state on page readiness and actions. With 12 test lots this payload is small, but it should not become the permanent architecture for hundreds of lots.

Required correction:

- Use a small catalog-summary payload for browsing.
- Load lot details and bid history only when a lot is opened.
- Push state after actions and meaningful backend changes.
- Use a slower safety refresh rather than frequent complete-state polling.

### 5. Semantic duplicate auction websites across packages

JOB-13's corrected auction screen is located at:

```text
ui/modules/apps/redfoxJob13Auctions_v012/site/**
```

JOB-04 v0.3.4 reportedly contains a different older auction site at:

```text
ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/**
```

These are not exact path duplicates, but they are two competing implementations of the same visible auction destination. The old shared-browser site is the one that displayed marketplace negotiation/Buy behavior and generated a much larger list. Which screen the phone opens depends on the shared host/route—not on JOB-13's isolated UI App.

Required coordination:

- JOB-04 must remove its copied auction site, as already planned for its slim rebuild.
- JOB-01/shared browser owner must register the JOB-13 route exactly once.
- JOB-13 must not independently replace `redfoxCareerWeb`, phone layout, or the core UI bundle.

## GitHub consistency finding

GitHub issue #40 correctly records JOB-13 as an online-only, isolated job and forbids direct replacement of JOB-01/JOB-02/JOB-04/JOB-09 authoritative files.

However, the actual JOB-13 source tree and binary are not committed to the repository. GitHub currently contains coordination/audit records and interface examples, not the exact v0.1.2 source package. This weakens reproducibility and makes exact cross-mod comparison harder.

Required correction for the next build:

- Commit the JOB-13-owned source tree or an exact source manifest on a JOB-13 branch.
- Record artifact name, SHA-256, changed paths, static checks, runtime result, and keep/reject decision for every version.
- Do not commit or absorb other jobs' shared/core files.

## Current verdict

```text
JOB-13 namespace isolation: PASS
Shared/core UI replacement check: PASS
Unrelated website bundling check: PASS
Duplicate ZIP path check: PASS
Continuous persistence behavior: FAIL — must fix
Runtime documentation packaging: CLEANUP REQUIRED
Phone route ownership: EXTERNAL DEPENDENCY — JOB-01/shared host
Three-mod compatibility: NOT YET PROVEN
v0.1.2 release status: TEST BUILD ONLY; DO NOT CALL RELEASE-READY
```

## Exact next step

Obtain the exact currently installed JOB-04 Wrecking Yard ZIP and JOB-09 Tow/Recovery ZIP. Perform a three-way internal-path and SHA-256 comparison against JOB-13 v0.1.2 before another combined runtime test.

The next JOB-13 build should be a slim performance-correction build containing only JOB-13 runtime files, dirty-state persistence, lazy WEUI loading, and reduced browser-state transfer. No shared phone/browser/core files may be added.
