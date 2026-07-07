# RedFox Command Screen Handoff — v0.16.8 Widget Standard / Damage Icon / Bridge Proof

Timestamp = 2026-07-06 20:50 America/Los_Angeles
Chat ID = RF-CMD01
Chat Name = Command Screen Chat
Screen status = 🟨 NEEDS TEST

## Current delivered build

```text
RedFox_CommandScreen_v0_16_8_WIDGET_STANDARD_DAMAGE_ICON_BRIDGE_PROOF_PORTABLE_WITH_ELECTRON_RUNTIME.zip
```

Also delivered:

```text
RedFox_CommandScreen_v0_16_8_WIDGET_STANDARD_DAMAGE_ICON_BRIDGE_PROOF_FULL_SOURCE_no_runtime.zip
RedFox_CommandScreen_v0_16_8_WIDGET_STANDARD_DAMAGE_ICON_BRIDGE_PROOF_OVERLAY_only_changed_files.zip
RedFox_CommandScreen_Diff_Report_v0_16_7_to_v0_16_8_WIDGET_STANDARD_DAMAGE_ICON_BRIDGE_PROOF.zip
```

## Why v0.16.8 was made

David tested v0.16.7 and found:

- Command Screen receiver accepted a manual PowerShell POST.
- BeamNG was not sending real packets yet.
- The v0.16.7 BeamNG Damage Monitor layout was unacceptable because text overlapped when resized.
- Damage display needs to look like the in-game damage UI: a vehicle silhouette/icon, not a text report.
- Clock + Weather must show time/weather/temperature at the top line so shrinking the widget does not hide weather/temp at the bottom.

## What changed in v0.16.8

- Replaced text-heavy BeamNG Damage Monitor with compact BeamNG Damage Icon widget.
- Copied the uploaded Improved Vehicle Damage App SVG into Command Screen assets:

```text
app/assets/beamng_damage/damage_car.svg
```

- Added damage icon color settings:
  - icon/base color
  - outline color
  - good border
  - warning border
  - danger border
  - offline color
- Added BeamNG Bridge Debug widget with:
  - receiver status
  - packet count
  - last packet age
  - last source
  - raw latest packet
  - manual test packet button
- Started one-second Command Screen bridge polling. v0.16.7 had a polling function but did not start the polling interval.
- Updated the BeamNG bridge UI app to send a heartbeat every 2 seconds so David can prove the game-side app is loaded even before real damage exists.
- Reworked Clock + Weather to a top-line compact layout: time + weather + temperature.
- Clock + Weather can optionally show weather icons from `app/assets/weather/`.
- Added RedFox Widget Standard CSS for new visual widgets to reduce overlap/overflow.

## Bridge status after v0.16.8

```text
Command Screen receiver = manually proven by David before v0.16.8
BeamNG sender heartbeat = added in v0.16.8, NEEDS TEST
Real damage stream = NOT proven
Production bridge = NOT proven
```

## What David needs to test

1. Launch v0.16.8 portable.
2. Add BeamNG Damage Icon and confirm it is visual/icon-only.
3. Resize it smaller/larger and confirm no text overlap.
4. Pencil-edit the Damage Icon and change colors.
5. Add BeamNG Bridge Debug and click manual test packet.
6. Confirm packet count increments and Damage Icon reacts.
7. Install/reinstall the included BeamNG bridge UI app, restart BeamNG, add the RedFox CommandScreen Bridge app in BeamNG UI Apps, and see if packet count rises every 2 seconds from heartbeat.
8. Test Clock + Weather small and confirm time/weather/temp stay visible at top.

## What the next chat needs to know

- Do not re-expand Damage Icon into a text report.
- Keep details/debug text in BeamNG Bridge Debug only.
- If heartbeat fails, switch bridge strategy to Lua/custom protocol instead of spending more time on UI app fetch.
- If heartbeat works, add speed/RPM/gear widget next before deeper damage/tire/race data.
- Survival Rating ZIP was uploaded as future reference only and is not integrated yet.
- A later Colorize Mode should allow pencil -> colorize -> click part/text/background/border -> choose color.
