# JOB-12 Standalone WebUI Keybind Test v0.5.1

**Status:** BUILT FOR DAVID RUNTIME TEST — CORRECTED LAUNCH METHOD  
**Job:** JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

## Correction

v0.5.0 incorrectly used a HUD UI App. David required a configurable key that opens a standalone full-screen WebUI menu.

v0.5.1 removes the UI App launcher and uses:

```text
Options → Controls → Open RedFox Sponsor System
```

The user assigns any key. Pressing it loads the Sponsor-owned Lua extension and opens the custom WebUI state:

```text
menu.redfoxSponsorSystem
```

## Included paths

```text
lua/ge/extensions/core/input/actions/redfox_sponsor_system.json
lua/ge/extensions/redfox_sponsorSystemTest.lua
ui/modModules/redfoxSponsorSystem/redfoxSponsorSystem.js
ui/modModules/redfoxSponsorSystem/redfoxSponsorSystem.html
ui/modModules/redfoxSponsorSystem/redfoxSponsorSystem.css
scripts/RedFox_Sponsor_System/modScript.lua
```

## Removed

```text
ui/modules/apps/RedFoxSponsorSystemTest/
```

The build is no longer opened through BeamNG UI Apps.

## Test

1. Disable/remove v0.5.0 and older Sponsor ZIPs.
2. Install v0.5.1.
3. Open Options → Controls.
4. Search `Open RedFox Sponsor System`.
5. Bind a key.
6. Load a map and press the key.
7. Confirm the full-screen SponsorHub/FoxMail/FoxText menu opens.

## Static checks

- Input-action JSON parsed.
- WebUI module JavaScript syntax passed.
- HUD UI App folder absent.
- Protected phone/PC/FoxNet/RLS paths absent.
- ZIP integrity passed.

Runtime remains unproven until David tests it.