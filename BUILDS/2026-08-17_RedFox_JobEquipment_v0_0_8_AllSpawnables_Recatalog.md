# RedFox Job Equipment Alpha v0.0.8 — All Spawnables / Exact Re-Catalog / Large Previews

**Date:** 2026-08-17  
**Baseline:** v0.0.7 exact RLS 2.7.0.1 compatibility patch  
**Status:** STATIC/PACKAGE VERIFIED — DAVID RUNTIME TEST REQUIRED

## Owner request

Expand Job Equipment beyond automatically detected props:

- show larger preview images more like BeamNG's vehicle selector;
- expose all spawnable configs, not only guessed props;
- allow exact configs to be manually included/excluded from the Prop Catalog;
- allow a normal vehicle (for example a dead car) to be spawned as a non-enterable scene prop;
- reuse JOB-09 Tow's working exact model/config re-catalog idea so a misclassified semi can be saved as Semi Tractor rather than Passenger;
- allow individual, selected-group, filtered-group, or every-spawnable prop-catalog marking.

## JOB-09 pattern reused

The project record for JOB-09 v0.3.0 documents exact model/config category overrides. v0.0.8 mirrors that pattern rather than inventing model-wide overrides.

Vehicle classes:

- Passenger / Light Vehicle
- Motorcycle / Three-Wheel
- Tow Truck / Recovery Equipment
- Heavy / Vocational Truck
- Semi Tractor
- Trailer / Lowboy / Carrier
- Bus / Coach / Skoolie
- Boat / Watercraft
- Aircraft / Helicopter
- Construction / Industrial
- Rail / Train
- Roadside Hazard / Lost Prop
- Other Non-Road / Unclassified

Vehicle class and Prop Catalog membership are deliberately separate axes.

## v0.0.8 implementation

- Primary catalog: every config from `core_vehicles.getConfigList(true)`.
- Adds BeamNG models from `core_vehicles.getModelList(true)` when no normal config exists.
- Adds search across model/config/class/purpose/source/type.
- Views: Prop Catalog, All Spawnables, Favorites, Selected.
- Exact config Prop Catalog add/remove/auto reset.
- Selection + bulk mark/exclude/reset.
- Explicit Mark Every Spawnable As Prop / Reset Every Spawnable To Auto.
- Exact-config vehicle reclassification with full JOB-09 class set and quick Passenger/Semi/Trailer/Prop/Construction buttons.
- Larger selector preview rendering, using BeamNG registry preview first and `ImTextureHandler(path):getID()`.
- Any config can use `SPAWN AS PROP`.
- Vehicle-as-prop uses `autoEnterVehicle=false`, live `playerUsable=false`, and best-effort ignition level 0.
- Existing ownership-safe cleanup, object-ID reuse protection, favorites, purpose/color categories, OFF/5/10/15/30/60 timers, Despawn Props, 8 saved layouts, RLS input-action refresh, and Lua-reload tracking are preserved.
- Existing settings/layout paths are retained so prior user data can carry forward.

## Exact paid RLS 2.7.0.1 audit

Compared final v0.0.8 packaged paths against the reconstructed paid RLS 2.7.0.1 archive (3,902 normalized content files).

- Exact file-path collisions: **0**
- No `ui/` files packaged.
- No `levels/` files packaged.
- No `vehicles/` or JBeam overrides packaged.
- No Career, RLS overhaul, maintenance, parts, auction, phone, or Vue overrides packaged.

## Verification

- Lua `loadfile` syntax via texlua: PASS
- Packaged JSON parsing: PASS
- Baseline function-preservation check: PASS (no v0.0.7 local/public function names lost)
- Required feature assertions: PASS
- Final ZIP reopen/integrity: PASS
- Final ZIP file count: 8
- Final ZIP SHA-256: `0804c36b565e2f93eccddad44be55e1c16234486fa4ec4ec22c271dc4eec1257`
- Packaged alpha008.lua SHA-256: `2d8c06e097121e864d18337902ba31113ff5e35c5b93f6307dfdf5de5793b369`

## Important install rule

Disable/remove v0.0.7 before v0.0.8. The input action IDs intentionally remain stable from v0.0.6 so saved keybinds can survive; running both Job Equipment versions at once would duplicate those action IDs.

## Runtime acceptance test

1. Load RLS 2.7.0.1 Career with only Job Equipment v0.0.8 enabled.
2. Open All Spawnables and confirm cars, semis, trailers, real props, and heavy equipment appear.
3. Confirm large preview images appear for a stock vehicle and stock prop.
4. Spawn a normal car as a prop; confirm no auto-entry and no walk-entry.
5. Re-catalog an exact config (e.g. Semi), close/reopen, and confirm persistence.
6. Add/remove exact configs from Prop Catalog and confirm persistence.
7. Test selected/all bulk prop-catalog controls.
8. Test Despawn Props, one auto-despawn timer, and one saved layout.

Do not claim image rendering or vehicle-as-prop runtime behavior proven until David tests it in BeamNG.
