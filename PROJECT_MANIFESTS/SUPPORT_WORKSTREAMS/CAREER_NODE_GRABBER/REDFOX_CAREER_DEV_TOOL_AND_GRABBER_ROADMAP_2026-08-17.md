# RedFox Career Dev Tool + Grabber — Full Roadmap / Handoff

**Support lane:** SUPPORT-02 — Career Node Grabber / Developer Mode Compatibility  
**Date:** 2026-08-17  
**Owner:** David / Captain  
**Current RLS baseline:** paid RLS Career Overhaul 2.7.0.1  
**Current BeamNG generation:** 0.38-era/new RLS baseline used in this work  
**Runtime rule:** nothing is called fixed until David tests the exact ZIP.

---

## 1. Current direction

The project is returning to the **full RedFox Career Dev Tool first**, because the grabber worked before the latest RLS update and the dev tool gives one place to repair more than one compatibility break at once.

The immediate goal is **not** to keep guessing at a totally custom node-physics implementation. The first priority is to inspect RLS 2.7.0.1 and restore the same practical Career behavior RedFox had before the update while avoiding the failures already discovered.

The standalone RedFox Grabber experiments are retained as diagnostic/reference work, but they are not the primary implementation path unless the updated full-tool route cannot be made safe.

---

## 2. Non-negotiable development rules

1. Inspect the exact current source/package before changing it.
2. Smallest possible functional patch.
3. No silent behavior changes.
4. No stock BeamNG or RLS full-file replacement unless David explicitly approves an exact patch after inspection.
5. Do not ship RLS `lua/ge/extensions/overrides/career/career.lua` inside RedFox.
6. Do not enable broad RLS Cheats Mode as a workaround.
7. Do not write Career saves directly unless David explicitly asks.
8. Do not automatically change money, XP, reputation, inventory, or progression.
9. Do not claim runtime success from static inspection.
10. Every delivered build must be documented here/GitHub with version, exact changes, risks, SHA-256, and runtime status.
11. Preserve working features while repairing broken ones.

---

## 3. What worked before the latest RLS changes

Earlier RedFox Career tooling could make the Node Grabber usable in Career. The user specifically reports that the grabber worked before the newest RLS update.

Earlier standalone/public Node Grabber work also proved that RedFox could expose the familiar Node Grabber controls in Career-related builds. However, some older implementations depended on compatibility techniques that are no longer acceptable for the current paid RLS baseline.

The practical target remains the normal familiar controls:

- Left Ctrl — show/activate grabber nodes
- Left Mouse — grab/drag
- Mouse Wheel — strength
- Middle Mouse — pin/attach/detach behavior

The desired eventual RedFox visual identity remains:

- Purple = RedFox selectable/detected node
- Green = hovered node
- Brighter green = active grabbed/selected state

---

## 4. Old standalone public Node Grabber history

### Original known-good development lineage

Known older development package:

`RedFox_Grabber_UI_v0_1_0_TEST(1).zip`

### Public v1.0.0 approach

Public release:

`RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL.zip`

That build achieved compatibility by shipping/pasting a patched RLS Career core override:

`lua/ge/extensions/overrides/career/career.lua`

The patch inserted logic into RLS's `updateNodegrabberBlocking()` so that when RedFox forced the grabber on, the `careerNodeGrabberActions` input group was unblocked.

This is now considered **obsolete/unsafe for current RLS** because it replaces an entire RLS core file and can become stale as RLS changes.

### Conclusion

Do not revive the old full `career.lua` override for a public/current build.

---

## 5. RLS Node Grabber blocking mechanism found

In current RLS 2.7.0 / 2.7.0.1, RLS still defines the normal stock node-grabber action group:

```lua
local nodegrabberActions = {
  "nodegrabberGrab",
  "nodegrabberRender",
  "nodegrabberStrength",
  "nodegrabberAction"
}
```

RLS uses the group:

`careerNodeGrabberActions`

In RLS 2.7.0.1 `lua/ge/extensions/overrides/career/career.lua`, the behavior remains approximately:

- Cheats Mode: unblock `careerNodeGrabberActions`
- Normal Career/global-camera/non-walking cases: block `careerNodeGrabberActions` and call `be.nodeGrabber:onMouseButton(false)`
- Other state: unblock the group

This confirms that the current RLS still actively owns the stock Career grabber path.

