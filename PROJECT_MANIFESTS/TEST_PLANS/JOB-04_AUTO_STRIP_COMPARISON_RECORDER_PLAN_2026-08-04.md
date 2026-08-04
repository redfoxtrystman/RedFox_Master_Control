# JOB-04 Auto-Strip Comparison Recorder Plan

**Date:** 2026-08-04  
**Tracking:** issue #54

## Goal

Make Auto-Strip Good Parts + Scrap the Remainder testable without requiring David to manually write down or compare a large parts list while tired.

## Safety boundary

The temporary recorder is read-only. It must not:

- remove or install parts;
- change vehicle configuration;
- change money;
- move vehicles between garages;
- create or delete Career inventory records;
- run the Wrecking Yard transaction itself;
- alter stock Career/RLS files.

It only snapshots and compares data already exposed by Career/RLS and JOB-04.

## UI

Temporary app title:

```text
RedFox Salvage Comparison Recorder
```

Controls:

```text
Control Vehicle ID: [select]
Auto-Strip Test Vehicle ID: [select]
[ Capture Both Before ]
[ Capture Control After Manual Strip ]
[ Capture Test After Yard Auto-Strip ]
[ Compare Results ]
[ Export JSON ]
[ Export CSV ]
```

The app should warn when model/config do not match.

## Snapshot fields

- exact Career inventory ID;
- model, configuration, year, mileage;
- current garage/location;
- installed part inventory records;
- containing slot and part name;
- part condition/integrity/odometer when exposed;
- RLS part value;
- whether normalized part name contains `junk`;
- source vehicle ID/location for each returned part;
- unresolved part/slot entries;
- total part counts and values;
- vehicle/RLS reference value;
- JOB-04 chassis/remainder quote;
- daily scrap rate;
- labor charge;
- final JOB-04 payment and transaction ID after the real transaction completes.

## Comparison report

The report must separate:

```text
Matched returned parts
Missing from auto-strip result
Unexpected extra returned parts
Duplicate returned parts
Junk parts correctly retained
Junk parts incorrectly returned
Good parts incorrectly retained
Unresolved slots/parts
Manual-strip total value
Auto-strip returned-part total value
Expected labor difference
Actual cash difference
PASS / WARNING / FAIL
```

## Persistence

Save under a dedicated non-runtime-test folder such as:

```text
settings/redfox/job04_test/auto_strip_comparisons/<comparison_id>.json
settings/redfox/job04_test/auto_strip_comparisons/<comparison_id>.csv
```

The comparison ID should include both inventory IDs and a timestamp/day marker.

## Test workflow

1. Back up Career.
2. Obtain two identical model/config vehicles and claim them into real Career inventory.
3. Capture both before states.
4. Manually strip the control vehicle using normal RLS parts UI.
5. Capture control after state.
6. Run JOB-04 Auto-Strip on the second vehicle.
7. Capture test after state.
8. Compare.
9. Confirm every returned part exists once in RLS parts inventory.
10. Confirm junk/unresolved parts remained with the remainder and contributed value.
11. Confirm vehicle removal/payment occurred once.
12. Restart Career and repeat the comparison read to verify persistence.

## Acceptance

Auto-strip is not accepted merely because the transaction completes. It passes only when the comparison report shows that good returned parts match the manual-strip control within documented mod-vehicle discrepancies, junk parts are retained and valued correctly, no part is duplicated/lost, and the labor-adjusted payout is correct.
