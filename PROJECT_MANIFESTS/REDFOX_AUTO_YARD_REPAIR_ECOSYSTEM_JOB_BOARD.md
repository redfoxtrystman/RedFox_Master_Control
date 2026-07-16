# RedFox Auto Yard / Tow / Repair / Wrecking Ecosystem Job Board

**Date created:** 2026-07-16  
**Owner:** David / Captain  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Project prefix:** `RF-AUTO`  
**Coordinator:** Existing `JOB-00 — Coordinator / Integration / Verification` chat  
**Status:** PLANNING / ARCHITECTURE — implementation remains owned by existing project chats where noted

---

# 1. Purpose

This board defines the connected BeamNG Career ecosystem David wants to build:

- Tow company and recovery dispatch
- Winches, hooks, straps, chains, cranes, and recovery rigging
- Full tow yard and impound operations
- Scrap yard and wrecking yard gameplay
- Mechanical repair shop
- Used-parts removal, storage, refurbishment, resale, and installation
- Auto-body repair and paint shop
- Damaged-vehicle rebuilding and resale
- Better walking/player movement and interaction
- Shared tools and equipment
- RLS Career Overhaul compatibility
- Shared IceFox/FoxNet phone, PC, and Hub access
- Map facilities and unrestricted developer travel tools
- Diagnostics, logging, and safe testing

The long-term goal is one coherent game ecosystem where a player can recover a wreck from a ditch, tow it to a yard, inspect it, part it out or repair it, refurbish usable parts, rebuild vehicles, run a repair/body shop, and sell or scrap completed assets through the existing RedFox/RLS systems.

This board does **not** replace the current FoxNet rebuild board. It is a subproject architecture and responsibility map. Existing jobs keep ownership of systems they already own.

---

# 2. Non-negotiable design decisions

## 2.1 Use BeamNG's real parts

Initial versions work with the vehicle parts BeamNG already defines through slots/configuration. Do not simulate every individual bolt unless a future investigation proves that level of detail is practical and worthwhile.

Examples of valid initial targets:

- Wheel/tire assemblies
- Brake parts when separately exposed
- Doors
- Hood
- Trunk/tailgate
- Fenders
- Bumpers
- Lights
- Seats
- Engine
- Transmission
- Suspension components
- Exhaust components
- Other actual configuration slots

## 2.2 Tool interaction, not fake deletion

The intended gameplay is:

1. Equip a valid tool.
2. Aim at a real removable part.
3. Highlight the target.
4. Click or hold to remove/install.
5. Update the actual vehicle configuration.
6. Create a physical or inventory representation.
7. Store, repair, refurbish, sell, reinstall, or scrap the part.

## 2.3 Two-click recovery hook workflow

The immediate towing requirement does not depend on restoring the stock node grabber.

Preferred interaction:

1. Activate Hook/Recovery Mode.
2. Click/select the hook, cable, strap, chain, or winch end.
3. Click/select a valid attachment point on the target vehicle.
4. Create the connection.
5. Operate winch pay-in/pay-out.
6. Release one connection or all connections.

Realistic mode rejects mirrors, glass, trim, doors, and weak panels. Developer/Recovery Override may attach to a selected structural node when necessary.

## 2.4 Separate realistic interaction and developer override

**Realistic mode:** human-scale interaction, appropriate tools, valid hardpoints, no ripping doors off by accident.

**Recovery/Developer Override:** full recovery grabber, structural-node attachment, unusual crane/winch setups, vehicle testing, emergency repositioning.

## 2.5 RLS cheats mode is not an unlock mechanism

Do not enable RLS `cheatsMode` to unlock tools. RLS can force the player balance to `$1 trillion` while cheats are enabled. Dev, grabber, teleport, and tool systems must remain independent of RLS cheat mode.

## 2.6 Money never changes on load

No module may add, remove, reset, or set money during startup, map load, extension load, or a recurring loop. Money changes only after a deliberate typed amount and explicit button press.