Important: static inspection alone did **not** prove that simply intercepting this group would be safe or sufficient at runtime.

---

## 6. Narrow input-filter interceptor experiments

A newer compatibility concept stopped replacing `career.lua` and instead wrapped/intercepted only:

`core_input_actionFilter.addAction`

The intended rule was:

- if RedFox grabber is ON
- and RLS requests block=true for `careerNodeGrabberActions`
- forward the same request as block=false
- leave all other input groups untouched

This was much narrower than the old full-file replacement.

### Earlier dev-tool line

Examples included:

- `RedFox_Career_Dev_Tools_v2_0_1_UNPROVEN_TEST.zip`
- `RedFox_Career_Dev_Tools_v2_0_2_NODE_UNLOCK_UNPROVEN_TEST.zip`
- `RedFox_Career_Dev_Tools_v2_0_3_RMOD_NODE_SWITCH_UNPROVEN_TEST.zip`

v2.0.3 used a persistent ON/OFF switch and attempted to preserve RLS blocking when OFF.

### Risks already identified

- global wrapper stacking/reload risk
- load-order interaction with other mods
- RLS may directly release `be.nodeGrabber` in addition to blocking input
- later RLS updates may change group names/flow
- static compatibility does not equal runtime success

---

## 7. RLS Cheats Mode / one-trillion-dollar failure

This is a critical regression that must never be reintroduced.

Toolkit v1.0.12 attempted a one-click grabber by calling:

```lua
career_modules_cheats.enableCheatsMode(true)
```

That was wrong for normal Career use.

RLS 2.7.0/2.7.0.1 `playerAttributes.lua` contains Cheats Mode behavior that forces money to roughly:

`1e12`

It also blocks/overrides normal money changes while cheats mode is active.

RLS persists cheats state in:

`career/rls_career/cheats.json`

with a `cheatsMode` flag.

RLS `cheats.lua` exposes an enable path but no normal symmetric disable path in the inspected code. Therefore once RedFox enabled it, the save/session could remain contaminated and the balance could stay at one trillion.

### v1.0.13 money-safety response

Build:

`RedFox_RLS_Career_Full_Toolkit_v1.0.13_MONEY_SAFETY_Grabber_FIX_TEST.zip`

SHA-256:

`4fbf71218ac1bf34d53b1227ca536cfc592db717bc79b40f89678cec1309a97c`

Changes included:

- removed `enableCheatsMode(true)`
- removed automatic `patchAll()` from extension load
- removed repeating broad `patchAll()` loop
- lifecycle hooks stopped writing money/XP
- manual money controls stayed manual
- grabber attempted only narrow exact-group reassertion
- stale RLS `career.lua` override remained absent

### Rule going forward

**RedFox must never use RLS Cheats Mode just to obtain the Grabber or normal dev-tool UI functions.**

No build should automatically repair/alter a contaminated save unless David explicitly asks for a save-repair operation.

---

## 8. Toolkit UI/menu regression after RLS update

After the new RLS update, the user reported that the full dev-tool menu requests stopped working (Garage, Vehicle Selector, and related menu opens).

Inspection of v1.0.13 showed stale calls such as:

```lua
guihooks.trigger('MenuOpenModule', 'vehicleselect')
```

and older module-opening assumptions.

Current RLS 2.7.x heavily uses:

```lua
extensions.ui_router.navigate(...)
```

Examples found:

- Vehicle selector from pause: `ui_vehicleSelector_general.openFromPause()`
- Vehicle selector route: `pause.vehicleSelector`
- Career inventory: `career.computer.vehicleInventory`
- Part shopping: `career.computer.partShopping`
- Maintenance: `maintenance`

The old generic `MenuOpenModule` approach is therefore stale for many current RLS menus.

### Required dev-tool architecture change

Replace broad/global `patchAll()` logic with **per-feature adapters**:

- Vehicle Selector adapter
- Vehicle Inventory adapter
- Part Shopping adapter
- Maintenance adapter
- Auction adapter
- Vehicle Shopping adapter
- Engine Package/Swap adapter
- Garage/property adapter
- future version-aware compatibility adapter layer

Each adapter should detect the current API and fail visibly/diagnostically rather than silently doing nothing.

---

## 9. Debug-window root cause already found

An empty Dear ImGui "Debug" window appeared in earlier Toolkit builds.

Multiple earlier attempts incorrectly tried to suppress/intercept/remove the window.

