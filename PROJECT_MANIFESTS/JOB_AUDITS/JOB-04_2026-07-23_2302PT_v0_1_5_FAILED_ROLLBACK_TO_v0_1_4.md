# JOB-04 Scrap Yard / Wrecking Yard — v0.1.5 Failure and v0.1.6 Rollback

**Date/time:** 2026-07-23 2302 PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Status:** v0.1.5 failed runtime. Roll back to v0.1.4 behavior.

---

## User runtime result

David reported that the v0.1.5 performance + PC/phone parity build broke both access paths:

```text
Phone: does not load
PC: does not load
Phone still takes a long time to enter
```

This invalidates v0.1.5 as the active test build.

---

## Last known working runtime build

The last known JOB-04 runtime build with proven positive behavior is:

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_PHONE_PC_BRIDGE_2026-07-22_2222PT_v0_1_4_FROM_PHONE_WORKING_CURRENT_RLS_UI.zip
```

User-proven behavior from v0.1.4:

```text
Game loads enough to test
Scrap Yard opens
Buy flow opens
User bought a Mustang
```

Known v0.1.4 issue:

```text
Very slow page switching / white or grey hang up to ~30 seconds
Sell flow not tested
Seller patience may not decrement, likely RLS/session behavior or wrong listing mode, not current priority
```

---

## Rollback file created

A new rollback package was created as an exact byte-for-byte copy of the v0.1.4 working build, only renamed for tracking:

```text
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
```

This is intentionally **not** a new feature build. It is a named rollback to the build where buying worked.

---

## Static verification

```text
ZIP integrity: PASS
Exact copy of v0.1.4 source ZIP: PASS
Entry count: 939
Size: 24,742,835 bytes
SHA256: e6690693000c176d874f72abf3ffbe60d86815713a7ea65dbd0a1c84ece9fbb0
No redfoxScrapYardDirect: PASS
No __pycache__ / .pyc: PASS
Phone layout present: PASS
Scrap Yard UI page present: PASS
Scrap Yard root page present: PASS
Core UI file present: YES — inherited from v0.1.4 working build
```

The core UI file remains because v0.1.4 was the build that restored the phone/PC path and allowed buying. Future speed work must not be done by blind replacement.

---

## Active recommendation

Use v0.1.6 rollback for further testing until a careful inspect-only diff identifies exactly why v0.1.5 broke access.

Install only:

```text
RLS Career Overhaul 2.6.6
zzzz_RedFox_FoxNet_JOB04_SCRAPYARD_ROLLBACK_2026-07-23_2302PT_v0_1_6_EXACT_v0_1_4_BUY_WORKS.zip
```

Remove/disable:

```text
v0.1.5
v0.1.4 if using v0.1.6 rollback name
all older JOB-04 test zips
all other zzzz_RedFox_FoxNet... zips
all RedFox_ScrapYard_Direct... zips
```

---

## Next development rule

Do not make another performance patch by rewriting or mirroring files blindly.

Next step must be inspect-only:

```text
Compare v0.1.4 working vs v0.1.5 broken
Identify exact files changed
Identify why phone and PC access disappeared
Patch one small thing at a time
Keep buy path untouched
```

Potential safer speed fixes after diff:

```text
Only change Scrap Yard page JS after paint
Do not touch route registration
Do not touch phone icon registration
Do not touch ui-vue/dist/index.js unless absolutely required and reviewed
Do not replace working PC/phone shell behavior
```
