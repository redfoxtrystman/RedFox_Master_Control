# JOB-09 — Police Impound and Emergency Scenes v0.2.6

**Date:** 2026-07-21  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**  
**Pause state:** David is still camping. This build does not transfer or hand off JOB-09 ownership.

---

## Exact test package

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_6_PoliceImpoundEmergencyScenes.zip
Size: 118,799 bytes
SHA-256: 82eecc0652d61cc8b6d203d0bf7eb541bdee95532e8c82c2b2ecd59c0a0b2dbd
```

Source baseline:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_5_FleetIdentityHazardSites.zip
SHA-256: 52d453d601371a40fb7f675ec62468542939c3b201740845643a5761221cafbf
```

The installable ZIP is available in the active ChatGPT JOB-09 workspace. It is not committed as a binary to this GitHub repository.

---

## Focused additions

### New RedFox-native calls

1. **Police-Requested Vehicle Impound**
   - One passenger or performance-oriented target.
   - Police vehicle and cone support when enabled.
   - Agency tow payment.
   - Delivered vehicle enters the separate RedFox yard as an `impound_hold` record.

2. **Street-Racing Vehicle Impound**
   - Two performance-oriented targets.
   - Police vehicles and a cone taper.
   - Both targets must be delivered to the selected RedFox yard.
   - Agency payment is queued after the full scene is cleared.

3. **DUI Checkpoint Impound**
   - One passenger target.
   - Two police vehicles and checkpoint-style cone placement.
   - Delivered vehicle enters police impound hold.

### Emergency-scene support

A new setting, **Police / EMS / Cone Support at Major Scenes**, is enabled by default. It currently adds basic support layouts to:

- multi-vehicle accidents;
- semi/trailer rollover recovery;
- rolled-car recovery;
- street-racing impound;
- DUI checkpoint impound;
- police-requested impound.

The first test implementation uses dynamically selected police/ambulance configurations plus BeamNG cone props. All support vehicles and cones are tracked by the RedFox event and should be deleted on completion or cancellation.

This is a first runtime test, not a claim of complete traffic diversion, animated responders, fire-department operations, or universal map-safe placement.

### Yard and history

- Police calls use `paymentStatus = police_impound`.
- Payer is recorded as `Police / agency impound contract`.
- The agency pays the tow job; the vehicle remains cataloged in the RedFox yard on an impound hold.
- A new **Police / Enforcement** Tow History catalog was added.
- Police holds also appear in **Impound / Unpaid** for operational lookup.

---

## Uploaded third-party mods inspected

### Random Events 1.9.0.0

```text
random_events_1.9.0.0(1).zip
SHA-256: c35a240356989a23f83df04efecf34a3f41de1144046efdc434f229eb76766e6
```

Useful manager functions found include `getStatusJson`, `forceSpawn`, `toggleUI`, `rescan`/`forceRescan`, and `teleportTo`.

The status interface reports event IDs, types, and positions, but it does not expose the spawned target vehicle IDs or a supported claim/detach API. Its event modules keep ownership of spawned vehicles and delete them when the event despawns.

**v0.2.6 decision:** detect the mod, display active event types/count, and allow opening its panel. Do not take ownership of its live vehicles. RedFox police calls use RedFox-owned persistent targets instead.

### Traffic Reborn Free 1.4.0.0

```text
TrafficReborn_Free_v1.4.0.0(1).zip
SHA-256: a666ad1a07d007b64988ea4fec3911745d0d629e2d2929c45b6d8370de350e80
```

Useful manager functions found include `isRunning`, `spawn`, `setPoliceRatio`/`getPoliceRatio`, and `setEnforce`/`getEnforce`.

**v0.2.6 decision:** provide an explicit optional button that requests a 25% police ratio, enables enforcement, and starts Traffic Reborn traffic when stopped. A second button disables enforcement without stopping the user's traffic session. Nothing is changed automatically merely because Traffic Reborn is installed.

### Sandbox Tools 1.1.0.0

```text
sandbox_tools_1.1.0.0(1).zip
SHA-256: 578d359568a559af18a8ee30a49fc1e069c2a477c890f087402c6f3dd0cf65fd
```

The package exposes generic actions such as opening/closing normal couplers, freezing the current vehicle, spawning traffic, and running custom Lua. It does not provide a universal arbitrary-node rigging API or a tow-truck control adapter contract.

**v0.2.6 decision:** detect its presence only. Do not create a dependency.

---

## Third-party boundary

No Random Events, Traffic Reborn, or Sandbox Tools Lua, UI, models, textures, configurations, or other assets are copied or bundled in the RedFox package. The integrations are optional runtime calls to detected extension functions.

No explicit source-code reuse license was found inside the uploaded archives. Direct copying or redistribution was therefore rejected.

---

## Static verification completed

- ZIP integrity: PASS.
- Direct-root package layout: PASS.
- No duplicate ZIP entries: PASS.
- Main Lua syntax through `texlua loadfile`: PASS.
- Main Lua top-level execution with stubs: PASS.
- Optional-mod detection/control and police-offer smoke test with stubs: PASS.
- Packaged JSON parsing: PASS.
- Version consistency: PASS.
- Protected Career/RLS override path scan: PASS.
- Native executable/library scan: PASS.
- Third-party source/asset path inclusion scan: PASS.
- Packaged inventory checksum validation: PASS for 37 listed files.
- BeamNG runtime: **UNTESTED**.

---

## Intentionally not included

The following discussions remain separate later test systems and were not rushed into v0.2.6:

- universal one-to-four-point hook rigging;
- arbitrary hub/frame node attachment;
- universal tow-truck control adapter/setup wizard;
- game settings and Career-save backup manager;
- AI tow transport;
- autonomous hookup or winching;
- direct conversion of Random Events vehicles into RedFox targets;
- full traffic detours or animated police/EMS crews.

---

## First runtime test

1. Disable all older JOB-09 ZIPs, including v0.2.5.
2. Enable only v0.2.6.
3. Use a disposable Career save for the first responder-scene test.
4. Confirm existing yards, fleet records, history, and impounds load.
5. Run Police-Requested Vehicle Impound and confirm agency payment plus a yard hold.
6. Run Street-Racing Vehicle Impound and confirm two targets.
7. Run DUI Checkpoint Impound and inspect police/cone placement.
8. Run one Accident and one Semi Rollover and inspect police/EMS/cone cleanup.
9. Open Settings → Optional Mod Connections and check all installed-mod status.
10. Cancel a live call and verify every RedFox responder and cone is removed.

Return the relevant `beamng.log` section for any spawn, route, cleanup, UI, payment, or yard-record failure.