## 2.7 Preserve complete vehicle state

Systems involving towing, garage storage, map travel, parts removal, or rebuilding must preserve as much as BeamNG/RLS supports:

- Vehicle model/config
- Installed parts
- Tuning
- Paint
- Damage/condition
- Inventory identity
- Attached trailer/load/cargo where feasible
- Ownership and title state

## 2.8 One shared Hub/front door

Direct grabber/tool controls need their own bindings, but administrative systems should be reachable through one IceFox/FoxNet Hub rather than consuming many unrelated keys and UI apps.

---

# 3. Existing project ownership that must be reused

The following work already exists or is already assigned. New RF-AUTO chats must not duplicate it.

| Existing owner | Existing responsibility | RF-AUTO relationship |
|---|---|---|
| `JOB-00 — Coordinator / Integration / Verification` | Project coordination, integration, verification | Becomes the RF-AUTO organizer/coordinator. Maintains this board and routes work. |
| `JOB-01 — Phone + PC Platform Core` | Shared IceFox phone, PC, browser, app launcher, route registry | Owns the shared front-door/platform integration. RF-AUTO pages register into it. |
| `JOB-02 — Shared RLS / Career Bridge` | Shared RLS/Career data and commands | Owns approved money, inventory, ownership, garage, save/load, and Career bridge contracts. |
| `JOB-04 — Scrap Yard / Wrecking Yard` | Scrap Yard web/app/business logic | Owns the existing Scrap/Wrecking Yard lane. RF-AUTO physical gameplay integrates with it; no duplicate Scrap Yard chat should be created. |
| `JOB-08 — Insurance / Finance / Garage / Storage Pages` | Insurance, finance, garage, and storage pages | Owns related page/UI systems and future fleet insurance integration. |
| `JOB-09 — Tow / Recovery / Dispatch Integration` | Tow jobs, dispatch, billing, manifests, fleet/truck tracking | This existing job is the primary Tow Company/Dispatch owner and should be claimed/used rather than creating a duplicate dispatch chat. |
| `JOB-11 — QA / Logging / Failure Triage` | QA, logging, crash/failure triage | Owns formal runtime verification, failure reports, and cross-module QA. |
| Existing BeamNG Investigator / scanner work | File Viewer, external scanner, in-game diagnostic capture | Continues as diagnostics support and should not be rebuilt from scratch. |
| Existing character/weapons work | Walking movement, player weapons/tools experimentation | Character movement and shared hand/tool interaction should reuse that work when David supplies the files. |
| Existing dev-tool/grabber work | Career Dev Tools, standalone grabber experiments, teleport/time/money controls | Remains in the current grabber/dev chat until handed off through JOB-00. |

---

# 4. RF-AUTO work packages

These identifiers organize technical work without replacing official FoxNet `JOB-00` through `JOB-12` ownership.

## RF-AUTO-00 — Organizer / Architecture / Integration

**Owner:** Existing `JOB-00` chat.

Responsibilities:

- Maintain this board.
- Record current owners and existing builds.
- Prevent duplicate systems and file conflicts.
- Define shared contracts between towing, tools, parts, repair, scrap, body, Career, and Hub systems.
- Decide which existing chat owns each deliverable.
- Maintain dependency order.
- Track last-known-good and first-bad builds.
- Coordinate eventual RLS outreach.
- Require before-edit, after-edit, and after-ZIP checks.
- Ensure no module claims runtime success before David tests it.

Protected boundaries:

- Does not independently rewrite every subsystem.
- Does not reassign existing jobs without David's approval.
- Does not merge unproven modules into a shared release.

## RF-AUTO-01 — BeamNG Investigator / Diagnostics

**Existing work:** `RedFox BeamNG Investigator v0.2.0` external app and in-game diagnostic mod exist as unproven diagnostic builds.

Responsibilities:

