# JOB-04 Audit — Phone-Only Direction / PC Access Trashed

**Date:** 2026-07-23
**Job:** JOB-04 — Scrap Yard / Wrecking Yard
**Status:** Direction changed by David / Captain
**This is not a handoff.** This is a current design-direction audit so the next JOB-04 work does not repeat the failed PC/phone parity path.

## User decision
David decided that JOB-04 should stop trying to make Scrap Yard work through both PC and phone right now.

New direction:

```text
Trash PC access for Scrap Yard for now.
Use Scrap Yard only through the phone.
Revert to the full working version line.
Do not keep forcing PC route parity.
```

## Why this change was made
Recent test history showed:

- A prior phone-working line could open the Scrap Yard flow and buy vehicles.
- v0.1.4 / rollback line proved that David could buy a Mustang through the Scrap Yard flow.
- The PC/phone parity attempt in v0.1.5 broke both phone and PC loading.
- PC and phone access wrappers are not equivalent. Mirroring page files is not enough because PC and phone enter the site through different wrappers/routes.
- Trying to keep PC access working at the same time is causing repeated regressions.

## Known working / partially working references

### Proven buy-working line

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PHONE_PC_BRIDGE_2026-07-22_2222PT_v0_1_4_FROM_PHONE_WORKING_CURRENT_RLS_UI.zip
```

David reported that this line worked enough to:

```text
- load Scrap Yard
- open the buy flow
- buy a Mustang
```

Problem: it is very slow when opening/changing pages.

### Rollback copy of that line

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
```

Purpose: clearer dated rollback name for the v0.1.4 buy-working line.

### Possible fast phone base

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_9_9_PHONE_SCRAP_OPTIMIZED.zip
```

This is suspected to be the faster phone/Scrap baseline, but it may not include the exact proven buy path from v0.1.4/v0.1.6.

## Failed line to avoid

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PERFORMANCE_PC_PHONE_PARITY_2026-07-23_1433PT_v0_1_5.zip
```

David reported that this line broke both phone and PC access. Do not use it as the next base.

## New JOB-04 rule

JOB-04 must not chase PC access right now.

Allowed for next patch:

```text
- phone-only Scrap Yard access
- keep / restore the phone route that already worked
- preserve the proven buy path
- improve phone-only speed/loading behavior
- avoid changing PC wrapper/garage computer route
```

Not allowed unless David explicitly reverses this decision:

```text
- PC/phone parity patch
- PC Scrap Yard wrapper rewrite
- PC route registration work
- mirroring PC and phone wrappers
- replacing working phone path for a cleaner shared path
```

## Next recommended build

```text
v0.1.7 PHONE_ONLY_FAST_BASE_WITH_PROVEN_BUY_PATH
```

Recommended approach:

```text
1. Start from the last phone-working/fast baseline if inspection confirms it is safe.
2. Pull in only the proven buy path from v0.1.4/v0.1.6.
3. Do not modify PC access.
4. Do not modify more of ui/ui-vue/dist/index.js than already required by the working phone path.
5. Make page load draw immediately, then refresh vehicle stock only on button click.
6. Keep runtime behavior labeled unproven until David tests in BeamNG.
```

## Current install recommendation

For immediate use/testing, David should revert to the rollback of the v0.1.4 working line:

```text
RLS Career Overhaul 2.6.6
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
```

Remove/disable:

```text
v0.1.5 performance parity build
old v0.1.0-v0.1.4 duplicate JOB-04 zips, unless testing one exact known file
all other zzzz_RedFox_FoxNet... zips
all RedFox_ScrapYard_Direct... zips
```