The actual root cause was later identified: RedFox called:

`im.SetWindowFontScale()`

before `im.Begin()`.

That caused Dear ImGui to create/fall back to a Debug window.

The correct fix was moving font scaling inside the valid Begin/End window lifecycle.

Do not reintroduce the old window interception hacks.

---

## 10. Standalone fully renamed RedFox Grabber experiments

After the RLS stock-path/interceptor work still caused problems, a fully separate RedFox-named Grabber was proposed so RLS would not see stock action names.

Desired concept:

- own action IDs such as `redfoxCareerGrabber...`
- same physical controls as stock
- no `careerNodeGrabberActions`
- no RLS file override
- no Cheats Mode
- no money/XP/save changes
- own purple/green diagnostic rendering

### v1.1.0 stock-backend compatibility prototype

Built earlier:

`RedFox_Node_Grabber_Unlocker_v1.1.0_BeamNG_0.38_RLS_COMPAT_TEST.zip`

SHA-256:

`8ff4ad9425bf77e6721e5bf73a4177468208802de79d16f0ab6a344ef2a2f710`

This removed the stale `career.lua` override and used a narrow runtime wrapper around the input filter.

Runtime result reported by David:

**The grabber still set off the RLS cheat thing.**

Conclusion: failed for Career-safe use. Do not call this approach safe/working.

### Fully independent RedFox Career Grabber v0.1.0

Built:

`RedFox_Career_Grabber_v0.1.0_RLS_INDEPENDENT_TEST.zip`

SHA-256:

`61e965eb8686b84cd524246b06cc04708111427ca2fe8715094429cd645ac349`

Goal:

- RedFox-only action IDs
- same physical controls
- direct use/probing of BeamNG node backend
- no RLS input-group modification
- no Cheats Mode
- no money/XP/save writes

Problem: it did not provide the requested purple/green visual proof, making the runtime test inconclusive because BeamNG/RLS can already show yellow node dots.

David correctly pointed out that lack of RedFox colors meant there was no reliable way to tell whether RedFox node detection had actually activated.

Runtime observation: a keybind could be assigned, but there was no visible useful result and grabbing did not work. Because the visual proof was missing, this cannot be classified as a complete no-op with certainty.

### v0.2.0 purple/green + diagnostic experiment

Built:

`RedFox_Career_Grabber_v0.2.0_PURPLE_GREEN_WEUI_DIAGNOSTIC_TEST.zip`

SHA-256:

`22cdd22ec3a1b16e25cba2c2f194bb0d6cbe2674ca86cee9ed7ec59cb333db8a`

Intended additions:

- purple RedFox custom node markers
- green hovered node
- bright green active-hover state
- WEUI diagnostic status/counters
- same physical controls

Runtime result from David:

- RedFox could be turned on/off
- still no color change
- still could not grab anything
- expected WEUI diagnostic window did not appear

Important interpretation:

The ON/OFF control proves at least some RedFox action/extension path was alive. It does **not** prove node enumeration, custom rendering, hover detection, or actual grabbing worked.

A v0.2.1 narrow UI-key patch was planned, but the work stalled/froze before a corrected package was completed. Do not treat v0.2.1 as delivered.

---

## 11. BeamNG Investigator / diagnostics experiments

Built previously:

`RedFox_BeamNG_Investigator_v0_2_1_AUTO_UNPROVEN_TEST.zip`

Runtime result:

- scanner ran/collected something
- expected diagnostic ZIP was not created

The standalone investigator/export path was therefore paused. Diagnostic capability should instead be built into the full Dev Tool in a simpler visible way.

Preferred future diagnostics:

- capability scanner
- health/status indicators
- visible API-route status
- version detection
- safe mode
- compatibility log
- one-button environment report
- no dependency on a fragile auto-export ZIP for the first proof

---

## 12. New paid RLS 2.7.0.1 package inspection

The paid update was supplied in split archive parts and reconstructed for analysis.

The reconstructed archive contained roughly 4,955 entries.

Relevant Lua files extracted successfully.

One archive warning was found involving a filename-encoding mismatch in a Synthwave music filename. Therefore the archive reconstruction was usable for source analysis, but should not be described as perfectly pristine.

### Important 2.7.0.1 findings

#### A. Node Grabber restriction still exists

RLS still explicitly blocks/unblocks `careerNodeGrabberActions` and directly releases the engine node grabber in restricted states.