- Scan BeamNG installation and user folders.
- Search stock code, active mods, RLS overrides, logs, and captures.
- Trace node-grabber, input filters, camera mode, free camera, walking mode, Career, and RLS behavior.
- Compare Freeroam, stock Career, and RLS Career.
- Detect duplicate virtual paths and override conflicts.
- Export collected relevant files and reports.
- Preserve original File Viewer behavior as a separate tab.
- Later integrate with the existing mod manager as a separate module/tab, not one giant code path.

Current primary diagnostic question:

Why can RedFox actions display nodes in Career while the mouse/grab transition cannot acquire or hold a node?

Required capture details:

- Shift+C free-camera state
- Player vehicle identity remains active
- Camera ray/position/direction
- Input action maps and filters
- Grab button down/up
- Hovered/selected node where available
- Stock Freeroam success path
- Stock Career path
- RLS Career path

## RF-AUTO-02 — Character Movement and Interaction

**Existing work:** David already has a character/weapons/movement project and will provide its files. Reuse it; do not start over.

Responsibilities:

- Improve walking beyond the current ball-like feel.
- Smooth acceleration/deceleration.
- Strafing.
- Sprint.
- Crouch.
- Jump improvement.
- First-person and third-person handling.
- GTA V / Halo / Fortnite-inspired responsiveness without copying assets/code.
- Free-camera compatibility.
- Shared interaction ray for tools, hooks, parts, and hand interactions.
- Support existing/future weapon and handheld-tool work through one character framework.

## RF-AUTO-03 — Shared Tool and Equipment Framework

Responsibilities:

- Equip/unequip tools.
- Toolbelt or radial selector.
- Shared targeting/highlight system.
- Click or hold actions.
- Progress indicator.
- Tool audio/animation hooks.
- Interaction range and permissions.
- Purple/seafoam/green/red status language.
- Common API for recovery, mechanic, body, inspection, and weapon/tool projects.

Initial equipment:

- Impact gun
- Ratchet
- Pry bar
- Tow hook selector
- Cable/strap connector
- Flashlight
- Inspection scanner

Later equipment:

- Jack and stands
- Engine hoist
- Welder
- Grinder
- Plasma cutter
- Sand/media blaster
- Paint gun
- Body hammer/dolly
- Stud welder/slide hammer
- OBD/compression/paint/tire diagnostic tools

## RF-AUTO-04 — Recovery Hooks / Winches / Straps / Chains

**Immediate gameplay priority.**

Responsibilities:

- Two-click hook/attachment workflow.
- Work while Shift+C free camera is active and the truck remains the player vehicle.
- Select hook/cable/strap/chain end.
- Select valid vehicle hardpoint or structural node.
- Create/release connection.
- Winch pay-in/pay-out.
- Multiple connections.
- Snatch blocks later.
- Tow-hook finder.
- Snap-to-hardpoint option.
- Realistic weak-part rejection.
- Recovery Override mode.
- Safe release-all.
- Integrate with `JOB-09` dispatch jobs but do not own dispatch/business logic.

First practical milestone:

> Walk to or select a tow hook, select a strong point on a stranded vehicle, connect it, operate the winch, and release it without RLS cheat mode.

## RF-AUTO-05 — Standalone Recovery Grabber

**Existing work:** standalone RedFox node-grabber experiments exist; node rendering works but grab acquisition remains blocked/unresolved.

Responsibilities:

- Diagnose/restore or replace native grabbing without RLS cheat mode.
- Independent RedFox action names.
- Direct BeamNG node interaction.
- Shift+C free-camera compatibility.
- Purple available nodes.
- Seafoam hovered node.
- Green grabbed node.
- Red invalid node.
- Adjustable strength.
- Adjustable radius if supported.
- Fix/lock current node.
- Emergency release.
- On/off Recovery Override.
- No background loop.
- No money or save changes.

This remains separate from administrative Hub UI because direct grabbing needs hold/mouse controls.

