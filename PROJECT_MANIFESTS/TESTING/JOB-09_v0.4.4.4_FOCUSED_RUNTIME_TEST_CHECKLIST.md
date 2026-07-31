# JOB-09 v0.4.4.4 Focused Runtime Test Checklist

Use only:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_4_ActiveCallPerformanceEmergencyFilterSameYardClaimRuntimeSlim.zip`

SHA-256:

`61b1ef9e746f5978bba2cd7e7a4368aef4c19d2fe17f6c1207142d4fd3a4f6ad`

## Before loading

1. Back up the current Career save.
2. Back up `settings/redfox/`.
3. Disable or remove every older JOB-09 ZIP, including v0.4.4.3.
4. Install only the exact v0.4.4.4 ZIP above.
5. Fully restart BeamNG.
6. Do not delete existing tow-yard data or unfinished-job recovery data before the first load.

## Test 1 — clean load and preservation

- Confirm JOB-09 shows v0.4.4.4.
- Confirm existing tow yards, custody records, company/shop records, fleet records, history and settings still appear.
- Confirm no Lua error appears during Career load.

Stop and return `beamng.log` if data is missing or duplicated.

## Test 2 — active-call freeze/stutter

1. Close other RedFox apps where practical.
2. Start one ordinary Standard Car Tow.
3. Drive normally to the target.
4. Tow it normally for at least two minutes before drop-off.
5. Note whether the former repeating multi-second freeze returns.
6. Complete drop-off.

Record:

- whether freezing occurred;
- approximate interval between freezes;
- whether the tow window was open or closed;
- whether the call came from procedural dispatch, a saved scene or Random Events;
- whether the freeze stopped at drop-off.

If freezing remains, preserve the log immediately before starting another call.

## Test 3 — abandoned emergency filter

Run at least ten Abandoned Vehicle calls, or as many as practical.

Expected:

- no police vehicle;
- no sheriff/highway-patrol vehicle;
- no fire-department/fire-service vehicle;
- no ambulance/EMS vehicle;
- no emergency vehicle enters custody or private lien processing.

Record the target model/configuration names in order if any emergency configuration appears.

## Test 4 — normal vehicle variety

Run several ordinary Standard Tow and Rolled Car Recovery calls.

Expected:

- civilian vehicles remain the overwhelming majority;
- fire/police/EMS do not repeat in a streak;
- an emergency vehicle may appear rarely as a legitimate agency-paid breakdown/accident recovery;
- an emergency target must show government/emergency-services agency payment;
- an emergency target must never become random private payer-default/lien property.

## Test 5 — ordinary paid tow

Complete a normal civilian tow.

Expected:

- payment occurs exactly once;
- history records the job once;
- no custody record is created;
- no vehicle duplicates.

## Test 6 — payer default and lien routing

Use the existing test control for the next unpaid/default call where available, or continue testing until a default occurs.

Expected for a lienable civilian vehicle:

- no immediate payment;
- exact vehicle enters the selected yard's custody storage;
- existing three-day owner-search/lien process begins;
- one custody record only.

Expected for non-lienable equipment/attachment:

- found-property/no-title closure;
- no normal vehicle lien record.

## Test 7 — same-yard lien claim

Use an eligible custody vehicle after the lien period.

Expected:

- no message requiring a personal purchased garage;
- charge occurs once;
- exact custody record disappears once;
- exact vehicle appears once in the same yard's company/shop storage;
- model, configuration, damage/condition, value and history remain;
- no Career inventory vehicle is created during claim.

Save/reload and confirm the result persists.

## Test 8 — optional personal garage transfer

Only after Test 7 passes:

- use Send to Personal/RLS Garage on a noncritical shop vehicle;
- confirm this separate action requires a valid purchased garage;
- confirm exactly one Career inventory ID is created and placed;
- confirm the shop record is removed only after verified placement.

Stop immediately on duplicate, missing vehicle or lost money.

## Test 9 — Random Events

Test at least:

- Flat Tire or Stalled Vehicle;
- Multi-Car Crash;
- Police Traffic-Stop Impound;
- one scene that previously favored a tunnel.

Expected:

- most calls pay normally;
- minority default remains possible for civilian lienable targets;
- tunnels are rerolled/rejected by default;
- police/fire/EMS support remains support rather than abandoned private property;
- no Random Events source cleanup regression.

## Known deferred issue

The unfinished-job prompt may still fail to reconstruct and resume the scene after a crash. Use Abandon Saved Job if necessary. Do not classify that as a new v0.4.4.4 regression unless its behavior becomes worse than v0.4.4.3.

## Evidence to return on failure

- screenshot;
- exact call type and source;
- target model/configuration;
- approximate time of failure;
- whether the tow window and Tow Portal were open;
- latest `beamng.log`;
- money before/after for transaction failures;
- custody/shop record counts before/after for duplication or loss.