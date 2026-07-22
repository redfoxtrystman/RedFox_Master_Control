# JOB-09 — Camping Pause Addendum: v0.2.6

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Status:** **PAUSED WHILE DAVID IS CAMPING — NOT A HANDOFF**

This addendum updates the July 17 pause audit after David briefly returned to town and supplied three reference mods for inspection.

No job ownership changed. Resume the same regular-chat JOB-09 workspace.

---

## New current candidate

The current candidate changed from v0.2.5 to:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_6_PoliceImpoundEmergencyScenes.zip
Size: 118,799 bytes
SHA-256: 82eecc0652d61cc8b6d203d0bf7eb541bdee95532e8c82c2b2ecd59c0a0b2dbd
Status: BUILT — RUNTIME UNTESTED
```

v0.2.5 remains the source baseline and fallback package. It was not marked broken. v0.2.6 is the next test package because it contains the newly requested police/enforcement work.

The installable binary remains in the active ChatGPT workspace and is not committed to GitHub.

---

## Added after the original pause audit

- Police-Requested Vehicle Impound call.
- Street-Racing Vehicle Impound with two performance-oriented targets.
- DUI Checkpoint Impound.
- Police/agency tow payment.
- Persistent police impound-hold yard records.
- Police / Enforcement Tow History catalog.
- First-pass police, ambulance, and cone support at major scenes.
- Optional Random Events status and UI connection.
- Optional Traffic Reborn police-ratio/enforcement controls.
- Sandbox Tools presence detection.

---

## Reference mods inspected

```text
random_events_1.9.0.0(1).zip
TrafficReborn_Free_v1.4.0.0(1).zip
sandbox_tools_1.1.0.0(1).zip
```

The full audit is recorded at:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_THIRD_PARTY_TOW_EVENT_COMPATIBILITY_AUDIT_2026-07-21.md
```

Main result:

- Random Events does not expose a safe target-vehicle claim API, so live vehicles are not adopted.
- Traffic Reborn exposes useful optional police/enforcement controls.
- Sandbox Tools does not provide universal arbitrary-node rigging or unified tow controls.
- No third-party code or assets were copied.

---

## Still not added

The following remain planned separate experiments:

- universal one-to-four-point hook rigging;
- attachment to hubs, axles, suspension, frame, or manual node selections;
- universal tow-truck control adapter/setup wizard;
- settings and Career-save backup manager;
- AI delivery to the nearest reachable yard point;
- manual multi-wrecker/winch overlay;
- direct third-party offender/vehicle takeover;
- complete traffic detours and animated responder crews.

Do not claim these are in v0.2.6.

---

## Static status

v0.2.6 passed:

- Lua syntax;
- top-level stub execution;
- optional-integration smoke test;
- JSON parse;
- version consistency;
- protected-path scan;
- third-party inclusion scan;
- native-payload scan;
- ZIP integrity/layout/duplicate scan;
- packaged inventory hash validation.

BeamNG runtime is untested.

---

## New return test order

1. Disable every older JOB-09 ZIP, including v0.2.5.
2. Enable only v0.2.6.
3. Use a disposable Career save for the first test.
4. Confirm old yards, Fleet Book, Tow History, and impound records load.
5. Test Police-Requested Vehicle Impound.
6. Test Street-Racing Vehicle Impound.
7. Test DUI Checkpoint Impound.
8. Test one Accident and one Semi Rollover with emergency support enabled.
9. Confirm support vehicles/cones are removed on completion and cancellation.
10. Check Optional Mod Connections with the three supplied mods installed.
11. Return screenshots and `beamng.log` around any error.

Only after this test should JOB-09 decide whether to patch v0.2.6 or return to v0.2.5 and isolate the failing subsystem.
