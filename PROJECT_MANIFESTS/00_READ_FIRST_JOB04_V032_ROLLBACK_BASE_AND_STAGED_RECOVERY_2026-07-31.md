# READ FIRST — JOB-04 v0.3.2 Rollback Base and Staged Recovery

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Affected job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** OWNER CORRECTION — v0.3.2 IS THE DESIGNATED SOURCE BASE

## 1. Exact rollback source

Use this exact archive as the read-only source for the next JOB-04 recovery:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_2120PT_v0_3_2_JUNK_FOCUSED_JOES_UNDESIREABLES_FROM_ICON_v0_3_1.zip
SHA-256: 874f817f61bf7c32498d92f0a29d2c34ff1b5d6a01203a3ec94729d86e03cf76
ZIP bytes: 25,408,916
Files: 1,017
ZIP integrity: PASS
Duplicate internal paths: 0
```

This supersedes any coordinator wording that treated v0.3.4 as the automatic rollback source.

## 2. Why v0.3.2 was selected

v0.3.2 keeps the approved coupled runtime architecture:

```text
FoxNet welcome/browser
+ owner-edited phone/browser tile
+ Wrecking Yard page
+ fast junk-focused native inventory
```

The active Wrecking Yard route is:

```text
sites/scrap_yard/index_v032.html
```

The v0.3.2 selection prioritizes Joe's Junk, low-value Undesireables configurations, junk/project vehicles and selected tow/recovery vehicles while preserving native prices, IDs, seller data, negotiation and native purchase-menu routing.

## 3. What v0.3.2 does not yet contain as the final proven implementation

Later work added or attempted:

- owned-vehicle sale flow;
- whole-vehicle scrap;
- strip-and-scrap shell;
- verified returned parts;
- returned-part sale;
- catalytic-converter scrapping;
- native purchase completion and forced garage-delivery repair.

v0.3.2 contains older experimental Scrap Yard Lua and UI code, but the presence of those files is not proof that the later v0.3.3/v0.3.4 behavior is complete or safe. Do not report the later features as preserved until they are selectively backported and David tests them.

## 4. Confirmed package baggage

The designated base is still oversized and includes unrelated or historical content:

```text
Total files: 1,017
ui/: 457
sites/: 364
docs/: 103
assets/: 36
```

It includes unrelated page families and/or duplicate mirrors such as:

- Auction/FoxNet Auction pages;
- Recovery/Tow pages;
- BeamBook references;
- Parts Exchange;
- Insurance;
- Import/Export;
- Collector Exchange;
- Underground pages;
- old versioned Scrap Yard pages and assets;
- root-site mirrors plus `ui/modModules/redfoxCareerWeb` mirrors;
- old verification reports, diffs, MHTML captures and development records.

Removal must be based on a written path-ownership manifest. Do not delete a mirrored or shared-looking path merely because another copy exists; first prove which runtime host uses it.

## 5. Staged recovery — mandatory order

### Stage A — read-only ownership map

Before editing, classify every v0.3.2 path as:

```text
KEEP — required coupled welcome/browser runtime
KEEP — required JOB-04 Wrecking Yard runtime
KEEP TEMPORARILY — runtime ownership uncertain
MOVE TO RECORDS — reports/history/source captures
REMOVE FROM ACTIVE PACKAGE — belongs to another job
REMOVE FROM ACTIVE PACKAGE — obsolete duplicate proven unused
```

The exact owner-edited tile, welcome page, phone route, Wrecking Yard route, v0.3.2 inventory source and native purchase relay are protected.

### Stage B — cleanup-only candidate

Create one single combined JOB-04 ZIP from v0.3.2 that performs removal only.

Do not add the v0.3.3 selling work or v0.3.4 purchase repair in this build.

Test:

1. Career loads.
2. Phone opens.
3. Owner-edited FoxNet tile appears.
4. Approved welcome page appears.
5. Wrecking Yard opens as v0.3.2-cleanup.
6. Junk-focused listings load.
7. Show Different Cars works.
8. Refresh Yard Stock works.
9. Existing purchase path behaves exactly as the source base did.
10. Logs and performance are recorded.

If cleanup-only fails, restore the exact v0.3.2 source and identify the first removed required path.

### Stage C — purchase repair backport

Only after Stage B passes, selectively port the smallest proven v0.3.4 native purchase/garage-delivery changes. Do not copy the whole v0.3.4 archive.

The exact comparison currently shows v0.3.4 is mostly the same as v0.3.2:

```text
1,009 shared byte-identical files
30 added files
8 changed files
0 files removed
```

This makes a narrow backport possible.

### Stage D — selling/scrap backport

Only after buying is stable, port and test one operation at a time:

```text
owned-vehicle list
→ direct sell
→ whole-car scrap
→ strip-and-scrap shell
→ returned parts
→ returned-part sale
→ catalytic-converter scrap
```

Each operation must use exact Career/RLS inventory IDs and must not create fake money, ownership, inventory, parts or garage success.

## 6. Other jobs remain separate

Do not copy these back into JOB-04:

```text
JOB-05 — BeamBook Marketplace
JOB-09 — Tow / Recovery / Dispatch
JOB-13 — FoxNet Online Vehicle Auctions
```

The coupled exception applies only to the FoxNet welcome/browser page and JOB-04 Wrecking Yard because separating those two broke the known runtime path.

## 7. Current stop rule

```text
NO NEW BROAD ARCHITECTURE CHANGE
NO TWO-ZIP WELCOME/WRECKING-YARD SPLIT
NO FEATURE BACKPORT BEFORE CLEANUP-ONLY RUNTIME TEST
NO DELETION WITHOUT PATH-OWNERSHIP EVIDENCE
```

The next deliverable is the v0.3.2 path-ownership/keep-remove plan, followed by one cleanup-only combined ZIP.