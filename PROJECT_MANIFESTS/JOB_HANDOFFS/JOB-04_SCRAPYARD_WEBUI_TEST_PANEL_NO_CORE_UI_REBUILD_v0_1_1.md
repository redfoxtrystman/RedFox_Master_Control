# JOB-04 — Scrap Yard WebUI Test Panel No Core UI Rebuild v0.1.1

**Date:** 2026-07-22  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** Built locally for David to test; runtime unproven until tested in BeamNG.  
**Output ZIP:** `zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_NO_CORE_UI_OVERRIDE_v0_1_1.zip`

---

# Why this rebuild exists

The prior JOB-04 v0.1.0 test ZIP included:

```text
ui/ui-vue/dist/index.js
```

That is a global BeamNG Vue UI bundle. It caused or very likely caused the title/background/UI grey-screen failure David had to spend about 12 hours tracking down.

This v0.1.1 rebuild removes that file from the active package.

---

# Critical verification

```text
Core UI override check:
- ui/ui-vue/dist/index.js present: NO
- Approved core UI build: NO
- Result: PASS

Phone layout override check:
- lua/ge/extensions/ui/phone/layout.lua present: YES
- Approved phone/platform build: NO
- Result: WARN_PRESENT_HIGH_RISK
```

The phone layout file is still present because David asked whether the package includes phone/PC access and does not currently have a separate RedFox access mod installed. This is documented as high risk. If any phone/menu problem remains, the next stricter build must remove that file too and become PC/WebUI-only until JOB-01 owns phone registration.

---

# Static checks run

```text
ZIP reopen/testzip: PASS
Entry count: 931
ui/ui-vue/dist/index.js present: False
lua/ge/extensions/ui/phone/layout.lua present: True
__pycache__ present: False
Scrap Yard WebUI test page present: True
Scrap Yard WebUI Lua present: True
JavaScript syntax checks: PASS
```

Local output SHA256:

```text
6ecfc2dabb9625725dbedfe58ecb5f4cee5053d87f1e49ba6a89f6a116cbb62d
```

---

# What this build is meant to test

- RedFox/IceFox access to Scrap Yard test area.
- Scrap Yard WebUI test panel.
- All-map safe shop-data test.
- Stock RLS/BeamNG vehicle shopping data load.
- Stock purchase menu opening from selected shop listing.
- Owned career inventory vehicle listing.
- Stock inventory sell function call for selected owned vehicle.

---

# What this build does not claim

- Does not prove runtime success.
- Does not add a physical map Scrap Yard.
- Does not require West Coast.
- Does not implement tow-yard delivery.
- Does not implement final website integration.
- Does not fake money/storage/garage/inventory ownership.
- Does not include the banned global BeamNG Vue UI bundle.

---

# David test instructions

1. Remove the old v0.1.0 JOB-04 ZIP.
2. Remove or disable every other `zzzz_RedFox_FoxNet_Web_Ecosystem...` ZIP.
3. Install only this v0.1.1 ZIP plus RLS Career Overhaul.
4. Start BeamNG Career.
5. First confirm the title/background/menu no longer grey-screens.
6. Open RedFox/IceFox if available.
7. Open Scrap Yard.
8. Open the WebUI Test Panel.
9. Run:
   - Check Status
   - Load RLS Shop Data
   - Open Selected Purchase Menu
   - List Owned Career Vehicles
   - Sell only if intentionally selling that selected vehicle.
10. Send back `beamng.log`, `beamng.1.log` if rotated, and `beamng-launcher.log` if the title/menu is still broken.

---

# Next fallback if this still breaks UI

Make a stricter v0.1.2 that also removes:

```text
lua/ge/extensions/ui/phone/layout.lua
```

That version may lose phone icon/access, but it will isolate Scrap Yard WebUI testing from both global UI and global phone layout overrides.
