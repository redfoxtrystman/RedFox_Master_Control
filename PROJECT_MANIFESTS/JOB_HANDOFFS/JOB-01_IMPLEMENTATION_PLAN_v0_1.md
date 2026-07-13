# JOB-01 v0.1 Implementation and Verification Plan

Status: implementation in progress; runtime untested

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
- status stays `BUILT — RUNTIME UNTESTED`.

## David's required runtime test

1. Disable the older all-in-one FoxNet ZIP and Better Career.
2. Enable RLS Career Overhaul 2.6.6 plus the JOB-01 v0.1 test ZIP.
3. Clear BeamNG UI cache if the old phone bundle remains visible.
4. Start an RLS Career save on West Coast USA.
5. Open the existing RLS phone; confirm its existing apps remain.
6. Confirm one IceFox icon appears after Marketplace and opens IceFox Home.
7. Open an RLS computer; confirm `IceFox / FoxNet` appears.
8. Open it; confirm the desktop appears, then click the IceFox desktop icon.
9. Confirm phone and PC display `redfox.home` and the same registry count.
10. Confirm `Return to RLS Computer` works.
11. Repeat phone Home and PC Home on one non-West-Coast map.
12. Confirm ordinary RLS Marketplace and another existing phone app still open.
13. Capture `beamng.log` plus screenshots for JOB-11.

No one may report working, fixed, or done before this test passes.
