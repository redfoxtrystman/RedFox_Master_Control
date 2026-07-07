# RedFox Command Screen Roadmap — After v0.16.9

Timestamp = 2026-07-07
Chat ID = RF-CMD01
Screen status = 🟨 NEEDS TEST

## Packaging rule going forward

David wants normal Command Screen releases to include:

1. Full portable ZIP with Electron runtime.
2. Colored diff / verification report ZIP.

Do not make overlay-only ZIP or full-source-no-runtime ZIP unless David specifically asks.

Exception: BeamNG bridge mods are separate game mods and should be delivered as their own BeamNG-ready ZIP when changed.

## v0.16.9 current test purpose

v0.16.9 is not a final data bridge. It is a redundant packet-loss proof build.

It tests three BeamNG-to-CommandScreen methods:

1. HTTP POST JSON.
2. HTTP GET / image beacon.
3. UDP JSON through BeamNG Lua extension.

Success condition: at least one method increments method counts in Command Screen Bridge Debug.

## Issues David reported after v0.16.9

### Clock + Weather still wrong

Current problem:

- Time and temperature show, but weather condition/date/details are still not arranged as requested.
- David wants all critical info at the top of the widget at all times.

Required behavior:

- Top line must always show: time + weather condition + temperature.
- If icons/images are enabled, images go below the top line.
- If images are disabled, widget stays compact one-line/time-weather-temp style.
- Default/dummy weather images must actually display when image mode is enabled, even if they are simple placeholders.
- Weather/game-event icon set should include sunny, cloudy, rain, snow, storm, fog, wind, unknown, flood, tornado, blackout, infection.

### Legacy Simple Launcher needs clarification/default behavior

Current problem:

- David sees a Legacy Simple Launcher widget and did not explicitly ask for it.

Required behavior:

- Either hide it from default layouts or clearly label it as optional/fallback.
- It can remain available, but should not confuse the main BeamNG bridge workflow.
- Launcher links must be real and maintained.

### Web widget blank / links broken

Current problem:

- Web widget shows blank/placeholder area for some URLs.
- Changing site does not reliably load.
- Reddit and Discord pages/links were previously fixed by David but got changed again.

Required behavior:

- Do not show silent dummy blanks.
- If a site blocks embedding, show a clear blocked-site message and an Open External button.
- Verify default shortcuts/URLs for Reddit and Discord and preserve David's corrected values.
- Prefer a proper Electron BrowserView/webview/external-open fallback instead of pretending every site can iframe.

### System Reader lacks CPU temperature

Current problem:

- System Reader shows CPU/RAM/OS/app memory but no temp/fan sensors.
- David needs CPU temperature because he sometimes gets CPU over-temperature warnings.

Required behavior:

- Add a real sensor-provider path, not fake values.
- Preferred providers/fallbacks:
  1. HWiNFO sensor bridge/shared memory if available.
  2. LibreHardwareMonitor/OpenHardwareMonitor WMI/helper if available.
  3. Windows thermal-zone fallback only as low-confidence ACPI value.
- UI must label provider and confidence.
- Never fake CPU temp.

### Widget standard still needs transform support

Required standard for future widgets:

- Resize.
- Rotate.
- Recolor.
- Opacity.
- Border/outline color.
- Background color/image.
- Text color/size where text exists.
- Compact mode.
- Debug/details hidden unless opened.
- No text overlap.
- Safe minimum dimensions.

### Damage Icon widget

Keep the in-game-style icon approach.

Do not return to large text reports. Detailed JSON/debug text belongs in Bridge Debug only.

Future colorize mode:

- Pencil -> Colorize.
- Click part/background/text/border.
- Pick color.
- Apply to selected element.

Damage color logic:

- Green/orange/red are damage state colors.
- If user chooses a damage-state color as the main icon color, use an outer border/outline to preserve visible damage-state feedback.

### Survival Rating

Uploaded Survival Rating app should be treated as future reference.

It should probably sit under BeamNG / Damage-Safety and share bridge data with damage widgets, but do not integrate until the basic bridge path is proven.

## v0.16.9 test checklist for David

1. Start Command Screen v0.16.9.
2. Add BeamNG Bridge Debug.
3. Click manual test packet and confirm Command Screen count rises.
4. Install RedFox_CommandScreen_BeamNG_Bridge_v0_16_9.zip directly into Documents/BeamNG.drive/mods.
5. Restart BeamNG.
6. Add these UI apps:
   - RedFox CommandScreen POST Bridge
   - RedFox CommandScreen GET Bridge
   - RedFox CommandScreen UDP Starter
7. Watch Bridge Debug method counts.
8. Test one app at a time, then all three together.
9. Report which method counts rise: POST, GET/beacon, UDP.
10. Run for 60 seconds and report packet count/lost/duplicate/gap numbers if available.

## Next build recommendation

v0.16.10 should be a cleanup/fix pass before adding more telemetry.

Priority:

1. Fix Clock + Weather top-line layout and image behavior.
2. Fix Web widget blank behavior and default links.
3. Clarify/hide Legacy Simple Launcher from default layout.
4. Add CPU temperature sensor provider plan/UI state without fake readings.
5. If v0.16.9 bridge test succeeds, keep only the working bridge method or mark reliable methods.
6. If v0.16.9 bridge test fails, switch to a deeper BeamNG Lua/protocol/OutGauge-style proof instead of UI-app fetch.
