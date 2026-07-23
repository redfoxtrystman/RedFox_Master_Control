# JOB-09 — Active-Call Recovery, Tow Validation, Alerts, and Wreck Conditions v0.2.9

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**

## Exact test package

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_ActiveCallRecoveryAlertsDamage.zip
Size: 181,835 bytes
SHA-256: 95722351456b6caeb51b448a624bdb33ae4b89e17e45df5fa77a85b6439ea1f2
```

Source baseline:

```text
19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_8_CareerDayAssetManager.zip
SHA-256: b7ad5424f82f70cec998e1ee01345c8f608b01d60aac6a6f927f06e75019a018
```

The installable ZIP remains in the active ChatGPT JOB-09 workspace and is not committed to GitHub as a binary.

## Runtime findings behind this build

David reported:

- a window crash during testing;
- a power outage during a semi rollover call;
- the active call being lost because v0.2.8 kept it only in runtime memory;
- incoming calls being easy to miss;
- the two-minute acceptance window being too short;
- many Tow targets remaining fully functional;
- semi recovery too often adding a trailer even when the heavy vehicle had an integrated bed/body;
- police support selecting dated configurations;
- concern that a player could teleport to the target and drive it to the yard without the tow truck.

David also confirmed one v0.2.8 success:

```text
Western Star Tow Yard record -> personal Career inventory/garage: DAVID-TESTED WORKING
```

All other v0.2.8 systems remain partial because testing was interrupted.

## v0.2.9 additions

### Active-call save and recovery

- Active calls autosave every 12 seconds by default.
- Saves rotate between two independent JSON recovery files and the Career-profile state.
- A completed/cancelled-call tombstone prevents stale jobs from reappearing.
- Manual **Save Active Call Now** control.
- **Resume Saved Active Call** and **Discard Saved Active Call** controls after restart.
- Undelivered targets are reconstructed with saved model/configuration, position, rotation, scene role, damage profile, destination, payment plan, and progression preview.
- Responders are regenerated from the saved scene anchor.
- An unexpectedly missing target preserves the last snapshot instead of discarding it.

Exact live node/beam deformation at the moment of power loss is not guaranteed. The target's condition profile is reapplied.

### Tow/service vehicle validation

- The vehicle used to accept the call is recorded as the active service truck.
- RLS inventory ID is stored where available so a respawned service vehicle can be resolved.
- Manual **Set Current Vehicle as Active Tow/Service Truck** control.
- A recovery target cannot be assigned as its own service truck.
- Once a target moves, more than 100 meters of separation starts a 15-second warning/countdown.
- Delivery requires the assigned service truck within 35 meters.

This is RedFox-owned behavior modeled on the inspected RLS 2.6.8 Repo distance relationship. No RLS source is patched or bundled.

### Incoming dispatch alerts

- Existing settings migrate to a minimum five-minute acceptance period.
- Built-in BeamNG mission-information sound.
- Large RedFox incoming-dispatch screen banner.
- Repeating reminder every 30 seconds by default.
- Acceptance and repeat periods are adjustable in Settings.

### Target condition variety

New runtime profiles include:

- operational impound;
- operational abandoned;
- stalled;
- flat tire;
- neglected;
- minor collision;
- rollover damage;
- severe collision;
- heavy wreck.

Accident and rollover vehicles receive explicit ignition, tire, breakgroup, AI, hazard, and impact treatment rather than relying only on a mild placement impulse.

### Semi/heavy-carrier composition

Semi recovery can now produce:

- heavy truck only;
- tractor plus trailer;
- rigid/integrated carrier plus displaced cargo vehicle;
- transport tractor plus displaced cargo vehicle.

Configurations with flatbed, rollback, car-carrier, transport, delivery, or rigid-body naming prefer the cargo-vehicle scene instead of automatically adding a trailer.

### Police configuration preference

Emergency scenes score matching police configurations and prefer newer stock or modded choices such as modern interceptors, Bastion/Vivace/Tograc/Scout/Roamer/Lansdale-style vehicles, and configurations with recent model-year metadata. Older choices remain fallback-only when no modern compatible configuration exists.

## Deliberately not included

- Tow Company fleet ownership/storage.
- Tow Yard -> business inventory transfer.
- Personal <-> business transfer.
- Company bank routing, branches, insurance, or sale protection.
- Full World Editor Scene Builder.
- Exact deformation serialization.
- Bundled third-party CB audio.

These remain separate because company transfer can delete or duplicate valuable vehicles if rushed.

## Static verification

- ZIP integrity: PASS.
- Direct-root layout: PASS.
- Duplicate ZIP entries: none.
- Lua loadfile/local-variable limit: PASS.
- Top-level stub execution: PASS.
- JSON parsing: PASS.
- Packaged inventory checksum validation: PASS for 60 files.
- Protected Career/RLS override-path scan: PASS.
- Native executable/library scan: PASS.
- RLS source/assets bundled: NO.
- BeamNG/RLS runtime: **UNTESTED**.

## Required runtime test

1. Disable every older JOB-09 ZIP, including v0.2.8.
2. Enable only v0.2.9 on a disposable RLS Career save.
3. Accept a call, move a target, save, restart BeamNG, and resume.
4. Verify delivered targets do not respawn.
5. Verify target/service-truck separation warnings and delivery proximity.
6. Verify call sound, banner, reminders, and five-minute acceptance.
7. Run Standard, Rollover, Accident, and Semi calls and inspect target condition variety.
8. Confirm semi-only, semi/trailer, and carrier/cargo variants occur.
9. Confirm newer police configurations are preferred when installed.
10. Regression-test v0.2.8 storage clock, organized pages, progression, and personal claim.
11. Return `beamng.log` around any save, resume, spawn, alert, tow-validation, damage, UI, or persistence failure.

Do not use the valuable abandoned truck for company ownership testing. Company fleet storage is not in v0.2.9.