## RF-AUTO-06 — Vehicle Part Removal and Installation

Responsibilities:

- Discover actual BeamNG part/config slots.
- Map visible/aimed vehicle regions to removable parts.
- Require appropriate tools where desired.
- Remove the selected actual part from vehicle configuration.
- Create an inventory/physical representation.
- Install compatible stored parts.
- Preserve condition, paint, source vehicle, and compatibility.
- Avoid bolt-by-bolt simulation in initial versions.

Initial targets:

- Wheels/tires
- Doors
- Hood
- Trunk/tailgate
- Fenders
- Bumpers
- Lights
- Seats
- Engine/transmission
- Suspension/exhaust where exposed

## RF-AUTO-07 — Parts Inventory and Storage

Responsibilities:

- Record each removed part as an inventory item.
- Track part name/ID, source vehicle, compatibility, condition, damage, paint, value, repairability, and status.
- Physical drop zones for shelves/pallets/bins.
- Search/filter inventory.
- Used/new/refurbished/scrap categories.
- Install from storage.
- Prevent duplication/loss.
- Use `JOB-02` RLS/Career bridge contracts.
- Coordinate page/UI with `JOB-08` and Hub/platform with `JOB-01`.

## RF-AUTO-08 — Mechanical Repair Shop

Responsibilities:

- Diagnose mechanical damage.
- Repair individual existing BeamNG parts.
- Replace damaged components.
- Work orders/estimates.
- Labor time and tool requirements.
- Repair bays/lifts/shop computers.
- Customer and company-owned vehicles.
- Road-test workflow.
- Insurance integration later through `JOB-08`.

Initial approach may combine menus and targeted tool actions. It does not need a full animation for every repair step.

## RF-AUTO-09 — Refurbishment / Parts Reconditioning

Responsibilities:

- Decide whether parts are reusable, repairable, refurbishable, or scrap.
- Clean parts.
- Straighten minor damage where supported.
- Refinish wheels/body parts.
- Restore condition/value.
- Preserve provenance.
- Allow dented or ugly parts to be reused rather than automatically discarded.
- Feed repaired parts back into RF-AUTO-07 inventory.

## RF-AUTO-10 — Auto Body and Paint Shop

**Later phase.**

Responsibilities:

- Body-panel removal/installation.
- Dent repair.
- Panel replacement.
- Sanding.
- Sand/media blasting.
- Bare-metal visual state.
- Primer state.
- Paint selection/booth.
- Clear coat.
- Color matching.
- Labor/material cost.

Suggested staged visual states:

1. Existing painted/damaged state
2. Stripped/bare metal silver-gray
3. Primer
4. Repainted/clear-coated

Operate on real removable body parts where possible.

## RF-AUTO-11 — Tow Company / Recovery Dispatch

**Owner:** Existing official `JOB-09` lane.

Existing/planned features to preserve:

- Tow jobs and dispatch
- Scene bubble/zone tracking
- Entry/exit timestamps
- Multiple-trip jobs
- Multiple-truck operations
- Required drop-off behavior
- Truck names and fleet identity
- Company naming
- Cargo/tow manifest
- Realistic tow bill/invoice
- Recovery difficulty/payment
- Impound, scrap, repair, and storage destinations
- Fleet insurance later through `JOB-08`

RF-AUTO-04 supplies physical hook/winch actions; `JOB-09` owns job/business/dispatch flow.

## RF-AUTO-12 — Scrap Yard / Wrecking Yard Operations

**Owner:** Existing official `JOB-04` lane for Scrap Yard/Wrecking Yard. Do not create a competing Scrap Yard owner.

Physical gameplay responsibilities to integrate:

- Receive complete vehicles.
- Confirm ownership/salvage authorization.
- Choose sell complete, repair, rebuild, part out, or scrap.
- Remove valuable parts through RF-AUTO-06.
- Store/sell/refurbish parts through RF-AUTO-07/09.
- Track remaining shell value/weight.
- Crush/dispose of stripped shells later.
- Environmental/disposal costs later.