#### B. Cheats Mode remains dangerous

Cheats Mode is still referenced across multiple systems including player attributes/payments/business/shopping/weather-related code. It remains unsuitable as a general RedFox compatibility flag.

#### C. New winch exists

File:

`lua/ge/extensions/rlsYankem.lua`

Header identifies it as a universal vehicle-to-vehicle winch controller.

`M.toggleWinch()` exists in the inspected file.

This should be audited for input-binding conflicts and possible towing interaction with the RedFox Grabber.

#### D. Used-car auction exists

RLS 2.7.0.1 contains a substantial used-car auction system despite the user not hearing it mentioned in the update video.

Relevant files include:

- `career/modules/usedCarAuction.lua`
- `usedCarAuctionLots.lua`
- `usedCarAuctionNpcs.lua`
- `levels/west_coast_usa/auction.filters.json`
- `auction.sites.json`
- auction facility/triggers/assets

#### E. Maintenance expanded

Relevant files:

- `career/modules/maintenanceComputer.lua`
- `maintenanceComputerConfig.lua`
- `maintenanceMode.lua`
- `guides/maintenance-wear-system-report.md`
- `tireSystem.lua`

Maintenance uses the current UI router.

#### F. Engine swapping/packages

File found:

`career/modules/enginePackages.lua`

This needs a deeper functional/API audit before RedFox exposes it through the Dev Tool.

---

## 13. New requested Dev Tool feature — Disable Tow Damage Penalties

David requested a checkbox for new recovery/tow missions so damaged mission vehicles do not deduct money and XP.

Required behavior:

- checkbox such as `Disable Tow Damage Penalties`
- target damage-based deductions only
- preserve normal mission payout
- preserve XP rewards except the damage penalty itself
- preserve mission progression
- preserve damage tracking
- no global payment/playerAttributes override
- no Cheats Mode

Before implementation, inspect the exact RLS 2.7.0.1 recovery/tow mission reward/penalty code and patch only the damage-penalty calculation or hook.

Search/audit terms:

`recovery`, `tow`, `damage`, `penalty`, `xp`, `money`, `payment`, mission reward calculation.

---

## 14. Other Full Toolkit feature history/status

### Photo Manager

Working:

- taking photos
- thumbnail lock

Unresolved:

- custom photo filters did not work reliably

Future requested direction:

- categories
- history/dashboard

### Teleport

Older v1.0.4 did not work.

v1.0.5 attempted a rewrite.

Desired behavior:

- tow/shop destination offset onto usable roadway
- map-marker teleport exact where appropriate
- hauled vehicles/cargo travel too
- eventual cross-map support
- RedFox implementation, not copying another mod's UI

### Insurance

Profile 3 inspection previously showed D-Series inventory IDs 28 and 52 missing insurance records while ID 42 appeared valid.

David explicitly did not want direct save editing.

Dev Tool goal:

- diagnose in-game
- repair through the live game/module APIs if possible
- never silently edit save JSON

Current insurance repair remains unfinished; previous UI sometimes reported unavailable RLS insurance module/getInvVehs paths.

### Career backup/converter ideas

Desired eventual system:

- date-coded ZIP backups
- support RLS / vanilla / Better Career
- manifest/hashes/source paths/dependencies
- dry-run restore
- collision checks
- field-mapped migration/conversion, not blind file copying

### Small Game UI status LED

Planned:

- dark gray = off
- yellow = dev tools active
- green = grabber active
- draggable
- click opens WEUI manager

---

## 15. Current save-safety conclusions

A previous `Profile 3.zip` inspection found autosave1/2/3; autosave2/3 parsed and autosave3 appeared newer/not obviously corrupt.

Do not directly modify Career saves unless explicitly requested.

For any compatibility test that could affect state, use a copied/noncritical profile first.

---

## 16. Recommended implementation order from here

### PHASE 1 — Rebaseline the Full Dev Tool against RLS 2.7.0.1

1. Re-open the newest actual Full Toolkit source package before editing.
2. Inventory every current button/feature and mark:
   - working
   - stale API
   - unsafe
   - unknown
3. Remove/keep removed all broad automatic patching.
4. Confirm no Cheats Mode call exists anywhere in automatic paths.
5. Replace stale menu opens with per-feature current RLS/UI-router adapters.
6. Add a visible WEUI status/capability page with bindable open/close action.
7. Make failures explicit instead of silent.

