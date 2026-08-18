# RedFox Job Equipment Alpha v0.0.9 — Start Hidden / Manual Open

**Date:** 2026-08-18  
**Baseline:** v0.0.8 All Spawnables / Re-catalog / Large Previews  
**Status:** STATIC/PACKAGE VERIFIED — RUNTIME TEST REQUIRED

## User-reported problem

The Job Equipment ImGui window opened immediately during BeamNG startup, even before the title screen.

## v0.0.9 behavior

- The extension still loads silently so timers, tracked cleanup, layouts, and input actions remain available.
- The window starts hidden on every fresh BeamNG session.
- It stays hidden at the title screen and after entering a level/Career until explicitly opened.
- Use the existing `Toggle RedFox Job Equipment` control to open/close it.
- Opening it during play does not make it auto-open on the next game launch.
- BeamNG serialization/deserialization may preserve current in-session visibility during Ctrl+L/Lua reloads.
- Existing X close button and `CLOSE WINDOW` button are preserved.

## Preserved v0.0.8 features

All Spawnables, large previews, exact model/config re-cataloging, Prop Catalog, spawn vehicle as prop, favorites, categories/color coding, OFF/5/10/15/30/60-minute despawn, tracked cleanup, and 8 saved scene layouts remain.

## Verification

- Lua syntax via texlua loadfile: PASS
- JSON: PASS
- ZIP reopen/test: PASS
- Paid RLS 2.7.0.1 exact path collisions: 0
- ZIP SHA-256: `59ca8bae2a25abe2ea6ba1adeecbfe3748d7d21a028d10ea1ba220b62080dfa7`

## Runtime acceptance

1. Disable/remove v0.0.8.
2. Install v0.0.9.
3. Launch BeamNG; verify the window does not appear before/at title screen.
4. Enter Career/free roam; verify it remains hidden.
5. Open it using the bound Toggle RedFox Job Equipment action.
6. Close with X, restart BeamNG, and verify it remains hidden until toggled.
