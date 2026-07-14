# JOB-12 Standalone Sponsor System Test Build v0.5.0

**Status:** BUILT FOR DAVID RUNTIME TEST — NOT FINAL ICEFOX INTEGRATION  
**Date:** 2026-07-13  
**Job:** JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards

## Purpose

This build implements the approved intermediate standalone WebUI test harness. It allows JOB-12 sponsor UI/state/backend behavior to be tested without touching the shared IceFox/FoxNet phone or PC platform.

## ZIP

```text
RedFox_SponsorSystem_Standalone_Test_v0_5_0.zip
```

The ZIP is delivered directly in the JOB-12 chat. GitHub records the build contract and verification; it does not claim BeamNG runtime success before David tests it.

## Included

```text
lua/ge/extensions/redfox_sponsorSystemTest.lua
scripts/RedFox_Sponsor_System/modScript.lua
ui/modules/apps/RedFoxSponsorSystemTest/app.js
ui/modules/apps/RedFoxSponsorSystemTest/app.json
mod_info/REDFOXSPONSORTEST/info.json
README.txt
_redfox_verification/VERIFICATION_REPORT.txt
_redfox_verification/VERIFICATION_REPORT.html
```

## Test route

```text
BeamNG UI Apps → RedFox Sponsor System Test
```

## Implemented test loop

1. Open SponsorHub tab.
2. Apply/subscribe to the BeamNG GmbH Community Driver Test Program.
3. Automatic test approval creates an offer.
4. FoxMail receives formal messages.
5. FoxText receives short alerts.
6. Accept or decline the offer exactly once.
7. Acceptance grants status, Sponsor XP, reputation, and Sponsor Points.
8. State is written to a Sponsor-owned settings JSON file.
9. One test vehicle can record the optional decal honor toggle.
10. Developer tools can reset/reload state and add small status/pending-wallet test values.

## Intentionally disabled / pending

- No Career money deposit.
- No phone or PC registration.
- No FoxNet/IceFox platform files.
- No RLS edits.
- No Career startup module.
- No BeamHesi/drift reward hooks in this clean test build yet.

Those integrations wait for JOB-01 and JOB-02 contracts. The standalone UI/state/backend should remain reusable; final integration should replace only adapters/manifests.

## Protected-file verification

Confirmed absent from the ZIP:

- phone shell
- PC shell
- IceFox/FoxNet browser core
- shared navigation
- shared registry implementation
- RLS files
- Career startup modules
- vehicle shopping/inventory/garage/storage code
- FoxFax or other app-owned pages

## Static verification completed

- JavaScript syntax check passed with Node.
- JSON parsing passed.
- Expected Lua exports were confirmed present.
- Protected path scan passed.
- ZIP integrity test passed.

## Runtime status

**UNPROVEN until David tests it in BeamNG.**

Required first report:

- Does the UI App appear?
- Does the backend load?
- Does Apply create the offer and messages?
- Does Accept update status once?
- Does state persist after restart?
- Any `RedFoxSponsorTest` errors in `beamng.log`?
