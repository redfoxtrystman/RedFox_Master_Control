# JOB-10 — Full Websites v0.3.1 — Pre-Integration Checkpoint

**Date:** 2026-07-14  
**Owner:** JOB-10 — Visual Design / Real Website Polish  
**Status:** Browser prototype approved direction / not integrated / not runtime-proven

## Package

```text
RedFox_JOB10_Full_Websites_v0_3_1.zip
```

SHA-256:

```text
0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
```

Primary file:

```text
START_HERE.html
```

## Changes from v0.3.0

- FoxNet Auctions now produces a variable daily pool of roughly 90–110 active vehicles instead of exactly 100.
- Category totals and results derive from the actual generated daily pool.
- BeamBook no longer swaps Wall posts on a repeating timer. A different set loads when BeamBook is opened; the feed remains stable while the player reads it.
- Scrap Yard is now explicitly a legal Scrap & Wrecking Yard.
- The legal yard includes rotating cheap vehicles for sale: parts cars, wrecked vehicles, salvage-title vehicles, rough runners, rebuilders, and occasional decent low-cost finds.
- Wrecking-yard vehicle listings remain eligible for available legal history/FoxFax presentation.
- Black Market inventory is separated from the legal yard and focuses on high-end stolen/off-book vehicles sold below normal value.
- Black Market vehicles do not offer FoxFax/history reports.
- Black Market listings show high estimated Shadow DMV legalization costs.
- Chop Shop guidance keeps engines, transmissions, axle/rear-end assemblies, VIN-stamped body sections, and other serialized major components in the underground market. Only clearly unmarked components may qualify for the normal Parts Exchange.
- Most Wanted now represents expensive and hard-to-get targets, including exotics, competition cars, heavy machinery, aircraft freight, high-end semis, trailers, and valuable cargo.

## Isolated browser verification

Passed:

- daily auction total remained in the intended 90–110 range;
- auction category filter worked;
- next-day auction rotation changed the visible inventory;
- legal wrecking-yard sale cards rendered and opened legal purchase/history presentation;
- Black Market cards rendered without FoxFax and displayed legalization cost;
- Most Wanted included semi/trailer cargo and aircraft/freight categories;
- BeamBook remained stable while open and changed when re-entered;
- no uncaught JavaScript errors occurred in the stripped-asset interaction test.

## Integration boundary

This package is still a standalone browser prototype. It does not modify or prove:

```text
BeamNG runtime
RLS or Career code
money or banking
ownership
insurance
vehicle shopping
vehicle thumbnails
map detection
missions or spawning
parts inventory
legal/illegal inventory separation
Shadow DMV transactions
auction day detection
AI buyer tick behavior
```

The design is now close enough for the next phase to begin planning exact presentation-only handoffs with JOB-00, JOB-01, JOB-02, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-09, JOB-11, and JOB-12. No runtime source should be replaced until the owning job supplies its stable contract and JOB-00 approves integration.