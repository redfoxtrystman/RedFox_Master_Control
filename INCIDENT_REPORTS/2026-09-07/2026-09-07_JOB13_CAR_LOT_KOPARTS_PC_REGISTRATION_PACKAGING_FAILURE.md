# INCIDENT REPORT — JOB13 Car Lot + KoParts PC registration/package regression

**Date:** 2026-09-07  
**Owner:** David / Captain  
**Scope:** RedFox Used Car Lot + JOB13 KoParts  
**Severity:** HIGH  
**Status:** FAILED — STOPPED  

## Executive summary

David reported that after installing the newly supplied full Car Lot and KoParts builds, **both entries disappeared from the Career PC**. This was a preventable process and packaging failure.

The owner had already supplied working code where the PC entries were loading. The requested work was limited to trade/manager/entitlement repairs in Car Lot and stuck-purchase recovery in KoParts. The working PC registration/loading path therefore should have been treated as protected and byte-preserved unless a route-specific change was explicitly required.

Instead, the assistant created and handed new full ZIPs without performing the required archive-root verification against BeamNG's expected mod layout. The resulting ZIPs preserved wrapper/master directories from the source archives rather than presenting the mod runtime paths at the correct archive root. This can prevent BeamNG from discovering `scripts/`, `lua/`, `ui/`, and `mod_info/` as a mod at all, which directly explains why the PC entries disappeared.

This incident also violated the mandatory GitHub/version order of operations because the builds were handed to David before the required source snapshot, release manifest, GitHub issue update, and runtime-result gate were durably recorded.

## Affected builds — QUARANTINED / DO NOT USE

### Car Lot
`RedFox_Used_Car_Lot_v0_1_9_63C_TRADE_REALISM_MANAGER_ENTITLEMENT_REPAIR--------V_0.39.4.zip`

SHA-256:
`2cbba4f70db3323da8f5c7bb96ee40905fca7d7feba406b1a6c28c412457aee4`

Observed by David:
- Car Lot entry disappeared from Career PC.

### KoParts
`RedFox_JOB13_KoParts_v0_1_9_62B_STUCK_PURCHASE_RECOVERY_OVERRIDE--------V_0.39.4.zip`

SHA-256:
`89992cc922d60ce45fc6ff799661ea82906fb536e02668ee58fac24a8035790f`

Observed by David:
- KoParts entry disappeared from Career PC.

## Confirmed technical failure — archive root/layout

Post-failure inspection of the exact delivered ZIPs found that runtime files were not packaged at the archive root.

### Car Lot delivered ZIP example
Instead of beginning with runtime paths such as:

```text
lua/ge/extensions/...
scripts/...
ui/...
mod_info/...
```

the archive begins under:

```text
RedFox_Used_Car_Lot_v0_1_9_63_OFFER_PERSISTENCE_HOTFIX--------V_0.39.4/
```

and then the runtime tree appears below that wrapper directory.

### KoParts delivered ZIP example
The KoParts source archive contained multiple wrapper/master folders. The delivered ZIP preserved those folders instead of normalizing the selected JOB13 mod tree to the archive root. The archive begins with paths such as:

```text
--MASTER MOD--RedFox_Used_Car_Lot/...
```

rather than one authoritative JOB13 runtime root.

This was not a BeamNG runtime-logic mystery. The packaging itself was invalid for the installation method David was told to use.

## Why this should have been caught by the triple-check/order-of-operations process

The repository's mandatory process file requires, before delivery:

1. read canonical status and latest runtime result;
2. identify exact current source/artifact hash;
3. preserve full source;
4. build from committed source;
5. verify ZIP integrity, duplicate entries, file inventory, protected paths, expected module/version strings, size and SHA-256;
6. create and commit the release manifest;
7. update the job issue before handing the ZIP to David;
8. only then provide the artifact;
9. record David's runtime result before starting another version.

The assistant performed syntax/CRC checks, but did **not** perform the decisive BeamNG archive-root check:

```text
At ZIP root, does the exact runtime mod tree expose the same working scripts/lua/ui/mod_info paths as the owner-tested baseline?
```

