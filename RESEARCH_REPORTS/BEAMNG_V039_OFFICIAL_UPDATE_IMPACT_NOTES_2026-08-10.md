# Official BeamNG v0.39 Update Impact Notes

Generated local time: 2026-08-10

Purpose:
Tie the local RedFox/RLS/Tow scan results to BeamNG's official v0.39 notes, so tomorrow's recovery work stays grounded in both local evidence and upstream changes.

This is a documentation-only note.

No BeamNG files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.

Verification labels:

- `static_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## Official Sources Checked

BeamNG v0.39 release highlights:
`https://www.beamng.com/game/news/blog/beamng-drive-v0-39/`

BeamNG v0.39 release notes:
`https://www.beamng.com/game/news/patch/beamng-drive-v0-39/`

Official release date shown by BeamNG:
2026-07-29

Local live install version observed from launcher/log evidence:
BeamNG `0.39.4.0`, build `20972`

Old backup version observed from launcher/log evidence:
BeamNG `0.38.6.0`, build `19963`

## Official Changes That Matter For RedFox Recovery

### UI, Router, And Web Bridge Risk

Official v0.39 notes say the Pause menu was rebuilt around Lua Router and scoped navigation, and that Vehicle Configuration, BigMap, Photomode, Replays, HUD Apps, Career screens, and related routes were moved to the same navigation model.

The notes also say:

- UI Apps were renamed to HUD Apps.
- HUD app management and layout editing were ported to Vue.
- the Main Menu, Radial Menu, Map Mode, mission screens, Career Computer, Garage, selectors, and Options now route through Lua Router or related Vue flows.
- Runtime Vue SFC compilation is now the runtime loading architecture for Vue UI mods.
- modders are directed to `ui/ui-vue/mods/README.md` for mod setup, `index.js` load/unload entry points, UI slots, Pause-menu tabs/buttons, and Lua Router routes.

Recovery impact:

- RLS should be tested first with its v0.39-aware route bridge rather than old global UI bundle overrides.
- RedFox Tow/FoxNet should not be broad-merged across JOB04/JOB09/JOB13.
- JOB09 should keep the single-relay web bridge shape unless a fresh runtime log proves another route is required.
- Any missing `ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js` adapter should be added only if the fresh v0.39 log still asks for that legacy Angular host path.

### Career Risk

Official v0.39 notes list Career updates for profile creation, multiple manual saves, dealership behavior, mod vehicle dealership handling, developer options, taxis, vehicle thumbnails, save corruption recovery, and robustness against changed/removed vehicles from mods or game updates.

Recovery impact:

- Do not start the first test in Career.
- Test Freeroam Small Grid clean lane first.
- Add RLS base only after the clean lane is understood.
- Add career maps only after RLS base is understood.
- Test RedFox Tow after clean lane and RLS base are no longer producing unrelated errors.

### Vehicle, Tow, And JBeam Risk

Official v0.39 notes include vehicle light/material changes, common tow hitch changes, clickable triggers on all tow hitches, trailer behavior changes, new vehicle APIs, new node/coupler/latch accessors, and changed handling of vehicle instabilities.

The notes also say a vehicle with repeated instabilities can be removed instead of just pausing physics.

Recovery impact:

- Tow vehicle control unification should be based on v0.39 controls/triggers rather than old assumptions.
- Heli/tow/JBeam crashes should be checked against fresh logs because v0.39 may remove unstable mod vehicles faster than old versions did.
- The first Tow repair should focus on web/phone state bridge stability before adding hook-click or tow-truck control standardization.

### World Editor, Surface Studio, And Material Work

Official v0.39 notes list:

- Material Editor validation/error-checking changes.
- Material Editor object picker highlight behavior changes.
- Terrain Material Editor material import support and validation/error reporting.
- Terrain Importer fixes for deleted terrain, texture maps showing all available terrain materials, material import fixes, textureMap material preset save/load, and mesh import with a heightmap.
- Terrain Painter now has the ability to swap painted material with another from the library.
- Asset Browser material preview thumbnails.
- Vehicle UI texture tool.

Recovery impact:

- Surface Studio's material-scan and material-swap direction is aligned with new official terrain/material tooling.
- The first Surface Studio repair should lean on v0.39 Terrain Painter/Terrain Material Editor behavior, not older file-only global material replacement.
- Because the official Terrain Painter now supports material swapping from the library, Surface Studio should aim to bridge to the current in-game editor workflow before doing larger map-wide conversions.

### Memory, Logs, And Crash Triage

Official v0.39 notes list:

- optimized RAM use in static collision processing.
- improved texture link lookup and loading memory behavior.
- a low-memory detector that can deny manually spawning vehicles or traffic if the game thinks it may run out of memory.
- log file size limiting that trims the middle of oversized logs while preserving earliest and latest records.
- corrupted install handling that exits to desktop when critical install files are detected as corrupted.
- Mod Manager speed improvements for enable/disable work tied to UI app metadata.

Recovery impact:

- David's low-memory crash screenshot may be influenced by active mod count, map size, vehicle count, stale user state, or v0.39's stricter low-memory handling.
- A clean lane test must be done before blaming one mod.
- Fresh logs are important because v0.39 log trimming may remove middle context from noisy sessions.
- Large RLS maps should be tested one at a time only after RLS base is understood.

## Roadmap Confirmation

The official notes support the current RedFox recovery order:

1. Keep current active lane minimal.
2. Test Freeroam Small Grid with only GarageHub and RaceBuilder active.
3. Inspect fresh `beamng.log`.
4. If clean, test isolated RLS base.
5. Inspect fresh `beamng.log`.
6. If RLS base is clean enough, test one RLS map at a time.
7. Repair RedFox Tow from the single-relay v0.4.9.6 web baseline, not the broken v0.4.9.7 merged bridge.
8. Only then continue deeper features: tow controls, hook-click workflow, Surface Studio material editing, race/spawner catalogs.

## Do Not Change Because Of This Note

- Do not start from scratch.
- Do not edit Hub files unless David explicitly asks.
- Do not broad-merge JOB04/JOB09/JOB13.
- Do not ship old global `ui/ui-vue/dist` overrides.
- Do not install multiple versions of the same RedFox mod at once.
- Do not call this runtime verified until David tests it in BeamNG.
