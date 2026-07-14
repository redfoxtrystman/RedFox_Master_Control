# JOB-01 v0.2 Implementation and Verification Plan

Status: built; runtime untested

## Exact runtime edit set

RedFox-owned files are listed in `JOB-01_PLATFORM_OWNED_FILES.txt`.

The build modifies exactly two files read from the verified RLS 2.6.6 ZIP:

1. `ui/ui-vue/dist/index.js`
   - add one `redfox-icefox` manifest;
   - add one `phone-redfox-icefox` iframe route;
   - add one `redfox-icefox-desktop` iframe route;
   - add a registry-only parent/iframe message adapter.
2. `lua/ge/extensions/ui/phone/layout.lua`
   - add `redfox-icefox` after Marketplace to default layouts;
   - migrate existing saved layouts when the ID is absent.

No other RLS file is emitted.

## Build gates

- exact RLS archive SHA-256;
- every patch anchor occurs exactly once;
- one manifest, one phone route, one PC route;
- two layout ID occurrences: default plus migration;
- no duplicate ZIP paths;
- ZIP CRC passes;
- JavaScript parses;
- RedFox Lua contains no Career authority mutation calls;
- output contains TXT and HTML verification reports;
- original working-system IceFox logo hash matches the source archive;
- all packaged RedFox SVG assets parse as XML;
- PC and phone reference the same shared browser JavaScript, CSS, registry, and
  destination paths;
- status stays `BUILT — RUNTIME UNTESTED`.

## David's required runtime test

1. Disable the older all-in-one FoxNet ZIP and Better Career.
2. Enable RLS Career Overhaul 2.6.6 plus the JOB-01 v0.2 test ZIP.
3. Clear BeamNG UI cache if the old phone bundle remains visible.
4. Start an RLS Career save on West Coast USA.
5. Open the existing RLS phone; confirm its existing apps remain.
6. Confirm one IceFox icon appears after Marketplace and opens IceFox Home.
7. Confirm the icon is the original orange-and-white IceFox fox head, not the
   temporary blue generic mark.
8. Open an RLS computer; confirm `IceFox / FoxNet` appears.
9. Open it; confirm the RedFox start screen appears, then click its IceFox card.
10. Confirm phone and PC show the same dark browser, coastal hero, quick-access
    registry, and `redfox.home` destination count.
11. Test back, forward, reload, home, search, favorite, theme, minimize/close,
    and `Return to RLS Computer`.
12. Repeat phone Home and PC Home on one non-West-Coast map.
13. Confirm ordinary RLS Marketplace and another existing phone app still open.
14. Capture `beamng.log` plus screenshots for JOB-11.

No one may report working, fixed, or done before this test passes.
