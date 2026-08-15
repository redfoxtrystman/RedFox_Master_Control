# RedFox Job Equipment Alpha v0.0.6 — BeamNG 0.39 / Newer RLS Compatibility Hardening

**Date:** 2026-08-15  
**Module:** RedFox Job Equipment / Prop Spawner  
**Baseline:** v0.0.5 Layout Presets + BeamNG Previews  
**Status:** STATIC/PACKAGE VERIFIED — DAVID RUNTIME TEST REQUIRED

## Important source limitation

David reported a brand-new paid Patreon RLS release and said it had been uploaded/reassembled in another chat. That exact newest paid RLS archive was **not available to the current chat/File Library at build time**, so this is **not** a file-for-file audit of that exact paid release.

This patch is based on:

- the verified BeamNG 0.39 behavior;
- the repository's existing RLS 2.7.0 hotfix compatibility audit;
- a direct source audit of RedFox Job Equipment v0.0.5.

When the recombined paid RLS ZIP is supplied to the current chat, run an exact shared-path/API/lifecycle comparison before calling compatibility fully proven.

## Why v0.0.5 needed hardening

### 1. Heavy startup scan

v0.0.5 recursively scanned `/vehicles/` for every `*.pc` during extension load. With a larger RLS/mod loadout this can increase startup stalls and makes the extension more sensitive to 0.39 load timing.

### 2. Raw config-file assumptions

BeamNG 0.39 changed custom-config naming/display behavior. Using BeamNG's own `core_vehicles.getConfigList(true)` registry is safer than treating `.pc` filenames as the authoritative catalog.

### 3. Object-ID cleanup safety

v0.0.5 primarily tracked spawned equipment by BeamNG object ID. If a tracked prop disappeared outside this mod and the engine later reused that ID, a future cleanup could theoretically target the replacement object.

### 4. Spawn refusal can be legitimate

BeamNG 0.39 can refuse manual vehicle spawning under low-memory conditions. The tool must fail safely and report the refusal rather than assume RLS caused the failure.

## v0.0.6 changes

- Deferred equipment scan until the level/vehicle registry is ready.
- Primary catalog source is now `core_vehicles.getConfigList(true)`.
- Recursive `.pc` scan is retained only as compatibility fallback.
- BeamNG registry preview path remains the first-choice thumbnail source.
- Every spawned prop receives a unique RedFox ownership name.
- Cleanup requires ownership-name/model verification before deletion.
- Recycled object IDs are explicitly protected.
- If the ownership tag cannot be confirmed, the just-spawned object is rolled back instead of becoming an unsafe/untracked cleanup target.
- `autoEnterVehicle=false` and `playerUsable=false` retained.
- Existing categories, favorites, OFF/5/10/15/30/60 timers, per-item/category/all cleanup, close/toggle controls, thumbnails, and 8 saved layouts retained.
- Tow-complete cleanup remains intentionally absent per David's request.

## Non-conflict design

The v0.0.6 archive contains no:

- `ui/` files;
- RLS overhaul files;
- Career inventory/shop/maintenance/parts files;
- map/level files;
- vehicle/JBeam asset overrides;
- phone/router files;
- RedFox JOB-04/JOB-09/JOB-13 files.

Unique primary paths:

- `lua/ge/extensions/redfoxJobEquipment/alpha006.lua`
- `lua/ge/extensions/core/input/actions/redfox_job_equipment_alpha006.json`
- `scripts/redfox_job_equipment_alpha_v006/modScript.lua`

## Verification

- Lua structural/block/delimiter check: PASS
- JSON parse: PASS
- v0.0.5 feature-preservation assertions: PASS
- forbidden override path scan: PASS
- v0.0.5 vs v0.0.6 exact packaged file collisions: 0
- final ZIP reopen/test: PASS
- final ZIP entries: 7
- ZIP SHA-256: `bc3777db7b501b1644efb7951b091a617ff6faf3c9a9f4cd981fd0481dfb1c4d`

## Runtime acceptance test

1. Disable/remove v0.0.5.
2. Enable v0.0.6 with the new RLS.
3. Enter Career and wait about 2 seconds after map load.
4. Confirm scan completes, preferably with `source: BeamNG config registry`.
5. Confirm thumbnails display.
6. Spawn one cone; use `Despawn Props`; confirm only the RedFox cone is removed.
7. Test one timer preset.
8. Save/reload one layout.
9. Watch `beamng.log` for spawn refusal, low-memory, config, or extension-load errors.

Do not label exact newest-paid-RLS compatibility proven until that exact archive is inspected and David completes this runtime test.
