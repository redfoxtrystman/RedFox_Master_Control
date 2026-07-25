# JOB-09 — v0.2.6 Selection and Spawn Repair

**Date:** 2026-07-24  
**Module:** `redfox_tow_recovery_dispatch`  
**Visible name:** RedFox Tow & Recovery Dispatch  
**Status:** **BUILT — RUNTIME UNTESTED**

## Installable candidate

- File: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_6_SelectionSpawnRepair.zip`
- SHA-256: `f0cd2878fe0d7e02c04c293e28faa6e4ae7e16262cf5b8dedf34b62ab16c51a1`
- The binary ZIP is delivered in the active ChatGPT workspace and is **not uploaded to GitHub**.

## Runtime findings that triggered this patch

David confirmed that v0.2.5 could complete police, abandoned, and semi calls; Fleet Book registration/rename/role persistence worked; and curve, parking, straight, slope, and dirt-road scene sites appeared. Three concrete problems remained:

1. A RedFox/police-supported scene used a 1969-style police car.
2. A T-Series rollback/flatbed tow configuration was selected with a loaded semi trailer despite not being a valid road tractor.
3. A long loaded trailer spawned buried in sloped dirt terrain.

## Focused changes

### Police configuration year filtering

- Scans installed eligible police/law-enforcement configurations.
- Parses `Years`, `Year`, and common table/string/number forms.
- Default minimum final model year: **2000**.
- Missing-year police configurations are excluded by default.
- Adds saved settings for filter enable, minimum year, and unknown-year fallback.
- Adds `[RedFox][TOW][POLICE_POOL]` diagnostics.
- RedFox road scenes can spawn a stationary qualifying police support unit.

**Boundary:** this applies to police support selected by RedFox. It does not overwrite BeamNG ambient/pursuit police pools or external scene-provider pools.

### Fifth-wheel tractor/trailer compatibility

- Excludes rollback, wrecker, rotator, tow-truck, flatbed-body, dump, mixer, box-body, and similar vocational configs from road-tractor duty.
- Reads installed `.pc` part selections when available.
- Recognizes common `fifthwheel_v2`, legacy `fifthwheel`, kingpin, tractor, day-cab, and sleeper signatures.
- Excludes utility, boat, travel, gooseneck, pintle, dolly, and ball-hitch trailer classes from semi fifth-wheel scenes.
- Semi rollover calls now require both a compatible tractor and trailer.
- Adds `[RedFox][TOW][PAIR]` diagnostics.

### Elevated scene spawning

- Regular crash targets default to 3.5 m above intended placement.
- Heavy/bus/tractor targets default to 4.5 m.
- Trailers default to 6.0 m.
- Targets stabilize once and are then released with planned impact velocity.
- Emergency support vehicles use normal ground placement.
- All three lift values are saved settings.

### Impound economy adjustment

- Default compressed storage rate changed from `$75` to `$750` per game day.
- Old schema using the untouched `$75` default migrates once.
- Non-default player rates remain unchanged.
- Three-day hold remains unchanged.

## Persistence and protected boundaries

- Existing settings, layout, yard/profile, and saved-scene file paths are unchanged.
- Fleet Book, tow yards, yard records, impound records, history, and layouts are preserved.
- No stock Career module or shared phone/PC platform files are included or replaced.

## Static verification

- ZIP integrity: PASS.
- Lua syntax/loadfile compilation: PASS.
- Main-chunk local-variable ceiling: PASS.
- JSON parse: PASS.
- Protected-path scan: PASS.
- Version consistency: PASS.
- Metadata-rule unit samples: PASS.
- Settings migration unit sample: PASS.
- BeamNG runtime: UNTESTED.

## Required focused test

1. Disable all older JOB-09 ZIPs and enable only v0.2.6.
2. Confirm Career, Fleet Book, yard, impound, and history persistence.
3. Complete one ordinary tow smoke test.
4. Run multiple road scenes and verify RedFox police support year selection.
5. Run at least three semi rollover calls and confirm no tow/rollback config is used as tractor.
6. Test a semi/trailer scene on uneven terrain.
7. Capture and later reuse one saved scene.
8. Return screenshots, `[POLICE_POOL]`, `[PAIR]`, and `beamng.log` on any error.

## Not implemented in this patch

Convoy AI, fleet teleport recall, fire/burned-out scenes, major pileups, illegal towing, specialized yards, hazmat/water/aircraft work, cross-map cargo preservation, GM UI, website, and phone command center remain planned work.