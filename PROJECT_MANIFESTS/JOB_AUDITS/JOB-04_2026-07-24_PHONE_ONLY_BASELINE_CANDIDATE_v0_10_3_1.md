# JOB-04 Audit — Phone-Only Baseline Candidate v0.10.3.1

**Date:** 2026-07-24
**Job:** JOB-04 — Scrap Yard / Wrecking Yard
**Status:** Open / baseline candidate identified

## User correction
David reported that the previously linked rollback copy was broken and uploaded this file as the likely correct phone-working baseline:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works(2).zip
```

## Inspection result
The uploaded ZIP was inspected directly from the sandbox path.

```text
ZIP integrity: PASS
Entry count: 1371
Size: 24,441,941 bytes
```

## Important contents found

```text
ui/ui-vue/dist/index.js: present
lua/ge/extensions/ui/phone/layout.lua: present
ui/modModules/redfoxCareerWeb/phone/index.html: present
ui/modModules/redfoxCareerWeb/phone/browser_home.html: present
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js: present
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html: present
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js: present
sites/scrap_yard/index.html: present
sites/scrap_yard/assets/js/scrap.js: present
```

## Safety checks

```text
lua/ge/extensions/redfoxScrapYardDirect.lua: absent
scripts/redfoxScrapYardDirect/modScript.lua: absent
redfoxScrapYardDirect marker: absent
```

This candidate does not contain the banned standalone Scrap Yard Direct startup module.

## Important warning
This candidate still contains the broad BeamNG/RLS UI file:

```text
ui/ui-vue/dist/index.js
```

It also includes RedFox phone/browser route markers:

```text
phone-redfox-browser
redfox_browser_default
redfoxDirectVehicleShoppingPatchV01031
```

The file hash observed for `ui/ui-vue/dist/index.js` matches the previously identified broad UI override hash:

```text
1f700638131de1a5471d303cf69fd3829e32acbfca74f5e05740ca45e27857e7
```

Therefore this file may be required for the old phone path to appear, but it is also the dangerous area that can break BeamNG's main UI/loading/title background if mismatched.

## Current direction
Use this as the candidate to compare against the known buy-working v0.1.4/v0.1.6 line and the fast v0.9.9 line.

Do not build a new version until the exact baseline choice is confirmed.

Planned next approach, if approved:

```text
v0.1.7 PHONE-ONLY BASELINE TEST
- start from this uploaded v0.10.3.1 phone-working candidate
- do not add PC access
- do not add PC parity changes
- do not touch/broaden wrappers
- only rename/package with date/time and reports if David wants a clean tracked copy
```

## Runtime status
Runtime behavior of this uploaded candidate is not proven in the current session. It is only statically inspected.
