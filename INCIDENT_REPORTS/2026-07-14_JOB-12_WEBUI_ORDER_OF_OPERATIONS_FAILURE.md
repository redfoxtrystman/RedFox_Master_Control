# JOB-12 Incident Report: WebUI Order-of-Operations Failure

**Date:** 2026-07-14
**Job:** JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
**Owner:** Sponsor System chat
**Status:** Open; corrective build required

## Summary

David requested a configurable key that opens a standalone WebUI menu so the sponsor system could be tested before phone and PC integration. The first JOB-12 test package instead used a BeamNG HUD UI App. That was the wrong launch method. After correction, the second package opened a keybind-driven WebUI, but its buttons and state updates did not work.

This was an instruction-following and order-of-operations failure. The request was clear. JOB-12 substituted a different launcher, then packaged a larger interface before proving the smallest UI-to-Lua event path.

## Timeline

### 2026-07-14 — request received

Required sequence:

1. Configurable keybind.
2. Standalone WebUI menu.
3. Functional sponsor controls.
4. Test independently.
5. Link the same app into phone and PC later.

### 2026-07-14 — v0.5.0 built

Package:

```text
RedFox_SponsorSystem_Standalone_Test_v0_5_0.zip
```

GitHub build record commit:

```text
b5c74e85e4b6fc6e04c428df6d27969e8cc16d2e
```

This package used a HUD UI App. It did not follow the requested keybind-opened standalone menu design.

### 2026-07-14 — user correction

David corrected JOB-12 and restated that the test must be a key-opened WebUI, not a game HUD UI App.

### 2026-07-14 — v0.5.1 built

Package:

```text
RedFox_SponsorSystem_Standalone_WebUI_Keybind_Test_v0_5_1.zip
```

GitHub build record commit:

```text
37be7c72626b7773655ff7766f684ee42602cf06
```

The configurable control and standalone menu opened, but Apply, offer generation, FoxMail, FoxText, status, XP, reputation, points, wallet, and developer actions did not update.

### 2026-07-14 08:49:56 local time

Runtime screenshot showed:

- Standalone WebUI open.
- Unsigned Driver status.
- Zero XP, reputation, and Sponsor Points.
- Apply button visible.
- FoxMail and FoxText counts both zero.

Screenshot filename:

```text
Screenshot 2026-07-14 084956.png
```

### 2026-07-14 08:50:04 local time

Developer Tools screenshot showed:

- Buttons visible.
- Pending wallet still zero.
- No assigned vehicle records.
- No visible backend state change.

Screenshot filename:

```text
Screenshot 2026-07-14 085004.png
```

## What JOB-12 did wrong

### Wrong launcher

A HUD UI App was chosen even though the requested interaction was a keybind-opened standalone WebUI menu.

### Wrong order of operations

Correct order:

1. Inspect a known working keybind/WebUI pattern.
2. Prove one button calls Lua.
3. Prove Lua returns state to the page.
4. Add one sponsor action.
5. Add the larger interface only after the connection works.

Actual order:

1. Build the full interface.
2. Add several tabs and buttons.
3. Run syntax and ZIP checks.
4. Package the mod.
5. Discover runtime event failure during David's test.

### Static checks were treated as enough to ship a runtime test

JavaScript syntax, JSON parsing, expected Lua exports, and ZIP integrity do not prove that UI events reach Lua or that returned state reaches the WebUI.

### Too many features were added before proving one end-to-end action

The build included SponsorHub, FoxMail, FoxText, Developer Tools, wallet display, and vehicle records before a basic backend ping was proven.

## Why the instruction was not followed

The reasons were implementation mistakes by JOB-12:

1. Architecture isolation was prioritized over the exact requested user interaction.
2. The term WebUI was interpreted too broadly even though the surrounding request clearly specified a key-opened menu.
3. The build was rushed to provide a downloadable ZIP.
4. A familiar HUD UI App pattern was used as an unauthorized substitute.
5. The corrected build reused an unproven UI-to-Lua event pattern without first validating one button.

These explain the failure but do not excuse it.

## Corrective order of operations

No new full sponsor package should be released until these steps pass in order:

1. Keybind appears in Controls.
2. Key opens standalone WebUI.
3. Back or Close returns to gameplay.
4. Ping Backend button calls the Lua extension.
5. Lua returns a counter or timestamp.
6. WebUI displays the returned value.
7. Generate BeamNG Offer changes offer count from zero to one.
8. FoxMail count changes to one.
9. FoxText count changes to one.
10. Apply, Accept, and Decline are added only after the above works.

Required log prefixes:

```text
[RedFox][SPONSOR][WEBUI]
[RedFox][SPONSOR][UI]
[RedFox][SPONSOR][LUA]
[RedFox][SPONSOR][STATE]
[RedFox][SPONSOR][APPLY]
[RedFox][SPONSOR][MAIL]
[RedFox][SPONSOR][TEXT]
```

## Required verification report fields

```text
Requested launcher: keybind-opened standalone WebUI
HUD UI App included: NO
Keybind appears: PROVEN or UNPROVEN
Menu opens: PROVEN or UNPROVEN
Close works: PROVEN or UNPROVEN
UI-to-Lua ping: PROVEN or UNPROVEN
Lua-to-UI return: PROVEN or UNPROVEN
Offer generation: PROVEN or UNPROVEN
FoxMail update: PROVEN or UNPROVEN
FoxText update: PROVEN or UNPROVEN
Persistence: PROVEN or UNPROVEN
```

## Rule for all RedFox chats

A requested interaction method cannot be replaced with a technically similar alternative without explicit approval.

Examples:

- Keybind-opened menu is not a HUD UI App.
- Existing phone app is not a replacement phone shell.
- Stock purchase is not vehicle spawning.
- Isolated page add-on is not a duplicate FoxNet ecosystem.

## Ownership

This failure belongs to JOB-12. It was not caused by JOB-01, JOB-02, RLS, BeamNG, or unclear instructions. David's requested launcher and testing sequence were clear.