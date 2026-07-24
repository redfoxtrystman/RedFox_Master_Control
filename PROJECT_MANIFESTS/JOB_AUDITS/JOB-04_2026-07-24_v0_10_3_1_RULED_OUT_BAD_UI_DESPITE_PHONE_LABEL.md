# JOB-04 — v0.10.3.1 Ruled Out As Baseline Despite “Phone Works” Label

**Date:** 2026-07-24
**Job:** JOB-04 — Scrap Yard / Wrecking Yard
**Status:** Correction / baseline candidate rejected

## Correction

David clarified that the uploaded file:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works(2).zip
```

is **not** a usable baseline even though the name/report suggests phone-only worked.

Reason:

```text
It has the bad UI behavior where BeamNG loading/title/background becomes grey.
```

## Static inspection result

The ZIP does contain the phone files and Scrap Yard files, but it also contains the risky BeamNG core UI override:

```text
ui/ui-vue/dist/index.js
```

Observed SHA256 for that file:

```text
1f700638131de1a5471d303cf69fd3829e32acbfca74f5e05740ca45e27857e7
```

This matches the already-known bad UI override family that was associated with grey loading/title screen problems.

## Important interpretation

A filename/report saying “phone works” only proves that the phone route/icon may exist in that package. It does **not** prove the package is safe for BeamNG’s current UI runtime.

For JOB-04 baseline decisions:

```text
v0.10.3.1 phone-only works candidate = REJECTED
Reason = bad grey-screen UI override
```

## Current baseline search status

Known facts now:

```text
v0.1.5 = broken, do not use
v0.1.6 rollback copy = not trusted / likely wrong target
v0.10.3.1 phone-only candidate = rejected because bad UI grey screen
v0.9.9 PHONE_SCRAP_OPTIMIZED = possible fast baseline candidate, not yet confirmed as buy-working
v0.1.4 = buy flow worked but was very slow
```

## Next safe direction

Do not build from v0.10.3.1.

Next work should either:

1. Identify the true fast phone-working baseline by testing older packages one at a time, or
2. Build from a fast phone baseline that does **not** include the bad UI override, then add only the proven Scrap Yard buy path.

Do not touch PC access for now. JOB-04 direction remains phone-only until David changes it.