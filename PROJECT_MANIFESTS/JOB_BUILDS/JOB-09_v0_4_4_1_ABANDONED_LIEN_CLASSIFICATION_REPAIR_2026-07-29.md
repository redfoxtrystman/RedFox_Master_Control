# JOB-09 v0.4.4.1 — Abandoned/Lien Classification Regression Repair

**Date:** 2026-07-29  
**Status:** Built and statically verified; BeamNG runtime untested

## Exact artifact

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_1_AbandonedLienClassificationRegressionRepair.zip
SHA-256: 9c975a2b215a0be40367135f6a71b124926e42d0fe86b1a34af2893eacade1a9
Size: 1,691,362 bytes
ZIP entries: 171
Packaged files: 146
```

## Repair

v0.4.4 incorrectly allowed broad `construction` classifications to become `heavy_target` entries. Detached crane pieces, spreader bars and other equipment could therefore enter abandoned calls and then fail the title/lien intake expected for complete vehicles.

v0.4.4.1:

- separates general tow eligibility from abandoned/lien eligibility;
- makes construction configurations unreviewed by default;
- blocks detached crane parts, spreader bars, rigging, counterweights, outriggers and similar equipment from abandoned/lien selection;
- blocks police, law-enforcement, ambulance, fire and tow-support configurations from ordinary abandoned calls;
- preserves normal passenger vehicles, heavy trucks, semis, trailers and buses;
- allows a complete mobile crane only after an exact manual heavy-target classification;
- validates abandoned/lien eligibility after spawning and again at yard intake;
- adds a no-lien/no-payment escape for old saved jobs containing non-lienable targets;
- records catalog role, source and lien eligibility on generated targets;
- exposes the reason an entry is allowed or blocked in the catalog UI.

## Preserved v0.4.4 features

- Random Events 2.1 detection and warm-up
- Timber Spill and RV Trouble imports
- vehicle/item catalog and external manager
- Scene Builder per-item classification
- saved-scene enable/disable controls
- mandatory police blockers
- active-job recovery
- per-yard custody, company and sales capacities/upgrades
- real RLS garage linking and same-inventory-ID transfer
- lien claim verification and rollback
- direct sale, Copart-style auction and scrap
- portal, records, fleet and invoices

## Verification

- 59/59 source checks passed
- all Lua compiled with `texlua --luaconly`
- all JSON parsed
- all JavaScript passed syntax checking
- mocked classification and module-load tests passed
- ZIP CRC, duplicate-entry and path-safety checks passed
- no native/executable payloads
- no Random Events source overrides
- no stock Career/RLS core overrides
- exact 146-file source-to-re-extraction hash comparison passed
- independently re-extracted packaged copy passed 59/59 checks

## Runtime caveat

Actual BeamNG, Career/RLS, Random Events 2.1, custody, lien and scene behavior is not claimed working until David tests this exact artifact.