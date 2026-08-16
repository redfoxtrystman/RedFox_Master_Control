# RedFox Job Equipment Alpha v0.0.7 — Exact RLS 2.7.0.1 Audit

**Date:** 2026-08-15  
**Status:** exact owner-supplied RLS source audited; Job Equipment v0.0.7 package built; runtime test still required.

## Reconstructed RLS input

The paid RLS archive was reconstructed from the three owner-supplied split parts:

- `rls_career_overhaul_2.7.0.1 split.z01`
- `rls_career_overhaul_2.7.0.1 split.z02`
- `rls_career_overhaul_2.7.0.1 split.zip`

Recombined archive:

- size: 554,092,589 bytes
- SHA-256: `4eea948c84be852b3fa34eb935cbfbab07ed1710c123eec9cac427474c2be660`
- central-directory entries: 4,955
- content files: 3,902

ZIP testing found one non-code filename warning for a Synthwave MP3 containing a curly apostrophe mismatch between local and central directory names. Inspected Lua/gameplay files tested correctly.

## Exact compatibility findings

1. **Zero packaged path collisions** between RLS 2.7.0.1 and Job Equipment v0.0.6.
2. RLS 2.7.0.1 **does not override** `lua/ge/extensions/core/vehicles.lua`, so Job Equipment's `core_vehicles.getConfigList` and `core_vehicles.spawnNewVehicle` dependency remains intact.
3. RLS `gameplay/physicalCargo.lua` continues to spawn props through `core_vehicles.spawnNewVehicle(... autoEnterVehicle=false)`, validating the physical-prop architecture.
4. RLS `overhaul/walkEnterVehicle.lua` explicitly rejects live vehicles when `veh.playerUsable == false`. v0.0.7 now explicitly sets the live spawned object's `playerUsable=false` after spawn instead of relying only on the spawn option; a `gameplay_walk` blacklist fallback is included.
5. RLS 2.7.0.1's extension manager documents a BeamNG 0.39 condition where normal input-action caches may exist before mod action files finish mounting. RLS refreshes its own action files via `core_input_actions.onFileChanged` and bindings via `core_input_bindings.onFileChanged`. Job Equipment v0.0.7 now does the same for its Toggle/Despawn controls.
6. Existing v0.0.6 action IDs are preserved so user keybinds can survive the update.
7. RLS parking manipulates only IDs explicitly inserted into its parked-vehicle state; it does not adopt every manually spawned object.
8. RLS Used Car Auction cleanup deletes only its tracked auction-lot IDs.
9. RLS maintenance/business/inventory systems use their own inventory/business vehicle mappings rather than arbitrary manually spawned Job Equipment objects.
10. RLS adds Heavy Machinery/Forklift/Forkable Load content with standard preview metadata. Job Equipment's BeamNG registry scan and preview lookup are compatible with these assets.
11. Job Equipment v0.0.6 could lose its in-memory spawned/timer ownership list after a Lua reload while leaving physical props alive. v0.0.7 adds `onSerialize`/`onDeserialized` tracking preservation and `onVehicleDestroyed` pruning; destructive cleanup still validates the unique RedFox ownership name/model before deletion.

## v0.0.7 non-conflict architecture

No RLS, Career, parts, engine-swap, maintenance, dealership, auction, phone, Vue, map, vehicle, or JBeam file is overridden.

Primary unique paths:

- `lua/ge/extensions/redfoxJobEquipment/alpha007.lua`
- `lua/ge/extensions/core/input/actions/redfox_job_equipment_alpha007.json`
- `scripts/redfox_job_equipment_alpha_v007/modScript.lua`

Exact RLS 2.7.0.1 packaged path collisions: **0**.

## Package verification

Final Job Equipment package:

`RedFox_JobEquipment_Alpha_v0_0_7_EXACT_RLS_2_7_0_1_PATCH.zip`

- ZIP integrity: PASS
- JSON parse: PASS
- Lua delimiter/static structure checks: PASS
- v0.0.6 core features preserved: categories, favorites, previews, OFF/5/10/15/30/60 timers, Despawn Props, per-item/per-category cleanup, close/toggle controls, and 8 saved layouts
- SHA-256: `9fc5880625056d84bbb21bb83ed5052717c661e17576be7536156633ccdc2de4`

## Runtime acceptance

1. Disable/remove v0.0.6 and older Job Equipment alphas.
2. Enable v0.0.7 with RLS 2.7.0.1.
3. Confirm Toggle/Despawn actions appear in Controls.
4. Confirm catalog scan and thumbnails.
5. Spawn one cone/prop and verify walking mode cannot enter it.
6. Despawn it and verify unrelated RLS/player vehicles remain.
7. Test one timer and one saved layout.
8. Optional developer test: Ctrl+L, then verify Despawn Props still recognizes pre-reload RedFox props.
