# JOB-04 Audit — v0.2.1 Rollback: v0.2.0 First Bad Stock Loading

**Date:** 2026-07-25 1246PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Filed by:** Sol / ChatGPT

## Runtime Report From David

David tested:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_0929PT_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK_FROM_v0_1_9.zip
```

David reported that v0.2.0 is broken:

```text
Whatever you did in this last patch broke it.
Now they don't auto-spawn at all, and it still takes time to get into this part.
So it is not linked to the current RLS, shops, and marketplace how they list their cars.
Even when clicking refresh, it does not pull up cars.
So this patch is foobar and we need to roll back.
```

## Classification

```text
v0.2.0 = FIRST BAD for Scrap Yard stock loading / listing population
v0.1.9 = rollback baseline / last pre-v0.2.0 package
v0.2.1 = exact rollback package to v0.1.9 bytes
```

## Rollback Package Created

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-25_1246PT_v0_2_1_ROLLBACK_TO_v0_1_9_LAST_STOCK_LOADING.zip
```

This rollback ZIP is an exact byte-for-byte copy of:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-24_2141PT_v0_1_9_REMOVE_UNAPPROVED_WARNINGS_ONLY_FROM_v0_1_8.zip
```

No files inside the rollback mod ZIP were edited.

## Verification

```text
v0.1.9 source ZIP integrity: PASS
v0.2.0 broken ZIP integrity: PASS
v0.2.1 rollback ZIP integrity: PASS
v0.1.9 entry count: 927
v0.2.0 entry count: 932
v0.2.1 entry count: 927
v0.1.9 SHA256: 6aca6905fb6a7099d9445276c60378891d01fb266aeac533555e0ddd51306d8f
v0.2.1 SHA256: 6aca6905fb6a7099d9445276c60378891d01fb266aeac533555e0ddd51306d8f
Rollback exact same bytes as v0.1.9: PASS
```

## Files Changed In Broken v0.2.0 Compared To v0.1.9

```text
modified: assets/js/icefox_front.js
modified: sites/scrap_yard/assets/css/scrap.css
modified: sites/scrap_yard/assets/js/scrap.js
modified: ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
modified: ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
modified: ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
modified: ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
modified: ui/ui-vue/dist/index.js
added: docs/job04/FILE_TREE_JOB-04_v0_2_0.txt
added: docs/job04/OPEN_THIS_VERIFICATION_REPORT_JOB-04_ScrapYard-WreckingYard_2026-07-25_0929PT_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK.html
added: docs/job04/OPEN_THIS_VERIFICATION_REPORT_JOB-04_ScrapYard-WreckingYard_2026-07-25_0929PT_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK.txt
added: docs/job04/VERIFY_JOB-04_v0_2_0_RLS_FAST_LOAD_FULL_CAR_IMAGES_SPAM_CHECK.json
added: docs/job04/VERIFY_JOB-04_v0_2_0_checks.csv
```

## Cause Direction / Next Rule

The v0.2.0 attempt changed the shop-data request and refresh path too broadly. It broke listing population. Do not reuse the v0.2.0 fast-load logic as-is.

Next corrected attempt must:

```text
1. Start from v0.1.9 / v0.2.1 rollback, not v0.2.0.
2. Keep the old listing/load path intact unless inspection proves the exact safe edit.
3. Fix image cropping separately first if needed.
4. Do not modify ui/ui-vue/dist/index.js unless absolutely proven necessary.
5. Do not remove the working auto-spawn/listing behavior during testing.
6. Do not add Fords as filler/static fake listings.
7. Do not add warnings.
8. Do not add regional import, refresh limits, timers, or sell/scrap work until buy/listing works again.
```

## Status

```text
Rollback built.
v0.2.0 marked broken.
Next work must be inspect-only before any new fix attempt.
```