That missing check allowed a ZIP to be internally valid yet unusable as a BeamNG mod.

## Protected working code violation

David correctly pointed out that the PC path was already working and was not part of the requested behavior change.

The required preservation rule should have been:

```text
If PC registration/loading is owner-tested working and the requested repair is unrelated,
then PC registration files, loader order, route registration, archive root, and startup structure
must remain byte-identical or have an explicitly justified and reviewed diff.
```

The assistant failed to enforce that protection gate.

## Process violations

- FAILED ORDER OF OPERATIONS
- FAILED TRIPLE-CHECK / PACKAGE-ROOT VERIFICATION
- FAILED PROTECTED-WORKING-CODE PRESERVATION
- ARTIFACT HANDED TO OWNER BEFORE REQUIRED GITHUB RELEASE CHECKPOINT
- FAILED BUILD NOT MARKED FAILED BEFORE subsequent work
- OWNER FORCED TO RECOMPILE/ROLL BACK TO WORKING CODE

## Owner impact

David lost both Car Lot and KoParts PC entries and had to restore/compile the prior working versions himself. This created another avoidable full BeamNG test/reload cycle and reduced confidence that unrelated working systems would remain protected while requested business logic was changed.

## Immediate corrective controls

### Control 1 — archive-root gate
Before any BeamNG mod ZIP is handed to David:

- inspect the first-level ZIP paths;
- require exactly the intended mod runtime root;
- reject wrapper folders such as build-name/master-name directories unless the documented installation method explicitly requires unpacking that wrapper;
- prove `scripts/`, `lua/`, `ui/`, `mod_info/` and other expected runtime directories are reachable at the same root depth as the owner-tested baseline.

### Control 2 — protected PC/startup hash gate
For Car Lot and KoParts, before behavior edits:

- hash all PC registration, loader, route, startup and manifest files from the owner-tested baseline;
- if the requested work does not require those files, they must remain byte-identical;
- any changed protected file requires an explicit reason and before/after diff before packaging.

### Control 3 — three-way verification
Every candidate must be checked against:

1. **owner-tested working baseline** — protected behavior/files;
2. **edited source tree** — only authorized changes;
3. **final packaged ZIP** — same edited files, correct root, no wrapper/duplicate paths.

A build fails the gate if any of the three disagree unexpectedly.

### Control 4 — no user handoff before GitHub checkpoint
No future Car Lot or KoParts artifact is to be handed to David until:

- exact source snapshot exists in GitHub;
- release manifest is committed;
- job issue is updated with hash/status/test/rollback;
- package root and protected-path checks are documented.

### Control 5 — current working owner's builds become baseline
David stated he has already recompiled/restored the old working versions. Those exact owner-current files must be treated as the next baseline. Do not rebuild from the failed 63C/62B artifacts.

## Required next action

Do **not** create another mod yet.

First:

1. obtain/inspect David's exact current working Car Lot and KoParts files;
2. hash and inventory the PC/startup/route files;
3. compare them against the failed delivered packages;
4. document exactly which files and package-depth differences caused the PC disappearance;
5. reserve a new unused version only after the failed versions are durably marked `FAILED — STOPPED`;
6. cherry-pick only requested business-logic changes onto the owner-tested working source while preserving the PC/startup path;
7. run the three-way verification before packaging.

## Related repository controls

- `PROJECT_MANIFESTS/PROCESS/REQUIRED_VERSION_GITHUB_ORDER_OF_OPERATIONS_2026-07-27.md`
- Issue #40 — JOB13 KoParts
- Issue #72 — RedFox Used Car Lot
- Issue #23 — version-control/order-of-operations audit
- Issue #68 — prior failed order-of-operations/boundary incident

## Acceptance condition

This incident remains open until a future Car Lot/KoParts candidate:

- preserves the owner-tested PC entry and startup path;
- passes archive-root and protected-file triple-checks;
- is documented in GitHub before delivery;
- and is runtime-tested by David without losing either PC entry.
