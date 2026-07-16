# JOB-09 — Fleet Identity and Hazard Sites v0.2.5 Handoff

**Date:** 2026-07-16  
**Owner:** JOB-09 regular-chat workstation  
**Status:** **BUILT — RUNTIME UNTESTED**

## Candidate

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip`

- Size: 95,645 bytes
- SHA-256: `52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf`
- Source baseline: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_4_CatalogedHistory.zip`
- ZIP integrity: PASS
- JSON parse: PASS
- Lua syntax: PASS via `texlua loadfile`
- Lua main-chunk local-variable limit: PASS
- Protected Career/shared-platform path scan: PASS
- BeamNG runtime: UNTESTED

## Focused additions

### Tow Fleet Book

The player configures and paints a tow truck in BeamNG, then registers the current vehicle. Each per-Career-profile record stores:

- player-editable unit name;
- automatic call sign;
- fleet role: light-duty, flatbed/rollback, heavy wrecker, rotator, or support/service;
- model and exact part configuration;
- three captured paint palettes and PBR paint values;
- capture map and time.

A selected unit can be renamed, assigned another role, or updated from the current player vehicle after configuration/paint changes. This build records identity only; it does not spawn or drive fleet vehicles.

### Map-aware hazard sites

The road-graph scan now catalogs:

- ordinary road segments;
- intersections;
- sharp curves;
- steep grades.

New procedural accident plans:

- `intersection_tbone`
- `sharp_curve_rollover`

Active calls show site type and available intersection/curve/grade details. Settings show scan counts. One diagnostic line is logged per map:

`[RedFox][TOW][SITE_SCAN] level=... roadSegments=... intersections=... sharpCurves=... steepGrades=...`

Maps with incomplete navigation data may expose fewer semantic sites. Normal road-segment scenes remain as fallback.

### Scene paints

Procedural scene vehicles use a weighted realistic color distribution by default rather than unrestricted random RGB. The setting can be disabled.

### History

New records also store the scene site and scene plan. Existing v0.2.4 history remains compatible and is not rewritten.

## Explicitly not implemented

- hired drivers or dispatcher payroll;
- AI transport to a tow yard;
- automatic hookup, winching, or rotator operation;
- multi-truck winch-control overlay;
- property/business conversion or passive income;
- website/phone/PC integration.

Those future items were sent to JOB-00 in GitHub issue #5. JOB-09 remains focused on the standalone Tow mod.

## Required first test

1. Disable all older JOB-09 ZIPs and enable only v0.2.5.
2. Load the same Career profile and confirm old history/yard data remains.
3. Configure and paint a tow truck; register and rename it in Tow Fleet Book.
4. Reload and confirm the fleet record persists.
5. Run multiple accident calls and inspect Scene site / Scene plan.
6. Return a Fleet Book screenshot, a semantic-site screenshot if generated, and the complete SITE_SCAN and EVENT_LIBRARY log lines.
