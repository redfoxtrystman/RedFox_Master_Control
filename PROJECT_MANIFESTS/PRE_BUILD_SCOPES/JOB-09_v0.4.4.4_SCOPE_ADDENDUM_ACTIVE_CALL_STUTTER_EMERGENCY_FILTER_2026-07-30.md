# JOB-09 v0.4.4.4 Approved Scope Addendum — Active-Call Stutter and Emergency-Vehicle Filtering

**Date/time approved:** 2026-07-30, after the initial v0.4.4.4 source checkpoint  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Base scope commit:** `992e5e3ac07f791e0e2237d3f4808dd8822668b2`  
**Initial source checkpoint:** `ee6e2acb38ee747f352e4504055cb3e9eac09d5e`

## New runtime evidence

David reported two additional issues while testing the current JOB-09 build:

1. During an active tow call, gameplay repeatedly freezes for several seconds, briefly resumes, and freezes again. The stutter stops after the target is delivered and the active call ends. This strongly localizes the defect to active-call update work rather than general idle JOB-09 operation.
2. The last several selected vehicles were fire-department vehicles. Emergency configurations are being over-selected for abandoned calls and potentially for unpaid/default/lien outcomes.

## Authorized additional repair scope

### Active-call performance

- Profile and measure all work entered only while an active call exists.
- Remove or throttle repeated expensive target, route, scene, condition, roster, support, and persistence scans.
- Ensure event-driven state writes and bounded periodic checkpoints rather than repeated heavy work every active-call tick.
- Preserve route updates, completion detection, police/support validation, active-job recovery checkpoints, and gameplay correctness.
- Do not hide a failure by disabling required call logic.

### Emergency vehicle call eligibility

- Police, fire, ambulance/EMS, rescue and other government emergency/service configurations must not be selected for:
  - abandoned-vehicle calls;
  - random payer-default calls;
  - ordinary private lien/impound acquisition;
  - found abandoned ownership flows.
- Emergency/service vehicles remain eligible for appropriate agency-paid calls, breakdowns, accidents, collisions, rollovers, severe damage, and explicit police/fire/municipal recovery scenarios.
- Emergency vehicles should not randomly default into private lien ownership. If an agency call cannot pay, use an agency/accounting outcome rather than ordinary abandoned-title acquisition.
- Preserve manually reviewed exact-configuration overrides where the catalog explicitly identifies a non-emergency civilian configuration.
- Add selection-history safeguards so one emergency service/model/configuration cannot dominate repeated calls.

## Order-of-operations effect

The already-created source checkpoint is retained as an intermediate checkpoint. No v0.4.4.4 package was created or distributed before this addendum. The source will now be revised, fully reverified, and a new final source checkpoint will supersede the intermediate one.

No JOB-04, JOB-13, Browser Core, Random Events, BeamNG, Career/RLS or other job-owned source is authorized for modification.