# RLS Base Preflight Static Assessment

Generated local time: 2026-08-10

Purpose:
Prepare the isolated RLS test step without enabling, copying, moving, or editing any mod files.

## Status

This was a read-only static inspection.

No BeamNG game files were edited.
No active mod files were edited.
No ZIP files were modified.
No RLS files were copied into the active mods folder.

Verification labels:

- `static_checked`
- `zip_integrity_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## RLS Base ZIPs To Test Later

Held folder:
`D:\RedFoxMods\backups\beamng_v039_active_mods_hold_20260809_230822\CAREER NEW`

Recommended isolated RLS base test set:

- `rls_career_collection_release.zip`
- `rls_career_overhaul_2.7.0.zip`
- `rls_repo_mod_manager.zip`

Do not include these in the first RLS base test:

- RLS map packs
- RLS RaceTab
- RLS RealCargo
- RLS non-repo mod collection
- RLS tanker hotfix
- RedFox Tow
- JOB04/FoxNet
- JOB13 Auctions
- tow vehicle packs

## RLS Base Summary

`rls_career_collection_release.zip`

- 32 entries
- mod info title: RLS Career Collection 5.3
- No Lua files found in the ZIP summary
- No legacy `ui/modModules` entries
- No Vue mod entries

`rls_career_overhaul_2.7.0.zip`

- 4,802 entries
- mod info title: RLS Career Overhaul v2.7.0 Beta
- 229 Lua files
- 108 gameplay files
- 57 legacy `ui/modModules` entries
- 4 `ui/ui-vue/mods` entries
- 1 phone layout override at `lua/ge/extensions/ui/phone/layout.lua`
- No `ui/ui-vue/dist/index.js` or `index.css` global dist override found in this ZIP summary

`rls_repo_mod_manager.zip`

- 18 entries
- includes legacy module `ui/modModules/repoManager/repoManager.js`
- very small compared with RLS overhaul

## v0.39-Aware RLS Evidence

RLS Overhaul 2.7.0 includes:

- `lua/ge/extensions/overhaul/uiRoutes.lua`
- `ui/ui-vue/mods/rls_career_overhaul/index.js`

`uiRoutes.lua` says BeamNG 0.39's Lua router is authoritative and registers custom RLS routes through:
`ui_router_routeManager.registerModRoutes(...)`

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

The Vue mod index notes that BeamNG 0.39 serves the Vue shell from `ui-vue/dist`, so RLS uses official mod entry points under:
`ui/ui-vue/mods/rls_career_overhaul/`

Important conclusion:
RLS 2.7.0 appears intentionally adapted for BeamNG v0.39 UI routing.

## RLS Risk Surface

RLS Overhaul 2.7.0 is still high risk because it has a large override surface.

Override modules include:

- `career/career`
- `career/saveSystem`
- career delivery modules
- career insurance modules
- career inventory
- career marketplace
- career part shopping
- career vehicle shopping
- `core/recoveryPrompt`
- `core/cameraModes/unicycle`
- `freeroam/bigMapPoiProvider`
- `freeroam/vueBigMap`
- `gameplay/markerInteraction`
- `gameplay/missions/progress`
- `gameplay/parking`
- `gameplay/police`
- gameplay traffic police/vehicle modules
- UI minimap modules
- UI pause providers
- `ui/router/routeHandlers`

Important conclusion:
RLS must be tested by itself before any RedFox Tow/FoxNet work. If it fails, the failure could come from career state, phone route state, overrides, or old user settings.

## Current-Game Path Collisions

RLS Overhaul 2.7.0 has 61 same-path collisions with the current BeamNG v0.39 game folder.

Notable collision groups:

- gameplay logistics JSON
- gameplay insurance JSON
- `lua/vehicle/controller/playerController.lua`
- legacy `ui/modules` assets
- `ui/ui-vue/src/App.vue`
- career route/source files
- career vehicle shopping/source files
- career inventory/source files
- pause shell source
- refuel UI source
- vehicle config tuning source
- game context store source

Important conclusion:
The isolated RLS runtime log must be checked carefully for route/override errors before adding RedFox Tow.

## Log Search Targets For RLS Test

After David performs the isolated RLS base test, search the fresh log for:

- `RLS`
- `rls`
- `overhaul`
- `overrideManager`
- `overhaul_uiRoutes`
- `Registered`
- `registerModRoutes`
- `routeManager`
- `phone-main`
- `phoneLayout`
- `ui_phone_layout`
- `ui/ui-vue/mods/rls_career_overhaul`
- `career_saveSystem`
- `vehicleShopping`
- `insurance`
- `marketplace`
- `playerController`
- `fatal`
- `exception`
- `error`
- `out of memory`
- `D3D`
- `VRAM`

## Isolated RLS Test Gate

Only run this after the current clean RedFox lane passes.

David steps:

1. Keep the old full mod stack disabled.
2. Add only the three RLS base ZIPs listed above.
3. Start BeamNG.
4. Enter Career/RLS.
5. Open the phone if possible.
6. Check whether the phone apps/routes appear or are blank.
7. Exit BeamNG.
8. Let Codex read the fresh `beamng.log`.

Do not add maps until base RLS passes.

Do not add RedFox Tow until base RLS passes.

Do not call RLS stable until David confirms it works in BeamNG.
