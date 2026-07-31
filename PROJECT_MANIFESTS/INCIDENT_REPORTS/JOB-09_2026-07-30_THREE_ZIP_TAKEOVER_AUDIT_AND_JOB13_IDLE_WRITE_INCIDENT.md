# JOB-09 Three-ZIP Takeover Audit and JOB-13 Idle-State Write Incident

**Date:** 2026-07-30  
**Owner:** David / Captain  
**Primary job:** JOB-09 — Tow / Recovery / Dispatch  
**Audit type:** Read-only exact-binary package, code and cross-job compatibility audit  
**Mod files edited:** NONE  
**ZIPs repackaged:** NONE

## Owner instructions preserved

- Inspect every supplied ZIP entry and source file rather than relying on filenames.
- Do not guess or silently change code.
- Report conflicts, ownership violations and unapproved changes before repair.
- Preserve exact artifacts and hashes.

## Exact audited inputs

### JOB-09

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_3_ExactYardGarageLinkPerformanceRepair.zip`

- SHA-256: `61f870dbe354cda5ad6ff15b3f1a6a81c2376250108b4a7bc82d17c23fc9201e`
- ZIP entries: 164
- Uncompressed bytes: 4,690,822

### JOB-04 upload supplied for compatibility comparison

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1430PT_v0_3_4_NATIVE_PURCHASE_FORCED_GARAGE_DELIVERY_FROM_v0_3_3.zip`

- SHA-256: `e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75`
- ZIP entries: 1,047
- Uncompressed bytes: 48,403,159

### JOB-13

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip`

- SHA-256: `1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071`
- ZIP entries: 41
- Uncompressed bytes: 503,822

## Exact audit coverage

All 1,252 ZIP entries were opened, read and hashed.

Checks completed:

- ZIP CRC/integrity
- duplicate internal paths
- unsafe traversal paths
- nested archives
- executable/native payloads
- SHA-256 per file
- cross-ZIP path comparison
- cross-ZIP byte-identical content comparison
- JSON parsing
- JavaScript syntax checking
- Lua compilation using `texlua --luaconly`
- HTML/CSS/image readability
- extension names, input actions, UI identifiers and save paths
- shared/global Career/RLS function use
- cross-job auction, scrap, custody and transaction ownership

## Validation result

```text
Corrupt ZIPs: 0
Unsafe paths: 0
Duplicate internal active paths: 0
Nested archives: 0
Executable/native payloads: 0
Malformed JSON: 0
JavaScript syntax failures: 0
Lua compile failures: 0
Cross-ZIP identical active paths: 0
Cross-ZIP byte-identical files: 0
```

The exact three archives do not overwrite one another through identical internal paths. Any runtime failure involving this exact combination is therefore not proven to be a same-path load-order collision.

## Finding 1 — Uploaded JOB-04 file is still the pre-split full v0.3.4 bundle

The supplied JOB-04 archive exactly matches the pre-split v0.3.4 input recorded by the later v0.3.5 split audit. It is not the slim v0.3.5 feature module and it is not the separate Browser Core package.

Confirmed content still present:

- shared main BeamNG/RLS UI bundle;
- phone layout override;
- generic RedFox browser bridge;
- complete stale Recovery/Tow website copy;
- complete stale FoxNet Auctions website copy;
- BeamBook, FoxFax, Parts, Export, Insurance and other unrelated websites;
- duplicate website mirrors;
- historical reports and MHTML captures.

This archive is therefore unsafe to describe as the post-split slim JOB-04 package. It may still conflict with the installed BeamNG/RLS version or with the authoritative Browser Core even though it does not duplicate JOB-09 or JOB-13 paths.

### JOB-04 composition detail

- Historical/development records: 195 files / 22,686,423 bytes
- Unrelated feature websites: 658 files / 18,529,590 bytes
- Shared browser/core: 50 files / 5,866,537 bytes
- JOB-04 feature/runtime or mirror: 92 files / 1,108,975 bytes
- Other: 52 files / 211,634 bytes
- Exact duplicated site-mirror pairs: 371
- MHTML reference captures: 4 files / 15,637,920 bytes

Dangerous shared/core paths include:

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
lua/ge/extensions/ui/phone/layout.lua
lua/ge/extensions/redfoxCareerWeb.lua
```

## Finding 2 — JOB-09 v0.4.4.3 is path-isolated but heavily bloated

JOB-09 contains no JOB-04/JOB-13 website copies and no stock Career/RLS or shared Browser Core override paths.

Its active names are JOB-09-specific, including:

```text
lua/ge/extensions/redfoxTowRecoveryDispatch.lua
lua/ge/extensions/core/input/actions/redfox_tow_recovery_dispatch.json
lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json
scripts/redfox_tow_recovery_dispatch/modScript.lua
ui/modules/apps/redfoxTowPortal/**
```

However, 141 of 164 entries are reports, diffs, inventories or development documentation. Two external catalog-manager files are also mounted inside the playable ZIP. These files do not create the observed path collision, but future packages must use a runtime allowlist.

## Finding 3 — JOB-09 current code still contains superseded or unresolved behavior

The exact v0.4.4.3 ZIP still:

1. requires a purchased personal Career/RLS garage before lien claim and creates a Career inventory vehicle during claim;
2. does not implement David's superseding custody-to-same-yard company/shop claim flow;
3. directly calls Random Events event-module `spawn()` without reproducing the manager's normal spawn-context setup, leaving JOB-09-imported scenes able to favor unsuitable links such as tunnels;
4. uses raw substring classification where the Rail/Train token `train` can match text such as `drivetrain`;
5. contains internal auction and scrap disposition fallbacks that functionally overlap JOB-13 and JOB-04 ownership.

These are functional/ownership concerns, not direct internal-path conflicts. No correction was made during this audit.

## Finding 4 — JOB-13 confirmed idle disk-write incident

**Severity:** Medium performance and storage-wear defect  
**Runtime scope:** JOB-13 extension loaded, auction page may be closed  
**Direct JOB-09 path collision:** No

In `lua/ge/extensions/redfoxJob13Auction.lua`:

- `M.onUpdate()` calls `tickLots()` every 0.5 seconds;
- `tickLots()` always calls `saveState(false)` even when no lot or auction data changed;
- `saveState(false)` permits a full JSON write every two seconds.

Therefore the standalone auction backend can write its state file approximately:

```text
30 times per minute
1,800 times per hour
```

while loaded and idle. This is a confirmed code-path defect. It may contribute to stutter or storage activity when JOB-13 runs with other large mods, but it does not by itself prove the cause of every reported slowdown or Career-load failure.

### Required repair category

- dirty-state tracking;
- event-driven saves after actual state changes;
- periodic safety checkpoint only while an auction has time-dependent active work;
- no repeated idle write when nothing changed;
- retain forced save on unload and transaction boundaries.

JOB-13 owns this correction. JOB-09 must not silently patch JOB-13 source.

## Finding 5 — Narrow global-hook risk in JOB-04

`redfoxWreckingYardPurchase.lua` temporarily replaces the global Career functions:

```text
career_modules_vehicleShopping.buyFromPurchaseMenu
career_modules_vehicleShopping.cancelPurchase
```

It restores them after submission, cancellation or extension unload. This is narrower than a permanent override, but it can still collide with another mod that wraps the same functions during an active purchase session.

The stale JOB-04 browser bridge also exposes auction/recovery transaction action names that conceptually belong to JOB-13/JOB-09. This creates ownership ambiguity even without shared paths.

## Cross-job verdict

```text
JOB-09 direct path collision with supplied JOB-04/JOB-13: NOT FOUND
JOB-09 copied unrelated websites/shared browser core: NOT FOUND
JOB-09 package bloat: CONFIRMED
JOB-09 superseded claim design: CONFIRMED
JOB-09 Random Events spawn-context gap: CONFIRMED
JOB-09 train/drivetrain classification bug: CONFIRMED
JOB-04 supplied as post-split slim package: FALSE — exact upload is pre-split v0.3.4
JOB-04 shared/core and unrelated-content risk: CONFIRMED
JOB-13 idle repeated state writes: CONFIRMED
All-three runtime compatibility: NOT PROVEN BY STATIC AUDIT
```

## Safe next order of operations

1. Do not edit or repackage the exact JOB-09 v0.4.4.3 archive yet.
2. Do not install the supplied pre-split JOB-04 v0.3.4 alongside the split Browser Core/slim JOB-04 packages.
3. Verify the exact installed JOB-04 files are Browser Core v0.1.0 plus slim JOB-04 v0.3.5 before compatibility testing.
4. Test Career load in sequence: Browser Core + slim JOB-04; add exact JOB-09; then add JOB-13.
5. Capture `beamng.log` at the first failing combination before changing JOB-09.
6. Repair JOB-13 idle writes in JOB-13 ownership.
7. After David approves scope, build the next JOB-09 version from a clean runtime allowlist and address only the approved JOB-09 functional defects.

## Change record

```text
Mod source changed: NONE
ZIP contents changed: NONE
User save files changed: NONE
GitHub documentation added: THIS INCIDENT REPORT ONLY
Runtime claims made without BeamNG test: NONE
```