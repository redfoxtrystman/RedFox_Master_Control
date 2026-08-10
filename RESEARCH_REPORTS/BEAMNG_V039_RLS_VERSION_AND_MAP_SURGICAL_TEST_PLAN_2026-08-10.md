# RLS Version And Map Surgical Test Plan

Generated local time: 2026-08-10

Purpose:
Prepare the RLS side of the BeamNG v0.39 recovery with exact version evidence and a safe test order before any files are enabled, copied, edited, or repaired.

This is a read-only analysis report.

No BeamNG files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.

Verification labels:

- `static_checked`
- `code_compared`
- `zip_integrity_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## RLS Core ZIPs Found

Found RLS overhaul core candidates:

- `D:\Games\Steam\steamapps\common\ALL MY MODS IN FOLDERS\redfox donations for redfox career mode\rls_career_overhaul_2.6.6.zip`
- `D:\Games\Steam\steamapps\common\--------donation mods--------\-----------------------------------------------------\rls_career_overhaul_2.7_alpha.zip`
- `D:\Games\Steam\steamapps\common\--------donation mods--------\-----------------------------------------------------\rls_career_overhaul_2.7.0_beta.zip`
- `D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\CAREER NEW\rls_career_overhaul_2.7.0.zip`

Not found in the current filename scan:

- `rls_career_overhaul_2.6.8.zip`

Do not rely on `2.6.8` unless David points to another copy.

## Core Version Structure

`rls_career_overhaul_2.6.6.zip`

- ZIP size: 43,066,347 bytes
- file entries: 378
- Lua files: 198
- gameplay files: 50
- legacy `ui/modModules` files: 29
- Vue mod entries: 0
- global `ui/ui-vue/dist` entries: 4
- `uiRoutes.lua`: absent
- `ui/ui-vue/mods/rls_career_overhaul/index.js`: absent
- phone layout override: present
- player controller override: present

`rls_career_overhaul_2.7_alpha.zip`

- ZIP size: 416,307,029 bytes
- file entries: 3,668
- Lua files: 234
- gameplay files: 60
- legacy `ui/modModules` files: 47
- Vue mod entries: 2
- global `ui/ui-vue/dist` entries: 0
- `uiRoutes.lua`: present
- `ui/ui-vue/mods/rls_career_overhaul/index.js`: present
- phone layout override: present
- player controller override: present

`rls_career_overhaul_2.7.0_beta.zip`

- ZIP size: 562,904,850 bytes
- file entries: 3,795
- Lua files: 236
- gameplay files: 60
- legacy `ui/modModules` files: 47
- Vue mod entries: 2
- global `ui/ui-vue/dist` entries: 0
- `uiRoutes.lua`: present
- `ui/ui-vue/mods/rls_career_overhaul/index.js`: present
- phone layout override: present
- player controller override: present

Held active-stack candidate:
`rls_career_overhaul_2.7.0.zip`

- ZIP size: 562,920,568 bytes
- file entries: 3,793
- Lua files: 236
- gameplay files: 60
- legacy `ui/modModules` files: 47
- Vue mod entries: 2
- global `ui/ui-vue/dist` entries: 0
- `uiRoutes.lua`: present
- `ui/ui-vue/mods/rls_career_overhaul/index.js`: present
- phone layout override: present
- player controller override: present

## Important v0.39 Evidence

Local BeamNG v0.39 file:

`D:\Games\Steam\steamapps\common\BeamNG.drive\ui\ui-vue\mods\README.md`

confirms that Vue UI mods live under:

`/ui/ui-vue/mods/%mod_name%/`

It also documents `ui_router_routeManager.registerModRoutes(...)` as the route-registration bridge.

Local BeamNG v0.39 file:

`D:\Games\Steam\steamapps\common\BeamNG.drive\lua\ge\extensions\ui\uiMods.lua`

discovers Vue mod files under:

`/ui/ui-vue/mods`

## Main Version Conclusion

Use the held `rls_career_overhaul_2.7.0.zip` as the first RLS core test candidate.

Reason:

- It appears intentionally updated for BeamNG v0.39.
- It uses official `ui/ui-vue/mods/rls_career_overhaul/`.
- It includes `lua/ge/extensions/overhaul/uiRoutes.lua`.
- It avoids shipping global `ui/ui-vue/dist/index.js` and `index.css`.

Do not use `2.6.6` as the first test baseline.

Reason:

- `2.6.6` ships global `ui/ui-vue/dist/index.css`, `index.html`, `index.js`, and `index.js.map`.
- It does not include the v0.39 route bridge.
- It does not include the official `ui/ui-vue/mods/rls_career_overhaul/index.js`.

## RLS 2.7.0 Route Evidence

Held `2.7.0` includes:

- `lua/ge/extensions/overhaul/uiRoutes.lua`
- `ui/ui-vue/mods/rls_career_overhaul/index.js`
- `ui/ui-vue/mods/rls_career_overhaul/RlsCareerOverlays.vue`

`uiRoutes.lua` states that BeamNG 0.39's Lua router is authoritative in release builds and registers RLS custom screens at runtime.

It uses source id:

`rls-career-overhaul`

It calls:

`ui_router_routeManager.registerModRoutes(routeSourceId, routes)`

It registers many phone routes, including:

- `phone-main`
- `phone-app-store`
- `phone-bank`
- `phone-marketplace`
- `phone-repo`
- `phone-settings`
- `phone-skills`
- `phone-taxi`
- `phone-tuning-shop`

It also registers:

`menu.overhaulManager`

This is exactly the kind of v0.39 route repair that older builds were missing.

## RLS 2.7.0 Risk Surface

The held RLS core still has a large override surface.

Override examples include:

- `career/career`
- `career/saveSystem`
- career delivery modules
- career fuel module
- career inventory
- career marketplace
- career part shopping
- career vehicle shopping
- `core/recoveryPrompt`
- `core/cameraModes/unicycle`
- `freeroam/facilities`
- `freeroam/vueBigMap`
- `gameplay/markerInteraction`
- `gameplay/missions/progress`
- `gameplay/parking`
- `gameplay/police`
- minimap modules
- pause providers
- `ui/router/routeHandlers`

Important:
RLS can break because of load order, career save state, phone layout, route registration, override collisions, or memory. It must be tested isolated before Tow/FoxNet.

## Difference Between 2.7.0 Beta And Held 2.7.0

Held `2.7.0` and `2.7.0_beta` are close, but not identical.

Entries added in held `2.7.0`:

- `lua/ge/extensions/overrides/gameplay/markerInteraction.lua`
- `ui/ui-vue/src/modules/vehicleConfig/components/LiveWheelData.vue`
- `ui/ui-vue/src/modules/vehicleConfig/components/Tuning.vue`
- `vehicles/autobello/info_rls_hardcore_piccolina.json`
- `vehicles/bluebuck/rls_hardcore_bluebuck.pc`
- `vehicles/covet/rls_hardcore_covet.pc`
- `vehicles/pessima/rls_hardcore_pessima.pc`

Entries removed from held `2.7.0` compared with beta:

- `lua/ge/extensions/ui/router/routeHandlers.lua`
- `ui/modules/loading/loading.css`
- `ui/ui-vue/src/modules/career/components/partShopping/PartSubTree.vue`
- `ui/ui-vue/src/modules/refuel/components/FuelGauge.vue`
- `ui/ui-vue/src/modules/refuel/components/FuelTypeSettings.vue`
- `ui/ui-vue/src/modules/refuel/refuelStore.js`
- `vehicles/bluebuck/rls_race_ai/rls_hardcore_bluebuck.pc`
- `vehicles/covet/rls_race_ai/rls_hardcore_covet.pc`
- `vehicles/pessima/rls_race_ai/rls_hardcore_pessima.pc`

Notable same-path size changes include:

- `lua/ge/extensions/overhaul/overrideManager.lua`
- `lua/ge/extensions/overrides/career/career.lua`
- `lua/ge/extensions/overrides/career/modules/fuel.lua`
- `lua/ge/extensions/overrides/career/modules/inventory.lua`
- `lua/ge/extensions/overrides/career/modules/marketplace.lua`
- `lua/ge/extensions/overrides/career/modules/vehicleShopping.lua`
- `lua/ge/extensions/overrides/career/saveSystem.lua`
- `lua/vehicle/extensions/overrideAI.lua`
- `ui/ui-vue/src/App.vue`
- `ui/ui-vue/src/modules/refuel/views/RefuelMain.vue`

Conclusion:
Held `2.7.0` looks like the intended newer build, but if it fails, compare failures against `2.7.0_beta` before making broad repairs.

## Collection ZIPs Found

Found collection candidates:

- `rls_career_collection_5.2_release.zip`
- `rls_career_collection_5.4.zip`
- `rls_career_collection_5.5.zip`
- held `rls_career_collection_release.zip`

Held `rls_career_collection_release.zip`:

- ZIP size: 17,445,578 bytes
- file entries: 21
- Lua files: 1
- JSON files: 13
- no level files
- no UI files
- no gameplay files

Collection `5.5`:

- ZIP size: 3,415,521 bytes
- file entries: 12
- Lua files: 1
- JSON files: 7
- no level files
- no UI files
- no gameplay files

Conclusion:
For the first isolated RLS base test, use the held `rls_career_collection_release.zip` because it is already paired with the held active-stack RLS base and has the expected broader dependency collection shape.

Do not swap to collection `5.5` until the held base has been tested or David specifically wants that comparison.

## Map Pack Evidence

Held Skeleton Coast:

`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\career maps\rls_career_overhaul_skeleton_coast_beta_0.1.2.zip`

- ZIP size: 797,652,383 bytes
- file entries: 4,438
- Lua files: 6
- JSON files: 364
- JBeam files: 27
- level files: 4,123
- gameplay files: 4
- level root: `skeleton_coast`
- Lua roots:
  - `lua/ge/extensions/landmarks`
  - `lua/ge/extensions/skeletonCoast`

Skeleton Coast notable large files:

- `levels/skeleton_coast/theTerrain.ter`: 50,331,748 bytes
- several ship `.dae` meshes from 15 MB to 39 MB
- multiple 16 MB to 22 MB terrain/background textures

Held The Gap:

`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\career maps\rls_career_overhaul_the_gap_1.1.zip`

- ZIP size: 1,159,707,346 bytes
- file entries: 1,357
- Lua files: 3
- JSON files: 306
- JBeam files: 0
- level files: 1,349
- gameplay files: 4
- level root: `otb_the_gap_11_8_25`
- Lua root:
  - `lua/ge/extensions/theGap`

The Gap notable large files:

- `levels/otb_the_gap_11_8_25/the_gap.ter`: 201,326,668 bytes
- `t_backdrop_base_b.color.dds`: 89,478,660 bytes
- `t_terrain_base_b.png`: 70,497,825 bytes
- `cutlogs.dae`: 54,603,110 bytes
- multiple 20 MB to 51 MB terrain, heightmap, and backdrop files

Conclusion:
Skeleton Coast and The Gap should not be used in the first RLS base test. They are large map/memory tests and should be added one at a time after RLS core loads.

## Recommended RLS Test Order

Only do this after the clean RedFox lane passes.

Test A: RLS base only

Use only:

- `rls_career_collection_release.zip`
- `rls_career_overhaul_2.7.0.zip`
- `rls_repo_mod_manager.zip`

Do not include:

- RLS maps
- RLS RaceTab
- RLS RealCargo
- RLS non-repo mod collection
- RLS tanker hotfix
- RedFox Tow
- JOB04/FoxNet
- JOB13 Auctions
- tow vehicle packs

Test B: one small/known RLS map

After base passes, add only one map pack and test.

Test C: The Gap

Test The Gap by itself with RLS base. Use a normal stock vehicle first, not helicopter, tow shop purchase, or heavy Tow workflow.

Test D: Skeleton Coast

Test Skeleton Coast by itself with RLS base. Use a normal stock vehicle first. Because of the previous memory/fatal report, watch for out-of-memory, D3D, VRAM, texture, and autosave-loop signs.

## Log Search Targets After RLS Tests

Search the fresh `beamng.log` for:

- `RLS`
- `rls`
- `overhaul`
- `overrideManager`
- `overhaul_uiRoutes`
- `registerModRoutes`
- `Failed to register`
- `phone-main`
- `phoneLayout`
- `ui_phone_layout`
- `rls_career_overhaul`
- `career_saveSystem`
- `vehicleShopping`
- `marketplace`
- `inventory`
- `fuel`
- `markerInteraction`
- `routeHandlers`
- `out of memory`
- `D3D`
- `VRAM`
- `fatal`
- `exception`
- `error`

## Stop Rule

Do not patch RLS blindly.

If held `2.7.0` fails:

1. Read the fresh runtime log.
2. Identify whether the failure is route/UI, override/load-order, career save, map memory, or user-state pollution.
3. Compare against `2.7.0_beta` only if the log points at one of the files changed between beta and held.
4. Do not roll back to `2.6.6` unless the v0.39 route evidence is fully understood, because `2.6.6` uses the older global UI override pattern.

Do not mark RLS stable until David tests it in BeamNG and reports it working.