Hard safety boundary from the main board remains active:

- No startup Scrap Yard Career module.
- No automatic map-load generator.
- No fake money/garage/storage path.
- Use approved `JOB-02` bridge contracts.

## RF-AUTO-13 — Vehicle Rebuilding and Resale

Responsibilities:

- Build from damaged/incomplete vehicles.
- Install compatible used/refurbished parts.
- Track build cost and labor.
- Title/status handling: clean, salvage, rebuilt, parts-only.
- Inspection workflow.
- Calculate sale value.
- Sell through existing BeamBook, auctions, collector exchange, dealer, or direct systems using their existing job owners.

## RF-AUTO-14 — Career Economy and RLS Bridge

**Owner:** Existing official `JOB-02` lane.

Responsibilities:

- Approved money transactions.
- Ownership.
- Vehicle inventory.
- Part inventory.
- Garage/storage.
- XP/reputation.
- Rewards and expenses.
- Save/load.
- Map transition state.
- Prevent accidental startup mutations.
- Typed manual dev money controls only.
- No `cheatsMode` dependency.

## RF-AUTO-15 — Facilities and Map Integration

Responsibilities:

- Tow yards.
- Impound lots.
- Wrecking/scrap yards.
- Repair shops.
- Body shops.
- Parts warehouses.
- Paint booths.
- Vehicle lifts.
- Customer drop-off points.
- Cross-map travel nodes.
- Document how maps are registered with RLS Career travel and facilities.
- Add developer map switch from any location separately from normal in-world travel points.

Map switching must account for current vehicle, walking state, cargo, trailers, and persistence limitations.

## RF-AUTO-16 — Unified Hub and UI

**Owners involved:** Existing `JOB-01` platform, `JOB-10` visual design, relevant app/page jobs, and `JOB-00` integration.

Responsibilities:

One shared Hub/front door for:

- Career dev tools
- Typed money add/remove/set/zero
- Teleport
- Time-of-day controls
- Garage/parts/config
- Tow company
- Parts inventory
- Repair orders
- Scrap/wrecking yard
- Body shop
- Map travel
- Diagnostics/status

Direct grabbing and handheld tool actions remain separate controls, but settings and launch/status pages may appear in the Hub.

## RF-AUTO-17 — QA / Logging / Failure Triage

**Owner:** Existing official `JOB-11` lane.

Responsibilities:

- Independent module tests.
- Combination tests.
- Save corruption/duplication checks.
- Money duplication checks.
- Vehicle/part loss checks.
- Cross-map state checks.
- Lua-loop/log-flood checks.
- Input conflicts.
- Memory/CEF impact.
- Last-known-good and first-bad tracking.
- Exact before-edit, after-edit, and after-ZIP evidence.
- Runtime status only after David tests.

---

# 5. Development phases

## Phase 1 — Make towing physically usable

1. Continue RF-AUTO-01 Investigator.
2. Build RF-AUTO-04 two-click Recovery Hook System.
3. Continue RF-AUTO-05 Standalone Recovery Grabber.
4. Integrate supplied character/movement work into RF-AUTO-02.
5. Define RF-AUTO-03 Tool Framework interfaces.

## Phase 2 — Make parts removable and reusable

6. RF-AUTO-06 Part removal/installation.
7. RF-AUTO-07 Parts inventory/storage.
8. RF-AUTO-09 Refurbishment.
9. RF-AUTO-08 Mechanical repair.

## Phase 3 — Build operating businesses

10. Existing `JOB-09` Tow/Dispatch integration.
11. Existing `JOB-04` Scrap/Wrecking Yard integration.
12. RF-AUTO-13 Rebuilding/resale.
13. RF-AUTO-10 Body/Paint shop.

## Phase 4 — Complete shared Career ecosystem

