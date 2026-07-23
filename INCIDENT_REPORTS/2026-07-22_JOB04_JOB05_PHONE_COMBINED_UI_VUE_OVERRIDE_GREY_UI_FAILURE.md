# JOB-04 / JOB-05 combined phone test — BeamNG UI override failure

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Status:** FAILED — STOPPED  
**Failed build:** `zzzz_RedFox_FoxNet_JOB04_ScrapYard_JOB05_BeamBook_PHONE_LIVE_v0_3_0_RUNTIME_UNTESTED.zip`

## Runtime symptom

David reported that enabling the combined phone test broke the BeamNG user interface: loading images and the loading screen remained grey. Disabling the ZIP removed the active test target.

## Exact cause found

The ZIP contained this game-owned compiled UI path:

```text
ui/ui-vue/dist/index.js
```

File identity in the failed ZIP:

- Size: 4,457,903 bytes
- SHA-256: `1f700638131de1a5471d303cf69fd3829e32acbfca74f5e05740ca45e27857e7`

This is not an isolated RedFox website file. It is a complete compiled BeamNG Vue UI bundle. The old FoxNet/RLS experiments patched this file to add the `redfox-browser` phone manifest, phone route, direct Career data calls, and stock purchase handling. Replacing a current BeamNG compiled UI bundle with an older patched bundle can break unrelated UI, loading screens, loading images, menus, and routes after game updates.

The project history itself confirms the prior method required a full restart because it changed `ui/ui-vue/dist/index.js`. That method is no longer accepted for JOB-05 builds.

## Additional audit correction

The failed combined ZIP was not a website-only replacement. Compared with the supplied phone-working reference ZIP, it had:

- 113 added files
- 35 removed files
- 28 changed files

Changes included Scrap Yard files, `info.json`, and `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`. Therefore the previous claim that only two mirrored BeamBook website folders changed was incorrect.

## New hard rule

JOB-05 must not package or replace:

```text
ui/ui-vue/dist/index.js
```

JOB-05 must also not ship any complete compiled BeamNG/RLS UI bundle. Phone integration must wait for a supported current-version extension/registry path or be built from the exact current platform source under JOB-01 ownership.

## Safe replacement built

```text
RedFox_BeamBook_Direct_UI_200_Realistic_v0_3_1_RUNTIME_UNTESTED.zip
```

- SHA-256: `88dd4b6897da0b1648274209a4587f7d6ae242f251b3a1954526aa1d661a42ed`
- Files: 71
- ZIP integrity: PASS
- JavaScript syntax: PASS
- JSON validation: PASS
- Fallback listings: 200
- `ui/ui-vue/` files: 0
- Runtime: UNTESTED

The replacement is a standard isolated BeamNG UI App. It renders BeamBook directly without an iframe relay, requests live Career listings through its own lazy-loaded JOB-05 extension, and does not modify the phone, PC, Scrap Yard, global shopping functions, or compiled BeamNG UI.

## Required cleanup and test

1. Disable/remove the failed combined ZIP.
2. Clear BeamNG cache through Launcher > Support Tools because the compiled Vue override may remain cached.
3. Fully restart BeamNG.
4. Confirm the normal loading screen and UI recover before enabling any RedFox test ZIP.
5. Test the direct BeamBook UI App by itself.
6. Do not resume phone integration from the failed compiled-bundle method.
