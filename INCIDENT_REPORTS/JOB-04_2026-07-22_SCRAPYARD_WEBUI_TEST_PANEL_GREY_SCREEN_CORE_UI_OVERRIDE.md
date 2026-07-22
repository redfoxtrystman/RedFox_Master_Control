# JOB-04 Runtime Failure Note — Scrap Yard WebUI Test Panel Grey Screen / Title Background Failure

**Date:** 2026-07-22
**Job:** JOB-04 — Scrap Yard / Wrecking Yard
**Reported by:** David / Captain
**Status:** Open / needs patched test ZIP
**This is not a handoff.** This records the current pause/failure state so testing can continue from the same chat.

## User report

David reported that the test ZIP:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0.zip
```

causes BeamNG to refuse to load the background screen on the title/main menu and then shows a grey screen when the game loads.

## Inspection performed

The uploaded ZIP was inspected from:

```text
/mnt/data/zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0(2).zip
```

Static checks performed:

```text
ZIP integrity: PASS
Entry count: 932
Node syntax check on ui/ui-vue/dist/index.js: PASS
Node syntax check on RedFox/IceFox front scripts: PASS
```

## Important finding

The ZIP includes this global BeamNG UI override:

```text
ui/ui-vue/dist/index.js
```

That file is the compiled Vue UI bundle for the whole game UI, not just the RedFox page. If this file is stale, mismatched with David's BeamNG build, or conflicts with RLS, it can break the main menu/title UI and cause a grey screen.

This is the highest-risk file in the package and is the most likely cause of the reported title background / grey screen failure.

The ZIP also includes:

```text
lua/ge/extensions/ui/phone/layout.lua
```

That is a phone layout override. It is less likely to cause the title background failure, but it can conflict with RLS because RLS also ships phone layout code.

## Relevant file hashes found during inspection

Current JOB-04 ZIP:

```text
ui/ui-vue/dist/index.js
SHA256: 1f700638131de1a5471d303cf69fd3829e32acbfca74f5e05740ca45e27857e7

lua/ge/extensions/ui/phone/layout.lua
SHA256: 8d73384b223e74d1f9934837326fa720ffddf6929cbfa8e8395cf4fea4634f6d
```

RLS 2.6.6 reference ZIP had its own versions:

```text
ui/ui-vue/dist/index.js
SHA256: 824abb4f2ce265d6061987c99c239b013d71652cbe609bbf9f2114f1f5ba4661

lua/ge/extensions/ui/phone/layout.lua
SHA256: 9660828c6a87737abb085c938112e030f2ac8f71b7340ab9e0919b828410e9af
```

The JOB-04 `ui/ui-vue/dist/index.js` is not identical to RLS 2.6.6. It contains RedFox phone/browser route changes and an appended direct vehicle-shopping patch.

## Immediate rule

Do not use JOB-04 v0.1.0 as a runtime test build until patched.

## Proposed patch direction

Build JOB-04 v0.1.1 as a no-core-UI emergency test package:

```text
Remove from JOB-04 package:
- ui/ui-vue/dist/index.js

Likely preserve for inspection before deciding:
- lua/ge/extensions/ui/phone/layout.lua
```

Reason:

- JOB-04 should not override the whole BeamNG Vue UI just to test Scrap Yard backend actions.
- RLS should own its own compiled UI files.
- JOB-04 should stay inside RedFox/IceFox page files and its Scrap Yard test Lua only.

## Files that should remain part of JOB-04 test package

```text
lua/ge/extensions/redfox_scrapyard_webui_test.lua
lua/ge/extensions/redfoxCareerWeb.lua
ui/modModules/redfoxCareerWeb/
sites/scrap_yard/
sites/scrap_yard_webui_test/
assets/
reports: CHANGE_SCOPE, OPEN_THIS_VERIFICATION_REPORT txt/html, VERIFY json, FILE_TREE, FILE_INVENTORY
```

## Hard rules still active

```text
No redfoxScrapYardDirect.
No startup career module.
No map-load parking/shop generation.
No fake money.
No fake garage insert.
No fake storage insert.
No fake ownership.
Runtime success is unproven until David tests in BeamNG.
```

## What is needed next

1. David should remove/disable v0.1.0 from BeamNG mods.
2. JOB-04 should build a patched v0.1.1 without `ui/ui-vue/dist/index.js` after approval.
3. David should test v0.1.1 with RLS installed and only one FoxNet/RedFox ZIP active.
4. David should send `beamng.log` if the title screen or grey screen still fails.
