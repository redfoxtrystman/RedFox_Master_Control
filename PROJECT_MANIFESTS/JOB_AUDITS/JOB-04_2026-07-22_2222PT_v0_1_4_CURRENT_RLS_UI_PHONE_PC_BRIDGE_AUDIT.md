# JOB-04 Scrap Yard / Wrecking Yard — v0.1.4 Current RLS UI Phone + PC Bridge Audit

**Date/time:** 2026-07-22 2222PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** Build created, runtime unproven until David tests in BeamNG.

## Trigger

David tested the prior JOB-04 builds and reported:

- v0.1.3 broke BeamNG UI/loading/title background into grey screen behavior.
- PC Scrap Yard still did not receive RLS/BeamNG shop data.
- Phone RedFox/IceFox icon was missing in some newer builds.
- David uploaded the known phone-working but PC-broken baseline:
  `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_2_PC_DIRECT_BRIDGE_FIX PHONE WORKS BUT NO PC.zip`

David correctly pointed out that the old phone-working path needed to be duplicated instead of continuing to drift across branches.

## Root cause conclusion

The phone-working branch depends on a patched BeamNG/RLS Vue UI file:

```text
ui/ui-vue/dist/index.js
```

That file registers the phone app and the phone route:

```text
redfox-browser
/career/phone-redfox-browser
redfox-phone-browser-frame
```

The failed v0.1.3 reused the old phone-working `index.js` directly. That restored the phone route, but it also reintroduced an older full core UI override. That is the likely reason BeamNG's loading/title/main UI went grey.

Online BeamNG references also point toward this being a core UI mod problem:

- BeamNG support says UI loading problems can be caused by mods.
- BeamNG forum material identifies `ui/ui-vue/dist/index.js` as part of the main menu/background UI area.
- BeamNG loading screens are also connected to `ui/modules/loading`, so future RedFox builds must not override that area unless intentionally building a loading-screen mod.

## Build strategy for v0.1.4

Do **not** use the old whole RedFox `ui/ui-vue/dist/index.js` anymore.

Instead:

1. Start from the v0.10.3.3 PC mirror-phone relay build, because it has the PC bridge scripts that mirror the phone behavior.
2. Replace `ui/ui-vue/dist/index.js` with the current RLS Career Overhaul 2.6.6 UI file.
3. Patch only the RedFox phone browser manifest and route component into that current RLS file.
4. Add the matching current RLS `ui/ui-vue/dist/index.css` so JS and CSS are paired.
5. Keep the phone layout and browser page from the phone-working branch.
6. Keep the v0.10.3.3 PC mirror-phone relay scripts.
7. Do not add or restore any loading-screen override.

## New build

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PHONE_PC_BRIDGE_2026-07-22_2222PT_v0_1_4_FROM_PHONE_WORKING_CURRENT_RLS_UI.zip
```

## Baseline and sources

```text
Base ZIP:
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_3_PC_MIRROR_PHONE_RELAY_FIX.zip

Uploaded phone-working reference:
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_2_PC_DIRECT_BRIDGE_FIX PHONE WORKS BUT NO PC.zip

Current RLS UI source:
rls_career_overhaul_2.6.6(2).zip
```

## Files intentionally changed / replaced

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
```

## Key preserved files

```text
lua/ge/extensions/ui/phone/layout.lua
ui/modModules/redfoxCareerWeb/phone/browser_home.html
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/assets/js/scrap.js
```

## Static checks

```text
ZIP integrity: PASS
ZIP reopened/testzip: PASS
Entry count: 939
Size: 24,742,835 bytes
SHA256: e6690693000c176d874f72abf3ffbe60d86815713a7ea65dbd0a1c84ece9fbb0
ui/ui-vue/dist/index.js present: PASS
ui/ui-vue/dist/index.css present: PASS
RedFox phone manifest present: PASS
RedFox phone route present: PASS
redfox-phone-browser-frame present: PASS
No ui/modules/loading override: PASS
No redfoxScrapYardDirect: PASS
No startup Scrap Yard career module: PASS
Phone layout present: PASS
Phone browser page present: PASS
PC front scripts present: PASS
Scrap Yard page present: PASS
Relevant JavaScript syntax checks: PASS
```

## Required install rules for David

Only install:

```text
RLS Career Overhaul 2.6.6
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PHONE_PC_BRIDGE_2026-07-22_2222PT_v0_1_4_FROM_PHONE_WORKING_CURRENT_RLS_UI.zip
```

Remove/disable:

```text
old JOB-04 v0.1.0
old JOB-04 v0.1.1
old JOB-04 v0.1.2
old JOB-04 v0.1.3
all other zzzz_RedFox_FoxNet... zips
all RedFox_ScrapYard_Direct... zips
```

## Test order

1. Start BeamNG.
2. Confirm the loading/title/menu background does not stay grey.
3. Enter Career mode.
4. Check phone for FoxNet Browser / IceFox / RedFox browser app.
5. Open PC IceFox / FoxNet.
6. Open Scrap Yard.
7. Click Refresh Yard List.
8. If it still fails, send `beamng.log` and the last button/path tested.

## Runtime status

Unproven until David tests this exact ZIP in BeamNG.

## Stop condition

If this build still greys out BeamNG UI, immediately remove it and do not continue patching `ui/ui-vue/dist/index.js` inside JOB-04. That would mean JOB-01/JOB-02 must own the phone/PC platform patch and JOB-04 should only own the Scrap Yard site files.
