# RF-AUTO Organizer Handoff to JOB-00

**Date:** 2026-07-16  
**From:** Career Dev / Grabber planning chat  
**To:** `JOB-00 — Coordinator / Integration / Verification`  
**Owner directive:** David / Captain  
**Primary board:** `PROJECT_MANIFESTS/REDFOX_AUTO_YARD_REPAIR_ECOSYSTEM_JOB_BOARD.md`

---

## Owner instruction

David instructed that the full Tow Yard / Scrap Yard / Wrecking Yard / Repair Shop / Body Shop ecosystem plan be placed on GitHub and handed to the organizer chat. David also clarified that several components are already being developed, so existing chats must make those components rather than creating duplicate replacements.

---

## JOB-00 required action

1. Read the entire RF-AUTO board.
2. Audit current repository manifests, claims, releases, incident reports, and handoffs.
3. Identify which RF-AUTO packages already have active owners or existing builds.
4. Keep those packages with their existing chats.
5. Mark genuinely unowned packages as available rather than silently assigning them.
6. Define the first shared interface contracts.
7. Keep implementation focused on the immediate towing blocker:
   - usable hook/strap/cable/winch attachment;
   - node/recovery grabber diagnosis;
   - free-camera targeting while the truck remains active;
   - no RLS cheat mode.
8. Coordinate future work without making the current Career Dev / Grabber chat the organizer.

---

## Existing ownership that must be preserved

- `JOB-00`: organizer/integration/verification.
- `JOB-01`: IceFox phone/PC/platform/Hub front door.
- `JOB-02`: RLS/Career bridge, approved money/inventory/ownership/save paths.
- `JOB-04`: Scrap Yard / Wrecking Yard.
- `JOB-08`: insurance/finance/garage/storage pages and later fleet insurance.
- `JOB-09`: Tow / Recovery / Dispatch business and job flow.
- `JOB-11`: QA/logging/failure triage.
- Existing BeamNG Investigator work: scanner and in-game capture.
- Existing character/weapons/movement work: reuse when David provides files.
- Existing Career Dev / Grabber work: remain in the current technical chat.

No competing Scrap Yard, Tow Dispatch, Career Bridge, Hub, QA, or platform chats should be created.

---

## Existing work specifically noted in the source chat

### Career developer tools

- Manual dev-tool UI direction.
- Money must change only after a typed value and explicit Add/Remove/Set/Zero button.
- No money mutation on load.
- No RLS `cheatsMode` dependency.
- Dev access includes garage/config/vehicle testing/teleport/time tools.

### Node/recovery grabber

- Separate direct-control module.
- Node rendering was reached, but grab acquisition remained unresolved.
- Need targeted comparison of Freeroam, stock Career, and RLS Career.
- Shift+C free camera is heavily used for towing setups while the player remains in the tow truck.
- Desired future colors: purple available nodes, seafoam hover, green grabbed, red invalid.

### BeamNG Investigator

- Existing File Viewer baseline.
- External scanner and in-game diagnostic were planned/built as unproven tests.
- Intended capture: camera mode, active player vehicle, action filters/maps, grab down/up, node selection, extensions, logs, and overrides.

### Recovery hooks

- David accepts a two-click workflow:
  1. select hook/cable/strap/chain;
  2. select attachment location.
- This may be preferable to relying on stock node grabber for normal towing.
- Realistic mode should use strong/human-valid attachment points.
- Recovery Override may use structural nodes.

### Character and tools

- Separate character/weapons work already exists.
- Desired movement feel is closer to Halo, GTA V, or Fortnite than BeamNG's ball-like walking.
- Shared tool framework should support mechanical, body, recovery, inspection, and weapon/tool projects.

### Parts and businesses

- Initial removal/install works with BeamNG's existing parts/config slots, not every bolt.
- Removed parts should be stored, repaired/refurbished, sold, scrapped, or reinstalled.
- Dented fenders and similar panels should be reusable where possible.
- Later body-shop stages may include bare metal, primer, and repaint states.

---

## First milestone for coordination

The organizer should treat this as the first end-to-end target:

> In RLS Career with cheat mode disabled, select a tow hook or cable, select a valid strong point on a stranded vehicle, connect it, operate the winch, release it, and complete the interaction without money changes, save damage, or a recurring script loop.

The stock/recovery node grabber can remain a parallel developer override project.

---

## Status language

Everything remains planning, partial, or runtime untested until David tests the exact build. Do not call any part fixed, working, ready, safe, complete, or final based only on source, syntax, file presence, or ZIP integrity.

---

## Current chat after handoff

The Career Dev / Grabber chat will focus only on:

- Grabber diagnosis/override.
- Recovery grabber technical work.
- Manual-only dev tools.
- Typed money controls.
- Teleport/time/dev functions.
- Investigator support.

JOB-00 owns the broader ecosystem organization from this point forward.
