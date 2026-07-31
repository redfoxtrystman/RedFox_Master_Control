# JOB-09 v0.4.4.5 Source Verification — Scene Manager and Linked-Garage Delivery

**Date:** 2026-07-31
**Owner:** David / Captain
**Source base:** JOB-09 v0.4.4.4 runtime-slim artifact
**Base SHA-256:** `61b1ef9e746f5978bba2cd7e7a4368aef4c19d2fe17f6c1207142d4fd3a4f6ad`
**Target version:** `0.4.4.5`
**Packaging status at this checkpoint:** NOT YET PACKAGED

## Authorized scope

- Replace the confusing Scene Builder presentation with a guided Scene Manager.
- Make the custody/lien → Tow Company Garage → linked real RLS garage flow explicit.
- Preserve all v0.4.4.4 performance, emergency-filter, Random Events, classification, storage, and runtime-slim behavior.
- Do not edit Browser Core, JOB-04, JOB-13, stock Career/RLS, or Random Events.

## Exact source files changed

| Path | v0.4.4.4 SHA-256 | v0.4.4.5 source SHA-256 |
|---|---|---|
| `lua/ge/extensions/redfoxTowRecoveryDispatch.lua` | `b21794af172a746d720723c2b69d189c99c40ff93d84945ff579d5ad4527e249` | `5fb7716ed4d105f942a2060856ebd2a106c3a2a8a452c4126d05a5bd820628c6` |
| `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json` | `25820513799bb9fda53dd211dafec6b36a3e077f2711e0137006695b9da438bb` | `b348c7b3cd4fe724e916c1f29d83b74237698bc237996c1edd61c7b1b191bcb4` |
| `mod_info/redfox_tow_recovery_dispatch/info.json` | `04dcceef739d3b54c8584d270a89d055eabe6b9f8ef757becd655045bcda9d66` | `43b123d1345d54a8a2eefbfe6928ce20a856b111371b961069906df8f79c7520` |
| `ui/modules/apps/redfoxTowPortal/app.json` | `eb0e498e0ab79be356fc187bb90f067bf8ef3408243c9331d19bfbb5a9aa4638` | `e92e5daf15d431f78c53b54320ecf03e8f50ec7d6980d0eb829a6ffd30b981c6` |
| `ui/modules/apps/redfoxTowPortal/assets/css/portal.css` | `20c4b77a1773478b97de26cb6e3d4642c73804e8828b02e01571100062409418` | `160c84469f6dadfe55861f890cc8f459241164d3e3d1004f52477419ad2e17ae` |
| `ui/modules/apps/redfoxTowPortal/assets/js/portal.js` | `fd115370175cc3e128bbda15ba379b116bce861c294479dbae1f9ea5e37f8126` | `8e24b5581334db3fa58a7d77c7005a19054a14f1d23b6c255b1db86cd82df4d2` |
| `ui/modules/apps/redfoxTowPortal/portal.html` | `e2e30581124f5867e673c23b168721de205abe9cf04ff6a9ae3e6d813059716a` | `b65e15deba92185e78d7ff70bb13952d62ad479fd4d12f626e8a6ba3eb8827cf` |

No other runtime file changed.

## Scene Manager changes

- User-facing name changed from Scene Builder to **Scene Manager**.
- Five guided steps:
  1. load a call scene;
  2. turn editing on only when required;
  3. select an object and choose Keep or Do Not Save for a reusable template;
  4. accept or reject the live scene for the current job;
  5. optionally save the layout as a reusable scene.
- Basic controls appear before technical controls.
- Position/rotation, equipment teaching, role classification, and prop spawning are hidden under Advanced Scene Tools.
- UI explicitly states that Accept affects the current job while Keep/Do Not Save affects only a future reusable template.
- Live tow targets remain protected from deletion.

## Garage-delivery changes

### Stage 1 — custody / lien

- Legal hold and eligibility remain unchanged.
- `Claim into Tow Company Garage` pays the lien, capped storage, and title fee exactly once.
- Exact yard identity and Tow Company Garage capacity are verified.
- The custody record is atomically replaced by a same-yard claimed company asset.

### Stage 2 — linked real RLS garage

- New explicit action: `Deliver to Linked RLS Garage`.
- Exact yard, current map, purchased-garage link, and native garage space are checked before creating ownership.
- A persistent garage-delivery transaction is staged before spawning or creating a Career vehicle.
- If an earlier pending inventory ID exists, delivery resumes verification instead of creating a second vehicle.
- Exactly one owned Career/RLS inventory vehicle is created and its final garage location is verified.
- The virtual Tow Company Garage record is removed only after owned-vehicle and location verification.
- Failed delivery removes the temporary inventory vehicle and restores Tow Company Garage state.
- If temporary inventory removal cannot be verified, the exact inventory ID is preserved in a locked conflict record rather than risking a duplicate or silent deletion.
- v0.4.4.4 `shop_transfer_personal` calls remain supported as a compatibility alias.

## Source verification result

```text
Focused checks passed: 62
Runtime allowlist: 16 exact files
Lua compilation: PASS
JavaScript syntax: PASS (2/2)
JSON parse: PASS (4/4)
Images readable: PASS (6/6)
HTML local references: PASS
Version consistency: PASS
Scene Manager action/label checks: PASS
Garage transaction ordering checks: PASS
Pending-delivery idempotency checks: PASS
Rollback/conflict protection checks: PASS
Shared/core protected paths: ABSENT
Browser Core active-path overlap: 0
JOB-04 slim active-path overlap: 0
JOB-13 active-path overlap: 0
```

## Important status

This is a source/static verification checkpoint. BeamNG runtime behavior is not proven. Packaging and independent re-extraction verification must occur after this commit.