### PHASE 2 — Restore the Grabber inside the Full Dev Tool

Goal: recover the pre-update practical behavior before expanding features.

1. Compare the last build David remembers working against RLS 2.7.0.1.
2. Trace all current RLS grabber control points, not only `addAction`:
   - action group blocking
   - direct `be.nodeGrabber:onMouseButton(false)` calls
   - camera/walking state hooks
   - any cheats-state checks
   - any newer input/router changes
3. Build a narrow RedFox ON/OFF adapter around the current runtime behavior.
4. Keep the same familiar physical controls.
5. Add diagnostic status in the Dev Tool so David can see:
   - RedFox grabber ON/OFF
   - whether RLS requested block/unblock
   - effective RedFox state
   - whether engine grab backend receives press/release
   - read-only Cheats Mode state
6. Do not call Cheats Mode.
7. Do not modify RLS files.
8. Test on a copied save.

### PHASE 3 — RedFox purple/green visualization

Once actual grabbing works again:

1. Add RedFox-specific overlay renderer.
2. Purple detected/selectable nodes.
3. Green hovered node.
4. Brighter green active-grab state.
5. Ensure stock yellow display can be distinguished from RedFox state.

If the engine does not expose enough information for perfect overlay alignment, document the exact limitation rather than faking a success state.

### PHASE 4 — Repair all major Dev Tool menu functions

Priority adapters:

1. Vehicle Selector
2. Career Vehicle Inventory
3. Part Shopping
4. Maintenance
5. Garage/property functions
6. Vehicle Shopping/dealers
7. Auction
8. Engine packages/swapping
9. Insurance diagnostics/repair

### PHASE 5 — RLS 2.7.0.1-specific enhancements

1. `Disable Tow Damage Penalties` checkbox
2. RLS Yankem/winch compatibility status and optional shortcuts
3. Auction helper access
4. Maintenance helper access
5. Engine-package/swap access
6. current vehicle-shop integration

### PHASE 6 — Remaining Toolkit systems

1. Photo filters/categories/history
2. Teleport rewrite completion
3. Insurance live repair
4. backup/restore/converter
5. draggable Game UI LED
6. environment report/capability scanner

---

## 17. Exact next proof

The next build should be a **Full Dev Tool compatibility rebaseline**, not another blind standalone Grabber guess.

It should contain only enough changes to prove:

1. Dev Tool WEUI opens through a clearly bindable RedFox action.
2. Current RLS version/capabilities are displayed.
3. Vehicle Selector or one current UI-router menu opens correctly.
4. Grabber ON/OFF diagnostics show the current RLS block state without enabling Cheats Mode.
5. Actual grabbing is attempted through the current known-good engine path.
6. Money remains unchanged.
7. RLS Cheats Mode remains false.
8. Save reloads normally.

Only after that proof should multiple other features be repaired in batches.

---

## 18. Known failed / abandoned approaches — do not repeat blindly

- Shipping a stale full RLS `career.lua` override.
- Enabling RLS Cheats Mode for Node Grabber access.
- Broad automatic `patchAll()` loops.
- Automatic money/XP lifecycle writes.
- Claiming a Debug-window fix before runtime proof.
- Trying to suppress the Debug window instead of fixing invalid ImGui call order.
- Treating stock yellow node dots as proof that RedFox node detection works.
- Calling the v0.1.0/v0.2.0 independent Grabber successful when purple/green rendering and grabbing did not work.
- Relying on the failed diagnostic ZIP exporter as the first debugging path.
- Direct save editing for insurance/money unless David explicitly requests it.

---

## 19. Current status summary

**Known:**

- RLS 2.7.0.1 still actively blocks the stock Career Node Grabber.
- RLS Cheats Mode still has dangerous economic side effects.
- old RedFox menu-opening APIs are stale against new RLS UI routing.
- the full Dev Tool needs a compatibility rebaseline.
- the standalone custom Grabber tests have not yet produced working purple/green grabbing.
- RedFox ON/OFF action execution itself worked in the latest standalone test, but node rendering/grabbing and WEUI did not.

**Decision:**

Return to the Full Dev Tool, rebaseline it against RLS 2.7.0.1, restore one current menu route and the Grabber safely, then repair the rest feature-by-feature. Keep the standalone independent Grabber as a fallback/reference branch rather than the primary immediate path.

**Runtime status of next build:** UNTESTED until David tests the exact ZIP.
