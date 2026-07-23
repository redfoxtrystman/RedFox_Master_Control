# JOB-04 Scrap Yard / Wrecking Yard — v0.1.2 PC/Phone Access Patch Audit

**Date/time label:** 2026-07-22 1225PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Build:** `zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PC_PHONE_ACCESS_2026-07-22_1225PT_v0_1_2_RLS266_UI_COMPAT.zip`  
**Runtime status:** UNPROVEN until David tests in BeamNG.

---

## Why this build exists

David tested:

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_2026-07-22_1045PT_v0_1_1_NO_CORE_UI_OVERRIDE.zip
```

Result:

```text
- Scrap Yard on PC does not work.
- Phone internet / IceFox icon is missing.
```

v0.1.1 removed `ui/ui-vue/dist/index.js` to avoid the title/menu grey-screen failure, but that also removed the earlier phone app manifest/route hook. PC also lacked a proper Angular modModule state registration and garage-computer access button.

---

## Files changed / added in v0.1.2

### Fresh RLS 2.6.6 UI compatibility patch

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
ui/entrypoints/main/tiles/redfox-browser.png
```

Important: this reintroduces `ui/ui-vue/dist/index.js`, but it was rebuilt from the uploaded `rls_career_overhaul_2.6.6(2).zip` file, not from the older RedFox test ZIP that caused the grey screen.

Added phone app manifest:

```text
id: redfox-browser
name: IceFox
route: /career/phone-redfox-browser
iconTile: redfox-browser.png
```

Added phone route:

```text
/career/phone-redfox-browser
```

The route loads:

```text
/ui/modModules/redfoxCareerWeb/phone/index.html
```

### PC Angular state registration

```text
ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js
ui/modModules/redfoxCareerWeb/redfoxCareerWeb.html
ui/modModules/redfoxCareerWeb/redfoxScrapYardTest.html
```

Added PC states:

```text
menu.redfoxCareerWeb
menu.redfoxScrapYardTest
```

`menu.redfoxCareerWeb` loads the IceFox / RedFox web page.  
`menu.redfoxScrapYardTest` loads the Scrap Yard WebUI test panel directly.

### Safe PC access helper

```text
lua/ge/extensions/redfoxCareerWebAccess.lua
scripts/redfox_career_web/modScript.lua
```

This loader only registers PC computer buttons. It does not patch vehicleShopping, inventory, money, garage, storage, map loading, or Scrap Yard stock generation.

Expected PC buttons:

```text
IceFox / RedFox Web
Scrap Yard WebUI Test Panel
```

---

## Hard rules preserved

```text
No redfoxScrapYardDirect.
No startup Scrap Yard career module.
No map-load parking/shop generation.
No West Coast dependency.
No fake money.
No fake storage.
No fake garage insert.
No fake vehicle ownership.
```

This remains an all-map test design.

---

## Static verification performed

```text
ZIP integrity: PASS
ZIP reopened/testzip: PASS
No __pycache__ / .pyc: PASS
No redfoxScrapYardDirect path: PASS
No startup Scrap Yard career module: PASS
Required Scrap Yard WebUI test files present: PASS
Required PC state files present: PASS
Required PC access Lua/modScript present: PASS
Required phone tile/icon file present: PASS
```

Node syntax checks passed for:

```text
ui/ui-vue/dist/index.js
ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard_webui_test/assets/js/scrap_test.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
```

---

## Build checksum

```text
SHA256: 8065f16f570e1d0f1e0f63231b475328e37721922944a2b25f07607448cf8cae
Size: 24,632,115 bytes
```

---

## Test instructions for David

Install only:

```text
RLS Career Overhaul 2.6.6
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PC_PHONE_ACCESS_2026-07-22_1225PT_v0_1_2_RLS266_UI_COMPAT.zip
```

Remove/disable:

```text
old JOB-04 v0.1.0 ZIP
old JOB-04 v0.1.1 ZIP
all other zzzz_RedFox_FoxNet... ZIPs
all RedFox_ScrapYard_Direct... ZIPs
```

Test order:

```text
1. Start BeamNG.
2. Confirm the title/menu/background loads normally.
3. Start Career mode.
4. Check phone for IceFox icon.
5. Check PC/garage computer for IceFox / RedFox Web.
6. Check PC/garage computer for Scrap Yard WebUI Test Panel.
7. Open Scrap Yard WebUI Test Panel.
8. Click Check Status.
9. Click Load RLS Shop Data.
```

Failure report needed:

```text
beamng.log
beamng.1.log if rotated
whether grey screen came back
whether phone icon appeared
whether PC buttons appeared
what map/career save was used
last button clicked before failure
```

---

## Known risk

Because BeamNG/RLS phone app manifests live inside `ui/ui-vue/dist/index.js`, adding the phone icon currently requires a UI compatibility override. This v0.1.2 build uses the fresh RLS 2.6.6 file as the base. If the grey title/menu screen returns, remove this ZIP and treat the UI compatibility override as still unsafe.