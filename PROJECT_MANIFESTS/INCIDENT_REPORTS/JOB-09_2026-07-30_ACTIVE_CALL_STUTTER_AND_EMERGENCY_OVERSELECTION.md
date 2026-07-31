# JOB-09 Incident Report — Active-Call Stutter and Emergency-Vehicle Overselection

**Date:** 2026-07-30  
**Reported by:** David / Captain  
**Affected tested build:** JOB-09 v0.4.4.3  
**Repair candidate:** JOB-09 v0.4.4.4  
**Severity:** High gameplay-performance defect plus medium dispatch-realism/ownership defect

## Incident A — active-call freeze/stutter

### Runtime evidence

David reported that while a tow call was active, the game repeatedly froze for several seconds, briefly resumed, and froze again. After teleporting/flying the target to the destination and completing drop-off, the freezing stopped.

This strongly localizes the problem to logic entered only while an active JOB-09 call exists. It does not prove one specific operation was the sole cause.

### Confirmed recurring active-call work in v0.4.4.3

Source review found:

1. route and marker path reconstruction every eight seconds during an active call;
2. a complete active-job recovery snapshot and JSON write every ten seconds;
3. periodic snapshot work resolving the tow truck through Career inventory scanning;
4. repeated support-item identity resolution during snapshots;
5. every imported Random Events active scene entering the bridge update every frame, even when the scene did not require continued ticking.

These operations stop or become inactive when the call completes, matching the reported timing.

### v0.4.4.4 correction

- route/marker work is phase and movement driven;
- static delivery routes are not periodically rebuilt;
- pickup route refresh requires elapsed time and meaningful movement;
- active-job checkpoint default is 30 seconds, with a 15-second hard minimum;
- untouched old 10-second settings migrate to 30 seconds;
- identical checkpoint fingerprints skip writes;
- periodic checkpoint logs are suppressed;
- current player truck is used instead of scanning all Career inventory objects;
- known support metadata is reused;
- snapshot construction uses a protected re-entry/error guard;
- Random Events bridge per-frame work is limited to imports and explicit `keepTick` scenes.

### Status

```text
Source defect/risk: CONFIRMED
Repair implemented: YES
Static verification: PASS
BeamNG runtime proof: PENDING DAVID
Sole cause of every observed freeze: NOT YET PROVEN
```

## Incident B — repeated fire/emergency vehicles in abandoned calls

### Runtime evidence

David reported approximately the last five selected target vehicles were fire-department vehicles, including abandoned-vehicle work.

### Confirmed source defects

- Fire identification covered `fire truck`, `fire engine`, `fire rescue` and similar narrow names but did not cover common names such as `Fire Department`, `Fire Dept`, `Fire Service`, `Fire Brigade`, `Fire Chief`, `Pumper Truck` and `Brush Truck`.
- A missed fire configuration could fall through to generic heavy-target classification.
- Normal target selection did not separate civilian and emergency pools by a controlled agency-call probability.
- There was no emergency-target cooldown across successive calls.

### Required ownership/realism rule

Police, fire, ambulance/EMS and similar emergency-service vehicles must not become:

- abandoned/private-property targets;
- random private payer-default acquisitions;
- ordinary private lien/title vehicles.

They may still require towing after a breakdown, collision, rollover or severe damage, but those calls should be agency paid. An emergency agency vehicle must not randomly default into private tow-company ownership.

### v0.4.4.4 correction

- expanded police/fire/EMS identification;
- emergency metadata overrides an accidental generic heavy-target role for abandoned/lien safety;
- abandoned/private-lien eligibility rejects emergency configurations;
- appropriate emergency recovery calls remain possible;
- controlled target chances: 6% tow, 10% recovery, 12% accident;
- eight-selection cooldown after one emergency target;
- civilian pool exhaustion cannot force emergency repetition;
- emergency target jobs force government/emergency-services agency payment;
- saved civilian scene templates cannot reroll into emergency replacements.

### Status

```text
Classification gap: CONFIRMED
Emergency selection-policy gap: CONFIRMED
Repair implemented: YES
Static token/policy tests: PASS
BeamNG runtime proof: PENDING DAVID
```

## Exact repair artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_4_ActiveCallPerformanceEmergencyFilterSameYardClaimRuntimeSlim.zip`

- SHA-256: `61b1ef9e746f5978bba2cd7e7a4368aef4c19d2fe17f6c1207142d4fd3a4f6ad`
- Status: STATIC/MOCK VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Change boundary

No JOB-04, JOB-13, Browser Core, Random Events, stock BeamNG or Career/RLS source was edited. Saved-job resume reconstruction remains deferred.