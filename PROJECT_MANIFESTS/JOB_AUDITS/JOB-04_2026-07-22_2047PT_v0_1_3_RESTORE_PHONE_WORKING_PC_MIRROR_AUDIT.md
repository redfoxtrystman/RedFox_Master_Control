# JOB-04 — Scrap Yard / Wrecking Yard
# Build Audit — 2026-07-22 2047PT — v0.1.3

## Status

This is a corrective build after David reported:

- Scrap Yard on PC still does not load RLS/BeamNG shop vehicles.
- Phone IceFox / internet icon is not showing.
- The older branch had worked on phone, including buying vehicles, but not PC.

This audit is not a handoff. JOB-04 stays in this chat.

## Build file

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_RESTORE_PHONE_PC_2026-07-22_2047PT_v0_1_3_FROM_PHONE_WORKING_BASELINE.zip
```

## SHA256

```text
8d32fc116aabf04e1de78468f9325e7031f042f46ac5e0c5238011c819c23e6c
```

## Baseline used

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_3_PC_MIRROR_PHONE_RELAY_FIX.zip
```

Reason: this line was built from the phone-working Scrap Yard branch and already contains the PC mirror-phone relay patch. The v0.1.1/v0.1.2 emergency branch is abandoned for now because it removed or replaced the known working phone bridge/UI path.

## What this build is supposed to do

- Restore the phone IceFox app/icon route from the phone-working line.
- Keep the Scrap Yard page that asks for `RedFoxRequestCareerData`.
- Keep the known `ui/ui-vue/dist/index.js` direct vehicleShopping bridge from v0.10.3.1/v0.10.3.3.
- Keep the PC mirror relay in both PC IceFox front scripts.
- Make the PC Scrap Yard page ask for the same RLS/BeamNG vehicleShopping data the phone page used.
- Keep stock purchase flow using `career_modules_vehicleShopping.openPurchaseMenu("instant", shopId)`.

## Important code markers preserved

```text
redfoxDirectVehicleShoppingPatchV01031
__redfoxPcMirrorPhoneRelay1033
__redfoxPhoneCareerRelay097
RedFoxRequestCareerData
RedFoxScrapYardOpenPurchaseMenu
redfox-browser
```

## Key files present

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
ui/modModules/redfoxCareerWeb/phone/index.html
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
sites/scrap_yard/index.html
sites/scrap_yard/assets/js/scrap.js
```

## Static checks run

```text
ZIP integrity: PASS
Entry count: 1385
Size: 24,684,005 bytes
No redfoxScrapYardDirect files: PASS
No startup Scrap Yard career module: PASS
Phone layout present: PASS
Phone browser present: PASS
UI Vue direct bridge present: PASS
PC mirror relay present in both PC scripts: PASS
Phone relay present: PASS
Scrap Yard request message present: PASS
Purchase request message present: PASS
No __pycache__ / .pyc: PASS
Relevant JavaScript syntax checks: PASS
```

## What this build does not do

- Does not create `redfoxScrapYardDirect`.
- Does not add a startup Scrap Yard career module.
- Does not generate parking spots at map load.
- Does not fake money.
- Does not fake garage/storage/inventory.
- Does not manually create ownership.
- Does not depend on West Coast. It is intended for all maps.

## Install rule for David

Only install this one FoxNet/RedFox web ZIP at a time.

Remove or disable:

```text
old JOB-04 v0.1.0/v0.1.1/v0.1.2 zips
old zzzz_RedFox_FoxNet_Web_Ecosystem zips
RedFox_ScrapYard_Direct_v0_1_0.zip
RedFox_ScrapYard_Direct_v0_1_1_ONLINE_ONLY_SAFE.zip
RedFox_ScrapYard_Direct_v0_1_2_NO_EARLY_DEP_SAFE_TEST.zip
```

The latest log available during this work still showed an old `RedFox_ScrapYard_Direct_v0_1_0.zip` mounted from `/mods/Career_redfox/`. That mod is banned for this job because previous testing showed it caused dependency/load/freezing problems.

## Test order

1. Install RLS Career Overhaul 2.6.6.
2. Install this exact JOB-04 v0.1.3 ZIP.
3. Start BeamNG and confirm no grey screen/title background failure.
4. Enter Career mode.
5. Check phone for IceFox app/icon.
6. Open PC IceFox / RedFox web.
7. Open Scrap Yard.
8. Click Refresh Yard List.
9. If still no cars, send `beamng.log`, `beamng.1.log`, screenshot, and a list/screenshot of installed FoxNet/ScrapYard ZIPs.

## Runtime status

UNPROVEN until David tests this exact ZIP in BeamNG.

## Known risk

This build includes `ui/ui-vue/dist/index.js` because that is where the known phone-working bridge lived. Removing that file stopped the grey-screen risk but also removed the phone entry/bridge. This v0.1.3 prioritizes restoring the known phone-working route and PC parity.

If the grey screen returns, stop testing and remove this ZIP.