14. Existing `JOB-02` bridge/economy integration.
15. RF-AUTO-15 facilities/map travel.
16. Existing `JOB-01`/`JOB-10`/RF-AUTO-16 Hub integration.
17. Existing `JOB-11` full-system QA.

---

# 6. Shared interface contracts to define before integration

JOB-00 must coordinate written contracts for:

1. **Target Selection Contract** — camera ray, free camera, walking/vehicle identity, hovered object/part/node.
2. **Tool Action Contract** — tool ID, target type, hold/click, duration, success/failure, animation/audio hooks.
3. **Recovery Connection Contract** — source hook, target hardpoint/node, rope/chain type, limits, ownership, release.
4. **Vehicle Part Contract** — vehicle inventory ID, slot/part ID, condition, paint, source, install compatibility.
5. **Parts Inventory Contract** — add/remove/transfer/store/refurbish/sell/install.
6. **Work Order Contract** — customer/vehicle, requested tasks, parts, labor, estimate, status, payment.
7. **Scrap Decision Contract** — repair/rebuild/part-out/scrap, authorization, shell state, disposal.
8. **Career Transaction Contract** — approved money and ownership mutations through JOB-02 only.
9. **Hub Registration Contract** — shared destination/page IDs through JOB-01.
10. **Map Travel Contract** — source map/location, destination, player state, vehicles/cargo, rollback.
11. **Diagnostic Contract** — logs, event IDs, status, test evidence, version/build identity.

---

# 7. Immediate current-chat scope after handoff

After this board is created, the current Career Dev / Grabber chat returns to only:

- Standalone node grabber diagnosis and override work
- Recovery grabber research
- Career Dev Tools manual-only behavior
- Typed money controls that do nothing on load
- Teleport/time/dev access
- Supporting the Investigator capture for node-grabber diagnosis

It does **not** become the overall RF-AUTO organizer. JOB-00 takes that role.

---

# 8. RLS outreach threshold

David may approach RLS after the project proves basic working gameplay, not merely plans or static checks.

Suggested minimum demonstration:

1. Recover a vehicle with hook/winch workflow in RLS Career without cheats mode.
2. Deliver it through a tow job.
3. Remove at least one real BeamNG part.
4. Preserve it in parts inventory.
5. Reinstall, refurbish, sell, or scrap it.
6. Save/reload without money, vehicle, or part duplication.
7. Demonstrate one coherent Hub/Career integration path.

At that point, prepare a technical integration proposal rather than asking RLS to adopt an unproven concept.

---

# 9. Global operating rules

- Existing official job ownership wins over new RF-AUTO labels.
- Do not duplicate an existing chat's system.
- Inspect existing work before starting over.
- Use BeamNG/RLS systems rather than fake parallel money, inventory, garage, or ownership systems.
- No startup money changes.
- No RLS cheat-mode dependency.
- No recurring patch loops without a proven necessity, rate limiting, and QA approval.
- No startup Scrap Yard Career module.
- Do not overwrite phone/PC/Hub shells.
- Preserve working source and exact baselines.
- Before edit: inspect and document.
- After edit: verify actual edited behavior paths.
- After packaging: reopen the final ZIP and verify promised contents.
- Static checks are not runtime proof.
- Required status remains `BUILT — RUNTIME UNTESTED` until David tests the exact package.
- JOB-11 must review cross-system builds.

---

# 10. Organizer handoff

`JOB-00 — Coordinator / Integration / Verification` must now:

1. Read this entire board.
2. Compare it with all existing jobs/builds.
3. Mark each RF-AUTO package as existing, assigned, available, blocked, or deferred.
4. Route already-existing work back to its current owner.
5. Create new chats only for genuinely unowned components.
6. Publish interface-contract priorities.
7. Keep the first implementation milestone focused on usable towing hooks/grabbing.
8. Do not pull the current grabber/dev chat away from its immediate technical scope.

Signed,

**Sol / Career Dev and Grabber planning chat**  
Handoff requested by **David / Captain**
